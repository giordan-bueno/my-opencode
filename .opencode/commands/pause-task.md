---
description: Pause the current task and update its progress file status. Usage: /pause-task <project-name> <reason>
agent: build
---

Pausing the current task. The task's progress file will be marked as paused and the PROGRESS.md pointer will be reset.

- **Project name**: $1
- **Reason**: $ARGUMENTS

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
3. Change the `Status` field in the progress file from `In Progress` to `[PAUSED: <reason>]`
4. Read the current `Spec Status` from the PROGRESS.md header
5. Reset `$1/PROGRESS.md` to:
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
---

- [x] 1. Clone & navigate
  - Repo cloned to fix-auth-bug/external-repo/, branch fix-auth
- [x] 2. Identify issue
  - Bug: auth validator crashes on empty email → src/auth/validator.ts:42
- [!] 3. Implement fix
  - BLOCKED: awaiting clarification on empty string vs null behavior
- [ ] 4. Run tests
- [ ] 5. Verify — @<project>_reviewer
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