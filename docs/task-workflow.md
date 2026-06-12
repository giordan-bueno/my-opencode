# Task Workflow Reference

This workspace uses **Spec-Driven Development (SDD)**: requirements and design must be approved by the human before any code is written. Every requirement gets a stable `R<n>` ID that traces through design → subtasks → code → review. See `.opencode/agents/docs/project-setup/sdd-reference.md` for full details on EARS syntax, design format, and traceability rules.

## Task Lifecycle

Each project has a **subtask template** (`docs/subtasks.md`) defining the ordered steps every task must follow. Every template ends with a **Verify** step handled by the reviewer subagent.

### Starting a New Task

1. **User creates task folder** — e.g., `project-x/fix-auth-bug/` and clones the repo
2. **User creates task prompt** (optional) — e.g., `project-x/fix-auth-bug/task-prompt.md` with the outlier.ai task instructions
3. **User runs** `/start-task project-x fix-auth-bug`
4. **/start-task verifies** prerequisites (project folder, coordinator, subtask template, task folder exist; requirements.md exists; detects task-prompt.md if present)
5. **Spec review gate** — The coordinator reads `docs/requirements.md`, reads `task-prompt.md` (if present), creates `docs/design.md` (including Task Context and Task-Specific Requirements if task prompt exists), and presents both to the user for approval. No coding begins until specs are approved.
5. **User approves or requests changes** — If approved, `Spec Status: approved` and coding begins. If changes requested, `Spec Status: changes_requested` and the coordinator waits for guidance.
6. **Coordinator** reads `docs/subtasks.md`, creates/resets the `Active Task` header in `PROGRESS.md`, starts routing subagents
7. **Subagents** read `PROGRESS.md` and `docs/requirements.md` to find the active task, R<n> IDs they need to cover, and folder — do their work, update `PROGRESS.md` when done
8. **Coordinator** reads `PROGRESS.md` to determine next subtask and subagent
9. **Reviewer** verifies all work (last subtask): validates R<n> traceability, runs tests, checks standards, confirms requirements met
10. **Completion gate** — coordinator reports to the user for final approval. Task is not marked complete until the user confirms.
11. **Archive** — after user confirmation, the completed task moves to the `History` section of `PROGRESS.md`, Active Task resets to `<none>`

### Pausing a Task

If a task is interrupted (e.g., outlier task expires), use `/pause-task` to archive progress to History:

```
/pause-task <project-name> <reason>
```

The entry is tagged `[PAUSED: <reason>]` with all subtask status preserved. The Active Task resets to `<none>` so a new task can be started.

### Resuming a Task

Later, `/resume-task` restores the exact progress from History:

```
/resume-task <project-name> <task-folder-name>
```

The task section is moved from History back to the active area, the `[PAUSED: <reason>]` tag is removed, and the coordinator continues from the first incomplete subtask.

### PROGRESS.md Format

```markdown
# Progress Tracker — <project-name>

---
Active Task: <task-folder-name or "none">
Task Folder: <project-name>/<task-folder-name>/ or "none">
Spec Status: <pending | approved | changes_requested>
---

## <task-folder-name>
- [x] 1. <completed subtask>
  - <context notes from subagent>
  - Covers: R1, R2
- [ ] 2. <pending subtask>
- [!] 3. <blocked subtask>
  - BLOCKED: <description of what's blocking>
- [ ] N. Verify — @<project>_reviewer: Run tests, check standards, confirm all requirements met

## History

### completed-task — 2026-06-09 14:30
- [x] 1. <completed subtask>
  - <context notes>
- [x] N. Verify — APPROVED
  - All tests passing, code follows standards.

### paused-task — 2026-06-08 11:15 [PAUSED: task expired on outlier]
- [x] 1. <completed subtask>
- [!] 2. <blocked subtask>
  - BLOCKED: <description>
- [ ] 3. <pending subtask>
```

## Subtask Status Markers

| Marker | Meaning | Action |
|--------|---------|--------|
| `[ ]` | Pending | Not yet started, ready for routing |
| `[x]` | Completed | Subagent finished successfully |
| `[!]` | Blocked | Subagent cannot proceed, needs user intervention |

| `Spec Status: pending` | Requirements and design presented, awaiting human approval |
| `Spec Status: approved` | Human approved specs, coding subagents can begin |
| `Spec Status: changes_requested` | Human requested changes, coordinator waiting for guidance |

When a subtask is `[!]` blocked, the subagent adds a `BLOCKED:` note explaining what's preventing progress. The coordinator reports this to the user and waits for guidance.

## Commands

| Command | Purpose |
|---------|---------|
| `/new-project <name> <file1.pdf> [file2.pdf ...]` | Create a new project from watermarked PDFs |
| `/update-project <name> <file1.pdf> [file2.pdf ...]` | Update an existing project with new PDFs |
| `/start-task <project-name> <task-folder-name>` | Start a new task, verify prerequisites, invoke coordinator |
| `/pause-task <project-name> <reason>` | Archive active task to History with `[PAUSED: <reason>]` tag |
| `/resume-task <project-name> <task-folder-name>` | Restore paused task from History, continue from first incomplete subtask |