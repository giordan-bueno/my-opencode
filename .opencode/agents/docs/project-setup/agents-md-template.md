# AGENTS.md Template

Use this template when creating project AGENTS.md files (~60 lines max):

````markdown
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
├── progress-<task>-fb1.md ← Feedback round progress (e.g., progress-fix-auth-bug-fb1.md)
├── .gitignore         ← Ignores task folders, tracks .md, docs/, *.pdf, progress-*.md
├── docs/
│   ├── requirements.md  ← EARS requirements with R<n> IDs (from PDFs)
│   ├── design-<task>.md  ← Per-task technical design (created at task start, one per task)
│   ├── design-<task>-fb1.md ← Feedback round designs (e.g., design-fix-auth-bug-fb1.md)
│   ├── subtasks.md    ← Subtask template with R<n> traceability
│   ├── verification.md ← What "done" looks like (objective criteria for the reviewer)
│   ├── testing.md     ← Testing strategy, approach, and project-specific rules
│   ├── workflow.md
│   ├── tech-stack.md
│   ├── standards.md
│   └── [other-docs].md
├── <task-folder>/     ← One per task (user-created, gitignored)
│   ├── task-prompt.md ← Task-specific prompt from outlier.ai (gitignored, per-task)
│   ├── feedback-1.md  ← QC feedback rounds (gitignored, per-task)
│   └── [external-repo]/  ← Cloned repo for this task (gitignored)
└── *.pdf              ← Clean instruction PDFs
```

## Workflows
[1-2 key workflows, concise]
- **Task type A**: [brief description]
- **Task type B**: [brief description]

**Every task ends with a verification step**: The last subtask in every template is always "Verify" — routed to the reviewer subagent. After review, the coordinator reports to the user for final approval before marking the task complete.

**Every coding task starts with code exploration**: After spec approval, the first subtask for coding projects is "Explore codebase" — routed to the coder. The coder reads relevant source files, identifies hidden dependencies, existing tests, and produces a Code Exploration report in the design file. The coordinator then revises the subtask plan based on findings before routing implementation subtasks.

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

**`progress-<task-name>.md`** — A per-task file with full subtask status, context notes, and structured handoff:
```markdown
# Task: <task-name>

---
Status: In Progress
Created: YYYY-MM-DD
Design: docs/design-<task-name>.md
Task Prompt: <task-folder>/task-prompt.md (or "None")
Spec Status: pending | approved | changes_requested
---

## Context Summary
- Completed: <brief summary of completed subtasks with R<n> IDs, or "None yet">
- Current: <what's being worked on now, or "Starting">
- Next: <what comes next, or "To be determined">
- Key files: <most important files for this task, or "To be discovered">
- Blocker: <any blockers, or "None">

- [x] 1. <subtask from template> — @<project>_<role>
  - Modified: <files changed, with lines if relevant>
  - Covers: R1, R2
  - Key decisions: <important decisions, or omit>
  - For next subagent: <critical info for next subagent, or omit>
- [ ] 2. <subtask from template>
- [!] 3. <blocked subtask>
  - BLOCKED: <description of what's blocking>
- [ ] N. Verify — @<project>_reviewer: Run tests, check standards, confirm all requirements met

## Handoff Notes
- Environment: <env vars, config, setup requirements discovered during work>
- Existing tests: <test suites that must keep passing, regression baseline>
- Reuse: <existing utilities, patterns, or modules that should be reused>
- Warning: <things to avoid, hidden dependencies, non-obvious constraints>
```

- **PROGRESS.md** is the single source of truth for "what task is active right now" — subagents check the `Active Task` field to know which task file to read
- **Context Summary** gives a 5-line executive summary at the top of each progress file — subagents read this first for quick orientation before diving into subtask details
- **Structured Handoff** fields (Modified, Covers, Key decisions, For next subagent) ensure critical information flows between subagents — the **worker subagent** writes these when it finishes its subtask; the coordinator verifies them (single-writer rule)
- **Handoff Notes** accumulate environment-level discoveries across the entire task — any subagent can add entries about env vars, test baselines, reusable patterns, or warnings
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

- **@<project>_coordinator** - **Primary** orchestrator (`mode: primary`, tier: balanced) — switch to it (Tab) to drive a task; holds the spec/completion gates, manages PROGRESS.md, delegates to workers at depth 1
- **@<project>_coder** - Implements code changes (worker subagent, tier: coding)
  - Routes to: implementation subtasks
- **@<project>_tester** - Writes and runs tests tracing R<n> IDs (tier: coding)
  - Routes to: test writing subtasks
- **@<project>_reviewer** - Verifies completed work, checks standards, validates R<n> traceability (tier: reasoning)
  - Routes to: Verify subtask (always last)

*(If coding subagents are not listed, they will be created after tech discovery during the first task. Use `/add-subagent` to add them later.)*

## Tech Discovery Status

When the project PDFs don't specify the tech stack (language, framework, test runner, etc.), this section tracks what is known and what needs discovery:

```markdown
## Tech Discovery Status
- Tech stack: [Known: <details> | Partially known: <what's known> | Discovery required]
- Testing framework: [Known: <details> | Discovery required]
- Last updated: [Date or "Pending first task"]
- Discovery source: [PDFs / First task repo / Task prompt / Feedback]
```

**If tech stack is "Discovery required"**: Coding subagents (coder, tester, reviewer) should be proposed after the first task discovers the tech stack from the repo. The coordinator can still operate — it routes to available subagents and reports missing subagents to the user.

**When tech is discovered during a task**: The coordinator updates `docs/tech-stack.md`, `docs/testing.md`, and `docs/standards.md` with the discovered information, marks the Tech Discovery Status as "Known" in AGENTS.md, and recommends `/add-subagent` to create coding subagents if they don't exist yet.

## Installed Skills

Skills from [skills.sh](https://www.skills.sh/) extend subagent capabilities with procedural knowledge. Installed skills are listed here and attached to subagents via their `# skills:` frontmatter field.

### Global (available to all projects)
- git-commit — Conventional commit workflow

### Project-specific (<project>)
*(No project-specific skills installed yet. Use `/add-skill <project> <source> --skill <name> --attach <role>` to install skills.)*

**Recommended skills for this project's tech stack**: Search [skills.sh](https://www.skills.sh/) by language, framework, or task keywords to discover relevant skills. See `docs/skills-recommendations.md` for search methodology.

## Reference (load when needed)
- Requirements & traceability: `docs/requirements.md`
- Technical design (per-task): `docs/design-<task-name>.md`
- Task prompt (per-task): `<task-folder>/task-prompt.md`
- Detailed workflow: `docs/workflow.md`
- Tech stack setup: `docs/tech-stack.md`
- Testing strategy: `docs/testing.md`
- Coding standards: `docs/standards.md`
- Subtask template: `docs/subtasks.md`
- Verification criteria: `docs/verification.md`
- [Other project-specific docs]
````

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
!.agents/
!.agents/**
```

This ensures task folders (with their external repos) are automatically ignored regardless of naming, while tracked files stay in git.