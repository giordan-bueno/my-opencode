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
- The project has `$1/docs/requirements.md` (EARS requirements) — if missing, STOP and report that @project-setup should have created it

If any prerequisite is missing, STOP and report the issue to the user with clear instructions on what to create.

## Step 1b: Detect task prompt

Check if `$1/$2/task-prompt.md` exists in the task folder:
- **If it exists**: Read its contents. This is the task-specific prompt from outlier.ai — it contains instructions, context, and requirements unique to this task. Pass it to the coordinator in Step 2.
- **If it does NOT exist**: Ask the user: "No `task-prompt.md` found in `$1/$2/`. Do you have a task prompt from outlier.ai to provide? If yes, create the file at `$1/$2/task-prompt.md` with the prompt content before continuing." Wait for user response before proceeding.

## Step 2: Invoke the project coordinator

Delegate to the **@${1}_coordinator** subagent with these instructions:
- Project: $1
- Task: $2
- Task folder: $1/$2/
- Task prompt: (contents of `$1/$2/task-prompt.md` if it exists, otherwise note "No task-specific prompt provided — use project-level requirements only")

The coordinator should perform the following in sequence:

### 2a. Setup PROGRESS.md
- Read `$1/PROGRESS.md` to check if there's already an active task. If `Active Task` is not `<none>`, ask the user whether to switch tasks or continue the current one.
- Create or update the `Active Task` header in `$1/PROGRESS.md`:
  ```
  ---
  Active Task: $2
  Task Folder: $1/$2/
  Spec Status: pending
  ---
  ```
- Add a new task section below the header using the subtask template from `$1/docs/subtasks.md`. **If a task prompt was provided**, adapt the subtask list based on the task prompt's context — add task-specific steps, skip project steps that don't apply, and include task-specific requirements as additional R<n> IDs in the design. The last subtask must always be the **Verify** step routed to the reviewer subagent:
  ```
  ## $2
  - [ ] 1. <subtask from template>
  - [ ] 2. <subtask from template>
  [... all subtasks from template]
  - [ ] N. Verify — @${1}_reviewer: Run tests, check standards, confirm all requirements met
  ```

### 2b. Spec review gate
- Read `$1/docs/requirements.md` — if it doesn't exist or is empty, STOP and report that requirements must be created first (@project-setup should have created this)
- **If a task prompt was provided**: Extract task-specific requirements from it and add them to the design. Continue R<n> numbering from the project requirements (e.g., if project has R1-R5, task-specific requirements start at R6). Add a "Task Context" section to design.md summarizing the task prompt, and a "Task-Specific Requirements" section listing the new R<n> IDs.
- Create `$1/docs/design.md` for this task (approach, files to modify, R<n> coverage, alternatives, risks). See `.opencode/agents/docs/project-setup/sdd-reference.md` for the design format.
- Present `$1/docs/requirements.md`, `$1/docs/design.md`, and (if applicable) the task summary to the user for approval:
  > "Spec for task `$2`:
  > **Requirements**: [list R<n> IDs from requirements.md]
  > **Design**: [summary of approach, files, alternatives]
  > Approve spec and proceed? (y/n/changes)"
- **Do NOT route any coding subagents until the user approves the spec**
- If the user approves → set `Spec Status: approved` in PROGRESS.md header, begin subtask routing
- If the user requests changes → set `Spec Status: changes_requested`, report what needs changing, wait for user guidance

### 2c. Route subtasks
- After spec approval, begin routing the first subtask to the appropriate project subagent
- After each subagent completes, update PROGRESS.md with results and move to the next subtask
- After ALL subtasks (including Verify) are `[x]` and the reviewer approves, **report to the user for final approval** — do NOT mark the task complete automatically

See `.opencode/agents/docs/project-setup/sdd-reference.md` for the SDD process, EARS syntax, and traceability rules.