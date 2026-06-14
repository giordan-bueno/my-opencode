# Task Workflow Reference

This workspace uses **Spec-Driven Development (SDD)**: requirements and design must be approved by the human before any code is written. Every requirement gets a stable `R<n>` ID that traces through design → subtasks → code → review. See `.opencode/agents/docs/project-setup/sdd-reference.md` for full details on EARS syntax, design format, and traceability rules.

## Task Lifecycle

Each project has a **subtask template** (`docs/subtasks.md`) defining the ordered steps every task must follow. For coding projects, the template includes an "Explore codebase" subtask before implementation, a "Write and run tests" subtask before the Verify step, and a final Verify step. The explorer subtask (typically the coder) reads the codebase and produces a Code Exploration report that may revise the subtask list and expand the test plan.

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

### Applying QC Feedback

When QC sends feedback on a completed task, use `/feedback` to create a new feedback round:

```
/feedback <project-name> <task-folder-name> <feedback-file>
```

Example: `/feedback project-x fix-auth-bug feedback-1.md`

1. **User creates feedback file** — e.g., `project-x/fix-auth-bug/feedback-1.md` with QC feedback
2. **User runs** `/feedback project-x fix-auth-bug feedback-1.md`
3. **Command** marks the original progress file as `[COMPLETED]`
4. **Command creates** `progress-<task>-fb1.md` (new progress file) and updates PROGRESS.md pointer
5. **Coordinator** reads the feedback file, derives new subtasks, creates `docs/design-<task>-fb1.md`
6. **R<n> numbering continues** — if original task ended at R8, feedback requirements start at R9
7. **Spec review gate** — coordinator presents feedback requirements and design for approval
8. **Subagents work** in the same task folder and repo, addressing the feedback
9. **Reviewer** verifies all feedback items addressed
10. **Completion gate** — coordinator reports to user for final approval
11. **If more feedback**: Create `feedback-2.md`, run `/feedback` again → `progress-<task>-fb2.md`, `design-<task>-fb2.md`

Feedback rounds are self-contained: own progress file, own design file, own spec review. But they work on the same codebase as the original task.

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
Spec Status: pending | approved | changes_requested
---

- [x] 1. <completed subtask>
  - <context notes from subagent>
  - Covers: R1, R2
- [ ] 2. <pending subtask>
- [!] 3. <blocked subtask>
  - BLOCKED: <description of what's blocking>
- [ ] N. Write and run tests — @<project>_tester: Write tests covering R<n> IDs per Test Plan, run test suite, report results
- [ ] N+1. Verify — @<project>_reviewer: Review test results, check R<n> traceability, verify standards, confirm all requirements met
```

**Feedback round progress files** (`progress-<task>-fb<N>.md`) include two additional fields:
```markdown
# Task: <task-name>-fb<N> (Feedback Round <N>)

---
Status: In Progress
Created: YYYY-MM-DD
Previous: progress-<task-name>.md (or progress-<task-name>-fb<N-1>.md)
Feedback: <task-folder>/feedback-<N>.md
Design: docs/design-<task-name>-fb<N>.md
Task Prompt: <task-folder>/task-prompt.md (or "None")
Spec Status: pending | approved | changes_requested
---
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
| `/add-subagent <project-name> <role>` | Add a new subagent to an existing project |
| `/start-task <project-name> <task-folder-name>` | Start a new task, verify prerequisites, create progress file, invoke coordinator |
| `/pause-task <project-name> <reason>` | Change progress file status to paused, reset pointer |
| `/resume-task <project-name> <task-folder-name>` | Restore pointer, change status back to In Progress |
| `/feedback <project-name> <task-folder-name> <feedback-file>` | Apply QC feedback: creates feedback progress file and design, runs spec review |