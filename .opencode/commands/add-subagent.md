---
description: Add a new subagent to an existing project. Usage: /add-subagent <project-name> <role>
agent: build
---

Adding a new subagent to an existing project. Here are the details:

- **Project name**: $1
- **Subagent role**: $2

Execute the following steps:

## Step 1: Verify prerequisites

Before proceeding, confirm:
- The project folder `$1/` exists
- The project has an AGENTS.md at `$1/AGENTS.md`
- There is no existing subagent with the same role at `.opencode/agents/$1_$2.md`

If any prerequisite is missing, STOP and report the issue to the user.

## Step 2: Gather project context

Read the following files to understand the project and determine the best subagent configuration:
- `$1/AGENTS.md` — Project rules, context, and current subagent list
- `$1/docs/subtasks.md` — Subtask template to see what tasks need subagent routing
- `$1/docs/requirements.md` — Requirements to understand what the project involves
- `$1/docs/verification.md` — Verification criteria (if exists)
- Any existing subagent files in `.opencode/agents/` that match the pattern `$1_*.md` — to avoid overlapping responsibilities

Also read the subagent creation reference:
- `.opencode/agents/docs/project-setup/subagent-creation.md` — Tier selection logic and approval workflow
- `.opencode/agents/docs/project-setup/subagent-template.md` — Prompt template structure

## Step 3: Propose the subagent

Based on the project context and the requested role, propose a subagent to the user:

```
Proposed subagent: @$1_$2
Tier: [fast/balanced/coding/reasoning]
Model: opencode-go/<primary>
Fallback: opencode-go/<fallback1> [, opencode/<fallback2>]
Skills: [None, or list skills this subagent needs]
Purpose: [brief description based on project analysis]
Complexity: [why this tier was chosen]

Permissions:
  read: allow
  edit: [allow/deny]
  bash: [allow/deny]
  glob: [allow/deny]
  grep: [allow/deny]
  skill: [allow/deny]
  [task: allow if coordinator, otherwise omit]

Approve? (y/n)
```

Wait for explicit user approval. If rejected, stop — do not create the subagent file.

## Step 4: Create the subagent file

After approval, create `.opencode/agents/$1_$2.md` with a role-specific prompt following the template structure:

- Use frontmatter with `description`, `mode: subagent`, `model`, `# tier`, `# fallback`, `# skills` (empty by default), and `permission` fields
- Include a `## Project Context` section that instructs the subagent to read `$1/AGENTS.md` dynamically
- Include a `## Skills` section that lists any assigned skills (or "None assigned" if empty)
- Include a `## Your Responsibilities` section with role-specific tasks
- Include `## Progress Tracking`, `## SDD Awareness`, and `## Reference` sections following the template
- Set permissions based on the role (see `.opencode/agents/docs/project-setup/subagent-template.md` for role-based permission guidelines)
- **Important**: Replace all `<project>` and `<project-name>` placeholders with the actual project name `$1`

## Step 5: Update the project AGENTS.md

Add the new subagent to the "Project Subagents" section in `$1/AGENTS.md`:

```markdown
- **@$1_$2** - [purpose] (tier: [fast/balanced/coding/reasoning])
```

If there is no "Project Subagents" section yet, create it at the end of the file.

Also update `$1/docs/subtasks.md` if the new subagent should be routed to from any subtask steps. For example, if adding a tester subagent, relevant subtasks should be updated to route to `@$1_$2` instead of a generic role.

## Step 6: Commit the changes

Delegate to the **@git-committer** subagent with these instructions:
- Commit `.opencode/agents/$1_$2.md`, `$1/AGENTS.md`, and any updated docs to the main workspace repository
- Use commit message: `docs($1): add $2 subagent`