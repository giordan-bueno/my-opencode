# Task Workflow Reference

This workspace uses **Spec-Driven Development (SDD)**: requirements and design must be approved by the human before any code is written. Every requirement gets a stable `R<n>` ID that traces through design → subtasks → code → review. See `.opencode/agents/docs/project-setup/sdd-reference.md` for full details on EARS syntax, design format, and traceability rules.

## Orchestration model

Tasks are driven by the project's **coordinator**, which is a **primary** agent (`mode: primary`) — switch to it (Tab → `@<project>_coordinator`) and run the task commands from there. The coordinator holds the human approval gates (spec review, completion) and delegates each subtask to a **worker subagent** (`@<project>_coder`, `_tester`, `_reviewer`) at **depth 1**. **No subagent invokes another subagent** — workers complete their subtask and return to the coordinator. (The coordinator is primary precisely because a subagent cannot hold interactive approval gates and cannot reliably delegate to other subagents in OpenCode.)

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
12. **Archive** — after user confirmation, `progress-fix-auth-bug.md` Status changes to `[COMPLETED]`, PROGRESS.md pointer resets to `<none>`, and the coordinator commits both via @git-committer (message `docs(<project>): complete task <task-name>`)

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
Spec Changes Requested: <none — populated only if Spec Status is `changes_requested`, replaced with user's verbatim feedback>
---

## Context Summary
- Completed: <brief summary of completed subtasks with R<n> IDs, or "None yet">
- Current: <what's being worked on now, or "Starting">
- Next: <what comes next, or "To be determined">
- Key files: <most important files for this task, or "To be discovered">
- Blocker: <any blockers, or "None">

- [x] 1. <completed subtask> — @<project>_<role>
  - Modified: <files changed, with lines if relevant>
  - Covers: R1, R2
  - Key decisions: <important implementation decisions, or omit>
  - For next subagent: <critical info the next subagent needs, or omit>
- [ ] 2. <pending subtask>
- [!] 3. <blocked subtask>
  - BLOCKED: <description of what's blocking>
- [ ] N. Write and run tests — @<project>_tester: Write tests covering R<n> IDs per Test Plan, run test suite, report results
- [ ] N+1. Verify — @<project>_reviewer: Review test results, check R<n> traceability, verify standards, confirm all requirements met

## Handoff Notes
- Environment: <env vars, config, setup requirements discovered during work>
- Existing tests: <test suites that must keep passing, regression baseline>
- Reuse: <existing utilities, patterns, or modules that should be reused>
- Warning: <things to avoid, hidden dependencies, non-obvious constraints>
```

**Context Summary** is updated by every subagent after completing work. It provides a 5-line executive summary that lets any subagent understand the task state without reading the full progress file. Key guidelines:
- Keep it to 5 lines maximum
- Update `Current` and `Next` after each subtask completion
- Update `Key files` and `Blocker` as discoveries are made during work
- Remove `Blocker` line or set to `None` when resolved

**Structured Handoff** fields under each completed subtask ensure critical information flows between subagents:
- **Modified** (required): Files changed during this subtask, with line numbers if relevant
- **Covers** (required): R<n> IDs addressed by this subtask
- **Key decisions** (optional): Important implementation choices that affect future work
- **For next subagent** (optional): Critical information the next subagent needs but might not discover on its own

**Handoff Notes** at the bottom accumulate important environment-level information discovered during the task. Any subagent can add entries. These persist across the entire task lifecycle.

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

## Context Summary
- Completed: None yet
- Current: Starting feedback round
- Next: Explore codebase changes from feedback
- Key files: <same as original task, or updated>
- Blocker: None
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

**Source of truth**: `Spec Status` is duplicated in two places — the `PROGRESS.md` pointer (a convenience cache for "what is active right now") and the per-task `progress-<task-name>.md` header (authoritative). `/pause-task` resets the pointer's copy to `<none>` but preserves the per-task copy (plus `Spec Changes Requested`), so `/resume-task` restores the exact spec state from the per-task file. If the two ever disagree, **the per-task `progress-<task-name>.md` wins**.

When a subtask is `[!]` blocked, the subagent adds a `BLOCKED:` note explaining what's preventing progress. The coordinator reports this to the user and waits for guidance.

## Test Failure Protocol

This is the **canonical** retry procedure for failing tests. The coordinator template references this document; do not duplicate the protocol elsewhere.

When the tester reports failing tests, the coordinator follows a structured retry procedure:

1. **Attempt 1**: Route to coder to fix the failing tests. Coder reads tester's notes, fixes implementation, updates progress. After the fix, **route back to the tester to re-run the suite** (tests never auto-rerun — the tester must be invoked again).
2. **Attempt 2**: If tests still fail after re-run, route to coder again with the new error output and more specific instructions. Then route back to tester.
3. **Attempt 3**: If tests still fail, route to coder one final time for thorough diagnosis. Then route back to tester.
4. **After 3 failed attempts**: Report to the user with options:
   - Provide additional guidance and re-route to coder
   - Skip the failing test and continue (mark as known issue in progress — see format below)
   - Route to reviewer to evaluate if the test is critical or can be deferred

Each attempt is recorded in the progress file's subtask notes (e.g., "Attempt 2/3: Fixed null check, test still failing with different error"). The coordinator tracks attempt count per failing test.

### Known-Issue Format

When the user decides to skip a failing test (option 2 above), record it under the test subtask in `progress-<task-name>.md` using this format so the reviewer can verify it during the Verify step:

```markdown
- [x] N. Write and run tests — @<project>_tester
  - Modified: tests/auth.test.ts (12 test cases), tests/errors.test.ts (4 test cases)
  - Covers: R1, R2, R6
  - Results: 11 passed, 1 failed
  - **Known Issue (skipped per user decision YYYY-MM-DD)**:
    - Test: "should return structured error for empty email"
    - Covers: R6
    - Reason for skip: [verbatim user reason, e.g., "downstream API not yet deployed, will be revisited in feedback round"]
    - Re-test plan: [what unblocks re-testing this, e.g., "Re-enable when AUTH-API-2 ships"]
```

The reviewer must flag any unresolved known issues in the Verify subtask and surface them in the completion gate summary to the user.

## Subagent Failure Recovery

If a subagent produces no output, crashes, or leaves the progress file in an inconsistent state (no `[x]` or `[!]` marker after starting):

1. **Check for partial changes**: Read the progress file and relevant code files to assess what was completed
2. **If no changes were made**: Re-route the same subtask to a fresh subagent invocation
3. **If partial changes were made**: Mark the subtask as `[!]` blocked with a note like "Subagent failed mid-task — partial changes detected in [files]. Manual review needed."
4. **Report to the user**: Describe what happened, what was partially completed, and recommend next steps

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