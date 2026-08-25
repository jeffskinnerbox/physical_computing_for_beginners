---
name: readme-generator
description: Generate or refresh a README.md for one specific directory in this repo. Use when the user asks for a README, directory overview, or folder summary for a named directory (e.g. "generate a README for explainers/", "add a README to handouts"). Reads CLAUDE.md for project context and, if a README.md already exists in the target directory, treats it as a directive for what the new one should cover.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
license: MIT
metadata:
  author: Jeff Irland (Makersmiths)
  version: "0.0.1"
---

# README Generator

Generate a `README.md` for one directory the user names — never the whole repo, and never
directories the user didn't ask about.

## Step 1: Read CLAUDE.md for context

Read the root `CLAUDE.md` first. It defines the repo's source-of-truth pipeline, generation
order, directory purposes, and markdown conventions. The generated README must fit that context
(what generates what, where the directory sits in the pipeline) rather than describing the
directory in isolation.

## Step 2: Scope to the specified directory only

Confirm which directory the user means. If it's ambiguous (e.g. multiple similarly-named
directories, or no directory named at all), ask before proceeding rather than guessing.

Read the contents of that directory:

- List every file and subdirectory in it (non-recursive is usually enough; go one level into
  subdirectories if the top level is mostly folders).
- Read each file's content (or enough of it — headings, intro paragraph) to summarize its
  purpose accurately. Don't guess a file's purpose from its name alone.
- Check whether a `README.md` already exists in the directory.

## Step 3: Determine the content plan

**If a `README.md` already exists in the directory:** treat its current content as a directive/
outline for what the new README should cover — not boilerplate to discard. Preserve any
section headers, "Future Topics" style lists, or notes the existing file already establishes,
and fill them in / update them from the actual directory contents. If the existing README lists
planned-but-not-yet-created files (like `explainers/README.md`'s "Future Explainers Topics"),
reconcile that list against what now actually exists in the directory — move completed items out
of the "future" list.

**If no `README.md` exists:** use this exact section structure:

```markdown
# README
{Purpose of this specific folder/module}

## Usage
{How it fits into the larger project (often linking back to root README)}

## Build Process
{Local build/test instructions if they differ from root}

## Contents
{summaries the directory using a table like this}

| Topic | File/Diectory Name | Description/Summary |
|:------|:----------|:------------|
```

- Each row of the Contents table gets one file or subdirectory. The **Description/Summary**
  column must be no more than 50 words.
- If the directory has no meaningful local build/test process (true for most directories in this
  documentation-only repo — see `CLAUDE.md`), say so plainly in **Build Process** rather than
  inventing steps (e.g. "No build process — this directory holds static markdown/reference
  files.").
- If a root `README.md` exists, link back to it under **Usage**; if it doesn't, describe how this
  directory fits into the repo per `CLAUDE.md` instead of inventing a link.

## Step 4: Grill me before writing

Before writing the file, invoke the `grill-me` skill to resolve ambiguities — e.g. how deep to
summarize subdirectories, whether stale/planned-but-missing entries should be dropped or kept,
whether a table row is needed for files like `.bak` backups or lint configs. Do not write the
README until that back-and-forth is resolved (or the user's answers are exhausted, per grill-me's
own skip-and-assume rule).

## Step 5: Write the file

Follow this repo's markdown conventions from `CLAUDE.md`:

- Unordered-list indent is 4 spaces, not 2.
- 2 blank lines above headings, 0 below.
- Any URLs use reference-style links (`[text][01]`) with numbered definitions at the bottom —
  never raw/inline URLs.

If a same-name `.bak` backup convention applies (per the user's global instructions), back up an
existing `README.md` to `README.md.bak` before overwriting it.

## Step 6: Lint and correct

Run `npx markdownlint-cli2 "<directory>/README.md"` against the repo's `.markdownlint-cli2.jsonc`.
Fix any *new* warnings the generated file introduces. Per `CLAUDE.md`, the repo tolerates
pre-existing warning classes (MD013 long lines, MD036 emphasis-as-heading, MD060 table-pipe
spacing) — don't chase those to zero, just make sure the new file doesn't add other, unrelated
lint failures.

## Critical Rules

- **NEVER** generate a README for a directory the user didn't specify.
- **ALWAYS** read `CLAUDE.md` before drafting — the README must be consistent with the project's
  documented structure and conventions.
- **ALWAYS** treat an existing `README.md` in the target directory as a directive for content,
  not something to overwrite blindly.
- **ALWAYS** run `grill-me` before writing the file.
- **ALWAYS** lint the finished file and fix newly introduced warnings.
