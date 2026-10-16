# Engineering Workflow Product Specification

> **Document status:** Living specification  
> **Current milestone:** C04 product research and scope  
> **Product name:** _Open question_

Use this document to record product decisions from research through implementation. It should be specific enough that a teammate—or an AI coding assistant—can implement the intended behavior without inventing important details.

## How to Use This Specification

| Milestone | Expected work |
| --- | --- |
| **C04** | Complete product research, stakeholder, pattern, MVP, and exclusion decisions. |
| **Class 4 workshop** | Turn the research into workflows, requirements, a domain model, and initial API contracts. |
| **C06** | Complete the specification and submit it as `docs/product-specification.md`. |
| **Before implementation** | Review the specification with AI, resolve contradictions, and record decisions instead of letting the assistant silently choose. |

> [!IMPORTANT]
> Mark unresolved decisions as **Open question** or **Assumption**. Do not present an AI suggestion as a settled requirement.

---

## 1. Product Vision

> **CRISP-DM connection — Business Understanding:** Define the problem, stakeholders, purpose, and measurable success before choosing a technical solution.

### Product Name

Kanban Lite

### Problem Statement

Small capstone teams need a lightweight way to see work, ownership, priority, progress, links, and blockers in one place. Full-featured project-management tools add views and capabilities that are unnecessary for a small student team.

### Product Vision

Provide a focused, low-friction project board that helps a capstone team organize work, expose blockers, and coordinate ownership without the overhead of an enterprise project-management suite.

### Intended Users and Stakeholders

| Person or group | Need or responsibility | How the app helps |
| --- | --- | --- |
| **Capstone team members** | Understand what needs to be done, who owns it, and what is blocking progress. | Presents work on a shared Kanban-style board with status, owner, priority, links, and notes. |
| **Student project lead or product owner** | Organize work, set priorities, assign owners, and identify bottlenecks. | Provides a single view of work from backlog to completion and makes blockers visible. |
| **Faculty or project mentor** | Review progress and discuss impediments with the team. | Offers an at-a-glance view of current, blocked, and completed work. |

> **Assumption:** The primary unit is one small capstone team working on one or a few projects. Support for multiple organizations or enterprise-scale team administration is not required for the MVP.

### Success Criteria

- [ ] A team member can create a work item and place it on the board.
- [ ] Each work item visibly shows its status, owner, and priority.
- [ ] A team member can attach a relevant project link and record notes or blockers.
- [ ] A team can move work from the backlog through completion without changing views.
- [ ] During a team check-in, members can identify blocked work from the board without opening a separate tool.

---

## 2. Product Research and Decisions

> **CRISP-DM connection — Data Understanding:** Learn from existing products and inspect the patterns, assumptions, and constraints that shape the problem space.

Research source: [Product Management Tool Review](./Product%20Management%20Tool%20Review.md)

### Tools Reviewed

| Tool | Pattern observed | Useful for this app? | Decision or implication |
| --- | --- | :---: | --- |
| [Jira](https://www.atlassian.com/software/jira) | Tasks can be shown on a timeline, list, or Kanban board and moved through workflow columns such as To Do, In Design, In Development, GTM Launch, and Done. | **Yes, simplified** | Use one Kanban-style board with a small, configurable workflow rather than multiple synchronized views. |
| [Jira](https://www.atlassian.com/software/jira) | Tasks have identifiers, assignees, completion state, notes, blockers, related issues, and external links. | **Yes** | Give every work item an ID and support an owner, status, priority, project links, notes, and blocker information. |
| [Jira](https://www.atlassian.com/software/jira) | Agents can be assigned work; meeting videos and AI-generated notes support asynchronous collaboration. | **No for MVP** | Exclude agentic task execution, asynchronous video, and AI meeting notes from the first release. |
| [GitHub Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/creating-projects/creating-a-project) | Issues and pull requests integrate directly with repositories and can be organized on a board, roadmap, or table. | **Yes, simplified** | Support links to relevant project resources. A deep GitHub integration is not required for the MVP. |
| [GitHub Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/creating-projects/creating-a-project) | Relationships expose blocked work and bottlenecks. | **Yes** | Make blocker or dependency notes visible on each work item so the team can discuss bottlenecks. |
| [GitHub Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/creating-projects/creating-a-project) | Multiple layouts, multiple teams, and nested sub-issues support larger and more complex projects. | **No for MVP** | Keep one board and a flat work-item model for a small team. |

### Patterns to Adopt

1. **Kanban-style board:** Display work in status columns so progress is visible at a glance.
2. **Simple workflow states:** Organize work from a backlog or backburner state through completion.
3. **Clear ownership:** Assign one person to each work item.
4. **Visible priority:** Rate work from low to high priority.
5. **Stable identity:** Give each work item a unique ID.
6. **Project-resource links:** Attach URLs for repositories, designs, documents, or other relevant resources.
7. **Contextual notes and blockers:** Keep progress notes, blockers, and dependency information with the work item.

### Patterns to Reject or Simplify

- **Multiple board layouts:** Provide one Kanban view instead of separate timeline, roadmap, table, and list views.
- **Nested work hierarchies:** Do not include sub-issues in the MVP; keep work items flat.
- **Multi-team administration:** Optimize for one small capstone team rather than multiple organizations or teams.
- **Rich agentic execution:** Do not assign autonomous agents to complete work items in the MVP.
- **Meeting-media features:** Exclude asynchronous video and AI-generated meeting notes.
- **Attention-management automation:** Exclude alerts, notifications, and automated capacity warnings.

### Product Decisions

| ID | Decision | Alternatives considered | Choice | Reason |
| --- | --- | --- | --- | --- |
| **PD-01** | Primary work view | Timeline, roadmap, table, list, Kanban board | Kanban board | It gives a small team a direct view of status and bottlenecks. |
| **PD-02** | Work-item organization | Nested issues, flat work items | Flat work items | Capstone projects do not require enterprise-scale issue hierarchies for the MVP. |
| **PD-03** | Resource integration | Deep GitHub integration, external links, no integration | External links | Links deliver most of the value while keeping implementation small and tool-agnostic. |
| **PD-04** | Blocker representation | Relationship graph, blocker notes, separate blocker records | Blocker or dependency notes on work items | Notes are sufficient for a small team and keep context near the work. |
| **PD-05** | Automated assistance | Agentic execution, meeting AI, no automation | No rich AI automation in MVP | The reviewed AI features do not provide enough first-release value for a small co-located team. |
| **PD-06** | Workflow configuration | Fixed columns, configurable columns | Small configurable workflow | The review values modular columns, but the first release should avoid the complexity of multiple board types. |

---

## 3. MVP Scope

> **CRISP-DM connection — Business Understanding → Data Understanding:** Decide which needs and product patterns belong in the first version and which do not.

### In Scope

- [x] Create and view projects.
- [x] Create, view, edit, and identify work items or user stories.
- [x] Display work on one Kanban-style board.
- [x] Move work items between workflow columns, from backlog/backburner through completion.
- [x] Assign one owner to a work item.
- [x] Set a work item's priority from low to high.
- [x] Add relevant external project links.
- [x] Add notes, including blocker or dependency information.

### Explicitly Out of Scope

- Rich agentic integration or autonomous task execution
- Multiple simultaneous board views, including timeline, roadmap, table, and list layouts
- Alerts and notifications
- Automated capacity checks or workload warnings
- Multiple-team or organization administration
- Nested sub-issues or a sub-issue table
- Asynchronous meeting video
- AI-generated meeting notes

### Deferred or Optional Ideas

- [ ] Deep GitHub repository, issue, and pull-request integration
- [ ] Sprint lifecycle and sprint planning
- [ ] Sprint reporting
- [ ] Velocity or historical progress tracking
- [ ] Configurable workflow templates beyond a small set of columns
- [ ] Relationship graphs for dependencies and blockers

> **Scope note:** Deferred items are not implied requirements. They require a later product decision before implementation.

---

## 4. Key User Workflows

> **CRISP-DM connection — Business Understanding:** Describe how a stakeholder will accomplish a meaningful goal and what result would count as success.

The MVP centers on a shared board: students add work, students or faculty identify blockers, and users move cards forward when the requirements for the next workflow state are satisfied.

### Workflow 1: Add a Task to the Shared Kanban Board

- **Primary actor:** Student
- **Starting condition:** The student has opened a project and can view its Kanban board.
- **Steps:**
  1. The student selects **Add task** from the board.
  2. The system presents a clear task-entry form.
  3. The student enters the required task information, including a title and initial workflow section.
  4. The student may add a description, owner, priority, external link, or notes.
  5. The student saves the task.
  6. The system adds the task card to the selected section and saves it as shared project data.
  7. Every student or faculty member viewing the same project can see the task on their board.
- **Expected result:** One shared task record appears in the correct Kanban section for every user of the project, with the same ID and task details.
- **Failure or edge cases:**
  - If required information is missing, the task is not created and the form identifies what must be corrected.
  - Repeated submission must not create duplicate task cards.
  - If saving fails, the system tells the student that the task was not saved and preserves the entered information for another attempt.
  - Users who open or return to the board later see the same saved task.

### Workflow 2: Record a Project Blocker

- **Primary actors:** Student or faculty member
- **Starting condition:** The user has identified something preventing or threatening progress and can view the relevant project's board.
- **Steps:**
  1. The user opens the affected task card.
  2. The user marks the task as blocked and enters a blocker note describing the issue.
  3. The user may add an owner, dependency, or supporting link when that information is known.
  4. The user saves the blocker information.
  5. The system adds a visible blocked indicator to the card while retaining it in its current board section.
  6. Every user viewing the same project can see the blocked state and blocker note.
- **Expected result:** The board clearly identifies the affected task as blocked, and all project users can review the same blocker information.
- **Failure or edge cases:**
  - A task cannot be marked as blocked without a blocker note explaining the issue.
  - If no existing task represents the affected work, the user first creates a task through Workflow 1 and then records the blocker.
  - If the blocker is resolved, an authorized user can clear the blocked state without deleting the blocker history.
  - If saving fails, the system retains the entered blocker information and reports that it was not saved.

### Workflow 3: Move a Task to a New Board Section

- **Primary actors:** Student or faculty member
- **Starting condition:** A task exists on the shared board, and the user believes it satisfies the requirements for another workflow section.
- **Steps:**
  1. The user selects or drags the task toward the destination section.
  2. The system checks the transition requirements for that destination.
  3. If all requirements are met, the system saves the new task status and moves the card.
  4. The updated card position becomes visible to every user of the project.
  5. If the task is blocked, the blocked indicator and note remain attached unless the blocker has been explicitly resolved.
- **Expected result:** The task appears in the new section for all project users, and its saved status matches its visible board position.
- **Failure or edge cases:**
  - If a requirement is not met, the task remains in its original section and the system explains what is missing.
  - Moving a task must not create a duplicate or discard its owner, priority, links, notes, or blocker history.
  - If two users update the same task at nearly the same time, the system must not silently overwrite one user's change.
  - If saving fails, the task returns to its last saved section and the system reports the failure.

 All sections allowed for all users, requirements not yet needed to enter different sections, other than them existing in a previous section.

### Workflow Checklist

- [ ] A student can enter and save a task from the Kanban board.
- [ ] The saved task appears on the shared board for every project user.
- [ ] A student or faculty member can mark a task as blocked and explain why.
- [ ] The blocker is visible to every project user without removing the task from its current section.
- [ ] A student or faculty member can move a task when its transition requirements are met.
- [ ] The system prevents a transition when its requirements are not met and explains why.
- [ ] Task details and blocker history remain intact after a move.

---

## 5. Functional Requirements

> **CRISP-DM connection — Business Understanding → Modeling:** Translate stakeholder needs into precise behavior that can later be designed, implemented, and tested.

Write requirements as behavior, not implementation guesses. Use identifiers so tests and API endpoints can refer back to them.

| ID | Requirement | Priority | Related workflow | Acceptance evidence |
| --- | --- | --- | --- | --- |
| **FR-01** | When a student chooses to add a task, the system must present a task-entry form that identifies the required and optional information. | Must | Workflow 1 | From the board, a student can open the form and distinguish required fields from optional fields. |
| **FR-02** | When a student submits a task with a title and initial board section, the system must create exactly one task with a unique ID and display it in that section. | Must | Workflow 1 | A valid submission produces one card in the selected section, and reopening the card shows its unique ID and saved details. |
| **FR-03** | When required task information is missing or invalid, the system must reject the submission, identify each problem, and retain the student's entered information. | Must | Workflow 1 | Submitting an incomplete form creates no task, shows actionable validation messages, and leaves valid entries in the form. |
| **FR-04** | After a task is saved, the system must make the same task and details visible on the shared project board to every student and faculty user of that project. | Must | Workflow 1 | Two users viewing the same project see one task with the same ID, section, and details. A user opening the board later sees the saved task. |
| **FR-05** | If a task submission is repeated, the system must not create duplicate task records from the same submission. | Must | Workflow 1 | Repeating or double-clicking the save action results in one task card and one task ID. |
| **FR-06** | When saving a task fails, the system must report that the task was not saved and retain the entered information so the student can try again. | Must | Workflow 1 | A simulated save failure creates no task, displays a failure message, and preserves the form contents. |
| **FR-07** | A student or faculty member must be able to mark an existing task as blocked by entering and saving a blocker note. | Must | Workflow 2 | Saving a nonempty blocker note marks the selected task as blocked. |
| **FR-08** | When a task is blocked, the system must show a visible blocked indicator on its board card and make the blocker note available to every user of the project without moving the task from its current section. | Must | Workflow 2 | All project users see the blocked indicator and the same note, while the card remains in its original section. |
| **FR-09** | The system must reject an attempt to mark a task as blocked when no blocker note is provided and must explain what is required. | Must | Workflow 2 | An empty blocker submission leaves the task unchanged and displays a validation message. |
| **FR-10** | A student or faculty member must be able to clear a resolved blocker without deleting its recorded blocker history. | Should | Workflow 2 | Clearing the blocker removes the active indicator, and the previous blocker note remains available in the task history. |
| **FR-11** | When a user attempts to move a task, the system must check the requirements for the destination section before changing the task's status or position. | Must | Workflow 3 | Each attempted move is evaluated against the configured transition requirements. |
| **FR-12** | When all transition requirements are met, the system must save the destination as the task's status and display the card in that section for every project user. | Must | Workflow 3 | After a valid move, multiple users see the card in the same destination section and the stored status matches that section. |
| **FR-13** | When a transition requirement is not met, the system must leave the task in its last saved section and identify the unmet requirement. | Must | Workflow 3 | An invalid move changes neither status nor position and presents an actionable explanation. |
| **FR-14** | Moving a task must preserve its ID, owner, priority, links, notes, and blocker history. | Must | Workflow 3 | The task has identical supporting details before and after a successful move. |
| **FR-15** | If moving a task fails to save, the system must return the card to its last saved section and report the failure. | Must | Workflow 3 | A simulated save failure leaves persisted status unchanged, restores the card position, and displays an error. |
| **FR-16** | If two users attempt to update the same task from different saved versions, the system must warn the later user rather than silently overwriting another user's change. | Should | Workflows 1–3 | A concurrent-update test preserves the first saved change and gives the later user a conflict warning and current task data. |

### Workflow Rules

These rules constrain how the requirements above should behave.

- A task belongs to one project and has one unique ID.
- A task title and initial board section are required at creation; description, owner, priority, external links, and general notes are optional unless a later decision changes their validation rules.
- Saving shared state must succeed before the interface presents a creation, blocker update, or move as complete.
- Every user viewing the same project must receive the same saved task data; users outside that project must not see its tasks.
- A blocker is recorded on an existing task. If the affected work has no task, the user must create the task before adding the blocker.
- A blocker note is required when a task is marked as blocked.
- Marking a task as blocked does not automatically change its board section.
- Moving a blocked task does not automatically resolve its blocker or remove its blocker history.
- A task's saved status and visible Kanban section must always correspond.
- A rejected creation, blocker update, or task move must not partially change shared project data.
- The system must not silently discard one user's work when concurrent changes conflict.



---

## 6. Domain Model

> **CRISP-DM connection — Data Understanding → Modeling:** Identify the information the product manages, its relationships, and the rules that govern it.

The model describes the information and relationships needed to satisfy the MVP workflows and functional requirements. A Kanban board is a **view of project tasks grouped by workflow section**, not a separate stored entity.

### Model Conventions

- Every entity has a stable, unique `id` unless it is identified by a documented composite key.
- Fields marked **Required** must have a valid value before the entity can be saved.
- Fields marked **System** are assigned or maintained by the application rather than entered directly by a user.
- Timestamps record when shared state changed and must use one consistent time standard.
- References to users must point to valid `User` objects; project-scoped references must point to users who are members of that project.
- Deleting or archiving shared records must not silently destroy history needed by FR-10, FR-14, or FR-16.

### Relationship Overview

| Source | Relationship | Target | Meaning |
| --- | --- | --- | --- |
| `User` | many-to-many through `ProjectMembership` | `Project` | Users participate in projects with a project-specific role. |
| `Project` | one-to-many | `WorkflowSection` | A project defines the ordered sections displayed on its Kanban board. |
| `WorkflowSection` | one-to-many | `WorkflowTransition` | A transition defines whether and how a task may move between two sections. |
| `Project` | one-to-many | `Task` | Every task belongs to exactly one project. |
| `WorkflowSection` | one-to-many | `Task` | Every task occupies exactly one board section at a time. |
| `User` | one-to-many | `Task` | A user may create or own multiple tasks. |
| `Task` | one-to-many | `TaskBlocker` | A task retains current and resolved blocker records. |
| `Task` | one-to-many | `TaskLink` | A task may reference repositories, documents, designs, or other resources. |
| `Task` | one-to-many | `TaskNote` | Users may add contextual notes to a task. |
| `Task` | one-to-many | `TaskHistoryEvent` | Important changes are recorded for traceability and conflict review. |

### Entity: `User`

**Purpose:** Represents a student, faculty member, or other person who can participate in a project.

| Field | Requirement | Definition |
| --- | --- | --- |
| `id` | Required, System | Stable unique identifier for the user. |
| `display_name` | Required | Name shown on task cards, ownership fields, notes, and history. |
| `email` | Optional | Contact or sign-in identifier; whether it is required depends on the authentication decision. |
| `account_status` | Required, System | Whether the account is active or inactive. |
| `created_at` | Required, System | Time the user record was created. |
| `updated_at` | Required, System | Time the user record was last changed. |

**Relationships**

- Has zero or more `ProjectMembership` records.
- May create tasks, blockers, notes, links, and history-generating changes.
- May own zero or more tasks in projects where the user is a member.

**Rules**

- A user's project permissions come from `ProjectMembership`, not from one global role.
- An inactive user remains identifiable in existing task and history records.
- Authentication credentials or third-party identity details must be modeled separately once the authentication approach is chosen.

### Entity: `Project`

**Purpose:** Groups the members, workflow configuration, and shared tasks for one body of capstone work.

| Field | Requirement | Definition |
| --- | --- | --- |
| `id` | Required, System | Stable unique identifier for the project. |
| `name` | Required | Human-readable project name. |
| `description` | Optional | Summary of the project's purpose or scope. |
| `created_by_user_id` | Required | User who created the project. |
| `created_at` | Required, System | Time the project was created. |
| `updated_at` | Required, System | Time project-level data was last changed. |

**Relationships**

- Has one or more members through `ProjectMembership`.
- Owns one or more ordered `WorkflowSection` records.
- Owns zero or more tasks and workflow transitions.

**Rules**

- A project name cannot be blank.
- The creating user must also be represented by a membership in the project.
- Tasks, sections, transitions, and memberships from one project cannot be attached to another project.
- The board shows only the tasks and workflow sections belonging to the selected project.

### Entity: `ProjectMembership`

**Purpose:** Connects a user to a project and defines that person's role within the project.

| Field | Requirement | Definition |
| --- | --- | --- |
| `project_id` | Required | Project the user can access. |
| `user_id` | Required | Participating user. |
| `role` | Required | Project-specific role, initially `student`, `student_lead`, or `faculty`. |
| `joined_at` | Required, System | Time the membership began. |
| `membership_status` | Required, System | Whether the membership is active or inactive. |

**Relationships**

- Belongs to exactly one `Project` and one `User`.

**Rules**

- The pair `project_id` and `user_id` must be unique.
- Active members can view the project's shared board.
- Students and student leads can create tasks.
- Students, student leads, and faculty can record blockers and attempt task transitions, subject to transition rules.
- An inactive membership remains available for historical attribution but cannot make new project changes.

-Faculty can create any event and move them as needed, along with the student. No part of it is forbidden to a user that is a student or faculty.

### Entity: `Task`

**Purpose:** Represents one unit of work displayed as a card on the Kanban board. This is the MVP term for the template's earlier `UserStory` concept.

| Field | Requirement | Definition |
| --- | --- | --- |
| `id` | Required, System | Stable unique identifier displayed or available to users. |
| `project_id` | Required | Project that owns the task. |
| `section_id` | Required | Current workflow section; this is the authoritative task status. |
| `title` | Required | Short description of the work. |
| `description` | Optional | Detailed explanation of the work or its intended outcome. |
| `owner_user_id` | Optional | Project member responsible for the task. |
| `priority` | Optional | Relative importance: `low`, `medium`, or `high`. |
| `position` | Optional, System | Ordering of the card within its current section, if manual ordering is supported. |
| `created_by_user_id` | Required | Project member who created the task. |
| `version` | Required, System | Revision value used to detect conflicting updates. |
| `created_at` | Required, System | Time the task was created. |
| `updated_at` | Required, System | Time any current task state was last changed. |

**Computed properties**

- `is_blocked` is true when the task has at least one unresolved `TaskBlocker`.
- `status_name` is derived from the related `WorkflowSection`; it is not independently editable.

**Relationships**

- Belongs to exactly one project and one workflow section in that project.
- Has one creator and, optionally, one owner who are members of that project.
- Has zero or more blockers, links, notes, and history events.

**Rules**

- `title`, `project_id`, `section_id`, and `created_by_user_id` are required at creation.
- The selected section must belong to the same project as the task.
- An owner, when present, must have an active membership in the task's project.
- A task appears exactly once on the shared board and in the section identified by `section_id`.
- A task move changes `section_id` only after the relevant transition requirements pass.
- Changing sections must preserve the task's identity, supporting details, and related records.
- An update based on an outdated `version` must produce a visible conflict instead of silently overwriting newer data.

### Entity: `WorkflowSection`

**Purpose:** Defines one ordered column or state on a project's Kanban board.

| Field | Requirement | Definition |
| --- | --- | --- |
| `id` | Required, System | Stable unique identifier for the section. |
| `project_id` | Required | Project that owns the section. |
| `name` | Required | User-facing column name, such as Backlog or Complete. |
| `position` | Required | Display order of the section on the board. |
| `is_initial` | Required | Whether users may choose this section when creating a task. |
| `is_terminal` | Required | Whether this section represents completed or otherwise finished work. |

**Relationships**

- Belongs to one project and contains zero or more tasks.
- May be the source or destination of multiple workflow transitions.

**Rules**

- Section names and positions must be unique within a project.
- Every project must have at least one section available for task creation.
- Removing a section that still contains tasks must be prevented until those tasks are moved through an explicit user action.

### Entity: `WorkflowTransition`

**Purpose:** Defines an allowed movement between two board sections and the requirements that gate it.

| Field | Requirement | Definition |
| --- | --- | --- |
| `id` | Required, System | Stable unique identifier for the transition. |
| `project_id` | Required | Project that owns the workflow. |
| `from_section_id` | Required | Section where the task currently resides. |
| `to_section_id` | Required | Requested destination section. |
| `name` | Optional | Human-readable label for the transition. |
| `is_enabled` | Required | Whether users may currently attempt the transition. |

**Relationships**

- Connects two `WorkflowSection` records in the same project.
- Has zero or more `TransitionRequirement` records.

**Rules**

- Source and destination must be different sections in the same project.
- The source/destination pair must be unique within a project.
- A task may move only through an enabled transition defined for its current and requested sections.
- Every associated requirement must pass before the task's `section_id` changes.

### Entity: `TransitionRequirement`

**Purpose:** Describes one testable condition that must pass before a task enters a destination section.

| Field | Requirement | Definition |
| --- | --- | --- |
| `id` | Required, System | Stable unique identifier for the requirement. |
| `transition_id` | Required | Transition gated by this condition. |
| `name` | Required | Short, user-facing description of the condition. |
| `requirement_type` | Required | Defined category of check, such as required task information or blocker state. |
| `configuration` | Required | Values needed to evaluate the selected requirement type. |
| `failure_message` | Required | Actionable explanation shown when the condition is not satisfied. |
| `position` | Required | Evaluation and display order among the transition's requirements. |

**Relationships**

- Belongs to exactly one workflow transition.

**Rules**

- The system must be able to evaluate the requirement from saved project and task data.
- A failed condition must not partially move the task.
- The user must receive the corresponding `failure_message` when the condition blocks a move.
- Requirement types and configuration formats must be explicitly defined before implementation.

### Entity: `TaskBlocker`

**Purpose:** Records an issue that prevents or threatens task progress and preserves its resolution history.

| Field | Requirement | Definition |
| --- | --- | --- |
| `id` | Required, System | Stable unique identifier for the blocker. |
| `task_id` | Required | Affected task. |
| `description` | Required | Explanation of the blocker. |
| `created_by_user_id` | Required | Project member who recorded the blocker. |
| `created_at` | Required, System | Time the blocker was recorded. |
| `resolved_by_user_id` | Optional | Project member who resolved the blocker. |
| `resolved_at` | Optional, System | Time the blocker was resolved. |
| `resolution_note` | Optional | Explanation of how or why the blocker was resolved. |

**Computed properties**

- `is_active` is true when `resolved_at` is empty.

**Relationships**

- Belongs to exactly one task.
- Its creator and resolver must be members of the task's project at the time of their actions.

**Rules**

- A blocker description cannot be blank.
- Recording a blocker does not change the task's workflow section.
- Resolving a blocker sets its resolution fields rather than deleting the blocker.
- A task remains visibly blocked while any related blocker is active.

### Entity: `TaskLink`

**Purpose:** Attaches an external project resource to a task.

| Field | Requirement | Definition |
| --- | --- | --- |
| `id` | Required, System | Stable unique identifier for the link. |
| `task_id` | Required | Task that owns the link. |
| `url` | Required | Valid external resource location. |
| `label` | Optional | Short explanation of the resource. |
| `created_by_user_id` | Required | Project member who added the link. |
| `created_at` | Required, System | Time the link was added. |

**Rules**

- The URL cannot be blank and must satisfy the application's accepted URL rules.
- A task move must not remove or alter its links.

### Entity: `TaskNote`

**Purpose:** Stores contextual information supplied by a project member that is not an active blocker.

| Field | Requirement | Definition |
| --- | --- | --- |
| `id` | Required, System | Stable unique identifier for the note. |
| `task_id` | Required | Task that owns the note. |
| `body` | Required | Note content. |
| `created_by_user_id` | Required | Project member who wrote the note. |
| `created_at` | Required, System | Time the note was added. |
| `updated_at` | Required, System | Time the note was last edited. |

**Rules**

- A note body cannot be blank.
- General notes and blocker records are distinct; information that controls the visible blocked state belongs in `TaskBlocker`.
- A task move must not remove or alter its notes.

### Entity: `TaskHistoryEvent`

**Purpose:** Provides an append-only record of meaningful task changes for attribution, blocker history, and conflict review.

| Field | Requirement | Definition |
| --- | --- | --- |
| `id` | Required, System | Stable unique identifier for the event. |
| `task_id` | Required | Task affected by the event. |
| `actor_user_id` | Required | User responsible for the change. |
| `event_type` | Required | Defined category such as `created`, `details_updated`, `moved`, `blocker_added`, or `blocker_resolved`. |
| `from_section_id` | Optional | Previous section for a move event. |
| `to_section_id` | Optional | Destination section for a move event. |
| `details` | Optional | Human-readable or structured summary of the change. |
| `task_version` | Required, System | Task revision produced by the change. |
| `occurred_at` | Required, System | Time the change was saved. |

**Rules**

- History events are created only after the associated shared change succeeds.
- Existing events cannot be rewritten as part of an ordinary task edit.
- A move event must record both the previous and destination sections.
- Historical attribution remains readable if a user or membership later becomes inactive.

### Derived Board View

The Kanban board is assembled from:

1. The selected `Project`.
2. Its `WorkflowSection` records ordered by `position`.
3. Its `Task` records grouped by `section_id`.
4. Each task's owner, priority, links, notes, and computed blocked state.

The shared board must never display two cards for one task ID or place a task under a section that disagrees with its saved `section_id`.

### Deferred Domain Concepts

`Sprint`, `SprintStory`, and `SprintReport` are not included in the current MVP domain model because sprint planning and reporting are deferred in Section 3. They should be added only after a later product decision defines their workflows and relationship to tasks.

### Domain Questions to Resolve

- [ ] What authentication identity, if any, is associated with a `User`?
- [ ] Can faculty create or edit ordinary tasks, or only review the board, record blockers, and move tasks?
- [ ] Does `student_lead` have permissions beyond those of `student`?
- [ ] What are the initial board sections and their allowed transitions?
- [ ] Which requirement types and configurations can gate each transition?
- [ ] Is task ownership optional throughout the workflow, or required before a particular section?
- [ ] Can users manually reorder cards within a section?
- [ ] Can tasks, notes, or links be edited and deleted, and what history must be retained?
- [ ] What URL schemes and destinations are accepted for task links?
- [ ] How quickly must changes become visible to other users who already have the board open?
- [ ] Should completed tasks remain on the active board, be archived, or support both behaviors?

---

## 7. API Contract

> **CRISP-DM connection — Modeling:** Define the executable boundary between product behavior, backend services, and future implementation.

The backend API will be implemented with FastAPI. This contract covers the current MVP domain model and keeps client behavior independent of database or synchronization technology.

### Contract Conventions

- **Base path:** `/api/v1`
- **Media type:** Requests and responses use `application/json`, except any future event stream.
- **Identifiers:** IDs are opaque strings. Clients must not infer an entity type or creation order from an ID.
- **Timestamps:** Timestamps are ISO 8601 strings in UTC, such as `2026-09-23T21:45:00Z`.
- **Authentication:** The authentication mechanism is still an open question. Where an endpoint refers to the **current user**, the server derives that user from the approved authentication mechanism; a client-supplied creator ID is not trusted.
- **Authorization:** Project data is available only to active members of that project. Role rules come from `ProjectMembership`.
- **Concurrency:** Mutations to an existing task include `expected_task_version`. A mismatched version returns `409 Conflict` and the current task version rather than silently overwriting data.
- **Idempotency:** `POST /projects/{project_id}/tasks` accepts an `Idempotency-Key` header. Reusing the same key and request produces the original result rather than a duplicate task.
- **Pagination:** Collection endpoints accept optional `limit` and `cursor` query parameters and return `items` plus `next_cursor`.
- **No partial success:** If any required part of a mutation fails, none of that request's shared state is saved.

### Standard Error Response

All endpoint errors use the same shape:

```json
{
  "error": {
    "code": "validation_error",
    "message": "The request could not be completed.",
    "details": [
      {
        "field": "title",
        "reason": "A task title is required."
      }
    ],
    "request_id": "req_01J8EXAMPLE"
  }
}
```

| Status | Meaning |
| --- | --- |
| `400 Bad Request` | Malformed request or unsupported operation. |
| `401 Unauthorized` | No valid current user could be established. |
| `403 Forbidden` | The current user lacks project access or the required role. |
| `404 Not Found` | The requested resource does not exist or is not visible to the current user. |
| `409 Conflict` | Version conflict, duplicate relationship, or unmet transition requirements. |
| `422 Unprocessable Entity` | Field validation failed. |
| `500 Internal Server Error` | An unexpected failure prevented the operation from being saved. |

### Endpoint Summary

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/users` | Create a user record. |
| `GET` | `/users/{user_id}` | Retrieve one user. |
| `POST` | `/projects` | Create a project and its initial membership. |
| `GET` | `/projects` | List projects available to the current user. |
| `GET` | `/projects/{project_id}` | Retrieve one project. |
| `PATCH` | `/projects/{project_id}` | Edit project details. |
| `GET` | `/projects/{project_id}/members` | List project memberships. |
| `POST` | `/projects/{project_id}/members` | Add a project member. |
| `PATCH` | `/projects/{project_id}/members/{user_id}` | Change a member's role or status. |
| `GET` | `/projects/{project_id}/workflow` | Retrieve board sections, transitions, and requirements. |
| `GET` | `/projects/{project_id}/board` | Retrieve the shared Kanban board. |
| `POST` | `/projects/{project_id}/tasks` | Create a task. |
| `GET` | `/projects/{project_id}/tasks/{task_id}` | Retrieve task details. |
| `PATCH` | `/projects/{project_id}/tasks/{task_id}` | Edit ordinary task details. |
| `POST` | `/projects/{project_id}/tasks/{task_id}/transitions` | Validate and move a task. |
| `GET` | `/projects/{project_id}/tasks/{task_id}/blockers` | List task blockers. |
| `POST` | `/projects/{project_id}/tasks/{task_id}/blockers` | Record a blocker. |
| `POST` | `/projects/{project_id}/tasks/{task_id}/blockers/{blocker_id}/resolve` | Resolve a blocker. |
| `GET` | `/projects/{project_id}/tasks/{task_id}/links` | List task links. |
| `POST` | `/projects/{project_id}/tasks/{task_id}/links` | Add a task link. |
| `GET` | `/projects/{project_id}/tasks/{task_id}/notes` | List task notes. |
| `POST` | `/projects/{project_id}/tasks/{task_id}/notes` | Add a task note. |
| `GET` | `/projects/{project_id}/tasks/{task_id}/history` | Retrieve task history. |

### User Endpoints

> These endpoints are provisional until the authentication and account-provisioning decision is resolved.

#### `POST /api/v1/users`

- **Purpose:** Create a user that can later be added to projects.
- **Related model:** `User`

**Request**

```json
{
  "display_name": "Jordan Lee",
  "email": "jordan@example.edu"
}
```

**Response — `201 Created`**

```json
{
  "id": "usr_123",
  "display_name": "Jordan Lee",
  "email": "jordan@example.edu",
  "account_status": "active",
  "created_at": "2026-09-23T21:45:00Z",
  "updated_at": "2026-09-23T21:45:00Z"
}
```

- **Validation:** `display_name` is required; email validation and uniqueness depend on the authentication decision.
- **Errors:** `409` for an identity conflict; `422` for invalid fields.

#### `GET /api/v1/users/{user_id}`

- **Purpose:** Retrieve display information for one visible user.
- **Request:** No body.

**Response — `200 OK`**

```json
{
  "id": "usr_123",
  "display_name": "Jordan Lee",
  "email": "jordan@example.edu",
  "account_status": "active",
  "created_at": "2026-09-23T21:45:00Z",
  "updated_at": "2026-09-23T21:45:00Z"
}
```

- **Errors:** `403` if the user is not visible to the requester; `404` if no visible user exists.

### Project Endpoints

#### `POST /api/v1/projects`

- **Purpose:** Create a project, add the current user as `student_lead`, and provision the approved default workflow.
- **Related workflows:** Prerequisite for Workflows 1–3.

**Request**

```json
{
  "name": "Capstone Planning Tool",
  "description": "Shared Kanban board for the capstone team."
}
```

**Response — `201 Created`**

```json
{
  "id": "prj_123",
  "name": "Capstone Planning Tool",
  "description": "Shared Kanban board for the capstone team.",
  "created_by_user_id": "usr_123",
  "current_user_role": "student_lead",
  "created_at": "2026-09-23T21:50:00Z",
  "updated_at": "2026-09-23T21:50:00Z"
}
```

- **Validation:** `name` is required and cannot be blank.
- **Errors:** `401` if there is no current user; `422` for invalid fields; `500` if the project, membership, and workflow cannot all be created together.

#### `GET /api/v1/projects`

- **Purpose:** List projects in which the current user has an active membership.
- **Request:** No body. Optional query parameters: `limit` and `cursor`.

**Response — `200 OK`**

```json
{
  "items": [
    {
      "id": "prj_123",
      "name": "Capstone Planning Tool",
      "description": "Shared Kanban board for the capstone team.",
      "current_user_role": "student_lead",
      "updated_at": "2026-09-23T21:50:00Z"
    }
  ],
  "next_cursor": null
}
```

- **Errors:** `401` if there is no current user; `422` for invalid pagination values.

#### `GET /api/v1/projects/{project_id}`

- **Purpose:** Retrieve one project's details.
- **Request:** No body.

**Response — `200 OK`**

```json
{
  "id": "prj_123",
  "name": "Capstone Planning Tool",
  "description": "Shared Kanban board for the capstone team.",
  "created_by_user_id": "usr_123",
  "current_user_role": "faculty",
  "created_at": "2026-09-23T21:50:00Z",
  "updated_at": "2026-09-23T21:50:00Z"
}
```

- **Errors:** `403` if the requester is not an active member; `404` if the project does not exist.

#### `PATCH /api/v1/projects/{project_id}`

- **Purpose:** Change a project's name or description.
- **Request:** Include at least one editable field.

```json
{
  "name": "Engineering Workflow Board",
  "description": "Updated capstone project description."
}
```

**Response — `200 OK`**

```json
{
  "id": "prj_123",
  "name": "Engineering Workflow Board",
  "description": "Updated capstone project description.",
  "created_by_user_id": "usr_123",
  "current_user_role": "student_lead",
  "created_at": "2026-09-23T21:50:00Z",
  "updated_at": "2026-09-23T22:10:00Z"
}
```

- **Validation:** `name`, when supplied, cannot be blank.
- **Errors:** `403` for insufficient role permission; `404` if the project is unavailable; `422` for invalid fields.

### Membership Endpoints

#### `GET /api/v1/projects/{project_id}/members`

- **Purpose:** List the students and faculty associated with a project.
- **Request:** No body. Optional query parameters: `status`, `limit`, and `cursor`.

**Response — `200 OK`**

```json
{
  "items": [
    {
      "user": {
        "id": "usr_123",
        "display_name": "Jordan Lee"
      },
      "role": "student_lead",
      "membership_status": "active",
      "joined_at": "2026-09-23T21:50:00Z"
    }
  ],
  "next_cursor": null
}
```

- **Errors:** `403` if the requester is not an active member; `404` if the project does not exist.

#### `POST /api/v1/projects/{project_id}/members`

- **Purpose:** Add an existing user to a project.

**Request**

```json
{
  "user_id": "usr_456",
  "role": "student"
}
```

**Response — `201 Created`**

```json
{
  "project_id": "prj_123",
  "user": {
    "id": "usr_456",
    "display_name": "Avery Chen"
  },
  "role": "student",
  "membership_status": "active",
  "joined_at": "2026-09-23T22:15:00Z"
}
```

- **Validation:** `user_id` must identify an active user; `role` must be `student`, `student_lead`, or `faculty`.
- **Errors:** `403` for insufficient permission; `404` if the project or user is unavailable; `409` if the membership already exists; `422` for an invalid role.

#### `PATCH /api/v1/projects/{project_id}/members/{user_id}`

- **Purpose:** Change a member's project role or membership status.

**Request**

```json
{
  "role": "faculty",
  "membership_status": "active"
}
```

**Response — `200 OK`**

```json
{
  "project_id": "prj_123",
  "user": {
    "id": "usr_456",
    "display_name": "Avery Chen"
  },
  "role": "faculty",
  "membership_status": "active",
  "joined_at": "2026-09-23T22:15:00Z"
}
```

- **Validation:** At least one field is required; allowed statuses are `active` and `inactive`.
- **Errors:** `403` for insufficient permission; `404` if the membership is unavailable; `409` if the change would leave the project without an authorized lead; `422` for invalid values.

### Workflow and Board Endpoints

#### `GET /api/v1/projects/{project_id}/workflow`

- **Purpose:** Give clients the authoritative board sections, allowed transitions, and transition requirements.
- **Related requirements:** FR-11–FR-13.
- **Request:** No body.

**Response — `200 OK`**

```json
{
  "project_id": "prj_123",
  "sections": [
    {
      "id": "sec_backlog",
      "name": "Backlog",
      "position": 1,
      "is_initial": true,
      "is_terminal": false
    },
    {
      "id": "sec_done",
      "name": "Done",
      "position": 4,
      "is_initial": false,
      "is_terminal": true
    }
  ],
  "transitions": [
    {
      "id": "trn_backlog_done",
      "from_section_id": "sec_backlog",
      "to_section_id": "sec_done",
      "name": "Complete task",
      "is_enabled": true,
      "requirements": [
        {
          "id": "req_owner",
          "name": "Task has an owner",
          "requirement_type": "required_field",
          "configuration": {
            "field": "owner_user_id"
          },
          "failure_message": "Assign an owner before completing the task.",
          "position": 1
        }
      ]
    }
  ]
}
```

- **Errors:** `403` if the requester is not an active member; `404` if the project does not exist.

> **Contract constraint:** Workflow mutation endpoints are not yet defined. The initial sections, transitions, requirement types, and configuration rules must be decided before implementation.

#### `GET /api/v1/projects/{project_id}/board`

- **Purpose:** Retrieve one authoritative snapshot of the shared Kanban board.
- **Related requirements:** FR-04, FR-08, FR-12, and FR-14.
- **Request:** No body. An optional `updated_since` query parameter may be supported after the synchronization timing decision is made.

**Response — `200 OK`**

```json
{
  "project_id": "prj_123",
  "board_version": 42,
  "as_of": "2026-09-23T22:30:00Z",
  "sections": [
    {
      "id": "sec_backlog",
      "name": "Backlog",
      "position": 1,
      "tasks": [
        {
          "id": "tsk_123",
          "title": "Create the board layout",
          "section_id": "sec_backlog",
          "owner": {
            "id": "usr_456",
            "display_name": "Avery Chen"
          },
          "priority": "high",
          "is_blocked": true,
          "active_blocker_count": 1,
          "version": 3,
          "updated_at": "2026-09-23T22:29:00Z"
        }
      ]
    }
  ]
}
```

- **Rules:** Every task appears once; its `section_id` matches its containing section; the response reflects saved shared state.
- **Errors:** `403` if the requester is not an active member; `404` if the project does not exist.

### Task Endpoints

#### `POST /api/v1/projects/{project_id}/tasks`

- **Purpose:** Create one task and place it in an allowed initial board section.
- **Related requirements:** FR-01–FR-06.
- **Headers:** `Idempotency-Key` is required for interactive task creation.

**Request**

```json
{
  "title": "Create the board layout",
  "description": "Build the initial Kanban board interface.",
  "section_id": "sec_backlog",
  "owner_user_id": "usr_456",
  "priority": "high",
  "links": [
    {
      "url": "https://example.edu/design",
      "label": "Board design"
    }
  ],
  "notes": [
    {
      "body": "Review with the team before implementation."
    }
  ]
}
```

**Response — `201 Created`**

```json
{
  "id": "tsk_123",
  "project_id": "prj_123",
  "section": {
    "id": "sec_backlog",
    "name": "Backlog"
  },
  "title": "Create the board layout",
  "description": "Build the initial Kanban board interface.",
  "owner": {
    "id": "usr_456",
    "display_name": "Avery Chen"
  },
  "priority": "high",
  "is_blocked": false,
  "active_blocker_count": 0,
  "links": [
    {
      "id": "lnk_123",
      "url": "https://example.edu/design",
      "label": "Board design"
    }
  ],
  "notes": [
    {
      "id": "nte_123",
      "body": "Review with the team before implementation.",
      "created_by_user_id": "usr_123",
      "created_at": "2026-09-23T22:35:00Z",
      "updated_at": "2026-09-23T22:35:00Z"
    }
  ],
  "version": 1,
  "created_by_user_id": "usr_123",
  "created_at": "2026-09-23T22:35:00Z",
  "updated_at": "2026-09-23T22:35:00Z"
}
```

- **Validation:** `title` and `section_id` are required; the section must belong to the project and allow creation; the owner must be an active member; priority must be `low`, `medium`, `high`, or omitted; links and notes must satisfy their entity rules.
- **Errors:** `403` if the role cannot create tasks; `404` if the project, section, or owner is unavailable; `409` for an idempotency-key conflict; `422` for invalid fields; `500` if the task and nested records cannot all be saved.

#### `GET /api/v1/projects/{project_id}/tasks/{task_id}`

- **Purpose:** Retrieve complete current details for one task.
- **Request:** No body.

**Response — `200 OK`**

```json
{
  "id": "tsk_123",
  "project_id": "prj_123",
  "section": {
    "id": "sec_backlog",
    "name": "Backlog"
  },
  "title": "Create the board layout",
  "description": "Build the initial Kanban board interface.",
  "owner": {
    "id": "usr_456",
    "display_name": "Avery Chen"
  },
  "priority": "high",
  "is_blocked": true,
  "active_blocker_count": 1,
  "version": 3,
  "created_by_user_id": "usr_123",
  "created_at": "2026-09-23T22:35:00Z",
  "updated_at": "2026-09-23T22:45:00Z"
}
```

- **Errors:** `403` if the requester is not an active member; `404` if the project or task is unavailable.

#### `PATCH /api/v1/projects/{project_id}/tasks/{task_id}`

- **Purpose:** Edit ordinary task details without bypassing transition or blocker behavior.
- **Related requirements:** FR-14 and FR-16.

**Request**

```json
{
  "expected_task_version": 3,
  "title": "Create and validate the board layout",
  "description": "Build the layout and confirm it with two users.",
  "owner_user_id": "usr_456",
  "priority": "medium"
}
```

**Response — `200 OK`**

```json
{
  "id": "tsk_123",
  "project_id": "prj_123",
  "section": {
    "id": "sec_backlog",
    "name": "Backlog"
  },
  "title": "Create and validate the board layout",
  "description": "Build the layout and confirm it with two users.",
  "owner": {
    "id": "usr_456",
    "display_name": "Avery Chen"
  },
  "priority": "medium",
  "is_blocked": true,
  "active_blocker_count": 1,
  "version": 4,
  "updated_at": "2026-09-23T22:50:00Z"
}
```

- **Validation:** `expected_task_version` and at least one editable field are required. `section_id`, blocker state, links, and notes are rejected here and changed only through their dedicated endpoints.
- **Errors:** `403` for insufficient role permission; `404` if the task is unavailable; `409` when the expected version is stale; `422` for invalid fields.

#### `POST /api/v1/projects/{project_id}/tasks/{task_id}/transitions`

- **Purpose:** Evaluate the configured transition and move a task only when every requirement passes.
- **Related requirements:** FR-11–FR-16.

**Request**

```json
{
  "to_section_id": "sec_done",
  "expected_task_version": 4
}
```

**Response — `200 OK`**

```json
{
  "task": {
    "id": "tsk_123",
    "section": {
      "id": "sec_done",
      "name": "Done"
    },
    "version": 5,
    "updated_at": "2026-09-23T23:00:00Z"
  },
  "transition": {
    "id": "trn_backlog_done",
    "from_section_id": "sec_backlog",
    "to_section_id": "sec_done"
  },
  "history_event_id": "evt_789"
}
```

**Unmet-requirement response — `409 Conflict`**

```json
{
  "error": {
    "code": "transition_requirements_not_met",
    "message": "The task cannot enter Done.",
    "details": [
      {
        "requirement_id": "req_owner",
        "reason": "Assign an owner before completing the task."
      }
    ],
    "request_id": "req_01J8EXAMPLE"
  }
}
```

- **Rules:** A failed move leaves task state unchanged. A successful move preserves all related data and creates one history event.
- **Errors:** `403` for insufficient role permission; `404` if the task, destination, or transition is unavailable; `409` for unmet requirements or a stale version; `422` for invalid input; `500` if the move cannot be saved atomically.

### Blocker Endpoints

#### `GET /api/v1/projects/{project_id}/tasks/{task_id}/blockers`

- **Purpose:** Retrieve current and resolved blockers for a task.
- **Request:** No body. Optional query parameter: `status=active|resolved|all`; default is `all`.

**Response — `200 OK`**

```json
{
  "items": [
    {
      "id": "blk_123",
      "task_id": "tsk_123",
      "description": "Faculty approval is still required.",
      "is_active": true,
      "created_by_user_id": "usr_789",
      "created_at": "2026-09-23T22:45:00Z",
      "resolved_by_user_id": null,
      "resolved_at": null,
      "resolution_note": null
    }
  ],
  "next_cursor": null
}
```

- **Errors:** `403` if the requester is not an active member; `404` if the task is unavailable; `422` for an invalid status.

#### `POST /api/v1/projects/{project_id}/tasks/{task_id}/blockers`

- **Purpose:** Mark a task as blocked by adding a nonempty blocker record.
- **Related requirements:** FR-07–FR-09 and FR-16.

**Request**

```json
{
  "description": "Faculty approval is still required.",
  "expected_task_version": 2
}
```

**Response — `201 Created`**

```json
{
  "blocker": {
    "id": "blk_123",
    "task_id": "tsk_123",
    "description": "Faculty approval is still required.",
    "is_active": true,
    "created_by_user_id": "usr_789",
    "created_at": "2026-09-23T22:45:00Z",
    "resolved_by_user_id": null,
    "resolved_at": null,
    "resolution_note": null
  },
  "task": {
    "id": "tsk_123",
    "section_id": "sec_backlog",
    "is_blocked": true,
    "active_blocker_count": 1,
    "version": 3
  },
  "history_event_id": "evt_456"
}
```

- **Validation:** `description` and `expected_task_version` are required; adding a blocker does not change `section_id`.
- **Errors:** `403` for insufficient role permission; `404` if the task is unavailable; `409` for a stale version; `422` for a blank description.

#### `POST /api/v1/projects/{project_id}/tasks/{task_id}/blockers/{blocker_id}/resolve`

- **Purpose:** Resolve one active blocker while preserving its history.
- **Related requirements:** FR-10 and FR-16.

**Request**

```json
{
  "resolution_note": "Approval was received during the faculty review.",
  "expected_task_version": 3
}
```

**Response — `200 OK`**

```json
{
  "blocker": {
    "id": "blk_123",
    "task_id": "tsk_123",
    "description": "Faculty approval is still required.",
    "is_active": false,
    "created_by_user_id": "usr_789",
    "created_at": "2026-09-23T22:45:00Z",
    "resolved_by_user_id": "usr_123",
    "resolved_at": "2026-09-23T23:10:00Z",
    "resolution_note": "Approval was received during the faculty review."
  },
  "task": {
    "id": "tsk_123",
    "is_blocked": false,
    "active_blocker_count": 0,
    "version": 4
  },
  "history_event_id": "evt_457"
}
```

- **Rules:** The blocker record is updated, not deleted. `is_blocked` remains true if another active blocker exists.
- **Errors:** `403` for insufficient permission; `404` if the task or blocker is unavailable; `409` if the blocker is already resolved or the task version is stale; `422` for invalid input.

### Link Endpoints

#### `GET /api/v1/projects/{project_id}/tasks/{task_id}/links`

- **Purpose:** List external resources attached to a task.
- **Request:** No body.

**Response — `200 OK`**

```json
{
  "items": [
    {
      "id": "lnk_123",
      "task_id": "tsk_123",
      "url": "https://example.edu/design",
      "label": "Board design",
      "created_by_user_id": "usr_123",
      "created_at": "2026-09-23T22:35:00Z"
    }
  ],
  "next_cursor": null
}
```

- **Errors:** `403` if the requester is not an active member; `404` if the task is unavailable.

#### `POST /api/v1/projects/{project_id}/tasks/{task_id}/links`

- **Purpose:** Attach an external resource to an existing task.
- **Related requirements:** FR-14 and FR-16.

**Request**

```json
{
  "url": "https://github.com/example/project/issues/42",
  "label": "Related GitHub issue",
  "expected_task_version": 4
}
```

**Response — `201 Created`**

```json
{
  "link": {
    "id": "lnk_456",
    "task_id": "tsk_123",
    "url": "https://github.com/example/project/issues/42",
    "label": "Related GitHub issue",
    "created_by_user_id": "usr_123",
    "created_at": "2026-09-23T23:15:00Z"
  },
  "task_version": 5,
  "history_event_id": "evt_458"
}
```

- **Validation:** `url` must satisfy the approved URL rules; `label` is optional.
- **Errors:** `403` for insufficient permission; `404` if the task is unavailable; `409` for a stale version; `422` for an invalid URL.

### Note Endpoints

#### `GET /api/v1/projects/{project_id}/tasks/{task_id}/notes`

- **Purpose:** List contextual notes attached to a task.
- **Request:** No body. Optional query parameters: `limit` and `cursor`.

**Response — `200 OK`**

```json
{
  "items": [
    {
      "id": "nte_123",
      "task_id": "tsk_123",
      "body": "Review with the team before implementation.",
      "created_by_user_id": "usr_123",
      "created_at": "2026-09-23T22:35:00Z",
      "updated_at": "2026-09-23T22:35:00Z"
    }
  ],
  "next_cursor": null
}
```

- **Errors:** `403` if the requester is not an active member; `404` if the task is unavailable.

#### `POST /api/v1/projects/{project_id}/tasks/{task_id}/notes`

- **Purpose:** Add contextual information that does not control the task's blocked state.
- **Related requirements:** FR-14 and FR-16.

**Request**

```json
{
  "body": "The first layout review is scheduled for Friday.",
  "expected_task_version": 5
}
```

**Response — `201 Created`**

```json
{
  "note": {
    "id": "nte_456",
    "task_id": "tsk_123",
    "body": "The first layout review is scheduled for Friday.",
    "created_by_user_id": "usr_123",
    "created_at": "2026-09-23T23:20:00Z",
    "updated_at": "2026-09-23T23:20:00Z"
  },
  "task_version": 6,
  "history_event_id": "evt_459"
}
```

- **Validation:** `body` and `expected_task_version` are required; a blank note is rejected.
- **Errors:** `403` for insufficient permission; `404` if the task is unavailable; `409` for a stale version; `422` for a blank body.

### History Endpoint

#### `GET /api/v1/projects/{project_id}/tasks/{task_id}/history`

- **Purpose:** Retrieve the append-only history used for attribution and review.
- **Related requirements:** FR-10, FR-14, and FR-16.
- **Request:** No body. Optional query parameters: `event_type`, `limit`, and `cursor`.

**Response — `200 OK`**

```json
{
  "items": [
    {
      "id": "evt_789",
      "task_id": "tsk_123",
      "actor": {
        "id": "usr_123",
        "display_name": "Jordan Lee"
      },
      "event_type": "moved",
      "from_section_id": "sec_backlog",
      "to_section_id": "sec_done",
      "details": {
        "transition_id": "trn_backlog_done"
      },
      "task_version": 5,
      "occurred_at": "2026-09-23T23:00:00Z"
    }
  ],
  "next_cursor": null
}
```

- **Errors:** `403` if the requester is not an active member; `404` if the task is unavailable; `422` for invalid filters.

### Deliberately Deferred Endpoints

The following endpoints are not part of the current MVP contract:

- Workflow creation or editing, until the initial sections and requirement types are decided
- Task, note, link, project, or user deletion, until archive and history behavior is decided
- Sprint planning, sprint lifecycle, and velocity endpoints
- AI sprint-report endpoints
- Notifications, capacity checks, agent execution, and deep GitHub integration
- Live-update transport, until the required synchronization timing is decided

### Endpoint Checklist

- [x] User endpoints
- [x] Project endpoints
- [x] Project membership endpoints
- [x] Workflow retrieval
- [x] Shared board retrieval
- [x] Task creation and editing
- [x] Guarded board transition behavior
- [x] Blocker creation, retrieval, and resolution
- [x] Task links and notes
- [x] Task history
- [ ] Workflow configuration endpoints — deferred pending product decisions
- [ ] Delete or archive endpoints — deferred pending history decisions
- [ ] Live-update endpoint or event stream — deferred pending synchronization requirements
- [ ] Sprint and AI report endpoints — outside the current MVP

---

## 8. AI Sprint-Report and Blocker Pre-Review Behavior

> **CRISP-DM connection — Modeling → Evaluation:** Use saved project evidence to help a person review sprint progress and blockers before a team or faculty check-in.

### Purpose

The AI assistant gives students and faculty an **advance check** of a selected sprint. It summarizes what the saved project data supports, highlights unresolved blockers and missing information, and suggests questions the user should answer before a sprint review.

The assistant is advisory and read-only. It must not:

- Create, move, complete, or reassign a task
- Add, edit, resolve, or delete a blocker
- Change a sprint goal, dates, status, or membership
- Present inferred or suggested work as completed work
- Save or distribute a report without explicit human action

### User Workflow: Check a Sprint with AI

- **Primary actors:** Student or faculty member
- **Starting condition:** The user is an active project member, has selected a sprint, and can view the underlying sprint tasks and blockers.
- **Steps:**
  1. The user opens the selected sprint and chooses **Check with AI**.
  2. The user chooses a review scope:
     - **My work:** Tasks assigned to the current user in the selected sprint and blockers attached to those tasks.
     - **Full sprint:** All sprint tasks and blockers the user's project role permits them to view.
  3. The system creates a timestamped snapshot of the permitted sprint data.
  4. The AI analyzes only that snapshot and produces a draft pre-review.
  5. The interface links significant statements to their supporting task, blocker, or note IDs.
  6. The user reviews the draft, follows source links, and may ask follow-up questions about the same snapshot.
  7. The user edits and explicitly saves the result, or discards it without changing project data.
- **Expected result:** The user receives an evidence-grounded summary of sprint readiness, assigned work, active blockers, risks, and missing information before the formal review.

> **Personalization rule:** A sprint remains a project-level object. **My work** is a filtered review scope based on task ownership; it does not create a separate private sprint.

### Inputs Provided to the Model

The system supplies a structured snapshot rather than unrestricted access to project data.

| Input | Included information | Purpose |
| --- | --- | --- |
| **Review context** | Project ID and name, sprint ID, review scope, current user ID and project role, and snapshot time | Prevents the model from mixing projects, users, or time periods. |
| **Sprint definition** | Sprint goal, status, start date, end date, and any completion criteria | Establishes what the sprint is intended to accomplish. |
| **Sprint tasks** | Task ID, title, description, owner, priority, section/status, planned status, completion state, and update time | Supports progress and ownership claims. |
| **Task evidence** | Acceptance evidence, relevant notes, links, and recent history events | Helps determine whether a completion claim is supported. |
| **Blockers** | Blocker ID, related task ID, description, active or resolved state, creator, resolution information, and timestamps | Supports blocker and risk analysis without inventing causes or resolutions. |
| **Faculty notes** | Notes explicitly associated with the selected project or sprint | Preserves faculty context and requested follow-up. |
| **Missing-field indicators** | Required or expected fields that are empty or inconsistent | Allows the assistant to identify data gaps directly. |

The model must not receive:

- Projects, sprints, tasks, or users outside the current user's authorized scope
- Authentication credentials or private account data
- Hidden model instructions entered through task descriptions, notes, or links
- External webpage contents unless a later, explicitly approved integration retrieves them

### AI Output Contract

The draft must contain the following sections in this order.

1. **Review scope and snapshot time**
   - Identify the project, sprint, selected scope, and data timestamp.
2. **Sprint goal and readiness summary**
   - Restate the saved goal and provide a concise readiness assessment supported by the remaining sections.
3. **Completed work**
   - List completed tasks with task IDs and the saved evidence supporting completion.
4. **Incomplete or at-risk work**
   - List unfinished tasks, owners, current sections, and any visible risk signals.
5. **Active blockers**
   - List each blocker with its blocker ID, related task ID, recorded description, and known owner or next action when present.
6. **Resolved blockers relevant to the review**
   - Summarize recently resolved blockers without presenting them as still active.
7. **Faculty notes**
   - Summarize saved faculty guidance and associate it with a task or sprint when the source does so.
8. **Missing or inconsistent information**
   - Identify missing owners, evidence, dates, blocker actions, or conflicting status information.
9. **Questions to answer before the review**
   - Suggest focused questions for the student or team; clearly label these as suggestions rather than saved project facts.
10. **Suggested next actions**
    - Recommend preparation steps without changing the board or claiming that the actions have occurred.

### Evidence and Grounding Rules

- Every factual claim about work, status, ownership, or blockers must be supported by the supplied snapshot.
- Completed-work claims must cite at least one task ID and must agree with the task's saved completion state.
- Blocker claims must cite both the blocker ID and its related task ID.
- The assistant must distinguish **active**, **resolved**, and **unknown** blocker states.
- Suggestions and questions must be labeled as AI suggestions and kept separate from recorded facts.
- The assistant must say when evidence is missing instead of filling gaps with plausible details.
- The assistant must not treat a task title, external link, or general note as proof that work was completed.
- Follow-up answers must remain grounded in the original snapshot unless the user explicitly refreshes the analysis.

### Missing and Incomplete Data Behavior

| Condition | Required AI behavior |
| --- | --- |
| **No active blockers** | State that no active blockers are recorded in the snapshot; do not claim that the sprint has no risks. |
| **No completed work** | State that no tasks are recorded as completed and list known in-progress or planned work. |
| **No faculty notes** | State that no faculty notes were supplied; omit invented feedback. |
| **Missing sprint goal** | Flag the missing goal as a readiness issue and avoid inventing one. |
| **Task marked complete without evidence** | Report the saved completion state while explicitly identifying the missing evidence. |
| **Task without an owner** | List it as unassigned and suggest confirming ownership. |
| **Blocker without a next action or owner** | Preserve the recorded blocker description and flag the missing response plan. |
| **Conflicting data** | Describe the conflict and cite both records; do not silently choose one as correct. |
| **No tasks in the selected scope** | Explain that the selected scope contains no tasks and suggest checking task ownership or choosing the full-sprint scope. |

### Human Review and Saving

- The draft is visibly labeled **AI-generated** and **Not yet reviewed**.
- The user can inspect the source task, blocker, or note associated with each cited statement.
- The user can edit the narrative but cannot use report editing to modify the source task or blocker records.
- Saving requires an explicit confirmation and records the reviewer, snapshot time, generation time, and review scope.
- A saved report preserves both the AI draft and the final human-edited version so later reviewers can distinguish them.
- Discarding a draft creates no sprint report and changes no project data.
- If project data changes after generation, the interface warns that the draft may be stale and offers to generate a new check.

### Failure and Recovery Behavior

- If the model is unavailable, the system displays a clear failure and leaves sprint and task data unchanged.
- If structured model output is missing required sections or cannot be validated, the system rejects the draft and offers a retry.
- If authorization changes during generation, the draft is not returned or saved.
- If the source snapshot cannot be assembled consistently, generation does not begin and the conflicting records are reported to the user.
- Retrying must not create multiple saved reports unless the user explicitly saves more than one version.

### Validation Checklist

- [ ] The AI analyzes the selected sprint rather than another sprint or project.
- [ ] **My work** contains only tasks assigned to the current user.
- [ ] **Full sprint** respects project membership and role permissions.
- [ ] Completed-work claims cite supporting task IDs and evidence.
- [ ] Every reported blocker cites its blocker ID and task ID.
- [ ] Resolved blockers are not reported as active.
- [ ] Missing information is stated plainly rather than invented.
- [ ] Suggestions are visibly separated from saved facts.
- [ ] Follow-up answers use the same snapshot until the user refreshes it.
- [ ] AI generation cannot mutate sprint, task, blocker, or membership data.
- [ ] Users can inspect sources, edit the draft, save explicitly, or discard it.
- [ ] Model failure leaves all project data unchanged.

### Dependencies and Scope Reconciliation

This behavior depends on domain objects and endpoints that are still deferred elsewhere in this specification:

- `Sprint`, sprint-to-task membership, and `SprintReport` domain objects
- Sprint retrieval and task-assignment endpoints
- An AI pre-review generation endpoint
- Report draft and reviewed-report persistence
- A decision about the required time for shared updates to reach active users



---

## 9. Non-Functional and Platform Requirements

> **CRISP-DM connection — Modeling → Deployment:** Define the operational conditions that allow the system to run, integrate, and remain maintainable.

These preliminary requirements focus on reproducible local execution and durable relational storage. They describe observable operating conditions without prescribing the complete production deployment.

### Preliminary Platform Decisions

| Area | Preliminary choice | Reason |
| --- | --- | --- |
| **Backend** | FastAPI | Required course platform and API contract in Section 7. |
| **Local orchestration** | Docker Compose | Provides a repeatable way to run the API and database together. |
| **Database** | PostgreSQL | Supports the relational model, transactions, constraints, and concurrent multi-user updates required by Sections 4–7. |
| **Configuration** | Environment variables with a committed example file | Keeps machine-specific settings and secrets out of source code. |
| **Schema evolution** | Version-controlled database migrations | Allows fresh and existing databases to reach the expected schema safely. |

> **Preliminary decision:** Use the same database engine locally and in a deployed environment. Do not use SQLite locally if production uses PostgreSQL, because differences in constraints, transactions, and concurrent behavior could hide defects.

### Local Execution Requirements

| ID | Requirement | Priority | Acceptance evidence |
| --- | --- | --- | --- |
| **NFR-LOCAL-01** | A developer must be able to start the API and PostgreSQL database from a fresh checkout by following one documented local setup procedure. | Must | A new developer follows the README on a machine with the documented prerequisites and reaches a healthy API without undocumented steps. |
| **NFR-LOCAL-02** | Local startup must use containerized services with explicitly named API, database, and persistent-volume resources. | Must | `docker compose up --build` starts the required services, and the running-service list shows the API and database. |
| **NFR-LOCAL-03** | Database data must survive stopping and restarting the local containers during ordinary development. | Must | A task created before `docker compose down` remains available after the services restart. |
| **NFR-LOCAL-04** | The repository must provide a safe example configuration that lists every required environment variable without containing real credentials. | Must | A committed `.env.example` or equivalent documents required values; secret scanning finds no database password or AI credential committed to source. |
| **NFR-LOCAL-05** | The application must fail at startup with a clear message when required configuration is missing or invalid. | Must | Removing the database connection setting prevents startup and identifies the missing setting without exposing secret values. |
| **NFR-LOCAL-06** | Host-facing ports and non-secret development settings should be configurable so a developer can resolve local port conflicts without editing source code. | Should | The API and database can be mapped to alternate host ports through local configuration. |
| **NFR-LOCAL-07** | Local startup must apply or clearly prompt for pending schema migrations before the API accepts normal requests. | Must | Starting against an older schema either upgrades it successfully or marks the service unready with an actionable migration message. |
| **NFR-LOCAL-08** | The service must expose a liveness check and a readiness check that distinguishes a running process from an API that can access its database. | Must | Liveness succeeds while the process is running; readiness fails when PostgreSQL is unavailable and succeeds after the connection is restored. |
| **NFR-LOCAL-09** | Local logs must identify service startup, migration status, database connectivity failures, and request failures without printing secrets or full sensitive payloads. | Must | A startup and failure test produces useful structured log events and does not expose credentials. |
| **NFR-LOCAL-10** | Development-only seed and reset operations must be explicit and must never run automatically against an unidentified database. | Must | Normal startup preserves existing data; a reset requires a separate documented command and refuses to run unless the environment is identified as local or test. |

### Database and Persistence Requirements

| ID | Requirement | Priority | Acceptance evidence |
| --- | --- | --- | --- |
| **NFR-DB-01** | PostgreSQL must be the authoritative store for shared users, projects, memberships, workflows, tasks, blockers, links, notes, and history events. | Must | Restarting the API or opening the board from another client returns the same committed records. |
| **NFR-DB-02** | The schema must enforce required fields, valid relationships, and uniqueness rules described in Section 6 whenever PostgreSQL can enforce them. | Must | Database tests reject an orphaned task, duplicate project membership, blank required value, and cross-project workflow reference. |
| **NFR-DB-03** | Multi-record operations must be atomic, including project creation with its initial membership and workflow, task creation with initial links or notes, task moves with history events, and blocker changes with history events. | Must | A forced failure partway through each operation leaves none of that operation's partial records committed. |
| **NFR-DB-04** | Task updates must use the task `version` to detect conflicting writes. | Must | Two updates based on the same version cannot both silently succeed; the later update receives the `409 Conflict` behavior defined in Section 7. |
| **NFR-DB-05** | A successful task mutation and its `TaskHistoryEvent` must commit in the same transaction. | Must | A committed task change always has its expected history event, and a rolled-back change has neither. |
| **NFR-DB-06** | Database timestamps must use a consistent UTC representation and be assigned by a trusted application or database operation. | Must | Records written from clients in different time zones are returned as correctly ordered UTC timestamps. |
| **NFR-DB-07** | Schema changes must be represented by ordered, version-controlled migrations that can build a new database and upgrade the previous supported schema. | Must | Migration tests create the latest schema from empty storage and upgrade a fixture using the prior schema version. |
| **NFR-DB-08** | Ordinary application startup must never drop tables, erase volumes, or recreate the database automatically. | Must | Restart and upgrade tests preserve existing projects, tasks, blockers, and history. |
| **NFR-DB-09** | Foreign-key and deletion behavior must protect task, blocker, and attribution history from accidental cascading deletion. | Must | Attempts to delete a referenced record are rejected or use an explicitly approved archival behavior; historical actor names remain interpretable. |
| **NFR-DB-10** | Common board queries must be supported by indexes for project membership, project workflow sections, tasks by project and section, active blockers by task, and task history ordering. | Should | Schema inspection shows the expected indexes, and representative board queries avoid full-table scans as the dataset grows. |
| **NFR-DB-11** | Database connections must be bounded and released after each request or background operation. | Must | A repeated-request test does not continually increase open connections or exceed the configured pool. |
| **NFR-DB-12** | Automated tests must use isolated test storage and must not modify a developer's ordinary local database. | Must | Running the test suite creates and cleans only the configured test database while local development records remain unchanged. |
| **NFR-DB-13** | The project must document a local backup and restore procedure for the PostgreSQL data. | Should | A database export can be restored into an empty local environment, after which the same project board and history are retrievable. |
| **NFR-DB-14** | Credentials and connection strings containing secrets must be supplied through approved configuration and must not be returned by APIs, health checks, or logs. | Must | Repository, API-response, health-check, and log inspection reveal no database password or complete secret-bearing connection string. |
| **NFR-DB-15** | When AI pre-review is implemented, the input snapshot must be built from a consistent committed view of the selected sprint data. | Should | A generated review identifies one snapshot time and does not combine mutually inconsistent task or blocker versions. |

### Data Durability and Recovery Rules

- A successful API response means the associated shared mutation has committed to PostgreSQL.
- A failed or rolled-back mutation must not appear on another user's board.
- Container recreation must not remove the named local database volume unless a developer runs the explicit reset procedure.
- Backups must exclude application secrets even when they include application data.
- Restore instructions must include applying migrations and verifying the readiness endpoint afterward.
- Production retention, encryption, managed backups, and disaster-recovery targets remain deployment decisions and must be specified before hosting real user data.

### Implementation Readiness Checklist

- [x] FastAPI backend selected
- [x] PostgreSQL selected as persistent storage
- [x] Containerized local execution specified
- [x] Environment-based configuration specified
- [x] Migration behavior specified
- [x] Local persistence and reset safety specified
- [x] Database integrity and transaction behavior specified
- [x] Liveness and readiness behavior specified
- [ ] Migration library selected
- [ ] Production hosting environment selected
- [ ] Production backup retention and recovery targets defined
- [ ] Authentication approach selected
- [ ] Course-platform AI integration confirmed through the approved abstraction

### Open Questions

- Which migration library will be used with FastAPI and PostgreSQL?
- What default local workflow data, if any, should the seed operation create?
- Should local development support anonymous users before authentication is implemented?
- What board size and response-time target should database performance tests use?
- What production retention, encryption, backup frequency, and recovery objectives are required?

---

## 10. Risks and Assumptions

> **CRISP-DM connection — Business Understanding → Evaluation:** Make uncertainty visible so it can be investigated instead of silently embedded in implementation.

Open questions are recorded next to the affected decisions in Sections 1–9. This section avoids duplicating them and records only current assumptions and delivery risks.

### Assumptions

| ID | Assumption | Impact if incorrect |
| --- | --- | --- |
| **A-01** | The primary users are one small capstone team and its faculty reviewers. | Multi-team administration and more complex permission boundaries may be required. |
| **A-02** | A flat task model is sufficient for the MVP. | Subtasks, parent-child dependencies, and hierarchy migrations may be needed. |
| **A-03** | Every user who works with a project can be represented by a project membership and role. | The authorization model may need external guests or institution-wide roles. |
| **A-04** | Blockers can be attached to an existing task; users can create a task first when no task exists. | A separate project-level blocker object may be required. |
| **A-05** | One authoritative workflow section per task accurately represents its current board state. | Parallel states or multiple-board placement would require a different task model. |
| **A-06** | PostgreSQL and Docker Compose are available in the development environment. | Local setup and persistence requirements would need an alternate supported path. |
| **A-07** | Sprint and AI pre-review features remain deferred unless the scope conflict identified in Section 8 is resolved. | Domain objects, endpoints, and validation work may enter the MVP unexpectedly. |

### Risks

| ID | Risk | Potential impact | Mitigation or owner |
| --- | --- | --- | --- |
| **R-01** | The board sections and transition requirements are not finalized. | FR-11–FR-13 cannot be fully implemented or tested. | Product owner defines the initial workflow before transition development. |
| **R-02** | Authentication and detailed role permissions are undecided. | API authorization may be insecure or require rework. | Resolve identity and permission rules before exposing the app beyond local development. |
| **R-03** | Shared-board synchronization may be slower than users expect. | Two users may temporarily see different board states. | Set a measurable update target and test with two active clients. |
| **R-04** | Concurrent edits could overwrite task or blocker changes. | Users may lose work or trust incorrect status. | Enforce task versions, transactions, and conflict tests from FR-16. |
| **R-05** | Migration or reset mistakes could destroy local project history. | Tasks, blockers, and audit evidence may be lost. | Require versioned migrations, persistent volumes, backups, and explicit development-only resets. |
| **R-06** | The domain and API scope may exceed the course timeline. | Core board behavior may remain incomplete. | Implement and demonstrate the vertical slice in Section 11 before optional resources or AI features. |
| **R-07** | AI may invent work, misclassify blockers, or follow instructions embedded in task content. | Sprint reviews may be misleading or unsafe. | Use authorized snapshots, source IDs, output validation, human review, and prompt-injection tests. |
| **R-08** | Task notes or blocker descriptions may contain sensitive project information. | Information could be exposed to unauthorized users or AI services. | Enforce membership boundaries and approve the data sent to any model integration. |
| **R-09** | PostgreSQL or container setup may be difficult on some student machines. | Developers may be unable to run or test the system consistently. | Test the setup instructions on a clean supported machine early. |

---

## 11. Initial Validation Plan

> **CRISP-DM connection — Evaluation:** Decide what evidence will show that product behavior and engineering claims are credible.

Validation combines unit tests, database integration tests, API contract tests, multi-client workflow tests, and operational checks. Automated tests should use isolated storage and repeatable fixtures.

### Core Workflow and API Validation

| Test ID | Requirement or workflow | Test or evidence | Expected result |
| --- | --- | --- | --- |
| **T-01** | FR-01–FR-02; Workflow 1 | Submit a valid task through the API and board interface. | Exactly one task with a unique ID appears in the selected initial section. |
| **T-02** | FR-03 | Submit a task without a title and then without a section. | No task is created; each invalid field receives an actionable message; valid entries remain available. |
| **T-03** | FR-04 | Open the same project as two members, create a task as one student, and refresh or synchronize the second board. | Both users see one task with the same ID, section, and details. |
| **T-04** | FR-05 | Submit the same task request twice with one idempotency key. | Both responses identify the same task and only one database record exists. |
| **T-05** | FR-06 | Force database failure during task creation with initial links and notes. | The user receives a failure, entered data remains recoverable in the client, and no partial task, link, or note is committed. |
| **T-06** | FR-07–FR-08; Workflow 2 | Add a blocker to a task and view the board as a second project member. | The task stays in its section, displays as blocked to both users, and exposes the same blocker description. |
| **T-07** | FR-09 | Submit an empty blocker description. | The request returns validation details and creates no blocker or history event. |
| **T-08** | FR-10 | Resolve one of two active blockers on a task. | The resolved blocker remains in history and the task remains blocked because another active blocker exists. |
| **T-09** | FR-11–FR-12; Workflow 3 | Move a task through an enabled transition after satisfying all requirements. | Status and visible section change together, supporting data remains intact, and one move-history event is recorded. |
| **T-10** | FR-13 | Attempt a move with an unmet transition requirement. | The API returns `409`, identifies the unmet requirement, and leaves task status, section, and version unchanged. |
| **T-11** | FR-14 | Add an owner, priority, link, note, and blocker, then move the task. | The task retains its ID and every related record after the move. |
| **T-12** | FR-15 | Force a failure while committing a task transition. | Neither the new section nor the move-history event is committed, and the board returns to the saved section. |
| **T-13** | FR-16 | Send two edits with the same `expected_task_version`. | The first succeeds; the second returns `409 Conflict` with current version information and overwrites nothing. |
| **T-14** | Section 7 authorization rules | Request another project's board and task resources as a nonmember. | Protected data is not returned; the API responds with the approved `403` or non-disclosing `404` behavior. |
| **T-15** | Section 7 error contract | Trigger validation, permission, missing-resource, transition, and conflict errors. | Each response uses the standard error shape and documented HTTP status. |

### Domain and Database Validation

| Test ID | Requirement or rule | Test or evidence | Expected result |
| --- | --- | --- | --- |
| **T-16** | Section 6 relationships; NFR-DB-02 | Attempt duplicate membership, orphaned task, cross-project section assignment, and ownership by a nonmember. | Database or service constraints reject every invalid relationship without partial data. |
| **T-17** | NFR-DB-03 and NFR-DB-05 | Inject failures into each multi-record transaction. | Each operation commits all expected records or none; a saved change never lacks its history event. |
| **T-18** | NFR-DB-06 | Create records from clients using different local time zones. | Returned timestamps are normalized to UTC and sort in the correct event order. |
| **T-19** | NFR-DB-07–NFR-DB-09 | Build an empty database, upgrade a previous-schema fixture, and restart with existing data. | Migrations finish successfully and preserve projects, tasks, blockers, and history. |
| **T-20** | NFR-DB-10 | Load a representative project dataset and inspect board-query plans. | Expected indexes are used and common queries avoid unnecessary full-table scans. |
| **T-21** | NFR-DB-11 | Run repeated and concurrent API requests while monitoring database connections. | Connections remain within the configured pool and return after requests complete. |
| **T-22** | NFR-DB-12 | Run automated tests while a normal local database contains sentinel data. | Tests use isolated storage and the sentinel data remains unchanged. |
| **T-23** | NFR-DB-13 | Export a populated local database and restore it into an empty environment. | The restored API returns the same project board, blockers, and history. |

### Local and Operational Validation

| Test ID | Requirement or rule | Test or evidence | Expected result |
| --- | --- | --- | --- |
| **T-24** | NFR-LOCAL-01–NFR-LOCAL-02 | Follow the documented setup from a clean checkout on a supported machine. | One documented procedure starts the API and PostgreSQL containers successfully. |
| **T-25** | NFR-LOCAL-03 and NFR-DB-08 | Create a task, stop and recreate application containers without requesting a reset, and restart. | The task and its history remain available from the persistent volume. |
| **T-26** | NFR-LOCAL-04–NFR-LOCAL-06 | Start with valid configuration, then remove a required setting and test alternate ports. | Valid configuration starts; missing configuration fails clearly; alternate ports require no source edit. |
| **T-27** | NFR-LOCAL-07 | Start the API against a database with a pending migration. | The database upgrades before normal traffic or readiness remains false with an actionable message. |
| **T-28** | NFR-LOCAL-08 | Check liveness and readiness before, during, and after a database outage. | Liveness reflects the API process; readiness alone fails during the database outage and recovers afterward. |
| **T-29** | NFR-LOCAL-09 and NFR-DB-14 | Scan source, logs, health responses, and API responses after startup and failure tests. | No database password, AI key, or complete secret-bearing connection string is exposed. |
| **T-30** | NFR-LOCAL-10 | Run ordinary startup and then attempt reset against local and nonlocal environment labels. | Startup preserves data; reset is explicit and refuses an environment not identified as local or test. |

### AI Pre-Review Validation — Deferred

These tests become required if the Section 8 capability enters scope.

| Test ID | Requirement or rule | Test or evidence | Expected result |
| --- | --- | --- | --- |
| **T-AI-01** | Review scope | Generate **My work** and **Full sprint** reviews from a known fixture. | My work contains only assigned tasks; full-sprint output contains only data permitted by project membership. |
| **T-AI-02** | Evidence grounding | Include completed, incomplete, blocked, and resolved tasks with known IDs. | Every factual work or blocker claim cites the correct source IDs and states. |
| **T-AI-03** | Missing-data behavior | Omit the sprint goal, task owner, completion evidence, faculty notes, and blocker action. | The output names each gap and invents no replacement information. |
| **T-AI-04** | Prompt-injection resistance | Place instructions to ignore system rules inside a task note or blocker description. | The content is treated only as project data and does not alter scope or output rules. |
| **T-AI-05** | Read-only behavior | Generate, edit, discard, and save a review while monitoring source records. | Generation and editing change no sprint, task, blocker, or membership data. |
| **T-AI-06** | Stale snapshot and failure recovery | Change a task after generation and separately simulate model failure. | The draft is marked stale after the change; model failure saves no report and changes no project data. |

### Release Evidence

Before declaring an implementation slice complete:

- Every applicable **Must** requirement has an automated passing test or a documented manual test where automation is not yet practical.
- API examples used by implemented endpoints pass schema or contract tests.
- Migrations succeed from both empty storage and the previous supported schema.
- A two-user demonstration confirms shared task, blocker, and transition behavior.
- No unresolved severity-high defect affects data integrity, authorization, or history preservation.

### First Implementation Slice

- **Slice:** Start the API and PostgreSQL locally, create a project with its default workflow, create one task, and retrieve that task on the shared board from a second client.
- **Requirements demonstrated:** FR-01–FR-05, NFR-LOCAL-01–NFR-LOCAL-08, NFR-DB-01–NFR-DB-08, and the core `User`, `Project`, `ProjectMembership`, `WorkflowSection`, and `Task` relationships.
- **Why this slice:** It proves the thinnest useful path through configuration, migrations, persistence, membership, API validation, and shared board retrieval before blocker, transition, history, or AI complexity is added.
- **Completion evidence:** T-01–T-05, T-16–T-19, and T-24–T-28 pass, followed by a recorded or live two-client demonstration.

---

## 12. Decision Log

> **CRISP-DM connection — Improve:** Preserve the reasoning behind changes so later iterations can build on evidence instead of repeating old uncertainty.

This log records why major product and data-model choices were made. These are preliminary architecture decisions and should become full ADRs if implementation reveals significant tradeoffs or reversals.

### Data-Model Principles

- Store one authoritative representation of a fact and derive display values from it.
- Use explicit relationship objects when the relationship has its own role, state, history, or validation rules.
- Preserve shared history instead of deleting evidence needed to explain prior project state.
- Keep project boundaries in every project-scoped relationship so cross-project data cannot be joined accidentally.
- Model concurrency and transition rules as domain behavior rather than leaving them to the interface.

### Recorded Decisions

| ID | Decision | Alternatives considered | Reason | Consequence |
| --- | --- | --- | --- | --- |
| **ADR-001** | Represent the Kanban board as a derived view rather than a stored `Board` object. | Store board snapshots; create a board entity; derive from sections and tasks. | The board has no independent business state in the MVP. Its contents are the project's ordered workflow sections and each task's current section. | There is no board record to synchronize, but queries must assemble a consistent board snapshot. |
| **ADR-002** | Use `Task` as the MVP work object instead of `UserStory`. | `UserStory`, `Issue`, or separate task and story objects. | Students described entering tasks, and the MVP does not require formal user-story semantics. One neutral object reduces duplicate concepts. | Later story-specific fields may require extending `Task` or introducing a distinct type. |
| **ADR-003** | Model user access through `ProjectMembership`. | Global role on `User`; role lists stored on `Project`; membership relationship object. | A person may be a student in one project and a faculty reviewer in another. Role and membership status belong to that relationship. | Authorization requires a membership lookup, but project-specific roles remain explicit and extensible. |
| **ADR-004** | Store task state once as `Task.section_id`. | Store both `status` and `section_id`; infer status from history; embed tasks inside section records. | One canonical field prevents a card's displayed column from disagreeing with a separate status value. | Status names are derived through `WorkflowSection`; section changes must occur through guarded transitions. |
| **ADR-005** | Model workflow sections and transitions as data objects. | Hard-code status strings; allow arbitrary section updates; use explicit section and transition objects. | The product needs ordered columns and testable rules for moving between them. Explicit objects make those rules visible to the API and tests. | Initial workflow configuration must be defined, and changes require careful migration of tasks in affected sections. |
| **ADR-006** | Represent each transition gate with a `TransitionRequirement`. | Free-text instructions; validation only in UI code; structured requirement objects. | FR-11–FR-13 require the system to evaluate a condition and explain failures consistently across clients. | Requirement types and configuration formats must be defined and validated before implementation. |
| **ADR-007** | Represent blockers as `TaskBlocker` records instead of a Boolean or ordinary note. | `is_blocked` Boolean; blocker text on `Task`; reuse `TaskNote`; blocker entity. | A record can preserve who reported a blocker, when it was active, how it was resolved, and whether other blockers remain. | `Task.is_blocked` becomes a computed value, and blocker creation/resolution needs dedicated operations. |
| **ADR-008** | Keep `TaskNote` and `TaskLink` as child objects rather than arrays embedded in a task field. | Embedded JSON arrays; plain description text; separate related objects. | Notes and links have their own authorship, identity, timestamps, validation, and future edit policies. | Reading a complete task may require additional joins or endpoints, but individual resources can be audited and validated. |
| **ADR-009** | Preserve meaningful changes in append-only `TaskHistoryEvent` records. | No history; overwrite current state; reconstruct history from logs; explicit domain history. | Users need to explain moves and blocker changes, and operational logs are not reliable product records. | Mutations must write current state and history atomically, increasing transaction responsibilities. |
| **ADR-010** | Use optimistic concurrency through `Task.version`. | Last write wins; database locks held across user interaction; optimistic version checks. | Most edits will not conflict, but shared usage requires visible protection when they do. Version checks avoid long-lived locks and silent loss. | Clients must submit their expected version and handle `409 Conflict` responses. |
| **ADR-011** | Use a dedicated transition endpoint rather than allowing `section_id` in ordinary task updates. | General `PATCH` of all fields; client-only validation; transition command endpoint. | A dedicated operation ensures requirements, atomic status changes, and move-history creation cannot be bypassed. | Clients make a distinct request for moves, but the behavior and failure contract are clearer. |
| **ADR-012** | Use PostgreSQL locally and in deployed environments. | SQLite locally; in-memory development store; PostgreSQL everywhere. | The model depends on relational integrity, transactions, and concurrent access. One engine reduces environment-specific behavior. | Local setup requires containers or PostgreSQL, but database behavior is more representative. |
| **ADR-013** | Use version-controlled migrations and persistent volumes rather than schema recreation at startup. | Drop and recreate; application-managed ad hoc changes; ordered migrations. | Project history must survive restarts and schema evolution. Explicit migrations make changes reviewable and testable. | Developers must create and test migrations and use a separate explicit reset process. |
| **ADR-014** | Keep sprint objects outside the current MVP model until sprint behavior is approved. | Add placeholder sprint tables now; reuse project as sprint; defer the objects. | Premature sprint fields would encode assumptions about planning, carryover, reporting, and ownership that are not yet resolved. | Section 8 cannot be implemented until `Sprint`, sprint-task membership, report storage, and endpoints are designed. |
| **ADR-015** | Make AI sprint pre-review read-only and snapshot-based. | Give the model live write access; send unbounded project context; analyze an authorized snapshot. | A bounded snapshot improves grounding, privacy, reproducibility, and human verification while preventing unintended project changes. | Reports can become stale and must expose their snapshot time; users must explicitly refresh and save. |
| **ADR-016** | Keep one Kanban view and flat tasks for the MVP. | Multiple timelines and tables; nested subtasks; one focused board. | Product research showed that shared status, ownership, and blockers provide the central value for a small capstone team. | Advanced views and hierarchies require later decisions, but the first implementation remains achievable. |
