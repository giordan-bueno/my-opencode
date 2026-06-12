# Task Workflow Reference

This workspace uses **Spec-Driven Development (SDD)**: requirements and design must be approved by the human before any code is written. Every requirement gets a stable `R<n>` ID that traces through design → subtasks → code → review. See `.opencode/agents/docs/project-setup/sdd-reference.md` for full details on EARS syntax, design format, and traceability rules.

## Task Lifecycle

Each project has a **subtask template** (`docs/subtasks.md`) defining the ordered steps every task must follow. Every template ends with a **Verify** step handled by the reviewer subagent.

### Starting a New Task

1. **User creates task folder** — e.g., `project-x/fix-auth-bug/` and clones the repo
2. **User creates task prompt** (optional) — e.g., `project-x/fix-auth-bug/task-prompt.md` with the outlier.ai task instructions
3. **User runs** `/start-task project-x fix-auth-bug`
4. **/start-task verifies** prerequisites (project folder, coordinator, subtask template, task folder exist; requirements.md exists; detects task-prompt.md if present)
5. **Coordinator creates progress file** — `progress-fix-auth-bug.md` with the subtask list and sets the PROGRESS.md pointer
6. **Spec review gate** — The coordinator reads `docs/requirements.md`, reads `task-prompt.md` (if present), creates `docs/design-fix-auth-bug.md` (per-task, including Task Context and Task-Specific Requirements if task prompt exists), and presents both to the user for approval. No coding begins until specs are approved.
7. **User approves or requests changes** — If approved, `Spec Status: approved` and coding begins. If changes requested, `Spec Status: changes_requested` and the coordinator waits for guidance.
8. **Coordinator** routes subagents based on `progress-fix-auth-bug.md`
9. **Subagents** read `PROGRESS.md` to find the active task, then read `progress-fix-auth-bug.md` for subtask details, `docs/requirements.md` for R<n> IDs, and their assigned task folder
10. **Reviewer** verifies all work (last subtask): validates R<n> traceability, runs tests, checks standards, confirms requirements met
11. **Completion gate** — coordinator reports to the user for final approval. Task is not marked complete until the user confirms.
12. **Archive** — after user confirmation, `progress-fix-auth-bug.md` Status changes to `[COMPLETED]`, PROGRESS.md pointer resets to `<none>`

### Pausing a Task

If a task is interrupted (e.g., outlier task expires), use `/pause-task`:

```
/pause-task <project-name> <reason>
```

The progress file status changes to `[PAUSED: <reason>]` and the PROGRESS.md pointer resets to `<none>` so a new task can be started. No data is moved — just a status field change.

### Resuming a Task

Later, `/resume-task` restores the pointer and changes the status back:

```
/resume-task <project-name> <task-folder-name>
```

The PROGRESS.md pointer is set back to the task name, and `progress-<task-name>.md` Status changes from `[PAUSED: <reason>]` to `In Progress`. The coordinator continues from the first incomplete subtask.

## Progress Tracking Format

Progress tracking uses two levels of files:

**PROGRESS.md** (minimal pointer):
```markdown
# Progress Tracker — <project-name>

---
Active Task: <task-folder-name or "none">
Task Folder: <project-name>/<task-folder-name>/ or "none">
Spec Status: <pending | approved | changes_requested | "none">
---
```

**progress-<task-name>.md** (per-task details):
```markdown
# Task: <task-name>

---
Status: In Progress | [PAUSED: reason] | [COMPLETED]
Created: YYYY-MM-DD
Design: docs/design-<task-name>.md
Task Prompt: <task-folder>/task-prompt.md (or "None")
---

- [x] 1. <completed subtask>
  - <context notes from subagent>
  - Covers: R1, R2
- [ ] 2. <pending subtask>
- [!] 3. <blocked subtask>
  - BLOCKED: <description of what's blocking>
- [ ] N. Verify — @<project>_reviewer: Run tests, check standards, confirm all requirements met
```

## Subtask Status Markers

| Marker | Meaning | Action |
|--------|---------|--------|
| `[ ]` | Pending | Not yet started, ready for routing |
| `[x]` | Completed | Subagent finished successfully |
| `[!]` | Blocked | Subagent cannot proceed, needs user intervention |

## Task Status Values

| Status | Meaning | Action |
|--------|---------|--------|
| `In Progress` | Task is active | Coordinator routes subagents |
| `[PAUSED: reason]` | Task is paused | No routing, can be resumed with `/resume-task` |
| `[COMPLETED]` | Task is done | No routing, task is archived |

## Spec Status Values

| Status | Meaning | Action |
|--------|---------|--------|
| `pending` | Requirements and design presented, awaiting human approval |
| `approved` | Human approved specs, coding subagents can begin |
| `changes_requested` | Human requested changes, coordinator waiting for guidance |

When a subtask is `[!]` blocked, the subagent adds a `BLOCKED:` note explaining what's preventing progress. The coordinator reports this to the user and waits for guidance.

## Commands

| Command | Purpose |
|---------|---------|
| `/new-project <name> <file1.pdf> [file2.pdf ...]` | Create a new project from watermarked PDFs |
| `/update-project <name> <file1.pdf> [file2.pdf ...]` | Update an existing project with new PDFs |
| `/start-task <project-name> <task-folder-name>` | Start a new task, verify prerequisites, create progress file, invoke coordinator |
| `/pause-task <project-name> <reason>` | Change progress file status to paused, reset pointer |
| `/resume-task <project-name> <task-folder-name>` | Restore pointer, change status back to In Progress |