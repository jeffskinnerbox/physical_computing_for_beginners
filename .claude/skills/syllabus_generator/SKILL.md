---
name: syllabus-generator
description: Generate a complete course syllabus for a makerspace workshop. Use when an instructor needs a syllabus, course outline, course schedule, or course map for a hands-on workshop. Designed for volunteer makerspace instructors, not professional teachers. The generated syllabus must be consistent with any existing lesson plans for the same project.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
license: MIT
metadata:
  author: Jeff Irland (Makersmiths)
  version: "0.0.1"
---

# Syllabus Generator

Generate comprehensive, ready-to-publish course syllabus for makerspace workshops.
A syllabus is the high-level course map that tells students what to expect:
topics, schedule, materials, objectives, and how progress is measured.
It covers the *what* and *when* — the lesson plans cover the *how*.

## Definitions
For shared terminology and type definitions across all the skills in `.claude/skills/`, read `.claude/skills/shared/definitions.md`.

## Curriculum vs Syllabus vs Lesson Plan

These three documents serve different purposes and operate at different levels of detail:

| Document | Scope | Audience | Answers |
| :--------- | :------ | :--------- | :-------- |
| **Curriculum** | All Courses | Program designers | What subjects are taught across the program? |
| **Syllabus** | One Course (all classes) | Students & instructors | What topics, when, what materials, what's expected? |
| **Lesson Plan** | One Design Session | Instructor only | How do I teach this specific Design Session step-by-step? |

The syllabus is the bridge: it takes curriculum-level goals and breaks them into a Class-by-Class schedule
that lesson plans then flesh out with detailed teaching instructions.

**Critical rule:** Syllabus, lesson plans, and bill of materials (BOM) for the same course must be consistent.
If a syllabus exists, lesson plans must follow its structure. If lesson plans exist, the syllabus must reflect them.
The BOM is the single source of truth for all cost and sourcing information —
the syllabus must NOT include prices, per-student costs, or purchase links for components.
Reference the BOM for cost details instead.

## Makerspace Context

This skill is designed for **makerspace workshops**, not traditional classrooms. Key differences:

- **Instructors are volunteers** — skilled makers, engineers, hobbyists — not certified teachers.
  They know their subject deeply but may have no formal teaching training.
- **No grades.** Progress is measured by completion of milestone assignments, active participation,
  and periodic friendly competitions.
- **Hands-on first.** Minimize lectures. Students learn by building, testing, breaking, and fixing.
- **Mixed-age groups.** A single Class may have 12-year-olds alongside adults.
  The syllabus must describe how to accommodate this range.
- **Students keep what they build.** Materials budgets matter — the BOM tracks all costs.
- **Self-paced within structure.** Class have a schedule, but students progress at their own speed
  within each phase.

## When to Use This Skill

Activate when:
- An instructor asks for a "syllabus," "course outline," "course schedule," or "course map"
- Someone needs to plan a new makerspace workshop or course
- An existing syllabus needs to be updated or restructured
- A course description is needed for enrollment, marketing, or organizational approval

## How to Generate a Syllabus

### Step 1: Gather Context

Before generating anything, read existing project files to understand the course:

1. **Check for existing course documents** — Glob for `*.md` files in the project directory.
   Read the main course document (e.g., `building-a-line-following-robot.md`) for technical content,
   design iterations, and learning progression.
2. **Check for existing lesson plans** — If lesson plans exist, the syllabus MUST align with their
   Class structure, topics, materials, and assessment methods.
3. **Check for a bill of materials** — Use accurate costs and sourcing info.
4. **Check CLAUDE.md** — for project-specific conventions and context.
5. **Collect all URL links** — As you read source documents, collect every URL reference
   (product links, tutorial links, video links, datasheets, etc.). These must be preserved
   in the generated syllabus. See "Link Management" below for formatting rules.

If no existing documents are found, collect from the user:
- **Topic**: What will students build or learn?
- **Audience**: Age range, skill level, background assumptions
- **Duration**: Number of Class, hours per Class
- **Facility**: What tools/equipment does the makerspace provide?
- **Budget**: Target cost per student (detailed in the BOM, not the syllabus)

If information is missing, make reasonable assumptions, state them explicitly, and proceed.

### Step 2: Define Course Structure

Organize the course into **phases** that group related Classes around milestones.
Each phase should:
- Build on the previous phase's skills
- Conclude with a competition or demonstration
- Be testable — there should be a clear deliverable or observable outcome

Within each phase, define individual **Classes** with:
- A descriptive title (e.g., "Class 5 — Meet the Microcontroller")
- A bullet list of what gets covered (topics, build tasks, concepts)
- Any milestone assignments due

### Step 3: Write the Syllabus Sections

Generate each section below. Every section is required unless marked optional.

### Step 4: Review for Consistency

Before finalizing, verify:
- [ ] Every Class mentioned in "Lessons Breakdown" appears in the "Course Schedule" and vice versa
- [ ] Materials listed in "Technology Requirements" match what's actually used in "Lessons Breakdown"
- [ ] Prerequisites match what the course actually demands (don't require skills that are taught in Class 1)
- [ ] Assessment methods are consistent (competitions and milestones, not quizzes and grades)
- [ ] If lesson plans exist, the syllabus Class topics, numbering, and materials match exactly
- [ ] No cost/pricing information in the syllabus — costs belong in the BOM only
- [ ] Component names match the BOM exactly
- [ ] All URLs from source documents are preserved in the output
- [ ] All links use reference-style format with `[01]`, `[02]`, etc. at bottom of file
- [ ] No duplicate URLs in the reference list

### Step 5: Export

Export to the requested format:
- **.md** — GitHub-flavored markdown (default). Clean headers, tables, bullet lists.
- **.docx** — Use pandoc: `pandoc -f gfm input.md -o output.docx`
- **.pdf** — Use pandoc with a PDF engine: `pandoc -f gfm input.md -o output.pdf`

## Document Output Structure

The final syllabus must contain these sections in this order:

```text
# Course Syllabus: [Course Title]

* Organization / Format / Audience metadata

## 1. Course Description
## 2. Learning Objectives
## 3. Prerequisites
## 4. Technology Requirements
## 5. Course Structure & Format
## 6. Lessons Breakdown
## 7. Recommended & Supplemental Studies
## 8. Assignment Descriptions
```

### Document Section Details

**1. Course Description** (5-20 sentences)
Extended description of the course scope, content, progression, and philosophy.
Mention: what students build, the iterative design approach, hands-on emphasis,
that students keep their materials, and how assessment works (no grades, competitions or demonstration instead).

**2. Learning Objectives**
Group by category (e.g., Hardware & Electronics, Programming, Robotics Concepts, Design & Problem-Solving).
Use concrete, observable outcomes: "Students will be able to [do X]" — not vague goals like "understand robotics."
Keep language accessible; avoid education jargon.

**3. Prerequisites**
Three subsections:
- **Required** — age, math level, attendance commitment
- **Recommended but Not Required** — prior experience that helps but isn't assumed
- **Provided by the Course** — what the course teaches from scratch (so students don't self-select out)

**4. Technology Requirements**
List what hardware, software, and tools are used in the course — but **do not include prices,
per-student costs, or purchase links**. That information belongs in the Bill of Materials.
The syllabus names the components; the BOM prices and sources them.
- **Hardware Per Student** — list component names (no costs or purchase links)
- **Shared Tools** — provided by the makerspace (soldering stations, multimeters, etc.)
- **Software** — all free; list with download/install links
- **Student Computer Requirements** — OS, USB port, internet
- Include a note directing readers to the BOM for costs, quantities, and sourcing

#### 5. Course Structure & Format
- **Class Flow** — table showing the standard time breakdown for each Class
  (e.g., Review & Q&A, Mini-Lecture, Guided Build, Testing & Documentation, Wrap-Up)
- **Course Phases** — table mapping phases to Classes, focus areas, and design iterations
- **Pacing & Age Differentiation** — how the mixed-age classroom is handled
  (templates for younger students, challenge extensions for older ones, buddy pairing)

**6. Lessons Breakdown**
Organized by phase, then by Class. Each Class entry includes:
- Class number and title
- Bullet list of topics, build tasks, and concepts covered
- Any milestone assignment due after this Class
- Competition details (if this Class concludes a phase)

**7. Recommended & Supplemental Studies**
Curated links and resources organized by type:
Videos, Websites, YouTube Channels, Books (optional), Tools.
Every link should be directly relevant to the course content. No filler.
All links use reference-style format — the actual URLs go in the reference list at the bottom of the file.

#### 8. Assignment Descriptions
- **Ongoing Assignments** — build journal, code repository
- **Milestone Assignments** — completion-based (no grades), one per phase or major Class
  Describe format, length, and what to cover. Focus on documentation and reflection.
- **Competitions** — table listing each competition, when it occurs, and the challenge.
  Include rules: age brackets, multiple attempts, award categories, no elimination.

### Link Management

All URLs referenced in the generated syllabus must use **reference-style markdown links**.
This keeps the document body clean and readable while collecting all URLs in one place at the bottom.

**Rules:**
1. In the document body, use numbered reference tags: `[link text][01]`, `[link text][02]`, etc.
2. Collect all reference definitions at the **very bottom** of the file, after all content sections.
3. Number references sequentially with zero-padded two-digit numbers: `[01]`, `[02]`, `[03]`, ... `[10]`, `[11]`, etc.
4. **No duplicate URLs.** If the same URL is referenced multiple times in the document, reuse the same reference number.
5. Preserve all URLs found in source documents (course documents, BOM, lesson plans). Do not drop links.
6. Every reference definition must follow this format with no space before the colon:

   ```text
   [01]:https://example.com/page
   [02]:https://example.com/other-page
   ```

**Example in document body:**

```markdown
Using the [MiOYOOW Line Following Robot Car Kit][01], the student will build the robot.
Install [CircuitPython][02] and [Thonny][03] on student laptops.
```

**Example at bottom of file:**

```markdown
[01]:https://www.amazon.com/WHDTS-Soldering-Electronics-Following-Competition/dp/B07ZH4XLQ3?th=1
[02]:https://circuitpython.org/
[03]:https://thonny.org/
```

## Best Practices

1. **Consistency first** — if lesson plans exist, the syllabus must match them exactly in Class numbering,
   topics, and materials. Read lesson plans before generating.
2. **Makerspace voice** — write for volunteer instructors and motivated students, not for academic review boards.
   Keep language direct and practical. Avoid jargon like "pedagogical frameworks" or "learning taxonomies."
3. **Specificity over generality** — name actual components (Raspberry Pi Pico W, not "a microcontroller"),
   actual software (CircuitPython, not "a programming language").
4. **Realistic scope** — each Class is ~2 hours. Don't cram too much into one Class.
   A hands-on build always takes longer than you think.
5. **Costs live in the BOM** — the syllabus names components but never prices them.
   Direct readers to the Bill of Materials for costs, quantities, sourcing, and budget totals.
6. **Age differentiation** — every Class should work for the full age range.
   Describe how younger and older students experience the same content differently.
7. **Iterative design** — the course itself models iterative design. Make this explicit in the structure:
   identify problems with previous design, propose improvements, implement, test, document.
8. **Assessment without grades** — competitions, milestone assignments, build journals, and peer demonstrations.
   Never mention grades, GPAs, rubrics, or formal quizzes.

## Examples

### Example: Good Syllabus Class Entry

```markdown
**Class 4 — Upgrade to IR Sensors**
- Why LDRs struggle: ambient light dependency, slow response, limited contrast detection
- Introduction to TCRT5000 IR emitter/phototransistor modules: how they work, why they're better
- Replace LDRs with TCRT5000 modules — wiring, calibration, and testing
- Comparative testing: run both sensor types under 3 lighting conditions, document results
- **Milestone Assignment:** Sensor Comparison Study (LDR vs IR)
```

### Example: Good Learning Objective

```markdown
- Compare sensor technologies (LDR vs IR emitter/phototransistor) and select appropriate sensors for a task
```

### Example: Bad Learning Objective (too vague/academic)

```markdown
- Demonstrate comprehension of sensor modalities and their application domains (Bloom's Level 2)
```

### Example: Good Competition Entry

```markdown
> **Competition #1: Consistency Challenge**
> Most consistent lap times across varying lighting conditions.
> Age brackets: 12-14, 15-18, Adults. Multiple attempts allowed.
```

## Critical Rules

- **NEVER** include grades, rubrics, GPA calculations, or formal quizzes
- **NEVER** use academic jargon (Bloom's taxonomy, SMART objectives, scaffolding, differentiated instruction)
  unless the user specifically requests it
- **ALWAYS** read existing project files before generating — don't start from scratch if context exists
- **NEVER** include prices, per-student costs, or purchase links in the syllabus — those belong in the BOM
- **ALWAYS** verify consistency with lesson plans and BOM if they exist
- **ALWAYS** use reference-style links (`[text][01]`) with definitions at the bottom of the file — never inline URLs
- **ALWAYS** preserve URLs from source documents — do not drop links found in course docs, BOM, or lesson plans
- **NEVER** duplicate a URL in the reference list — reuse the same `[NN]` number for repeated references
- If unsure about technical details, flag them as "[VERIFY]" rather than guessing
