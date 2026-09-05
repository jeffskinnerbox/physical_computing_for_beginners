# README

Student-facing, detailed build+code walkthroughs for Physical Computing for Beginners: one lesson
script per class (Pre-Class through Class 6), each explanatory text plus fully-commented
CircuitPython built up in phases, with the complete final code listed at the end.


## Usage

See the root [README][01] for the full course documentation map, and the project's `CLAUDE.md`
for the generation pipeline behind it. Lesson scripts are distinct from the instructor-facing lesson plans in
`lesson_plans/`: the lesson plan is the teaching guide an instructor works from, while the lesson
script is the detailed, student-readable walkthrough a student can follow on their own. Neither is
generated from the other via a dedicated skill — they're written ad-hoc (see "My 8th Prompt" in
`input/my-prompts.md`) but must stay consistent with the class outline fixed in the syllabus and
with each other, flowing class-to-class with minimal repetition. Regenerate/reconcile them one
class at a time, stopping for review, rather than all six at once.


## Build Process

No build process — this directory holds static markdown source files plus the CircuitPython code
they walk through inline as fenced code blocks (no standalone `.py` files). Per this user's
file-change convention, editing a script here also writes/updates a matching `.md.bak` mechanical
backup (e.g. `class-00-lesson-script.md.bak`); none currently exist because these files haven't
been hand-edited since being generated.


## Contents

| Topic | File/Directory Name | Description/Summary |
| :------ | :---------- | :------------ |
| Pre-Class lesson script | `class-00-lesson-script.md` | Walkthrough for flashing CircuitPython onto the Pico 2 W, installing Mu/Thonny, downloading the library bundle, and writing a first blink+heartbeat program. No wiring yet. |
| Class 1 lesson script | `class-01-lesson-script.md` | Walkthrough for wiring a pushbutton and KY-040 rotary encoder to two LEDs; builds without debouncing first so the reader sees the raw problem, then adds it. |
| Class 2 lesson script | `class-02-lesson-script.md` | Walkthrough for an HC-SR04 ultrasonic sensor and SG90 servo, built separately then combined into a sensor-on-servo sweep that previews the Random Rover's scan behavior. |
| Class 3 lesson script | `class-03-lesson-script.md` | Walkthrough for a DRV8833 dual H-bridge motor driver and DC gearbox motors; the reader attempts open-loop square/circle driving and experiences dead-reckoning drift firsthand. Also introduces wheel odometry (an IR optocoupler per wheel) and the first version of a Pico-hosted rover status website. |
| Class 4 lesson script | `class-04-lesson-script.md` | Walkthrough for the LSM9DS1 9-DOF IMU over I2C; fuses raw accelerometer/gyroscope data into stable roll/pitch/yaw with a Mahony filter, streamed to a live 3D viewer and added to the rover status website running since Class 3. |
| Class 5 lesson script | `class-05-lesson-script.md` | Walkthrough for combining the Class 2 sensor/servo sweep and Class 3 motor driver into the autonomous Random Rover, with two new fixed safety sensors. Also refactors the rover status website into a library so the collision-avoidance program can drive and serve live telemetry (scan heading, drive state, stop reason) at the same time. |
| Class 6 lesson script | `class-06-lesson-script.md` | Walkthrough for finishing/tuning the Random Rover, then three optional stretch goals: encoder speed control, a rolling-history chart added to the rover status website running since Class 3, and a TFT status display. |


[01]:../README.md
