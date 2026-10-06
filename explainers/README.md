# README

This folder is where the "why does it work that way?" questions live. A lesson script or lesson
plan can't stop to explain, say, the whole history of the microcontroller every time it mentions
one — that would bury the actual build instructions. So whenever a concept in the course is worth
a real explanation rather than a one-line aside, it gets pulled out into its own document here,
written in plain English for a middle/high-school reader. Each one is generated with the
`/explainer` skill, which favors a narrative structure — status quo, then the problem, then the
solution — over a dry glossary-style definition, so a student reads it more like a short story
about *why* something was invented than a spec sheet about *what* it is.


## Contents

| Topic | File | Description/Summary |
| :------ | :---------- | :------------ |
| The Random Rover | [`what-is-the-random-rover.md`][01] | What kind of robot the course's capstone is, why obstacle-avoiding rovers are a common first robotics build, and how its sense-decide-act loop compares to a Roomba and to more advanced autonomous machines. |
| Microprocessors vs. microcontrollers | [`microprocessor-vs-microcontroller.md`][02] | The historical split between microprocessors (Intel 4004) and microcontrollers (TI TMS 1000), what distinguishes them, and why the Pico 2 W's RP2350 microcontroller is the right chip for this course. |
| MicroPython vs. CircuitPython | [`micropython-vs-circuitpython.md`][03] | The two Python variants used on microcontrollers — shared origins, where they diverge (upload workflow, libraries, governance), and why this course picks CircuitPython. Also contrasts both with C/C++. |
| What is a pinout? | [`raspberry-pi-pico-2w-pinout.md`][04] | What a pinout is, what it's used for, how it's communicated (silkscreen, diagrams, tables, datasheets), where to find the Pico 2 W's (pinout.xyz), and how to find one for any other device. |
| Types of pins on the Pico 2 W | [`types-of-pins-on-raspberry-pi-pico-2w.md`][05] | Every non-`GPnn` pin label on the Pico 2 W pinout — `GND`, `VBUS`, `VSYS`, `3V3 EN`, `3V3 OUT`, `ADC VREF`, `ADC GND`, `GP26 A0`/`GP27 A1`/`GP28 A2`, `RUN` — what each is for, how it behaves electrically, and how (or whether) it's reached from CircuitPython. |
| Breadboards and Dupont wires | [`what-are-breadboards-and-dupont-wires.md`][06] | Where the names come from, why breadboards are used, board sizes and tie-point layout (center channel, power rails, rows), jumper wire lengths/terminals/colors, substituting solid 22 AWG wire, and when not to use either. |
| Serial communication (SPI, I2C, UART) | [`spi-i2c-uart-serial-communications.md`][07] | What serial communication is and why microcontrollers depend on it, then UART, I2C, and SPI — what each moves and how, and how to reach each from CircuitPython on the Pico 2 W (including the course's LSM9DS1 over I2C and the Class 6 TFT over SPI). |
| Glossary of terms for microcontrollers | [`glossary-of-terms-for-microcontrollers.md`][08] | Quick-lookup, topic-grouped definitions for MCU jargon: the chip (MCU, CPU, register), memory (RAM, SRAM, Flash, EEPROM, NVM), I/O (GPIO, pull-up/pull-down, ADC, DAC, PWM), serial protocols, event handling (interrupt, ISR, timers, DMA, RTOS), and startup/safety/power (firmware, watchdog, brown-out, sleep modes). |
| IMUs and the Mahony filter (series part 1 of 3) | [`what-is-an-imu-and-mahony-filter.md`][09] | What an IMU is (gyroscope, accelerometer, magnetometer — the course's 9-DOF LSM9DS1), why raw readings are rates and directions rather than angles, how the Class 4 Mahony filter fuses them (and what `MAHONY_KP`/`MAHONY_KI` do), and how Mahony compares to complementary, Madgwick, Kalman, and Extended Kalman filters. |
| Gimbal lock (series part 2 of 3) | [`what-is-gimbal-lock.md`][10] | Euler angles (roll/pitch/yaw), how gimbal lock loses a degree of freedom in physical gimbals and in software, the Apollo story ("a fourth gimbal for Christmas," Apollo 13), why NASA didn't add a fourth gimbal or use quaternions, and where gimbal lock still bites today. |
| Quaternions (series part 3 of 3) | [`what-are-quaternion-and-why-use-them.md`][11] | What quaternions are, Hamilton's 1843 Broom Bridge invention and their comeback in graphics/aerospace/robotics, and why the Class 4 Mahony filter stores orientation as a quaternion (`q0..q3`) instead of Euler angles — with an optional worked example. |
| Tuning and calibrating the Random Rover | [`strategy-for-tuning-calibration-random-rover.md`][12] | Student-facing guide for after the course. Part 1: calibration vs. tuning vs. preference-setting, every tunable parameter rated by importance, a bottom-up strategy, and realistic improvement targets. Part 2: a step-by-step procedure, Steps 0-11 (get ready, power, mechanics, servo aim, compass, motors, turning, scans, speed/stopping distance, safety nets, preferences, 5-minute arena run), with time estimates, tools, hardware-safety warnings, and ripple effects between parameters. |


## Purpose / Role in Repository

Explainers sit off to the side of the main syllabus/lesson-plan/BOM generation pipeline described
in the root [README][13] and [`CLAUDE.md`][14]. They're supplementary reading, not something a
student needs to get through before a class — the answer to a question a curious student might ask
mid-build ("wait, why CircuitPython and not MicroPython?") without making every
[lesson script][15] stop and explain it inline. A lesson plan or lesson script is free to link out
to one of these whenever it touches a concept an explainer already covers in more depth.

The tuning and calibration explainer is the one exception that's more than background: it's the
next stop after Class 6, and the root README points students to it for tuning their rover. Its
procedure is also folded, rewritten for the full-build files and tools, into section 8 of the
[full build script][16] — so if you change a tuning step or starting value in one, reconcile the
other. Its tuning log is [`full_build/src/tuning-log-template.md`][17], and the `servo_check.py`
and `motor_check.py` tools in [`full_build/`][18] come from its Steps 3 and 5.


## Usage

Read any explainer on its own; none depend on another, except the IMU → gimbal lock → quaternions
series, which reads best in that order alongside Class 4.

Nothing to build here — it's all static markdown. To add an explainer, invoke the `/explainer`
skill with the topic, then move that topic out of the Future list below and into the Contents
table. To hand someone a Word doc or PDF instead, convert with pandoc:

```bash
pandoc -f gfm what-is-the-random-rover.md -o what-is-the-random-rover.docx
```


## Notes

- Explainers are written for the student, so keep the plain-English, narrative voice when
    regenerating; follow the repo's markdown conventions (4-space list indent, reference-style
    links) in [`CLAUDE.md`][14].
- Related folders: [`lesson_scripts/`][15] (student walkthroughs that link here),
    [`lesson_plans/`][19] (instructor guides), [`handouts/`][20] (short per-class summaries and
    reference links).


## Future Explainers Topics
These are future explainer topics, not yet written (checked against this folder's contents — none
of them exist yet; move an entry into the Contents table above once its file is generated):

- what-are-pull-up-pull-down-resistors.md
- what-are-the-types-of-displays.md
- devices-that-need-debouncing.md
- what-devices-have-deceptive-behavior-like-buttons.md
- what-is-an-odometer.md
- what-is-a-buck-converter.md
- what-is-git-and-github.md
- what-is-wheel-odometry.md
- how-does-a-microcontroller-host-a-website.md
- why-5v-for-digital-but-33v-for-analog.md
- what-is-a-servo-motor.md
- why-is-analog-output-used-for-transducers.md


[01]:what-is-the-random-rover.md
[02]:microprocessor-vs-microcontroller.md
[03]:micropython-vs-circuitpython.md
[04]:raspberry-pi-pico-2w-pinout.md
[05]:types-of-pins-on-raspberry-pi-pico-2w.md
[06]:what-are-breadboards-and-dupont-wires.md
[07]:spi-i2c-uart-serial-communications.md
[08]:glossary-of-terms-for-microcontrollers.md
[09]:what-is-an-imu-and-mahony-filter.md
[10]:what-is-gimbal-lock.md
[11]:what-are-quaternion-and-why-use-them.md
[12]:strategy-for-tuning-calibration-random-rover.md
[13]:../README.md
[14]:../CLAUDE.md
[15]:../lesson_scripts/README.md
[16]:../full_build/full-build-script.md
[17]:../full_build/src/tuning-log-template.md
[18]:../full_build/README.md
[19]:../lesson_plans/README.md
[20]:../handouts/README.md
