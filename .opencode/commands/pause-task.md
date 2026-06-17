---
description: Pause the current task and update its progress file status. Usage: /pause-task <project-name> <reason>
agent: build
---

Pausing the current task. The task's progress file will be marked as paused and the PROGRESS.md pointer will be reset.

- **Project name**: $1
- **Reason**: $2 .. $N (all arguments after the project name)

Execute the following steps:

## Step 1: Verify prerequisites

Before pausing, confirm:
- The project folder `$1/` exists
- The file `$1/PROGRESS.md` exists
- There is an active task (Active Task is not `<none>`)

If there is no active task, report: "No active task to pause. PROGRESS.md shows Active Task: <none>."

## Step 2: Update progress file and reset pointer

Read `$1/PROGRESS.md` to get the active task name, then:

1. Read the current `Active Task` from `$1/PROGRESS.md` (this gives you the task name, e.g., `fix-auth-bug`)
2. Read `$1/progress-<task-name>.md` — the per-task progress file
3. Change the `Status` field in the progress file from `In Progress` to `[PAUSED: <reason>]`. **Leave the progress file's `Spec Status:` and `Spec Changes Requested:` header fields untouched** — they are preserved in the per-task file so `/resume-task` can restore the exact spec state. (Only the PROGRESS.md *pointer's* `Spec Status` is reset to `<none>` below.)
4. Reset `$1/PROGRESS.md` to:
   ```
   ---
   Active Task: <none>
   Task Folder: <none>
   Spec Status: <none>
   ---
   ```

The result should look like:

**PROGRESS.md** (pointer reset):
```markdown
# Progress Tracker — <project-name>

---
Active Task: <none>
Task Folder: <none>
Spec Status: <none>
---
```

**progress-fix-auth-bug.md** (status changed):
```markdown
# Task: fix-auth-bug

---
Status: [PAUSED: task expired on outlier]
Created: 2026-06-11
Design: docs/design-fix-auth-bug.md
Task Prompt: fix-auth-bug/task-prompt.md
Spec Status: approved
Spec Changes Requested: <none>
---

## Context Summary
- Completed: Clone repo (R1), Identify issue (R2) — bug at src/auth/validator.ts:42
- Current: Implement fix (R3,R5) — blocked on @company/auth-lib API
- Next: Run tests → Verify
- Key files: src/auth/validator.ts, src/errors/handler.ts
- Blocker: Need clarification on empty string vs null handling

- [x] 1. Clone & navigate — @project-x_coder
  - Modified: .gitmodules, fix-auth-bug/external-repo/
  - Covers: R1
- [x] 2. Identify issue — @project-x_coder
  - Modified: docs/design-fix-auth-bug.md (Code Exploration section)
  - Covers: R2
  - For next subagent: Auth middleware registered before session middleware in app.ts:23
- [!] 3. Implement fix — @project-x_coder
  - BLOCKED: auth module uses custom validator from @company/auth-lib — need clarification
- [ ] 4. Run tests
- [ ] 5. Verify — @project-x_reviewer: Run tests, check standards, confirm all requirements met

## Handoff Notes
- Environment: Requires JWT_SECRET in .env (discovered in src/config.ts:8)
- Existing tests: tests/auth.test.ts (12 tests) must pass — regression baseline
- Reuse: logAction() in src/utils/logger.ts for audit logging (R4)
- Warning: Do NOT modify src/auth/session.ts — it handles session auth separately
```

## Step 3: Commit the paused progress

Delegate to the **@git-committer** subagent with these instructions:
- Commit `$1/PROGRESS.md` and `$1/progress-<task-name>.md` to the main workspace repository
- Use commit message: `docs($1): pause task <task-name> — <reason>`

## Notes

- This command does NOT delete any task folders or external repos. They remain on disk in case the task is resumed later.
- Paused tasks can be resumed later with `/resume-task $1 <task-folder-name>`
- Design files (`docs/design-<task-name>.md`) are per-task and remain in `docs/` — no action needed during pause since they are never overwritten by other tasks.
- Task prompt files (`<task-folder>/task-prompt.md`) remain in the task folder — no action needed during pause.
- The task's progress file stays in the project folder with `Status: [PAUSED: <reason>]` as a clear marker.