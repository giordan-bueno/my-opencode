---
description: Update an existing outlier.ai project with new instruction PDFs. Usage: /update-project <project-name> <file1.pdf> [file2.pdf ...]
agent: build
---

An existing outlier.ai project needs to be updated with new instructions. Here are the details:

- **Project name**: $1
- **New watermarked PDF files**: $2 .. $N (all arguments after the project name)

Execute the following steps in order:

## Step 1: Clean new PDFs and add to project folder

Delegate to the **@pdf-cleaner** subagent with these instructions:
- Project name: $1
- PDF files to clean: $2 .. $N (all PDF paths after the project name — do NOT include the project name as a PDF path)
- The subagent should use the `delete-watermarks` tool for each PDF, saving clean versions into the existing `$1/` folder.
- Note: The `$1/` folder and `.gitignore` already exist — do NOT recreate them. Only clean and save the PDFs.
- If this step fails, STOP and report the error to the user. Do not proceed to Step 2.

## Step 2: Commit new clean PDFs

After Step 1 completes successfully, delegate to the **@git-committer** subagent with these instructions:
- Commit the new clean PDFs to the main workspace repository
- Use commit message: `chore($1): add cleaned PDFs from update`
- If this step fails, STOP and report the error to the user. Do not proceed to Step 3.

## Step 3: Update project files and manage subagents

After Step 2 completes successfully, delegate to the **@project-setup** subagent with these instructions:
- Project folder: $1/
- Read the existing `$1/AGENTS.md` first to understand current rules and structure.
- Read existing reference docs in `$1/docs/` to understand what's already documented.
- Read the existing `$1/docs/subtasks.md` to understand the current subtask template.
- Read the existing `$1/docs/requirements.md` to understand current requirements and R<n> IDs.
- **Read the existing `$1/PROGRESS.md`** to preserve its format and any existing task history. Do NOT reset or delete task history — only update the subtask template if it changed, and preserve the `Active Task` header format.
- Read the existing `$1/docs/verification.md` if it exists, to understand current verification criteria.
- Check existing subagents in `.opencode/agents/` that match the pattern `$1_*.md` to understand current subagent setup.
- Then read the newly added clean PDF files in the `$1/` folder.
- Compare the new PDF content with the existing AGENTS.md, reference docs, subtask template, and subagents.
- **Merge** the new information while maintaining the lean routing layer approach:
  - Update `$1/AGENTS.md` only if new principles, behaviors, or autonomy rules are needed (keep it ~60 lines)
  - Add or update reference docs in `$1/docs/` for detailed workflows, tech stack changes, or new standards
  - Update `$1/docs/requirements.md` with any new or changed requirements from the new PDFs, continuing R<n> numbering from the existing max ID
  - Update `$1/docs/subtasks.md` if the new PDFs introduce new steps or change the task workflow
  - Add any new rules, steps, or constraints not already present
  - Update any rules that have changed or been clarified in the new PDFs
  - Keep existing rules that are not contradicted by the new PDFs
  - Do NOT remove existing rules unless the new PDFs explicitly contradict them
- Remember: "AGENTS.md is a routing layer, not an encyclopedia"
- **Identify new subagents** needed based on new PDF content:
  - Analyze new PDFs for distinct task types not covered by existing subagents
  - If no coordinator subagent exists (`$1_coordinator`), propose one
  - For each new subagent needed (one at a time):
    - Present proposal to user with: name (`$1_<role>`), tier (fast/balanced/coding/reasoning), primary model, fallback chain, purpose, and complexity reasoning
    - Wait for explicit approval before creating
    - If approved: Create `$1_<role>.md` in `.opencode/agents/` with role-specific prompt. **Replace all `<project>` and `<project-name>` placeholders with the actual project name.**
    - If rejected: Skip without asking why, continue to next proposed subagent
  - **No maximum limit**: Create as many subagents as the PDFs require
  - **Non-overlapping responsibilities**: Each subagent must have a single, well-defined scope. No two subagents should handle the same task type.
  - Use underscore naming convention: `$1_<role>.md`
  - Model selection: fast for mechanical tasks, coding for coding/testing, reasoning for review/planning, balanced for setup/config and coordination
- **Update existing subagents** if their responsibilities have changed:
  - If new PDFs clarify or expand an existing subagent's role, update its prompt
  - If new PDFs contradict an existing subagent's instructions, update to reflect new information
- After all subagent changes, update `$1/AGENTS.md` "Project Subagents" section to reflect current state
- If this step fails, STOP and report the error to the user. Do not proceed to Step 4.

## Step 4: Commit updated project files and subagents

After Step 3 completes successfully, delegate to the **@git-committer** subagent with these instructions:
- Commit all updated files (`$1/AGENTS.md`, `$1/PROGRESS.md`, `$1/docs/`, any updated subagent files) to the main workspace repository
- Note: Only commit files that changed — check git status first
- Use commit message: `docs($1): update project rules, subtask template, and subagents from new instruction PDFs`