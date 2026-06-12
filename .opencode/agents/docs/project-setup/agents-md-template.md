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
├── PROGRESS.md        ← Minimal pointer: which task is active
├── progress-<task>.md ← One per task: full subtask status and context (e.g., progress-fix-auth-bug.md)
├── .gitignore         ← Ignores task folders, tracks .md, docs/, *.pdf, progress-*.md
├── docs/
│   ├── requirements.md  ← EARS requirements with R<n> IDs (from PDFs)
│   ├── design-<task>.md  ← Per-task technical design (created at task start, one per task)
│   ├── subtasks.md    ← Subtask template with R<n> traceability
│   ├── verification.md ← What "done" looks like (objective criteria for the reviewer)
│   ├── workflow.md
│   ├── tech-stack.md
│   ├── standards.md
│   └── [other-docs].md
├── <task-folder>/     ← One per task (user-created, gitignored)
│   ├── task-prompt.md ← Task-specific prompt from outlier.ai (gitignored, per-task)
│   └── [external-repo]/  ← Cloned repo for this task (gitignored)
└── *.pdf              ← Clean instruction PDFs
```

## Workflows
[1-2 key workflows, concise]
- **Task type A**: [brief description]
- **Task type B**: [brief description]

**Every task ends with a verification step**: The last subtask in every template is always "Verify" — routed to the reviewer subagent. After review, the coordinator reports to the user for final approval before marking the task complete.

**Every task starts with spec approval**: Before code is written, the coordinator presents `docs/requirements.md` and `docs/design-<task-name>.md` for human review. No coding until specs are approved. See SDD reference for details.

## Progress Tracking

Progress tracking uses two levels of files:

**`PROGRESS.md`** — A minimal pointer that tells subagents which task is active:
```markdown
# Progress Tracker — <project-name>

---
Active Task: <task-folder-name or "none">
Task Folder: <project-name>/<task-folder-name>/ or "none">
Spec Status: <pending | approved | changes_requested | "none">
---
```

**`progress-<task-name>.md`** — A per-task file with full subtask status and context notes:
```markdown
# Task: <task-name>

---
Status: In Progress
Created: YYYY-MM-DD
Design: docs/design-<task-name>.md
Task Prompt: <task-folder>/task-prompt.md (or "None")
---

- [x] 1. <subtask from template>
  - <context notes from subagent>
  - Covers: R1, R2
- [ ] 2. <subtask from template>
- [!] 3. <blocked subtask>
  - BLOCKED: <description of what's blocking>
- [ ] N. Verify — @<project>_reviewer: Run tests, check standards, confirm all requirements met
```

- **PROGRESS.md** is the single source of truth for "what task is active right now" — subagents check the `Active Task` field to know which task file to read
- **progress-<task-name>.md** contains the detailed subtask list, context notes, and status for one specific task
- Each task gets its own progress file — no data movement between sections, no History to manage
- Paused tasks: Status changes to `[PAUSED: reason]`, PROGRESS.md pointer resets to `<none>`
- Resumed tasks: Status changes back to `In Progress`, PROGRESS.md pointer set to the task name
- Completed tasks: Status changes to `[COMPLETED]`, PROGRESS.md pointer resets to `<none>`
- Old progress files stay in the project folder as historical reference

## User vs AI Responsibilities

**User tasks** (on outlier.ai):
- [Task 1] → AI can assist by [X]
- [Task 2] → AI can assist by [Y]

**AI tasks** (handled directly):
- [Task 1] → See `docs/workflow.md` for details
- [Task 2] → See `docs/tech-stack.md` for setup

## Project Subagents

- **@<project>_coordinator** - Routes tasks to subagents, manages PROGRESS.md, handles completion gate (tier: balanced)
- **@<project>_<role1>** - [purpose] (tier: [fast/balanced/coding/reasoning])
- **@<project>_reviewer** - Verifies completed work, checks standards, runs tests (tier: reasoning)

## Reference (load when needed)
- Requirements & traceability: `docs/requirements.md`
- Technical design (per-task): `docs/design-<task-name>.md`
- Task prompt (per-task): `<task-folder>/task-prompt.md`
- Detailed workflow: `docs/workflow.md`
- Tech stack setup: `docs/tech-stack.md`
- Coding standards: `docs/standards.md`
- Subtask template: `docs/subtasks.md`
- Verification criteria: `docs/verification.md`
- [Other project-specific docs]
```

## Key Principles

- **Target ~60 lines** for the main AGENTS.md
- **Never invent information** not present in the PDFs
- **Preserve project terminology** from the PDFs
- **Include specific commands/paths** in reference docs, not main file
- **When ambiguous**, default to documenting how the AI can assist the user
- **Create reference docs** for any topic that needs more than 3-4 lines
- **Every requirement gets a stable R<n> ID** that traces through design, subtasks, code, and review — see `.opencode/agents/docs/project-setup/sdd-reference.md`

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
!progress-*.md
!docs/
!docs/**
!*.pdf
```

This ensures task folders (with their external repos) are automatically ignored regardless of naming, while tracked files stay in git.