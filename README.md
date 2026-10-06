# Physical Computing for Beginners

*A Makersmiths hands-on class.*

No prior coding required. Students wire up sensors, motors, and a microcontroller, then teach
them to talk to each other. Six two-hour classes plus a Pre-Class stack up to one capstone: the
Random Rover, a robot car that scans its surroundings and steers itself clear of whatever's in
the way.


## Table of Contents
- [Overview][01]
- [What You'll Build][02]
- [Course Structure][03]
- [Getting Started][04]
- [Repository Layout][05]
- [How This Repository Is Generated][06]
- [Safety Notes][07]
- [Status and Support][08]
- [Credits and License][09]


## Overview

| | |
| :--- | :---- |
| **Audience** | Middle/high schoolers; no prior Python/CircuitPython experience required |
| **Format** | 1 Pre-Class + 6 Classes, 2 hours each, at Makersmiths' Electronics room |
| **Capstone project** | The Random Rover — an obstacle-avoiding robot car |
| **Hardware** | Raspberry Pi Pico 2 W, pushbutton + KY-040 rotary encoder, HC-SR04 ultrasonic sensor, SG90 servo, DRV8833 dual H-bridge driver, 9V battery + 5V buck converter, IR optocoupler wheel-speed sensors, LSM9DS1 IMU, limit switch + IR obstacle sensor, 1.14" ST7789 TFT display |
| **Software** | CircuitPython on the Pico (edited in Mu or Thonny); laptop-side Python run with `uv` for the Class 4 3D orientation viewer and the full-build deploy/test/calibration scripts |


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
the heading and collision-avoidance state are posted live to the rover website. Class 6 finishes
the Rover and opens up stretch goals: encoder-based speed control, a rolling-history chart added
to the already-running rover website, and a TFT status display.

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
[syllabus][10] is the authoritative class-by-class outline; this table is a summary.


## Getting Started

**Prerequisites:** a Windows 11 laptop with a USB port and admin rights (the setup guides are
Windows 11 only — no Linux/macOS student guides yet; the full-build scripts also run on Linux and
macOS), a Raspberry Pi Pico 2 W with a data-capable USB cable, and the kit from the
[bill of materials][11].

**Students**, in this order:

1. Before Pre-Class, work through the [setup guides][12]: [check for Windows 11 + WSL][13],
    [install WSL][14] if needed, [install Python][15], then the
    [CircuitPython dev environment][16].
2. Pre-Class: flash CircuitPython and get the onboard LED blinking, following
    [the Pre-Class lesson script][17].
3. Each class: follow that class's walkthrough in [`lesson_scripts/`][18]. Dip into
    [`explainers/`][19] whenever you want the "why" behind something.
4. Before Class 4, do the [wireframe install guide][20]. It downloads `wireframe.py` on its own,
    so run the 3D orientation viewer from the folder the guide put it in (optional serial port
    argument, e.g. `COM5` or `/dev/ttyACM0`):

    ```bash
    uv run wireframe.py
    ```

    From a clone of this repo, run `uv run lesson_scripts/wireframe.py` instead.

5. After the course, tune your rover with the
    [tuning and calibration explainer][21] (also folded into section 8 of the full build script).

**Instructors:** start from the [syllabus][10], then the [BOM][11] for ordering, then the
per-class lesson plans in [`lesson_plans/`][22]. Handouts and slide decks for some classes are in
[`handouts/`][23].

**Rebuilding or building a second rover?** The [full build script][24] builds the finished Random
Rover (Classes 1-6 plus all three stretch goals) in one session, then tests and tunes it. Keep the
rover on its stand when deploying — it starts driving as soon as `code.py` lands:

```bash
cd full_build
uv run deploy.py rover                  # install libraries + rover code onto CIRCUITPY
uv run deploy.py test                   # part-by-part device test on the Pico
uv run deploy.py restore                # put the rover code.py back
uv run test/system_test.py              # whole-rover test from the laptop (exit 0 = pass)
uv run deploy.py tool mag_calibration   # also: servo_check, motor_check
```

See the [`full_build/` README][25] for the test-laptop setup scripts and the rest of the commands.


## Repository Layout

```text
input/            Source of truth: my-vision.md (seed doc) + my-prompts.md (prompt log)
methodology/      Background notes: course terms, Spec-Kit vs. Script methodology, 2026-10-04 prompt audit (not generated)
lesson_plans/     Instructor-facing syllabus, BOM, and per-class lesson plans (class-00 .. class-06)
lesson_scripts/   Student-facing build+code walkthroughs (class-00 .. class-06), plus wireframe.py (Class 4 laptop 3D viewer)
full_build/       One-session build of the finished rover: full-build-script.md (build, test, tune/calibrate),
                  src/pico rover code, src/tools calibration scripts, src/laptop WiFi viewer, deploy.py,
                  test-laptop setup scripts, device/system tests
tech_setup_check/ Windows 11 install/setup guides, plus hand-maintained git/Python-venv/SSH notes and setup-github.sh
explainers/       Standalone "why does it work that way" deep dives (Pico pinout, IMU/Mahony, quaternions, tuning, ...)
handouts/         Per-class markdown handouts, single-file HTML slide decks, reference links
communications/   Course marketing copy and announcements (not course content)
expenses/         Purchase receipts (not course content; gitignored, local only)
.claude/skills/   Claude Code skills that generate the course docs
CLAUDE.md         Generation pipeline and repo conventions
```

Each directory has its own README with the details:

- [`input/`][26] — seed document and prompt log
- [`methodology/`][27] — course terminology, authoring methodology, prompt audit
- [`lesson_plans/`][22] — syllabus, lesson plans, BOM
- [`lesson_scripts/`][18] — student walkthroughs and `wireframe.py`
- [`full_build/`][25] — deploy, calibration tools, and on-device/system tests
- [`tech_setup_check/`][12] — setup guides and helpers
- [`explainers/`][19] — deep-dive explainers and future topics
- [`handouts/`][23] — handouts, slide decks, and reference links
- [`communications/`][28] — course description and announcements


## How This Repository Is Generated

`input/my-vision.md` is the seed document: course description, class-by-class outline, bill of
materials, and the map of what gets generated from it. Everything else — syllabus, lesson plans,
install guides, BOM, explainers — is generated *from* that file via Claude Code skills, so when
the vision changes, regenerate/reconcile the downstream docs rather than hand-editing them out of
sync. Check `input/my-prompts.md` first to see the exact prompt that produced the current version.

| Document | Skill | Output |
| --- | --- | --- |
| Syllabus | `/syllabus_generator` | `lesson_plans/syllabus-*.md` |
| Lesson Plan | `/lesson_plan_generator` | `lesson_plans/class-0X-lesson-plan.md` |
| Lesson Script | ad-hoc (see `input/my-prompts.md`) | `lesson_scripts/class-NN-lesson-script.md` |
| Install Instructions | `/teen-install-instructions` | `tech_setup_check/*.md` |
| Bill of Materials | `/bill_of_materials_generator` | `lesson_plans/BOM.md` |
| Explainer | `/explainer` | `explainers/*.md` |
| Slide Deck | `/html_slide_deck` | `handouts/*-summary.html` |
| README | `/readme_generator` | `README.md` + per-directory `README.md` |

The skills live in `.claude/skills/`. See [`CLAUDE.md`][29] for the full generation pipeline and
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

From Class 5 on, the rover drives itself the moment `code.py` is saved. Keep it on a stand (wheels
off the table) whenever you deploy code or edit files on `CIRCUITPY`.


## Status and Support

Active course development — materials for all seven sessions, the full build, and the tuning
guide exist and are still being refined and reconciled against `input/my-vision.md`. Report
problems or suggest changes via [GitHub issues][30] on the
[project repository][31].


## Credits and License

Makersmiths. No LICENSE file is present in this repo, so no open-source license has been granted;
ask via [GitHub issues][30] before reusing the material.


[01]:#overview
[02]:#what-youll-build
[03]:#course-structure
[04]:#getting-started
[05]:#repository-layout
[06]:#how-this-repository-is-generated
[07]:#safety-notes
[08]:#status-and-support
[09]:#credits-and-license
[10]:lesson_plans/syllabus-physical-computing-for-beginners.md
[11]:lesson_plans/BOM.md
[12]:tech_setup_check/README.md
[13]:tech_setup_check/check-for-windows-11-and-wsl.md
[14]:tech_setup_check/install-wsl-on-windows-11.md
[15]:tech_setup_check/install-python-on-windows-11.md
[16]:tech_setup_check/install-circuitpython-dev-env-on-windows-11.md
[17]:lesson_scripts/class-00-lesson-script.md
[18]:lesson_scripts/README.md
[19]:explainers/README.md
[20]:tech_setup_check/install-wireframe-on-windows-11.md
[21]:explainers/strategy-for-tuning-calibration-random-rover.md
[22]:lesson_plans/README.md
[23]:handouts/README.md
[24]:full_build/full-build-script.md
[25]:full_build/README.md
[26]:input/README.md
[27]:methodology/README.md
[28]:communications/README.md
[29]:CLAUDE.md
[30]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/issues
[31]:https://github.com/jeffskinnerbox/physical_computing_for_beginners
