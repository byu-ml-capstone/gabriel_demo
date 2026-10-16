from unittest.mock import patch

from fastapi.testclient import TestClient

import main
from main import app


client = TestClient(app)
USER_HEADERS = {"X-User-ID": "usr_test"}


def test_project_routes_require_local_identity():
    response = client.get("/api/v1/projects")
    assert response.status_code == 401


def test_create_user_validates_blank_name():
    response = client.post("/api/v1/users", json={"display_name": "  "})
    assert response.status_code == 422


def test_create_project_provisions_through_dao():
    expected = {"id": "prj_test", "name": "Capstone", "current_user_role": "student_lead"}
    with patch.object(main.kanban_dao, "create_project", return_value=expected) as create:
        response = client.post(
            "/api/v1/projects",
            headers=USER_HEADERS,
            json={"name": "Capstone", "description": None},
        )
    assert response.status_code == 201
    assert response.json() == expected
    create.assert_called_once_with("usr_test", "Capstone", None)


def test_board_returns_shared_snapshot():
    expected = {
        "project_id": "prj_test",
        "board_version": 0,
        "as_of": "2026-10-15T00:00:00Z",
        "sections": [],
    }
    with patch.object(main.kanban_dao, "get_board", return_value=expected):
        response = client.get("/api/v1/projects/prj_test/board", headers=USER_HEADERS)
    assert response.status_code == 200
    assert response.json() == expected


def test_task_creation_requires_idempotency_key():
    response = client.post(
        "/api/v1/projects/prj_test/tasks",
        headers=USER_HEADERS,
        json={"title": "First task", "section_id": "sec_backlog"},
    )
    assert response.status_code == 400


def test_replayed_task_creation_returns_existing_task():
    task = {"id": "tsk_test", "title": "First task"}
    with patch.object(main.kanban_dao, "create_task", return_value=(task, True)):
        response = client.post(
            "/api/v1/projects/prj_test/tasks",
            headers={**USER_HEADERS, "Idempotency-Key": "request-1"},
            json={"title": "First task", "section_id": "sec_backlog"},
        )
    assert response.status_code == 200
    assert response.headers["Idempotency-Replayed"] == "true"
    assert response.json() == task


def test_transition_moves_task_through_dao():
    expected = {
        "task": {"id": "tsk_test", "version": 2},
        "transition": {
            "id": "trn_test",
            "from_section_id": "sec_backlog",
            "to_section_id": "sec_progress",
        },
        "history_event_id": "evt_test",
    }
    with patch.object(main.kanban_dao, "transition_task", return_value=expected) as move:
        response = client.post(
            "/api/v1/projects/prj_test/tasks/tsk_test/transitions",
            headers=USER_HEADERS,
            json={"to_section_id": "sec_progress", "expected_task_version": 1},
        )
    assert response.status_code == 200
    assert response.json() == expected
    move.assert_called_once_with(
        "prj_test", "tsk_test", "usr_test", "sec_progress", 1
    )


def test_transition_conflict_is_visible():
    with patch.object(
        main.kanban_dao,
        "transition_task",
        side_effect=ValueError("task version conflict: expected 1, current version is 2"),
    ):
        response = client.post(
            "/api/v1/projects/prj_test/tasks/tsk_test/transitions",
            headers=USER_HEADERS,
            json={"to_section_id": "sec_progress", "expected_task_version": 1},
        )
    assert response.status_code == 409
    assert "current version is 2" in response.json()["detail"]


def test_transition_rejects_invalid_version():
    response = client.post(
        "/api/v1/projects/prj_test/tasks/tsk_test/transitions",
        headers=USER_HEADERS,
        json={"to_section_id": "sec_progress", "expected_task_version": 0},
    )
    assert response.status_code == 422
