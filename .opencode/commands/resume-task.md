---
description: Resume a paused task by restoring the pointer and updating the progress file status. Usage: /resume-task <project-name> <task-folder-name>
---

Resuming a previously paused task. The PROGRESS.md pointer will be set to the task and the progress file status will change back to In Progress.

- **Project name**: $1
- **Task folder name**: $2

> **Run this with the `@${1}_coordinator` agent active** (it is a **primary** agent so it can pause to ask you questions and hold the gates; switch to it however your client does). The active primary resumes orchestration directly and delegates subtasks to worker subagents at **depth 1**; **no subagent invokes another subagent.**

Execute the following steps:

## Step 1: Verify prerequisites

Before resuming, confirm:
- The project folder `$1/` exists
- The file `$1/PROGRESS.md` exists
- The file `$1/progress-$2.md` exists — this is the paused task's progress file. If it doesn't exist, report: "No paused task '$2' found. Available progress files: <list progress-*.md files>."
- If there is already an active task (Active Task is not `<none>`), ask the user whether to pause the current task first (using `/pause-task`) or cancel the resume

If the task folder `$1/$2/` doesn't exist, warn the user: "Task folder '$1/$2/' doesn't exist. You may need to recreate it and re-clone the external repo before resuming. Continue anyway?"

## Step 2: Update pointer and progress file

Read `$1/progress-$2.md` and `$1/PROGRESS.md`, then:

1. Read the `Status` field from `$1/progress-$2.md` — it should be `[PAUSED: <reason>]`
2. Read the `Spec Status` field from `$1/progress-$2.md` — it preserves the spec status from when the task was paused (pending, approved, or changes_requested)
3. Update `$1/PROGRESS.md` pointer to:
   ```
   ---
   Active Task: $2
   Task Folder: $1/$2/
   Spec Status: <from progress file>
   ---
   ```
4. Update `$1/progress-$2.md` — change `Status: [PAUSED: <reason>]` to `Status: In Progress`
5. Update the **Context Summary** in `$1/progress-$2.md`:
   - `Current`: Update to reflect which subtask is next (first `[ ]` or `[!]` item)
   - `Next`: Update to preview the following subtask
   - `Blocker`: Set to `None` if all blockers were resolved, or keep existing blocker description if still unresolved

## Step 3: Notify the user and resume orchestration

After restoring the task (you are the active primary — the `@${1}_coordinator` agent — resuming the task directly):

1. Report to the user:
   > "Resumed task '$2'. Status changed from Paused to In Progress.
   >
   > Progress: [x] completed, [ ] pending, [!] blocked.
   >
   > Note: If the external repo or task folder has changed since pausing, subagents should re-verify their context before continuing."

2. If there are `[!]` blocked subtasks in the progress file, remind the user:
   > "This task has blocked subtasks. Resolve the blockers before continuing, or start a different task with `/start-task` and come back to this one later."

3. As the active primary (`@${1}_coordinator`), resume orchestration directly:
   - Project: $1
   - Task: $2 (resumed)
   - Read `$1/PROGRESS.md` — the pointer has been updated to this task
   - Read `$1/progress-$2.md` — the task has been restored from Paused to In Progress
   - Read `$1/docs/design-$2.md` — the design file for this task (should already exist from when the task was started)
   - **If `$1/$2/task-prompt.md` exists**: Read it for task-specific context and requirements
   - Check the `Spec Status` in the PROGRESS.md header:
     - If `approved`: Skip spec review and continue routing from the first incomplete subtask
     - If `pending`: Run the spec review phase — present the existing `design-$2.md` for approval (it was already created when the task was started) before routing coding subagents
     - If `changes_requested`: **Read the `Spec Changes Requested:` field from the progress file header** — it contains the user's verbatim feedback from when the task was paused. Report those exact changes to the user before proceeding (e.g., "Resumed task `$2` is in `changes_requested` state. The previously requested changes were: <verbatim content of Spec Changes Requested field>. Do you want to (a) revise the design now, (b) approve as-is, or (c) provide updated feedback?")
   - Check which subtask is next (first `[ ]` or `[!]` item in `progress-$2.md`) and begin routing
   - If a subtask was `[!]` blocked, ask the user for guidance before routing to a subagent

## Step 4: Commit the resumed progress

Delegate to the **@git-committer** subagent with these instructions:
- Commit `$1/PROGRESS.md` and `$1/progress-$2.md` to the main workspace repository
- Use commit message: `docs($1): resume task $2`

## Notes

- Resumed tasks preserve ALL previous progress — completed subtasks stay `[x]`, blocked subtasks stay `[!]`, pending subtasks stay `[ ]`
- If the task folder doesn't exist, the user needs to recreate it manually before subagents can work in it
- **If the subtask template (`docs/subtasks.md`) has changed since the task was paused**: The progress file reflects the ORIGINAL template from when the task was started. The coordinator should compare the current `docs/subtasks.md` with the subtask list in the progress file and inform the user of any discrepancies. The coordinator may add new subtasks to the progress file (marking them `[ ]`) if the template adds required steps, but should NOT remove completed subtasks or reorder existing ones.
- Any blockers that existed when the task was paused are still present — the user should resolve them before the coordinator continues routing
- Design files are per-task (`docs/design-<task-name>.md`) — they are never overwritten by other tasks, so the resumed task's design is intact
- Task prompt files (`<task-folder>/task-prompt.md`) remain in the task folder — no action needed during resume