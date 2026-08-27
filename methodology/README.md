# README

This is background reading, not build material. Two files: class/course/workshop definitions,
and a personal note comparing development methodologies. Nothing here is produced by a skill,
and nothing downstream is generated from it, it's context the user reads before picking up work
elsewhere in the repo.


## Usage

Start with the root [README][01] for the full course documentation map, and `CLAUDE.md` for how
this directory sits alongside `input/`. These two files used to live in `input/`; they moved
here because they're background the user consults, not source material any skill consumes.
`input/my-vision.md` stays the sole seed document for generated course content, nothing here
feeds it.


## Build Process

No build process. This directory holds static markdown reference files, nothing compiles or
generates from them. Per this user's file-change convention, editing a file here writes a
matching `.md.bak` backup alongside it.


## Contents

| Topic | File/Directory Name | Description/Summary |
| :------ | :---------- | :------------ |
| Class vs. course vs. workshop | `course-methodology.md` | Definitions distinguishing a class, a course, and a workshop, and lecture/seminar/tutorial formats, plus external articles on applying coding agents to non-programming work. |
| Authoring methodology comparison | `spec-kit-methodology.md` | Personal note comparing the two methodologies the user applies with Claude Code — Spec-Kit (software) and the parallel Script Methodology (course material) — as context for how this repo is meant to be worked. |


[01]:../README.md
