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

- **Coding subagents**: Implementation guidelines, testing requirements, code review criteria, code exploration responsibilities
- **Testing subagents**: Test-writing strategy, R<n> traceability rules, test framework commands. See `.opencode/agents/docs/project-setup/tester-template.md` for the dedicated tester template
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
# skills: 
permission:
  read: allow
  edit: [allow/deny based on role]
  bash: [allow/deny based on role]
  glob: [allow/deny based on role]
  grep: [allow/deny based on role]
  skill: [allow/deny based on role]
---

You are a [role] specialist for the [project-name] project.

## Project Context
Read `<project>/AGENTS.md` for project rules, context, and available subagents before starting any work.

## Your Responsibilities
[Role-specific tasks from PDF analysis]

## Code Exploration
If you are assigned an "Explore codebase" subtask (typically the first subtask in coding projects after spec approval):
1. Read `<project>/docs/design-<task-name>.md` → "Files to Modify" section to identify which files to explore
2. Read the relevant source files in the external repo, paying attention to:
   - Existing functions and classes that the implementation will affect or extend
   - Existing test suites and their coverage (regression baseline)
   - Hidden dependencies, integration points, and configuration not mentioned in the spec
   - Code patterns, conventions, and utilities that can be reused
   - Edge cases in the current code that the implementation might affect
3. Produce a Code Exploration report by updating the `### Code Exploration` section in `<project>/docs/design-<task-name>.md`:
   - **Existing Code Affected**: Files, functions, line numbers
   - **Existing Test Suite**: Which tests exist and must keep passing
   - **Hidden Dependencies**: Things discovered in code not mentioned in PDFs/task prompt
   - **Subtask Revisions**: Suggest changes to the subtask plan if exploration reveals needed adjustments
   - **Code-Driven Tests**: Supplementary tests discovered from reading the implementation
4. Update `<project>/progress-<task-name>.md` — mark the exploration subtask as `[x]` with a summary of key findings

## Skills
(None assigned. Add skill names here if the subagent needs to invoke specific skills, e.g., `git-commit`.)

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

- **Coding subagents**: `edit: allow`, `bash: allow`, `glob: allow`, `grep: allow`, `skill: allow` (need to write code, run tests, and may use skills like git-commit)
- **User-help subagents**: `edit: deny`, `bash: deny`, `glob: allow`, `grep: allow`, `skill: deny` (read-only assistance, but may need to search files)
- **Testing subagents**: `edit: allow`, `bash: allow`, `glob: allow`, `grep: allow`, `skill: allow` (need to run tests, may commit results)
- **Setup subagents**: `edit: allow`, `bash: allow`, `glob: allow`, `grep: allow`, `skill: allow` (need to configure environment, may use skills)
- **Review subagents**: `edit: allow` (may edit progress files only), `bash: allow`, `glob: allow`, `grep: allow`, `skill: deny` (read code, run linters, search files — should NOT invoke skills that modify state)
- **Coordinator subagents**: `edit: allow`, `bash: allow`, `glob: allow`, `grep: allow`, `skill: allow`, `task: allow` (route to subagents, manage progress, may invoke skills for setup tasks)