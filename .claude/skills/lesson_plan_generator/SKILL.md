---
name: lesson-plan-generator
description: Generate detailed class-level lesson plans for a makerspace workshop. Use when an instructor needs a lesson plan, teaching guide, class plan, or class plan for a specific workshop class. Designed for volunteer makerspace instructors, not professional teachers. The generated lesson plan must be consistent with the course syllabus since both reference the same project.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
license: MIT
metadata:
  author: Jeff Irland (Makersmiths)
  version: "0.0.1"
---

# Lesson Plan Generator

Generate detailed, practical lesson plans for individual makerspace workshop Classes.
A lesson plan is the step-by-step teaching guide that tells the instructor exactly how to run
a single class: what to prep, what to say, what to build, how to handle problems, and how to wrap up.
It covers the *how* — the syllabus covers the *what* and *when*.

## Definitions
For shared terminology and type definitions across all the skills in `.claude/skills/`, read `.claude/skills/shared/definitions.md`.

## Curriculum vs Syllabus vs Lesson Plan

These three documents serve different purposes and operate at different levels of detail:

| Document | Scope | Audience | Answers |
| :--------- | :------ | :--------- | :-------- |
| **Curriculum** | All Courses | Program designers | What subjects are taught across the program? |
| **Syllabus** | One Course (all classes) | Students & instructors | What topics, when, what materials, what's expected? |
| **Lesson Plan** | One Design Session | Instructor only | How do I teach this specific Class step-by-step? |

The lesson plan takes the syllabus's Class outline and expands it into a minute-by-minute guide
with instructor notes, prep checklists, troubleshooting tips, and engagement strategies.

**Critical rule:** Lesson plans, syllabus, and bill of materials (BOM) for the same course must be consistent.
The lesson plan's Class number, title, topics, materials, and assessment must match the syllabus exactly.
The BOM is the single source of truth for all cost and sourcing information —
lesson plans must NOT include prices, per-student costs, or purchase links for components.
Reference the BOM for cost details instead.

## Makerspace Context

This skill is designed for **volunteer makerspace instructors**, not professional teachers.
Key implications:

- **Instructors are subject-matter experts, not education experts.**
  They know electronics, coding, and robotics — but may have never written a lesson plan.
  The plan must be concrete enough that a knowledgeable volunteer can pick it up and teach from it.
- **No grades, no quizzes.** Progress is measured through:
  - **Milestone assignments** — completion-based write-ups and demonstrations (no rubrics, no scores)
  - **Competitions** — friendly, multi-attempt, age-bracketed, celebratory
  - **Build journals** — ongoing documentation of the student's design journey
  - **Code walkthroughs** — explaining your code to a peer or on video
- **Hands-on is the default.** Mini-lectures exist to set up the build, not as the main event.
  If students aren't physically building, wiring, coding, or testing within the first 30 minutes,
  the lesson plan needs restructuring.
- **Mixed-age groups (12 through adult).** Every activity must include:
  - A baseline path accessible to the youngest students
  - Challenge extensions for older students and adults
- **Students keep their builds.** Don't design activities that destroy or disassemble previous work.
- **The makerspace provides shared tools** (soldering stations, multimeters, etc.)
  but students need their own laptops and the provided kit.

## When to Use This Skill

Activate when:
- An instructor asks for a "lesson plan," "Class plan," "teaching guide," or "class plan"
- Someone needs detailed Class-by-Class teaching instructions for a workshop
- A syllabus exists but the instructor needs the how-to-teach details for specific Classes
- An existing lesson plan needs to be updated, expanded, or restructured

## How to Generate a Lesson Plan

### Step 1: Read the Syllabus First

**This step is mandatory.** Before generating any lesson plan:

1. **Glob for the syllabus** — look for files like `*syllabus*`, `*course-outline*`, or `*course-schedule*`
2. **Read the syllabus thoroughly** — extract:
   - Class number, title, and phase it belongs to
   - Topics and activities listed for this Class
   - Materials and components needed
   - Any milestone assignments or competitions after this Class
   - The Class flow structure (time breakdown)
   - Age differentiation approach
3. **Read the main course document** — for technical depth, theory of operation details,
   component specifics, and design iteration context
4. **Read the bill of materials** — for accurate component names and to verify coverage
   (costs and sourcing live in the BOM, not the lesson plan)
5. **Check for existing lesson plans** — maintain consistency in format and style across Classes
6. **Collect all URL links** — As you read source documents, collect every URL reference
   (product links, tutorial links, video links, datasheets, etc.). These must be preserved
   in the generated lesson plan. See "Link Management" below for formatting rules.

If no syllabus exists, inform the user and suggest generating one first.
Ask the user if the would like to proceed with creating a Syllabus.
If answer is yes, do so, other wish halt and explain: "A lesson plan without a syllabus risks being inconsistent with the broader course."

### Step 2: Build the Class Plan

Structure the Class using the standard Class flow from the syllabus.
For a typical 2-hour makerspace Class:

| Segment | Duration | Purpose |
| :-------- | :--------: | :-------- |
| Review & Q&A | ~10 min | Revisit previous Class, answer questions, share discoveries |
| Mini-Lecture | ~20 min | New concepts with demos and visual aids |
| Guided Build | ~50-60 min | Hands-on construction, wiring, or coding with instructor support |
| Testing & Documentation | ~20 min | Test builds, record results in build journals |
| Wrap-Up | ~10 min | Summary, preview next Class, optional take-home challenge |

For each segment, provide:
- **What to do** — specific actions, not vague directives
- **What to say** — key talking points, analogies, and questions to ask students
- **What to watch for** — common mistakes, confusion points, safety issues
- **Time check** — when to move on even if not everyone is done

### Step 3: Write Instructor-Specific Content

For each lesson plan, include:

**Preparation Checklist** — Everything the instructor must do *before* students arrive:
- Materials to set out per workstation
- Software to pre-install or verify
- Test tracks to set up
- Spare components to have ready
- Any demos to prepare or test beforehand

**Key Talking Points** — For the mini-lecture, provide:
- 3-5 main concepts to convey
- A physical analogy or demonstration for each concept
- Questions to ask students (to check understanding without quizzing)
- Common misconceptions and how to address them

**Build Guide** — For the guided build, provide:
- Step-by-step instructions the instructor walks students through
- Wiring diagrams or code snippets if applicable
- Checkpoints where students should verify their work before proceeding
- What "done" looks like for this segment

**Troubleshooting Guide** — Common problems and fixes:
- Wiring mistakes (reversed polarity, wrong pins, loose connections)
- Code errors (syntax, logic, library issues)
- Mechanical issues (wheels slipping, sensors too high/low)
- "My robot doesn't work" diagnostic flowchart

**Age Differentiation Notes** — For each major activity:
- **Younger students (12-14):** Simplified instructions, buddy pairing, templates, visual aids
- **Older students (15-18) and adults:** Challenge extensions, deeper explanations, mentoring opportunities

### Step 4: Add Assessment Elements (No Grades)

If the syllabus specifies a milestone assignment or competition after this Class:

**Milestone Assignment:**
- Restate the assignment description from the syllabus
- Provide the instructor with guidance on what "complete" looks like (not a rubric — a description)
- Suggest how to give constructive feedback without scoring
- Note: these are completion-based — the goal is documentation and reflection, not perfection

**Competition:**
- Restate the competition rules from the syllabus
- Provide setup instructions (track layout, timing method, recording results)
- Suggest how to keep it fun and low-pressure (multiple attempts, celebrate improvement, recognize different strengths)
- List award categories

### Step 5: Review for Consistency

Before finalizing, verify:
- [ ] Class number and title match the syllabus exactly
- [ ] Topics covered match the syllabus Class description
- [ ] Materials listed match both the syllabus and the bill of materials (names only, no costs)
- [ ] No cost/pricing information in the lesson plan — costs belong in the BOM only
- [ ] Time allocations fit within the Class duration from the syllabus
- [ ] Assessment method matches the syllabus (competitions and milestones, not quizzes)
- [ ] Technical details (component names, pin numbers, code libraries) are accurate
- [ ] Age differentiation is included for every major activity
- [ ] The lesson plan builds on what was taught in previous Classes (no orphan concepts)
- [ ] All URLs from source documents are preserved in the output
- [ ] All links use reference-style format with `[01]`, `[02]`, etc. at bottom of file
- [ ] No duplicate URLs in the reference list

### Step 6: Export

Export to the requested format:
- **.md** — GitHub-flavored markdown (default). Clean headers, tables, bullet lists.
- **.docx** — Use pandoc: `pandoc -f gfm input.md -o output.docx`
- **.pdf** — Use pandoc with a PDF engine: `pandoc -f gfm input.md -o output.pdf`

## Output Structure

The final lesson plan must contain these sections in this order:

```text
# Lesson Plan: [Class Title]

* Class metadata (number, phase, duration, prerequisites from prior Classes)

## 1. Class Overview
## 2. Learning Goals
## 3. Preparation Checklist
## 4. Materials & Components
## 5. Class Timeline
   ### 5a. Review & Q&A
   ### 5b. Mini-Lecture
   ### 5c. Guided Build
   ### 5d. Testing & Documentation
   ### 5e. Wrap-Up
## 6. Troubleshooting Guide
## 7. Age Differentiation Notes
## 8. Assessment (if applicable)
## 9. Instructor Tips
## 10. Resources & References
```

### Link Management

All URLs referenced in the generated lesson plan must use **reference-style markdown links**.
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

### Section Details

**1. Class Overview** (3-5 sentences)
What this Class accomplishes, where it fits in the course progression,
and what students will have built/learned by the end.

**2. Learning Goals** (3-5 goals)
Concrete, observable outcomes for this specific Class. Not course-wide objectives —
just what students should be able to do after *this* Class.
Use plain language: "Students will wire the sensor array to the Pico W and read sensor values."

**3. Preparation Checklist**
Bulleted list of everything the instructor needs to do before the Class.
Include time estimates (e.g., "Set up soldering stations — 15 min before class").

**4. Materials & Components**
Table listing per-student and shared materials needed for this specific Class.
List component names and quantities only — **do not include prices or purchase links**.
Costs and sourcing belong in the Bill of Materials.
Only list what's actually used this Class, not the full course BOM.

**5. Class Timeline**
The main body of the lesson plan. Each segment gets its own subsection with:
- Duration and time check
- Detailed instructor actions and talking points
- Student activities
- What to watch for (common problems, safety concerns)
- Transition to next segment

**6. Troubleshooting Guide**
Table or list of "Problem → Likely Cause → Fix" entries specific to this Class's activities.

**7. Age Differentiation Notes**
How to modify the Class for younger vs older students. Specific, not generic.
Bad: "Simplify for younger students." Good: "Give 12-14 students the pre-labeled wiring diagram from assets/Class-6-wiring.pdf."

**8. Assessment** (only if syllabus specifies one for this Class)
Milestone assignment details or competition setup instructions.

**9. Instructor Tips**
Practical wisdom: timing advice, common pitfalls, how to recover if things go wrong,
anecdotes or demos that work well, questions that spark good discussions.

**10. Resources & References**
Links to datasheets, tutorials, videos, and reference materials relevant to this Class's topics.
Include both instructor-prep resources and student-facing resources.
All links use reference-style format — the actual URLs go in the reference list at the bottom of the file.

## Best Practices

1. **Syllabus is the source of truth** — the lesson plan implements the syllabus, never contradicts it.
   Read the syllabus before writing any lesson plan.
2. **Write for a knowledgeable volunteer** — the reader knows the technical content but may have
   never taught a class. Tell them what to do, what to say, what to watch for.
3. **Be specific about time** — "Spend about 5 minutes on this" is more useful than
   "Briefly discuss." Include time checks so the instructor knows when to move on.
4. **Anticipate failure modes** — every hands-on activity has things that go wrong.
   Name them and provide fixes. This is the most valuable part of a lesson plan for a new instructor.
5. **The build is the lesson** — mini-lectures set up the build, not the other way around.
   If the lecture takes more than 20 minutes, it's too long.
6. **No grades, no quizzes** — assessment is through building, demonstrating, documenting,
   and competing. If a student built it and it works, they've learned.
7. **Include actual code and wiring** — for Classes involving CircuitPython or wiring,
   include the code snippets and connection details directly in the lesson plan.
   Don't just say "write code to read sensors" — show the code.
8. **Test the timing yourself** — if you estimate 20 minutes for a wiring task,
   double it for first-timers. Hands-on work always takes longer than expected.

## Examples

### Example: Good Class Overview

```markdown
## 1. Class Overview
This is the third Class of Phase 2 (Microcontroller). Students wire the DRV8833
motor driver to the Pico W, write CircuitPython motor control functions, and integrate
sensor data with motor output to create their first microcontroller-based line follower.
By the end, students will have a working robot that follows a line using proportional
steering from the sensor array — a major upgrade from the analog comparator circuit.
```

### Example: Good Learning Goal

```markdown
- Wire the DRV8833 motor driver to the Raspberry Pi Pico W using the provided pin diagram
- Write CircuitPython functions for forward, stop, left turn, right turn, and variable speed
- Integrate sensor array readings with motor control to follow a line
```

### Example: Bad Learning Goal (too academic)

```markdown
- Synthesize knowledge of motor control theory to design actuator interfaces (Bloom's Level 6)
```

### Example: Good Troubleshooting Entry

```markdown
| Problem | Likely Cause | Fix |
|:--------|:-------------|:----|
| One motor doesn't spin | Loose wire on DRV8833 output pin | Check all connections; reseat jumper wires |
| Both motors spin same direction | Motor leads swapped on one side | Swap the two wires on the non-working motor |
| Robot follows line but oscillates wildly | Proportional gain too high | Reduce the steering multiplier in code (try halving it) |
```

### Example: Good Age Differentiation

```markdown
**Younger students (12-14):** Provide the pre-wired breadboard diagram with color-coded wires.
Pair each younger student with an older student for the motor driver wiring.
Use the simplified motor test code (`motor_test_simple.py`) that only does forward/stop.

**Older students (15-18) and adults:** Challenge them to add variable-speed turning
(not just on/off). Have them experiment with different steering multipliers and
document which values give the smoothest line following.
```

## Critical Rules

- **NEVER** generate a lesson plan without first reading the syllabus. The syllabus is the source of truth.
- **NEVER** include prices, per-student costs, or purchase links in the lesson plan — those belong in the BOM
- **NEVER** include grades, rubrics, formal quizzes, multiple-choice tests, or Bloom's taxonomy references
- **NEVER** use education jargon (SMART objectives, scaffolding, differentiated instruction, formative assessment)
  unless the user specifically requests it
- **ALWAYS** include a troubleshooting guide — this is the most valuable section for volunteer instructors
- **ALWAYS** include age differentiation for every major activity
- **ALWAYS** include actual time estimates for every segment and activity
- **ALWAYS** verify that Class number, title, topics, and materials match the syllabus
- **ALWAYS** use reference-style links (`[text][01]`) with definitions at the bottom of the file — never inline URLs
- **ALWAYS** preserve URLs from source documents — do not drop links found in syllabus, course docs, or BOM
- **NEVER** duplicate a URL in the reference list — reuse the same `[NN]` number for repeated references
- **ALWAYS** flag as "[VERIFY]", if technical details are uncertain (pin numbers, library versions, exact code).
