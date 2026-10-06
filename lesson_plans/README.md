# README

Generated, instructor-facing course documents for Physical Computing for Beginners: the syllabus,
the bill of materials, and one lesson plan per class (Pre-Class through Class 6). Students follow
the matching student-facing walkthroughs in [`lesson_scripts/`][01] instead.


## Contents

| Topic | File | Description/Summary |
| :------ | :---------- | :------------ |
| Course syllabus | [`syllabus-physical-computing-for-beginners.md`][02] | The authoritative class-by-class outline: course description, learning objectives, prerequisites, technology requirements, course structure and format, lessons breakdown, supplemental studies, and assignments for the 1 Pre-Class + 6 Class series. Generated via `/syllabus_generator`. |
| Bill of materials | [`BOM.md`][03] | Single source of truth for cost and sourcing: per-student hardware, software, code blocks, and tools, with full cost math, plus an appendix of parts considered but not selected. Generated via `/bill_of_materials_generator`. |
| Pre-Class lesson plan | [`class-00-lesson-plan.md`][04] | Toolchain setup: install Mu/Thonny, flash CircuitPython onto the Pico 2 W, download the library bundle, and run a first blink+heartbeat program. No wiring yet. |
| Class 1 lesson plan | [`class-01-lesson-plan.md`][05] | Pushbutton switch and KY-040 rotary encoder wired to two LEDs; deliberately builds without debouncing first, then adds it, so students see the exact problem it solves. |
| Class 2 lesson plan | [`class-02-lesson-plan.md`][06] | HC-SR04 ultrasonic distance sensor and SG90 servo, combined into a sensor-on-servo sweep that previews the Random Rover's scanning behavior. |
| Class 3 lesson plan | [`class-03-lesson-plan.md`][07] | DRV8833 dual H-bridge motor driver and DC gearbox motors; students attempt open-loop square/circle driving and directly experience dead-reckoning drift. Also introduces wheel odometry (an IR optocoupler per wheel) and the first version of the Pico-hosted rover status website, both extended in every class that follows. |
| Class 4 lesson plan | [`class-04-lesson-plan.md`][08] | LSM9DS1 9-DOF IMU read over I2C; raw accelerometer/gyroscope readings fused with a Mahony filter into stable roll/pitch/yaw, streamed to a live 3D viewer and added to the rover status website running since Class 3. |
| Class 5 lesson plan | [`class-05-lesson-plan.md`][09] | Combines Class 2's sensor/servo sweep and Class 3's motor driver into the autonomous Random Rover, plus two new fixed safety sensors (limit switch, IR obstacle sensor); calibrates and fuses the IMU's magnetometer so a compass heading steers closed-loop turns. Refactors the rover status website into a library so the collision-avoidance program can drive and serve live telemetry (compass heading, scan heading, drive state, stop trigger) at the same time. |
| Class 6 lesson plan | [`class-06-lesson-plan.md`][10] | Finishes and tunes the Random Rover, then offers three optional stretch goals reconnecting earlier circuits: encoder speed control, a rolling-history chart added to the rover status website, and a TFT status display. |


## Purpose / Role in Repository

These are the instructor's side of the course; the root [README][11] points instructors here after
the syllabus and BOM. Every file is generated *from* [`input/my-vision.md`][12] via a dedicated
skill (`/syllabus_generator`, `/lesson_plan_generator`, `/bill_of_materials_generator`) and must
stay consistent with it and with each other — when `my-vision.md` changes, regenerate or reconcile
these docs rather than hand-editing them out of sync. Check `input/my-prompts.md` for the prompt
that produced the current version; see [`CLAUDE.md`][13] for the full generation pipeline.

- The **syllabus** fixes the class outline; lesson plans follow it, and the root README's course
    table is only a summary of it.
- The **BOM** is the single source of truth for all cost and sourcing information — the syllabus
    and lesson plans name components but never prices.
- **Lesson plans** flow class-to-class with minimal repetition. Each embeds its class's
    `class-N-code-*.py` code inline as fenced code blocks; there are no standalone `.py` files here.
- The student-facing [lesson scripts][01] cover the same classes and must stay consistent with these
    plans.


## Usage

Instructors: read the syllabus, then the BOM for ordering, then each class's lesson plan before
teaching it. Each lesson plan covers overview, learning goals, preparation checklist, materials,
a class timeline, troubleshooting, age differentiation, assessment, instructor tips, and
resources.

Nothing to build — these are static markdown files. To share or print one, export it with pandoc;
no exported copy is kept in the repo, since it goes stale as the `.md` changes:

```bash
pandoc -f gfm syllabus-physical-computing-for-beginners.md -o syllabus-physical-computing-for-beginners.docx
```


## Notes

- Regenerate lesson plans one class at a time, stopping for review, rather than all seven at once.
- GPIO pin assignments are deliberately non-overlapping across classes so earlier circuits keep
    working; preserve that when editing class code or wiring.
- The rover status website (Classes 3-6) runs at `http://192.168.4.1:5000` — port 5000, not 80.
- Editing a file here also writes a matching `.md.bak` backup alongside it; `.bak` files are
    throwaway and gitignored.
- Related: [`lesson_scripts/`][01], [`handouts/`][14] (class summaries and slide decks),
    [`explainers/`][15] (background deep dives).


[01]:../lesson_scripts/README.md
[02]:syllabus-physical-computing-for-beginners.md
[03]:BOM.md
[04]:class-00-lesson-plan.md
[05]:class-01-lesson-plan.md
[06]:class-02-lesson-plan.md
[07]:class-03-lesson-plan.md
[08]:class-04-lesson-plan.md
[09]:class-05-lesson-plan.md
[10]:class-06-lesson-plan.md
[11]:../README.md
[12]:../input/my-vision.md
[13]:../CLAUDE.md
[14]:../handouts/README.md
[15]:../explainers/README.md
