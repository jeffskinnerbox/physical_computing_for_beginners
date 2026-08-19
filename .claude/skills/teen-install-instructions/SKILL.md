---
name: teen-install-instructions
description: Generates a well-commented, teen-friendly Markdown installation guide (Bash/PowerShell/Python commands) for setting up software on an Ubuntu 24.04 server, a Windows 11 laptop, or a CircuitPython-capable microcontroller. Written for a 12-18 year old reader who already knows basic Bash, PowerShell, and Python. Produces a structured document (purpose, install manifest table, target environment, step-by-step install/test/cleanup blocks), then runs the draft through a "currency check" subagent and a Docker sandbox-validation subagent before finalizing. Use this skill whenever the user wants to create an installation tutorial, setup guide, or onboarding walkthrough for a young learner, wants to document how to install a dev tool / library / board firmware for a student, or mentions things like "install guide for a teenager/student", "beginner setup instructions", "onboarding script for my kid", or setup docs targeting Ubuntu, Windows 11, or CircuitPython boards.
---

# Teen Install Instructions

Turns a rough idea ("get my student set up with X") into a polished, tested, step-by-step
Markdown install guide, written at a level a 12-18 year old with basic Bash/PowerShell/Python
literacy can follow without hand-holding.

Requires the **Task tool** (subagents) — this skill is designed for Claude Code. If the Task
tool isn't available, fall back per the note at the end of Step 4 and Step 5.

## Workflow overview

1. Intake — ask the user what/where/sources
2. Research the current, correct install steps
3. Draft the document to the required structure
4. Subagent A: currency check → fix → iterate
5. Subagent B: sandbox validation → fix → iterate
6. Summarize + write the final file

Keep a running "iteration log" (in scratch, not shown to the user until Step 6) of every
finding from both subagents and what you changed in response — you'll need it for the final
summary.

---

## Step 1: Intake

Before drafting anything, ask the user (use the elicitation/button tool if available, otherwise
ask plainly — one round, batch the questions, don't drip them out one at a time):

1. **What & name**: a one-sentence description of what's being installed, and a short name/title
   for this guide. Slugify it (lowercase, hyphens) to use as the default output filename, e.g.
   "CircuitPython Neopixel Setup" → `circuitpython-neopixel-setup.md`.
2. **Preferred sources**: any URLs or local file paths that are good references for these install
   steps. Make clear these are a starting point, not exclusive — you'll still verify against
   current official docs.
3. **Target(s)**: confirm which of Ubuntu 24.04 server, Windows 11 laptop, or a CircuitPython
   board this covers (can be more than one in the same guide).
4. **Whatever else is ambiguous** — ask as many follow-ups as needed to remove real ambiguity
   before drafting. Common gaps worth checking:
   - Exact CircuitPython board model (Feather, Pico, QT Py, etc.) if that target applies
   - Whether the user has sudo/admin rights on the target machine
   - Pin specific versions, or always install latest-stable
   - Any accounts/API keys/tokens the install will need
   - Offline/network-restricted environment or normal internet access

Don't proceed to drafting until these are answered — an ambiguous target (e.g. "a Feather" vs.
"which Feather") produces wrong commands, not just imperfect ones.

## Step 2: Research

- `web_fetch` every URL the user gave you; read every local path they gave you.
- Run `web_search` to confirm each tool's *current* official install instructions and latest
  stable version — the user's sources are a starting point, not gospel, and may be stale.
- Note the version numbers and dates you find; you'll need these for the manifest table and for
  Subagent A to check against.

## Step 3: Draft the document

Follow the exact section order and formatting rules below. See `assets/document-template.md`
for a ready-to-fill skeleton — start from it rather than improvising the layout.

**Section order:**

1. **Purpose** — plain-language: what does the reader gain once this is done? Write to the
   student, not about them.
2. **What gets installed** — a Markdown table: `Component | What it does | Why you need it |
   Instructions source | Official docs`. One row per tool/package/library. "Instructions source"
   is the URL you actually drew the steps from (a user-supplied source or one you found in Step
   2). "Official docs" is a link to that project's real reference documentation.
3. **Target environment** — the hardware/software the reader needs before starting: OS +
   version, minimum RAM/disk, required accounts, network access, anything that must already be
   true.
4. **Installation** (one or more sections) — the actual walkthrough. See rules below.

**Installation section rules:**

- Start a new `##` section every time the target machine or the primary tool changes (e.g.
  moving from "on the Ubuntu server" to "on your Windows laptop" to "flashing the board"). Open
  each new section with 2-3 sentences of plain-language context: what's about to happen and why
  the reader is switching gears.
- If one section's install sequence is long, split it into `###` sub-sections for each major
  block (e.g. "Install the package manager", "Install the library", "Verify the sensor").
- Every command block must be fenced with the right language tag (`bash`, `powershell`,
  `python`) and **densely commented in plain language**. The reader knows basic Bash/PowerShell/
  Python syntax but not why a particular flag or step exists — comment the *why*, not just
  restate the command. Assume nothing about jargon: define acronyms and flags inline the first
  time they appear.
- Every major block ends with:
  - **Test it** — at least one check like `<tool> --version`, plus, wherever it's actually
    possible, running the installed tool against a small piece of real/sample data (not just a
    version check). Show expected output where practical.
  - **Clean up** — remove any test/sample data or temp files created just for the test, so the
    environment is left in the state a real project would want.
- Never invent a command you haven't verified in Step 2 (or that Subagent A/B will verify) —
  guessing flags for a 12-18 year old audience is how they end up debugging a typo instead of
  learning the tool.

## Step 4: Currency check (Subagent A)

Launch a subagent with the Task tool using the prompt in `agents/currency-checker.md`, passing
it the full draft plus the sources you used.

- If it returns required changes, make them, then re-run the subagent on the updated draft.
- Cap it at 3 rounds. If disagreement remains after 3 rounds, stop, keep your best-judgment
  version, and record the unresolved point for the Step 6 summary rather than looping forever.
- Log every finding and fix (or non-fix, with reason) to your iteration log.

*No Task tool available:* do this pass yourself instead. Explicitly switch hats — re-read the
draft as a skeptical reviewer checking each command against current docs, not as its author —
and log findings the same way.

## Step 5: Sandbox validation (Subagent B)

Launch a subagent with the Task tool using the prompt in `agents/sandbox-validator.md`, passing
it the full (post-Step-4) draft.

- **Ubuntu-target sections**: the subagent actually builds a Docker sandbox (`ubuntu:24.04`
  base) and executes each install/test/cleanup block for real, capturing exit codes and output.
- **Windows 11 and CircuitPython sections**: these can't run in a Linux container. The subagent
  instead does a careful static review (syntax, logical ordering, missing steps) and produces a
  manual-verification checklist for a human to run on real hardware/a real Windows machine. Mark
  these sections in the final doc as "manually verified" rather than "sandbox-tested" — don't
  blur the two.
- If the subagent identifies missing prerequisites (e.g. the base image lacks `curl`), fold
  those into the guide's own install steps if the *reader* would also need them, or into the
  Dockerfile/test harness only if they're sandbox-only artifacts.
- Fix errors it finds, re-run, cap at 3 rounds same as Step 4, log everything.

*No Task tool / no Docker available:* do a careful manual dry-run of the Ubuntu commands
yourself where safe to do so (e.g. in this session's own Linux container), and fall back to the
static-review approach for all three targets. Say clearly in the final summary that sandbox
execution didn't happen and why.

## Step 6: Finalize

- Write a short summary **in the chat response** (not necessarily inside the document) of: what
  Subagent A and Subagent B each flagged, and what you changed in response. If something was
  left unresolved after 3 rounds, say so plainly.
- Save the finished document to the filename from Step 1 (default: the slugified name + `.md`
  if the user didn't specify one).
- Present the file to the user.
