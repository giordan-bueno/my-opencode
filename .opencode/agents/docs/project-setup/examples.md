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
---

## fix-auth-bug
- [x] 1. Clone & navigate
  - Repo cloned to fix-auth-bug/external-repo/, branch fix-auth
- [x] 2. Identify issue
  - Bug: auth validator crashes on empty email → src/auth/validator.ts:42
- [ ] 3. Implement fix
- [ ] 4. Run tests
- [ ] 5. Verify — @project-x_reviewer: Run tests, check standards, confirm all requirements met

## add-login-feature
- [x] 1. Clone & navigate
  - Repo cloned to add-login-feature/external-repo/, main branch
- [x] 2. Identify scope
  - Need: login form component, auth service, route guards
- [ ] 3. Generate tests
- [ ] 4. Implement feature
- [ ] 5. Verify — @project-x_reviewer: Run tests, check standards, confirm all requirements met
```

**Benefits**:
- Active Task header immediately tells subagents which task and folder
- Context notes pass essential information between subagents
- Past tasks stay visible for reference (not deleted)
- Clear status on every subtask
- **Verify subtask is always the last step** — reviewer checks all work before completion gate

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

## Key Takeaway

The good version is a **routing layer** that points to detailed docs. The bad version tries to be an **encyclopedia** that includes everything inline.

For PROGRESS.md: **Always include the Active Task header** and **always add context notes** — subagents are stateless and need this information passed explicitly.

**Rule of thumb**: If a section needs more than 3-4 lines, move it to a reference doc in `<project>/docs/`.