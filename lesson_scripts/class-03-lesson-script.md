# Lesson Script: Class 3 — Dual H-Bridge Motor Driver


* **Class:** 3 of 6 (plus Pre-Class)
* **Duration:** ~2 hours
* **What You'll Need:** see [Section 2](#2-what-youll-need)
* **Before You Start:** Your Class 1 (button/encoder, `GP2`-`GP4`, `GP14`-`GP15`) and Class 2
    (sensor/servo sweep, `GP6`-`GP8`) circuits should still be working and stay exactly as they are
    on your breadboard — you're building next to them today, not replacing anything.

---


## 1. What This Project Is

Every circuit you've built so far has been about *reading* the world — a switch, a knob, a
distance sensor. Today's the first day you *move* something with real force behind it. You'll wire
a DRV8833 dual H-bridge motor driver to your Pico and the two DC gearbox motors in your car
chassis kit, running them off their own 9V battery instead of your Pico's power.

First you'll get both wheels spinning forward, reverse, and stopped on command — that part will
feel easy. Then you'll try to drive your car in an exact 12-inch square and a 12-inch-diameter
circle, using nothing but timed moves. That part won't feel easy, and that's on purpose: you're
about to discover, firsthand, why "driving blind" — no way to check your actual position against
where you meant to be — drifts. By the end, you'll be able to name the specific reasons why, not
just say "it's not accurate."

## 2. What You'll Need

| Component | Quantity | Purpose This Project |
| :---------- | :--------: | :---------------------- |
| Raspberry Pi Pico 2 W (with header) | 1 | Runs your CircuitPython code |
| DRV8833 dual H-bridge motor driver breakout | 1 | Drives both DC gearbox motors from PWM logic signals |
| Emo Smart Robot Car Chassis Kit | 1 | The two motors under test and the chassis they drive |
| 9V battery clip and 9V battery | 1 each | Separate power for the motors, independent of the Pico's logic power |
| Breadboard (from Classes 1-2) | 1 | Your existing circuits stay on it, untouched |
| Dupont jumper wires | ~10 | Point-to-point connections |
| USB cable | 1 | Powers the Pico and carries the serial console |
| Laptop with Mu or Thonny | 1 | Where you write/save code and read the serial console |
| Marked 12" square / 12"-diameter circle test track | 1 (shared) | Your target for the calibration exercise |

**Additional components for the Homework Assignments** (Section 9) — no homework has been written
for this class yet; this section will be filled in when that content is added.

## 3. Meet the Hardware

**DRV8833 dual H-bridge motor driver.** A DC motor spins one direction when current flows through
it one way, and the opposite direction when reversed. Your Pico's GPIO pins can only push current
one direction at a low, safe voltage — they have no built-in way to "reverse" a motor, and they
can't safely supply the higher current a real motor needs anyway. An **H-bridge** is a small
switching circuit (named for its shape — an "H" with the motor as the crossbar) with four switches
arranged so flipping which pair is closed reverses current through the motor, without your Pico
ever sourcing that current itself. The DRV8833 packs two complete H-bridges onto one board — one
per motor — so your Pico only has to send small logic-level signals to control both motors'
direction and speed, while a separate 9V battery supplies the actual driving current.

**Locked-antiphase control.** The DRV8833 supports a couple of control schemes; this project uses
**locked-antiphase**, where each motor gets two PWM signal pins (`AIN1`/`AIN2` for Motor A,
`BIN1`/`BIN2` for Motor B) driven in opposite phase. The relative phase and duty cycle between
that pair determines direction and speed. The `adafruit_motor.motor.DCMotor` class hides this
detail behind a simple `.throttle` property from `-1.0` (full reverse) to `1.0` (full forward),
with `0.0` actively braking the motor.

**Why PWM duty cycle isn't the same as speed.** A 50% duty cycle does *not* mean the motor spins
at 50% of its top speed. Some of that duty cycle gets eaten by stall torque (a motor needs a
minimum voltage just to overcome friction and start moving at all), gearbox/wheel friction, and
voltage sag (a loaded 9V battery delivers less than its rated voltage). That's why this project
caps throttle with a `MAX_THROTTLE` constant — to limit current draw, not to set a precise speed.

**Why two power sources still need a common ground.** The motors run off their own 9V battery
(`VM` on the DRV8833), completely separate from the Pico's USB-supplied logic power — this
protects the Pico from motor electrical noise and current spikes. But the DRV8833's logic pins
still receive PWM signals measured relative to the Pico's 0V (ground). If the two power supplies
don't share a common ground, the DRV8833 has no consistent "zero" to measure the Pico's signal
against, and the logic won't behave reliably even though each supply is individually fine. This is
why the wiring table below includes a Pico-to-DRV8833 ground jumper even though the motors have
their own separate battery.

**Pinout summary** (Raspberry Pi Pico 2 W — new pins only; Classes 1-2 are unaffected):

| Pin | What we use it for |
| :---- | :-------------------- |
| `GP9` | DRV8833 `AIN1` (Motor A) |
| `GP10` | DRV8833 `AIN2` (Motor A) |
| `GP11` | DRV8833 `BIN1` (Motor B) |
| `GP12` | DRV8833 `BIN2` (Motor B) |
| 9V battery `+` | DRV8833 `VM` (motor power) |
| 9V battery `-` and Pico `GND` | DRV8833 `GND` (common ground) |

## 4. Build It: Phase 1 — Motor Driver Library and Basic Test

### Wiring for this phase

This is the complete wiring for the whole project — nothing changes for Phase 2.

| Component | Pico 2 W Pin |
| :---------- | :------------- |
| DRV8833 `AIN1` (Motor A) | `GP9` |
| DRV8833 `AIN2` (Motor A) | `GP10` |
| DRV8833 `BIN1` (Motor B) | `GP11` |
| DRV8833 `BIN2` (Motor B) | `GP12` |
| DRV8833 `VM` (motor power) | 9V battery `+` |
| DRV8833 `GND` | 9V battery `-` **and** Pico `GND` (common ground) |
| DRV8833 `AOUT1`/`AOUT2` | Motor A leads |
| DRV8833 `BOUT1`/`BOUT2` | Motor B leads |

Your Class 1 and Class 2 circuits stay exactly where they are on the breadboard. Before writing
any code, trace this wiring out loud, and specifically confirm the Pico's `GND` is jumpered to the
DRV8833's `GND` — a missing common ground is the wiring mistake that produces the most confusing
symptoms later (logic that "sort of" works, or works intermittently).

### What this code does

This phase is two files. First, `motor_driver.py` — a small library, not something you run
directly — that wraps the DRV8833's raw PWM control behind simple `drive(left, right)` and `stop()`
functions, capping current draw with `MAX_THROTTLE`. Second, a short scratch script that imports
that library and exercises it: forward, reverse, a turn, and stop, printing each move as it
happens.

### The code

Save this first file as `motor_driver.py` on your `CIRCUITPY` drive (not `code.py` — other code
imports this one).

```python
# class-3-code-1.py -- save as motor_driver.py
# DRV8833 motor driver library -- forward/reverse/stop/speed, per channel.

import board
import pwmio
from adafruit_motor import motor

# Caps duty cycle to limit current for these TT gearbox motors. Raise this
# in small steps if the car barely moves; lower it if motors run hot.
MAX_THROTTLE = 0.6

# Each motor gets a PWM pin pair, driven in opposite phase (locked-antiphase).
pwm_ain1 = pwmio.PWMOut(board.GP9, frequency=50)
pwm_ain2 = pwmio.PWMOut(board.GP10, frequency=50)
pwm_bin1 = pwmio.PWMOut(board.GP11, frequency=50)
pwm_bin2 = pwmio.PWMOut(board.GP12, frequency=50)

# DCMotor wraps the pin pair behind a simple .throttle property:
# -1.0 (full reverse) to 1.0 (full forward), 0.0 brakes, None coasts.
motor_a = motor.DCMotor(pwm_ain1, pwm_ain2)
motor_b = motor.DCMotor(pwm_bin1, pwm_bin2)


def _clamp(throttle):
    """Limit a throttle value to +/- MAX_THROTTLE, passing None through unchanged."""
    if throttle is None:
        return None
    return max(-MAX_THROTTLE, min(MAX_THROTTLE, throttle))


def drive(left, right):
    """left/right: -1.0 (full reverse) to 1.0 (full forward), or None to coast."""
    motor_a.throttle = _clamp(left)
    motor_b.throttle = _clamp(right)


def stop():
    """Actively brake both motors (0.0 brakes; None would coast instead)."""
    motor_a.throttle = 0.0
    motor_b.throttle = 0.0
```

Now save this second file as `code.py`, replacing whatever was there before, to test the library:

```python
# Scratch test script for motor_driver.py -- exercises forward/reverse/turn/stop.
import time
import motor_driver

print("Class 3, Phase 1 -- motor driver test starting...")

print("forward")
motor_driver.drive(0.5, 0.5)
time.sleep(1)

print("reverse")
motor_driver.drive(-0.5, -0.5)
time.sleep(1)

print("turn (left wheel back, right wheel forward)")
motor_driver.drive(-0.5, 0.5)
time.sleep(1)

print("stop")
motor_driver.stop()
```

### Try it / what you should see

You should see `forward` print, then both wheels spin the same direction at the same rate for one
second. Then `reverse` prints and both wheels reverse. Then the turn command prints and the wheels
spin opposite directions from each other. Then `stop` prints and both wheels stop immediately.

If a motor spins the wrong direction, its two leads are almost certainly swapped at `AOUT1`/`AOUT2`
(or `BOUT1`/`BOUT2`) — swap the physical wires rather than fighting it in code, unless you'd rather
practice fixing it in software by swapping that motor's throttle sign instead.

### Checkpoint

Confirm: `drive(0.5, 0.5)` moves both wheels forward together, `drive(-0.5, -0.5)` reverses both
together, and `drive(-0.5, 0.5)` spins the wheels in opposite directions (a turn-in-place).
`stop()` should halt both wheels immediately.

## 5. Build It: Phase 2 — Attempt the Square and Circle

### Wiring for this phase

No wiring changes — same circuit as Phase 1.

### What this code does

This program builds two higher-level moves — `drive_straight(inches)` and `turn_90()` — purely
out of *timing*: drive at a fixed speed for a calculated number of seconds, then stop. It chains
those into `drive_square(12)` (four straight-and-turn segments) and `drive_circle(12)` (many short
straight segments with small turns between them, approximating a circle). There's no way for the
car to check whether it actually went 12 inches or turned exactly 90 degrees — it's just trusting
the clock. This approach is called **open-loop control**, or "dead reckoning," and the gap between
what it *should* do and what it *actually* does is the whole point of today's Independent Work.

### The code

Save this as `code.py`, replacing Phase 1's scratch test script. `motor_driver.py` stays on the
drive unchanged — this new file imports it.

```python
# class-3-code-2.py
# Phase 2: attempt a 12" square and a 12"-diameter circle -- open-loop, timed moves only.

import time
import math
import motor_driver

# These three constants MUST be calibrated for your specific robot -- they
# will not be correct as-is. Time a measured straight run and a measured
# 90-degree turn on your own car, then adjust these until your car's actual
# movement matches what you told it to do.
SPEED = 0.5                    # throttle used for all moves
SECONDS_PER_INCH = 0.09        # calibrate: time a measured straight run, divide by inches
SECONDS_PER_90_DEGREES = 0.4   # calibrate: time a measured 90-degree turn


def drive_straight(inches):
    print("move: straight", inches, "in")
    motor_driver.drive(SPEED, SPEED)
    time.sleep(inches * SECONDS_PER_INCH)
    motor_driver.stop()


def turn_90():
    print("move: turn 90 deg")
    motor_driver.drive(-SPEED, SPEED)
    time.sleep(SECONDS_PER_90_DEGREES)
    motor_driver.stop()


def drive_square(side_inches=12):
    print("attempt: square, side", side_inches, "in")
    for _ in range(4):
        drive_straight(side_inches)
        time.sleep(0.2)  # brief pause so moves don't blur together
        turn_90()
        time.sleep(0.2)
    print("attempt: square complete")


def drive_circle(diameter_inches=12):
    # Approximate a circle as many short straight segments, each followed
    # by a small turn -- like walking a circle by taking short steps and
    # pivoting slightly after each one.
    print("attempt: circle, diameter", diameter_inches, "in")
    circumference = math.pi * diameter_inches
    segments = 24
    seg_length = circumference / segments
    seg_turn = SECONDS_PER_90_DEGREES / 9  # roughly 10 degrees per segment
    for _ in range(segments):
        drive_straight(seg_length)
        motor_driver.drive(-SPEED, SPEED)
        time.sleep(seg_turn)
        motor_driver.stop()
    print("attempt: circle complete")


print("Class 3, Phase 2 -- square/circle attempts starting...")
drive_square(12)
time.sleep(1)
drive_circle(12)
```

### Try it / what you should see

Your car should complete a full attempted square and a full attempted circle without you touching
anything, printing a status line for each individual move as it happens. The shape it traces will
almost certainly *not* be a clean 12-inch square or circle — corners may not be square, sides may
be different lengths, the circle may be lopsided. That's expected. Ask yourself: you told it to go
exactly 12 inches — what did it actually do, and why might that be?

### Checkpoint

Run `drive_square(12)` and `drive_circle(12)` on your test track and confirm the car completes
both attempts start to finish without help, tracing a recognizable (even if imperfect) square and
circle shape.

## 6. Troubleshooting Guide

| Problem | Likely Cause | Fix |
| :-------- | :------------- | :---- |
| Neither motor spins | `VM` not connected to the 9V battery, or the battery is dead | Check battery voltage; confirm `VM` and battery `GND` wiring |
| One motor doesn't spin | Loose wire on a DRV8833 output pin, or a dead motor | Reseat jumper wires; swap in a spare motor to isolate the fault |
| Both motors spin but the car barely moves | `MAX_THROTTLE` set too low, or wheels aren't touching the floor | Raise `MAX_THROTTLE` in small steps; confirm the chassis is set down properly |
| A motor spins the wrong direction | Its leads are swapped at `AOUT1`/`AOUT2` (or `BOUT1`/`BOUT2`) | Swap the two leads, or swap that motor's throttle sign in code |
| Both motors spin the same direction on a "turn" command | Motor B's leads are wired with opposite polarity convention from Motor A | Swap Motor B's leads (or throttle sign) so `+1` means the same physical direction for both |
| Logic behaves erratically even though wiring looks right | Missing common ground between the 9V circuit and the Pico | Add a jumper from DRV8833 `GND` to Pico `GND` |
| Square/circle drifts wildly between runs on the same settings | Battery voltage sagging as it depletes | Swap in a fresh 9V battery and re-calibrate the timing constants |
| Car pulls to one side even at equal throttle | Real mechanical difference between the two gearbox motors | Compensate with slightly different left/right throttle values |
| `ImportError: no module named 'motor_driver'` | The library file wasn't saved with the right name | Confirm the first file is saved as exactly `motor_driver.py`, not `class-3-code-1.py` |

## 7. Put It All Together

This is the finished project in one place — build straight to a calibrated square/circle attempt
without going through the individual phases above.

### Complete wiring

| Component | Pico 2 W Pin |
| :---------- | :------------- |
| DRV8833 `AIN1` (Motor A) | `GP9` |
| DRV8833 `AIN2` (Motor A) | `GP10` |
| DRV8833 `BIN1` (Motor B) | `GP11` |
| DRV8833 `BIN2` (Motor B) | `GP12` |
| DRV8833 `VM` (motor power) | 9V battery `+` |
| DRV8833 `GND` | 9V battery `-` **and** Pico `GND` (common ground) |
| DRV8833 `AOUT1`/`AOUT2` | Motor A leads |
| DRV8833 `BOUT1`/`BOUT2` | Motor B leads |

(Classes 1-2's circuits stay untouched on the breadboard alongside this.)

### Complete code

You need **two files** on your `CIRCUITPY` drive: `motor_driver.py` (the library, unchanged from
Phase 1) and `code.py` (the square/circle attempt, same as Phase 2).

```python
# motor_driver.py -- DRV8833 motor driver library.
import board
import pwmio
from adafruit_motor import motor

MAX_THROTTLE = 0.6  # calibrate per robot

pwm_ain1 = pwmio.PWMOut(board.GP9, frequency=50)
pwm_ain2 = pwmio.PWMOut(board.GP10, frequency=50)
pwm_bin1 = pwmio.PWMOut(board.GP11, frequency=50)
pwm_bin2 = pwmio.PWMOut(board.GP12, frequency=50)

motor_a = motor.DCMotor(pwm_ain1, pwm_ain2)
motor_b = motor.DCMotor(pwm_bin1, pwm_bin2)


def _clamp(throttle):
    if throttle is None:
        return None
    return max(-MAX_THROTTLE, min(MAX_THROTTLE, throttle))


def drive(left, right):
    motor_a.throttle = _clamp(left)
    motor_b.throttle = _clamp(right)


def stop():
    motor_a.throttle = 0.0
    motor_b.throttle = 0.0
```

```python
# code.py -- complete project: attempt a 12" square and 12"-diameter circle.
import time
import math
import motor_driver

SPEED = 0.5                    # calibrate per robot
SECONDS_PER_INCH = 0.09        # calibrate per robot
SECONDS_PER_90_DEGREES = 0.4   # calibrate per robot


def drive_straight(inches):
    motor_driver.drive(SPEED, SPEED)
    time.sleep(inches * SECONDS_PER_INCH)
    motor_driver.stop()


def turn_90():
    motor_driver.drive(-SPEED, SPEED)
    time.sleep(SECONDS_PER_90_DEGREES)
    motor_driver.stop()


def drive_square(side_inches=12):
    print("square, side", side_inches, "in")
    for _ in range(4):
        drive_straight(side_inches)
        time.sleep(0.2)
        turn_90()
        time.sleep(0.2)


def drive_circle(diameter_inches=12):
    print("circle, diameter", diameter_inches, "in")
    circumference = math.pi * diameter_inches
    segments = 24
    seg_length = circumference / segments
    seg_turn = SECONDS_PER_90_DEGREES / 9
    for _ in range(segments):
        drive_straight(seg_length)
        motor_driver.drive(-SPEED, SPEED)
        time.sleep(seg_turn)
        motor_driver.stop()


print("Class 3 project running -- square/circle attempt.")
drive_square(12)
time.sleep(1)
drive_circle(12)
```

## 8. What You Learned

You made your car move with real force for the first time, and then discovered exactly why moving
it *precisely* is harder than it sounds. Specifically, you now know:

* How an H-bridge lets a single motor spin both forward and reverse from simple logic-level
    signals, and why the DRV8833 needs two logic pins per motor (locked-antiphase control)
* Why PWM duty cycle isn't the same thing as motor speed — stall torque, friction, and voltage sag
    all eat into it
* Why two separate power supplies (the Pico's logic power and the motors' 9V battery) still need a
    shared ground reference to work together reliably
* What "open-loop control" (dead reckoning) means, and — from direct experience — why it drifts:
    no wheel/heading feedback to check against, battery voltage sag over time, and wheel slip or
    friction differences between the two motors

That gap — no way to check where you actually are against where you meant to be — is exactly what
an IMU (inertial measurement unit) starts to address. That's next class.

## 9. Homework Assignment

No homework assignments have been written for this class yet. This section will be filled in with
optional take-home exercises, following the same format as the Pre-Class homework in
[`class-00-lesson-script.md`](class-00-lesson-script.md#10-homework-assignment) (what the code
does, full commented code, and real-world examples).

## References

* [Adafruit CircuitPython Motor Library — API Reference][01] — the `adafruit_motor.motor.DCMotor`
    API used in this script
* [Adafruit DRV8833 DC/Stepper Motor Driver Breakout Board][02] — the motor driver used this
    project, including its locked-antiphase and phase/enable control modes
* [Driving A DC Motor With CircuitPython][03] — background on PWM-based DC motor speed control

---

[01]:https://docs.circuitpython.org/projects/motor/en/latest/api.html
[02]:https://learn.adafruit.com/adafruit-drv8833-dc-stepper-motor-driver-breakout-board
[03]:https://www.woolseyworkshop.com/2022/07/25/driving-a-dc-motor-with-circuitpython/
