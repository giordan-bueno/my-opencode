---
description: Start working on a task within an existing project. Usage: /start-task <project-name> <task-folder-name>
agent: build
---

Starting a new task on an existing project. Here are the details:

- **Project name**: $1
- **Task folder name**: $2

Execute the following steps:

## Step 1: Verify prerequisites

Before starting, confirm:
- The project folder `$1/` exists
- The project has a coordinator subagent (`@${1}_coordinator`) defined in `.opencode/agents/`
- The task folder `$1/$2/` exists (the user should have already created it and cloned any external repos)
- The project has `$1/docs/subtasks.md` (subtask template)

If any prerequisite is missing, STOP and report the issue to the user with clear instructions on what to create.

## Step 2: Invoke the project coordinator

Delegate to the **@${1}_coordinator** subagent with these instructions:
- Project: $1
- Task: $2
- Task folder: $1/$2/
- Read `$1/docs/subtasks.md` to get the ordered subtask template
- Create or update the `Active Task` header in `$1/PROGRESS.md`:
  ```
  ---
  Active Task: $2
  Task Folder: $1/$2/
  ---
  ```
- Add a new task section below the header using the subtask template:
  ```
  ## $2
  - [ ] 1. <subtask from template>
  - [ ] 2. <subtask from template>
  [... all subtasks from template]
  ```
- Begin routing the first subtask to the appropriate project subagent