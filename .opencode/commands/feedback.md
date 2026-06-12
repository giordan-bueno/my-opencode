---
description: Apply QC feedback to a completed task. Creates a new feedback round with its own progress file and design. Usage: /feedback <project-name> <task-folder-name> <feedback-file>
agent: build
---

Applying QC feedback to a completed task. This creates a new feedback round with its own progress file, design, and subtasks, working in the same task folder and repo.

- **Project name**: $1
- **Task folder name**: $2
- **Feedback file**: $3 (e.g., feedback-1.md)

Execute the following steps:

## Step 1: Verify prerequisites

Before applying feedback, confirm:
- The project folder `$1/` exists
- The project has a coordinator subagent (`@${1}_coordinator`) defined in `.opencode/agents/`
- The task folder `$1/$2/` exists
- The original progress file `$1/progress-$2.md` exists and its Status is `[COMPLETED]` or `[COMPLETED: Feedback Round N]`
- The feedback file `$1/$2/$3` exists in the task folder
- If this is not the first feedback round, check that previous feedback progress files are completed (e.g., `progress-$2-fb1.md` must be `[COMPLETED]` before creating `progress-$2-fb2.md`)

If any prerequisite is missing, STOP and report the issue to the user with clear instructions.

**Determine the feedback round number**:
- List all `progress-$2-fb*.md` files in `$1/` to find the current round number
- If no feedback rounds exist, this is round 1 (suffix: `fb1`)
- If `progress-$2-fb1.md` exists and is completed, this is round 2 (suffix: `fb2`)
- And so on. The suffix is always `fb<N>` where N is the next round number.

## Step 2: Invoke the project coordinator

Delegate to the **@${1}_coordinator** subagent with these instructions:
- Project: $1
- Task: $2
- Task folder: $1/$2/
- Feedback round: fb<N> (the round number determined in Step 1)
- Feedback file: $1/$2/$3

The coordinator should perform the following in sequence:

### 2a. Create feedback progress file and update pointer

- Update `$1/PROGRESS.md` pointer:
  ```
  ---
  Active Task: $2-fb<N>
  Task Folder: $1/$2/
  Spec Status: pending
  ---
  ```
  Note: The Task Folder stays the same (same repo, same codebase). Only the Active Task name changes to include the feedback suffix.

- Create a new `$1/progress-$2-fb<N>.md` file:
  ```markdown
  # Task: $2 (Feedback Round <N>)

  ---
  Status: In Progress
  Created: [current date]
  Previous: progress-$2.md (or progress-$2-fb<N-1>.md for subsequent rounds)
  Feedback: $2/$3
  Design: docs/design-$2-fb<N>.md
  Task Prompt: $2/task-prompt.md (or "None")
  ---

  - [ ] 1. <subtask derived from feedback>
  - [ ] 2. <subtask derived from feedback>
  [... subtasks addressing the QC feedback]
  - [ ] N. Verify — @${1}_reviewer: Confirm all feedback items addressed, run tests, check standards
  ```

  **The coordinator should read the feedback file** and derive subtasks from it. The subtasks should address every item in the QC feedback. The Verify subtask must always be last.

- Mark the original (or previous feedback) progress file as completed if not already:
  - In `$1/progress-$2.md` (or `$1/progress-$2-fb<N-1>.md`), change Status to `[COMPLETED]`

### 2b. Spec review gate

- Read `$1/docs/requirements.md` to get project-level requirements
- Read `$1/$2/$3` (the feedback file) to extract feedback-specific requirements
- Read `$1/$2/task-prompt.md` if it exists, for original task context
- Create `$1/docs/design-$2-fb<N>.md` for this feedback round. This design should:
  - Include a **Feedback Context** section summarizing the QC feedback
  - Include a **Feedback Requirements** section with new R<n> IDs continuing from the original task's numbering (e.g., if the original task ended at R8, feedback requirements start at R9)
  - List files to modify and which R<n> they cover
  - Reference the previous design if relevant (e.g., "Building on the approach in design-$2.md, the feedback requires...")
- Present `$1/docs/requirements.md`, `$1/docs/design-$2-fb<N>.md`, and the feedback summary to the user for approval:
  > "Feedback Round <N> for task '$2':
  > **Feedback from**: $3
  > **New Requirements**: R<N+1>, R<N+2>, ... (from QC feedback)
  > **Design**: [summary of approach to address feedback]
  > Approve spec and proceed? (y/n/changes)"
- **Do NOT route any coding subagents until the user approves the spec**
- If the user approves → set `Spec Status: approved` in PROGRESS.md header, begin subtask routing
- If the user requests changes → set `Spec Status: changes_requested`, report what needs changing, wait for user guidance

### 2c. Route subtasks

- After spec approval, begin routing the first subtask to the appropriate project subagent
- After each subagent completes, update `$1/progress-$2-fb<N>.md` with results and move to the next subtask
- After ALL subtasks (including Verify) are `[x]` and the reviewer approves, **report to the user for final approval** — do NOT mark the task complete automatically

## Step 3: Commit the feedback setup

Delegate to the **@git-committer** subagent with these instructions:
- Commit `$1/PROGRESS.md`, `$1/progress-$2-fb<N>.md`, and `$1/docs/design-$2-fb<N>.md` to the main workspace repository
- If the original progress file status changed, commit that too
- Use commit message: `docs($1): apply feedback round <N> to task $2`

## Notes

- This command does NOT create a new task folder or clone a new repo. It works in the EXISTING task folder with the EXISTING repo.
- Feedback rounds are numbered sequentially: fb1, fb2, fb3, etc.
- Each feedback round gets its own progress file and design file, but works in the same task folder.
- The original progress file and design file remain intact as historical reference.
- R<n> IDs for feedback requirements continue from where the original task left off (e.g., if original task used R1-R8, feedback starts at R9).
- If QC sends another round of feedback after this one, run `/feedback` again with the next feedback file (e.g., feedback-2.md).