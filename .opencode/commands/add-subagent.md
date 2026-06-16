---
description: Add or update a subagent for an existing project. Usage: /add-subagent <project-name> <role> [--update]
agent: build
---

Adding or updating a subagent for an existing project. Here are the details:

- **Project name**: $1
- **Subagent role**: $2
- **Mode**: $3 (if `--update`, refreshes an existing subagent with new context; otherwise creates a new one)

Execute the following steps:

## Step 1: Determine mode and verify prerequisites

**If mode is `--update`** (updating an existing subagent):
- Confirm the subagent file exists at `.opencode/agents/$1_$2.md`
- If it doesn't exist, STOP and suggest running without `--update` to create a new subagent
- Skip to Step 2

**If mode is create** (new subagent):
- Confirm:
  - The project folder `$1/` exists
  - The project has an AGENTS.md at `$1/AGENTS.md`
  - There is no existing subagent with the same role at `.opencode/agents/$1_$2.md`
- If any prerequisite is missing, STOP and report the issue to the user

## Step 2: Gather project context

Read the following files to understand the project and determine the best subagent configuration:
- `$1/AGENTS.md` — Project rules, context, and current subagent list (including "Tech Discovery Status" section if present)
- `$1/docs/subtasks.md` — Subtask template to see what tasks need subagent routing
- `$1/docs/requirements.md` — Requirements to understand what the project involves
- `$1/docs/tech-stack.md` — Tech stack and setup info (especially important if tech discovery was recently completed)
- `$1/docs/testing.md` — Testing strategy and framework (important for tester subagents)
- `$1/docs/verification.md` — Verification criteria (if exists)
- Any existing subagent files in `.opencode/agents/` that match the pattern `$1_*.md` — to avoid overlapping responsibilities (or to read the current subagent prompt if updating)

Also read the subagent creation reference:
- `.opencode/agents/docs/project-setup/subagent-creation.md` — Tier selection logic and approval workflow
- `.opencode/agents/docs/project-setup/subagent-template.md` — Prompt template structure

**For `--update` mode**: Also read the current subagent file at `.opencode/agents/$1_$2.md` to understand what needs to be refreshed. Focus on incorporating newly discovered tech stack information from `docs/tech-stack.md`, `docs/testing.md`, and `docs/standards.md` into the subagent's prompt.

## Step 3: Propose the subagent (or update plan)

**If mode is `--update`**: Show the user what will change:

```
Updating subagent: @$1_$2
Changes:
- [list specific sections that will be updated with new tech stack info]
- [e.g., "Adding Python/FastAPI context to prompt based on tech discovery"]
- [e.g., "Updating test framework references from 'Discovery required' to 'pytest'"]

Approve update? (y/n)
```

Wait for explicit user approval. If rejected, stop — do not modify the subagent file.

**If mode is create**: Propose a subagent to the user:

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

## Step 4: Create or update the subagent file

**If mode is `--update`**: Update the existing `.opencode/agents/$1_$2.md` file:
- Read the current file and update the role-specific prompt sections with newly discovered tech stack information
- Add project-specific context from `docs/tech-stack.md`, `docs/testing.md`, and `docs/standards.md`
- Keep the existing frontmatter (model, tier, permissions) unless the user explicitly requests changes
- Preserve any hand-tuned prompt sections that the user may have customized

**If mode is create**: Create `.opencode/agents/$1_$2.md` with a role-specific prompt following the template structure:

- Use frontmatter with `description`, `mode: subagent`, `model`, `# tier`, `# fallback`, `# skills` (empty by default), and `permission` fields
- Include a `## Project Context` section that instructs the subagent to read `$1/AGENTS.md` dynamically
- Include a `## Skills` section that lists any assigned skills (or "None assigned" if empty)
- Include a `## Your Responsibilities` section with role-specific tasks
- Include `## Progress Tracking`, `## SDD Awareness`, and `## Reference` sections following the template
- Set permissions based on the role (see `.opencode/agents/docs/project-setup/subagent-template.md` for role-based permission guidelines)
- **Important**: Replace all `<project>` and `<project-name>` placeholders with the actual project name `$1`

## Step 4b: Recommend skills for the new subagent

After creating a subagent (create mode only), search the skills.sh ecosystem for skills that would enhance this subagent:

1. **Determine search keywords** based on the subagent's role and the project's tech stack:
   - Role keywords: coder → `tdd`, `debugging`, `<language>`; tester → `tdd`, `testing`, `<test-framework>`; reviewer → `verification`, `code-review`; coordinator → `planning`, `workflow`
   - Tech stack keywords: the language and framework from `$1/docs/tech-stack.md` and `$1/AGENTS.md`
2. **Search skills.sh** using the keywords:
   - `https://www.skills.sh/?q=<keyword>` for each relevant keyword
   - Or CLI: `npx skills find <keyword>`
3. **Check already installed skills** (from `$1/AGENTS.md` → "Installed Skills" section)
4. **Filter and evaluate results**: Prefer skills with 1K+ installs, security audit passes, and reputable sources
5. **Present search results to the user**:
   > "I searched skills.sh for skills relevant to @$1_$2's role and this project's tech stack. Here's what I found:
   > - [skill name] — [description] ([install count] installs) → Install with: `/add-skill $1 <source> --skill <name> --attach $2`
   > - [skill name] — [description] ([install count] installs) → Install with: `/add-skill $1 <source> --skill <name> --attach $2`
   > 
   > You can also search for more skills at https://www.skills.sh/ or with `npx skills find <keyword>`."
6. **Do NOT auto-install skills** — only recommend. The user decides which to install via `/add-skill`.

## Step 5: Update the project AGENTS.md

**If mode is `--update`**: Update the "Tech Discovery Status" section in `$1/AGENTS.md` — mark the relevant fields as "Known" since the subagent now has the discovered tech context.

**If mode is create**: Add the new subagent to the "Project Subagents" section in `$1/AGENTS.md`:

```markdown
- **@$1_$2** - [purpose] (tier: [fast/balanced/coding/reasoning])
```

If there is no "Project Subagents" section yet, create it at the end of the file.

Also update `$1/docs/subtasks.md` if the new subagent should be routed to from any subtask steps. For example, if adding a tester subagent, relevant subtasks should be updated to route to `@$1_$2` instead of a generic role.

## Step 6: Commit the changes

Delegate to the **@git-committer** subagent with these instructions:

**If mode is `--update`**:
- Commit `.opencode/agents/$1_$2.md`, `$1/AGENTS.md`, and any updated docs to the main workspace repository
- Use commit message: `docs($1): update $2 subagent with discovered tech stack`

**If mode is create**:
- Commit `.opencode/agents/$1_$2.md`, `$1/AGENTS.md`, and any updated docs to the main workspace repository
- Use commit message: `docs($1): add $2 subagent`