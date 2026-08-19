---
name: theory-of-operation
description: Generate a theory of operation document for a technology, software program, machine, electronic circuit, or system. Use when someone needs to understand how something works internally — both as a brief plain-language overview and as a detailed step-by-step decomposition of its operation. Covers any domain — hardware, software, mechanical, chemical, or hybrid systems.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
license: MIT
metadata:
  author: Jeff Irland (Makersmiths)
  version: "0.0.1"
---

# Theory of Operation Generator

Generate clear, well-structured theory of operation documents that explain how a technology,
software program, machine, electronic circuit, or system works. Each document contains two
required sections: a **brief overview** (1-2 paragraphs) and a **detailed step-by-step
decomposition** of the system's operation.

## Definitions
For shared terminology and type definitions across all the skills in `.claude/skills/`, read `.claude/skills/shared/definitions.md`.

## What Is a Theory of Operation?

A theory of operation is a description of how a device or system is intended to work.
It provides the reader with a mental model of the system's internal behavior — what happens
inside when the system runs, and why. The term has roots in military technical manuals
(MIL-STD-40051 specifically addresses "Theory of Operation" sections) and is standard practice
in electronics, aerospace, and software engineering documentation.

As engineers on the EEVblog forum put it: a theory of operation documents expected behavior
so that deviations become detectable. Without a specification of normal operation,
identifying faults is guesswork. In German engineering practice, this is called a
*Funktionsbeschreibung* — a prose description of a circuit's or system's workings that
accompanies every design.

A theory of operation consolidates scattered knowledge into a single coherent narrative.
It is not as detailed as schematics, CAD drawings, or source code, but it captures the
underlying engineering rationale — the "how and why" that makes the detailed design make sense.

### What It Is NOT

A theory of operation is **not**:
- A **user manual** — how to operate the system (buttons, menus, procedures)
- A **build guide** — how to assemble or manufacture it
- A **datasheet** — exhaustive electrical/mechanical specifications
- A **troubleshooting guide** — what to do when it fails
- A **tutorial** — how to learn a skill using the system
- A **math model** — rigorous equations and proofs

It may reference any of these, but its sole purpose is explaining **how the system works**
when it works correctly.

## When to Use This Skill

Activate when:
- Someone asks for a "theory of operation," "how it works" document, or "operating principle"
- Documentation is needed that explains a component, circuit, algorithm, machine, or system
- A design needs a prose companion that captures the engineering rationale
- Someone asks "how does [X] work?" and the answer warrants a structured document
- Knowledge preservation is needed — capturing how a system works before institutional
  knowledge is lost

## How to Generate a Theory of Operation

### Step 1: Identify the Subject and Scope

Determine exactly what the document covers. Ask:
- **What is the subject?** A single component, a subsystem, or a complete system?
- **What domain?** Electronics, software, mechanical, chemical, hybrid?
- **What scope level?**
  - **Narrow:** A single component or module (e.g., "H-bridge motor driver," "binary search algorithm")
  - **Medium:** A subsystem with multiple interacting parts (e.g., "PID control loop," "USB handshake protocol")
  - **Broad:** A complete system (e.g., "autonomous line-following robot," "laser printer")

If scope is ambiguous, default to medium — useful without being unwieldy.

### Step 2: Research the Subject

Before writing:

1. **Search for authoritative sources** — manufacturer datasheets, application notes, RFCs,
   official documentation, peer-reviewed papers, and reputable engineering references.
2. **Identify the core operating principle** — the fundamental mechanism that makes the system work.
   Every system has one central idea; find it.
3. **Map the signal/data/energy flow** — trace the path from input to output.
   This flow becomes the backbone of the step decomposition.
4. **Note key parameters** — voltages, frequencies, data rates, thresholds, tolerances —
   whatever characterizes normal operation.
5. **Collect URLs** — every source referenced must be preserved in the final document.

If technical details are uncertain, flag them as `[VERIFY]` rather than guessing.

### Step 3: Write the Brief Overview

Write **1-2 paragraphs** that give the reader a correct mental model of the system.
This section must:

- **State what the system does** — its purpose and function, in one sentence
- **Name the core operating principle** — the fundamental mechanism, in plain language
- **Identify key inputs and outputs** — what goes in, what comes out
- **Mention the major stages or components** — name them without detailed explanation
- **Be self-contained** — a reader who stops here should have a correct, simplified understanding

**Tone:** Precise but conversational. Define technical terms on first use. A motivated
non-specialist should be able to follow the overview without outside references.

**Length:** Aim for 80-200 words. Enough to be substantive, short enough to be read in under a minute.

### Step 4: Write the Detailed Step-by-Step Decomposition

Decompose the system's operation into discrete, ordered steps. Each step gets:

#### Step Title
A short, descriptive name (3-8 words). Examples:
- "IR Light Emission and Reflection"
- "Analog-to-Digital Conversion"
- "PID Error Calculation"
- "TCP Three-Way Handshake"
- "Fuel-Air Mixture Ignition"

#### Detailed Description
A thorough explanation covering:
- **What triggers this step** — what condition or input initiates it
- **What happens** — the physical, electrical, chemical, or computational process
- **What components or code are involved** — name the specific parts
- **What the result is** — the output, state change, or effect produced
- **How it connects to the next step** — explicit transition

#### Decomposition Guidelines

- **Follow the operational sequence** — the order things happen when the system runs.
  This is often different from the assembly order or teaching order.
- **Aim for 4-10 steps.** Fewer than 4 usually means steps are too coarse and conflate
  multiple operations. More than 10 usually means the scope is too broad — consider
  splitting into separate documents for subsystems.
- **One concept per step.** If a step explains two distinct operations, split it.
- **Include concrete values.** "The ADC returns a 16-bit value (0-65535)" is more useful
  than "the ADC digitizes the signal."
- **Note failure modes where they aid understanding.** "If the timing exceeds 2ms, the
  watchdog resets the controller" explains both the step and the system's self-protection.

### Step 5: Add Supporting Elements (As Needed)

Include any of these that genuinely help the reader. Omit those that don't add value.

**Block Diagram or Signal Flow**
A text-based diagram showing major stages and flow from input to output:

```text
[Input] --> [Stage 1] --> [Stage 2] --> [Stage 3] --> [Output]
```

For branching flows:

```text
Sensor Array ──> ADC ──> Error Calc ──> PID Controller
                                             │
                                             v
                                        Motor Driver ──> Motors
```

**Key Parameters Table**
Operating values that characterize normal behavior:

| Parameter | Typical Value | Notes |
| :---------- | :------------- | :------ |
| Supply voltage | 5V DC | Regulated |
| Clock frequency | 16 MHz | Crystal oscillator |

Include only parameters that build understanding — not exhaustive datasheet specs.

**Common Misconceptions**
Address 2-4 frequent misunderstandings:

- **Misconception:** "The sensor detects color."
  **Reality:** It detects reflectance — how much light bounces back, regardless of color.

### Step 6: Review for Quality

Before finalizing, verify:
- [ ] Brief overview is self-contained — stands alone as a correct summary
- [ ] Overview is 1-2 paragraphs (80-200 words), not longer
- [ ] Steps follow the operational sequence, not the build or teaching sequence
- [ ] Every step has both a title and a detailed description
- [ ] Each step covers: trigger, process, components, result, and transition to next step
- [ ] Step count is between 4 and 10
- [ ] No unexplained jargon — every technical term defined on first use
- [ ] The document explains how it works, not how to build or use it
- [ ] Concrete values and units included where they aid understanding
- [ ] All URLs preserved using reference-style links at the bottom of the file
- [ ] No duplicate URLs in the reference list
- [ ] Uncertain details flagged as `[VERIFY]`

### Step 7: Export

Export to the requested format:
- **.md** — GitHub-flavored markdown (default)
- **.docx** — Use pandoc: `pandoc -f gfm input.md -o output.docx`
- **.pdf** — Use pandoc with a PDF engine: `pandoc -f gfm input.md -o output.pdf`

## Output Structure

The final document must follow this structure:

```text
# Theory of Operation: [Subject Name]

**Subject:** [what the document covers]
**Scope:** [narrow / medium / broad]
**Target Audience:** [who this is written for]
**Date:** [generation date]

## 1. Overview

[1-2 paragraph brief description]

## 2. Detailed Operation

### Step 1: [Step Title]
[Detailed description]

### Step 2: [Step Title]
[Detailed description]

### Step 3: [Step Title]
[Detailed description]

...continue for all steps (typically 4-10)...

## 3. Block Diagram (if applicable)

## 4. Key Parameters (if applicable)

## 5. Common Misconceptions (if applicable)

## 6. Sources & References
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
- **Scope:** narrow / medium / broad
- **Target Audience:** who this is written for (default: general technical audience)
- **Date:** generation date

**1. Overview**
One to two paragraphs. Must answer: What does this system do? What is the core principle?
What goes in and what comes out? Self-contained — a complete summary on its own.

**2. Detailed Operation**
The heart of the document. Steps ordered by operational sequence. Each step has a title
and a detailed description covering trigger, process, components, result, and transition.

**3. Block Diagram** (optional, encouraged for hardware and hybrid systems)
Text-based diagram showing flow from input to output through major stages.

**4. Key Parameters** (optional, encouraged for hardware)
Table of typical operating values.

**5. Common Misconceptions** (optional, include when the subject has well-known confusions)
Misconception/reality pairs that correct frequent misunderstandings.

**6. Sources & References**
All reference-style link definitions. Include datasheets, application notes, official docs,
and any sources consulted during research.

## Writing Principles

1. **Explain operation, not construction.** The question is "what happens when it runs?"
   not "how do I build it?"
2. **Follow the signal/data/energy flow.** Structure steps along the path from input to output.
3. **Plain English first, then precision.** Introduce concepts in everyday language,
   then add the technical term. "The chip compares two voltages and outputs high or low —
   this is called a *comparator*."
4. **Concrete before abstract.** Describe what physically happens before the theory behind it.
5. **Include numbers that build intuition.** "Reads ~60,000 on white, ~3,000 on black"
   beats "output varies with reflectance."
6. **One concept per step.** If a step covers two operations, split it.
7. **Connect steps explicitly.** End each step by stating what it produces and how the next
   step uses it. No gaps in the chain.
8. **Match the audience.** Default is a general technical audience. Adjust depth if the
   user specifies otherwise (e.g., high school students, experienced engineers).

## Examples

### Example: Good Brief Overview

```markdown
## 1. Overview

An H-bridge motor driver allows a microcontroller to spin a DC motor in both directions
and control its speed, using just a few logic-level signals. The core principle is simple:
four switches (typically MOSFETs) are arranged in an "H" pattern around the motor. By closing
different pairs of switches, current flows through the motor in either direction — forward or
reverse. Speed control is achieved by rapidly switching the current on and off (PWM) faster
than the motor can respond mechanically, so the motor sees an average voltage proportional
to the duty cycle.

The DRV8833, for example, packages two full H-bridges into a single chip. It takes logic-level
input signals (IN1, IN2 per channel), handles the MOSFET switching internally, and can deliver
up to 1.5A per channel from a 2.7-10.8V supply. A microcontroller controls direction by setting
which input is active and controls speed by applying a PWM signal to that input.
```

### Example: Good Operational Step

```markdown
### Step 3: PWM Speed Regulation

The microcontroller generates a pulse-width modulation (PWM) signal on the active input pin —
a square wave that rapidly toggles between high and low at a fixed frequency (typically 1-20 kHz
for small DC motors). The DRV8833 responds by switching its internal MOSFETs on and off at
that same rate, chopping the motor supply voltage into pulses.

Because the motor's mechanical inertia and inductance act as a low-pass filter, the motor
cannot speed up and slow down fast enough to follow each individual pulse. Instead, it responds
to the average voltage, which is proportional to the PWM duty cycle. A 50% duty cycle delivers
roughly half the supply voltage as average power; 100% delivers full voltage.

This PWM signal from the microcontroller is the input to Step 4, where the resulting motor
speed produces wheel rotation that moves the robot.
```

### Example: Bad Operational Step (too vague)

```markdown
### Step 3: Motor Control

The motor driver controls the motor speed based on signals from the microcontroller.
```

This is bad because it names no mechanism (PWM), gives no values, explains no physics,
and provides no connection to adjacent steps.

### Example: Good Block Diagram

```markdown
## 3. Block Diagram

Microcontroller                 DRV8833                      Motor
┌───────────┐             ┌──────────────────┐           ┌───────────┐
│  GPIO Pin ├─── IN1 ────>│  H-Bridge A      ├── OUT1 ──>│           │
│  (PWM)    │             │  (4 MOSFETs)     ├── OUT2 ──>│  DC Motor │
│           ├─── IN2 ────>│                  │           │           │
└───────────┘             └────────┬─────────┘           └───────────┘
                                   │
                            VM (motor supply)
                              2.7V - 10.8V
```

## Applicability Across Domains

This skill works for any domain. Adapt the vocabulary and supporting elements accordingly:

| Domain | "Steps" Follow... | Key Parameters | Block Diagram Shows... |
| :------- | :------------------- | :--------------- | :----------------------- |
| Electronics | Signal path | Voltages, currents, frequencies | Circuit signal flow |
| Software | Data/control flow | Data sizes, latencies, throughput | Module/component interaction |
| Mechanical | Energy/force path | Torques, speeds, tolerances | Force/motion transmission |
| Chemical | Reaction sequence | Temperatures, pressures, concentrations | Process flow |
| Hybrid systems | Primary operational loop | Mix of above | System-level interaction |


## Critical Rules

- **NEVER** generate without researching the subject first — check sources, datasheets, documentation
- **NEVER** explain how to build, assemble, or use the system — this is not a build guide or user manual
- **NEVER** use jargon without immediately defining it in plain language
- **ALWAYS** include both the brief overview AND the detailed steps — both are required
- **ALWAYS** make the brief overview self-contained — it must stand alone as a correct summary
- **ALWAYS** limit the overview to 1-2 paragraphs (80-200 words)
- **ALWAYS** follow the operational sequence in steps, not the build or teaching sequence
- **ALWAYS** give every step both a title and a detailed description
- **ALWAYS** include concrete values and units where they build intuition
- **ALWAYS** connect steps explicitly — no gaps in the operational chain
- **ALWAYS** preserve URLs from source documents — do not drop links found in course docs, BOM, or lesson plans
- **ALWAYS** use reference-style links (`[text][01]`) with definitions at the bottom — never inline URLs
- **NEVER** duplicate a URL in the reference list — reuse the same `[NN]` number
- **ALWAYS** flag uncertain technical details as `[VERIFY]`
