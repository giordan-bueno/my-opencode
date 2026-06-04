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

## Workspace Structure

```
my-opencode/                         ← Main repo (your GitHub backup)
├── .agents/skills/                  ← Installed skills (git-commit, etc.)
├── .opencode/
│   ├── agents/                       ← All subagent definitions (global + project)
│   │   ├── pdf-cleaner.md            ← Global: PDF cleaning subagent
│   │   ├── project-setup.md          ← Global: project setup subagent
│   │   ├── git-committer.md          ← Global: commit handling subagent
│   │   ├── docs/                     ← Reference docs for subagent prompts
│   │   │   └── project-setup/       ← Ref docs loaded on demand by @project-setup
│   │   └── <project>_<role>.md       ← Dynamic: created per-project by @project-setup
│   ├── commands/                     ← Custom commands (new-project, update-project)
│   ├── tools/                        ← Custom tools (delete-watermarks)
│   └── package.json                  ← Plugin dependencies (OpenCode reads this)
├── <project-name>/                   ← One folder per outlier.ai project
│   ├── AGENTS.md                     ← Project-specific rules + subagent routing
│   ├── *.pdf                         ← Clean instruction PDFs
│   ├── docs/                         ← Detailed reference docs (loaded on demand)
│   └── [external-repo]/             ← Optional: cloned repos (local-only, in .gitignore)
├── docs/                             ← Workspace-level reference docs
│   └── workflow.md                   ← Git workflow reference
└── AGENTS.md                         ← This file
```

## Workflows

**New project**: `/new-project <name> <file1.pdf> [file2.pdf ...]`

**Update project**: `/update-project <name> <file1.pdf> [file2.pdf ...]`

**Working on a project**: Read `<project-name>/AGENTS.md` for context and rules.

## Git Workflow

**Two repository types**:
- **Main repo** (this folder): Project setup files → push to your GitHub
- **External repos** (inside projects with `.git/`): Code changes → local-only, never pushed

**Auto-detect**: Nested `.git/` folder = external repo. No `.git/` = main repo.

**Project subagents**: When `@project-setup` creates new subagents, the `.md` files go into `.opencode/agents/` (tracked in main repo, committed alongside project setup changes).

## Subagents

**Global** (always available):
- **@pdf-cleaner** - Cleans watermarked PDFs, creates project folders
- **@project-setup** - Reads PDFs, creates/updates project AGENTS.md and project subagents
- **@git-committer** - Handles commits for both main and external repos

**Project-specific** (dynamic, created by @project-setup per project):
- **@<project>_coordinator** - Routes tasks to the right project subagent
- **@<project>_<role>** - Project-specific subagents (coder, tester, etc.)
- Stored in `.opencode/agents/<project>_<role>.md`, tracked in main repo

## Reference (load when needed)

- Tool details: `.opencode/tools/` directory
- Subagent definitions: `.opencode/agents/` directory
- Subagent reference docs: `.opencode/agents/docs/` directory
- Command definitions: `.opencode/commands/` directory
- Git commit skill: `.agents/skills/git-commit/SKILL.md` (generic commit skill; the @git-committer subagent wraps this with workspace-specific logic)
