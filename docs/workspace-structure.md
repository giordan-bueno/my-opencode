# Workspace Structure Reference

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
│   ├── commands/                     ← Custom commands (new-project, update-project, start-task, pause-task, resume-task)
│   ├── tools/                        ← Custom tools (delete-watermarks)
│   └── package.json                  ← Plugin dependencies (OpenCode reads this)
├── <project-name>/                   ← One folder per outlier.ai project
│   ├── AGENTS.md                     ← Project rules + subagent routing
│   ├── PROGRESS.md                   ← Minimal pointer: which task is active
│   ├── progress-<task>.md            ← One per task: full subtask status and context (e.g., progress-fix-auth-bug.md)
│   ├── progress-<task>-fb1.md       ← Feedback round progress (e.g., progress-fix-auth-bug-fb1.md)
│   ├── .gitignore                    ← Created by @pdf-cleaner; ignores task folders, tracks .md, docs/, *.pdf, progress-*.md
│   ├── docs/
│   │   ├── requirements.md               ← EARS requirements with R<n> IDs (from PDFs)
│   │   ├── design-<task>.md              ← Per-task technical design (one per task, e.g., design-fix-auth-bug.md)
│   │   ├── design-<task>-fb1.md          ← Feedback round designs (e.g., design-fix-auth-bug-fb1.md)
│   │   ├── subtasks.md               ← Subtask template for every task in this project
│   │   ├── verification.md          ← Objective criteria for what "done" looks like
│   │   ├── workflow.md               ← Detailed workflows
│   │   ├── tech-stack.md             ← Setup, dependencies, configuration
│   │   └── standards.md              ← Coding standards, conventions
│   ├── <task-folder>/                ← One per task (user-created, gitignored)
│   │   ├── task-prompt.md            ← Task-specific prompt from outlier.ai (per-task, gitignored)
│   │   ├── feedback-1.md            ← QC feedback rounds (per-task, gitignored)
│   │   └── [external-repo]/          ← Cloned repo for this task (gitignored)
│   └── *.pdf                         ← Clean instruction PDFs
├── docs/                             ← Workspace-level reference docs
│   ├── git-workflow.md               ← Git workflow reference
│   ├── model-strategy.md             ← Model tier and fallback reference
│   ├── task-workflow.md              ← Task lifecycle reference
│   └── workspace-structure.md         ← This file
└── AGENTS.md                         ← Workspace routing layer (lean, ~60 lines)
```

## Repository Types

- **Main repo** (the `my-opencode/` root): Tracks project folders, clean PDFs, AGENTS.md files, workspace config. Push to your own GitHub for backup/sync.
- **External repos** (inside project `<task-folder>/` directories): Contain code for outlier.ai tasks. Local-only — never pushed. Auto-detected by nested `.git/` folders.

## Key Files

- **`AGENTS.md`** (root): Workspace routing layer. Read first for any project work.
- **`<project>/AGENTS.md`**: Project-specific rules and subagent routing. Read before working on that project.
- **`<project>/PROGRESS.md`**: Minimal pointer file. Contains only the active task name, folder, and spec status. Subagents read this to find which progress file to open.
- **`<project>/progress-<task>.md`**: Per-task progress files. Each task gets its own file with full subtask status, context notes, and completion state. Created by the coordinator during `/start-task`. Feedback rounds create suffixed files (e.g., `progress-fix-auth-bug-fb1.md`).
- **`<project>/docs/design-<task>-fb<N>.md`**: Feedback round design files. Each QC feedback round gets its own design file with R<n> IDs continuing from where the original task left off.
- **`<project>/<task-folder>/task-prompt.md`**: Task-specific prompt from outlier.ai. Contains instructions unique to this task. Created by the user before running `/start-task`. Read by the coordinator and subagents for task context.
- **`<project>/.gitignore`**: Whitelist pattern (`*` then `!file` negations). Ensures only tracked files are committed, not task folders or external repos.