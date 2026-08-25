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

Use this response style:

- Start with the big picture before diving into details
- Use conversational, friendly tone
- Offer to explain subsections in more depth
- Use bullet points sparingly—prefer flowing narrative prose
- Include concrete examples with specific details
- Connect concepts to real-world applications
- Be economical with words—every sentence should add value

Follow this repo's markdown conventions from `CLAUDE.md`:

- Unordered-list indent is 4 spaces, not 2.
- 1 blank lines above headings, zero below.
- Any URLs use reference-style links (`[text][01]`) with numbered definitions at the bottom —
  never raw/inline URLs.

If a same-name `.bak` backup convention applies (per the user's global instructions), back up an
existing `README.md` to `README.md.bak` before overwriting it.

Link management:
All URLs must use **reference-style markdown links**.
This keeps the document body clean and readable while collecting all URLs in one place at the bottom.

**Rules:**
1. In the document body, use numbered reference tags: `[link text][01]`, `[link text][02]`, etc.
2. Collect all reference definitions at the **very bottom** of the file, after all content sections.
3. Number references sequentially with zero-padded two-digit numbers: `[01]`, `[02]`, `[03]`, ... `[10]`, `[11]`, etc.
4. **No duplicate URLs.** If the same URL is referenced multiple times in the document, reuse the same reference number.
5. Preserve all URLs found in source documents (syllabus, course documents, BOM). Do not drop links.
6. Every reference definition must follow this format with no space before the colon:

   ```text
   [01]:https://example.com/page
   [02]:https://example.com/other-page
   ```

**Example in document body:**

```markdown
Wire the [Pololu QTR-8A Reflectance Sensor Array][01] to the [Raspberry Pi Pico W][02].
Refer to the [SparkFun Line Follower Array Hookup Guide][03] for wiring details.
```

**Example at bottom of file:**

```markdown
[01]:https://www.pololu.com/product/960
[02]:https://www.raspberrypi.com/products/raspberry-pi-pico/
[03]:https://learn.sparkfun.com/tutorials/sparkfun-line-follower-array-hookup-guide
```

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
