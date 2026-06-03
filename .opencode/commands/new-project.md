---
description: Set up a new outlier.ai project from watermarked PDFs. Usage: /new-project <project-name> <file1.pdf> [file2.pdf ...]
agent: build
---

A new outlier.ai project needs to be set up. Here are the details:

- **Project name**: $1
- **Watermarked PDF files**: $ARGUMENTS

Execute the following steps in order:

## Step 1: Clean PDFs and create project folder

Delegate to the **@pdf-cleaner** subagent with these instructions:
- Project name: $1
- PDF files to clean: all PDF paths provided after the project name
- The subagent should use the `delete-watermarks` tool for each PDF, saving clean versions into the `$1/` folder.

## Step 2: Commit new project folder and clean PDFs

After Step 1 completes successfully, delegate to the **@git-committer** subagent with these instructions:
- Commit the new `$1/` folder and clean PDFs to the main workspace repository
- Use commit message: `feat($1): set up new project with cleaned PDFs`

## Step 3: Create project AGENTS.md

After Step 2 completes successfully, delegate to the **@project-setup** subagent with these instructions:
- Project folder: $1/
- Read all clean PDF files inside the `$1/` folder
- Analyze the project rules and create `$1/AGENTS.md`

## Step 4: Commit project AGENTS.md

After Step 3 completes successfully, delegate to the **@git-committer** subagent with these instructions:
- Commit the new `$1/AGENTS.md` to the main workspace repository
- Use commit message: `docs($1): add project rules from instruction PDFs`
