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
- **Coder** (`<project>_coder`) — implements code changes, explores codebase before implementation. Tier: coding. Reads `docs/requirements.md` (R<n> IDs), `docs/design.md` (technical approach, Code Exploration section), and the actual codebase before implementing. Also responsible for the "Explore codebase" subtask that discovers hidden dependencies, existing tests, and code-driven test needs.
- **Tester** (`<project>_tester`) — writes test files tracing R<n> IDs, runs test suites, reports results. Never edits implementation files. Tier: coding. Always proposed alongside the coder for coding projects. See `tester-template.md`.
- **Reviewer** (`<project>_reviewer`) — verifies completed work, checks standards, validates R<n> traceability (reads test results, does not re-run). Never edits code. Tier: reasoning. Always proposed AFTER the tester. See `reviewer-template.md`.

**Propose based on PDF content**:
- **Navigator** (`<project>_navigator`) — assists user with outlier.ai website tasks. Tier: fast.

**Every coding project should have at least**: coordinator + coder + tester + reviewer. The tester writes and runs tests before the reviewer verifies. The reviewer reads test results (does not re-run) and validates R<n> traceability.

## Approval Workflow

For each identified subagent:

1. **Present proposal** to user:
   ```
   Proposed subagent: @<project>_<role>
   Tier: [fast/balanced/coding/reasoning]
   Model: opencode-go/<primary>
   Fallback: opencode-go/<fallback1> [, opencode/<fallback2>]
   Skills: [list skills the subagent should invoke, or "None"]
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

## Skills Assignment

Subagents can invoke OpenCode skills (e.g., `git-commit`) during task execution. Skills are declared in two places:

1. **Frontmatter `# skills:` comment** — Documents which skills the subagent is expected to use. Left empty by default; add skill names when a specific subagent needs them (e.g., `# skills: git-commit` for a coder that should commit its work).
2. **Prompt `## Skills` section** — Describes when and how to use each skill. Left as "None assigned" by default; add entries when a skill is assigned.

### Which subagents get skills?

| Role | `skill` permission | Typical skills |
|------|-------------------|----------------|
| Coordinator | `allow` | May invoke skills for setup or routing |
| Coder | `allow` | `git-commit` (if tasks require committing code) |
| Tester | `allow` | `git-commit` (if tasks require committing test files) |
| Reviewer | `deny` | None — reviewers read and report, never modify state |
| Navigator | `deny` | None — read-only assistance |
| Setup specialist | `allow` | `git-commit` (if tasks require committing configs) |

### Skill usage per task

The coordinator decides whether a skill is needed on a per-task basis by reading `task-prompt.md` and `design-<task-name>.md`. When a task requires committing code, the coordinator includes "use git-commit skill" in the subtask instructions. When it doesn't, the skill is not mentioned.

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
