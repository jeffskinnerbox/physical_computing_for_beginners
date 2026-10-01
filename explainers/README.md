# README

This folder is where the "why does it work that way?" questions live. A class script or lesson
plan can't stop to explain, say, the whole history of the microcontroller every time it mentions
one — that would bury the actual build instructions. So instead, whenever a concept in the course
is worth a real explanation rather than a one-line aside, it gets pulled out into its own document
here, written in plain English for a middle/high-school reader. Each one is generated with the
`explainer` skill, which favors a narrative structure — status quo, then the problem, then the
solution — over a dry glossary-style definition, so a student reads it more like a short story
about *why* something was invented than a spec sheet about *what* it is.


## Usage

See the root [README][01] for the full course map, and [`CLAUDE.md`][02] for the generation
pipeline behind it. Explainers sit off to the side of the main syllabus/lesson-plan/BOM generation
pipeline: they're supplementary reading, not something a student needs to get through before a class. Think of them
as the answer to a question a curious student might ask mid-build — "wait, why CircuitPython and
not MicroPython?" — without making every lesson script stop and explain it inline. A lesson plan
or lesson script is free to link out to one of these whenever it touches a concept an explainer
already covers in more depth.


## Build Process

Nothing to build here — it's all static markdown. If you want a new explainer, that's what the
`explainer` skill is for; just invoke it with the topic you want covered. If you'd rather hand
someone a Word doc or PDF instead of a markdown file, pandoc will convert any of these directly:
`pandoc -f gfm <file>.md -o <file>.docx`, following the same export convention described in
[`CLAUDE.md`][02].


## Contents

| Topic | File/Directory Name | Description/Summary |
| :------ | :---------- | :------------ |
| CircuitPython vs. MicroPython | `micropython-vs-circuitpython.md` | Compares the two Python variants used on microcontrollers — their shared origins, where they diverge (upload workflow, libraries, governance), and why this course picks CircuitPython. Also contrasts both with C/C++. |
| The Random Rover | `what-is-the-random-rover.md` | Explains what kind of robot the course's capstone project is, why obstacle-avoiding rovers are a common first robotics build, and how its sense-decide-act loop compares to a Roomba and to more advanced autonomous machines. |
| Tuning and calibrating the Random Rover | `strategy-for-tuning-calibration-random-rover.md` | Student-facing guide to tuning a finished rover: what calibration vs. tuning vs. preference-setting means, every tunable parameter rated by importance, a bottom-up strategy, realistic improvement targets, then an 11-step procedure (power, mounting, servo aim, compass, motors, turns, scans, stop distance, safety nets, preferences, 5-minute arena test) with time estimates, tools, hardware-safety warnings, and ripple effects between parameters. |
| Microprocessors vs. microcontrollers | `microprocessor-vs-microcontroller.md` | Explains the historical split between microprocessors (Intel 4004) and microcontrollers (TI TMS 1000), what distinguishes them, and why the Pico 2 W's RP2350 microcontroller is the right chip for this course's projects. |
| Raspberry Pi Pico 2 W pinout | `raspberry-pi-pico-2w-pinout.md` | Explains what a pinout is (Wikipedia), what it's used for, how it's communicated (silkscreen, diagrams, tables, datasheets), where to find the Pico 2 W's (pinout.xyz), and how to find one for any other device. |
| SPI, I2C, and UART serial communications | `spi-i2c-uart-serial-communications.md` | Explains what serial communication is and why microcontrollers depend on it, then breaks down UART, I2C, and SPI — what each abbreviation stands for, how each protocol moves data, and how to reach each one from CircuitPython on the Pico 2 W (including this course's own LSM9DS1 over I2C and the Class 6 TFT over SPI). |
| Types of pins on the Pico 2 W | `types-of-pins-on-raspberry-pi-pico-2w.md` | Walks through every non-`GPnn` pin label on the Pico 2 W pinout — `GND`, `VBUS`, `VSYS`, `3V3 EN`, `3V3 OUT`, `ADC VREF`, `ADC GND`, `GP26 A0`/`GP27 A1`/`GP28 A2`, and `RUN` — what each is for, how it operates electrically, and how (or whether) it's reached from CircuitPython. |
| Glossary of terms for microcontrollers | `glossary-of-terms-for-microcontrollers.md` | Quick-lookup, topic-grouped definitions for MCU jargon — the chip itself (MCU, CPU, register), memory (RAM, SRAM, Flash, EEPROM, NVM), input/output (GPIO, pull-up/pull-down resistor, ADC, DAC, PWM), serial protocols (SPI, I2C, UART, linking to the dedicated doc), event handling (interrupt, ISR, timers, DMA, RTOS), and startup/safety/power (firmware, watchdog timer, brown-out reset, sleep modes). |
| Breadboards and Dupont wires | `what-are-breadboards-and-dupont-wires.md` | Explains the "breadboard" and "Dupont wire" names' origins, what each is (Wikipedia), why breadboards are used, board sizes and tie-point layout (center channel, power rails, row wiring), jumper wire lengths/terminal types/colors, making your own or substituting solid 22 AWG wire, and when not to use either. |
| IMUs and the Mahony filter (series part 1 of 3) | `what-is-an-imu-and-mahony-filter.md` | Explains what an IMU is (gyroscope, accelerometer, magnetometer — the course's 9-DOF LSM9DS1), what IMUs are good for, why raw readings are rates and directions rather than angles, how the Mahony filter fuses them (and what `MAHONY_KP`/`MAHONY_KI` do), and how Mahony compares to complementary, Madgwick, Kalman, and Extended Kalman filters. |
| Gimbal lock (series part 2 of 3) | `what-is-gimbal-lock.md` | Defines Euler angles (roll/pitch/yaw), explains how gimbal lock loses a degree of freedom in both physical gimbals and software, tells the Apollo story (warning lights, "a fourth gimbal for Christmas," Apollo 13), why NASA didn't add a fourth gimbal or use quaternions, and where gimbal lock still bites today. |
| Quaternions (series part 3 of 3) | `what-are-quaternion-and-why-use-them.md` | Explains what quaternions are, Hamilton's 1843 Broom Bridge invention and their comeback in graphics/aerospace/robotics, and why the Class 4 Mahony filter stores orientation as a quaternion (`q0..q3`) instead of Euler angles — with an optional worked example. |


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



[01]:../README.md
[02]:../CLAUDE.md
