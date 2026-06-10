---
description: Pause the current task and archive progress to history. Usage: /pause-task <project-name> <reason>
agent: build
---

Pausing the current task. The active task's progress will be archived to the History section of PROGRESS.md so it can be resumed later.

- **Project name**: $1
- **Reason**: $ARGUMENTS

Execute the following steps:

## Step 1: Verify prerequisites

Before pausing, confirm:
- The project folder `$1/` exists
- The file `$1/PROGRESS.md` exists
- There is an active task (Active Task is not `<none>`)

If there is no active task, report: "No active task to pause. PROGRESS.md shows Active Task: <none>."

## Step 2: Archive the active task to History

Read `$1/PROGRESS.md` and modify it as follows:

1. Read the current Active Task header and the active task section (everything from `## <task-name>` until the next `##` heading or the `## History` section)
2. Copy the entire active task section into the `## History` section, adding a timestamp and reason:
   ```
   ### <task-folder-name> — [YYYY-MM-DD HH:MM] [PAUSED: <reason>]
   - [x] 1. <completed subtask>
     - <context notes preserved as-is>
   - [ ] 2. <pending subtask>
   - [!] 3. <blocked subtask>
     - BLOCKED: <blocked reason preserved as-is>
   ... all subtasks preserved exactly as they are
   ```
3. Insert this entry at the **top** of the History section (newest first)
4. Delete the active task section from the main area
5. Reset the Active Task header:
   ```
   ---
   Active Task: <none>
   Task Folder: <none>
   ---
   ```

The result should look like:
```markdown
# Progress Tracker — <project-name>

---
Active Task: <none>
Task Folder: <none>
---

## History

### fix-auth-bug — 2026-06-09 14:30 [PAUSED: task expired on outlier]
- [x] 1. Clone & navigate
  - Repo cloned to fix-auth-bug/external-repo/, branch fix-auth
- [x] 2. Identify issue
  - Bug: auth validator crashes on empty email → src/auth/validator.ts:42
- [!] 3. Implement fix
  - BLOCKED: awaiting clarification on empty string vs null behavior
- [ ] 4. Run tests
- [ ] 5. Verify — @<project>_reviewer

### add-login-feature — 2026-06-08 16:45
- [x] 1. Clone & navigate
  - Repo cloned to add-login-feature/external-repo/, main
... etc
```

## Step 3: Commit the paused progress

Delegate to the **@git-committer** subagent with these instructions:
- Commit the updated `$1/PROGRESS.md` to the main workspace repository
- Use commit message: `docs($1): pause task — <reason>`

## Notes

- This command does NOT delete any task folders or external repos. They remain on disk in case the task is resumed later.
- Paused tasks can be resumed later with `/resume-task $1 <task-folder-name>`
- If you cannot re-claim the task on outlier.ai, the paused entry stays in History as an archive.