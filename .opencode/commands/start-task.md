---
description: Start working on a task within an existing project. Usage: /start-task <project-name> <task-folder-name>
---

Starting a new task on an existing project. Here are the details:

- **Project name**: $1
- **Task folder name**: $2

> **Run this with the `@${1}_coordinator` agent active.** It is a **primary** agent — that is what lets it pause to ask you questions and hold the human approval gates; switch to it however your client does. The active primary executes this command and orchestrates the task directly — it delegates individual subtasks to worker subagents (`@${1}_coder`, `@${1}_tester`, `@${1}_reviewer`) at **depth 1**. **No subagent invokes another subagent.** Driving from the coordinator (Balanced tier) keeps token cost low **and** loads the coordinator's prompt guardrails (Hard Rules, single-writer, spec/completion gates). You *can* run it from `build`, but `build` does **not** load those guardrails — it would orchestrate at higher cost and without the coordinator's built-in rules. Prefer the coordinator.

Execute the following steps (you, the active primary, perform them — there is no separate coordinator subagent to invoke):

## Step 1: Verify prerequisites

Before starting, confirm:
- The project folder `$1/` exists
- The project has a coordinator agent (`@${1}_coordinator`, a **primary** agent) defined in `.opencode/agents/`
- The task folder `$1/$2/` exists (the user should have already created it and cloned any external repos)
- The project has `$1/docs/subtasks.md` (subtask template)
- The project has `$1/docs/requirements.md` (EARS requirements) — if missing, STOP and report that @project-setup should have created it
- Read `$1/docs/subtasks.md` to identify the subagents referenced in the template (e.g., `@${1}_coder`, `@${1}_tester`, `@${1}_reviewer`). For each subagent referenced, check if its definition file exists in `.opencode/agents/`.

**Missing subagent handling — deferred vs hard block**:
- **If a referenced subagent is missing AND it is a coding subagent (`coder`, `tester`, `reviewer`) AND `$1/AGENTS.md` has a "Tech Discovery Status" section with any field marked "Discovery required"**: This is the deferred-subagent scenario. Do NOT STOP. Warn the user: "Subagent `@${1}_<role>` is not yet created because the tech stack was unknown at project setup. Tech Discovery will run in Step 1c and will recommend creating the missing subagents via `/add-subagent` before the task can proceed past Spec Review." Continue to Step 1b.
- **If a referenced subagent is missing AND no deferred-creation context exists** (Tech Discovery already complete, or the missing subagent is not a coding role): STOP and report: "Subagent `@${1}_<role>` is referenced in the subtask template but has not been created yet. Run `/add-subagent $1 <role>` to create it before starting the task."

If any other prerequisite is missing, STOP and report the issue to the user with clear instructions on what to create.

## Step 1b: Detect task prompt

Check if `$1/$2/task-prompt.md` exists in the task folder:
- **If it exists**: Read its contents. This is the task-specific prompt from outlier.ai — it contains instructions, context, and requirements unique to this task. Pass it to the coordinator in Step 2.
- **If it does NOT exist**: Ask the user: "No `task-prompt.md` found in `$1/$2/`. Do you have a task prompt from outlier.ai to provide? If yes, create the file at `$1/$2/task-prompt.md` with the prompt content before continuing." Wait for user response before proceeding.

## Step 1c: Tech Discovery

Check if the project's tech stack is incomplete (i.e., `docs/tech-stack.md` contains "Discovery required" sections or the AGENTS.md "Tech Discovery Status" says anything is unknown):

1. **Read `$1/AGENTS.md`** — look for a "## Tech Discovery Status" section. If it exists and any field says "Discovery required", proceed with tech discovery.
2. **Read `$1/docs/tech-stack.md`** — look for "## Discovery Required" sections. If present, proceed with tech discovery.
3. **Inspect the task folder for a cloned repo** — check if `$1/$2/` contains a subdirectory with `.git/` (an external repo).
4. **If an external repo exists**: Detect the tech stack by examining dependency files:
   - `package.json` → Node.js (check for frameworks: React, Vue, Next.js, Express, etc.)
   - `requirements.txt` / `pyproject.toml` / `setup.py` / `Pipfile` → Python (check for frameworks: Django, Flask, FastAPI, etc.)
   - `Cargo.toml` → Rust
   - `go.mod` → Go
   - `pom.xml` / `build.gradle` → Java (check for Spring Boot, Maven, Gradle)
   - `Gemfile` → Ruby (check for Rails, Sinatra)
   - `*.csproj` / `*.fsproj` → .NET (C#, F#)
   - `composer.json` → PHP (check for Laravel, Symfony)
   - Also check for: `Dockerfile`, `docker-compose.yml` (containerization), `.github/workflows/` (CI/CD), test config files (`jest.config.*`, `pytest.ini`, `vitest.config.*`, etc.)
5. **Read the task prompt** (if it exists) — it may contain CLI commands, language references, or framework mentions that reveal the tech stack.
6. **If tech stack info is discovered**:
    - Update `$1/docs/tech-stack.md` with the discovered information (replace "Discovery required" sections with actual content)
    - Update `$1/docs/testing.md` with the discovered test framework and runner commands
    - Update `$1/docs/standards.md` with project-specific conventions discovered from the repo
    - Update the "Tech Discovery Status" section in `$1/AGENTS.md` to mark discovered fields as "Known"
    - **Note**: This is initial shallow discovery from dependency files only. The coordinator will perform deeper discovery during code exploration (e.g., hidden dependencies, framework-specific patterns, test config discovered by reading actual code). Do not mark fields as fully known if only inferred from dependency files — leave room for the coordinator to refine.
    - Check if the project has coding subagents (coder, tester, reviewer). If NOT (they were deferred at setup because the tech stack was unknown):
      - This is the **expected one-time bootstrap** for a tech-deferred project — not an error. Report to the user: "Tech discovery found: [language/framework/test runner]. The coding subagents were deferred at setup; create all three now in one short sequence: `/add-subagent $1 coder`, then `/add-subagent $1 tester`, then `/add-subagent $1 reviewer` (each reads the freshly-discovered stack from `docs/tech-stack.md`). Then re-run `/start-task $1 $2` to continue."
      - **Then STOP — do not proceed to Step 2.** Do NOT create `progress-$2.md` or update the PROGRESS.md pointer yet; that avoids leaving a half-created task that the re-run would collide with. First commit only the Tech Discovery doc updates via **@git-committer** (message `docs($1): tech discovery for $2`) so they are not lost, then stop and wait for the user to create the subagents and re-run `/start-task`.
    - If coding subagents DO exist but their prompts lack tech-specific details, recommend `/add-subagent $1 <role> --update` to refresh them with the discovered information.
7. **If no external repo exists and tech stack is still unknown**: Report to the user: "No external repo found in the task folder and the tech stack is still unknown. The coordinator will proceed with available information. Consider cloning the repo before starting, or use `/add-subagent` after discovering the tech stack during code exploration."
8. **If no tech discovery is needed** (all fields known): Skip this step and proceed to Step 1d.

## Step 1d: Skill recommendations

Based on the tech stack (either known from PDFs or discovered in Step 1c), search the skills.sh ecosystem for relevant skills:

1. **Check which skills are already installed** — read `$1/AGENTS.md` → "Installed Skills" section, and the global `.agents/skills/` directory
2. **Search skills.sh for relevant skills** using the discovered tech stack keywords. **Use the `npx skills find <keyword>` CLI** — it queries the same skills.sh catalog as the website and prints each skill's name, install count, and `skills.sh` link. Use the CLI rather than the `https://www.skills.sh/?q=` URL: that web search renders results in-browser via JavaScript, so fetching it returns nothing.
   - By language: `npx skills find <language>` (e.g., python, rust, go)
   - By framework: `npx skills find <framework>` (e.g., react, django, nextjs)
   - By task type: `npx skills find tdd` (also debugging, testing, verification)
   - (Each result includes a `skills.sh/<owner>/<repo>/<skill>` link — open it in a real browser for the full page.)
   - Read `docs/skills-recommendations.md` for search methodology and role-based keyword suggestions
3. **Evaluate search results**: Prefer skills with 1K+ installs, security audit passes, and reputable sources. Read the skill description to verify relevance.
4. **Filter out already-installed skills** (both global and project-scoped)
5. **Present recommendations to the user**:
   > "Based on the discovered tech stack [[language/framework]], I searched skills.sh and found these relevant skills:
   > **Framework/language-specific**:
   > - [skill name from search results] — [description from skills.sh] → attach to: [coder/tester/reviewer]
   > **Role-based**:
   > - [skill name from search results] — [description from skills.sh] → attach to: [role]
   > 
   > Install with: `/add-skill $1 <source> --skill <name> --attach <role>`"
6. **If no relevant skills are found**: That's fine — skills are optional. Proceed to Step 2.
7. **If the user wants to install skills later**: That's fine — skills can be added at any time via `/add-skill` during a task. Proceed to Step 2.

## Step 2: Orchestrate the task

As the **active primary** (the `@${1}_coordinator` agent), orchestrate the task directly. Context:
- Project: $1
- Task: $2
- Task folder: $1/$2/
- Task prompt: (contents of `$1/$2/task-prompt.md` if it exists, otherwise note "No task-specific prompt provided — use project-level requirements only")

Perform the following in sequence. (The full orchestration playbook lives in the `@${1}_coordinator` agent prompt and `docs/task-workflow.md` — this command does not duplicate it.)

### 2a. Update PROGRESS.md pointer and create progress file

- Read `$1/PROGRESS.md` to check if there's already an active task. If `Active Task` is not `<none>`, ask the user whether to switch tasks or continue the current one.
- Update the `$1/PROGRESS.md` pointer:
  ```
  ---
  Active Task: $2
  Task Folder: $1/$2/
  Spec Status: pending
  ---
  ```
- Create a new `$1/progress-$2.md` file with the subtask list copied from `$1/docs/subtasks.md` in order. The template already contains the project's required steps:
    - For coding projects, `subtasks.md` already includes "Explore codebase" as the first implementation subtask and "Write and run tests" before the Verify step.
    - For TDD projects, `subtasks.md` already includes "Write fail-to-pass tests" (RED) before exploration and "Write pass-to-pass + code-driven tests" (GREEN) after implementation.
    - The last subtask is always **Verify**, routed to the reviewer.
    ```markdown
    # Task: $2

    ---
    Status: In Progress
    Created: [current date]
    Design: docs/design-$2.md
    Task Prompt: $2/task-prompt.md (or "None")
    Spec Status: pending
    Spec Changes Requested: <none — populated only if spec review returns `changes_requested`>
    ---

    ## Context Summary
    - Completed: None yet
    - Current: Awaiting spec approval
    - Next: <first subtask from docs/subtasks.md>
    - Key files: To be discovered
    - Blocker: None

    - [ ] 1. <first subtask from docs/subtasks.md, copied verbatim with assigned subagent>
    - [ ] 2. <second subtask from docs/subtasks.md>
    [... all subtasks from docs/subtasks.md in order]
    - [ ] N. Verify — @${1}_reviewer: Review test results, check R<n> traceability, verify standards, confirm all requirements met

    ## Handoff Notes
    (To be populated during work — environment, dependencies, warnings)
    ```
   **If a task prompt is provided**, adapt the subtask list based on the task prompt's context — add task-specific steps, skip project steps that don't apply, and include task-specific requirements as additional R<n> IDs in the design. The last subtask must always be the **Verify** step routed to the reviewer subagent.

   After the coder completes the "Explore codebase" subtask, read the Code Exploration section in `docs/design-$2.md` and revise the subtask list in the progress file if the exploration suggests changes (e.g., splitting subtasks, adding steps, reordering).

### 2b. Commit task setup files

Delegate to the **@git-committer** subagent (depth 1) right after creating the progress file above and **before** presenting the spec below:
- Commit `$1/PROGRESS.md` and `$1/progress-$2.md` to the main workspace repository.
- **Also commit any files modified during Step 1c (Tech Discovery)** if it ran (typically `$1/docs/tech-stack.md`, `$1/docs/testing.md`, `$1/docs/standards.md`, and the `$1/AGENTS.md` Tech Discovery Status section) — use `git status` to detect them.
- **Do NOT commit `$1/docs/design-$2.md` yet** — it stays a draft until the user approves the spec (committed in 2d).
- Commit message: `docs($1): start task $2 — progress file` (or `docs($1): start task $2 — progress file and tech discovery` if Tech Discovery also ran).

### 2c. Spec review gate
- Read `$1/docs/requirements.md` — if it doesn't exist or is empty, STOP and report that requirements must be created first (@project-setup should have created this)
- **If a task prompt was provided**: Extract task-specific requirements from it and add them to the design. Continue R<n> numbering from the project requirements (e.g., if project has R1-R5, task-specific requirements start at R6). Add a "Task Context" section to design summarizing the task prompt, and a "Task-Specific Requirements" section listing the new R<n> IDs.
- Create `$1/docs/design-$2.md` for this task (approach, files to modify, R<n> coverage, alternatives, risks). The design file is named per-task (e.g., `docs/design-fix-auth-bug.md`) so it is never overwritten by other tasks. See `.opencode/agents/docs/project-setup/sdd-reference.md` for the design format.
- Present `$1/docs/requirements.md`, `$1/docs/design-$2.md`, and (if applicable) the task summary to the user for approval:
  > "Spec for task `$2`:
  > **Requirements**: [list R<n> IDs from requirements.md]
  > **Task Context**: [brief summary of the task prompt, or "No task-specific prompt"]
  > **Design**: [summary of approach, files, alternatives]
  > Approve spec and proceed? (y/n/changes)"
- **Do NOT route any coding subagents until the user approves the spec**
- If the user approves → set `Spec Status: approved` in PROGRESS.md header, begin subtask routing
- If the user requests changes → set `Spec Status: changes_requested`, report what needs changing, wait for user guidance

### 2d. Route subtasks
- After spec approval, begin routing the first subtask to the appropriate project subagent
- **After spec approval, commit the design file**: Delegate to **@git-committer** to commit `$1/docs/design-$2.md` to the main workspace repository with message: `docs($1): spec approved for task $2 — design`
- After each subagent completes, update `$1/progress-$2.md` with results and move to the next subtask
- After ALL subtasks (including Verify) are `[x]` and the reviewer approves, **report to the user for final approval** — do NOT mark the task complete automatically

See `.opencode/agents/docs/project-setup/sdd-reference.md` for the SDD process, EARS syntax, and traceability rules.

*(Task setup is committed in 2b, before the spec gate; the per-task design is committed in 2d after approval.)*