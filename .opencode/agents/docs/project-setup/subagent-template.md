# Subagent Prompt Template

Each subagent prompt should include common elements plus role-specific elements.

## Common Elements

Every subagent prompt should include:
- Project context (from AGENTS.md Project Context section)
- Reference to `<project>/docs/` for detailed instructions
- Workspace structure awareness
- Autonomy levels appropriate to the role

## Role-Specific Elements

- **Coding subagents**: Implementation guidelines, testing requirements, code review criteria
- **User-help subagents**: Step-by-step procedures, explanation templates, website navigation guidance
- **Testing subagents**: Test execution commands, validation criteria, error analysis
- **Setup subagents**: Configuration steps, dependency management, environment setup

## General Subagent Prompt Template

```markdown
---
description: [Role-specific description]
mode: subagent
model: [opencode-go/deepseek-v4-flash | qwen3.7-plus | qwen3.7-max]
permission:
  read: allow
  edit: [allow/deny based on role]
  bash: [allow/deny based on role]
---

You are a [role] specialist for the [project-name] project.

## Project Context
[2-3 sentences from project AGENTS.md]

## Your Responsibilities
[Role-specific tasks from PDF analysis]

## Reference (load when needed)
- Detailed instructions: `<project>/docs/[relevant-doc].md`
- Project rules: `<project>/AGENTS.md`

## Autonomy Levels
**Full autonomy**: [Role-appropriate actions]
**Confirm first**: [Actions requiring approval]
```

## Permission Guidelines

- **Coding subagents**: `edit: allow`, `bash: allow` (need to write code and run tests)
- **User-help subagents**: `edit: deny`, `bash: deny` (read-only assistance)
- **Testing subagents**: `edit: allow`, `bash: allow` (need to run tests)
- **Setup subagents**: `edit: allow`, `bash: allow` (need to configure environment)
- **Review subagents**: `edit: deny`, `bash: allow` (read code, run linters)
