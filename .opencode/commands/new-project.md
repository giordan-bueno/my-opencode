---
description: Set up a new outlier.ai project from watermarked PDFs. Usage: /new-project <project-name> <file1.pdf> [file2.pdf ...]
agent: build
---

A new outlier.ai project needs to be set up. Here are the details:

- **Project name**: $1
- **Watermarked PDF files**: $ARGUMENTS

Execute the following steps in order:

## Step 1: Clean PDFs and create project folder

Delegate to the **@pdf-cleaner** subagent with these instructions:
- Project name: $1
- PDF files to clean: all PDF paths provided after the project name
- The subagent should use the `delete-watermarks` tool for each PDF, saving clean versions into the `$1/` folder.

## Step 2: Commit new project folder and clean PDFs

After Step 1 completes successfully, delegate to the **@git-committer** subagent with these instructions:
- Commit the new `$1/` folder and clean PDFs to the main workspace repository
- Use commit message: `feat($1): set up new project with cleaned PDFs`

## Step 3: Create project AGENTS.md, reference docs, subtask template, and identify subagents

After Step 2 completes successfully, delegate to the **@project-setup** subagent with these instructions:
- Project folder: $1/
- Read all clean PDF files inside the `$1/` folder
- Create a **lean, principle-based** `$1/AGENTS.md` (~60 lines) that serves as a routing layer
- Create detailed reference docs in `$1/docs/` folder:
  - `subtasks.md` - Ordered subtask template defining the steps every task in this project must follow, with subagent assignments
  - `workflow.md` - Step-by-step workflows from the PDFs
  - `tech-stack.md` - Setup instructions, dependencies, configuration
  - `standards.md` - Coding standards, conventions, constraints
  - Additional docs as needed for complex topics
- Create `$1/PROGRESS.md` with initialized header (Active Task: none, Task Folder: none)
- Create `$1/.gitignore` that ignores everything by default but un-ignores: .gitignore, AGENTS.md, PROGRESS.md, docs/, docs/**, *.pdf
- The AGENTS.md should include: Project Context, Decision Rules, Core Behaviors, Autonomy Levels, Workspace Structure, Workflows, Progress Tracking section, User vs AI Responsibilities, and Reference pointers to the docs/ folder
- Follow the principle: "AGENTS.md is a routing layer, not an encyclopedia"
- **After creating AGENTS.md**, analyze the PDFs to identify distinct task types that warrant dedicated subagents
- **Always propose a coordinator subagent** (`$1_coordinator`) that orchestrates the other subagents and manages PROGRESS.md
- For each identified subagent (one at a time):
  - Present proposal to user with: name (`$1_<role>`), model (fast/balanced/reasoning), purpose, and complexity reasoning
  - Wait for explicit approval before creating
  - If approved: Create `$1_<role>.md` in `.opencode/agents/` with role-specific prompt
  - If rejected: Skip without asking why, continue to next proposed subagent
- **No maximum limit**: Create as many subagents as the PDFs require
- **Non-overlapping responsibilities**: Each subagent must have a single, well-defined scope. No two subagents should handle the same task type.
- Use underscore naming convention: `$1_<role>.md`
- Model selection: fast for mechanical tasks, reasoning for coding/testing, balanced for setup/config and coordination
- After all subagents are processed, update `$1/AGENTS.md` with a "Project Subagents" section listing all created subagents

## Step 4: Commit project setup files and subagents

After Step 3 completes successfully, delegate to the **@git-committer** subagent with these instructions:
- Commit the `$1/AGENTS.md`, `$1/PROGRESS.md`, `$1/.gitignore`, `$1/docs/` folder, and any created subagent files to the main workspace repository
- Use commit message: `docs($1): add project rules, subtask template, and subagents from instruction PDFs`