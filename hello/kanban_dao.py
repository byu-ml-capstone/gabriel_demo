"""PostgreSQL data access for the Kanban Lite first implementation slice."""

import hashlib
import json
from uuid import uuid4

import psycopg
from psycopg.rows import dict_row


DEFAULT_SECTIONS = (
    ("Backlog", True, False),
    ("In Progress", False, False),
    ("Review", False, False),
    ("Done", False, True),
)


def _id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex}"


def _iso(value):
    return value.isoformat().replace("+00:00", "Z") if value else None


class KanbanDAO:
    def __init__(self, database_url: str):
        self.database_url = database_url

    def ping(self) -> None:
        with psycopg.connect(self.database_url) as conn, conn.cursor() as cur:
            cur.execute("SELECT 1")

    def create_user(self, display_name: str, email: str | None) -> dict:
        user_id = _id("usr")
        with psycopg.connect(self.database_url, row_factory=dict_row) as conn:
            row = conn.execute(
                """INSERT INTO users (id, display_name, email)
                   VALUES (%s, %s, %s)
                   RETURNING id, display_name, email, account_status,
                             created_at, updated_at""",
                (user_id, display_name.strip(), email),
            ).fetchone()
        return self._user(row)

    def get_user(self, user_id: str) -> dict | None:
        with psycopg.connect(self.database_url, row_factory=dict_row) as conn:
            row = conn.execute(
                """SELECT id, display_name, email, account_status,
                          created_at, updated_at
                   FROM users WHERE id = %s""",
                (user_id,),
            ).fetchone()
        return self._user(row) if row else None

    def create_project(self, user_id: str, name: str, description: str | None) -> dict:
        project_id = _id("prj")
        section_ids = [_id("sec") for _ in DEFAULT_SECTIONS]
        with psycopg.connect(self.database_url, row_factory=dict_row) as conn:
            user = conn.execute(
                "SELECT id FROM users WHERE id = %s AND account_status = 'active'",
                (user_id,),
            ).fetchone()
            if not user:
                raise LookupError("current user not found")

            project = conn.execute(
                """INSERT INTO projects (id, name, description, created_by_user_id)
                   VALUES (%s, %s, %s, %s)
                   RETURNING id, name, description, created_by_user_id,
                             created_at, updated_at""",
                (project_id, name.strip(), description, user_id),
            ).fetchone()
            conn.execute(
                """INSERT INTO project_memberships
                       (project_id, user_id, role)
                   VALUES (%s, %s, 'student_lead')""",
                (project_id, user_id),
            )
            for position, ((section_name, initial, terminal), section_id) in enumerate(
                zip(DEFAULT_SECTIONS, section_ids), start=1
            ):
                conn.execute(
                    """INSERT INTO workflow_sections
                           (id, project_id, name, position, is_initial, is_terminal)
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (section_id, project_id, section_name, position, initial, terminal),
                )
            for source, destination in zip(section_ids, section_ids[1:]):
                conn.execute(
                    """INSERT INTO workflow_transitions
                           (id, project_id, from_section_id, to_section_id, name)
                       VALUES (%s, %s, %s, %s, %s)""",
                    (
                        _id("trn"), project_id, source, destination,
                        "Move to next section",
                    ),
                )
        return {
            **self._project(project),
            "current_user_role": "student_lead",
        }

    def list_projects(self, user_id: str) -> list[dict]:
        with psycopg.connect(self.database_url, row_factory=dict_row) as conn:
            rows = conn.execute(
                """SELECT p.id, p.name, p.description, pm.role AS current_user_role,
                          p.updated_at
                   FROM projects p
                   JOIN project_memberships pm ON pm.project_id = p.id
                   WHERE pm.user_id = %s AND pm.membership_status = 'active'
                   ORDER BY p.updated_at DESC, p.id""",
                (user_id,),
            ).fetchall()
        return [
            {**dict(row), "updated_at": _iso(row["updated_at"])} for row in rows
        ]

    def get_board(self, project_id: str, user_id: str) -> dict:
        with psycopg.connect(self.database_url, row_factory=dict_row) as conn:
            self._require_membership(conn, project_id, user_id)
            sections = conn.execute(
                """SELECT id, name, position
                   FROM workflow_sections
                   WHERE project_id = %s ORDER BY position""",
                (project_id,),
            ).fetchall()
            tasks = conn.execute(
                """SELECT t.id, t.title, t.section_id, t.priority, t.version,
                          t.updated_at, u.id AS owner_id,
                          u.display_name AS owner_display_name
                   FROM tasks t
                   LEFT JOIN users u ON u.id = t.owner_user_id
                   WHERE t.project_id = %s
                   ORDER BY t.position NULLS LAST, t.created_at, t.id""",
                (project_id,),
            ).fetchall()

        grouped = {section["id"]: [] for section in sections}
        for task in tasks:
            grouped[task["section_id"]].append(
                {
                    "id": task["id"],
                    "title": task["title"],
                    "section_id": task["section_id"],
                    "owner": (
                        {"id": task["owner_id"], "display_name": task["owner_display_name"]}
                        if task["owner_id"] else None
                    ),
                    "priority": task["priority"],
                    "is_blocked": False,
                    "active_blocker_count": 0,
                    "version": task["version"],
                    "updated_at": _iso(task["updated_at"]),
                }
            )
        return {
            "project_id": project_id,
            "board_version": sum(task["version"] for task in tasks),
            "as_of": _iso(self._now()),
            "sections": [
                {**dict(section), "tasks": grouped[section["id"]]}
                for section in sections
            ],
        }

    def create_task(
        self,
        project_id: str,
        user_id: str,
        idempotency_key: str,
        payload: dict,
    ) -> tuple[dict, bool]:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        request_hash = hashlib.sha256(canonical.encode()).hexdigest()
        with psycopg.connect(self.database_url, row_factory=dict_row) as conn:
            self._require_membership(conn, project_id, user_id)
            prior = conn.execute(
                """SELECT request_hash, task_id FROM task_creation_requests
                   WHERE project_id = %s AND user_id = %s AND idempotency_key = %s""",
                (project_id, user_id, idempotency_key),
            ).fetchone()
            if prior:
                if prior["request_hash"] != request_hash:
                    raise ValueError("idempotency key was already used for another request")
                return self._get_task(conn, project_id, prior["task_id"]), True

            section = conn.execute(
                """SELECT id, name FROM workflow_sections
                   WHERE id = %s AND project_id = %s AND is_initial = TRUE""",
                (payload["section_id"], project_id),
            ).fetchone()
            if not section:
                raise LookupError("initial workflow section not found")
            owner_id = payload.get("owner_user_id")
            if owner_id:
                self._require_membership(conn, project_id, owner_id)

            task_id = _id("tsk")
            task = conn.execute(
                """INSERT INTO tasks
                       (id, project_id, section_id, title, description,
                        owner_user_id, priority, created_by_user_id)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                   RETURNING *""",
                (
                    task_id, project_id, payload["section_id"], payload["title"].strip(),
                    payload.get("description"), owner_id, payload.get("priority"), user_id,
                ),
            ).fetchone()
            conn.execute(
                """INSERT INTO task_history_events
                       (id, task_id, actor_user_id, event_type, to_section_id,
                        details, task_version)
                   VALUES (%s, %s, %s, 'created', %s, %s, 1)""",
                (
                    _id("evt"), task_id, user_id, payload["section_id"],
                    json.dumps({"title": payload["title"].strip()}),
                ),
            )
            conn.execute(
                """INSERT INTO task_creation_requests
                       (project_id, user_id, idempotency_key, request_hash, task_id)
                   VALUES (%s, %s, %s, %s, %s)""",
                (project_id, user_id, idempotency_key, request_hash, task_id),
            )
            result = self._task(task, section)
        return result, False

    def get_task(self, project_id: str, task_id: str, user_id: str) -> dict | None:
        with psycopg.connect(self.database_url, row_factory=dict_row) as conn:
            self._require_membership(conn, project_id, user_id)
            return self._get_task(conn, project_id, task_id)

    def transition_task(
        self,
        project_id: str,
        task_id: str,
        user_id: str,
        to_section_id: str,
        expected_version: int,
    ) -> dict:
        """Move a task through an enabled transition and record one history event."""
        with psycopg.connect(self.database_url, row_factory=dict_row) as conn:
            self._require_membership(conn, project_id, user_id)
            current = conn.execute(
                """SELECT t.*, s.name AS section_name
                   FROM tasks t
                   JOIN workflow_sections s ON s.id = t.section_id
                   WHERE t.project_id = %s AND t.id = %s
                   FOR UPDATE OF t""",
                (project_id, task_id),
            ).fetchone()
            if not current:
                raise LookupError("task not found")
            if current["version"] != expected_version:
                raise ValueError(
                    f"task version conflict: expected {expected_version}, "
                    f"current version is {current['version']}"
                )

            transition = conn.execute(
                """SELECT wt.id, wt.from_section_id, wt.to_section_id,
                          destination.name AS to_section_name
                   FROM workflow_transitions wt
                   JOIN workflow_sections destination
                     ON destination.id = wt.to_section_id
                   WHERE wt.project_id = %s
                     AND wt.from_section_id = %s
                     AND wt.to_section_id = %s
                     AND wt.is_enabled = TRUE""",
                (project_id, current["section_id"], to_section_id),
            ).fetchone()
            if not transition:
                raise ValueError("task may only move to the next workflow section")

            updated = conn.execute(
                """UPDATE tasks
                   SET section_id = %s, version = version + 1, updated_at = NOW()
                   WHERE id = %s AND project_id = %s AND version = %s
                   RETURNING *""",
                (to_section_id, task_id, project_id, expected_version),
            ).fetchone()
            if not updated:
                raise ValueError("task changed while the move was being saved")

            history_id = _id("evt")
            conn.execute(
                """INSERT INTO task_history_events
                       (id, task_id, actor_user_id, event_type,
                        from_section_id, to_section_id, details, task_version)
                   VALUES (%s, %s, %s, 'moved', %s, %s, %s, %s)""",
                (
                    history_id,
                    task_id,
                    user_id,
                    current["section_id"],
                    to_section_id,
                    json.dumps({"transition_id": transition["id"]}),
                    updated["version"],
                ),
            )

        return {
            "task": self._task(
                updated,
                {"id": to_section_id, "name": transition["to_section_name"]},
            ),
            "transition": {
                "id": transition["id"],
                "from_section_id": transition["from_section_id"],
                "to_section_id": transition["to_section_id"],
            },
            "history_event_id": history_id,
        }

    @staticmethod
    def _require_membership(conn, project_id: str, user_id: str) -> None:
        member = conn.execute(
            """SELECT 1 FROM project_memberships
               WHERE project_id = %s AND user_id = %s
                 AND membership_status = 'active'""",
            (project_id, user_id),
        ).fetchone()
        if not member:
            raise PermissionError("active project membership required")

    def _get_task(self, conn, project_id: str, task_id: str) -> dict | None:
        task = conn.execute(
            """SELECT t.*, s.name AS section_name
               FROM tasks t JOIN workflow_sections s ON s.id = t.section_id
               WHERE t.project_id = %s AND t.id = %s""",
            (project_id, task_id),
        ).fetchone()
        return self._task(task, {"id": task["section_id"], "name": task["section_name"]}) if task else None

    @staticmethod
    def _now():
        from datetime import datetime, timezone
        return datetime.now(timezone.utc)

    @staticmethod
    def _user(row: dict) -> dict:
        return {
            **dict(row),
            "created_at": _iso(row["created_at"]),
            "updated_at": _iso(row["updated_at"]),
        }

    @staticmethod
    def _project(row: dict) -> dict:
        return {
            **dict(row),
            "created_at": _iso(row["created_at"]),
            "updated_at": _iso(row["updated_at"]),
        }

    @staticmethod
    def _task(row: dict, section: dict) -> dict:
        return {
            "id": row["id"],
            "project_id": row["project_id"],
            "section": dict(section),
            "title": row["title"],
            "description": row["description"],
            "owner_user_id": row["owner_user_id"],
            "priority": row["priority"],
            "is_blocked": False,
            "active_blocker_count": 0,
            "version": row["version"],
            "created_by_user_id": row["created_by_user_id"],
            "created_at": _iso(row["created_at"]),
            "updated_at": _iso(row["updated_at"]),
        }
