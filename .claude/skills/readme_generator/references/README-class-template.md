
# {{Course Title}}

*A Makersmiths hands-on class.*

{{One or two sentence pitch — who this is for, what they build, what skill it teaches.
Example: "A hands-on class for middle/high schoolers teaching physical computing with a
{{board/kit name}}, building up to {{capstone project}}."}}

## Table of Contents
- [Overview](#overview)
- [What You'll Build](#what-youll-build)
- [Course Structure](#course-structure)
- [Getting Started](#getting-started)
- [Repository Layout](#repository-layout)
- [How This Repository Is Generated](#how-this-repository-is-generated)
- [Safety Notes](#safety-notes)
- [Credits and License](#credits-and-license)

## Overview

| | |
| :--- | :---- |
| **Audience** | {{e.g. middle/high schoolers, no prior coding required}} |
| **Format** | {{N Classes + Pre-Class, length per session}} |
| **Capstone project** | {{what gets built by the end}} |
| **Hardware** | {{board + key modules}} |
| **Software** | {{language/IDE, e.g. CircuitPython}} |


## What You'll Build

{{Short narrative of the build arc — what exists after Pre-Class, what gets added each
subsequent class, and what the finished capstone project does. This should match the class-by-
class outline in the syllabus, not duplicate it in full.}}


## Course Structure

{{Table or list of Pre-Class + each class, one line each: what's added, key concept taught. Keep
in sync with the syllabus — this is a summary, not the source of truth.}}

| Class | Focus | New Hardware/Concept |
| --- | --- | --- |
| Pre-Class | {{e.g. board bring-up}} | |
| Class 1 | | |
| Class 2 | | |
| Class 3 | | |
| Class 4 | | |
| Class 5 | | |
| Class 6 | | |

Wiring/pin assignments are chosen so each class's circuit keeps working after later classes add
to it — nothing gets rewired mid-course.


## Getting Started

1. {{Read the install/setup guide: link to tech_setup_check/ or equivalent}}
2. {{Gather materials: link to the BOM}}
3. {{First thing a student does, e.g. flash CircuitPython to the board}}


## Repository Layout

```text
input/            Source-of-truth vision doc + prompt log — everything else is generated from this
lesson_plans/     Instructor-facing syllabus + per-class lesson plans, BOM
lesson_scripts/   Student-facing build+code walkthroughs, one per class
tech_setup_check/ Install/setup instructions per environment
explainers/       Standalone "why does it work that way" deep-dive docs
handouts/         Printable per-class handouts
communications/   Marketing copy, registration info (may contain PII — treat as sensitive)
expenses/         {{purpose}}
```

Adjust this list to match the actual top-level directories in your course repo — don't leave
placeholders that don't exist, and don't hide directories that do.


## How This Repository Is Generated

`{{input/my-vision.md or equivalent}}` is the seed document: course description, class-by-class
outline, bill of materials, and the map of what gets generated from it. Everything else —
syllabus, lesson plans, install guides, BOM — is generated *from* that file via Claude Code
skills, so when the vision changes, regenerate/reconcile the downstream docs rather than hand-
editing them out of sync.

| Document | Skill | Output |
| --- | --- | --- |
| Syllabus | `/syllabus_generator` | `lesson_plans/syllabus-*.md` |
| Lesson Plan | `/lesson_plan_generator` | `lesson_plans/class-0X-lesson-plan.md` |
| Lesson Script | {{ad-hoc/skill name}} | `lesson_scripts/class-NN-lesson-script.md` |
| Install Instructions | `/teen-install-instructions` | `tech_setup_check/*.md` |
| Bill of Materials | `/bill_of_materials_generator` | `lesson_plans/BOM.md` |
| Explainer | `/explainer` | `explainers/*.md` |

See `CLAUDE.md` for the full generation pipeline and conventions (markdown linting, link style,
export via pandoc, etc.) that apply when regenerating any of these.


## Safety Notes

{{Anything instructors/students must know before handling hardware — soldering, battery
handling, power tool use, allergens, etc. Delete this section if not applicable.}}


## Credits and License

{{Author, org (Makersmiths), license if any.}}
