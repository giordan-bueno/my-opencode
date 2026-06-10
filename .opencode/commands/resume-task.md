---
description: Resume a paused task from history, restoring its progress. Usage: /resume-task <project-name> <task-folder-name>
agent: build
---

Resuming a previously paused task. The task's progress will be restored from the History section of PROGRESS.md.

- **Project name**: $1
- **Task folder name**: $2

Execute the following steps:

## Step 1: Verify prerequisites

Before resuming, confirm:
- The project folder `$1/` exists
- The file `$1/PROGRESS.md` exists
- There is a paused entry for `$2` in the History section of `$1/PROGRESS.md`
- If there is already an active task (Active Task is not `<none>`), ask the user whether to pause the current task first (using `/pause-task`) or cancel the resume

If the paused entry doesn't exist in History, report: "No paused task '$2' found in History. Available paused tasks: <list task names from History>". If the task folder `$1/$2/` doesn't exist, warn the user: "Task folder '$1/$2/' doesn't exist. You may need to recreate it and re-clone the external repo before resuming. Continue anyway?"

## Step 2: Restore the task from History

Read `$1/PROGRESS.md` and modify it as follows:

1. Find the History entry for `$2` (match the task name after `### ` and before ` — `)
2. Extract all the subtask lines and context notes from that entry, **removing** the `[PAUSED: <reason>]` suffix from the header
3. Set the Active Task header to point to the resumed task:
   ```
   ---
   Active Task: $2
   Task Folder: $1/$2/
   ---
   ```
4. Add the restored task section to the active area (before `## History`):
   ```
   ## $2
   - [x] 1. <completed subtask from history>
     - <context notes preserved as-is>
   - [ ] 2. <pending subtask from history>
   - [!] 3. <blocked subtask from history>
     - BLOCKED: <blocked reason preserved as-is>
   ... all subtasks preserved exactly as they were
   ```
5. Remove the entry from the History section (it's now active again)

The result should look like:
```markdown
# Progress Tracker — <project-name>

---
Active Task: fix-auth-bug
Task Folder: project-x/fix-auth-bug/
---

## fix-auth-bug
- [x] 1. Clone & navigate
  - Repo cloned to fix-auth-bug/external-repo/, branch fix-auth
- [x] 2. Identify issue
  - Bug: auth validator crashes on empty email → src/auth/validator.ts:42
- [!] 3. Implement fix
  - BLOCKED: awaiting clarification on empty string vs null behavior
- [ ] 4. Run tests
- [ ] 5. Verify — @<project>_reviewer

## History

### add-login-feature — 2026-06-08 16:45
... other entries
```

## Step 3: Notify the user and route to coordinator

After restoring the task:

1. Report to the user:
   > "Resumed task '$2' from History. Progress restored from where it was paused.
   > 
   > Status: [x] completed, [ ] pending, [!] blocked.
   > 
   > Note: If the external repo or task folder has changed since pausing, subagents should re-verify their context before continuing."

2. If there are `[!]` blocked subtasks, remind the user:
   > "This task has blocked subtasks. Resolve the blockers before continuing, or skip them with `/start-task`."

3. Delegate to the **@${1}_coordinator** subagent with these instructions:
   - Project: $1
   - Task: $2 (resumed)
   - Read `$1/PROGRESS.md` — the task has been restored from History with its previous progress
   - Check which subtask is next (first `[ ]` or `[!]` item) and begin routing
   - If a subtask was `[!]` blocked, ask the user for guidance before routing to a subagent

## Step 4: Commit the resumed progress

Delegate to the **@git-committer** subagent with these instructions:
- Commit the updated `$1/PROGRESS.md` to the main workspace repository
- Use commit message: `docs($1): resume task $2`

## Notes

- Resumed tasks preserve ALL previous progress — completed subtasks stay `[x]`, blocked subtasks stay `[!]`, pending subtasks stay `[ ]`
- If the task folder doesn't exist, the user needs to recreate it manually before subagents can work in it
- If the subtask template (`docs/subtasks.md`) has changed since the task was paused, the restored progress reflects the OLD template. The coordinator should be aware of this.
- Any blockers that existed when the task was paused are still present — the user should resolve them before the coordinator continues routing