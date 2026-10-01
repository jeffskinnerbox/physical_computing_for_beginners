# Physical Computing for Beginners

*A Makersmiths hands-on class.*

No prior coding required. Students wire up sensors, motors, and a microcontroller, then teach
them to talk to each other. Six two-hour classes plus a Pre-Class stack up to one capstone: the
Random Rover, a robot car that scans its surroundings and steers itself clear of whatever's in
the way.


## Table of Contents
- [Overview](#overview)
- [What You'll Build](#what-youll-build)
- [Course Structure](#course-structure)
- [Getting Started](#getting-started)
- [Repository Layout](#repository-layout)
- [How This Repository Is Generated](#how-this-repository-is-generated)
- [Safety Notes](#safety-notes)
- [Status and Support](#status-and-support)
- [Credits and License](#credits-and-license)


## Overview

| | |
| :--- | :---- |
| **Audience** | Middle/high schoolers; no prior Python/CircuitPython experience required |
| **Format** | 1 Pre-Class + 6 Classes, 2 hours each, at Makersmiths' Electronics room |
| **Capstone project** | The Random Rover — an obstacle-avoiding robot car |
| **Hardware** | Raspberry Pi Pico 2 W, pushbutton + KY-040 rotary encoder, HC-SR04 ultrasonic sensor, SG90 servo, DRV8833 dual H-bridge driver, 9V battery + 5V buck converter, IR optocoupler wheel-speed sensors, LSM9DS1 IMU, limit switch + IR obstacle sensor, 1.14" ST7789 TFT display |
| **Software** | CircuitPython on the Pico; laptop-side Python (via `uv`) for the Class 4 3D orientation viewer and the full-build deploy/test scripts |


## What You'll Build

Pre-Class is just getting everyone's laptop and board talking to each other: flash CircuitPython,
blink the onboard LED, print a heartbeat to the serial console. Once that's working, every class
after it bolts on one new piece without disturbing what's already running:

- debounced button + rotary encoder for clean digital input (Class 1)
- HC-SR04 ultrasonic sensor + SG90 servo for distance sensing and motion (Class 2)
- DRV8833 dual H-bridge driver putting two motors under code control (Class 3)
- IR optocoupler wheel-speed sensors for wheel odometry, plus a Pico-hosted rover status website
    that starts here and grows every class after (Class 3)
- LSM9DS1 IMU with a Mahony filter for orientation sensing, posted to the same rover website
    (Class 4)

Class 5 folds the sensor, servo, and motor driver together into the Random Rover: it drives
forward, checks what's ahead, and steers itself clear of anything in the way. The IMU's
magnetometer is calibrated and fused in, so a drift-free compass heading steers every turn — and
the heading and collision-avoidance state are posted live to the rover website. Class 6 finishes the Rover and
opens up stretch goals: encoder-based speed control, a rolling-history chart added to the
already-running rover website, and a TFT status display.

The rover website runs with the Pico as its own WiFi access point at `http://192.168.4.1:5000` —
port 5000, not 80, because CircuitPython's Web Workflow may already hold port 80.

Nothing gets rewired mid-course. GPIO pins are assigned up front so a circuit built in Class 1
is still live and working by Class 6. The one exception is power: in Class 5 the HC-SR04 and servo
move from `VBUS` to the buck converter's `VSYS` rail so the Rover can run untethered.


## Course Structure

| Class | Focus | New Hardware/Concept |
| --- | --- | --- |
| Pre-Class | Laptop + board bring-up | Flash CircuitPython, serial console, blink + heartbeat |
| Class 1 | Push button + rotary encoder | Debounced digital input |
| Class 2 | Ultrasonic distance sensor + servo | HC-SR04, SG90 servo, PWM |
| Class 3 | Dual H-bridge motor driver | DRV8833, two DC motors, 9V battery (`VM`); wheel odometry (IR optocoupler) and the first version of the rover status website |
| Class 4 | Inertial measurement unit | LSM9DS1 (9-DOF), I2C, Mahony filter; orientation added to the rover website |
| Class 5 | Random Rover | Sensor + servo + motor driver combined for collision avoidance; limit switch + IR safety sensors; magnetometer compass for closed-loop turns; heading/scan/stop telemetry added to the rover website |
| Class 6 | Finish the Rover | Stretch goals: encoder speed control, rolling-history chart added to the rover website, TFT display |

Wiring/pin assignments are chosen so each class's circuit keeps working after later classes add
to it — nothing gets rewired mid-course (apart from Class 5's `VBUS`-to-`VSYS` power move). The
[syllabus][05] is the authoritative class-by-class outline; this table is a summary.


## Getting Started

1. Work through the Windows 11 setup guides in [`tech_setup_check/`][01] before Pre-Class (no
   Linux/macOS guides yet).
2. Gather materials from the [bill of materials][02].
3. Flash CircuitPython to the Pico 2 W and get the onboard LED blinking — that's the Pre-Class
   build, walked through in [`lesson_scripts/class-00-lesson-script.md`][03].
4. Already finished the course, or rebuilding a rover? The [full build script][04] builds the
   finished Random Rover (Classes 1-6 plus all stretch goals) in one session, with ready-to-deploy
   code and test scripts.

Instructors start from the [syllabus][05] and the per-class lesson plans in [`lesson_plans/`][06];
students follow the matching walkthroughs in [`lesson_scripts/`][07].


## Repository Layout

```text
input/            Source-of-truth vision doc + prompt log — everything else is generated from this
methodology/      Background notes on course terms and authoring methodology (not generated)
lesson_plans/     Instructor-facing syllabus + per-class lesson plans, BOM
lesson_scripts/   Student-facing build+code walkthroughs, one per class (class-00 .. class-06)
full_build/       One-session build of the finished rover: build script, Pico/laptop code, deploy + tests
tech_setup_check/ Windows 11 install/setup guides, plus hand-maintained git/Python/SSH notes
explainers/       Standalone "why does it work that way" deep-dive docs
handouts/         Printable per-class handouts and single-file HTML summaries/slide decks
communications/   Marketing copy, registration info (may contain PII — treat as sensitive)
src/              Laptop-side code + rover tuning material: wireframe/ (uv project, Class 4 3D viewer), rover/ (tuning log)
expenses/         Purchase receipts (gitignored, local only) — not course content
```

Each directory has its own README with details:

- [`input/`][08] — `my-vision.md` (source of truth) and `my-prompts.md` (prompt log)
- [`methodology/`][09] — course terminology and the authoring methodology behind this repo
- [`lesson_plans/`][06] — syllabus, lesson plans, BOM
- [`lesson_scripts/`][07] — student walkthroughs
- [`full_build/`][10] — deploy (`uv run deploy.py rover`), tools, and on-device/system tests
- [`tech_setup_check/`][01] — setup guides
- [`explainers/`][11] — deep-dive explainers and future topics
- [`handouts/`][12] — handouts and reference links
- [`communications/`][13] — course description and kick-off message
- [`src/`][14] — laptop-side code; see also [`src/wireframe/`][15]


## How This Repository Is Generated

`input/my-vision.md` is the seed document: course description, class-by-class outline, bill of
materials, and the map of what gets generated from it. Everything else — syllabus, lesson plans,
install guides, BOM, explainers — is generated *from* that file via Claude Code skills, so when
the vision changes, regenerate/reconcile the downstream docs rather than hand-editing them out of
sync.

| Document | Skill | Output |
| --- | --- | --- |
| Syllabus | `/syllabus_generator` | `lesson_plans/syllabus-*.md` |
| Lesson Plan | `/lesson_plan_generator` | `lesson_plans/class-0X-lesson-plan.md` |
| Lesson Script | ad-hoc (see `input/my-prompts.md`) | `lesson_scripts/class-NN-lesson-script.md` |
| Install Instructions | `/teen-install-instructions` | `tech_setup_check/*.md` |
| Bill of Materials | `/bill_of_materials_generator` | `lesson_plans/BOM.md` |
| Explainer | `/explainer` | `explainers/*.md` |
| README | `/readme_generator` | `README.md` + per-directory `README.md` |

The skills live in `.claude/skills/`. See [`CLAUDE.md`][16] for the full generation pipeline and
conventions (markdown linting, link style, export via pandoc, etc.) that apply when regenerating
any of these.


## Safety Notes

Class 3 onward puts a 9V battery on the breadboard, feeding motors through the DRV8833. Check
polarity before you connect it, and pull the battery any time you're rewiring — a live H-bridge
is not something you want to probe with a screwdriver.

Class 3 is the one soldering step: students solder Dupont leads onto the chassis motors and on/off
switch, supervised, at Makersmiths' soldering stations — iron back in its stand, safety glasses on,
fume extractor running. Every other connection in the course lives on the breadboard, which rides
on the chassis from Class 3 on.


## Status and Support

Active course development — materials for all seven sessions exist and are still being refined
and reconciled against `input/my-vision.md`. Report problems or suggest changes via
[GitHub issues][17].


## Credits and License

Makersmiths. No license file present in this repo.


[01]:tech_setup_check/README.md
[02]:lesson_plans/BOM.md
[03]:lesson_scripts/class-00-lesson-script.md
[04]:full_build/full-build-script.md
[05]:lesson_plans/syllabus-physical-computing-for-beginners.md
[06]:lesson_plans/README.md
[07]:lesson_scripts/README.md
[08]:input/README.md
[09]:methodology/README.md
[10]:full_build/README.md
[11]:explainers/README.md
[12]:handouts/README.md
[13]:communications/README.md
[14]:src/README.md
[15]:src/wireframe/README.md
[16]:CLAUDE.md
[17]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/issues
