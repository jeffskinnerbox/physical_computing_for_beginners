# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Course materials for "Physical Computing for Beginners," a Makersmiths hands-on class (1
Pre-Class + 6 Classes) teaching middle/high schoolers physical computing with a Raspberry Pi
Pico 2 W and CircuitPython, building up to an autonomous obstacle-avoiding robot car (the
"Random Rover"). This is a documentation repo, not a software project — there is no build, no
app, no test suite.

## Source of truth and generation order

`input/my-vision.md` is the seed document — course description, 6-class curriculum outline
(objectives, talking points, wiring continuity, planned `class-N-code-*.py` pseudocode), the BOM,
and the map of what documents get generated from it. Everything else in the repo is generated
*from* this file via the skills below, so when the vision changes, downstream docs (syllabus,
lesson plans, BOM, install guides) need to be regenerated/reconciled — don't hand-edit them out of
sync with `my-vision.md` without also reconciling.

`input/my-prompts.md` is a running log of the actual prompts used to generate each artifact
(chronological, "My Nth Prompt" sections) — check it before regenerating something to see the
exact invocation pattern and skill combination that produced the current version. Root-level
`junk.md`/`junk2.md` are stray scratch copies, not canonical — use `input/my-prompts.md` instead.

`input/course-methodology.md` has definitions/background the user reads before working the repo
(class vs. course vs. workshop, external articles on applying coding agents to non-programming
work) — background context, not a generated doc.

`input/spec-kit-methodology.md` is a personal background note comparing the two authoring
methodologies this user applies with Claude Code — Spec-Kit (for software) and a parallel "Script
Methodology" (for course material, where `my-vision.md`, BOM, syllabus, and lesson plans act as
executable contracts). It's context for *how* this repo is meant to be worked, not a generated
doc itself — don't regenerate or reconcile it the way you would syllabus/lesson-plan/BOM content.

Generation pipeline, per `my-vision.md`'s "Course Documentation" table:

| Document | Skill | Output location |
| ---------- | ------- | ------------------ |
| syllabus | `/syllabus_generator` (+ `/grill-me`) | `lesson_plans/syllabus-physical-computing-for-beginners.md` |
| lesson plan | `/lesson_plan_generator` (+ `/theory_of_operation`, `/history_and_application`, `/explainer`) | `lesson_plans/class-0X-lesson-plan.md` |
| install instructions | `/teen-install-instructions` | `tech_setup_check/*.md` |
| theory of operation | `/theory_of_operation` | — |
| explainer | `/explainer` | — |
| bill of materials | `/bill_of_materials_generator` | `lesson_plans/BOM.md` |
| lesson script | none (ad-hoc — see "My 8th Prompt" in `input/my-prompts.md`) | `lesson_scripts/class-NN-lesson-script.md` |

Lesson scripts are student-facing, detailed build+code walkthroughs (not the instructor-facing
lesson plan) — explanatory text plus fully-commented CircuitPython built up in phases, with the
complete final code listed at the end. All seven (`class-00` through `class-06`) exist in
`lesson_scripts/`. Regenerate/reconcile them the same class-at-a-time way as lesson plans.

`my-vision.md`'s Course Documentation table also lists a few document types with no skill built
yet and not present in the repo (build guide, wiring diagrams, code snippets, tested project
code — marked "TBD"). If asked to generate one of these, there is no dedicated skill to invoke;
check `input/my-prompts.md` first for whether an ad-hoc prompt pattern was already used.

Lesson plans must follow the class outline already fixed in the syllabus and flow class-to-class
with minimal repetition — generate/regenerate them one class at a time, stopping for review,
rather than all six at once. All seven (`class-00` Pre-Class through `class-06`) currently exist in
`lesson_plans/`; each embeds its class's `class-N-code-*.py` pseudocode inline as fenced code
blocks rather than as standalone `.py` files — those files are still not present in the repo as
separate artifacts.

## Course structure baked into the content

Six classes plus a Pre-Class, each building hardware/skills on top of the previous one without
rewiring what came before (see "Wiring Continuity" notes per class in `my-vision.md`):
Pre-Class (board bring-up) → Class 1 (button + rotary encoder, debouncing) → Class 2 (HC-SR04
ultrasonic sensor + SG90 servo) → Class 3 (DRV8833 dual H-bridge motor driver) → Class 4 (LSM9DS1
IMU with Mahony filter) → Class 5 (Random Rover: sensor+servo+motor driver combined for collision
avoidance) → Class 6 (finish Rover + stretch goals: encoder speed control, WiFi IMU chart, TFT
status display). GPIO pin assignments are deliberately non-overlapping across classes so old
circuits keep working when new ones are added — preserve that when editing class code or wiring
docs. `class-N-code-*.py` files referenced throughout `my-vision.md` are pseudocode/code
deliverables to be generated per-class (see "My 5th Prompt" in `input/my-prompts.md`), not yet
present in the repo as of this writing.

## Markdown conventions (all generated docs)

Linting/formatting: `npx markdownlint-cli2 "**/*.md"` against the committed `.markdownlint-cli2.jsonc`
(not installed globally). The linter is **not** clean on existing docs — it reports pre-existing,
tolerated warnings (MD013 long lines, MD036 emphasis-as-heading, MD060 table-pipe spacing). Don't
chase zero warnings; just confirm you didn't add *new* ones.

Non-default rules to honor when hand-editing:

- Unordered-list indent is **4 spaces** (`ul-indent`), not 2.
- Long lines allowed (`line-length` = 300).
- Headings: 2 blank lines above, 0 below.
- MD012 (blank lines), MD022, MD024, MD032, MD033 (inline HTML), MD036, MD041, MD045 are all disabled.

Links in generated docs use **reference-style** form (`[text][01]`) with definitions collected at
the bottom of the file, numbered `[01]`, `[02]`, … — no space before the colon, no duplicate URLs,
and never use the raw URL as the link text (write a short descriptive label instead).

Export: `pandoc -f gfm input.md -o output.docx` (or `-o output.pdf` with a PDF engine) — pandoc is
installed.

## Skills available in `.claude/skills/`

`bill_of_materials_generator`, `explainer`, `file-combining`, `grill-me`, `history_and_application`,
`lesson_plan_generator`, `syllabus_generator`, `teen-install-instructions`, `theory_of_operation`,
`wiring-diagram`. These are the primary tools for generating course content — prefer invoking the
matching skill over freehand-writing a new syllabus/lesson-plan/install-guide/BOM section from
scratch. `wiring-diagram` generates a labeled schematic PNG from a "Wiring — <Board> to <Module>"
markdown table and embeds it in the doc.

## Other directories

`communications/` holds course marketing copy and a registration roster containing real students'
names, emails, phone numbers, and addresses — treat `communications/registration.md` as sensitive
PII, not course content; don't quote or propagate it into generated docs or elsewhere.

`expenses/`, `explainers/`, and `handouts/` are new/mostly-empty working directories (as of this
writing `handouts/` has a draft definitions outline, the other two are empty) — no established
conventions yet.
