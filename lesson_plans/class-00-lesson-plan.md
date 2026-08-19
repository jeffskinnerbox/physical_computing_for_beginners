# Lesson Plan: Pre-Class — Prepare Your Laptop and Pico

* **Class:** Pre-Class (Phase 0 — Setup), before Class 1 of 6
* **Phase:** Phase 0 — Setup (get every laptop and Pico ready to code)
* **Duration:** ~2 hours (120 min)
* **Prerequisites from prior Classes:** None — this is the first session of the course. Students
  arrive with only their own Windows 11 laptop and, if already distributed, their Raspberry Pi Pico
  2 W. No prior CircuitPython or electronics experience is assumed.

---

## 1. Class Overview

This is the very first session of the course and the only one with no hardware build beyond the Pico
itself — everything here is toolchain setup. Students install the editors (Mu and Thonny), flash
CircuitPython firmware onto their Raspberry Pi Pico 2 W, download the Adafruit CircuitPython Library
Bundle they'll draw from all course long, and write, save, and run their first CircuitPython program:
one that blinks the onboard LED and prints a heartbeat count to the serial console. There is no
sensor, actuator, or breadboard wiring today — the entire point is proving that board, firmware, and
editor are all talking to each other, so every later Class can start from a working foundation instead
of debugging the toolchain mid-build. The Class also plants the course's research-first habit early:
students see, explicitly, that this whole project was assembled from public tutorials and
documentation (Instructables, GitHub, Adafruit Learn, SparkFun), and that they're expected to use
those same resources themselves whenever they get stuck.

## 2. Learning Goals

* Install the Mu and Thonny editors and download the Adafruit CircuitPython Library Bundle
* Flash CircuitPython firmware onto a Raspberry Pi Pico 2 W and locate the CIRCUITPY drive
* Write, save (as `code.py`), and run a first CircuitPython program on the Pico 2 W
* Connect to and use the serial console and the REPL to observe a running program
* Explain, in plain language, what "firmware" is and why it must be flashed before any student code
  can run
* Name at least two places (Instructables, GitHub, Adafruit Learn, SparkFun) where working makers
  find and adapt existing code and documentation

## 3. Preparation Checklist

* **1-2 days before:** Confirm every Pico 2 W in the course kit is a genuine, working unit — spot-check
  a sample by flashing CircuitPython and running a blink test on the instructor bench. (~20 min)
* **1-2 days before:** Download and stage local copies of the CircuitPython firmware `.uf2` file, the
  Mu Editor installer, the Thonny installer, and the Adafruit CircuitPython Library Bundle `.zip` on a
  USB stick or shared drive — classroom WiFi on the first night is exactly the wrong time to depend on
  everyone's home internet being fast and reliable. (~20 min)
* **1-2 days before:** Verify the course GitHub repository is public (or that every student can be
  added) and that this Class's install guide/handout is up to date and linked from it. (~10 min)
* **Day of, before students arrive:**
  * Set out one Pico 2 W (with header) and one USB cable at each workstation.
  * Pre-flash one reference Pico with CircuitPython and pre-test `class-0-code.py` end-to-end
        (blink + heartbeat count over serial) on the instructor's own laptop, using both Mu and
        Thonny, so you can speak to both editors from direct experience. (~20 min)
  * Have the staged installers/firmware/Library Bundle accessible over the local network or a
        shared USB stick, not solely from the public internet.
  * Have spare Pico 2 W boards and USB cables on hand — a bad or "charge-only" USB cable is the most
        common first-night failure, and it looks identical to a dead board until eliminated.
* **Have ready:** A short list of discussion prompts for "why CircuitPython instead of MicroPython or
  Arduino C++?" and "what is firmware, and why does it matter?" (see Direct Teaching below).

## 4. Materials & Components

Per-student unless noted. Component names only — see the course Bill of Materials for costs,
quantities, and sourcing.

| Component | Purpose This Class |
| :---------- | :-------------------- |
| Raspberry Pi Pico 2 W (with header) | The microcontroller being set up; no other hardware is wired yet |
| USB cable (student-supplied going forward, provided tonight if needed) | Power, firmware flashing, and serial connection to laptop |
| Windows 11 laptop (student-supplied, no sharing) | Runs the editors and holds the toolchain for the rest of the course |
| Shared: staged CircuitPython firmware, Mu/Thonny installers, Library Bundle (USB stick or local network share) | Backup distribution path independent of classroom internet speed |

## 5. Class Timeline

### 5a. Warm-up / Hook — ~10 min

**What to do:** Welcome the group, introduce the course's six-Class arc at a glance (button/encoder
→ distance sensor/servo → motor driver → IMU → autonomous rover → finish/showcase), and set
expectations for tonight: no wiring, no robot yet — just getting every tool talking to every other
tool.

**What to say:** "Every one of the next six Classes assumes your laptop and your board already talk
to each other reliably. Tonight is entirely about making sure that's true, so nothing later gets
derailed by a setup problem instead of the actual physical computing."

**What to watch for:** Students without a Windows 11 laptop present, or with a laptop that's
locked down by school/parental software restrictions that block installers — flag these early;
they may need IT support or an alternate plan before Class 1.

**Time check:** Keep this brief — the bulk of tonight's time belongs to the install steps below.

### 5b. Introduction — ~10 min

**What to do:** Introduce the Pico 2 W, CircuitPython, and the "leave no soldier behind" philosophy
of the course — a GitHub repository backstops every Class with working code, so no student is ever
stuck without a starting point.

**What to say:**

* "This board is a full computer small enough to fit on a breadboard. Tonight, it doesn't know how
  to run Python at all — that's the very first thing we fix."
* "This whole course, start to finish, was built the same way working makers build things: by
  reading real documentation and adapting real examples from Adafruit, GitHub, Instructables, and
  SparkFun. You'll be doing exactly that yourselves by Class 2 or 3."
* "If you ever get stuck on your own project after this course, the course GitHub repo and these
  same sites are where you go — not just where I go."

**Questions to ask students:** "Has anyone here already used Python, Scratch, or another programming
language? What was different about it?" (Surfaces prior experience without turning it into a test.)

### 5c. Direct Teaching — ~10 min

No hands-on work yet — discussion and a few slides/diagrams only.

**Concept 1 — What "firmware" is, and why it has to come first (Theory of Operation, brief).**
A brand-new Pico 2 W's onboard flash memory has no operating system and no Python interpreter — it
can't run a `.py` file any more than a laptop with no OS installed could run a Word document.
Firmware is the low-level software that turns the raw microcontroller chip into "a computer that
understands CircuitPython." Flashing CircuitPython onto the board is a one-time (or occasional)
step that installs that interpreter; only after that can any student-written `code.py` actually run.

*Step-by-step decomposition of "flash CircuitPython":*

1. Hold the Pico's `BOOTSEL` button while plugging it into USB (or while pressing reset, per the
   specific board).
2. The board enumerates as a mass-storage drive (like a blank USB flash drive), not as CIRCUITPY yet.
3. Drag the downloaded CircuitPython `.uf2` firmware file onto that drive.
4. The board automatically reboots, running the newly flashed CircuitPython firmware.
5. The board now enumerates as a CIRCUITPY drive — code editing is now possible.

>**NOTE:** **BOOTSEL** (short for boot selection)
>is a hardware mechanism, usually a physical button or pin connection,
>used on microcontrollers to force the chip into a special programming mode at startup.
>When activated, it lets you load new firmware via USB without needing an external programmer.

**Concept 2 — Why CircuitPython instead of MicroPython or Arduino C++.**
Ask: "What do you think a hobbyist project gains by using a simpler, more readable language, and
what might it give up?" Draw out: CircuitPython trades raw execution speed and low-level hardware
control (which Arduino's C++ and, to a lesser extent, MicroPython offer) for readability, a huge
library ecosystem for common sensors/actuators, and a much shorter path from "board in hand" to
"first working program" — the right tradeoff for a beginner course, less so for a
performance-critical embedded product.

**Concept 3 — Why the CIRCUITPY drive behaves like a USB flash drive.**
Once CircuitPython is running, the board exposes its onboard storage as an ordinary-looking USB
drive named CIRCUITPY. Saving a `.py` file to it is literally just a file copy — no special upload
tool required. CircuitPython automatically detects the file was changed and re-runs whatever is
saved as `code.py` (or `main.py`). Ask: "What do you think happens the instant you finish saving
`code.py`?" (The board notices the change and restarts the program immediately — this is why the
onboard LED will blink differently within a second of hitting save, which becomes the first "aha"
moment of Guided Practice.)

### 5d. Guided Practice — ~40 min

Instructor walks through each install step on the projector; students follow along in parallel on
their own laptops and boards.

**Step 1 — install the editors.**
Install [Mu Editor][01] (the course's recommended editor) and [Thonny][02] (an alternate editor,
also used with the Pico). Use the staged local installers if classroom internet is slow.

**Checkpoint 1:** Both editors open successfully and can see the laptop's file system.

**Step 2 — flash CircuitPython onto the Pico 2 W.**
Follow [Installing CircuitPython][03] (or the staged local `.uf2` firmware file): hold `BOOTSEL`,
plug in via USB, drag the firmware file onto the resulting mass-storage drive, and wait for the
board to reboot into CircuitPython.

**What to watch for:** A board that never shows the `BOOTSEL` mass-storage drive at all almost
always means a charge-only USB cable, not a bad board — swap the cable before troubleshooting
anything else.

**Checkpoint 2:** The board reboots and a drive named **CIRCUITPY** appears in File Explorer — see
[The CIRCUITPY Drive][04].

**Step 3 — install the Adafruit CircuitPython Library Bundle.**
Download the [Adafruit CircuitPython Library Bundle][05] (or use the staged local `.zip`) and unzip
it somewhere memorable on the laptop — see [CircuitPython Libraries][06]. This is the shared source
every later Class's `/lib` copies come from; students won't add anything to the board's `/lib`
folder tonight, since `class-0-code.py` needs no external libraries.

**Checkpoint 3:** Students can locate the unzipped Library Bundle folder on their own laptop without
instructor help.

**Step 4 — write, save, and run the first program.**
Using [Creating and Editing Code][07] and [Exploring Your First CircuitPython Program][08] as a
guide, open `class-0-code.py` in Mu or Thonny, save it onto the CIRCUITPY drive as `code.py`, and
watch the onboard LED begin blinking.

```python
# class-0-code.py
# Save as code.py on the CIRCUITPY drive. No external parts required.
import time
import board
import digitalio

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

heartbeat = 0

print("Pre-Class -- CircuitPython heartbeat starting...")

while True:
    led.value = not led.value
    heartbeat += 1
    print("heartbeat:", heartbeat)
    time.sleep(0.5)
```

**What to watch for:** A file saved as `class-0-code.py` (not renamed to `code.py`) will sit on the
drive without running — CircuitPython only auto-runs `code.py` or `main.py` by name. This is the
single most common "nothing happened" report tonight.

**Checkpoint 4:** The onboard LED visibly blinks on/off roughly twice a second.

**Step 5 — connect to the serial console and the REPL.**
Using [Connecting to the Serial Console][09], [Interacting with the Serial Console][10], and
[The REPL][11] as guides, open the serial console in Mu or Thonny and watch the `heartbeat:` count
increment in real time. Then try typing a line directly at the REPL prompt (e.g. `print("hello")`)
to see code execute interactively, separate from the saved `code.py` file.

**What "done" looks like for this segment:** Every student can point at their own onboard LED
blinking and, on the same screen, watch a live-incrementing `heartbeat:` count in the serial
console — the visual and the text confirming the same thing two different ways.

### 5e. Independent Work — ~40 min

**What to do:** Students (in pairs where possible) modify `code.py` in small, deliberate steps and
observe the result each time — the "build a little, test a little" habit the whole course is built
around. Suggested modifications:

* Change the `time.sleep(0.5)` value and observe the blink rate change.
* Change the printed message text and confirm it updates after saving.
* Deliberately introduce a syntax error (e.g., delete a colon) and read the resulting traceback in
  the serial console — a low-stakes first look at how CircuitPython reports errors.
* Browse the [course GitHub repository][12] and the [Adafruit Learn][13] site to get comfortable
  navigating both before they're needed for real troubleshooting in Class 1.

**What to watch for:** The most common failure at this stage is a student who "saved" but the editor
was still mid-write or the drive was ejected — CIRCUITPY drives can appear to accept a save that
didn't fully flush; if code isn't updating, have them close and reopen the file from the drive to
confirm what's actually saved there.

**Time check:** At the 30-minute mark, do a quick show-of-hands: "Who has a blinking LED and a live
heartbeat count in the serial console?" Redirect instructor attention to pairs still stuck.

### 5f. Closing / Wrap-up — ~10 min

**What to do:** Ask 2-3 volunteers to show their blinking LED and live serial console to the group.
Recap tonight's real milestone: not the blink itself, but proving the full chain — laptop, editor,
USB connection, firmware, and board — all work together.

**What to say:** "Nothing you did tonight was really about an LED — it was about proving this whole
chain works, end to end, so that starting next Class, every minute you spend is on the actual physical
computing, not fighting your setup. Next time, that chain gets its first real test: a button and a
rotary encoder, and you'll watch, with your own eyes, why reading them cleanly is harder than it
looks."

**Preview next Class:** Class 1 is the first Class with real wiring — a pushbutton switch on `GP2`
and a KY-040 rotary encoder on `GP3`/`GP4`, driving two LEDs. Nothing from tonight needs to be
undone; tonight's `code.py` will simply be replaced. Point students to the Class 1 references in the
syllabus if they want to read ahead.

## 6. Troubleshooting Guide

| Problem | Likely Cause | Fix |
| :-------- | :------------- | :---- |
| Pico never shows a `BOOTSEL` mass-storage drive when plugged in | Charge-only USB cable, or `BOOTSEL` not held while plugging in | Swap to a known-good data cable; retry holding `BOOTSEL` throughout the plug-in |
| CIRCUITPY drive never appears after flashing | Firmware file didn't fully copy before ejecting, or wrong `.uf2` for this board revision | Re-flash from the start; confirm the firmware file matches "Raspberry Pi Pico 2 W" specifically |
| LED never blinks after saving `code.py` | File saved as `class-0-code.py` instead of renamed to `code.py` | Rename the file to exactly `code.py` on the CIRCUITPY drive root |
| Serial console shows nothing at all | Wrong COM port selected, or board not in a data-capable USB port | Reselect the port in Mu/Thonny; try a different USB cable/port |
| Editor won't install (blocked by school/parental controls) | Laptop restricted from installing new software | Use the portable/no-install version if available, or flag for IT support before Class 1 |
| `code.py` edits don't seem to take effect | Editor didn't finish writing to the drive before it was ejected, or file was edited in a different location than the CIRCUITPY drive | Close and reopen the file directly from the CIRCUITPY drive to confirm what's actually saved; avoid ejecting mid-save |
| Traceback appears in the serial console after an edit | Expected — likely a real syntax error introduced during Independent Work's error-reading exercise | Read the traceback's line number and message aloud; this is the intended lesson, not a failure |

## 7. Age Differentiation Notes

**Younger students (12-14) and their parent/guardian:** Provide a pre-printed, laminated step
checklist (install Mu → install Thonny → flash CircuitPython → download Library Bundle → save
`code.py` → open serial console) so the sequence is a lookup, not something to remember. Pair a
younger student's typing/saving work with the parent/guardian's help reading installer prompts and
confirming file names. Start from `class-0-code.py` already provided rather than typed from scratch,
and focus their Independent Work on the "change one value, observe the result" modifications rather
than the deliberate-syntax-error exercise, which can be introduced with more guidance.

**Older students (15-18) and adults:** Have them read the traceback from Independent Work's
deliberate syntax error and diagnose the specific line and cause themselves before being told the
answer. Once the core milestone is met, challenge them to look through the unzipped Library Bundle
folder and identify two or three libraries by name that they predict the course will use later
(`adafruit_debouncer`, `adafruit_hcsr04`, `adafruit_motor` are all visible in the Bundle) — a preview
exercise that connects tonight's install to the rest of the course.

## 8. Assessment

**Milestone Assignment (per syllabus, Phase 0 / Pre-Class):** A running CircuitPython program on
your own Pico 2 W, visible over the serial console.

**What "complete" looks like:** The student can plug in their own Pico 2 W, show the onboard LED
blinking, open the serial console in Mu or Thonny, and show the `heartbeat:` count incrementing live
— all without instructor assistance in the moment.

**How to give feedback without scoring:** Ask the student to narrate, in their own words, what
happens between saving `code.py` and the LED changing behavior ("what actually happens when you hit
save?") rather than checking a box. If a pair can't get the full chain working in the time available,
that's fine — have them bring a working setup to the start of Class 1, and prioritize instructor
follow-up with them individually before then rather than losing Class 1 time to setup.

## 9. Instructor Tips

* Do the entire flash-and-blink sequence yourself, live, on the projector *before* students touch
  their own boards — this is the first thing many students have ever flashed firmware onto, and
  seeing it work once, start to finish, demystifies it.
* Stage every installer, the firmware file, and the Library Bundle locally (USB stick or local
  network share) rather than relying on classroom internet for a room full of simultaneous
  downloads — this single prep step prevents the most common first-night bottleneck.
* Charge-only USB cables are the single most common "my board doesn't work" report tonight — keep a
  labeled bin of confirmed data-capable cables and hand them out proactively to anyone struggling
  with the `BOOTSEL` step.
* The deliberate-syntax-error exercise (Independent Work) is worth insisting every pair actually try
  — reading and not fearing a traceback is a skill that pays off in every single later Class.
* Keep `class-0-code.py` on a shared drive/USB stick so a student who breaks their working file can
  recover instantly instead of losing session time.

## 10. Resources & References

* [Raspberry Pi Pico 2 W with Header — Product Page][14] — the board used throughout the course
* [CircuitPython Firmware for the Raspberry Pi Pico 2 W][03] — the firmware flashed onto the board
  this Class
* [What is CircuitPython?][15] — background on CircuitPython vs. MicroPython vs. Arduino C++
* [MicroPython][16] — referenced for the "why CircuitPython instead of MicroPython?" discussion
* [Recommended Editors][17] — Adafruit's overview of CircuitPython-friendly editors
* [Installing the Mu Editor][01] — step-by-step Mu install guide
* [Thonny setup for CircuitPython][02] — step-by-step Thonny install guide
* [The CIRCUITPY Drive][04] — what the CIRCUITPY drive is and how it behaves
* [Creating and Editing Code][07] — saving and editing `code.py`
* [Exploring Your First CircuitPython Program][08] — walkthrough of a first simple program
* [Connecting to the Serial Console][09] — how to open the serial console in Mu/Thonny
* [Interacting with the Serial Console][10] — reading and using serial console output
* [The REPL][11] — using the interactive REPL prompt
* [CircuitPython Libraries][06] — what the Library Bundle is and how `/lib` is used in later Classes
* [CircuitPython Hardware][18] — broader background on CircuitPython-compatible boards
* [Welcome to the Community!][19] — where to find help beyond this course
* [CircuitPython Documentation][20] — official reference documentation
* [Instructables][12] — maker-community tutorials referenced throughout the course
* [GitHub Docs][21] — used for the course GitHub repository
* [Adafruit Learn][13] — primary source for CircuitPython guides used across the course
* [SparkFun Docs][22] — additional maker-community documentation referenced throughout the course

---

[01]:https://learn.adafruit.com/welcome-to-circuitpython/installing-mu-editor
[02]:https://learn.adafruit.com/circuitpython-libraries-on-micropython-using-the-raspberry-pi-pico/thonny-setup
[03]:https://circuitpython.org/board/raspberry_pi_pico2_w/
[04]:https://learn.adafruit.com/welcome-to-circuitpython/the-circuitpy-drive
[05]:https://circuitpython.org/downloads
[06]:https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-libraries
[07]:https://learn.adafruit.com/welcome-to-circuitpython/creating-and-editing-code
[08]:https://learn.adafruit.com/welcome-to-circuitpython/exploring-your-first-circuitpython-program
[09]:https://learn.adafruit.com/welcome-to-circuitpython/kattni-connecting-to-the-serial-console
[10]:https://learn.adafruit.com/welcome-to-circuitpython/interacting-with-the-serial-console
[11]:https://learn.adafruit.com/welcome-to-circuitpython/the-repl
[12]:https://www.instructables.com/
[13]:https://learn.adafruit.com/
[14]:https://www.adafruit.com/product/6315
[15]:https://learn.adafruit.com/welcome-to-circuitpython/what-is-circuitpython
[16]:https://micropython.org/
[17]:https://learn.adafruit.com/welcome-to-circuitpython/recommended-editors
[18]:https://learn.adafruit.com/welcome-to-circuitpython/beginner-boards
[19]:https://learn.adafruit.com/welcome-to-circuitpython/welcome-to-the-community
[20]:https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-documentation
[21]:https://docs.github.com/en
[22]:https://docs.sparkfun.com/
