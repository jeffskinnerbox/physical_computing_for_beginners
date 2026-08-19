---
name: file-combiner
description: Combine multiple files (typically Markdown) into fewer files by identifying and merging common themes. Use when user asks to consolidate, merge, combine, or reduce a set of files. Never overwrites originals — always creates new files.
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion
---

# File Combiner

Consolidates multiple files into fewer thematically-organized files by identifying recurring topics and merging related content. Always creates new files; never overwrites originals.

## When to Use

- "Combine these files into one"
- "Merge these documents by topic"
- "Consolidate these files"
- "Reduce the number of files by combining similar content"
- User provides a set of files with overlapping or related content

## Instructions

### Step 1: Gather Owner Requirements

Before reading any files, ask the user:

1. **Predefined themes**: "Do you have specific themes you want the output organized around? If so, list them."
2. **Theme exclusivity**: "Are these the only themes to use, or can I propose additional themes if the content warrants them?"
3. **Audience**: "Who is the intended audience for the output documents? (e.g., technical team, executives, general public, students) This will shape tone, depth, and structure."

Record all answers — they constrain every subsequent step.

### Step 2: Read and Analyze All Files

1. Read every input file in full.
2. For each file, extract:
   - Recurring topics, terms, activities, and symbols
   - Central ideas or lessons
   - Key vocabulary clusters
3. Summarize each file's theme as a single sentence: a universal lesson or recurring concept.
4. Identify and catalog all **references** in each file:
   - Inline citations, footnotes, hyperlinks, and bibliography entries
   - Bulleted or grouped reference lists — treat each contiguous group as an atomic unit (do not split a grouped list across files)

### Step 3: Identify and Consolidate Themes

1. Start with any predefined themes the user provided.
2. If the user allows additional themes, identify them from the content and add to the list.
3. If the user said predefined themes are the only ones allowed, only use those — do not add new ones.
4. Group all content under the final theme list by similarity.
5. Continue merging until the number of theme groups is **≤ the number of input files**.
6. Aim for the fewest possible groups (ideally one), without forcing unrelated content together.
7. For each final theme group, write:
   - A short theme title (3–6 words)
   - A one-sentence description of the universal lesson or concept
   - The list of source files contributing to it
8. Track any content that does not fit under any theme — flag it as **leftover content**.

### Step 4: Review Themes with the User

Present the proposed theme groups in a clear table or list:

```
Theme: <Title>
Description: <One-sentence theme statement>
Sources: <file1.md, file2.md, ...>
```

Ask the user:
- Do these themes look right?
- Any themes to split, merge, rename, or reframe?
- Any content that must stay together or be kept separate?
- Any specific output filenames preferred?

If there is **leftover content** (content that doesn't fit any theme), present it clearly:

```
Leftover content (no matching theme):
- [brief description of content] from <filename>
- ...
```

Ask: "This content doesn't fit any of the proposed themes. Is it OK to leave it out of the new files, or should we find a place for it?"

Do not proceed until the user has approved or redirected all leftover content.

Incorporate all feedback before proceeding.

### Step 5: Create New Output Files

1. For each theme group, create a new Markdown file.
2. Output filename: derive from the theme title (lowercase, hyphens), e.g., `growth-and-resilience.md`.
3. Never use the same filename as any input file.
4. Structure each output file with the audience in mind (tone, depth, assumed knowledge):
   - `# <Theme Title>` as the H1 heading
   - `> <One-sentence theme statement>` as a blockquote summary
   - Sections organized by sub-topic, drawing from all contributing source files
   - Where needed for readability, repeat brief context from other output files rather than leaving gaps
5. Move (copy) content from original files into the new files — do not delete or modify originals.
6. **Preserve all references:**
   - Every reference from every input file must appear in at least one output file.
   - Place each reference in the output file whose theme best matches the referenced material.
   - If a reference is relevant to multiple output files, copy it into each relevant file.
   - Bulleted or otherwise grouped reference lists must be moved **as a complete group** — never split a contiguous reference list across different output files.
   - Collect all references for each output file into a dedicated `## References` section at the end of that file.

### Step 6: Verify Theme Coherence

For each new output file:
1. Re-read the full document.
2. Verify the stated theme is **supported by specific examples distributed throughout the entire document**, not just in one section.
3. If a section contradicts the theme or is unsupported, either:
   - Relocate the section to a more appropriate output file, or
   - Add a bridging sentence explaining the connection
4. Repeat until every output file is internally consistent.
5. Report the final file list and a one-line summary of what each contains.

## Key Principles

- **Never overwrite originals.** All output is written to new files.
- **All references must survive.** Every reference from every input file must appear in at least one output file. Grouped reference lists are atomic — move them whole, never split.
- **Output is always Markdown.** Even if inputs are plain text or other formats.
- **Fewer files is better.** Merge aggressively; only split when content is genuinely incompatible.
- **Repetition for readability is allowed.** Brief repeated context across files is preferable to confusing gaps.
- **Theme = universal lesson.** Identify the *why*, not just the *what*. List recurring ideas, words, and activities to surface the theme.
- **Output count ≤ input count.** Never produce more files than were provided.

## Theme Identification Guide

A strong theme:
- Appears as a recurring pattern (not a one-time mention) across multiple sections or files
- Can be stated as a universal, transferable lesson (e.g., "Consistent small actions compound into lasting change")
- Is supported by specific examples in multiple places throughout the text

Weak theme signals:
- Only appears in one file or one section
- Too narrow or too broad to anchor an entire document
- Cannot be demonstrated with at least 3 distinct examples from the combined text

## Examples

### Example 1: Consolidating journal entries

Input: `jan.md`, `feb.md`, `mar.md` (3 files about personal growth, habits, and reflection)

Themes found:
- Habit formation (recurring in all 3)
- Self-reflection practices (recurring in jan + mar)
- Dealing with setbacks (recurring in feb + mar)

Merged: "Habit formation" + "Dealing with setbacks" → **Resilience through Routine**

Output: 2 files — `resilience-through-routine.md`, `self-reflection-practices.md`

### Example 2: Merging technical notes

Input: `auth-notes.md`, `session-notes.md`, `token-notes.md`

Themes: all relate to identity and access management → merged into 1 file: `identity-and-access-management.md`

## Validation Checklist

Before finishing, confirm:
- [ ] Owner's predefined themes (if any) were collected upfront
- [ ] Theme exclusivity preference (fixed vs. open to additions) was confirmed
- [ ] Audience was identified and influenced document structure/tone
- [ ] All input files were read
- [ ] Theme count ≤ input file count
- [ ] Leftover content was identified and user approved omitting or placing it
- [ ] User reviewed and approved final themes
- [ ] No original files modified
- [ ] Each output file is valid Markdown with H1 heading and theme summary
- [ ] Each theme is verified with examples distributed throughout (not just one section)
- [ ] Output filenames do not collide with input filenames
- [ ] Every reference from every input file appears in at least one output file
- [ ] No grouped reference list was split across output files
- [ ] Each output file has a `## References` section if it contains any references
