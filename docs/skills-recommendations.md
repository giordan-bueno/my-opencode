# Skill Discovery Guide

This document describes how to discover, evaluate, and install skills from the [skills.sh](https://www.skills.sh/) ecosystem. **No specific skill names are listed here** — skills must be discovered dynamically by searching the ecosystem, since new skills are published constantly and availability changes over time.

## How to Discover Skills

> **Agents use the CLI; humans use the website.** The `https://www.skills.sh/?q=` search page (Method 1) renders results in-browser via JavaScript, so an *agent* fetching that URL gets nothing back. When the agent discovers skills it must use `npx skills find <keyword>` (Method 2) — the official CLI over the **same** skills.sh catalog (it prints each skill's `skills.sh` link). The `?q=` URLs are for **you** to open in a real browser.

### Method 1: Search skills.sh by keyword

Browse to [https://www.skills.sh/?q=<keyword>](https://www.skills.sh/) replacing `<keyword>` with the relevant search term. Examples:

- By language: `https://www.skills.sh/?q=python`, `https://www.skills.sh/?q=go`, `https://www.skills.sh/?q=rust`, `https://www.skills.sh/?q=java`, `https://www.skills.sh/?q=typescript`
- By framework: `https://www.skills.sh/?q=react`, `https://www.skills.sh/?q=nextjs`, `https://www.skills.sh/?q=django`, `https://www.skills.sh/?q=fastapi`, `https://www.skills.sh/?q=spring`
- By task type: `https://www.skills.sh/?q=tdd`, `https://www.skills.sh/?q=debugging`, `https://www.skills.sh/?q=testing`, `https://www.skills.sh/?q=code-review`, `https://www.skills.sh/?q=verification`

### Method 2: CLI search

```bash
npx skills find <keyword>
```

Examples:
```bash
npx skills find python
npx skills find react
npx skills find tdd
npx skills find debugging
```

### Method 3: Browse skills.sh

Browse the full directory at [https://www.skills.sh/](https://www.skills.sh/) and filter by topic:
- [Agent workflows](https://www.skills.sh/topic/agent-workflows)
- [Testing](https://www.skills.sh/topic/testing)
- [Databases](https://www.skills.sh/topic/databases)
- [Design & UI](https://www.skills.sh/topic/design)
- etc.

## When to Search for Skills

Search for skills at these points in the workflow:

1. **During project setup** (`/new-project`) — When the PDFs identify the tech stack, search for language/framework-specific skills before proposing subagents.
2. **During tech discovery** (`/start-task` Step 1c/1d) — When the tech stack is discovered from the repo, search for skills matching the discovered language and framework.
3. **After code exploration** — When the coordinator's code exploration reveals deeper tech details (specific libraries, test frameworks), search for relevant skills.
4. **When adding a subagent** (`/add-subagent`) — After creating a subagent, search for skills that match its role and the project's tech stack.
5. **Any time the user asks** — The `/add-skill` command supports searching skills.sh.

## Search Keywords by Role

When searching for skills for a specific subagent role, use these keyword categories:

| Role | Search keywords |
|------|----------------|
| Coder | `<language>`, `<framework>`, `tdd`, `debugging`, `best-practices` |
| Tester | `<language>`, `<test-framework>`, `tdd`, `testing`, `verification` |
| Reviewer | `code-review`, `verification`, `best-practices`, `<language>` |
| Coordinator | `planning`, `workflow`, `subagent`, `task-management` |

Combine role keywords with the project's specific language and framework keywords. For example, for a Python/FastAPI project:
- Coder: search `python`, `fastapi`, `tdd`, `debugging`
- Tester: search `python`, `pytest`, `testing`, `tdd`
- Reviewer: search `code-review`, `verification`, `python`

## Evaluating Skills

When you find skills from search results, evaluate them by:

1. **Install count** — Prefer skills with 1K+ installs (shown on skills.sh)
2. **Security audits** — Check the "Security Audits" section on the skill's skills.sh page. Prefer skills with audits from trusted sources (e.g., "Pass" ratings from Socket, Snyk).
3. **Source reputation** — Prefer skills from well-known sources (e.g., Anthropic, Vercel, Microsoft) or highly-starred GitHub repos.
4. **Recency** — Check when the skill was first seen and last updated. Prefer recently maintained skills.
5. **Skill description** — Read the SKILL.md content on the skills.sh page to verify the skill does what you need.

## Installing Skills

Once you've found a relevant skill:

```bash
# Project-scoped (recommended for framework-specific skills)
/add-skill <project> <source> --skill <name> --attach <role>

# Example (after searching and finding a skill):
/add-skill my-project <owner/repo> --skill <skill-name> --attach coder

# Global (for skills useful across all projects)
/add-skill --global <owner/repo> --skill <name>
```

The `/add-skill` command:
1. Installs the skill's SKILL.md files to the project's `.agents/skills/` directory (or global `.agents/skills/`)
2. If `--attach <role>` is specified, updates the subagent's `# skills:` frontmatter and `## Skills` section
3. Updates the project's `AGENTS.md` → "Installed Skills" section
4. Commits the changes

## Generating Custom Skills

When no community skill covers the project's specific needs, use the skill-creator to generate a custom skill:

```bash
/add-skill <project> anthropics/skills --skill skill-creator --attach coder
```

The skill-creator guides you through:
1. Defining what the skill should do
2. Writing a draft SKILL.md
3. Creating test prompts and evaluating
4. Iterating based on feedback
5. Saving to `.agents/skills/<custom-skill>/SKILL.md`

Common use cases for custom skills:
- Project-specific test runner workflows (e.g., "run pytest with coverage and report results")
- Framework conventions not covered by community skills
- CI/CD pipeline conventions
- Code style enforcement

## Skill File Structure

Skills are stored as SKILL.md files with YAML frontmatter:

```markdown
---
name: skill-name
description: What this skill does and when to use it
allowed-tools: Bash  # optional: restrict which tools the skill can use
---

# Skill Name

[Instructions for the agent to follow when this skill is activated]
```

Install locations:
- **Project-scoped**: `<project>/.agents/skills/<skill-name>/SKILL.md`
- **Global**: `.agents/skills/<skill-name>/SKILL.md`

## skills-lock.json

The root `skills-lock.json` tracks installed global skills with the source, source type, skill path **relative to the `.agents/` directory**, and a content hash for tamper detection:

```json
{
  "version": 1,
  "skills": {
    "git-commit": {
      "source": "github/awesome-copilot",
      "sourceType": "github",
      "skillPath": "skills/git-commit/SKILL.md",
      "computedHash": "<sha256>"
    }
  }
}
```

The `skillPath` field is intentionally **relative to `.agents/`** (not the workspace root), because the `skills.sh` CLI manages skills within that directory. Do not edit this file by hand — let `/add-skill` and the `npx skills` CLI maintain it.

`skills-lock.json` is tracked by git so installed global skills can be restored when cloning the workspace.

## Updating Skills

There is no `/update-skill` command yet. To update an installed skill:

1. **Check for upstream changes**: Visit the skill's page on [skills.sh](https://www.skills.sh/) or the source repo and look at the last-updated date.
2. **Reinstall**: Run `/add-skill` again with the same source and `--skill` name. The CLI replaces the local copy and updates the `computedHash` in `skills-lock.json`.
   - Project-scoped: `/add-skill <project> <source> --skill <name>` (re-attach is optional; the existing `# skills:` frontmatter entry stays)
   - Global: `/add-skill --global <source> --skill <name>`
3. **Verify the diff**: After reinstall, run `git diff .agents/skills/<name>/` (or `<project>/.agents/skills/<name>/`) to see what changed. Review the new SKILL.md content before continuing — an upstream change can alter the skill's behavior, allowed-tools, or invocation criteria.
4. **Commit the update**: The `/add-skill` flow ends with a commit. If you reinstalled to update, include the rationale in the commit body (e.g., `chore: refresh git-commit skill — upstream security patch`).

If a skill is removed upstream, the local copy still works (it's a self-contained SKILL.md file), but consider whether to keep it.