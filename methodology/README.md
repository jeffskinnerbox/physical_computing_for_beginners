# README

Background reading, not build material. Three files: class/course/workshop definitions, a
personal note comparing authoring methodologies, and a dated audit of this repo's Claude Code
instruction files. Nothing here is produced by the course-generation skills, and nothing
downstream is generated from it — it's context the user reads before picking up work elsewhere in
the repo.


## Contents

| Topic | File | Description/Summary |
| :------ | :---------- | :------------ |
| Class vs. course vs. workshop | [`course-methodology.md`][01] | Titled "Claude Code Methodology": external articles on applying coding agents to non-programming work, then definitions distinguishing a class, a course, and a workshop, and lecture/seminar/tutorial formats. |
| Authoring methodology comparison | [`spec-kit-methodology.md`][02] | Titled "My Claude Code Methodology": personal note comparing the two methodologies the user applies with Claude Code — Spec-Kit (software) and the parallel Script Methodology (course material, where `my-vision.md`, BOM, syllabus, and lesson plans act as executable contracts) — as context for how this repo is meant to be worked. |
| Prompt audit (2026-10-04) | [`prompt-audit-2026-10-04.md`][03] | Point-in-time audit of the Claude Code instruction files that load in this repo (project `CLAUDE.md`, the skills in `.claude/skills/`, the user's global `CLAUDE.md`), run with `/claude-api prompt-audit`, checking for dated prompting patterns, stale facts, and contradictions between files. Sections: assumptions, summary, findings, flags, how to apply, and a proposed diff. Edits were proposed only, not applied by the audit. |


## Purpose / Role in Repository

The root [README][04] lists this folder as background notes, separate from the generation
pipeline. [`input/my-vision.md`][05] stays the sole seed document for generated course content;
nothing here feeds it. `course-methodology.md` and `spec-kit-methodology.md` used to live in
`input/` and moved here because they're background the user consults, not source material any
skill consumes. The prompt audit is a snapshot of how the repo's Claude Code configuration looked
on 2026-10-04 — read it against the current files, since some of its findings may since have been
fixed.

See [`CLAUDE.md`][06] for how this folder sits alongside `input/` and the generation pipeline.


## Usage

Read these before working the repo; there's nothing to run or build. Don't regenerate or reconcile
them the way you would the syllabus, lesson plans, or BOM — they aren't generated docs.


## Notes

- Editing a file here also writes a matching `.md.bak` backup alongside it; `.bak` files are
    throwaway and gitignored.
- `course-methodology.md` and `spec-kit-methodology.md` use inline links rather than the repo's
    reference-style convention; they're personal notes, not generated docs.
- Related: [`input/`][07] for the seed document and prompt log.


[01]:course-methodology.md
[02]:spec-kit-methodology.md
[03]:prompt-audit-2026-10-04.md
[04]:../README.md
[05]:../input/my-vision.md
[06]:../CLAUDE.md
[07]:../input/README.md
