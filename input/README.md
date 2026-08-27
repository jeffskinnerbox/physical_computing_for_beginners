# README

Source documents that everything else in this repo is generated from. `my-vision.md` is the
seed document; the other files are supporting context read alongside it when generating or
regenerating course documentation.


## Usage

This repo has no root `README.md` — see the project's `CLAUDE.md` for the full course
documentation map. `input/my-vision.md` is the single source of truth: the course description,
6-class curriculum outline, BOM, and the generation-pipeline table that maps each document type
to the skill that produces it. When `my-vision.md` changes, downstream docs (syllabus, lesson
plans, lesson scripts, BOM, install guides) need to be regenerated or reconciled against it —
don't hand-edit them out of sync. `my-prompts.md` is a running log of the actual prompts used to
generate each artifact; check it before regenerating something to see the exact invocation
pattern and skill combination that produced the current version. `course-methodology.md` and
`spec-kit-methodology.md` are background reading the user consults before working the repo — not
generated docs, and not inputs to any skill's output.


## Build Process

No build process — this directory holds static markdown source/reference files. A mechanical
backup, `my-vision.md.bak`, sits alongside `my-vision.md` per this user's file-change convention
and isn't itself an authored source.


## Contents

| Topic | File/Directory Name | Description/Summary |
| :------ | :---------- | :------------ |
| Course vision (seed document) | `my-vision.md` | The single source of truth: course description, 6-class curriculum outline (objectives, talking points, wiring continuity, code pseudocode), the BOM, and the Course Documentation table mapping each generated doc to its skill. |
| Prompt history | `my-prompts.md` | Chronological log of the actual Claude Code prompts ("My Nth Prompt" sections) used to generate each artifact in the repo — check before regenerating something to see the exact invocation pattern used. |
| Course-creation background | `course-methodology.md` | Background definitions and reading the user consults before working the repo: class vs. course vs. workshop, and external articles on applying coding agents to non-programming work. |
| Authoring methodology comparison | `spec-kit-methodology.md` | Personal note comparing the two methodologies the user applies with Claude Code — Spec-Kit (software) and the parallel Script Methodology (course material) — as context for how this repo is meant to be worked. |
