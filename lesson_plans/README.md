# README

Generated, instructor-facing course documents for Physical Computing for Beginners: the syllabus,
the bill of materials, and one lesson plan per class (Pre-Class through Class 6).


## Usage

See the root [README][01] for the full course documentation map, and the project's `CLAUDE.md`
for the generation pipeline behind it. Every file here is generated *from* `input/my-vision.md` via a dedicated skill
(`/syllabus_generator`, `/lesson_plan_generator`, `/bill_of_materials_generator`) and must stay
consistent with it and with each other — when `my-vision.md` changes, these docs need to be
regenerated or reconciled, not hand-edited out of sync. Lesson plans must follow the class outline
fixed in the syllabus and flow class-to-class with minimal repetition; regenerate them one class at
a time, stopping for review, rather than all at once. The BOM is the single source of truth for all
cost and sourcing information — the syllabus and lesson plans reference component names but never
prices.


## Build Process

No build process — this directory holds static markdown source files. `syllabus-physical-
computing-for-beginners-Aug-16.docx` is a dated pandoc export of the syllabus
(`pandoc -f gfm input.md -o output.docx`) kept for sharing/printing, not an authored source in its
own right. Per this user's file-change convention, editing a `.md` file here also writes/updates a
matching `.md.bak` mechanical backup alongside it; none currently exist because these files haven't
been hand-edited since being generated.


## Contents

| Topic | File/Directory Name | Description/Summary |
| :------ | :---------- | :------------ |
| Course syllabus | `syllabus-physical-computing-for-beginners.md` | Course description, schedule, audience, and class-by-class outline for the 1 Pre-Class + 6 Class series, generated via `/syllabus_generator`. |
| Bill of materials | `BOM.md` | Single source of truth for cost and sourcing: per-student required/optional hardware, shared supplies, shipping, software, code blocks, and tools, with full cost math. |
| Pre-Class lesson plan | `class-00-lesson-plan.md` | Toolchain setup: install Mu/Thonny, flash CircuitPython onto the Pico 2 W, download the library bundle, and run a first blink+heartbeat program. No wiring yet. |
| Class 1 lesson plan | `class-01-lesson-plan.md` | Pushbutton switch and KY-040 rotary encoder wired to two LEDs; deliberately builds without debouncing first, then adds it, so students see the exact problem it solves. |
| Class 2 lesson plan | `class-02-lesson-plan.md` | HC-SR04 ultrasonic distance sensor and SG90 servo, combined into a sensor-on-servo sweep that previews the Random Rover's scanning behavior. |
| Class 3 lesson plan | `class-03-lesson-plan.md` | DRV8833 dual H-bridge motor driver and DC gearbox motors; students attempt open-loop square/circle driving and directly experience dead-reckoning drift. Also introduces wheel odometry (IR optocoupler per wheel) and the first version of a Pico-hosted rover status website, both extended in every class that follows. |
| Class 4 lesson plan | `class-04-lesson-plan.md` | LSM9DS1 9-DOF IMU read over I2C; raw accelerometer/gyroscope readings are fused with a Mahony filter into stable roll/pitch/yaw, streamed to a live 3D viewer. |
| Class 5 lesson plan | `class-05-lesson-plan.md` | Combines Class 2's sensor/servo sweep and Class 3's motor driver into the autonomous Random Rover, plus two new fixed safety sensors (limit switch, IR). |
| Class 6 lesson plan | `class-06-lesson-plan.md` | Finishes and tunes the Random Rover, then offers three optional stretch goals reconnecting earlier circuits: encoder speed control, a rolling-history chart added to the rover status website running since Class 3, and a TFT status display. |


[01]:../README.md
