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
- No Active Task pointer — subagents don't know which task to work on
- No Task Folder — subagents don't know where files are
- No context notes — next subagent has no idea what was found or done
- No separate progress file — task details mixed with pointer

## Good Example: Progress Tracking (Pointer + Per-Task File)

**PROGRESS.md** (pointer file):
```markdown
# Progress Tracker — project-x

---
Active Task: fix-auth-bug
Task Folder: project-x/fix-auth-bug/
Spec Status: approved
---
```

**progress-fix-auth-bug.md** (per-task file):
```markdown
# Task: fix-auth-bug

---
Status: In Progress
Created: 2026-06-11
Design: docs/design-fix-auth-bug.md
Task Prompt: fix-auth-bug/task-prompt.md
Spec Status: approved
---

- [x] 1. Clone & navigate
  - Repo cloned to fix-auth-bug/external-repo/, branch fix-auth
  - Covers: R1, R2
- [!] 3. Implement fix
  - BLOCKED: The auth module uses a custom validator from `@company/auth-lib` which isn't documented in the PDFs. Need user to clarify the expected behavior for empty strings vs null.
- [ ] 4. Run tests
- [ ] 5. Verify — @project-x_reviewer: Run tests, check standards, confirm all requirements met
```

**Benefits**:
- PROGRESS.md pointer immediately tells subagents which task is active — they then open the corresponding progress file
- Per-task files mean no data movement between sections — pause/resume is just a status change
- Context notes pass essential information between subagents
- `[!]` blocked marker clearly signals when a subagent is stuck and needs user intervention
- Old progress files stay as historical reference — no History section to manage
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

1. **Explore codebase and report findings** — @project-x_coder: Read relevant source files, existing test suite, hidden dependencies. Produce Code Exploration section in design file. Covers: all R<n>
2. **Implement JWT middleware** — @project-x_coder: Add JWT middleware to protected routes. Covers: R1, R2
3. **Add error handler** — @project-x_coder: Create error boundary for API calls. Covers: R3
4. **Add audit logger** — @project-x_coder: Log all data modifications with required fields. Covers: R4
5. **Write and run tests** — @project-x_tester: Write tests covering R1-R4 per Test Plan + code-driven tests from exploration. Run test suite and report results. Covers: R1, R2, R3, R4
6. **Verify** — @project-x_reviewer: Review test results, check R<n> traceability, verify standards, confirm all requirements met
```

## Good Example: Subtask Template for TDD Project

```markdown
## Subtask Template — TDD Project

1. **Write fail-to-pass tests** — @project-x_tester: Write failing tests for R1-R4 per draft Test Plan (RED phase). Covers: R1, R2, R3, R4
2. **Explore codebase and report findings** — @project-x_coder: Read relevant source files, existing test suite, hidden dependencies. Produce Code Exploration section. Covers: all R<n>
3. **Implement JWT middleware** — @project-x_coder: Add JWT middleware to protected routes. Covers: R1, R2
4. **Add error handler** — @project-x_coder: Create error boundary for API calls. Covers: R3
5. **Add audit logger** — @project-x_coder: Log all data modifications with required fields. Covers: R4
6. **Write pass-to-pass + code-driven tests, run full suite** — @project-x_tester: Write pass-to-pass tests, add code-driven tests from exploration, run full suite, all must pass (GREEN phase). Covers: R1, R2, R3, R4
7. **Verify** — @project-x_reviewer: Review test results, check R<n> traceability, verify standards, confirm all requirements met
```

## Good Example: Verification Criteria with R<n> References

```markdown
## Verification Criteria

- [ ] R1: JWT middleware blocks unauthenticated access
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
- [ ] R4: Audit logger records timestamp and user ID
  - Verification: Automated test
  - Test command: `npm test -- audit.test.ts`
  - Test type: Standard
- [ ] Code follows conventions defined in docs/standards.md
  - Verification: Manual code review
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

## Good Example: Paused Task

When a task is paused (e.g., outlier task expired), its progress file changes status:

**PROGRESS.md** (pointer resets):
```markdown
# Progress Tracker — project-x

---
Active Task: <none>
Task Folder: <none>
Spec Status: <none>
---
```

**progress-fix-auth-bug.md** (status changes to paused):
```markdown
# Task: fix-auth-bug

---
Status: [PAUSED: task expired on outlier]
Created: 2026-06-11
Design: docs/design-fix-auth-bug.md
Task Prompt: fix-auth-bug/task-prompt.md
Spec Status: approved
---

- [x] 1. Clone & navigate
  - Repo cloned to fix-auth-bug/external-repo/, branch fix-auth
- [x] 2. Identify issue
  - Bug: auth validator crashes on empty email → src/auth/validator.ts:42
- [!] 3. Implement fix
  - BLOCKED: auth module uses custom validator from @company/auth-lib — need clarification
- [ ] 4. Run tests
- [ ] 5. Verify — @project-x_reviewer
```

**Key points**:
- Paused tasks keep `[PAUSED: <reason>]` in their progress file Status field
- All progress is preserved: `[x]` completed, `[!]` blocked, `[ ]` pending
- Resuming with `/resume-task` simply changes Status back to `In Progress` and updates the PROGRESS.md pointer
- No data movement between sections — just a status field change

## Good Example: Design with Task Prompt

When a task has a task-specific prompt from outlier.ai (`task-prompt.md`), the design includes additional sections. Note that design files are per-task (e.g., `docs/design-fix-auth-bug.md`):

```markdown
## Design — fix-auth-bug (file: docs/design-fix-auth-bug.md)

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

For progress tracking: **PROGRESS.md is a minimal pointer** — subagents read it to find which `progress-<task>.md` file to open for details. Each task has its own progress file, so no data movement is needed for pause/resume/complete.

**Rule of thumb**: If a section needs more than 3-4 lines, move it to a reference doc in `<project>/docs/`.

## Good Example: Code Exploration Section

After the coder explores the codebase, the design file gets a Code Exploration section:

```markdown
### Code Exploration

#### Existing Code Affected
- `src/auth/middleware.ts:42` — Existing `validateToken()` function. The spec says "Add JWT middleware" but there's already an auth middleware that needs modification, not a new one.
- `src/auth/session.ts:15` — Session auth system that must coexist with new JWT auth. Not mentioned in the spec.
- `src/errors/handler.ts` — Existing error handler already returns JSON errors. R3 can reuse it instead of creating a new one.

#### Existing Test Suite
- `tests/auth.test.ts` — 12 existing tests, all must continue passing after changes (regression baseline)
- `tests/errors.test.ts` — 4 existing tests for error handling

#### Hidden Dependencies
- JWT secret must be in `process.env.JWT_SECRET` (discovered in `src/config.ts:8`)
- Auth middleware must be registered before session middleware in `src/app.ts:23`
- `logAction()` utility already exists in `src/utils/logger.ts` — should be reused for R4 instead of creating a new logger

#### Subtask Revisions
Based on code exploration, the original subtask plan is revised:
- Original subtask "Implement auth middleware" → Split into:
  - "Modify existing auth middleware to add JWT support" (R1, R2)
  - "Add error type for auth validation failures" (R3, R6)
- Original subtask "Add audit logger" → Clarify: reuse existing `logAction()` utility (R4)

#### Code-Driven Tests (supplementary to Test Plan)
- REGRESSION: All 12 existing tests in `tests/auth.test.ts` must pass after changes (Pass-to-pass)
- EDGE CASE: `validateToken(null)` should return 401 — discovered from `src/auth/middleware.ts:37` (Standard)
- INTEGRATION: JWT auth and session auth must coexist without conflicts (Standard)
```

**Key points**:
- The Code Exploration section is populated **after** the coder reads the codebase, not during spec review
- Subtask Revisions show how the plan adapts based on what the coder discovered
- Code-Driven Tests are supplementary — they don't replace the Test Plan, they extend it
- Existing Test Suite section provides the regression baseline that the tester must verify
- The coordinator reads these findings and may update the subtask list in the progress file

## Good Example: Feedback Round Progress File

When QC sends feedback on a completed task, a new feedback round creates a separate progress file:

**PROGRESS.md** (pointer updated to feedback round):
```markdown
# Progress Tracker — project-x

---
Active Task: fix-auth-bug-fb1
Task Folder: project-x/fix-auth-bug/
Spec Status: pending
---
```

**progress-fix-auth-bug-fb1.md** (feedback round progress):
```markdown
# Task: fix-auth-bug-fb1 (Feedback Round 1)

---
Status: In Progress
Created: 2026-06-12
Design: docs/design-fix-auth-bug-fb1.md
Task Prompt: fix-auth-bug/task-prompt.md
Feedback From: fix-auth-bug/feedback-1.md
Previous: progress-fix-auth-bug.md
Spec Status: pending
---

- [ ] 1. Fix email plus sign handling — @project-x_coder: Update regex to accept + in email addresses. Covers: R9
- [ ] 2. Add error codes to API responses — @project-x_coder: Add error_code field to all auth error responses. Covers: R10
- [ ] 3. Verify — @project-x_reviewer: Confirm R9-R10 are met, run tests, check feedback addressed
```

**progress-fix-auth-bug.md** (original, now completed):
```markdown
# Task: fix-auth-bug

---
Status: [COMPLETED]
Created: 2026-06-11
Design: docs/design-fix-auth-bug.md
Task Prompt: fix-auth-bug/task-prompt.md
Spec Status: approved
---

- [x] 1. Clone & navigate
- [x] 2. Implement fix
- [x] 3. Run tests
- [x] 4. Verify — @project-x_reviewer
```

**Key points**:
- Original progress file marked `[COMPLETED]` — clean separation
- Feedback round gets its own progress file with `-fb1` suffix
- R<n> IDs continue from original task (original was R1-R8, feedback starts R9)
- Same task folder and repo — feedback works on the same codebase
- Multiple feedback rounds: `-fb1`, `-fb2`, etc.