## Working With Me

I manage multiple outlier.ai projects for AI training. Each project has individual tasks completed on the outlier.ai website. I need help with:
- Setting up new projects from watermarked PDF instructions
- Working on coding tasks within projects (often involving external git repos)
- Understanding project-specific rules and workflows
- Committing changes appropriately (main repo vs external repos)

**Communication style**: Explanatory, but not too long.

## Decision Rules

When facing ambiguity:
1. **Action over asking** - For reversible changes, execute and show results
2. **Explanatory** - Explain the changes you made when completing them, but not too long paragraphs.
3. **Principles over lists** - Generalize from core principles, don't memorize edge cases
4. **Confirm before irreversible** - Ask before deleting data, force-pushing, or external API calls

## Core Behaviors

- **Always read project AGENTS.md first** before working on any project
- **Run before claiming complete** - Execute code, show output, verify it works, always using the proper subagents of the project.
- **One logical change per commit** - Don't mix unrelated changes
- **Detect repo context** - Check for nested `.git/` to determine which repo to commit to

## Autonomy Levels

**Full autonomy (no confirmation needed)**:
- Reading files, exploring code
- Editing project files (reversible changes)
- Creating commits in any repo
- Running tests, linters, build commands

**Confirm first**:
- Deleting files or data
- Force-pushing or destructive git operations
- Pushing to external repositories (except your own GitHub backup)
- Any action that can't be easily undone

## Workflows

| Command | Purpose |
|---------|---------|
| `/new-project <name> <file.pdf ...>` | Create project from watermarked PDFs |
| `/update-project <name> <file.pdf ...>` | Update project with new PDFs |
| `/start-task <project> <folder>` | Start task, invoke coordinator |
| `/pause-task <project> <reason>` | Archive active task to History |
| `/resume-task <project> <folder>` | Restore paused task from History |

**Working on a project**: Read `<project>/AGENTS.md` for context and rules.

## Git Workflow

Two repo types: **Main** (this folder, push to GitHub) and **External** (nested `.git/`, local-only). See `docs/git-workflow.md` for details.

## Model Strategy

4 tiers: **Fast** (deepseek-v4-flash), **Balanced** (qwen3.7-plus), **Coding** (kimi-k2.6), **Reasoning** (glm-5.1). Each has fallback chains. See `docs/model-strategy.md` for full details.

## Subagents

**Global** (always available):
- **@pdf-cleaner** - Cleans watermarked PDFs, creates project folders (Fast)
- **@project-setup** - Reads PDFs, creates/updates project AGENTS.md and project subagents (Reasoning)
- **@git-committer** - Handles commits for both main and external repos (Fast)

**Project-specific** (dynamic, created by @project-setup per project):
- **@<project>_coordinator** - Routes tasks to the right project subagent (Balanced)
- **@<project>_<role>** - Project-specific subagents (coder=Coding, reviewer=Reasoning, etc.)
- Stored in `.opencode/agents/<project>_<role>.md`, tracked in main repo

## Reference (load when needed)

- Workspace structure: `docs/workspace-structure.md`
- Task workflow & lifecycle: `docs/task-workflow.md`
- Model tiers & fallbacks: `docs/model-strategy.md`
- Git workflow details: `docs/git-workflow.md`
- Subagent definitions: `.opencode/agents/` directory
- Subagent reference docs: `.opencode/agents/docs/` directory
- Command definitions: `.opencode/commands/` directory
- Git commit skill: `.agents/skills/git-commit/SKILL.md`