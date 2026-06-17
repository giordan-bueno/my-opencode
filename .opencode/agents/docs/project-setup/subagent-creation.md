# Dynamic Subagent Creation

After creating the project AGENTS.md and reference docs, analyze the PDFs to identify distinct task types that warrant dedicated subagents.

## Model Selection Logic

Four tiers with fallback chains. The `model:` frontmatter field uses the primary; swap to a fallback manually if the primary is unavailable. **The canonical tier → model/fallback table lives in `docs/model-strategy.md`** — don't duplicate the model IDs here. This section only covers *which tier to choose* for a given role.

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
- **Coordinator** (`<project>_coordinator`) — a **primary** agent (`mode: primary`, NOT a subagent) that orchestrates all other (worker) subagents, manages PROGRESS.md, holds the human approval gates, and routes subtasks at **depth 1**. The user switches to it (Tab) to drive a task. Tier: balanced. See `coordinator-template.md`.

**Propose for coding projects**:
- **Coder** (`<project>_coder`) — implements code changes, explores codebase before implementation. Tier: coding. Reads `docs/requirements.md` (R<n> IDs), `docs/design-<task-name>.md` (technical approach, Code Exploration section), and the actual codebase before implementing. Also responsible for the "Explore codebase" subtask that discovers hidden dependencies, existing tests, and code-driven test needs. See `.opencode/agents/docs/project-setup/coder-template.md` for the structural template — it defines mandatory sections (Hard Rules, SDD Awareness, Code Exploration, structured handoff) and a placeholder `## Project-Specific Coding Rules` section that @project-setup fills in based on the project's PDFs, `docs/tech-stack.md`, and `docs/standards.md`.
- **Tester** (`<project>_tester`) — writes test files tracing R<n> IDs, runs test suites, reports results. Never edits implementation files. Tier: coding. Always proposed alongside the coder for coding projects. See `tester-template.md`.
- **Reviewer** (`<project>_reviewer`) — verifies completed work, checks standards, validates R<n> traceability (reads test results, does not re-run). Never edits code. Tier: reasoning. Always proposed AFTER the tester. See `reviewer-template.md`.

**Propose based on PDF content**:
- **Navigator** (`<project>_navigator`) — assists user with outlier.ai website tasks. Tier: fast.

**Every coding project should have at least**: coordinator + coder + tester + reviewer. The tester writes and runs tests before the reviewer verifies. The reviewer reads test results (does not re-run) and validates R<n> traceability.

## Deferred Subagent Creation

When the project PDFs do not specify a tech stack (language, framework, test runner), coding subagents (coder, tester, reviewer) cannot be fully configured. In this case:

1. **During project setup**: Propose only the coordinator agent (a **primary** agent). Tell the user: "The PDFs don't specify a tech stack. I'll create the coordinator now. After the first task discovers the tech stack from the repo, use `/add-subagent` to create coding subagents with the discovered information."
2. **During the first task** (`/start-task`): If a cloned repo exists in the task folder, the coordinator performs tech discovery by inspecting the repo's dependency files (package.json, requirements.txt, Cargo.toml, go.mod, pom.xml, etc.) and the task prompt. If new tech stack info is discovered:
   - Update `docs/tech-stack.md`, `docs/testing.md`, and `docs/standards.md` with the discovered information
   - Update the "Tech Discovery Status" section in `<project>/AGENTS.md`
   - Recommend `/add-subagent` to the user to create coding subagents (coder, tester, reviewer) if they don't exist yet
3. **After tech discovery**: The user runs `/add-subagent <project> coder`, `/add-subagent <project> tester`, and `/add-subagent <project> reviewer` to create the missing subagents with project-specific information from the discovered tech stack. The `/add-subagent` command reads the updated docs and task prompt to generate appropriate role-specific prompts.
4. **During code exploration**: Even if coding subagents exist, the coder's exploration may discover additional tech details (hidden dependencies, specific libraries, test frameworks not mentioned in PDFs). The coordinator updates docs with these findings.

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

Subagents can invoke OpenCode skills during task execution. Skills come from two sources:

1. **Bundled skills** (in `.agents/skills/`): installed into the workspace and tracked in git, e.g., `git-commit` (from the `awesome-copilot` source). Available to every project.
2. **skills.sh ecosystem** (installed via `/add-skill`): Community skills from [skills.sh](https://www.skills.sh/), e.g., `tdd`, `systematic-debugging`, framework-specific best practices

Skills are declared in two places:

1. **Frontmatter `# skills:` comment** — Documents which skills the subagent is expected to use. Left empty by default; add skill names when a specific subagent needs them (e.g., `# skills: git-commit` for a coder that should commit its work).
2. **Prompt `## Skills` section** — Describes when and how to use each skill. Left as "None assigned" by default; add entries when a skill is assigned.

> **Important — `# skills:` is documentary, not enforced.** It is a YAML *comment*: OpenCode does not parse it, and there is no per-agent skill allowlist. Any subagent with `skill: allow` can invoke **any** installed skill. So "attaching" a skill to one role (via `/add-skill --attach`) records *intent* and documents usage — it does **not** technically prevent other subagents from using that skill. Use the `skill: allow` / `skill: deny` permission to actually gate access (e.g., the reviewer has `skill: deny`).

### Which subagents get skills?

| Role | `skill` permission | Typical skills |
|------|-------------------|----------------|
| Coordinator | `allow` | May invoke skills for setup or routing |
| Coder | `allow` | `git-commit` (if tasks require committing code), plus framework-specific skills (TDD, debugging, etc.) |
| Tester | `allow` | `git-commit` (if tasks require committing test files), plus TDD skills |
| Reviewer | `deny` | None — reviewers read and report, never modify state |
| Navigator | `deny` | None — read-only assistance |
| Setup specialist | `allow` | `git-commit` (if tasks require committing configs) |

**Task (delegation) permission**: Only the **coordinator** — which is a `mode: primary` agent, not a subagent — gets `task: allow`. Every *worker* subagent (coder, tester, reviewer, navigator, setup) gets `task: deny`, so **no subagent ever invokes another subagent**. The coordinator is the single point of delegation, and it delegates only to depth-1 workers.

### skills.sh Integration

Subagents can also use skills from the [skills.sh](https://www.skills.sh/) ecosystem. These are reusable instruction packs installed via the `/add-skill` command. When a skill from skills.sh is relevant to a subagent's role (based on the project's tech stack), it should be discovered and installed via dynamic search.

**Discovering skills**: Do NOT rely on static recommendation lists — skills.sh is constantly updated. Instead, search dynamically. **An agent must use the `npx skills find <keyword>` CLI** — it returns the same catalog as the website (with each skill's `skills.sh` link). The `https://www.skills.sh/?q=` URLs below render results in-browser via JavaScript (not machine-readable), so they are for a human to open in a real browser:

1. **Search by language**: `https://www.skills.sh/?q=python`, `?q=rust`, `?q=go`, `?q=typescript`, etc.
2. **Search by framework**: `https://www.skills.sh/?q=react`, `?q=django`, `?q=nextjs`, `?q=fastapi`, etc.
3. **Search by task type**: `https://www.skills.sh/?q=tdd`, `?q=debugging`, `?q=testing`, `?q=verification`, `?q=code-review`, etc.
4. **CLI search** (if available): `npx skills find <keyword>`
5. **Browse by topic**: https://www.skills.sh/topic/testing, https://www.skills.sh/topic/agent-workflows, etc.

**Search keywords by role**:

| Role | Search keyword suggestions |
|------|---------------------------|
| Coder | `<language>`, `<framework>`, `tdd`, `debugging`, `best-practices` |
| Tester | `<language>`, `<test-framework>`, `tdd`, `testing`, `verification` |
| Reviewer | `code-review`, `verification`, `best-practices`, `<language>` |
| Coordinator | `planning`, `workflow`, `subagent`, `task-management` |

**Evaluating skills**: Prefer skills with 1K+ installs, security audit passes, and reputable sources. Read the skill description to verify relevance before installing.

**Installing a skill**: `/add-skill <project> <source> --skill <name> --attach <role>`

**Order of operations**:
1. Create subagents first (via `/add-subagent` or during project setup)
2. Search skills.sh for relevant skills based on the project's tech stack
3. Then install and attach skills (via `/add-skill`)
4. Skills are optional — only install what's relevant to the project's tech stack

### Skill usage per task

The coordinator decides whether a skill is needed on a per-task basis by reading `task-prompt.md` and `design-<task-name>.md`. When a task requires committing code, the coordinator includes "use git-commit skill" in the subtask instructions. When it doesn't, the skill is not mentioned.

## Naming Convention

Use underscore pattern: `<project>_<role>.md`

**Prefer underscores (not hyphens) in the project folder name itself**, so the combined agent id `<project>_<role>` stays unambiguous (e.g., `auth_service_coder`, not `auth-service_coder`). Sample names in the docs that use a hyphen (like `project-x`) are illustrative only.

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
