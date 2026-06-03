---
description: Update an existing outlier.ai project with new PDFs. Usage: /update-project <project-name> <file1.pdf> [file2.pdf ...]
agent: build
---

An existing outlier.ai project needs to be updated with new instruction PDFs. Here are the details:

- **Project name**: $1
- **New watermarked PDF files**: $ARGUMENTS

Execute the following steps in order:

## Step 1: Clean new PDFs

Delegate to the **@pdf-cleaner** subagent with these instructions:
- Project name: $1
- PDF files to clean: all PDF paths provided after the project name
- The project folder `$1/` already exists. Use the `delete-watermarks` tool for each PDF, saving clean versions into the existing `$1/` folder.
- Do NOT delete or modify any existing PDFs in the project folder.

## Step 2: Commit new clean PDFs

After Step 1 completes successfully, delegate to the **@git-committer** subagent with these instructions:
- Commit the new clean PDFs to the main workspace repository
- Use commit message: `chore($1): add cleaned PDFs from update`

## Step 3: Update project AGENTS.md

After Step 2 completes successfully, delegate to the **@project-setup** subagent with these instructions:
- Project folder: $1/
- Read the existing `$1/AGENTS.md` first to understand current rules.
- Then read the newly added clean PDF files in the `$1/` folder.
- Compare the new PDF content with the existing AGENTS.md rules.
- **Merge** the new information into the existing AGENTS.md:
  - Add any new rules, steps, or constraints not already present.
  - Update any rules that have changed or been clarified in the new PDFs.
  - Keep existing rules that are not contradicted by the new PDFs.
  - Do NOT remove existing rules unless the new PDFs explicitly contradict them.
- Preserve the existing AGENTS.md structure and formatting.

## Step 4: Commit updated AGENTS.md

After Step 3 completes successfully, delegate to the **@git-committer** subagent with these instructions:
- Commit the updated `$1/AGENTS.md` to the main workspace repository
- Use commit message: `docs($1): update project rules from new instruction PDFs`
