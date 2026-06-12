# AGENTS.md Examples: Good vs Bad

## Bad Example (Too Verbose)

```markdown
## Workflow
1. First, the user logs into outlier.ai and navigates to the project dashboard.
2. Then they click on "New Task" and select the task type from the dropdown.
3. The AI agent should then clone the repository using `git clone <url>`.
4. After cloning, run `npm install` to install dependencies.
5. Then run `npm run dev` to start the development server.
6. The user reviews the output on the outlier.ai interface...
[continues for 50+ lines]
```

**Problems**:
- Inline everything (no reference docs)
- Too detailed for main AGENTS.md
- Mixes user and AI responsibilities without clear separation
- 50+ lines when 5 would suffice

## Good Example (Lean with References)

```markdown
## Workflows
- **New task setup**: Clone repo, install deps, start dev server → See `docs/workflow.md`
- **Task submission**: User submits on outlier.ai, AI prepares code and explanations

## User vs AI Responsibilities
**User**: Logs into outlier.ai, selects tasks, reviews outputs
**AI**: Clones repos, installs deps, writes code, runs tests → See `docs/workflow.md`
```

**Benefits**:
- 5 lines instead of 50+
- Clear separation of responsibilities
- Points to detailed docs for implementation
- Easy to scan and understand

## Bad Example: Progress Tracking (No Context)

```markdown
## fix-auth-bug
- [x] 1. Clone repo
- [x] 2. Identify issue
- [ ] 3. Fix the bug
- [ ] 4. Run tests
```

**Problems**:
- No Active Task header — subagents don't know which task to work on
- No Task Folder — subagents don't know where files are
- No context notes — next subagent has no idea what was found or done
- Past and current tasks are indistinguishable

## Good Example: Progress Tracking (Active Task Header + Context)

```markdown
# Progress Tracker — project-x

---
Active Task: fix-auth-bug
Task Folder: project-x/fix-auth-bug/
Spec Status: approved
---

## fix-auth-bug
- [x] 1. Clone & navigate
  - Repo cloned to fix-auth-bug/external-repo/, branch fix-auth
- [x] 2. Identify issue
  - Bug: auth validator crashes on empty email → src/auth/validator.ts:42
  - Covers: R1, R2
- [!] 3. Implement fix
  - BLOCKED: The auth module uses a custom validator from `@company/auth-lib` which isn't documented in the PDFs. Need user to clarify the expected behavior for empty strings vs null.
- [ ] 4. Run tests
- [ ] 5. Verify — @project-x_reviewer: Run tests, check standards, confirm all requirements met

## History

### add-login-feature — 2026-06-08 16:45
- [x] 1. Clone & navigate
  - Repo cloned to add-login-feature/external-repo/, main branch
- [x] 2. Identify scope
  - Need: login form component, auth service, route guards
- [x] 3. Implement feature
  - Created LoginForm.tsx, AuthService.ts, RouteGuards.ts
- [x] 4. Run tests
  - All 23 tests passing
- [x] 5. Verify — APPROVED
  - Code follows standards, all requirements met.
```

**Benefits**:
- Active Task header immediately tells subagents which task and folder
- Context notes pass essential information between subagents
- `[!]` blocked marker clearly signals when a subagent is stuck and needs user intervention
- History section archives completed tasks with timestamps for easy reference
- Verify subtask is always the last step — reviewer checks all work before completion gate

## Good Example: Spec Approval Gate (SDD)

Before coding begins, the coordinator presents specs for human approval:

```markdown
---
Active Task: fix-auth-bug
Task Folder: project-x/fix-auth-bug/
Spec Status: pending
---
```

Coordinator presents to user:
> "Spec for task 'fix-auth-bug':
> **Requirements**: R1 (auth required), R2 (login redirect), R3 (error display), R4 (audit logging)
> **Task Context**: Fix the authentication validator crash when email is empty — the prompt asks for null-safe handling with proper error responses
> **Task-Specific Requirements**: R5 (null-safe email validation), R6 (proper error response for empty inputs)
> **Design**: Add null check in validator, create error response handler, add audit logging
> **Alternatives considered**: Session-based auth (rejected — PDF requires JWT)
> Approve spec and proceed? (y/n/changes)"

After approval:
```markdown
---
Active Task: fix-auth-bug
Task Folder: project-x/fix-auth-bug/
Spec Status: approved
---
```

## Good Example: Requirements with EARS and R<n> Traceability

```markdown
## Requirements — project-x

### R1: Authentication required
The system MUST require valid JWT credentials before granting access to any protected resource.

### R2: Login redirect
WHEN a user provides valid credentials, the system MUST redirect them to the dashboard within 2 seconds.

### R3: Error display
IF an API request fails, THEN the system MUST display a user-friendly error message and log the error.

### R4: Audit logging
WHILE the system is in production mode, the system MUST log all data modification operations with timestamp and user ID.
```

## Good Example: Subtask Template with R<n> References

```markdown
## Subtask Template

1. **Implement JWT middleware** — @project-x_coder: Add auth middleware to protected routes. Covers: R1, R2
2. **Add error handler** — @project-x_coder: Create error boundary for API calls. Covers: R3
3. **Add audit logger** — @project-x_coder: Log all data modifications with required fields. Covers: R4
4. **Verify** — @project-x_reviewer: Confirm R1-R4 are met, run tests, check standards
```

## Good Example: Verification Criteria with R<n> References

```markdown
## Verification Criteria

- [ ] R1: JWT middleware blocks unauthenticated access (test: `npm test -- auth.test.ts`)
- [ ] R2: Successful login redirects to dashboard (test: `npm test -- login.test.ts`)
- [ ] R3: Error handler catches API failures gracefully (test: `npm test -- errors.test.ts`)
- [ ] R4: Audit logger records timestamp and user ID (test: `npm test -- audit.test.ts`)
- [ ] Code follows conventions defined in docs/standards.md
- [ ] No debug artifacts left
```

## Good Example: Completion Gate

After all subtasks (including Verify) are marked `[x]` and the reviewer approves:

```
Coordinator: "All subtasks completed for task 'fix-auth-bug'. Reviewer has approved.
Summary:
- Fixed auth validator crash on empty email (src/auth/validator.ts:42)
- All tests passing (12/12)
- No regressions detected

Please review the changes and confirm task completion, or request changes."
```

The coordinator **never marks a task complete automatically** — it always waits for the user to confirm.

## Good Example: Paused Task in History

When a task is paused (e.g., outlier task expired), it moves to History with the `PAUSED` tag and all progress preserved:

```markdown
## History

### fix-auth-bug — 2026-06-09 14:30 [PAUSED: task expired on outlier]
- [x] 1. Clone & navigate
  - Repo cloned to fix-auth-bug/external-repo/, branch fix-auth
- [x] 2. Identify issue
  - Bug: auth validator crashes on empty email → src/auth/validator.ts:42
- [!] 3. Implement fix
  - BLOCKED: auth module uses custom validator from @company/auth-lib — need clarification on expected behavior
- [ ] 4. Run tests
- [ ] 5. Verify — @project-x_reviewer

### add-login-feature — 2026-06-08 16:45
- [x] 1. Clone & navigate
  - Repo cloned to add-login-feature/external-repo/, main branch
- [x] 2. Identify scope
  - Need: login form component, auth service, route guards
- [x] 3. Implement feature
  - Created LoginForm.tsx, AuthService.ts, RouteGuards.ts
- [x] 4. Run tests
  - All 23 tests passing
- [x] 5. Verify — APPROVED
  - Code follows standards, all requirements met.
```

**Key points**:
- Paused tasks keep `[PAUSED: <reason>]` tag so they're easy to identify in History
- All progress is preserved: `[x]` completed, `[!]` blocked, `[ ]` pending
- Resuming with `/resume-task` moves the entry back to the active area and removes the `PAUSED` tag

## Good Example: Design with Task Prompt

When a task has a task-specific prompt from outlier.ai (`task-prompt.md`), the design includes additional sections:

```markdown
## Design — fix-auth-bug

### Task Context
Fix the authentication validator crash when email is empty. The task prompt requires null-safe handling with proper error responses and audit trail for all auth failures.

### Task-Specific Requirements
### R5: Null-safe email validation
WHEN a user submits a form with an empty email field, the system MUST validate gracefully without crashing and return a structured error response.

### R6: Error response format
IF an authentication request fails validation, THEN the system MUST return a JSON error response with fields: `error`, `message`, `statusCode`.

### Approach
Add null check in auth validator before JWT verification, create dedicated error response handler for validation failures.

### Files to Modify
| File | Change Type | R<n> Covered |
|------|------------|--------------|
| src/auth/validator.ts | Modify | R1, R2, R5, R6 |
| src/errors/handler.ts | Create | R3, R6 |
| src/middleware/logger.ts | Modify | R4 |

### Alternatives Considered
1. **Silent fail with default** — Rejected: Task prompt explicitly requires structured error responses
2. **Global error boundary** — Rejected: Per-route handlers provide better error context

### Risks
- R5 edge case: null vs empty string vs undefined — must handle all three
- R6 response format must match the exact structure specified in the task prompt

### Dependencies
- jsonwebtoken@^9.0
- Existing Express middleware in src/middleware/
```

**Key points**:
- Task-specific R<n> IDs continue from project requirements (project has R1-R4, task-specific starts at R5)
- Task Context summarizes the task prompt so subagents understand the specific task they're working on
- Files to Modify table includes both project and task-specific R<n> IDs

The good version is a **routing layer** that points to detailed docs. The bad version tries to be an **encyclopedia** that includes everything inline.

For PROGRESS.md: **Always include the Active Task header** and **always add context notes** — subagents are stateless and need this information passed explicitly.

**Rule of thumb**: If a section needs more than 3-4 lines, move it to a reference doc in `<project>/docs/`.