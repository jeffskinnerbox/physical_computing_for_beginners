---
name: history-and-application
description: Generate a history and application document for a technology, software program, machine, electronic circuit, or system. Use when someone needs to understand the historical origins, key people, evolution over time, and practical applications of a topic. Each document contains two major sections — History and Application — each with a brief narrative and a detailed bulleted timeline.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
license: MIT
metadata:
  author: Jeff Irland (Makersmiths)
  version: "0.0.1"
---

# History and Application Generator

Generate clear, well-structured documents that trace the historical origins and practical
applications of a technology, software program, machine, electronic circuit, or system.
Each document contains two required major sections — **History** and **Application** — and
each section contains two required subsections: a **brief narrative** (0.25-0.5 pages) and
a **detailed bulleted timeline**.

## Definitions
For shared terminology and type definitions across all the skills in `.claude/skills/`, read `.claude/skills/shared/definitions.md`.

## What Is a History and Application Document?

A history and application document answers two questions about a technology or system:

1. **Where did it come from?** — Who invented it, when, why, and how did it evolve?
2. **Where has it been used?** — What real-world problems has it solved, in what industries,
   and how has its use expanded or changed?

This type of document gives readers context that pure technical documentation cannot.
Understanding *why* a technology exists and *how* it has been applied helps students grasp
its significance and see connections between disciplines. For a robotics workshop, knowing
that PID control started with ship steering in the 1920s, or that line-following robots
date to the 1960s, makes the technology feel less abstract and more human.

### What It Is NOT

A history and application document is **not**:
- A **theory of operation** — how the system works internally
- A **user manual** — how to operate or configure it
- A **build guide** — how to assemble or manufacture it
- A **datasheet** — exhaustive electrical/mechanical specifications
- A **tutorial** — step-by-step learning exercises

It may reference any of these, but its purpose is explaining **where the technology came from**
and **how it has been put to use**.

## When to Use This Skill

Activate when:
- Someone asks for the "history of," "origins of," or "background on" a technology
- Someone asks "where is [X] used?" or "what are the applications of [X]?"
- Workshop materials need contextual background on a component, algorithm, or system
- A lesson plan calls for motivational context — why this technology matters
- Someone asks "who invented [X]?" or "when was [X] developed?"

## How to Generate a History and Application Document

### Step 1: Identify the Subject and Scope

Determine exactly what the document covers. Ask:
- **What is the subject?** A specific component, algorithm, technique, or system?
- **What domain?** Electronics, software, mechanical, control theory, sensors, etc.?
- **How far back does the history go?** Some topics (electricity, optics) have roots
  200+ years ago. Others (microcontrollers, machine learning) are more recent. Go back
  as far as the meaningful precursors — typically up to ~200 years if relevant.

If scope is ambiguous, default to a focused treatment — one technology or technique,
not an entire field.

### Step 2: Research the Subject

Before writing:

1. **Search for authoritative sources** — academic histories, IEEE milestones, inventor
   biographies, patent records, manufacturer histories, museum archives, and reputable
   engineering references.
2. **Identify the key people** — inventors, engineers, researchers, companies. Get names,
   dates, and contributions right.
3. **Map the evolutionary timeline** — trace the path from earliest precursor to modern form.
   Identify the major turning points, breakthroughs, and enabling technologies.
4. **Research applications** — where and how the technology has been deployed. Look for
   both the original intended use and unexpected or expanded applications.
5. **Collect URLs** — every source referenced must be preserved in the final document.

If historical details are uncertain, flag them as `[VERIFY]` rather than guessing.

### Step 3: Write the History Section

This section has two required subsections:

#### 3a. Brief History Narrative (0.25-0.5 pages)

Write a **flowing narrative** (roughly 150-300 words) that tells the story of the
technology's origins and evolution. This subsection must:

- **Set the stage** — what problem or need drove the invention
- **Name the key people and dates** — who created it, when, and where
- **Trace the evolution** — how it changed, improved, or branched over time
- **Arrive at the present** — what the technology looks like today
- **Be self-contained** — a reader who stops here should have a correct, simplified
  understanding of the technology's history

**Tone:** Narrative and conversational, like a well-told story. A high school student
should be able to follow it without outside references.

**Time span:** Start as far back as ~200 years ago if meaningful precursors exist.
For newer technologies, start at the earliest relevant point.

#### 3b. Detailed History Timeline

A **bulleted chronological list** covering the same ground as the narrative but with
more specifics. Each entry should include:

- **Year or date range**
- **Person(s) or organization involved**
- **What happened** — the invention, discovery, publication, or milestone
- **Why it mattered** — its significance or what it enabled

Format:

```markdown
- **1822** — Charles Babbage designs the Difference Engine, the first automatic
  mechanical calculator. Though never fully built in his lifetime, it establishes
  the concept of programmable computation.
- **1843** — Ada Lovelace publishes notes on Babbage's Analytical Engine, including
  what is considered the first computer program — an algorithm for computing
  Bernoulli numbers.
```

Aim for **10-25 entries** depending on how rich the history is. Cover major milestones,
not every minor development.

### Step 4: Write the Application Section

This section follows the **same two-part structure** as the History section:

#### 4a. Brief Application Narrative (0.25-0.5 pages)

Write a **flowing narrative** (roughly 150-300 words) that describes how and where
the technology has been put to practical use. This subsection must:

- **Identify the earliest applications** — where was it first deployed?
- **Name the key industries or domains** — manufacturing, medicine, aerospace,
  consumer electronics, education, etc.
- **Describe how applications expanded** — from niche to mainstream, or from one
  field to many
- **Highlight current applications** — where is it used today?
- **Be self-contained** — stands alone as a correct summary of the technology's uses

**Tone:** Same as the history narrative — accessible, conversational, concrete.

#### 4b. Detailed Application Timeline

A **bulleted chronological list** of specific, notable applications. Each entry
should include:

- **Year or date range**
- **Industry, company, or context**
- **What the application was** — how the technology was used
- **Impact or significance** — what it achieved or enabled

Format:

```markdown
- **1947** — Bell Labs uses feedback control systems in early transistor
  manufacturing, enabling consistent production quality that makes commercial
  transistors viable.
- **1969** — NASA's Apollo Guidance Computer uses PID-style control for
  spacecraft attitude control during lunar missions.
```

Aim for **10-25 entries**. Include both landmark applications and surprising or
lesser-known uses that make the topic interesting.

### Step 5: Add Supporting Elements (As Needed)

Include any of these that genuinely help the reader. Omit those that don't add value.

**Key Figures Table**
A summary of the most important people in the technology's history:

| Person | Years | Contribution |
|:-------|:------|:-------------|
| James Watt | 1736-1819 | Improved the steam engine; introduced the centrifugal governor |
| Nicolas Minorsky | 1885-1970 | First formal analysis of PID control for ship steering |

**Evolution Diagram**
A text-based diagram showing major stages of development:

```text
Manual Control ──> Mechanical Governors ──> Analog Controllers ──> Digital PID ──> Adaptive Control
   (pre-1800)        (1788-1900)            (1920-1960)          (1970-2000)      (2000-present)
```

**Connection to This Workshop**
A brief paragraph (2-4 sentences) explaining how this technology relates to the
autonomous robot workshop. This helps students see why the history matters to what
they're building.

### Step 6: Review for Quality

Before finalizing, verify:
- [ ] History narrative is 0.25-0.5 pages (roughly 150-300 words), self-contained
- [ ] History timeline has 10-25 bulleted entries in chronological order
- [ ] Application narrative is 0.25-0.5 pages (roughly 150-300 words), self-contained
- [ ] Application timeline has 10-25 bulleted entries in chronological order
- [ ] Key people are named with dates and specific contributions
- [ ] Timeline goes back ~200 years where relevant, up to the present
- [ ] No unexplained jargon — every technical term defined on first use
- [ ] Tone is narrative and accessible for high school students
- [ ] All URLs preserved using reference-style links at the bottom of the file
- [ ] No duplicate URLs in the reference list
- [ ] Uncertain details flagged as `[VERIFY]`

### Step 7: Export

Save as a markdown file named after the topic in kebab-case with a
`history-and-application-` prefix:

- `history-and-application-pid-control.md`
- `history-and-application-line-following-robots.md`
- `history-and-application-infrared-sensors.md`

For other formats:
- **.docx** — Use pandoc: `pandoc -f gfm input.md -o output.docx`
- **.pdf** — Use pandoc with a PDF engine: `pandoc -f gfm input.md -o output.pdf`

## Output Structure

The final document must follow this structure:

```text
# History and Application: [Subject Name]

**Subject:** [what the document covers]
**Target Audience:** [who this is written for]
**Date:** [generation date]

## 1. History

### Brief History

[0.25-0.5 page narrative — origins, key people, evolution, present state]

### Detailed History Timeline

- **[Year]** — [Person/org] — [What happened]. [Why it mattered].
- **[Year]** — [Person/org] — [What happened]. [Why it mattered].
- ...continue for 10-25 entries...

## 2. Application

### Brief Application Overview

[0.25-0.5 page narrative — where/how it has been used, from earliest to present]

### Detailed Application Timeline

- **[Year]** — [Industry/context] — [How the technology was used]. [Impact].
- **[Year]** — [Industry/context] — [How the technology was used]. [Impact].
- ...continue for 10-25 entries...

## 3. Key Figures (if applicable)

## 4. Connection to This Workshop (if applicable)

## 5. Sources & References
```

### Link Management

All URLs must use **reference-style markdown links**.
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

#### Metadata Block
- **Subject:** what the document covers
- **Target Audience:** who this is written for (default: high school students)
- **Date:** generation date

**1. History**
Two subsections: a brief narrative (0.25-0.5 pages) telling the story of the technology's
origins and evolution, followed by a detailed bulleted timeline with 10-25 chronological
entries naming people, dates, and milestones.

**2. Application**
Two subsections mirroring the History structure: a brief narrative (0.25-0.5 pages) covering
how and where the technology has been applied, followed by a detailed bulleted timeline with
10-25 chronological entries naming industries, deployments, and impacts.

**3. Key Figures** (optional, encouraged)
Table of the most important people with dates and contributions.

**4. Connection to This Workshop** (optional, encouraged)
Brief paragraph connecting the topic to the autonomous robot workshop, helping students
see relevance.

**5. Sources & References**
All reference-style link definitions. Include historical references, biographies,
technical papers, and any sources consulted during research.

## Writing Principles

1. **Tell a story, not a list.** The narratives should read like a well-told story with
   a beginning, middle, and end — not like a textbook summary.
2. **Name names and dates.** History without specific people and dates is vague.
   "Someone invented it in the early 1900s" is weak. "Nicolas Minorsky analyzed
   automatic ship steering in 1922" is strong.
3. **Plain English first, then precision.** Introduce concepts in everyday language,
   then add the technical term. "A device that automatically adjusts itself to stay
   on course — this is called a *feedback controller*."
4. **Connect cause and effect.** Don't just list events — explain why each development
   led to the next. "Because vacuum tubes were unreliable and power-hungry, engineers
   sought a solid-state alternative — leading to the transistor."
5. **Include surprising details.** Good history writing includes unexpected facts that
   make the story memorable. "The first automatic pilot for ships was tested in 1911
   on a battleship, not a cargo vessel."
6. **Balance breadth and depth.** The narrative gives the big picture; the timeline
   gives the specifics. Don't make them redundant — the timeline should add detail
   the narrative omits.
7. **Match the audience.** Default is high school students in a robotics workshop.
   Keep language accessible, minimize math, and connect to things they know.

## Examples

### Example: Good Brief History Narrative

```markdown
### Brief History

The idea of a machine that follows a line on the ground has surprisingly deep roots.
It connects to two older ideas: autonomous vehicles and optical sensing. As early as
the 1940s, engineers were experimenting with simple vehicles that could sense light
and respond to it — William Grey Walter's "tortoise" robots (1948) used photosensors
to navigate toward light sources, demonstrating that a machine could exhibit seemingly
purposeful behavior with very simple circuits.

The first true line-following robot is generally credited to a team at Bell Labs in
the late 1950s. Their machine used photosensors to detect a painted line and adjusted
its steering accordingly. By the 1960s and 1970s, line-following became a standard
challenge in robotics education and competitions. The concept proved ideal for teaching
because it is mechanically simple, visually dramatic, and introduces core concepts —
sensing, feedback, and control — in a tangible way.

Today, line-following robots range from simple classroom kits using two photoresistors
to competition machines with 16-sensor arrays, PID controllers, and optimized chassis
that complete complex courses in seconds.
```

### Example: Good Timeline Entry

```markdown
- **1948** — William Grey Walter (Bristol, UK) builds "Elsie" and "Elmer," tortoise-shaped
  robots that use photosensors and simple analog circuits to navigate toward light.
  These are among the first autonomous robots and demonstrate that complex-looking
  behavior can emerge from simple sensing and feedback.
```

### Example: Bad Timeline Entry (too vague)

```markdown
- **1940s** — Early robots were built that could sense things.
```

This is bad because it names no person, no specific robot, no mechanism, and no significance.

### Example: Good Brief Application Narrative

```markdown
### Brief Application Overview

PID control is one of the most widely deployed algorithms in engineering — estimates
suggest that over 90% of industrial control loops use some form of PID. Its earliest
practical application was in ship steering: Nicolas Minorsky's 1922 analysis of
automatic helmsmen led directly to PID controllers for naval vessels. By the 1940s,
PID had spread to process industries — oil refineries, chemical plants, and power
stations used pneumatic PID controllers to regulate temperature, pressure, and flow.

The transition from analog to digital in the 1970s-1980s massively expanded PID's
reach. Microprocessors made it cheap to embed PID in everything from thermostats to
disk drives. Today, PID runs in automobile cruise control, drone flight stabilization,
3D printer temperature regulation, espresso machines, and — relevant to this workshop —
line-following robots that use PID to smoothly track a curved path.
```

## Applicability Across Domains

This skill works for any technology topic. Adapt the scope accordingly:

| Domain | History Starts With... | Applications Cover... |
| :------- | :----------------------- | :---------------------- |
| Electronics | Early electrical discoveries (~1800s) | Industrial, consumer, medical, military uses |
| Software/Algorithms | Mathematical foundations | Computing, automation, AI, web, mobile |
| Mechanical | Industrial revolution era | Manufacturing, transportation, robotics |
| Control Theory | Early governors and regulators | Process control, aerospace, automotive, robotics |
| Sensors | Early detection methods | Industrial, medical, environmental, consumer |

## Critical Rules

- **NEVER** generate without researching the subject first — check sources, historical records, biographies
- **NEVER** write the narratives as dry textbook summaries — tell a story
- **NEVER** use jargon without immediately defining it in plain language
- **ALWAYS** include both major sections (History and Application), each with both subsections (narrative and timeline)
- **ALWAYS** make each narrative self-contained — it must stand alone as a correct summary
- **ALWAYS** keep narratives to 0.25-0.5 pages (roughly 150-300 words each)
- **ALWAYS** include 10-25 timeline entries per section
- **ALWAYS** name specific people, dates, and places — no vague references
- **ALWAYS** connect cause and effect in the narrative — explain why, not just what
- **ALWAYS** preserve URLs from source documents — do not drop links found in course docs, BOM, or lesson plans
- **ALWAYS** use reference-style links (`[text][01]`) with definitions at the bottom — never inline URLs
- **NEVER** duplicate a URL in the reference list — reuse the same `[NN]` number
- **ALWAYS** flag uncertain historical details as `[VERIFY]`
- **ALWAYS** target high school students as the default audience — accessible language, minimal jargon
