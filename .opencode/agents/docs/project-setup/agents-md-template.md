# AGENTS.md Template

Use this template when creating project AGENTS.md files (~60 lines max):

```markdown
## Project Context
[2-3 sentences: what this project is, its purpose, tech stack]

## Decision Rules
[3-4 principles for handling ambiguity in THIS project]
1. **Principle over procedure** - [project-specific principle]
2. **Show don't tell** - [concrete behavioral definition]
3. **Confirm before [X]** - [specific to this project]

## Core Behaviors
[Non-negotiables for this project]
- **Always [X]** before [Y]
- **Never [X]** without [Y]
- **Exhaust [X]** before asking

## Autonomy Levels

**Full autonomy (no confirmation needed)**:
- [Specific actions safe for this project]

**Confirm first**:
- [Actions requiring approval in this project]

## Workspace Structure
```
<project-name>/
├── AGENTS.md          ← This file (project rules)
├── PROGRESS.md        ← Task progress tracker (active task + subtask status)
├── .gitignore         ← Ignores task folders, tracks .md, docs/, *.pdf
├── docs/
│   ├── subtasks.md    ← Subtask template (ordered steps every task follows)
│   ├── workflow.md
│   ├── tech-stack.md
│   ├── standards.md
│   └── [other-docs].md
├── <task-folder>/     ← One per task (user-created, gitignored)
│   └── [external-repo]/  ← Cloned repo for this task (gitignored)
└── *.pdf              ← Clean instruction PDFs
```

## Workflows
[1-2 key workflows, concise]
- **Task type A**: [brief description]
- **Task type B**: [brief description]

## Progress Tracking

Each project has a `PROGRESS.md` file that tracks task progress. The format is:
```markdown
# Progress Tracker — <project-name>

---
Active Task: <task-folder-name>
Task Folder: <project-name>/<task-folder-name>/
---

## <task-folder-name>
- [x] 1. <subtask from template>
  - <context notes from subagent>
- [ ] 2. <subtask from template>
- [ ] 3. <subtask from template>
```

- The **Active Task** header tells all subagents which task and folder to work on
- Subtasks come from `docs/subtasks.md` template
- Subagents update their subtask status and add context notes
- Past tasks stay in the file for reference

## User vs AI Responsibilities

**User tasks** (on outlier.ai):
- [Task 1] → AI can assist by [X]
- [Task 2] → AI can assist by [Y]

**AI tasks** (handled directly):
- [Task 1] → See `docs/workflow.md` for details
- [Task 2] → See `docs/tech-stack.md` for setup

## Project Subagents

- **@<project>_coordinator** - Routes tasks to subagents, manages PROGRESS.md (model: balanced)
- **@<project>_<role1>** - [purpose] (model: [fast/balanced/reasoning])
- **@<project>_<role2>** - [purpose] (model: [fast/balanced/reasoning])

## Reference (load when needed)
- Detailed workflow: `docs/workflow.md`
- Tech stack setup: `docs/tech-stack.md`
- Coding standards: `docs/standards.md`
- Subtask template: `docs/subtasks.md`
- [Other project-specific docs]
```

## Key Principles

- **Target ~60 lines** for the main AGENTS.md
- **Never invent information** not present in the PDFs
- **Preserve project terminology** from the PDFs
- **Include specific commands/paths** in reference docs, not main file
- **When ambiguous**, default to documenting how the AI can assist the user
- **Create reference docs** for any topic that needs more than 3-4 lines

## Per-Project .gitignore

**Note**: The per-project `.gitignore` is created by @pdf-cleaner during project setup (Step 1), before any commits. Do NOT recreate it in @project-setup.

Each project folder has a `.gitignore` with this content:

```gitignore
# Ignore everything by default
*

# But track these specific files/folders
!.gitignore
!AGENTS.md
!PROGRESS.md
!docs/
!docs/**
!*.pdf
```

This ensures task folders (with their external repos) are automatically ignored regardless of naming, while tracked files stay in git.