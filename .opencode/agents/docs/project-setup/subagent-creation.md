# Dynamic Subagent Creation

After creating the project AGENTS.md and reference docs, analyze the PDFs to identify distinct task types that warrant dedicated subagents.

## Model Selection Logic

**Fast model** (`opencode-go/deepseek-v4-flash`) for:
- Keywords: "user assistance", "checklist", "explanation", "guidance", "website", "outlier.ai", "documentation"
- Tasks: Following procedures, providing explanations, assisting with website tasks
- **NOT for**: code review, critical verification, quality assurance

**Balanced model** (`opencode-go/qwen3.7-plus`) for:
- Keywords: "setup", "configuration", "integration", "workflow", "coordination"
- Tasks: Project setup, configuration, moderate complexity, task routing

**Reasoning model** (`opencode-go/qwen3.7-max`) for:
- Keywords: "coding", "implementation", "testing", "debugging", "refactoring", "analysis", "architecture", "review", "verification"
- Tasks: Code writing, test execution, complex problem-solving, **code review and verification**

## Common Subagent Types

When analyzing the PDFs, look for these common patterns:

**Always propose**:
- **Coordinator** (`<project>_coordinator`) — orchestrates all other subagents, manages PROGRESS.md, handles routing. Model: balanced. See `coordinator-template.md`.

**Propose for coding projects**:
- **Coder** (`<project>_coder`) — implements code changes, writes tests. Model: reasoning.
- **Reviewer** (`<project>_reviewer`) — verifies completed work, checks standards compliance, runs tests. Never edits code. Model: reasoning. Always proposed AFTER the coder. See `reviewer-template.md`.

**Propose based on PDF content**:
- **Tester** (`<project>_tester`) — runs and verifies test suites. Model: reasoning. If separate from coder.
- **Navigator** (`<project>_navigator`) — assists user with outlier.ai website tasks. Model: fast.

**Every coding project should have at least**: coordinator + coder + reviewer. The reviewer is the last subtask in every template — it verifies all work before the human completion gate.

## Approval Workflow

For each identified subagent:

1. **Present proposal** to user:
   ```
   Proposed subagent: @<project>_<role>
   Model: [fast/balanced/reasoning] ([model-name])
   Purpose: [brief description from PDF analysis]
   Complexity: [why this model was chosen - reference specific PDF keywords]
   
   Approve? (y/n)
   ```

2. **Wait for response**:
   - If approved: Create the subagent
   - If rejected: Skip without asking why, continue to next proposed subagent

3. **Repeat** until all proposed subagents are processed

**No maximum limit**: Create as many subagents as the PDFs require. Each distinct task type should have its own subagent.

## Non-Overlapping Responsibilities

**Each subagent must have a single, well-defined scope**:
- No two subagents should handle the same task type
- Each subagent owns one specific area of the project
- If responsibilities overlap, merge them into one subagent or clarify the boundaries
- The coordinator handles routing; other subagents handle execution

## Naming Convention

Use underscore pattern: `<project>_<role>.md`

**Important**: When creating subagent files, replace all `<project>` and `<project-name>` placeholders in the template with the actual project name. Subagent prompts reference `<project>/PROGRESS.md`, `<project>/docs/subtasks.md`, etc. — these must use the real project folder name, not the placeholder.

Examples:
- `data_pipeline_extractor.md`
- `data_pipeline_validator.md`
- `web_scraper_navigator.md`
- `web_scraper_parser.md`

## AGENTS.md Documentation

After creating subagents, add this section to the project AGENTS.md:

```markdown
## Project Subagents

- **@<project>_<role1>** - [purpose] (model: [fast/balanced/reasoning])
- **@<project>_<role2>** - [purpose] (model: [fast/balanced/reasoning])
```
