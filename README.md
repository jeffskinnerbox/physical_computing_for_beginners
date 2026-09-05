
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
- [Credits and License](#credits-and-license)

## Overview

| | |
| :--- | :---- |
| **Audience** | Middle/high schoolers; no prior Python/CircuitPython experience required |
| **Format** | 1 Pre-Class + 6 Classes, 2 hours each, at Makersmiths' Electronics room |
| **Capstone project** | The Random Rover — an obstacle-avoiding robot car |
| **Hardware** | Raspberry Pi Pico 2 W, HC-SR04 ultrasonic sensor, SG90 servo, DRV8833 dual H-bridge driver, IR optocoupler wheel-speed sensors, LSM9DS1 IMU |
| **Software** | CircuitPython |


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
forward, checks what's ahead, and steers itself clear of anything in the way — with its
collision-avoidance state also posted live to the rover website. Class 6 finishes the Rover and
opens up stretch goals: encoder-based speed control, a rolling-history chart added to the
already-running rover website, and a TFT status display.

Nothing gets rewired mid-course. GPIO pins are assigned up front so a circuit built in Class 1
is still live and working by Class 6.


## Course Structure

| Class | Focus | New Hardware/Concept |
| --- | --- | --- |
| Pre-Class | Laptop + board bring-up | Flash CircuitPython, serial console, blink + heartbeat |
| Class 1 | Push button + rotary encoder | Debounced digital input |
| Class 2 | Ultrasonic distance sensor + servo | HC-SR04, SG90 servo, PWM |
| Class 3 | Dual H-bridge motor driver | DRV8833, two DC motors, 9V battery (`VM`); wheel odometry (IR optocoupler) and the first version of the rover status website |
| Class 4 | Inertial measurement unit | LSM9DS1 (9-DOF), I2C, Mahony filter; orientation added to the rover website |
| Class 5 | Random Rover | Sensor + servo + motor driver combined for collision avoidance; scan/heading/stop telemetry added to the rover website |
| Class 6 | Finish the Rover | Stretch goals: encoder speed control, rolling-history chart added to the rover website, TFT display |

Wiring/pin assignments are chosen so each class's circuit keeps working after later classes add
to it — nothing gets rewired mid-course.


## Getting Started

1. Work through the setup guide for your platform in [`tech_setup_check/`][01] before Pre-Class.
2. Gather materials from the [bill of materials][02].
3. Flash CircuitPython to the Pico 2 W and get the onboard LED blinking — that's the Pre-Class
   build, walked through in [`lesson_scripts/class-00-lesson-script.md`][03].


## Repository Layout

```text
input/            Source-of-truth vision doc + prompt log — everything else is generated from this
lesson_plans/     Instructor-facing syllabus + per-class lesson plans, BOM
lesson_scripts/   Student-facing build+code walkthroughs, one per class
tech_setup_check/ Install/setup instructions per environment
explainers/       Standalone "why does it work that way" deep-dive docs
handouts/         Printable per-class handouts
communications/   Marketing copy, registration info (may contain PII — treat as sensitive)
expenses/         Purchase receipts (photos, receipts/ subdir) — no established doc conventions yet
```


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

See `CLAUDE.md` for the full generation pipeline and conventions (markdown linting, link style,
export via pandoc, etc.) that apply when regenerating any of these.


## Safety Notes

Class 3 onward puts a 9V battery on the breadboard, feeding motors through the DRV8833. Check
polarity before you connect it, and pull the battery any time you're rewiring — a live H-bridge
is not something you want to probe with a screwdriver. There's no soldering anywhere in this
course; everything lives on a breadboard.


## Credits and License

Makersmiths. No license file present in this repo.


[01]:tech_setup_check/README.md
[02]:lesson_plans/BOM.md
[03]:lesson_scripts/class-00-lesson-script.md
</content>
