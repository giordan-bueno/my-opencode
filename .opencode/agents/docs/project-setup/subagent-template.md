# Subagent Prompt Template

Each subagent prompt should include common elements plus role-specific elements.

## Common Elements

Every subagent prompt should include:
- Project context (from AGENTS.md Project Context section)
- Reference to `<project>/docs/` for detailed instructions
- Reference to `<project>/PROGRESS.md` for task tracking
- Autonomy levels appropriate to the role

## Progress Tracking

**You are the single writer for your own subtask's status and handoff.** Mark your subtask, write your structured handoff fields, and update the Context Summary yourself *before returning* to the coordinator. The coordinator **verifies** your entries but does not overwrite them — so if you don't write them, the information is lost and the next subagent flies blind.

Every subagent MUST:
1. **Before starting work**: Read `<project>/PROGRESS.md` to find the `Active Task` and `Task Folder` — this tells you which task to work on and where files live. Then read `<project>/progress-<task-name>.md` — start with the **Context Summary** at the top for a quick orientation, then scroll to your assigned subtask.
2. **If a task prompt exists**: Read `<task-folder>/task-prompt.md` for task-specific context and requirements. This is the outlier.ai task prompt containing instructions unique to this task.
3. **After completing work**: Update `<project>/progress-<task-name>.md` with structured handoff information:
   - Mark your subtask as `[x]` and add the following structured fields:
     - **Modified** (required): Files you changed, with line numbers if relevant
     - **Covers** (required): R<n> IDs addressed by your work
     - **Key decisions** (use when applicable): Important implementation choices that affect future work
     - **For next subagent** (**REQUIRED if any of the conditions below is true; otherwise omit**):
       - The next subagent depends on a non-obvious side effect of your work (e.g., registration order, middleware sequence, file load order)
       - You discovered an environment requirement (env var, config file, port) the next subagent must satisfy
       - You discovered a framework quirk or hidden API contract (e.g., must-call-init-before-use)
       - You made a decision the next subagent could plausibly reverse without knowing why (e.g., chose a specific test framework option, picked one of multiple valid approaches)
       - You left a deliberate `[!]` blocker or known issue
       When in doubt, include it. A missing `For next subagent` after a critical handoff is the most common cause of downstream subagent failures.
   - Update the **Context Summary** at the top of the progress file:
     - `Completed`: Add your subtask summary with R<n> IDs
     - `Current`: Update to reflect the next subtask
     - `Next`: Update to preview the following subtask
     - `Key files`: Add any important files you discovered or modified
     - `Blocker`: Set to `None` if you resolved a blocker, or add one if you discovered one
   - Add entries to **Handoff Notes** if you discovered:
     - Environment requirements (env vars, config, setup)
     - Existing tests that must keep passing (regression baseline)
     - Existing utilities or patterns that should be reused
     - Warnings about hidden dependencies or non-obvious constraints

     **Handoff Notes format rules** (to keep the section structured and bounded):
     - Use the four categorical prefixes only: `Environment:`, `Existing tests:`, `Reuse:`, `Warning:`. One bullet per discovery.
     - **One discovery per bullet.** Do not chain unrelated findings into a single line.
     - Include the **discovery source** in parentheses (file path with line number when possible): e.g., `Environment: Requires JWT_SECRET in .env (src/config.ts:8)`.
     - **Do not duplicate** entries already in the section. If you would add a duplicate, instead append a clarification to the existing entry (e.g., `... — confirmed still required after R5 implementation`).
     - **Append, do not rewrite** — never delete or reorder prior entries. If an entry becomes obsolete (e.g., env var no longer used after a refactor), strike it through with `~~ ~~` markdown and add a sibling bullet explaining the change.
     - Soft cap: aim for **≤ 15 entries per task**. If you cross that, the discoveries are too granular — consolidate or move detail to the relevant doc (`docs/tech-stack.md`, `docs/standards.md`).
4. **If blocked**: Mark your subtask as `[!]` in `<project>/progress-<task-name>.md` and add a `BLOCKED:` note explaining what's preventing progress. Update the Context Summary `Blocker` line. The coordinator will report this to the user for guidance.

### Subtask Status Markers

| Marker | Meaning | When to use |
|--------|---------|-------------|
| `[ ]` | Pending | Subtask not yet started |
| `[x]` | Completed | Subtask finished successfully |
| `[!]` | Blocked | Cannot proceed, need user intervention |

Example PROGRESS.md entries:

Completed subtask with structured handoff:
```markdown
- [x] 3. Implement the fix — @project_coder
  - Modified: src/auth/validator.ts:42, src/errors/handler.ts:15-20
  - Covers: R3, R5
  - Key decisions: Used null-safe operator instead of try/catch
  - For next subagent: Auth middleware registered before session middleware in app.ts:23
```

Blocked subtask:
```markdown
- [!] 4. Run integration tests
  - BLOCKED: Integration test suite requires a database connection that's not configured.
  - Need: Database URL and credentials from user to proceed.
```

## Role-Specific Elements

- **Coding subagents**: See `.opencode/agents/docs/project-setup/coder-template.md` for the dedicated coder template (mandatory structural sections + project-specific customization slot).
- **Testing subagents**: Test-writing strategy, R<n> traceability rules, test framework commands, test execution and reporting. See `.opencode/agents/docs/project-setup/tester-template.md` for the dedicated tester template.
- **User-help subagents**: Step-by-step procedures, explanation templates, website navigation guidance.
- **Setup subagents**: Configuration steps, dependency management, environment setup.
- **Reviewer subagents**: See `.opencode/agents/docs/project-setup/reviewer-template.md` for the dedicated reviewer template.

The generic template below is the fallback for roles that don't have a dedicated template (navigator, setup, custom roles).

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
  task: deny
---

You are a [role] specialist for the [project-name] project. You are a **worker subagent**: do your assigned subtask and return to the primary coordinator. You never invoke another subagent (you have no `task` permission).

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

### Installing Skills

Skills can be added to subagents at any time using the `/add-skill` command. Skills come from two sources:

1. **Custom skills** in `.agents/skills/` (e.g., `git-commit`)
2. **skills.sh ecosystem** — community skills discovered by searching [skills.sh](https://www.skills.sh/)

To discover relevant skills, search skills.sh by keyword:
- By language/framework: `https://www.skills.sh/?q=python`, `?q=react`, `?q=rust`, etc.
- By task type: `https://www.skills.sh/?q=tdd`, `?q=debugging`, `?q=testing`, etc.
- CLI search: `npx skills find <keyword>`

To install a discovered skill:
```bash
/add-skill <project> <source> --skill <name> --attach <role>
```

When a skill is installed and attached to a subagent:
1. The skill's `SKILL.md` is placed in `<project>/.agents/skills/<skill-name>/` (project-scoped) or `.agents/skills/<skill-name>/` (global)
2. The skill name is added to the subagent's `# skills:` frontmatter field
3. A description of when to invoke the skill is added to this `## Skills` section
4. The subagent invokes the skill via OpenCode's skill system when the relevant task arises

## Progress Tracking
1. **Before starting**: Read `<project>/PROGRESS.md` to find the Active Task and Task Folder, then read `<project>/progress-<task-name>.md` — start with the **Context Summary** at the top for a quick orientation, then scroll to your assigned subtask
2. **After completing**: Update `<project>/progress-<task-name>.md` with structured handoff information — mark your subtask `[x]` with Modified, Covers, Key decisions, and For next subagent fields. Update the Context Summary and add entries to Handoff Notes as needed.

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

> **Two rules that apply everywhere:**
> - `read`, `glob`, `grep`, and `list` are read-only and effectively always available. `write` is **not** a separate OpenCode permission key — `edit: allow` already governs creating *and* modifying files.
> - **Only the coordinator (a `mode: primary` agent) gets `task: allow`.** Every *worker* subagent gets `task: deny`, so that **no subagent ever invokes another subagent** (subagent→subagent delegation is unreliable in OpenCode and has no depth guard). Workers complete their subtask and return to the coordinator.

- **Coding subagents** (coder): `edit: allow`, `bash: allow`, `glob: allow`, `grep: allow`, `skill: allow`, `task: deny` (write code, run builds, may use skills like git-commit)
- **Testing subagents** (tester): `edit: allow`, `bash: allow`, `glob: allow`, `grep: allow`, `skill: allow`, `task: deny` (write and run tests, may commit results)
- **Review subagents** (reviewer): `edit: allow` (progress files only), `bash: allow`, `glob: allow`, `grep: allow`, `skill: deny`, `task: deny` (read code, run linters, search — never modify state or delegate)
- **User-help subagents** (navigator): `edit: deny`, `bash: deny`, `glob: allow`, `grep: allow`, `skill: deny`, `task: deny` (read-only assistance)
- **Setup subagents**: `edit: allow`, `bash: allow`, `glob: allow`, `grep: allow`, `skill: allow`, `task: deny` (configure environment, may use skills)
- **Coordinator** (`mode: primary`, NOT a subagent): `edit: allow`, `bash: allow`, `glob: allow`, `grep: allow`, `skill: allow`, `task: allow` — the only agent that delegates; it also holds the human approval gates. See `coordinator-template.md`.