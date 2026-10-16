CREATE TABLE users (
    id              TEXT PRIMARY KEY,
    display_name    TEXT NOT NULL CHECK (btrim(display_name) <> ''),
    email           TEXT,
    account_status  TEXT NOT NULL DEFAULT 'active'
                    CHECK (account_status IN ('active', 'inactive')),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE projects (
    id                  TEXT PRIMARY KEY,
    name                TEXT NOT NULL CHECK (btrim(name) <> ''),
    description         TEXT,
    created_by_user_id  TEXT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE project_memberships (
    project_id         TEXT NOT NULL REFERENCES projects(id) ON DELETE RESTRICT,
    user_id            TEXT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    role               TEXT NOT NULL CHECK (role IN ('student', 'student_lead', 'faculty')),
    membership_status  TEXT NOT NULL DEFAULT 'active'
                       CHECK (membership_status IN ('active', 'inactive')),
    joined_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (project_id, user_id)
);

CREATE TABLE workflow_sections (
    id           TEXT PRIMARY KEY,
    project_id   TEXT NOT NULL REFERENCES projects(id) ON DELETE RESTRICT,
    name         TEXT NOT NULL CHECK (btrim(name) <> ''),
    position     INTEGER NOT NULL CHECK (position > 0),
    is_initial   BOOLEAN NOT NULL DEFAULT FALSE,
    is_terminal  BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE (project_id, name),
    UNIQUE (project_id, position),
    UNIQUE (id, project_id)
);

CREATE TABLE workflow_transitions (
    id               TEXT PRIMARY KEY,
    project_id       TEXT NOT NULL REFERENCES projects(id) ON DELETE RESTRICT,
    from_section_id  TEXT NOT NULL,
    to_section_id    TEXT NOT NULL,
    name             TEXT,
    is_enabled       BOOLEAN NOT NULL DEFAULT TRUE,
    CHECK (from_section_id <> to_section_id),
    UNIQUE (project_id, from_section_id, to_section_id),
    FOREIGN KEY (from_section_id, project_id)
        REFERENCES workflow_sections(id, project_id) ON DELETE RESTRICT,
    FOREIGN KEY (to_section_id, project_id)
        REFERENCES workflow_sections(id, project_id) ON DELETE RESTRICT
);

CREATE TABLE tasks (
    id                  TEXT PRIMARY KEY,
    project_id          TEXT NOT NULL REFERENCES projects(id) ON DELETE RESTRICT,
    section_id          TEXT NOT NULL,
    title               TEXT NOT NULL CHECK (btrim(title) <> ''),
    description         TEXT,
    owner_user_id       TEXT,
    priority            TEXT CHECK (priority IN ('low', 'medium', 'high')),
    position            INTEGER,
    created_by_user_id  TEXT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    version             INTEGER NOT NULL DEFAULT 1 CHECK (version > 0),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    FOREIGN KEY (section_id, project_id)
        REFERENCES workflow_sections(id, project_id) ON DELETE RESTRICT,
    FOREIGN KEY (project_id, owner_user_id)
        REFERENCES project_memberships(project_id, user_id) ON DELETE RESTRICT,
    FOREIGN KEY (project_id, created_by_user_id)
        REFERENCES project_memberships(project_id, user_id) ON DELETE RESTRICT
);

CREATE TABLE task_history_events (
    id               TEXT PRIMARY KEY,
    task_id          TEXT NOT NULL REFERENCES tasks(id) ON DELETE RESTRICT,
    actor_user_id    TEXT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    event_type       TEXT NOT NULL,
    from_section_id  TEXT REFERENCES workflow_sections(id) ON DELETE RESTRICT,
    to_section_id    TEXT REFERENCES workflow_sections(id) ON DELETE RESTRICT,
    details          JSONB,
    task_version     INTEGER NOT NULL,
    occurred_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE task_creation_requests (
    project_id       TEXT NOT NULL REFERENCES projects(id) ON DELETE RESTRICT,
    user_id          TEXT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    idempotency_key  TEXT NOT NULL,
    request_hash     TEXT NOT NULL,
    task_id          TEXT NOT NULL REFERENCES tasks(id) ON DELETE RESTRICT,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (project_id, user_id, idempotency_key)
);

CREATE INDEX idx_memberships_user_status
    ON project_memberships(user_id, membership_status);
CREATE INDEX idx_sections_project_position
    ON workflow_sections(project_id, position);
CREATE INDEX idx_tasks_project_section
    ON tasks(project_id, section_id, created_at);
CREATE INDEX idx_task_history_order
    ON task_history_events(task_id, occurred_at);
