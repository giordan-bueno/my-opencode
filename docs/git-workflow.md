# Git Workflow Reference

## Repository Structure

This workspace uses a **two-repository structure** to separate project management from task execution.

### Main Workspace Repository

**Location**: Root folder (`my-opencode/`)

**Tracks**:
- Project folders and their contents
- Clean (watermark-free) PDFs
- AGENTS.md files (workspace and project-level)
- PROGRESS.md files (task progress tracking)
- Subtask templates and reference docs (docs/ folders)
- Workspace configuration (`.opencode/`)

**Push destination**: Your own GitHub repository (for backup/sync across PCs)

**Push destination**: Your own GitHub repository (for backup/sync across PCs)

**Ignores**: External repos inside project folders (via `.gitignore`)

### External Project Repositories

**Location**: Inside project folders (e.g., `project-1/external-repo/`)

**Identified by**: Having their own `.git/` folder

**Tracks**: Code changes for outlier.ai tasks

**Push destination**: **Nowhere** (local-only, changes submitted via outlier.ai interface)

**Why local-only**: Changes are submitted through outlier.ai's interface (zip upload, etc.), not pushed to the original GitHub repository.

## How to Detect Which Repository

When committing changes, determine which repository owns the files:

1. **Check current working directory** - where are the changes located?
2. **Look for nested `.git/` folders** - if changed files are inside a directory containing `.git/`, it's an external repo
3. **If no nested `.git/` found** - changes belong to the main workspace repo

### Example Detection

```bash
# Working in project-1/src/
# Check if project-1/ has .git/
ls project-1/.git  # If exists, it's an external repo

# Working in project-1/AGENTS.md
# No nested .git/, so it's the main repo
```

## Commit Rules

### Main Repository Commits

**When to commit**:
- After creating a new project folder with clean PDFs
- After creating or updating a project's AGENTS.md
- After updating workspace configuration

**Commit message format**:
```
<type>(<project-name>): <description>
```

**Common commit types**:
- `feat(project-name)`: New project setup
- `docs(project-name)`: Updated AGENTS.md or project documentation
- `chore(project-name)`: Cleaned PDFs or minor project maintenance

**Example**:
```bash
git add project-1/
git commit -m "feat(project-1): set up new project with cleaned PDFs and AGENTS.md"
```

### External Repository Commits

**When to commit**:
- After implementing features or fixes for outlier.ai tasks
- After refactoring code
- After adding tests

**Commit message format**:
```
<type>(<scope>): <description>
```

**Common commit types**:
- `feat(scope)`: New feature implementation
- `fix(scope)`: Bug fix
- `refactor(scope)`: Code refactoring
- `test(scope)`: Adding/updating tests

**Example**:
```bash
cd project-1/external-repo
git add src/auth.ts
git commit -m "fix(auth): resolve login validation error"
```

## Important Rules

1. **Never push external repo changes** - they're local-only for outlier.ai submission
2. **Always use conventional commits** - follow the format: `<type>(<scope>): <description>`
3. **One logical change per commit** - don't mix unrelated changes
4. **Check git status first** - understand what changed before committing
5. **Never commit secrets** - check for .env, credentials, private keys before staging
6. **Preserve existing commits** - don't amend or rewrite, always create new commits

## Safety Protocol

- **NEVER force push** to any repository
- **NEVER run destructive git commands** without explicit request
- **NEVER skip git hooks** (--no-verify)
- If a commit fails, fix the issue and create a **NEW commit**

## Common Scenarios

### Scenario 1: New Project Setup

```bash
# Changes: project-1/ folder created with clean PDFs and AGENTS.md
# Action: Commit to MAIN repo
git add project-1/
git commit -m "feat(project-1): set up new project with cleaned PDFs and AGENTS.md"
```

### Scenario 2: Working on External Repo Bug Fix

```bash
# Changes: project-1/external-repo/src/bug.ts fixed
# Action: Commit to EXTERNAL repo
cd project-1/external-repo
git add src/bug.ts
git commit -m "fix(auth): resolve login validation error"
```

### Scenario 3: Updated Project Rules

```bash
# Changes: project-1/AGENTS.md updated with new PDF info
# Action: Commit to MAIN repo
git add project-1/AGENTS.md
git commit -m "docs(project-1): update rules from new instruction PDF"
```

### Scenario 4: Multiple Changes in External Repo

```bash
# Changes: Multiple files in project-1/external-repo/
# Action: Group logically, commit to EXTERNAL repo
cd project-1/external-repo

# First logical change
git add src/api.ts src/utils.ts
git commit -m "refactor(api): extract common request handler"

# Second logical change
git add tests/api.test.ts
git commit -m "test(api): add tests for request handler"
```

## The @git-committer Subagent

The **@git-committer** subagent handles commits automatically:

- **Model**: opencode-go/deepseek-v4-flash (fast, low-cost)
- **Detects repository type** based on nested `.git/` folders
- **Uses conventional commits** with appropriate type and scope
- **Commits after major steps** in workflows (PDF cleaning, AGENTS.md creation)

### Manual vs Automatic Commits

**Automatic** (via commands):
- `/new-project` and `/update-project` automatically call @git-committer

**Manual** (when working on tasks):
- Ask the main agent to commit: "commit these changes"
- The main agent will delegate to @git-committer

## Gitignore Configuration

### Root .gitignore

The root `.gitignore` file excludes:
- `node_modules/` - Dependencies
- `package-lock.json`, `skills-lock.json` - Lock files
- OS files - `.DS_Store`, `Thumbs.db`
- IDE files - `.vscode/`, `.idea/`
- Environment files - `.env`, `.env.local`

### Per-Project .gitignore

Each project folder has its own `.gitignore` that uses a whitelist pattern:

```gitignore
# Ignore everything by default
*

# But track these specific files/folders
!.gitignore
!AGENTS.md
!PROGRESS.md
!progress-*.md
!docs/
!docs/**
!*.pdf
```

This ensures:
- Task folders (with external repos) are automatically ignored regardless of naming
- Only explicitly tracked files are committed
- No need to manually add task folders to gitignore

**Important**: The `.gitignore` is created by @pdf-cleaner during project setup (Step 1) before any commits, ensuring git tracking works correctly from the start.

### Adding External Repos to Gitignore

When you clone an external repo into a project folder, add it to `.gitignore`:

```bash
# Example: project-1/my-external-repo/
echo "project-1/my-external-repo/" >> .gitignore
git add .gitignore
git commit -m "chore: add project-1/my-external-repo to gitignore"
```

This ensures the main repo doesn't track the external repo's files.
