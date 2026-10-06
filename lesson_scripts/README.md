# README

Student-facing, detailed build+code walkthroughs for Physical Computing for Beginners: one lesson
script per class (Pre-Class through Class 6), each explanatory text plus fully-commented
CircuitPython built up in phases, with the complete final code listed at the end. This is the
folder students work from in every class. Also here: `wireframe.py`, the Class 4 laptop-side 3D
orientation viewer.


## Contents

| Topic | File | Description/Summary |
| :------ | :---------- | :------------ |
| Pre-Class lesson script | [`class-00-lesson-script.md`][01] | Prepare your laptop and Pico: flash CircuitPython onto the Pico 2 W, install Mu/Thonny, download the library bundle, and write a first blink+heartbeat program. No wiring yet. |
| Class 1 lesson script | [`class-01-lesson-script.md`][02] | Pushbutton and KY-040 rotary encoder wired to two LEDs. Phase 1 shows the bounce; Phase 2 fixes it with debouncing. |
| Class 2 lesson script | [`class-02-lesson-script.md`][03] | HC-SR04 ultrasonic sensor and SG90 servo, each run alone (Phases 1-2), then combined into a sweep-and-report that previews the Random Rover's scan (Phase 3). |
| Class 3 lesson script | [`class-03-lesson-script.md`][04] | DRV8833 dual H-bridge motor driver library and test (Phase 1), open-loop square/circle and dead-reckoning drift (Phase 2), wheel odometry with an IR optocoupler per wheel (Phase 3), the first rover status website (Phase 4), drive straight with wheel feedback (Phase 5), and a homework Phase 6 tuning `KI`/`MAX_TRIM` by experiment. |
| Class 4 lesson script | [`class-04-lesson-script.md`][05] | LSM9DS1 9-DOF IMU over I2C: read and fuse roll/pitch/yaw with a Mahony filter (Phase 1), live 3D view on the laptop with `wireframe.py` (Phase 2), gyro bias calibration against yaw drift (Phase 3), and orientation added to the rover status website (Phase 4). |
| Class 5 lesson script | [`class-05-lesson-script.md`][06] | The Random Rover: limit switch + IR safety sensors and magnetometer calibration (Phase 1), `rover_server.py` upgraded to a 9-DOF filter with compass heading and a library mode (Phase 2), then the collision-avoidance rover with compass-steered turns and live telemetry (compass heading, scan heading, drive state, stop reason) on the rover website (Phase 3). |
| Class 6 lesson script | [`class-06-lesson-script.md`][07] | Tune the core rover, then three optional stretch goals: live encoder speed control, a rolling-history chart on the rover website, and an on-board TFT status display. |
| Class 4 3D viewer | [`wireframe.py`][08] | Laptop-side program (not for the Pico): reads roll/pitch/yaw CSV over USB serial and draws a live 3D box. Canonical copy embedded in `class-04-lesson-script.md`. |


## Purpose / Role in Repository

These are the student's side of the course; the root [README][09] sends students here for each
class. Lesson scripts are distinct from the instructor-facing lesson plans in
[`lesson_plans/`][10]: the lesson plan is the teaching guide an instructor works from, the lesson
script the walkthrough a student can follow on their own. Neither is generated from the other via
a dedicated skill — scripts are written ad-hoc (see "My 8th Prompt" in `input/my-prompts.md`) but
must stay consistent with the class outline fixed in the [syllabus][11] and with the lesson plans,
flowing class-to-class with minimal repetition.

Two places hold copies of code from these scripts as real files, and must be kept in sync when a
script's code changes:

- [`wireframe.py`][08] here — the Class 4 viewer. Its canonical copy is in
    `class-04-lesson-script.md` (Phase 2 and the final listing); keep all three identical.
- The rover files in [`full_build/src/pico/`][12] — copied unchanged from the Class 3/5/6 scripts,
    plus full-build-only glue. For example, the `poll_website()` `BrokenPipeError` guard lives in
    both `class-5-code.py` and `full_build/src/pico/code.py`.

Already finished the course, or rebuilding a rover? [`full_build/`][13] builds the finished Random
Rover (Classes 1-6 plus all three stretch goals) in one session, reusing this folder's code, and
the [tuning and calibration explainer][14] is the next stop after Class 6.


## Usage

Open the script for your class and work through it top to bottom; the Pico-side code runs on the
board from Mu or Thonny. For Class 4, first do the [wireframe install guide][15]. It downloads
`wireframe.py` on its own, so run the viewer from the folder the guide put it in (optional serial
port argument, e.g. `COM5` or `/dev/ttyACM0`):

```bash
uv run wireframe.py
```

From a clone of this repo, run `uv run lesson_scripts/wireframe.py` instead.

Students download `wireframe.py` from GitHub via that install guide, so don't move or rename it
without updating the guide's URL.


## Notes

- Each "Build It: Phase N" section has a fixed subsection order — Wiring for this phase → Software
    for this phase (a table of component | new / modified / unchanged + its `class-xx-phase-x-*.py`
    id | what it does) → What this code does → The code → Try it / what you should see →
    Checkpoint. Keep that order, and keep the Software table in sync whenever a phase's code
    changes.
- Regenerate/reconcile scripts one class at a time, stopping for review, rather than all at once.
- GPIO pin assignments don't overlap across classes, so earlier circuits keep working; the one
    rewiring is Class 5's `VBUS`-to-`VSYS` power move. The rover status website (Classes 3-6) runs
    at `http://192.168.4.1:5000` — port 5000, not 80.
- From Class 5 on, the rover drives the moment `code.py` is saved — keep it on a stand.
- Editing a script here also writes a matching `.md.bak` backup alongside it; `.bak` files are
    throwaway and gitignored.
- Related: [`explainers/`][16] for the "why" behind a concept, [`handouts/`][17] for class summaries
    and slide decks, [`tech_setup_check/`][18] for setup guides, and [`CLAUDE.md`][19] for repo
    conventions.


[01]:class-00-lesson-script.md
[02]:class-01-lesson-script.md
[03]:class-02-lesson-script.md
[04]:class-03-lesson-script.md
[05]:class-04-lesson-script.md
[06]:class-05-lesson-script.md
[07]:class-06-lesson-script.md
[08]:wireframe.py
[09]:../README.md
[10]:../lesson_plans/README.md
[11]:../lesson_plans/syllabus-physical-computing-for-beginners.md
[12]:../full_build/src/pico/
[13]:../full_build/README.md
[14]:../explainers/strategy-for-tuning-calibration-random-rover.md
[15]:../tech_setup_check/install-wireframe-on-windows-11.md
[16]:../explainers/README.md
[17]:../handouts/README.md
[18]:../tech_setup_check/README.md
[19]:../CLAUDE.md
