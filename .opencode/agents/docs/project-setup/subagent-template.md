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
2. **If a task prompt exists**: Read `<task-folder>/task-prompt.md` for task-specific context and requirements. This is the outlier.ai task prompt containing instructions unique to this task.
3. **After completing work**: Update `<project>/progress-<task-name>.md` (the per-task progress file) — mark your subtask as `[x]` and add context notes (key files, findings, errors) under the subtask
4. **If blocked**: Mark your subtask as `[!]` in `<project>/progress-<task-name>.md` and add a `BLOCKED:` note explaining what's preventing progress. The coordinator will report this to the user for guidance.

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
- [!] 4. Run integration tests
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
model: opencode-go/<primary>
# tier: [fast/balanced/coding/reasoning]
# fallback: opencode-go/<fallback1> [, opencode/<fallback2>]
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
1. **Before starting**: Read `<project>/PROGRESS.md` to find the Active Task and Task Folder, then read `<project>/progress-<task-name>.md` for subtask details
2. **After completing**: Update `<project>/progress-<task-name>.md` — mark your subtask as `[x]` and add context notes

## SDD Awareness
- Read `<project>/docs/requirements.md` to understand project-level requirements with `R<n>` IDs
- Read `<task-folder>/task-prompt.md` (if it exists) for task-specific context and requirements — extract any new requirements as task-specific R<n> IDs (continuing numbering from project requirements)
- Read `<project>/docs/design-<task-name>.md` for the technical approach (created per-task, named after the active task e.g., `design-fix-auth-bug.md`) — includes Task Context and Task-Specific Requirements sections if a task prompt was provided
- When updating PROGRESS.md, note which `R<n>` IDs were addressed in your subtask
- If you cannot cover an `R<n>` assigned to your subtask, mark it as `[!]` blocked with a `BLOCKED:` note explaining why

## Reference (load when needed)
- Detailed instructions: `<project>/docs/[relevant-doc].md`
- Requirements & traceability: `<project>/docs/requirements.md`
- Technical design: `<project>/docs/design-<task-name>.md`
- Task prompt (per-task): `<task-folder>/task-prompt.md`
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
- **Review subagents**: `edit: allow` (may edit progress files only), `bash: allow` (read code, run linters)