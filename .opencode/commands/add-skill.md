---
description: Install a skill from skills.sh and optionally attach it to a subagent. Usage: /add-skill <project> <source> [--skill <name>] [--attach <role>] or /add-skill --global <source> [--skill <name>]
agent: build
---

Install a skill from the skills.sh ecosystem and optionally attach it to a project subagent.

- **Scope**: `$1` (if `--global`, then global; otherwise project-scoped)
- **Source**: The skills.sh source (e.g., `mattpocock/skills`, `vercel-labs/agent-skills`, or a GitHub URL)
- **Skill name**: `$SKILL` (specific skill from the source, or all skills if omitted)
- **Attach to role**: `$ATTACH` (subagent role to attach the skill to, e.g., `coder`, `tester`)

## Step 1: Determine scope and validate

**If `--global` flag** (first argument is `--global`):
- Install to workspace root `.agents/skills/` directory
- Global skills are available to all projects and all subagents
- Skip project validation — global skills don't need a project folder
- Set `SCOPE=global` and `SKILLS_DIR=.agents/skills/`

**Otherwise** (project-scoped):
- `$1` is the project name (e.g., `my-project`)
- Confirm the project folder `$1/` exists and has an `AGENTS.md` at `$1/AGENTS.md`
- Set `SCOPE=project` and `SKILLS_DIR=$1/.agents/skills/`
- If the project's `.agents/skills/` directory doesn't exist, create it

## Step 1b: Discover skills (if source is unknown)

If the user doesn't know which skill to install, help them discover relevant skills:

1. **Search skills.sh by keyword**: Use `https://www.skills.sh/?q=<keyword>` with relevant keywords based on the project's tech stack and the subagent's role. Try multiple keywords:
   - Language: `?q=python`, `?q=rust`, `?q=go`, `?q=typescript`, `?q=java`
   - Framework: `?q=react`, `?q=django`, `?q=nextjs`, `?q=fastapi`, `?q=spring`
   - Task type: `?q=tdd`, `?q=debugging`, `?q=testing`, `?q=verification`, `?q=code-review`
2. **Use CLI search if available**: `npx skills find <keyword>`
3. **Present results**: Show the user the skill name, source, description, install count, and security audit status from the search results
4. **Let the user choose**: The user selects which skill(s) to install, then proceed to Step 2 with the chosen source and skill name

If the user already knows the source and skill name, skip this step and proceed directly to Step 2.

## Step 2: Parse source and skill name
- **Source** (required): The skills.sh package source. Examples:
  - `mattpocock/skills` — GitHub shorthand
  - `vercel-labs/agent-skills` — GitHub shorthand
  - `anthropics/skills` — GitHub shorthand
  - `https://github.com/owner/repo` — Full GitHub URL
  - `./my-local-skills` — Local path (for custom skills)
- **Skill name** (optional, via `--skill`): Specific skill to install from the source. If omitted, all skills from the source are installed. Examples:
  - `--skill tdd` — Install only the tdd skill
  - `--skill frontend-design` — Install only the frontend-design skill
  - Omitted — Install all skills from the source
- **Attach role** (optional, via `--attach`): Subagent role to attach the skill to. Only valid for project-scoped installs. Examples:
  - `--attach coder` — Attach to `<project>_coder` subagent
  - `--attach tester` — Attach to `<project>_tester` subagent

## Step 3: Install the skill

Run the skills CLI to install the skill:

**For project-scoped** (default):
```bash
npx skills add <source> --skill <name> -a opencode -p <project-dir> -y
```

**For global**:
```bash
npx skills add <source> --skill <name> -a opencode -g -y
```

If the `npx skills` command is not available, inform the user: "The skills CLI is not installed. Install it with `npm install -g skills` or use `npx skills` directly." Then try with `npx`.

After installation, verify the skill files exist in the target `SKILLS_DIR` directory.

## Step 4: Read the installed skill metadata

Read the installed `SKILL.md` file(s) in the target directory to get:
- `name` — The skill's unique identifier
- `description` — What the skill does
- `allowed-tools` (if present) — Tools the skill needs access to

If multiple skills were installed (no `--skill` filter), read each one.

## Step 5: Attach to subagent (if --attach specified)

**Only for project-scoped installs with `--attach <role>`**:

1. Read the subagent file at `.opencode/agents/<project>_<role>.md`
2. In the frontmatter, add the skill name to the `# skills:` field (comma-separated if skills already exist):
   ```yaml
   # skills: git-commit, <new-skill-name>
   ```
3. In the `## Skills` prompt section, add an entry for the new skill:
   ```markdown
   - **<skill-name>**: <skill-description> — Invoke when <when-to-use>
   ```
4. If the `## Skills` section doesn't exist, create it after `## Your Responsibilities`.

If the subagent file doesn't exist, report: "Subagent `@<project>_<role>` doesn't exist yet. Create it first with `/add-subagent <project> <role>`, then attach skills."

## Step 6: Update project AGENTS.md

**For project-scoped installs**:

Add/update the `## Installed Skills` section in `<project>/AGENTS.md`:

```markdown
## Installed Skills

### Global (available to all projects)
- git-commit — Conventional commit workflow

### Project-specific (<project>)
- <skill-name> — <skill-description>
```

If the section already exists, append the new skill to the appropriate subsection.

## Step 7: Commit the changes

Delegate to the **@git-committer** subagent with these instructions:
- **For project-scoped**: Commit `<project>/.agents/skills/`, `<project>/AGENTS.md`, and `.opencode/agents/<project>_<role>.md` (if modified) to the main workspace repository
- **For global**: Commit `.agents/skills/` and any modified subagent files to the main workspace repository
- Use commit message: `chore: add <skill-name> skill (project: <project> or global)`

## Step 8: Report to user

Report the installation result:

```
✓ Installed skill: <skill-name>
  Source: <source>
  Scope: <project-scoped in <project> / global>
  Location: <SKILLS_DIR>/<skill-name>/SKILL.md

<If --attach>:
  Attached to: @<project>_<role>
  Skills field: # skills: <existing-skills>, <skill-name>

Recommended next steps:
- Review the skill's SKILL.md for its capabilities
- The subagent will automatically load the skill when invoked
- Use `/add-skill <project> <source> --skill <name> --attach <role>` to add more skills
```

## Examples

```bash
# Install TDD skill for my-project's coder subagent
/add-skill my-project mattpocock/skills --skill tdd --attach coder

# Install systematic-debugging globally
/add-skill --global obra/superpowers --skill systematic-debugging

# Install all skills from a source for a project
/add-skill my-project vercel-labs/agent-skills

# Install frontend-design skill for a React project's coder
/add-skill react-project anthropics/skills --skill frontend-design --attach coder
```