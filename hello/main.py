import json
import logging
import os
import urllib.error
import urllib.request
from contextlib import asynccontextmanager
from pathlib import Path

import psycopg
from fastapi import FastAPI, Header, HTTPException, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field, field_validator

from greetings import APP_VERSION, GREETINGS, get_greeting
from kanban_dao import KanbanDAO
from notes_dao import NotesDAO

log = logging.getLogger("uvicorn.error")

# URL of the internal `time` sidecar defined in docker-compose.yaml. `time`
# is the Compose service name — Docker's built-in DNS on the compose network
# resolves it to the sidecar container. Only THIS app is Traefik-routed and
# public; `time` is internal-only.
TIME_SERVICE_URL = "http://time:8001"

# Postgres connection string, injected via docker-compose.yaml. Same
# service-name-as-DNS pattern — `db` resolves to the postgres sidecar
# container on the Compose network. Never publicly reachable.
DATABASE_URL = os.environ.get("DATABASE_URL")

# All Postgres access goes through the DAO. Routes below stay thin — they
# handle HTTP framing (status codes, error mapping) and delegate the
# actual SQL to NotesDAO methods.
notes_dao = NotesDAO(DATABASE_URL or "")
kanban_dao = KanbanDAO(DATABASE_URL or "")

# Env-gated admin reset endpoint. Off by default — students opt in via
# ALLOW_ADMIN_RESET=true in the environment (docker-compose.override.yml
# sets it for local; in Coolify you'd add it to the Application's env
# vars, use /admin/reset, then remove it).
ADMIN_RESET_ENABLED = os.environ.get("ALLOW_ADMIN_RESET", "").lower() in (
    "1",
    "true",
    "yes",
)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Startup: apply any pending schema migrations.

    Reads hello/migrations/*.sql, runs each file whose name isn't
    already recorded in the `_migrations` tracking table, records
    the newly-applied ones. Same code runs on staging AND production
    on every deploy, so schema stays in sync across environments
    automatically.

    See hello/notes_dao.py apply_migrations() for the implementation.

    OperationalError (db not reachable) is swallowed so /health can
    still respond during a partial outage; /notes will surface 503
    on request.
    """
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is required; see .env.example")
    try:
        notes_dao.apply_migrations()
    except psycopg.OperationalError as e:
        log.warning("startup: db unreachable, skipping migrations: %s", e)
    yield


STATIC_DIR = Path(__file__).parent / "static"
app = FastAPI(title="Kanban Lite", version="0.1.0", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class HealthResponse(BaseModel):
    ok: bool
    version: str


class NoteIn(BaseModel):
    body: str


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/demo/hello")
def hello(lang: str = "en"):
    return {"hello": get_greeting(lang)}


@app.get("/languages")
def languages():
    return {"supported": sorted(GREETINGS.keys())}


@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(ok=True, version=APP_VERSION)


@app.get("/ready", response_model=HealthResponse)
def readiness():
    try:
        kanban_dao.ping()
    except psycopg.OperationalError as e:
        raise HTTPException(status_code=503, detail="database is not ready") from e
    return HealthResponse(ok=True, version=APP_VERSION)


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class UserCreate(StrictModel):
    display_name: str = Field(min_length=1, max_length=120)
    email: str | None = Field(default=None, max_length=320)

    @field_validator("display_name")
    @classmethod
    def display_name_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("display name is required")
        return value.strip()


class ProjectCreate(StrictModel):
    name: str = Field(min_length=1, max_length=160)
    description: str | None = Field(default=None, max_length=2000)

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("project name is required")
        return value.strip()


class TaskCreate(StrictModel):
    title: str = Field(min_length=1, max_length=240)
    description: str | None = Field(default=None, max_length=10000)
    section_id: str
    owner_user_id: str | None = None
    priority: str | None = Field(default=None, pattern="^(low|medium|high)$")

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("task title is required")
        return value.strip()


class TaskTransition(StrictModel):
    to_section_id: str
    expected_task_version: int = Field(ge=1)


def current_user_id(x_user_id: str | None = Header(default=None)) -> str:
    """Temporary local identity boundary pending the authentication decision."""
    if not x_user_id:
        raise HTTPException(status_code=401, detail="X-User-ID header is required")
    return x_user_id


def map_data_error(error: Exception):
    if isinstance(error, PermissionError):
        raise HTTPException(status_code=403, detail=str(error)) from error
    if isinstance(error, LookupError):
        raise HTTPException(status_code=404, detail=str(error)) from error
    if isinstance(error, ValueError):
        raise HTTPException(status_code=409, detail=str(error)) from error
    if isinstance(error, psycopg.OperationalError):
        raise HTTPException(status_code=503, detail="database is unavailable") from error
    raise error


@app.post("/api/v1/users", status_code=201)
def create_user(body: UserCreate):
    try:
        return kanban_dao.create_user(body.display_name, body.email)
    except Exception as error:
        map_data_error(error)


@app.get("/api/v1/users/{user_id}")
def get_user(user_id: str):
    try:
        user = kanban_dao.get_user(user_id)
    except Exception as error:
        map_data_error(error)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


@app.post("/api/v1/projects", status_code=201)
def create_project(body: ProjectCreate, x_user_id: str | None = Header(default=None)):
    user_id = current_user_id(x_user_id)
    try:
        return kanban_dao.create_project(user_id, body.name, body.description)
    except Exception as error:
        map_data_error(error)


@app.get("/api/v1/projects")
def list_projects(x_user_id: str | None = Header(default=None)):
    user_id = current_user_id(x_user_id)
    try:
        return {"items": kanban_dao.list_projects(user_id), "next_cursor": None}
    except Exception as error:
        map_data_error(error)


@app.get("/api/v1/projects/{project_id}/board")
def get_board(project_id: str, x_user_id: str | None = Header(default=None)):
    user_id = current_user_id(x_user_id)
    try:
        return kanban_dao.get_board(project_id, user_id)
    except Exception as error:
        map_data_error(error)


@app.post("/api/v1/projects/{project_id}/tasks", status_code=201)
def create_task(
    project_id: str,
    body: TaskCreate,
    response: Response,
    x_user_id: str | None = Header(default=None),
    idempotency_key: str | None = Header(default=None),
):
    user_id = current_user_id(x_user_id)
    if not idempotency_key or not idempotency_key.strip():
        raise HTTPException(status_code=400, detail="Idempotency-Key header is required")
    try:
        task, replayed = kanban_dao.create_task(
            project_id,
            user_id,
            idempotency_key,
            body.model_dump(mode="json"),
        )
    except Exception as error:
        map_data_error(error)
    if replayed:
        response.status_code = 200
        response.headers["Idempotency-Replayed"] = "true"
    return task


@app.get("/api/v1/projects/{project_id}/tasks/{task_id}")
def get_task(
    project_id: str,
    task_id: str,
    x_user_id: str | None = Header(default=None),
):
    user_id = current_user_id(x_user_id)
    try:
        task = kanban_dao.get_task(project_id, task_id, user_id)
    except Exception as error:
        map_data_error(error)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    return task


@app.post("/api/v1/projects/{project_id}/tasks/{task_id}/transitions")
def transition_task(
    project_id: str,
    task_id: str,
    body: TaskTransition,
    x_user_id: str | None = Header(default=None),
):
    user_id = current_user_id(x_user_id)
    try:
        return kanban_dao.transition_task(
            project_id,
            task_id,
            user_id,
            body.to_section_id,
            body.expected_task_version,
        )
    except Exception as error:
        map_data_error(error)


@app.get("/time")
def current_time():
    """Fetch the current UTC time from the internal `time` sidecar."""
    try:
        with urllib.request.urlopen(f"{TIME_SERVICE_URL}/now", timeout=3) as resp:
            body = json.loads(resp.read())
        return {"from_time_service": body}
    except urllib.error.URLError as e:
        return {"error": "time service unreachable", "detail": str(e)}


@app.get("/notes")
def list_notes():
    try:
        return notes_dao.list_all()
    except psycopg.OperationalError as e:
        raise HTTPException(status_code=503, detail=f"db unreachable: {e}") from e


@app.post("/notes", status_code=201)
def create_note(note: NoteIn):
    try:
        return notes_dao.insert(note.body)
    except psycopg.OperationalError as e:
        raise HTTPException(status_code=503, detail=f"db unreachable: {e}") from e


@app.post("/admin/reset")
def admin_reset():
    """Drop and recreate the notes table. Destructive.

    Env-gated by ALLOW_ADMIN_RESET so you can't hit this by accident
    on a production Application. To use in Coolify: add
    ALLOW_ADMIN_RESET=true to the Application's Environment Variables,
    redeploy, POST here, then remove the env var. In local dev
    docker-compose.override.yml enables it by default.
    """
    if not ADMIN_RESET_ENABLED:
        raise HTTPException(
            status_code=403,
            detail="admin reset disabled; set ALLOW_ADMIN_RESET=true to enable",
        )
    try:
        notes_dao.reset()
    except psycopg.OperationalError as e:
        raise HTTPException(status_code=503, detail=f"db unreachable: {e}") from e
    return {"ok": True, "message": "notes table dropped and recreated (empty)"}
