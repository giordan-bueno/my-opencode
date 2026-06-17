---
description: Apply QC feedback to a completed task. Creates a new feedback round with its own progress file and design. Usage: /feedback <project-name> <task-folder-name> <feedback-file>
---

Applying QC feedback to a completed task. This creates a new feedback round with its own progress file, design, and subtasks, working in the same task folder and repo.

- **Project name**: $1
- **Task folder name**: $2
- **Feedback file**: $3 (e.g., feedback-1.md)

> **Run this while the `@${1}_coordinator` agent is active** (it is a **primary** agent — Tab to switch). The active primary orchestrates directly and delegates subtasks to worker subagents at **depth 1**; **no subagent invokes another subagent.**

Execute the following steps (you, the active primary, perform them — there is no separate coordinator subagent to invoke):

## Step 1: Verify prerequisites

Before applying feedback, confirm:
- The project folder `$1/` exists
- The project has a coordinator agent (`@${1}_coordinator`, a **primary** agent) defined in `.opencode/agents/`
- The task folder `$1/$2/` exists
- The original progress file `$1/progress-$2.md` exists and its Status is `[COMPLETED]` (the task must be completed before applying feedback)
- The feedback file `$1/$2/$3` exists in the task folder
- If this is not the first feedback round, check that previous feedback progress files are completed (e.g., `progress-$2-fb1.md` must be `[COMPLETED]` before creating `progress-$2-fb2.md`)

If any prerequisite is missing, STOP and report the issue to the user with clear instructions. Specifically:
- If the original task's status is not `[COMPLETED]`, report: "Task '$2' is not completed yet (status: <current status>). Complete the task using `/start-task` before applying feedback."
- If a previous feedback round is not completed, report: "Feedback round <N-1> is not completed yet. Complete it before starting a new feedback round."

**Determine the feedback round number**:
- List all `progress-$2-fb*.md` files in `$1/` to find the current round number
- If no feedback rounds exist, this is round 1 (suffix: `fb1`)
- If `progress-$2-fb1.md` exists and is completed, this is round 2 (suffix: `fb2`)
- And so on. The suffix is always `fb<N>` where N is the next round number.

## Step 2: Orchestrate the feedback round

As the **active primary** (the `@${1}_coordinator` agent), orchestrate directly. Context:
- Project: $1
- Task: $2
- Task folder: $1/$2/
- Feedback round: fb<N> (the round number determined in Step 1)
- Feedback file: $1/$2/$3

Perform the following in sequence:

### 2a. Create feedback progress file and update pointer

- **Check for an active task first**: read `$1/PROGRESS.md`. If `Active Task` is not `<none>` and is not this feedback round, ask the user whether to pause it (`/pause-task`) before starting the feedback round. Do not silently overwrite an in-progress pointer.
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
    Spec Status: pending
    ---

    ## Context Summary
    - Completed: None yet (feedback round)
    - Current: Awaiting spec approval
    - Next: Address feedback items after spec approval
    - Key files: To be reviewed
    - Blocker: None

    - [ ] 1. Explore codebase and report findings — @${1}_coder: Read relevant source files, identify changes from feedback, hidden dependencies, produce Code Exploration section in design file
    - [ ] 2. <subtask derived from feedback>
    [... subtasks addressing the QC feedback]
    - [ ] N-1. Write and run tests — @${1}_tester: Write tests covering feedback R<n> IDs per Test Plan + code-driven tests from exploration. Run test suite and report results
    - [ ] N. Verify — @${1}_reviewer: Review test results, check R<n> traceability for feedback items, verify standards

    ## Handoff Notes
    (Inherit relevant notes from original progress file, add new discoveries during feedback round)
    ```

  **The coordinator should read the feedback file** and derive subtasks from it. The subtasks should address every item in the QC feedback. The Verify subtask must always be last.

- Mark the original (or previous feedback) progress file as completed if not already (it should already be `[COMPLETED]` from the task's completion gate, but update it if needed):
  - In `$1/progress-$2.md` (or `$1/progress-$2-fb<N-1>.md`), ensure Status is `[COMPLETED]`

### 2b. Spec review gate

- Read `$1/docs/requirements.md` to get project-level requirements
- Read `$1/$2/$3` (the feedback file) to extract feedback-specific requirements
- Read `$1/docs/design-$2.md` (the original task design) to understand the context and find the last R<n> ID used — feedback R<n> IDs must continue from this number
- Read `$1/$2/task-prompt.md` if it exists, for original task context
- **Read the Handoff Notes from `$1/progress-$2.md`** (or the most recent feedback progress file) — copy relevant entries to the new progress file's Handoff Notes section. Environment variables, existing test baselines, reusable patterns, and warnings should carry forward to the feedback round.
- Create `$1/docs/design-$2-fb<N>.md` for this feedback round. This design should:
- Include a **Feedback Context** section summarizing the QC feedback
   - Include a **Feedback Requirements** section with new R<n> IDs continuing from the original task's numbering (e.g., if the original task ended at R8, feedback requirements start at R9)
   - Include a **Test Plan** section for feedback-specific tests
   - Leave a **Code Exploration** section placeholder for the coder to fill in after exploring the codebase
   - List files to modify and which R<n> they cover
  - Reference the previous design if relevant (e.g., "Building on the approach in design-$2.md, the feedback requires...")
- Present `$1/docs/requirements.md`, `$1/docs/design-$2-fb<N>.md`, and the feedback summary to the user for approval:
  > "Feedback Round <N> for task '$2':
  > **Feedback from**: $3
  > **New Requirements**: R<N+1>, R<N+2>, ... (from QC feedback)
  > **Design**: [summary of approach to address feedback]
  > Approve spec and proceed? (y/n/changes)"
- **Do NOT route any coding subagents until the user approves the spec**
- If the user approves → set `Spec Status: approved` in PROGRESS.md header, begin subtask routing (Step 4)
- If the user requests changes → set `Spec Status: changes_requested`, report what needs changing, wait for user guidance

## Step 3: Commit feedback setup files

After Step 2a completes (progress file created) and **before** presenting the spec in Step 2b, delegate to the **@git-committer** subagent (depth 1) with these instructions:
- Commit `$1/PROGRESS.md` and `$1/progress-$2-fb<N>.md` to the main workspace repository
- If the original progress file status changed, commit that too
- **Do NOT commit `$1/docs/design-$2-fb<N>.md` yet** — like the original task design, the feedback design is a draft until the user approves the spec. It is committed after approval (Step 4). This matches `/start-task`'s policy exactly.
- Use commit message: `docs($1): setup feedback round <N> for task $2`

Note: Setup files are committed before coding; the design is committed only after spec approval.

## Step 4: Route subtasks (after spec approval)

- **After spec approval, commit the feedback design file**: delegate to **@git-committer** (depth 1) to commit `$1/docs/design-$2-fb<N>.md` with message: `docs($1): spec approved for feedback round <N> — design`.
- As the active primary, route subtasks based on the progress file and spec approval, delegating each to the appropriate worker subagent at **depth 1**
- After each subagent completes, update `$1/progress-$2-fb<N>.md` with results and move to the next subtask
- After the coder completes the "Explore codebase" subtask, read the Code Exploration section in `docs/design-$2-fb<N>.md` and revise the subtask list if the exploration suggests changes
- After ALL subtasks (including Verify) are `[x]` and the reviewer approves, **report to the user for final approval** — do NOT mark the task complete automatically

## Notes

- This command does NOT create a new task folder or clone a new repo. It works in the EXISTING task folder with the EXISTING repo.
- Feedback rounds are numbered sequentially: fb1, fb2, fb3, etc.
- Each feedback round gets its own progress file and design file, but works in the same task folder.
- The original progress file and design file remain intact as historical reference.
- R<n> IDs for feedback requirements continue from where the original task left off (e.g., if original task used R1-R8, feedback starts at R9).
- If QC sends another round of feedback after this one, run `/feedback` again with the next feedback file (e.g., feedback-2.md).