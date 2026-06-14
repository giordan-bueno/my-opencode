# Model Strategy Reference

## Tier Routing Matrix

Subagents use models from 4 tiers. The `model:` field in frontmatter is the primary; swap to a fallback manually if the primary is unavailable (rate-limited, down, etc.).

| Tier | Primary | Fallback 1 (Go) | Fallback 2 (Zen Free) | Use For |
|------|---------|------------------|-----------------------|---------|
| **Fast** | `opencode-go/deepseek-v4-flash` | — | `opencode/deepseek-v4-flash-free` | Routing, state checks, git, PDF processing |
| **Balanced** | `opencode-go/qwen3.7-plus` | `opencode-go/minimax-m3` | — | Tool calling, coordination, schema generation |
| **Coding** | `opencode-go/kimi-k2.6` | `opencode-go/qwen3.7-max` | — | Refactoring, debugging, multi-file code generation |
| **Reasoning** | `opencode-go/glm-5.1` | `opencode-go/mimo-v2.5-pro` | `opencode/mimo-v2.5-free` | Architectural planning, verification, complex analysis |

## Model Details

### Fast Tier

**Primary: `opencode-go/deepseek-v4-flash`** — The fastest, lowest-overhead model. Infinite runway for micro-tasks and state checks. Essential for high-frequency operations that don't require deep reasoning.

**Fallback: `opencode/deepseek-v4-flash-free`** (Zen free tier) — Identical architecture to the Go version but subject to global traffic concurrency limits. Requires `/connect` setup for the `opencode` provider. Use when Go credits are throttled.

### Balanced Tier

**Primary: `opencode-go/qwen3.7-plus`** — Highest performance-to-quota ratio for agentic pipelines. Natively understands complex tool environments and interacts flawlessly with repository file trees. Masterful at function calling, tool interaction, and structure enforcement.

**Fallback: `opencode-go/minimax-m3`** — Exceptionally reliable at producing strict JSON structures and schema-bound tool outputs. Steps in when Qwen quota is consumed, ensuring your agent won't break mid-task.

### Coding Tier

**Primary: `opencode-go/kimi-k2.6`** — Surgical precision for codebases, repository indexing, and multi-file refactoring. Outperforms the rest of the stack when managing cross-dependencies within a repository, minimizing the code hallucinations that frequently stall automated development agents.

**Fallback: `opencode-go/qwen3.7-max`** — Flagship-grade code understanding and tool orchestration. Steps in when Kimi's premium quota is exhausted, bringing elite-level coding logic as a substitute.

### Reasoning Tier

**Primary: `opencode-go/glm-5.1`** — The definitive logic flagship. Unmatched deep reasoning and abstract planning. Should be explicitly reserved for the initial "Plan" and final "Verify" phases of the agent's execution cycle. Has the most restrictive quota in the Go tier.

**Fallback 1: `opencode-go/mimo-v2.5-pro`** — Deep multi-step agent execution with long-context reasoning. Reliable backup for complex analysis when GLM-5.1 quota is tight.

**Fallback 2: `opencode/mimo-v2.5-free`** (Zen free tier) — Massive 1M token context window. Outstanding for data ingestion and long-context reasoning when other models hit limits. Requires `/connect` setup for the `opencode` provider.

## Subagent Tier Assignments

| Subagent | Tier | Primary | Skills |
|----------|------|---------|-------|
| @pdf-cleaner | Fast | `opencode-go/deepseek-v4-flash` | None |
| @git-committer | Fast | `opencode-go/deepseek-v4-flash` | None |
| @project-setup | Reasoning | `opencode-go/glm-5.1` | None |
| @\<project\>_coordinator | Balanced | `opencode-go/qwen3.7-plus` | Varies per task |
| @\<project\>_coder | Coding | `opencode-go/kimi-k2.6` | Varies per task |
| @\<project\>_tester | Coding | `opencode-go/kimi-k2.6` | Varies per task |
| @\<project\>_reviewer | Reasoning | `opencode-go/glm-5.1` | None |

## Setup for Free Tier Fallbacks

Free tier models use the `opencode` (Zen) provider. To set them up:

1. Run `/connect` in the TUI
2. Select `OpenCode Zen`
3. Sign in at [opencode.ai/auth](https://opencode.ai/auth) and copy your API key
4. Paste the key

Once set up, free models are always available as emergency fallbacks at no cost.

## Changing Models

To swap a subagent's model when the primary is unavailable:

1. Open the subagent's `.md` file in `.opencode/agents/`
2. Change the `model:` line in the frontmatter to the fallback
3. The `# tier:` and `# fallback:` comments document the intended tier and fallback chain

Example — switching project-setup from primary to fallback 1:

```yaml
# Before (primary)
model: opencode-go/glm-5.1
# tier: reasoning
# fallback: opencode-go/mimo-v2.5-pro, opencode/mimo-v2.5-free

# After (fallback 1)
model: opencode-go/mimo-v2.5-pro
# tier: reasoning
# fallback: opencode-go/mimo-v2.5-pro, opencode/mimo-v2.5-free
```