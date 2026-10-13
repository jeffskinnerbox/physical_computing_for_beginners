# README

Everything else in this repo traces back to a file in here. `my-vision.md` is the seed: one
document, everything downstream grows from it. `my-prompts.md` rides along as supporting
context, the log you check when you need to know exactly how something got generated.


## Usage

Start with the root [README][01] for the full course documentation map, and `CLAUDE.md` for the
generation pipeline behind it. `input/my-vision.md` carries the weight here: course description,
the Pre-Class + 6-class curriculum outline, BOM, and the Course Documentation table listing each
document type, its audience, and what it's for (the skill that produces each one is mapped in
`CLAUDE.md`, not here). Change `my-vision.md` and the downstream docs go stale immediately —
syllabus, lesson plans, lesson scripts, BOM, install guides all need to be regenerated or
reconciled against it. Don't hand-edit them out of sync; that's how a syllabus quietly stops
matching the vision it was supposed to come from.

Before regenerating anything, check `my-prompts.md` first. It's a running log of the actual
prompts used to produce each artifact, so it tells you the exact invocation pattern and skill
combination that made the current version, not just what the skill can theoretically do. It's long
(44 numbered prompts so far), so jump to a section with `grep -n "My .* Prompt" my-prompts.md`.
The sections titled "My XXX Prompt" at the end are drafts that haven't been run — they describe
planned skills, not anything that exists in the repo.

Background reading the user consults before touching this repo, class/course/workshop
definitions, methodology comparisons, moved out to [`methodology/`][02]. It's context for how
the work happens, not source material any skill reads.


## Build Process

No build process. This directory is static markdown, source and reference material, nothing
compiles it. Per this user's file-change convention, editing a file here writes a matching
`.md.bak` backup alongside it; `.bak` files are throwaway and gitignored.


## Contents

| Topic | File/Directory Name | Description/Summary |
| :------ | :---------- | :------------ |
| Course vision (seed document) | `my-vision.md` | The single source of truth: course description, Pre-Class + 6-class outline (objectives, talking points, wiring continuity, pseudocode, optional homework list), the BOM, and the Course Documentation table (document, audience, description). |
| Prompt history | `my-prompts.md` | Chronological log of the actual Claude Code prompts ("My Nth Prompt" sections) used to generate each artifact in the repo — check before regenerating something to see the exact invocation pattern used. Ends with unrun "My XXX Prompt" drafts. |

Background definitions and methodology notes previously kept here (`course-methodology.md`,
`spec-kit-methodology.md`) have moved to [`methodology/`][02].


[01]:../README.md
[02]:../methodology/README.md
