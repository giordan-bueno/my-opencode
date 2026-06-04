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

## Key Takeaway

The good version is a **routing layer** that points to detailed docs. The bad version tries to be an **encyclopedia** that includes everything inline.

**Rule of thumb**: If a section needs more than 3-4 lines, move it to a reference doc in `<project>/docs/`.
