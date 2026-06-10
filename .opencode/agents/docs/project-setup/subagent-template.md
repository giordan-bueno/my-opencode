# Subagent Prompt Template

Each subagent prompt should include common elements plus role-specific elements.

## Common Elements

Every subagent prompt should include:
- Project context (from AGENTS.md Project Context section)
- Reference to `<project>/docs/` for detailed instructions
- Reference to `<project>/PROGRESS.md` for task tracking
- Autonomy levels appropriate to the role

## Progress Tracking

Every subagent MUST:
1. **Before starting work**: Read `<project>/PROGRESS.md` to find the `Active Task` and `Task Folder` — this tells you which task to work on and where files live
2. **After completing work**: Update `<project>/PROGRESS.md` — mark your subtask as `[x]` and add context notes (key files, findings, errors) under the subtask
3. **If blocked**: Mark your subtask as `[!]` in `<project>/PROGRESS.md` and add a `BLOCKED:` note explaining what's preventing progress. The coordinator will report this to the user for guidance.

### Subtask Status Markers

| Marker | Meaning | When to use |
|--------|---------|-------------|
| `[ ]` | Pending | Subtask not yet started |
| `[x]` | Completed | Subtask finished successfully |
| `[!]` | Blocked | Cannot proceed, need user intervention |

Example PROGRESS.md entries:

Completed subtask:
```markdown
- [x] 3. Implement the fix
  - Fixed auth validator in src/auth/validator.ts:42
  - Added null check for empty email field
  - All existing tests still pass
```

Blocked subtask:
```markdown
- [!]] 4. Run integration tests
  - BLOCKED: Integration test suite requires a database connection that's not configured.
  - Need: Database URL and credentials from user to proceed.
```

## Role-Specific Elements

- **Coding subagents**: Implementation guidelines, testing requirements, code review criteria
- **User-help subagents**: Step-by-step procedures, explanation templates, website navigation guidance
- **Testing subagents**: Test execution commands, validation criteria, error analysis
- **Setup subagents**: Configuration steps, dependency management, environment setup
- **Reviewer subagents**: See `.opencode/agents/docs/project-setup/reviewer-template.md` for the dedicated reviewer template

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

## Progress Tracking
1. **Before starting**: Read `<project>/PROGRESS.md` to find the Active Task and Task Folder
2. **After completing**: Update `<project>/PROGRESS.md` — mark your subtask as `[x]` and add context notes

## Reference (load when needed)
- Detailed instructions: `<project>/docs/[relevant-doc].md`
- Project rules: `<project>/AGENTS.md`
- Subtask template: `<project>/docs/subtasks.md`

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