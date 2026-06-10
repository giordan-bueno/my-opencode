# Dynamic Subagent Creation

After creating the project AGENTS.md and reference docs, analyze the PDFs to identify distinct task types that warrant dedicated subagents.

## Model Selection Logic

Four tiers with fallback chains. The `model:` frontmatter field uses the primary. Swap to a fallback manually if the primary is unavailable (rate-limited, down, etc.).

| Tier | Primary | Fallback 1 (Go) | Fallback 2 (Zen Free) |
|------|---------|------------------|------------------------|
| **Fast** | `opencode-go/deepseek-v4-flash` | — | `opencode/deepseek-v4-flash-free` |
| **Balanced** | `opencode-go/qwen3.7-plus` | `opencode-go/minimax-m3` | — |
| **Coding** | `opencode-go/kimi-k2.6` | `opencode-go/qwen3.7-max` | — |
| **Reasoning** | `opencode-go/glm-5.1` | `opencode-go/mimo-v2.5-pro` | `opencode/mimo-v2.5-free` |

**Fast tier** (`opencode-go/deepseek-v4-flash`) for:
- Keywords: "user assistance", "checklist", "explanation", "guidance", "website", "outlier.ai", "documentation"
- Tasks: Following procedures, providing explanations, assisting with website tasks, git operations, PDF processing
- Fallback: `opencode/deepseek-v4-flash-free` (Zen free tier, requires `/connect` setup)
- **NOT for**: code review, critical verification, quality assurance

**Balanced tier** (`opencode-go/qwen3.7-plus`) for:
- Keywords: "setup", "configuration", "integration", "workflow", "coordination"
- Tasks: Project setup, configuration, task routing, tool calling, schema generation
- Fallback: `opencode-go/minimax-m3` (reliable JSON structure and parameter adherence)
- **NOT for**: code generation, architectural planning, critical verification

**Coding tier** (`opencode-go/kimi-k2.6`) for:
- Keywords: "coding", "implementation", "debugging", "refactoring", "multi-file"
- Tasks: Code writing, cross-dependency management, repository intelligence, multi-file code generation
- Fallback: `opencode-go/qwen3.7-max` (flagship tool orchestration and edge-case handling)
- **NOT for**: simple procedures, lightweight routing, architectural planning

**Reasoning tier** (`opencode-go/glm-5.1`) for:
- Keywords: "architecture", "review", "verification", "analysis", "planning", "complex logic"
- Tasks: Architectural planning, complex analysis, code review, verification, deep reasoning
- Fallback 1: `opencode-go/mimo-v2.5-pro` (deep context agent processing)
- Fallback 2: `opencode/mimo-v2.5-free` (Zen free tier, 1M context window, requires `/connect` setup)
- **NOT for**: routine procedures, file system reads, lightweight routing

## Common Subagent Types

When analyzing the PDFs, look for these common patterns:

**Always propose**:
- **Coordinator** (`<project>_coordinator`) — orchestrates all other subagents, manages PROGRESS.md, handles routing. Tier: balanced. See `coordinator-template.md`.

**Propose for coding projects**:
- **Coder** (`<project>_coder`) — implements code changes, writes tests. Tier: coding.
- **Reviewer** (`<project>_reviewer`) — verifies completed work, checks standards compliance, runs tests. Never edits code. Tier: reasoning. Always proposed AFTER the coder. See `reviewer-template.md`.

**Propose based on PDF content**:
- **Tester** (`<project>_tester`) — runs and verifies test suites. Tier: coding. If separate from coder.
- **Navigator** (`<project>_navigator`) — assists user with outlier.ai website tasks. Tier: fast.

**Every coding project should have at least**: coordinator + coder + reviewer. The reviewer is the last subtask in every template — it verifies all work before the human completion gate.

## Approval Workflow

For each identified subagent:

1. **Present proposal** to user:
   ```
   Proposed subagent: @<project>_<role>
   Tier: [fast/balanced/coding/reasoning]
   Model: opencode-go/<primary>
   Fallback: opencode-go/<fallback1> [, opencode/<fallback2>]
   Purpose: [brief description from PDF analysis]
   Complexity: [why this tier was chosen - reference specific PDF keywords]
   
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

- **@<project>_<role1>** - [purpose] (tier: [fast/balanced/coding/reasoning])
- **@<project>_<role2>** - [purpose] (tier: [fast/balanced/coding/reasoning])
```
