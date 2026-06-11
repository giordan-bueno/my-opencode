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

## Design Format (docs/design.md)

**Per-task file** — created/overwritten each time a task starts via `/start-task`. Always created, even for simple tasks.

```markdown
## Design — <task-name>

### Approach
<Chosen approach with brief rationale>

### Files to Modify
| File | Change Type | R<n> Covered |
|------|------------|--------------|
| src/auth/middleware.ts | Modify | R1, R2 |
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

1. **Every `R<n>` must appear in at least one subtask** in `docs/subtasks.md`
2. **Every subtask must reference at least one `R<n>`** (except the Verify subtask, which implicitly covers all)
3. **Every `R<n>` must have at least one verification criterion** in `docs/verification.md`
4. **The reviewer checks the full chain**: R\<n\> → subtask → implementation → test

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
   - Create/present `docs/design.md`
   - Present both to the user for approval
   - Wait for response
   - If approved → set `Spec Status: approved`, begin subtask routing
   - If changes requested → set `Spec Status: changes_requested`, report what needs changing
3. If `approved`: Proceed with normal subtask routing
4. If `changes_requested`: Report to user, wait for guidance