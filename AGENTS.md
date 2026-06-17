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
| `/add-subagent <project> <role>` | Add a new subagent to an existing project |
| `/add-skill <project> <source> [--skill <name>] [--attach <role>]` | Install a skill from skills.sh and optionally attach to a subagent |
| `/add-skill --global <source> [--skill <name>]` | Install a skill globally (available to all projects) |
| `/start-task <project> <folder>` | Start task, spec review gate, invoke coordinator |
| `/pause-task <project> <reason>` | Change progress file status to paused, reset pointer |
| `/resume-task <project> <folder>` | Restore pointer, change status back to In Progress |
| `/feedback <project> <task-folder> <feedback-file>` | Apply QC feedback, create feedback round progress + design files |

**Working on a project**: Read `<project>/AGENTS.md` for context and rules. To drive a task, switch (Tab) to the project's `@<project>_coordinator` **primary** agent, then run `/start-task` — orchestration runs on the cheaper Balanced coordinator instead of the primary `build`.

## Git Workflow

Two repo types: **Main** (this folder, push to GitHub) and **External** (nested `.git/`, local-only). See `docs/git-workflow.md` for details.

## Model Strategy

4 tiers: **Fast** (`opencode-go/deepseek-v4-flash`), **Balanced** (`opencode-go/qwen3.7-plus`), **Coding** (`opencode-go/kimi-k2.6`), **Reasoning** (`opencode-go/glm-5.1`). Each has fallback chains. See `docs/model-strategy.md` for full details.

## Spec-Driven Development

Before any code is written, requirements and design must be approved by the human. Every task follows: `/start-task` → **spec review gate** → code → review → user confirms. See `docs/task-workflow.md` for the full lifecycle.

## Subagents

**Global** (always available):
- **@pdf-cleaner** - Cleans watermarked PDFs, creates project folders (Fast)
- **@project-setup** - Reads PDFs, creates/updates project AGENTS.md and project subagents (Reasoning)
- **@git-committer** - Handles commits for both main and external repos; invokes the `git-commit` skill for staging and message generation (Balanced)

**Project-specific** (dynamic, created by @project-setup per project):
- **@<project>_coordinator** - **Primary orchestrator** (`mode: primary`, Balanced). You switch to it (Tab) to drive a task; it holds the human approval gates and delegates subtasks to worker subagents at **depth 1**. Reads project AGENTS.md for routing.
- **@<project>_<role>** - Project-specific **worker** subagents (coder=Coding, tester=Coding, reviewer=Reasoning, etc.) — `mode: subagent`, `task: deny`
- **No subagent invokes another subagent** — only the coordinator (a primary agent) delegates; workers do their subtask and return. This is why the coordinator is primary, not a subagent.
- Subagents read `<project>/AGENTS.md` dynamically for project context — no hardcoded project info in prompts
- Stored in `.opencode/agents/<project>_<role>.md`, tracked in main repo
- Add new subagents with `/add-subagent <project> <role>` without re-running full project setup

**Skills**: Subagents can invoke OpenCode skills (e.g., `git-commit`). Skills come from two sources: (1) Custom skills in `.agents/skills/` (built-in), and (2) the [skills.sh](https://www.skills.sh/) ecosystem (installed via `/add-skill`). Skills are declared in the `# skills:` frontmatter field and the `## Skills` prompt section. The coordinator decides per-task whether a skill is needed. See `docs/skills-recommendations.md` for recommended skills by tech stack.

## Reference (load when needed)

- Workspace structure: `docs/workspace-structure.md`
- Task workflow & lifecycle: `docs/task-workflow.md`
- Model tiers & fallbacks: `docs/model-strategy.md`
- Git workflow details: `docs/git-workflow.md`
- Subagent definitions: `.opencode/agents/` directory
- Subagent reference docs: `.opencode/agents/docs/` directory
- Command definitions: `.opencode/commands/` directory
- Git commit skill: `.agents/skills/git-commit/SKILL.md`
- Skill discovery guide: `docs/skills-recommendations.md`