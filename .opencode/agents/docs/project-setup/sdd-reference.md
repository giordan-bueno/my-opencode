# Spec-Driven Development (SDD) Reference

This workspace uses an adapted SDD workflow inspired by [harness-sdd](https://github.com/betta-tech/harness-sdd). The core principle: **requirements and design are approved by the human BEFORE any code is written.** Every requirement gets a stable `R<n>` ID that traces through design → subtasks → code → review.

## The SDD Flow

```
/new-project → (project-setup produces docs + requirements) → /start-task → (spec review gate) → (code) → (review) → (user confirms)
```

The `/start-task` command checks spec status before routing subagents. If specs aren't approved yet, the coordinator presents them for human review.

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

### Task prompts and task-specific requirements

Many outlier.ai tasks come with a **task prompt** — specific instructions, context, or a prompt to implement/fix that's unique to each task. These are stored in `<task-folder>/task-prompt.md`.

Task prompts add **task-specific requirements** that complement the project-level requirements:

- **Project-level requirements** (in `docs/requirements.md`): Stable R<n> IDs derived from the project PDFs. These apply to ALL tasks in the project. Example: R1-R5.
- **Task-specific requirements** (in `docs/design.md` "Task-Specific Requirements" section): New R<n> IDs derived from the task prompt, continuing numbering from the project requirements. These apply only to THIS task. Example: R6-R8.
- The reviewer verifies BOTH: project R<n> and task-specific R<n> must be covered.

When a task prompt exists:
1. The coordinator reads `task-prompt.md` before creating `design.md`
2. The coordinator extracts new requirements from the task prompt, continuing R<n> numbering from `requirements.md`
3. The coordinator adapts the subtask list based on the task prompt's instructions
4. The reviewer checks implementation against both project and task-specific requirements

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
```

## Traceability Rules

The `R<n>` IDs create a chain that the reviewer verifies:

1. **Every project-level `R<n>` must appear in at least one subtask** in the adapted subtask list (from `docs/subtasks.md` template, possibly adapted for the task)
2. **Every task-specific `R<n>` must appear in at least one subtask** in the adapted subtask list
3. **Every subtask must reference at least one `R<n>`** (except the Verify subtask, which implicitly covers all)
4. **Every `R<n>` (project and task-specific) must have at least one verification criterion** in `docs/verification.md`
5. **The reviewer checks the full chain**: R\<n\> → subtask → implementation → test

If any `R<n>` is untested or uncovered, the reviewer reports `CHANGES_REQUESTED`.

## Subtask Format with Traceability

Enhanced `docs/subtasks.md` format — each subtask references which requirements it covers:

```markdown
## Subtask Template

1. **Implement auth middleware** — @<project>_coder: Add JWT middleware to protected routes. Covers: R1, R2
2. **Add error handler** — @<project>_coder: Create error boundary for API calls. Covers: R3
3. **Add audit logger** — @<project>_coder: Log all data modifications with required fields. Covers: R4
4. **Verify** — @<project>_reviewer: Confirm R1-R4 are met, run tests, check standards
```

## Verification Format with Traceability

Enhanced `docs/verification.md` — each criterion references R\<n\> IDs:

```markdown
## Verification Criteria

- [ ] R1: Auth middleware blocks unauthenticated access (test: `npm test -- auth.test.ts`)
- [ ] R2: Successful login redirects to dashboard (test: `npm test -- login.test.ts`)
- [ ] R3: Error handler catches API failures gracefully (test: `npm test -- errors.test.ts`)
- [ ] R4: Audit logger records timestamp, user ID, and action (test: `npm test -- audit.test.ts`)
- [ ] Code follows conventions defined in docs/standards.md
- [ ] No debug artifacts left (no console.log, print statements)
```

## Spec Status in PROGRESS.md

The active task header includes a `Spec Status` field:

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

When a task is archived to History, the spec status is preserved.

## Spec Review Gate

The spec review happens inside `/start-task`, not as a separate command. When the coordinator starts a new task:

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