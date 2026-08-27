---
name: readme-generator
description: Generate or refresh README.md files. Two modes — whole-project (scan the entire repo, classify project type, generate/update a root README.md plus README.md files for every significant subdirectory, using templates in `.claude/skills/readme_generator/references/`) and single-directory (generate/refresh the README.md for just one named directory). Use whole-project mode when the user asks to "generate READMEs for the whole project," "audit/refresh all the READMEs," or similar repo-wide requests. Use single-directory mode when the user names one specific directory (e.g. "generate a README for explainers/"). Reads CLAUDE.md for project context and treats any existing README.md as a directive for what the new one should cover.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, AskUserQuestion
license: MIT
metadata:
  author: Jeff Irland (Makersmiths)
  version: "0.1.0"
---

# README Generator

Generate or refresh `README.md` files for a project. Two modes:

- **Whole-project mode** — the user asks for READMEs across the whole repo (or doesn't name a
  specific directory). Runs the 4-step pipeline in [Whole-Project Mode](#whole-project-mode)
  below, using subagents and the templates in `.claude/skills/readme_generator/references/`.
- **Single-directory mode** — the user names one specific directory. Runs the lighter flow in
  [Single-Directory Mode](#single-directory-mode) and touches only that directory.

If it's ambiguous which mode is meant, ask before proceeding.

Both modes read the root `CLAUDE.md` first (if present) for the repo's source-of-truth pipeline,
generation order, directory purposes, and markdown conventions — the generated README(s) must fit
that context, not describe the repo/directory in isolation.

Both modes follow this repo's markdown conventions when writing:

- Unordered-list indent is 4 spaces, not 2.
- 2 blank lines above headings, 0 below.
- URLs use reference-style links (`[text][01]`) with numbered definitions at the bottom — never
  raw/inline URLs.

Both modes back up any `README.md` being overwritten to `README.md.bak` first (per the user's
global `.bak` convention), and never write a final file without the user reviewing and approving
it first.


## Whole-Project Mode

### Step 0: Scope check

Confirm the project is in scope for this skill. This skill is for **documentation of a codebase
or course/workshop project** — source code (Bash/C++/Python/ROS2) or class/course/workshop
material. If the target directory doesn't look like any of these (e.g. it's a data dump, a binary
asset archive, an unrelated document collection), **tell the user why it's out of scope and stop.
Don't generate speculative READMEs for a project type this skill doesn't cover.**

### Step 1: Survey subagent — classify and plan

Launch a subagent (`Agent`, `general-purpose`) to scan the **entire** directory structure (respect
`.gitignore`; skip `.git/`, `node_modules/`, build artifacts, and similar noise) and report:

1. **Project type** — one of: Bash code, C/C++ code, Python code, ROS2 code, or Class / Course /
   Workshop, per this mapping:

   | Project Type | Root Template | Sub-Dir Template |
   | :------------- | :------------------- | :---------------------- |
   | Bash code | `.claude/skills/readme_generator/references/README-coding-template.md` | `.claude/skills/readme_generator/references/README-subdir-template.md` |
   | C/C++ code | `.claude/skills/readme_generator/references/README-coding-template.md` | `.claude/skills/readme_generator/references/README-subdir-template.md` |
   | Python code | `.claude/skills/readme_generator/references/README-coding-template.md` | `.claude/skills/readme_generator/references/README-subdir-template.md` |
   | ROS2 code | `.claude/skills/readme_generator/references/README-ros2-template.md` | `.claude/skills/readme_generator/references/README-subdir-template.md` |
   | Class / Course / Workshop | `.claude/skills/readme_generator/references/README-class-template.md` | `.claude/skills/readme_generator/references/README-subdir-template.md` |

   If multiple types are present, the subagent determines the **predominant** type for the root
   README's template — but flags any relatively isolated subtree dominated by a *different* type
   (e.g. a `scripts/` folder of Bash utilities inside a mostly-Python project) so that subtree's
   README can lean on the other template instead in Step 3.

   If no type fits (or the mix is too even to call a predominant type), the subagent reports this
   explicitly rather than forcing a guess.

2. **Where README.md files are needed.** A directory needs one only if it has **more than two
   files** in it (not counting an existing `README.md`/`README.md.bak` itself). Subdirectories
   with two or fewer files are skipped — don't create noise READMEs for near-empty folders.

3. **For each directory needing one**: which template applies (root vs. sub-dir; and which
   project-type template for the root), and whether a `README.md` already exists there (existing
   content becomes a content directive in Step 2/3, per the single-directory flow's Step 3 rule).

**After Step 1**, present the classification and the planned README list/templates to the user:

- If a template was identified for every planned README: state which templates will be used and
  ask for approval before continuing. If the user doesn't approve, ask what to do instead.
- If a template could not be identified for the project (or part of it): explain why, and ask the
  user for guidance (e.g. a different template to add, or a bespoke structure) before continuing.

Do not proceed to Step 2 without this approval/guidance.

### Step 2: Root README subagent

Launch a subagent to scan the whole directory structure again and write the **root** `README.md`,
using the approved root template as structure and the project's actual content to fill it in. The
root README may reference subdirectory README.md files (or summarize their contents) but must
**not duplicate** subdirectory README content in full.

Back up any existing root `README.md` to `README.md.bak` first.

### Step 3: Sub-directory README subagent(s)

After Step 2 completes, launch a subagent that reads the finished root README, then creates/
updates the planned sub-directory README.md files **in descending order** (root's immediate
children first, then their children, etc.), using `.claude/skills/readme_generator/references/README-subdir-template.md` (or the
flagged alternate project-type template for an isolated subtree per Step 1).

Every sub-directory README must be **consistent with** the root README (same project framing,
same terminology) and may complement/expand on it — not contradict it. Add cross-references
between README.md files in the hierarchy where useful (e.g. a subdir README linking back to the
root, or to a sibling it depends on).

Back up any existing subdirectory `README.md` to `README.md.bak` first, per file.

### Step 4: Review subagent — checklist pass/fail

After Step 3 completes, launch a subagent to read **every** README.md written/updated in Steps 2–3
and score it against this checklist:

- Identity & Purpose
  - Title + one-line description of what the project/directory does
  - Badges (build status, version, license) — optional but present if CI exists
- Getting Started
  - Prerequisites/dependencies listed
  - Installation steps that are copy-pasteable
  - Minimal working example ("hello world" usage)
  - Quickstart runs without external context (no tribal knowledge assumed)
- Usage & API
  - Common use cases documented beyond the minimal example
  - Configuration options explained (if any)
  - Link to fuller docs if usage is complex
- Project Health
  - License file referenced/present
  - Contributing guide linked (or inlined) if external contributions expected
  - Contact/support channel (issues, discussions, email)
  - Status indicator (active/maintained/archived/experimental)
- Structural Correctness
  - All internal links resolve (no 404s)
  - Code blocks have correct syntax highlighting and actually run
  - Images/diagrams render (no broken paths)
  - No stale info (references to deprecated commands, old version numbers)
- Readability
  - Logical heading hierarchy (no skipped levels)
  - No walls of text — scannable with headers/bullets
  - Consistent formatting/style throughout

Not every item applies to every project (e.g. a documentation-only course repo has no CI badges,
no license file, no "code blocks that run"). The reviewer should mark inapplicable items N/A
rather than fail, and only fail items that genuinely apply and are missing/wrong.

**If any applicable item fails:** go back to Step 2 (regenerate root, then re-cascade Step 3) and
re-run Step 4. **Loop at most 5 times.** If still failing after 5 loops, stop, report the
remaining failures to the user, and ask how to proceed rather than looping indefinitely.

**If everything passes (or is N/A):** present the full set of generated/updated README.md files to
the user for review and approval before considering the task done. Use `grill-me` if there are
open ambiguities the checklist pass surfaced but couldn't resolve on its own.

### Step 5: Lint

Run `npx markdownlint-cli2 "**/*.md"` against the repo's `.markdownlint-cli2.jsonc`. Fix any *new*
warnings introduced by the generated/updated files. Per `CLAUDE.md`, pre-existing warning classes
(MD013, MD036, MD060, etc.) are tolerated repo-wide — don't chase those to zero.


## Single-Directory Mode

Generate a `README.md` for one directory the user names — never the whole repo, and never
directories the user didn't ask about.

### Step 1: Read CLAUDE.md for context

Read the root `CLAUDE.md` first. It defines the repo's source-of-truth pipeline, generation
order, directory purposes, and markdown conventions. The generated README must fit that context
(what generates what, where the directory sits in the pipeline) rather than describing the
directory in isolation.

### Step 2: Scope to the specified directory only

Confirm which directory the user means. If it's ambiguous (e.g. multiple similarly-named
directories, or no directory named at all), ask before proceeding rather than guessing.

Read the contents of that directory:

- List every file and subdirectory in it (non-recursive is usually enough; go one level into
    subdirectories if the top level is mostly folders).
- Read each file's content (or enough of it — headings, intro paragraph) to summarize its
    purpose accurately. Don't guess a file's purpose from its name alone.
- Check whether a `README.md` already exists in the directory.

If the directory has two or fewer files (and no existing README to refresh), tell the user a
README isn't warranted for a folder this small and ask whether they want one anyway.

### Step 3: Determine the content plan

**If a `README.md` already exists in the directory:** treat its current content as a directive/
outline for what the new README should cover — not boilerplate to discard. Preserve any
section headers, "Future Topics" style lists, or notes the existing file already establishes,
and fill them in / update them from the actual directory contents. If the existing README lists
planned-but-not-yet-created files (like `explainers/README.md`'s "Future Explainers Topics"),
reconcile that list against what now actually exists in the directory — move completed items out
of the "future" list.

**If no `README.md` exists:** classify the directory against the project-type table in
[Whole-Project Mode / Step 1](#step-1-survey-subagent--classify-and-plan) and use
`.claude/skills/readme_generator/references/README-subdir-template.md` as the base structure (this directory is, by definition, a
sub-directory of the project — even in single-directory mode, don't use a root template here).

### Step 4: Grill me before writing

Before writing the file, invoke the `grill-me` skill to resolve ambiguities — e.g. how deep to
summarize subdirectories, whether stale/planned-but-missing entries should be dropped or kept,
whether a table row is needed for files like `.bak` backups or lint configs. Do not write the
README until that back-and-forth is resolved (or the user's answers are exhausted, per grill-me's
own skip-and-assume rule).

### Step 5: Write the file

Follow the markdown conventions at the top of this document. If a same-name `.bak` backup
convention applies, back up an existing `README.md` to `README.md.bak` before overwriting it.

### Step 6: Lint and correct

Run `npx markdownlint-cli2 "<directory>/README.md"` against the repo's `.markdownlint-cli2.jsonc`.
Fix any *new* warnings the generated file introduces. Per `CLAUDE.md`, the repo tolerates
pre-existing warning classes (MD013 long lines, MD036 emphasis-as-heading, MD060 table-pipe
spacing) — don't chase those to zero, just make sure the new file doesn't add other, unrelated
lint failures.


## Critical Rules

- **NEVER** generate READMEs for directories out of scope for this skill (Step 0) — tell the user
    why and stop.
- **NEVER** create a README for a directory with two or fewer files, unless the user explicitly
    asks for one anyway.
- **NEVER**, in single-directory mode, touch any directory the user didn't name.
- **ALWAYS** read `CLAUDE.md` before drafting — every README must be consistent with the
    project's documented structure and conventions.
- **ALWAYS** treat an existing `README.md` as a directive for content, not something to overwrite
    blindly.
- **ALWAYS** get the user's approval of the template plan (whole-project Step 1) or resolve
    ambiguity via `grill-me` (single-directory Step 4) before writing.
- **ALWAYS** back up an overwritten `README.md` to `README.md.bak` first.
- **ALWAYS** get the user's review/approval of the finished README(s) before considering the task
    done.
- **ALWAYS** lint the finished file(s) and fix newly introduced warnings.
- In whole-project mode, **NEVER** loop the Step 2→4 regeneration cycle more than 5 times — stop
    and ask the user if the checklist still isn't passing after 5 loops.
