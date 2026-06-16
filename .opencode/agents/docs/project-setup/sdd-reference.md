# Spec-Driven Development (SDD) Reference

This workspace uses an adapted SDD workflow inspired by [harness-sdd](https://github.com/betta-tech/harness-sdd). The core principle: **requirements and design are approved by the human BEFORE any code is written.** Every requirement gets a stable `R<n>` ID that traces through design → code exploration → subtasks → code → tests → review.

## The SDD Flow

```
/new-project → (project-setup produces docs + requirements) → /start-task → (spec review gate) → (code exploration) → (revised subtasks + design) → (code) → (tests) → (review) → (user confirms)
```

The spec review gate approves the **draft** design based on requirements and task prompt. After approval, the coder explores the codebase and the design is revised based on findings (hidden dependencies, existing tests, code patterns). Subtasks and the test plan are then updated to reflect code-driven discoveries before implementation begins.

## Requirements Format (docs/requirements.md)

Requirements are extracted from PDFs during `/new-project`. Each gets a stable `R<n>` ID.

### EARS Syntax

Use **EARS (Easy Approach to Requirements Syntax)** when possible. Fall back to `MUST` statements when EARS patterns don't fit.

| Pattern | Template | When to use |
|---------|----------|-------------|
| **Ubiquitous** | `The system MUST <action>.` | Always applies |
| **Event-driven** | `WHEN <trigger>, the system MUST <action>.` | Triggered by an event |
| **State-driven** | `WHILE <state>, the system MUST <action>.` | During a state |
| **Optional** | `WHERE <feature>, the system MUST <action>.` | Optional feature |
| **Unwanted** | `IF <unwanted event>, THEN the system MUST <action>.` | Error/negative case |

Rules:
- Only `MUST` / `MUST NOT` are permitted modal verbs
- One requirement = one `MUST` assertion
- Every `R<n>` must be verifiable by a concrete test or check

### Example

```markdown
## Requirements — auth-service

### R1: Authentication required
The system MUST require valid credentials before granting access to any protected resource.

### R2: Login redirect
WHEN a user provides valid credentials, the system MUST redirect them to the dashboard.

### R3: Error display
IF an API request fails, THEN the system MUST display a user-friendly error message within 2 seconds.

### R4: Audit logging
WHILE the system is in production mode, the system MUST log all data modification operations with timestamp, user ID, and action.

---

## Traceability Matrix

| Acceptance Criterion (from PDF) | Requirements |
|--------------------------------|-------------|
| Users can't access dashboard without login | R1 |
| Successful login goes to dashboard | R2 |
| Errors don't crash the app | R3 |
| All changes are traceable | R4 |
```

### When PDFs lack system requirements

Not all outlier.ai projects are software development projects. Some PDFs are purely procedural (steps to follow on a website) with no "system MUST" statements. In these cases:

- Derive minimal requirements from the subtask template steps — each step that has a verifiable outcome becomes an `R<n>`
- Focus on **what constitutes "done"** rather than system behavior
- Example: "Clone the repo and navigate to the correct branch" → `R1: The task folder MUST contain the correct repo checked out to the specified branch`
- Keep requirements concise and verifiable — avoid inflating the count
- When EARS doesn't fit naturally, `MUST` statements are acceptable (e.g., `The task MUST pass all project tests`)

### When PDFs lack tech stack information

Some outlier.ai project PDFs don't specify the tech stack (language, framework, test runner, etc.). In these cases:

- `docs/tech-stack.md` is created with a **"## Discovery Required"** section listing what is unknown (language, framework, build tool, package manager, test runner, database, etc.) and how it will be discovered (from the repo during the first task, from task prompts, from feedback)
- `docs/testing.md` uses the placeholder **"Testing framework: Discovery required — will be determined from the repo during the first task"** instead of guessing
- `docs/standards.md` uses minimal generic conventions with a note **"To be updated after tech discovery during the first task"**
- `AGENTS.md` includes a **"## Tech Discovery Status"** section tracking what is known and what needs discovery
- Coding subagents (coder, tester, reviewer) may be **deferred** until the tech stack is discovered — the coordinator is created first, and coding subagents are added later via `/add-subagent`

**When tech discovery happens** (during `/start-task` or code exploration):
1. The repo's dependency files are inspected to identify language, framework, test runner, etc.
2. `docs/tech-stack.md`, `docs/testing.md`, and `docs/standards.md` are updated with discovered information
3. `AGENTS.md` "Tech Discovery Status" is updated to mark fields as "Known"
4. If coding subagents don't exist yet, the user is prompted to run `/add-subagent` for each missing role
5. If coding subagents exist but lack tech-specific context, the user is prompted to run `/add-subagent <project> <role> --update`

This affects the SDD flow:
- **Design and Test Plan**: If tech stack is unknown at spec review time, the design and test plan use placeholder information (e.g., "test framework: TBD"). After tech discovery during the first task, the coordinator revises the design and test plan with the discovered information.
- **Test Plan completion**: The full test plan (with test commands, test file paths, and test types) cannot be finalized until the tech stack is known. A partial test plan is created at spec review and revised after tech discovery.

### Task prompts and task-specific requirements

Many outlier.ai tasks come with a **task prompt** — specific instructions, context, or a prompt to implement/fix that's unique to each task. These are stored in `<task-folder>/task-prompt.md`.

Task prompts add **task-specific requirements** that complement the project-level requirements:

- **Project-level requirements** (in `docs/requirements.md`): Stable R<n> IDs derived from the project PDFs. These apply to ALL tasks in the project. Example: R1-R5.
- **Task-specific requirements** (in `docs/design-<task-name>.md` "Task-Specific Requirements" section): New R<n> IDs derived from the task prompt, continuing numbering from the project requirements. These apply only to THIS task. Example: R6-R8.
- The reviewer verifies BOTH: project R<n> and task-specific R<n> must be covered.

When a task prompt exists:
1. The coordinator reads `task-prompt.md` before creating `docs/design-<task-name>.md`
2. The coordinator extracts new requirements from the task prompt, continuing R<n> numbering from `requirements.md`
3. The coordinator adapts the subtask list based on the task prompt's instructions
4. The reviewer checks implementation against both project and task-specific requirements

### Feedback Rounds and R<n> Numbering

When QC sends feedback on a completed task, a new feedback round is created via `/feedback`. The feedback round:

- Gets its own progress file: `progress-<task>-fb<N>.md` (e.g., `progress-fix-auth-bug-fb1.md`)
- Gets its own design file: `docs/design-<task>-fb<N>.md` (e.g., `docs/design-fix-auth-bug-fb1.md`)
- Works in the **same task folder and repo** — no new clone needed
- **R<n> IDs continue from where the original task left off**. If the original task used R1-R8, feedback requirements start at R9.

Example: Original task has R1-R5 (project) + R6-R8 (task-specific). Feedback adds R9-R11 addressing QC issues.

```markdown
## Design — fix-auth-bug-fb1 (file: docs/design-fix-auth-bug-fb1.md)

### Feedback Context
QC feedback from round 1: auth validator rejects valid emails with plus signs, missing error codes in responses.

### Feedback Requirements
### R9: Handle plus signs in email validation
WHEN a user submits an email containing a plus sign, the system MUST accept it as valid.

### R10: Return error codes in API responses
IF an authentication request fails, THEN the system MUST include an error code in the JSON response.

### R11: Reject empty passwords with specific code
WHEN a user submits an empty password, the system MUST reject it with error code AUTH_EMPTY_PASSWORD.

### Approach
Fix email regex to allow plus signs, add error codes to existing error responses, add specific validation for empty passwords.
...
```

## Design Format (docs/design-<task-name>.md)

**Per-task file** — each task gets its own design file named `docs/design-<task-name>.md` (e.g., `docs/design-fix-auth-bug.md`). Created during the spec review phase of `/start-task`. Always created, even for simple tasks.

**Why per-task**: Previous tasks' designs are preserved, not overwritten. When pausing and resuming, the design file for a task already exists and can be read directly. Completed tasks' designs remain in `docs/` as historical reference.

**No cleanup needed**: Old design files stay in `docs/` permanently. They're small markdown files tracked by git and provide useful context for future tasks in the same project.

```markdown
## Design — <task-name>

### Task Context
<Brief summary of the task prompt from outlier.ai, or "No task-specific prompt — project-level requirements only">

### Task-Specific Requirements
<If a task prompt was provided, extract requirements unique to this task as R<n> IDs continuing from the project requirements. If project has R1-R5, task-specific requirements start at R6.>

### R6: <task-specific requirement from prompt>
<Description of the requirement extracted from the task prompt>

### Approach
<Chosen approach with brief rationale>

### Files to Modify
| File | Change Type | R<n> Covered |
|------|------------|--------------|
| src/auth/middleware.ts | Modify | R1, R2, R6 |
| src/errors/handler.ts | Create | R3 |
| src/middleware/logger.ts | Modify | R4 |

### Alternatives Considered
1. **Session-based auth** — Rejected: PDF instructions require JWT tokens
2. **Global error boundary** — Rejected: Per-route handlers provide better error context

### Risks
- R1 depends on JWT secret configuration — must verify env vars before testing
- R3 error display may need i18n consideration

### Dependencies
- jsonwebtoken@^9.0
- Existing Express middleware in src/middleware/

### Test Plan
For each R<n> covered by this task, define how it will be tested. This is created by the coordinator during the spec review phase and read by the tester subagent.

| R<n> | Test Type | Test File | Description |
|------|-----------|-----------|-------------|
| R1 | Fail-to-pass | tests/auth.test.ts | Verify unauthenticated requests are blocked |
| R2 | Pass-to-pass | tests/auth.test.ts | Verify valid credentials redirect to dashboard |
| R3 | Standard | tests/errors.test.ts | Verify API failures return error messages |
| R4 | Standard | tests/audit.test.ts | Verify audit log records timestamp, user ID, and action |
| R6 | Fail-to-pass | tests/auth.test.ts | Verify empty email returns structured error |

Test types:
- **Fail-to-pass** (TDD RED phase): Test must FAIL before implementation, PASS after. Write before the coder implements.
- **Pass-to-pass**: Test must PASS before and after changes. Used to verify no regressions.
- **Standard**: Test must PASS after implementation. Write after or alongside implementation.
```

### Code Exploration

After spec approval and before implementation, the coder explores the codebase. This section is populated **after** the exploration subtask completes, revising the draft design based on actual code findings.

```markdown
### Code Exploration

#### Existing Code Affected
- `src/auth/middleware.ts:42` — Existing `validateToken()` function that needs modification for R1
- `src/auth/session.ts:15` — Session auth system that must coexist with new JWT auth (not mentioned in spec)
- `src/errors/handler.ts` — Existing error handler that needs a new error type for R3

#### Existing Test Suite
- `tests/auth.test.ts` — 12 existing tests, all must continue passing (regression baseline)
- `tests/errors.test.ts` — 4 existing tests for error handling

#### Hidden Dependencies
- JWT secret must be in `process.env.JWT_SECRET` (not mentioned in PDF, discovered in `src/config.ts:8`)
- Auth middleware must be registered before session middleware in `src/app.ts:23`

#### Subtask Revisions
Based on code exploration, the original subtask plan is revised:
- Original subtask "Implement auth middleware" is split into:
  - "Modify existing auth middleware to add JWT support" (R1, R2)
  - "Add error type for auth validation failures" (R3)
- Original subtask "Add audit logger" should reuse existing `logAction()` utility in `src/utils/logger.ts`

#### Code-Driven Tests (supplementary to Test Plan above)
- REGRESSION: All 12 existing tests in `tests/auth.test.ts` must pass after changes (Pass-to-pass)
- EDGE CASE: `validateToken(null)` should return 401 — discovered from reading `src/auth/middleware.ts:37` (Standard)
- INTEGRATION: JWT auth and session auth must coexist — discovered from `src/app.ts:23` middleware order (Standard)
```
```

## Traceability Rules

The `R<n>` IDs create a chain that the reviewer verifies:

1. **Every project-level `R<n>` must appear in at least one subtask** in the adapted subtask list (from `docs/subtasks.md` template, possibly adapted for the task)
2. **Every task-specific `R<n>` must appear in at least one subtask** in the adapted subtask list
3. **Every subtask must reference at least one `R<n>`** (except the Verify subtask, which implicitly covers all)
4. **Every `R<n>` (project and task-specific) must have at least one verification criterion** in `docs/verification.md`
5. **The reviewer checks the full chain**: R\<n\> → design Test Plan → subtask → implementation → test

If any `R<n>` is untested or uncovered, the reviewer reports `CHANGES_REQUESTED`.

## Subtask Format with Traceability

Enhanced `docs/subtasks.md` format — each subtask references which requirements it covers:

### Standard Coding Project Template

```markdown
## Subtask Template — Coding Projects

1. **Explore codebase and report findings** — @<project>_coder: Read relevant source files, existing test suite, hidden dependencies. Produce Code Exploration section in design file. Revise subtask plan if needed. Covers: all R<n>
2. **Implement auth middleware** — @<project>_coder: Add JWT middleware to protected routes. Covers: R1, R2
3. **Add error handler** — @<project>_coder: Create error boundary for API calls. Covers: R3
4. **Add audit logger** — @<project>_coder: Log all data modifications with required fields. Covers: R4
5. **Write and run tests** — @<project>_tester: Write tests covering R1-R4 per Test Plan + code-driven tests from exploration. Run test suite and report results. Covers: R1, R2, R3, R4
6. **Verify** — @<project>_reviewer: Review test results, check R<n> traceability, verify standards, confirm all requirements met
```

### TDD Project Template (Fail-to-Pass)

For projects that use Test-Driven Development (specified in `docs/testing.md`):

```markdown
## Subtask Template — TDD Projects

1. **Write fail-to-pass tests** — @<project>_tester: Write failing tests for R1-R4 per draft Test Plan (RED phase). Covers: R1, R2, R3, R4
2. **Explore codebase and report findings** — @<project>_coder: Read relevant source files, existing test suite, hidden dependencies. Produce Code Exploration section in design file. Revise subtask plan if needed. Covers: all R<n>
3. **Implement auth middleware** — @<project>_coder: Add JWT middleware to protected routes. Covers: R1, R2
4. **Add error handler** — @<project>_coder: Create error boundary for API calls. Covers: R3
5. **Add audit logger** — @<project>_coder: Log all data modifications with required fields. Covers: R4
6. **Write pass-to-pass + code-driven tests, run full suite** — @<project>_tester: Write pass-to-pass tests, add code-driven tests from exploration, run full suite, all must pass (GREEN phase). Covers: R1, R2, R3, R4
7. **Verify** — @<project>_reviewer: Review test results, check R<n> traceability, verify standards, confirm all requirements met
```

## Verification Format with Traceability

Enhanced `docs/verification.md` — each criterion references R\<n\> IDs:

```markdown
## Verification Criteria

- [ ] R1: Auth middleware blocks unauthenticated access
  - Verification: Automated test
  - Test command: `npm test -- auth.test.ts`
  - Test type: Fail-to-pass
- [ ] R2: Successful login redirects to dashboard
  - Verification: Automated test
  - Test command: `npm test -- auth.test.ts`
  - Test type: Pass-to-pass
- [ ] R3: Error handler catches API failures gracefully
  - Verification: Automated test
  - Test command: `npm test -- errors.test.ts`
  - Test type: Standard
- [ ] R4: Audit logger records timestamp, user ID, and action
  - Verification: Automated test
  - Test command: `npm test -- audit.test.ts`
  - Test type: Standard
- [ ] Code follows conventions defined in docs/standards.md
  - Verification: Manual code review
- [ ] No debug artifacts left (no console.log, print statements)
  - Verification: Manual code review
```

Where test types are:
- **Fail-to-pass**: Test must FAIL before implementation and PASS after (TDD RED/GREEN)
- **Pass-to-pass**: Test must PASS before and after changes (regression check)
- **Standard**: Test must PASS after implementation

## Spec Status in PROGRESS.md

The PROGRESS.md pointer includes a `Spec Status` field:

```
---
Active Task: fix-auth-bug
Task Folder: project-x/fix-auth-bug/
Spec Status: pending | approved | changes_requested
---
```

| Status | Meaning |
|--------|---------|
| `pending` | Spec created (requirements + design), awaiting human approval |
| `approved` | Human approved, coding subagents can begin |
| `changes_requested` | Human requested changes, coordinator waiting for guidance |

### Progress file (per-task)

Each task gets its own progress file with full subtask details, context summary, and structured handoff:

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

- [x] 1. <completed subtask> — @<project>_<role>
  - Modified: <files changed, with lines if relevant>
  - Covers: R1, R2
  - Key decisions: <important decisions, or omit>
  - For next subagent: <critical info for next subagent, or omit>
- [ ] 2. <pending subtask>
- [ ] N. Verify — @<project>_reviewer: Review test results, check R<n> traceability, verify standards, confirm all requirements met

## Handoff Notes
- Environment: <env vars, config, setup requirements discovered during work>
- Existing tests: <test suites that must keep passing, regression baseline>
- Reuse: <existing utilities, patterns, or modules that should be reused>
- Warning: <things to avoid, hidden dependencies, non-obvious constraints>
```

**Context Summary** is updated by every subagent after completing work. It provides a 5-line executive summary that lets any subagent understand the task state without reading the full file.

**Structured Handoff** fields (Modified, Covers, Key decisions, For next subagent) ensure critical information flows between subagents. The coordinator updates these after each subtask completion.

**Handoff Notes** accumulate environment-level discoveries across the entire task. Any subagent can add entries about env vars, test baselines, reusable patterns, or warnings.

Spec Status is preserved in the per-task progress files.

## Feedback Rounds

When QC sends feedback on a completed task, a new feedback round is created via `/feedback`:

1. **User creates feedback file**: `project-x/fix-auth-bug/feedback-1.md` with QC feedback
2. **User runs**: `/feedback project-x fix-auth-bug feedback-1.md`
3. **Command creates**: `progress-fix-auth-bug-fb1.md` (new progress file) and `docs/design-fix-auth-bug-fb1.md` (new design)
4. **Spec review**: The coordinator presents the feedback requirements and design for approval
5. **Subagents work** in the same task folder and repo, addressing the feedback
6. **R<n> numbering continues**: If the original task ended at R8, feedback requirements start at R9
7. **When done**: Progress file Status changes to `[COMPLETED]`, ready for another feedback round or final completion

Each feedback round is self-contained with its own progress file, design file, and spec review gate, but works on the same codebase.

## Spec Review Gate

The spec review happens inside `/start-task` or `/feedback`, not as a separate command. When the coordinator starts a new task or feedback round:

1. Check `Spec Status` in PROGRESS.md
2. If `pending`:
   - Read `docs/requirements.md`
   - Create `docs/design-<task-name>.md` (e.g., `docs/design-fix-auth-bug.md`)
   - Present both to the user for approval
   - Wait for response
   - If approved → set `Spec Status: approved`, begin subtask routing
   - If changes requested → set `Spec Status: changes_requested`, report what needs changing
3. If `approved`: Proceed with normal subtask routing
4. If `changes_requested`: Report to user, wait for guidance