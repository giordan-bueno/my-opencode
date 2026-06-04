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
├── docs/              ← Detailed reference docs
│   ├── workflow.md
│   ├── tech-stack.md
│   ├── standards.md
│   └── [other-docs].md
├── *.pdf              ← Clean instruction PDFs
└── [project-files]/
```

## Workflows
[1-2 key workflows, concise]
- **Task type A**: [brief description]
- **Task type B**: [brief description]

## User vs AI Responsibilities

**User tasks** (on outlier.ai):
- [Task 1] → AI can assist by [X]
- [Task 2] → AI can assist by [Y]

**AI tasks** (handled directly):
- [Task 1] → See `docs/workflow.md` for details
- [Task 2] → See `docs/tech-stack.md` for setup

## Project Subagents

- **@<project>_<role1>** - [purpose] (model: [fast/balanced/reasoning])
- **@<project>_<role2>** - [purpose] (model: [fast/balanced/reasoning])

## Reference (load when needed)
- Detailed workflow: `docs/workflow.md`
- Tech stack setup: `docs/tech-stack.md`
- Coding standards: `docs/standards.md`
- [Other project-specific docs]
```

## Key Principles

- **Target ~60 lines** for the main AGENTS.md
- **Never invent information** not present in the PDFs
- **Preserve project terminology** from the PDFs
- **Include specific commands/paths** in reference docs, not main file
- **When ambiguous**, default to documenting how the AI can assist the user
- **Create reference docs** for any topic that needs more than 3-4 lines
