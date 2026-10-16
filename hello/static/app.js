const state = {
  userId: localStorage.getItem("kanban.userId"),
  projects: [],
  projectId: localStorage.getItem("kanban.projectId"),
  board: null,
  draggedTaskId: null,
};

const $ = (selector) => document.querySelector(selector);
const message = (text = "") => { $("#message").textContent = text; };

async function api(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (state.userId) headers["X-User-ID"] = state.userId;
  const response = await fetch(path, { ...options, headers });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body.detail || "The request could not be completed.");
  return body;
}

function setBusy(form, busy) {
  form.querySelectorAll("button, input, textarea, select").forEach((item) => item.disabled = busy);
}

async function initialize() {
  const signedIn = Boolean(state.userId);
  $("#identity-view").hidden = signedIn;
  $("#workspace").hidden = !signedIn;
  $("#change-user").hidden = !signedIn;
  if (!signedIn) return;
  try {
    await loadProjects();
  } catch (error) {
    message(error.message);
  }
}

async function loadProjects() {
  const data = await api("/api/v1/projects");
  state.projects = data.items;
  if (!state.projects.some((project) => project.id === state.projectId)) {
    state.projectId = state.projects[0]?.id || null;
  }
  localStorage.setItem("kanban.projectId", state.projectId || "");
  const select = $("#project-select");
  select.replaceChildren(...state.projects.map((project) => {
    const option = document.createElement("option");
    option.value = project.id;
    option.textContent = project.name;
    option.selected = project.id === state.projectId;
    return option;
  }));
  $("#empty").hidden = state.projects.length > 0;
  $("#new-task").disabled = !state.projectId;
  if (state.projectId) await loadBoard();
  else $("#board").replaceChildren();
}

async function loadBoard() {
  state.board = await api(`/api/v1/projects/${state.projectId}/board`);
  const columns = state.board.sections.map((section) => {
    const column = document.createElement("section");
    column.className = "column";
    column.dataset.sectionId = section.id;
    column.addEventListener("dragover", (event) => {
      if (canMoveTo(state.draggedTaskId, section.id)) {
        event.preventDefault();
        event.dataTransfer.dropEffect = "move";
        column.classList.add("drag-over");
      }
    });
    column.addEventListener("dragleave", () => column.classList.remove("drag-over"));
    column.addEventListener("drop", async (event) => {
      event.preventDefault();
      column.classList.remove("drag-over");
      const task = findTask(state.draggedTaskId);
      if (task) await moveTask(task, section.id);
    });
    const heading = document.createElement("h2");
    heading.append(document.createTextNode(section.name));
    const count = document.createElement("span");
    count.className = "count";
    count.textContent = section.tasks.length;
    heading.append(count);
    column.append(heading, ...section.tasks.map(taskCard));
    return column;
  });
  $("#board").replaceChildren(...columns);
  message();
}

function taskCard(task) {
  const card = document.createElement("article");
  card.className = `card priority-${task.priority || "none"}`;
  card.draggable = true;
  card.dataset.taskId = task.id;
  card.addEventListener("dragstart", (event) => {
    state.draggedTaskId = task.id;
    event.dataTransfer.effectAllowed = "move";
    event.dataTransfer.setData("text/plain", task.id);
    card.classList.add("is-dragging");
  });
  card.addEventListener("dragend", () => {
    state.draggedTaskId = null;
    card.classList.remove("is-dragging");
    document.querySelectorAll(".drag-over").forEach((item) => item.classList.remove("drag-over"));
  });
  const title = document.createElement("h3");
  title.textContent = task.title;
  const meta = document.createElement("p");
  meta.className = "meta";
  meta.textContent = [task.priority, task.owner?.display_name].filter(Boolean).join(" · ") || "Unassigned";
  card.append(title, meta);
  const nextSection = sectionAfter(task.section_id);
  if (nextSection) {
    const move = document.createElement("button");
    move.type = "button";
    move.className = "move-task";
    move.textContent = `Move to ${nextSection.name} →`;
    move.addEventListener("click", () => moveTask(task, nextSection.id));
    card.append(move);
  }
  return card;
}

function findTask(taskId) {
  for (const section of state.board?.sections || []) {
    const task = section.tasks.find((candidate) => candidate.id === taskId);
    if (task) return task;
  }
  return null;
}

function sectionAfter(sectionId) {
  const index = state.board?.sections.findIndex((section) => section.id === sectionId) ?? -1;
  return index >= 0 ? state.board.sections[index + 1] || null : null;
}

function canMoveTo(taskId, sectionId) {
  const task = findTask(taskId);
  return Boolean(task && sectionAfter(task.section_id)?.id === sectionId);
}

async function moveTask(task, toSectionId) {
  message("Moving task…");
  try {
    await api(`/api/v1/projects/${state.projectId}/tasks/${task.id}/transitions`, {
      method: "POST",
      body: JSON.stringify({
        to_section_id: toSectionId,
        expected_task_version: task.version,
      }),
    });
    await loadBoard();
  } catch (error) {
    await loadBoard().catch(() => {});
    message(error.message);
  }
}

$("#identity-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const values = Object.fromEntries(new FormData(form));
  if (!values.email) values.email = null;
  setBusy(form, true);
  try {
    const user = await api("/api/v1/users", { method: "POST", body: JSON.stringify(values) });
    state.userId = user.id;
    localStorage.setItem("kanban.userId", user.id);
    form.reset();
    await initialize();
  } catch (error) { message(error.message); }
  finally { setBusy(form, false); }
});

$("#project-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const values = Object.fromEntries(new FormData(form));
  if (!values.description) values.description = null;
  setBusy(form, true);
  try {
    const project = await api("/api/v1/projects", { method: "POST", body: JSON.stringify(values) });
    state.projectId = project.id;
    form.reset();
    form.hidden = true;
    await loadProjects();
  } catch (error) { message(error.message); }
  finally { setBusy(form, false); }
});

$("#task-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const values = Object.fromEntries(new FormData(form));
  values.description ||= null;
  values.priority ||= null;
  values.owner_user_id = null;
  values.section_id = state.board.sections[0].id;
  setBusy(form, true);
  try {
    await api(`/api/v1/projects/${state.projectId}/tasks`, {
      method: "POST",
      headers: { "Idempotency-Key": crypto.randomUUID() },
      body: JSON.stringify(values),
    });
    form.reset();
    form.hidden = true;
    await loadBoard();
  } catch (error) { message(error.message); }
  finally { setBusy(form, false); }
});

$("#project-select").addEventListener("change", async (event) => {
  state.projectId = event.target.value;
  localStorage.setItem("kanban.projectId", state.projectId);
  try { await loadBoard(); } catch (error) { message(error.message); }
});
$("#new-project").addEventListener("click", () => $("#project-form").hidden = false);
$("#new-task").addEventListener("click", () => $("#task-form").hidden = false);
$("#refresh").addEventListener("click", () => loadBoard().catch((error) => message(error.message)));
document.querySelectorAll(".cancel").forEach((button) => button.addEventListener("click", () => button.closest("form").hidden = true));
$("#change-user").addEventListener("click", () => {
  localStorage.removeItem("kanban.userId");
  localStorage.removeItem("kanban.projectId");
  location.reload();
});

initialize();
