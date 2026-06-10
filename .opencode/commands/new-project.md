---
description: Set up a new outlier.ai project from watermarked PDFs. Usage: /new-project <project-name> <file1.pdf> [file2.pdf ...]
agent: build
---

A new outlier.ai project needs to be set up. Here are the details:

- **Project name**: $1
- **Watermarked PDF files**: $ARGUMENTS

Execute the following steps in order:

## Step 1: Clean PDFs, create project folder and .gitignore

Delegate to the **@pdf-cleaner** subagent with these instructions:
- Project name: $1
- PDF files to clean: all PDF paths provided after the project name
- The subagent should use the `delete-watermarks` tool for each PDF, saving clean versions into the `$1/` folder.
- The subagent should also create a `.gitignore` file inside the `$1/` folder with the standard project .gitignore template (ignore everything by default, un-ignore .gitignore, AGENTS.md, PROGRESS.md, docs/, docs/**, *.pdf).
- If this step fails, STOP and report the error to the user. Do not proceed to Step 2.

## Step 2: Commit project folder, .gitignore, and clean PDFs

After Step 1 completes successfully, delegate to the **@git-committer** subagent with these instructions:
- Commit the `$1/` folder (including .gitignore and clean PDFs) to the main workspace repository
- Use commit message: `feat($1): set up new project with cleaned PDFs`
- If this step fails, STOP and report the error to the user. Do not proceed to Step 3.

## Step 3: Create project AGENTS.md, reference docs, subtask template, and identify subagents

After Step 2 completes successfully, delegate to the **@project-setup** subagent with these instructions:
- Project folder: $1/
- Read all clean PDF files inside the `$1/` folder
- Create a **lean, principle-based** `$1/AGENTS.md` (~60 lines) that serves as a routing layer
- Create detailed reference docs in `$1/docs/` folder:
  - `subtasks.md` - Ordered subtask template defining the steps every task in this project must follow, with subagent assignments
  - `verification.md` - Objective criteria for what "done" looks like (what the reviewer checks against, extracted from PDF requirements)
  - `workflow.md` - Step-by-step workflows from the PDFs
  - `tech-stack.md` - Setup instructions, dependencies, configuration
  - `standards.md` - Coding standards, conventions, constraints
  - Additional docs as needed for complex topics
- Create `$1/PROGRESS.md` with initialized header and empty history section (Active Task: none, Task Folder: none)
- NOTE: `$1/.gitignore` was already created by @pdf-cleaner in Step 1 — do NOT recreate it
- The AGENTS.md should include: Project Context, Decision Rules, Core Behaviors, Autonomy Levels, Workspace Structure, Workflows, Progress Tracking section, User vs AI Responsibilities, and Reference pointers to the docs/ folder
- Follow the principle: "AGENTS.md is a routing layer, not an encyclopedia"
- **After creating AGENTS.md**, analyze the PDFs to identify distinct task types that warrant dedicated subagents
- **Always propose a coordinator subagent** (`$1_coordinator`) that orchestrates the other subagents and manages PROGRESS.md
- **Always propose a reviewer subagent** (`$1_reviewer`) for projects that involve coding — the reviewer verifies completed work, checks standards, runs tests. Tier: reasoning (`opencode-go/glm-5.1`). See `.opencode/agents/docs/project-setup/reviewer-template.md`
- Every subtask template in `$1/docs/subtasks.md` must end with a **Verify** step routed to the reviewer subagent
- For each identified subagent (one at a time):
  - Present proposal to user with: name (`$1_<role>`), tier (fast/balanced/coding/reasoning), primary model, fallback chain, purpose, and complexity reasoning
  - Wait for explicit approval before creating
  - If approved: Create `$1_<role>.md` in `.opencode/agents/` with role-specific prompt
  - If rejected: Skip without asking why, continue to next proposed subagent
- **No maximum limit**: Create as many subagents as the PDFs require
- **Non-overlapping responsibilities**: Each subagent must have a single, well-defined scope. No two subagents should handle the same task type.
- Use underscore naming convention: `$1_<role>.md`
- Model selection: fast tier for mechanical tasks, coding tier for implementation, reasoning tier for review/planning, balanced tier for setup/config and coordination
- After all subagents are processed, update `$1/AGENTS.md` with a "Project Subagents" section listing all created subagents
- If this step fails, STOP and report the error to the user. Do not proceed to Step 4.

## Step 4: Commit project setup files and subagents

After Step 3 completes successfully, delegate to the **@git-committer** subagent with these instructions:
- Commit the `$1/AGENTS.md`, `$1/PROGRESS.md`, `$1/docs/` folder, and any created subagent files (in `.opencode/agents/`) to the main workspace repository
- Note: `$1/.gitignore` and `$1/*.pdf` were already committed in Step 2 — do NOT re-add unless they changed
- Use commit message: `docs($1): add project rules, subtask template, and subagents from instruction PDFs`