# Lesson Plan: Class 3 — Dual H-Bridge Motor Driver

* **Class:** 3 of 6 (plus Pre-Class)
* **Phase:** Phase 2 — Outputs & Motion (Class 3-4: driving motors and reading orientation)
* **Duration:** ~2 hours (120 min)
* **Prerequisites from prior Classes:** Classes 1 and 2 completed — every student has a working
  debounced pushbutton/rotary-encoder circuit (`GP2`-`GP4`, `GP14`-`GP15`) and a working HC-SR04 +
  SG90 sensor-sweep circuit (`GP6`-`GP8`) on their breadboard, and is comfortable wiring from a pin
  table, saving `code.py`, and reading the serial console. Both circuits stay on the breadboard,
  powered but unused, all Class — nothing from Class 1 or 2 is touched or rewired today.

---

## 1. Class Overview

This is the third Class of the course and the first of Phase 2 (Outputs & Motion) — the first Class
where students make the car actually move. Students wire a DRV8833 dual H-bridge motor driver to
their Pico 2 W and the two DC gearbox motors in the Emo Smart Robot Car Chassis Kit, running the
motors from their own 9V battery rather than the Pico's logic power. After a simple forward/reverse/
stop test, students try to drive the car in a 12-inch square and a 12-inch-diameter circle using
timed, uncorrected ("open-loop") moves — and discover that hitting an exact size is much harder than
just making the car move in *some* square or circle shape. That gap is the pedagogical point: by the
end of the Class, students will have directly experienced why "dead reckoning" drifts, and will be
able to name the specific causes (no wheel/heading feedback, battery voltage sag, wheel slip/
friction) rather than waving at one vague "it's not accurate."

## 2. Learning Goals

* Wire a DRV8833 dual H-bridge motor driver to the Pico 2 W and the chassis kit's two DC gearbox
  motors, powered from a separate 9V battery with a common ground back to the Pico
* Explain, in plain language, how an H-bridge lets a single motor spin both forward and reverse, and
  why the DRV8833 needs two logic pins per motor
* Write and use `motor_driver.py`, a small drive()/stop() library that throttles PWM duty cycle to
  keep motor current in a safe range
* Attempt a 12-inch square and a 12-inch-diameter circle using timed, open-loop moves, and observe
  the resulting drift from the target dimensions
* Name, specifically, the separate causes of that drift — missing wheel/heading feedback, battery
  voltage sag, and wheel slip/friction — rather than one generic explanation

## 3. Preparation Checklist

* **1-2 days before:** Confirm every student's Class 1 and Class 2 circuits are still intact and
  power up — a quick visual/serial spot-check, not a rebuild. (~15 min)
* **1-2 days before:** Verify `adafruit_motor` (already used in Class 2) is present in each
  student's Library Bundle folder; no new library is required for the DRV8833 itself since
  `motor_driver.py` is course-provided source, not a separate PyPI/Bundle package. (~5 min)
* **1-2 days before:** Charge or freshly stock 9V batteries — one per student workstation, plus 2-3
  spares. Confirm each battery clip and 5V buck converter module (if used for other onboard power)
  is present and wired correctly. (~15 min)
* **Day of, before students arrive:**
  * Set out one DRV8833 breakout board, one 9V battery with clip, and continued access to each
        workstation's existing breadboard and chassis kit at each workstation.
  * Measure and mark a 12-inch square and a 12-inch-diameter circle on the floor or a large sheet
        of paper/tape at 2-3 shared "test tracks" around the room — students calibrate against these
        visually, not on their own workstation surface. (~15 min)
  * Pre-build one reference circuit (DRV8833 + both motors) at the instructor bench and test
        `class-3-code-1.py` (`motor_driver.py`) and `class-3-code-2.py` end-to-end, including a
        rough calibration pass on `SPEED`, `SECONDS_PER_INCH`, and `SECONDS_PER_90_DEGREES` so you
        know what a realistic first attempt looks like. (~25 min)
  * Have spare DRV8833 boards, motor leads, and 9V batteries on hand — a dead or weak 9V battery
        is the single most common "my motors barely move" complaint in this Class.
* **Have ready:** A short list of discussion prompts for "what's missing?" (see Direct Teaching and
  Independent Work below), and the shared test-track locations communicated to students at the start
  of Guided Practice.

## 4. Materials & Components

Per-student unless noted. Component names only — see the course Bill of Materials for costs,
quantities, and sourcing.

| Component | Purpose This Class |
| :---------- | :-------------------- |
| Raspberry Pi Pico 2 W (with header) | Microcontroller running CircuitPython |
| DRV8833 Dual H-Bridge DC/Stepper Motor Driver Breakout Board | Drives both DC gearbox motors' speed and direction from PWM logic signals |
| Emo Smart Robot Car Chassis Kit (DC gearbox motors + wheels) | The two motors under test, and the chassis they drive |
| 9V battery clip and 9V battery | Separate power supply for the motors, independent of the Pico's logic power |
| Breadboard (830-point, from Class 1) | Circuit assembly surface — Class 1 and 2 circuits stay on it, untouched |
| Dupont jumper wires (shared) | Point-to-point wiring |
| USB cable (student-supplied, from Pre-Class) | Power + serial connection to laptop |
| Windows 11 laptop with Mu or Thonny (student-supplied) | Edit and run CircuitPython code |
| Shared: tape/marked 12-inch square and circle test tracks | Reference targets for the square/circle milestone |

## 5. Class Timeline

### 5a. Warm-up / Hook — ~10 min

**What to do:** Have every student plug in their Pico 2 W and confirm both Class 1 and Class 2
circuits still work — button/encoder LEDs respond, and the sensor-on-servo sweep still runs. Ask
2-3 students to describe, in one sentence, what today's H-bridge might have in common with the PWM
they already used to control the Class 2 servo.

**What to say:** "Everything you've wired so far has been about *reading* the world — a switch, an
encoder, a distance sensor. Today's the first day you *move* something with real force behind it.
Your button and encoder circuit, and your sensor-and-servo circuit, both stay wired exactly as they
are — you're adding motor control right alongside them."

**What to watch for:** Any Class 1/2 regressions (loose jumper, sensor mount shifted) — fix quickly
rather than losing momentum, since today's build shares breadboard space with both prior circuits.

**Time check:** If more than 2-3 boards need real rework, handle it during Guided Practice instead
of holding up the whole class now.

### 5b. Introduction — ~10 min

**What to do:** Introduce the DRV8833 and the two DC gearbox motors, and preview the square/circle
challenge — including the twist that "any size" will be easy but "exactly 12 inches" will not.

**What to say:**

* "This board's whole job is letting your Pico's tiny, safe logic signals control motors that draw
  way more current and run on a completely separate 9V battery."
* "First goal: get both wheels spinning forward, reverse, and stopped on command. Second goal — and
  this is the interesting one — drive a 12-inch square and a 12-inch circle *exactly*. The first
  part of that will feel easy. The second part won't, and that's on purpose."
* "By the end of today you'll be able to say precisely *why* it's hard — not just that it is."

**Questions to ask students:** "If I told you to walk in a perfect 12-foot square with your eyes
closed, using only a count in your head to know when to turn — how close do you think you'd get?"
(Sets up the open-loop/dead-reckoning idea before the term is introduced.)

### 5c. Direct Teaching — ~10 min

No code yet — diagrams and discussion only, using the whiteboard or projected diagram.

**Concept 1 — What an H-bridge does (Theory of Operation, brief).**
A DC motor spins one direction when current flows through it one way, and the opposite direction
when current is reversed. A microcontroller pin can only source current one direction at low
voltage — it has no way to "reverse" a motor by itself. An H-bridge is a small switching circuit
(named for its shape, an "H" with the motor as the crossbar) with four switches arranged so that
flipping which pair is closed reverses the current direction through the motor, without the
microcontroller ever needing to source high current itself. The DRV8833 packs two complete
H-bridges onto one board — one per motor — plus the switching logic, so the Pico only needs to send
small logic-level signals to control both motors' direction and speed.

*Step-by-step decomposition of one motor's control (locked-antiphase mode, used this Class):*

1. Pico sets `AIN1` and `AIN2` (Motor A's two logic pins) to a PWM signal pair, opposite phase.
2. The DRV8833's internal H-bridge switches follow that PWM pattern, driving current through the
   motor in the corresponding direction at a duty-cycle-proportional average voltage.
3. Motor spins forward, reverse, or brakes, depending on the relative phase/duty cycle of `AIN1`
   vs `AIN2`.
4. Motor B is controlled the same way, independently, on `BIN1`/`BIN2`.
5. `class-3-code-1.py` (`motor_driver.py`) wraps this pattern behind a simple `drive(left, right)`
   / `stop()` API using `adafruit_motor.motor.DCMotor`, so the rest of the course's code never has
   to think about raw PWM phases again.

**Concept 2 — Why PWM duty cycle isn't the same as motor speed.**
A 50% PWM duty cycle does not mean the motor spins at 50% of its top speed. Ask: "What do you think
eats up part of that 50%?" Draw out: stall torque (a motor needs a minimum voltage just to
*overcome friction and start moving at all* — below that, nothing happens no matter the duty cycle),
friction in the gearbox and wheels, and voltage sag under load (a loaded 9V battery delivers less
than its rated voltage). `MAX_THROTTLE` in `motor_driver.py` exists specifically to cap current draw
— not to set a "speed" in any precise sense.

**Concept 3 — Why two separate power sources still need a common ground.**
The motors run off their own 9V battery (`VM` on the DRV8833), completely separate from the Pico's
USB-supplied logic power — this protects the Pico from motor electrical noise and current spikes.
But the DRV8833's logic pins (`AIN1`/`AIN2`/`BIN1`/`BIN2`) still receive PWM signals *referenced to*
the Pico's 0V (ground). If the two power supplies don't share a common ground, the DRV8833 has no
consistent "zero" to measure the Pico's signal against, and the logic won't work reliably even
though each supply is individually fine. Ask: "What do you think 'common ground' actually means
electrically, not just as a wiring instruction?" (A shared reference point both circuits measure
voltage against.)

**Concept 4 — Locked-antiphase vs. phase/enable — a brief comparison.**
The DRV8833 supports two different control schemes: locked-antiphase (two PWM signals per motor,
used in `motor_driver.py`) and phase/enable (one direction pin + one PWM speed pin per motor).
Locked-antiphase gives smoother low-speed control and built-in active braking, at the cost of using
an extra PWM-capable pin per motor — which is why this course uses it, since the Pico 2 W has PWM
pins to spare.

### 5d. Guided Practice — ~40 min

Instructor builds along on the projector; students wire up and test in parallel.

**Wiring — third circuit of the course, alongside (not replacing) Class 1 and 2's.** Leave both
prior circuits exactly as-is on the breadboard; today's wiring uses entirely new pins and a
separate 9V power source.

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

**Checkpoint 1:** Before writing any code, have every pair trace their own wiring against the
table above out loud to a neighbor, and specifically confirm the Pico's `GND` is jumpered to the
DRV8833's `GND` — this is the wiring mistake that produces the most confusing symptoms later.
Wiring mistakes found now save debugging time later.

**Step 1 — motor driver library and basic test.**
Load `class-3-code-1.py` (save as `motor_driver.py` — this is a library file, imported by other
code, not run directly).

```python
# class-3-code-1.py  (save as motor_driver.py)
# DRV8833 motor driver library -- forward/reverse/stop/speed per channel.
import board
import pwmio
from adafruit_motor import motor

MAX_THROTTLE = 0.6  # [VERIFY] -- cap duty cycle to limit current for these TT gearbox motors

pwm_ain1 = pwmio.PWMOut(board.GP9, frequency=50)
pwm_ain2 = pwmio.PWMOut(board.GP10, frequency=50)
pwm_bin1 = pwmio.PWMOut(board.GP11, frequency=50)
pwm_bin2 = pwmio.PWMOut(board.GP12, frequency=50)

motor_a = motor.DCMotor(pwm_ain1, pwm_ain2)
motor_b = motor.DCMotor(pwm_bin1, pwm_bin2)


def _clamp(throttle):
    if throttle is None:
        return None
    capped = max(-MAX_THROTTLE, min(MAX_THROTTLE, throttle))
    return capped


def drive(left, right):
    """left/right: -1.0 (full reverse) to 1.0 (full forward), or None to coast."""
    motor_a.throttle = _clamp(left)
    motor_b.throttle = _clamp(right)


def stop():
    motor_a.throttle = 0.0  # 0.0 brakes; None coasts
    motor_b.throttle = 0.0
```

Then, at the REPL or in a short scratch `code.py`, import it and try each move while printing what's
happening:

```python
import time
import motor_driver

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

**What to watch for:** A motor that spins the wrong direction almost always means its two leads are
swapped at `AOUT1`/`AOUT2` (or `BOUT1`/`BOUT2`) — swap the two wires, don't fight it in code, unless
the class wants to practice fixing it in software (swap the `+1`/`-1` sign instead).

**Checkpoint 2:** Every pair should be able to print "forward" and see both wheels spin the same
direction at the same rate, print "reverse" and see both reverse, and print a turn command and see
the wheels spin opposite directions.

**Step 2 — attempt the square and circle (open-loop dead reckoning).**
Load `class-3-code-2.py`. Prints a discrete status message for each move — not a continuous stream,
since there's no wheel-speed feedback yet.

```python
# class-3-code-2.py
# Attempts a 12" square and a 12"-diameter circle -- open-loop, timed moves only.
import time
import motor_driver

SPEED = 0.5                  # [VERIFY] -- calibrate per robot
SECONDS_PER_INCH = 0.09      # [VERIFY] -- calibrate: time a measured straight run, divide by inches
SECONDS_PER_90_DEGREES = 0.4  # [VERIFY] -- calibrate: time a measured 90-degree turn


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
        time.sleep(0.2)
        turn_90()
        time.sleep(0.2)
    print("attempt: square complete")


def drive_circle(diameter_inches=12):
    # Approximate a circle as a many-sided polygon of short straight segments + small turns.
    print("attempt: circle, diameter", diameter_inches, "in")
    import math
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


print("Class 3 -- square/circle attempts starting...")
drive_square(12)
time.sleep(1)
drive_circle(12)
```

**What to watch for:** This is the moment students should see the car finish a "square-ish" or
"circle-ish" shape that is visibly *not* 12 inches, or not a clean right angle — let it be messy.
Ask: "You told it to go exactly 12 inches. What did it actually do?"

**What "done" looks like for this segment:** The car completes a full attempted square and a full
attempted circle without instructor intervention (even if the dimensions are off), with status
messages printing to the console for each move.

### 5e. Independent Work — ~40 min

**What to do:** Students (in pairs where possible) take their car to a shared test track and run
`drive_square()` and `drive_circle()` repeatedly, adjusting `SPEED`, `SECONDS_PER_INCH`, and
`SECONDS_PER_90_DEGREES` between attempts to get closer to the marked 12-inch targets. After each
attempt, have them note in their build journal: was the error mostly in the straight-line distance,
the turn angle, or both? Faster pairs can:

* Deliberately swap in a weaker or more depleted 9V battery mid-session and observe how much the
  calibration constants drift — a direct, hands-on demonstration of voltage sag.
* Try the square/circle attempt on a different floor surface (carpet vs. tile) and discuss wheel
  slip/friction as a distinct cause from voltage sag or timing.
* Begin sketching (on paper, no code yet) what information — beyond a timer — would let the car
  correct its own path instead of just guessing.

**What to watch for:** The most common failure at this stage is a car that pulls consistently to one
side even when both throttle values are equal — almost always a real mechanical difference between
the two motors/gearboxes (not a bug), and a good moment to point out that hardware variation is part
of why open-loop control drifts.

**Time check:** At the 30-minute mark, do a quick show-of-hands: "Who has completed at least one
full square and one full circle attempt, regardless of accuracy?" Redirect instructor attention to
pairs still stuck on the basic drive() test.

### 5f. Closing / Wrap-up — ~10 min

**What to do:** Ask 2-3 volunteers to run their best square and circle attempt on a shared test
track for the group. Open the "what is missing?" discussion: have the group name the specific,
separate causes of drift — no wheel/heading feedback, battery voltage sag, wheel slip/friction —
rather than settling for one vague "it's not accurate enough."

**What to say:** "Every one of you just built a car that can move with real purpose, but none of you
could make it hit an exact target reliably — and that's not a bug in your code, it's a fundamental
limit of driving 'blind,' with no way to check your actual position against your intended one.
That's exactly the gap the IMU fills next Class."

**Preview next Class:** Class 4 reuses none of today's, Class 1's, or Class 2's pins — it's the
LSM9DS1 9-DOF IMU over I2C on `GP0`/`GP1`, while today's motor driver circuit and both prior
circuits stay untouched on the breadboard. Point students to the Class 4 references in the syllabus
if they want to read ahead.

## 6. Troubleshooting Guide

| Problem | Likely Cause | Fix |
| :-------- | :------------- | :---- |
| Neither motor spins | `VM` not connected to the 9V battery, or battery dead | Check battery voltage with a meter; confirm `VM` and battery `GND` wiring |
| One motor doesn't spin | Loose wire on a DRV8833 output pin, or a dead motor | Reseat jumper wires; swap in a spare motor to isolate the fault |
| Both motors spin, but the car doesn't move (or barely moves) | `MAX_THROTTLE` set too low, or wheels not making contact with the floor | Raise `MAX_THROTTLE` in small steps; confirm chassis is set down properly |
| Motor spins the wrong direction | Motor leads swapped at `AOUT1`/`AOUT2` (or `BOUT1`/`BOUT2`) | Swap the two motor leads, or swap the sign of that motor's throttle in code |
| Both motors spin the same direction on a "turn" command | Motor B's leads wired with opposite polarity convention from Motor A | Swap Motor B's leads, or its throttle sign, so `+1` means the same physical direction for both |
| Logic behaves erratically even though wiring looks right | Missing common ground between the 9V battery circuit and the Pico | Add a jumper from DRV8833 `GND` to Pico `GND` |
| Square/circle attempt drifts wildly between runs on the same settings | Battery voltage sagging as it depletes during the session | Swap in a fresh 9V battery and re-calibrate `SPEED`/timing constants |
| Car pulls consistently to one side even at equal throttle | Real mechanical difference between the two gearbox motors | Compensate with slightly different left/right throttle values, or note the asymmetry in the build journal |
| `ImportError: no module named 'motor_driver'` | `motor_driver.py` not saved to the CIRCUITPY drive alongside `code.py` | Confirm `class-3-code-1.py` was saved as `motor_driver.py` in the CIRCUITPY root, not left named `class-3-code-1.py` |

## 7. Age Differentiation Notes

**Younger students (12-14) and their parent/guardian:** Provide the pin table above pre-printed
and laminated at the workstation so it's a lookup, not a memorization task. Pair a younger
student's fine-wiring work (especially the DRV8833's output-to-motor-lead connections) with the
parent/guardian's help holding the chassis steady. Start from `class-3-code-1.py` and
`class-3-code-2.py` already loaded as starting points, and have them focus on tuning the three
calibration constants (`SPEED`, `SECONDS_PER_INCH`, `SECONDS_PER_90_DEGREES`) by trial and error
rather than writing the drive functions from scratch.

**Older students (15-18) and adults:** Have them type `motor_driver.py`'s `drive()`/`stop()`
functions themselves from the wiring table and the locked-antiphase explanation, rather than
starting from the provided file. Once the square/circle milestone is met, challenge them to log
each attempt's actual measured dimensions (with a tape measure) against the target, across at least
three battery charge levels, and see if they can predict how far off the next attempt will be.

## 8. Assessment

**Milestone Assignment (per syllabus, Phase 2 / Class 3):** Car reliably drives a 12-inch square and
a 12-inch-diameter circle.

**What "complete" looks like:** The student can run `drive_square(12)` and `drive_circle(12)` on a
shared test track and produce a shape recognizably close to the 12-inch target — this is a
completion-based, "does it work in the real world" check, not a precision measurement. Minor drift
is expected and is itself part of the lesson.

**How to give feedback without scoring:** Ask the student to point at the marked test track and
narrate, specifically, what's causing the gap between their car's path and the target ("is this a
timing problem, a battery problem, or a slip problem — or all three?") rather than checking a box.
If a pair can't get a recognizable square or circle in the time available, that's fine — have them
bring a working version to the start of Class 4 and note it in their build journal.

## 9. Instructor Tips

* Run the square and circle attempt yourself, live, on a test track *before* students touch their
  own cars — a visibly imperfect instructor demo sets the right expectation better than a perfect
  one would.
* Common-ground mistakes produce the most confusing symptoms in this Class (logic that "sort of"
  works, or works intermittently) — if a pair is stuck and everything else checks out, verify the
  common ground jumper first.
* Keep a couple of freshly charged 9V batteries in rotation and swap them into a demo car mid-Class
  on purpose — a live, visible voltage-sag demonstration lands better than describing it.
* The "what is missing?" discussion (Closing) is the conceptual payoff of this whole Class — resist
  the urge to answer it for the students; let them arrive at "no feedback" themselves after wrestling
  with the calibration constants during Independent Work.
* Keep both code files (`class-3-code-1.py`/`motor_driver.py`, `class-3-code-2.py`) on a shared
  drive/USB stick so a student who breaks their working file can recover instantly instead of losing
  class time.

## 10. Resources & References

* [DC Motor Examples - Raspberry Pi Pico (CMU Creative Soft Robotics)][01] — worked examples of DC
  motor control from a Pico
* [Driving A DC Motor With CircuitPython][02] — background on PWM-based DC motor speed control
* [Adafruit CircuitPython Motor Library — API Reference][03] — the `adafruit_motor.motor.DCMotor`
  API used in `class-3-code-1.py`
* [Adafruit DRV8833 DC/Stepper Motor Driver Breakout Board][04] — the motor driver used this Class,
  including its locked-antiphase and phase/enable control modes

---

[01]:https://courses.ideate.cmu.edu/16-480/s2026/text/code/pico-motor.html
[02]:https://www.woolseyworkshop.com/2022/07/25/driving-a-dc-motor-with-circuitpython/
[03]:https://docs.circuitpython.org/projects/motor/en/latest/api.html
[04]:https://learn.adafruit.com/adafruit-drv8833-dc-stepper-motor-driver-breakout-board
