# Lesson Plan: Class 3 — Dual H-Bridge Motor Driver

* **Class:** 3 of 6 (plus Pre-Class)
* **Phase:** Phase 2 — Outputs & Motion (Class 3-4: driving motors and reading orientation)
* **Duration:** 2 hours (120 min). Wheel odometry and the first version of the rover status website
  fit inside the original 120-min slot by trimming Warm-up/Introduction to the essentials and holding
  Guided Practice/Independent Work to a tighter pace than Classes 1-2 — see the "Class Timeline" pacing
  note below for what to cut first if a group runs long.
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
end of the first half of the Class, students will have directly experienced why "dead reckoning"
drifts, and will be able to name the specific causes (no wheel/heading feedback, battery voltage sag,
wheel slip/friction) rather than waving at one vague "it's not accurate."

Having named "no wheel feedback" as one of those causes, the Class then closes part of that gap:
students mount a Slot Type IR Optocoupler at each driven wheel to read the wheel-speed encoder disc
already molded into the chassis kit's wheels, and write `wheel_odometry.py` to convert counted ticks
into a real speed in cm/s per wheel — while learning why that same sensor, on its own, cannot tell
them *which way* the wheel is turning. Finally, students stand up the first version of a Pico-hosted
rover status website (`rover_server.py`), so that live wheel speed and direction are visible on a
laptop browser with no serial cable, not just printed to the console. This website is deliberately
built small and reusable — Classes 4, 5, and 6 will each add more fields to this same site rather
than building a new one.

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
* Wire a Slot Type IR Optocoupler at each driven wheel (`GP16`/`GP17`) and explain how its slotted
  fork and onboard LM393 comparator turn a spinning encoder disc into a clean digital pulse train
  the Pico can count directly, no debouncing required
* Write and use `wheel_odometry.py`, converting counted ticks into real wheel speed in cm/s using
  the 67mm wheel diameter, and explain why a single-slot optocoupler alone cannot tell direction —
  and why pairing tick rate with the last direction commanded through `motor_driver.drive()` is a
  reasonable stand-in
* Stand up `rover_server.py`, the first version of a Pico-hosted rover status website: join WiFi,
  run `adafruit_httpserver`, and serve live wheel speed/direction on a `/data.json` route and a
  simple webpage, viewable from a laptop browser with no serial cable

## 3. Preparation Checklist

* **1-2 days before:** Confirm every student's Class 1 and Class 2 circuits are still intact and
  power up — a quick visual/serial spot-check, not a rebuild. (~15 min)
* **1-2 days before:** Verify `adafruit_motor` (already used in Class 2) is present in each
  student's Library Bundle folder; no new library is required for the DRV8833 itself since
  `motor_driver.py` is course-provided source, not a separate PyPI/Bundle package. (~5 min)
* **1-2 days before:** Verify `adafruit_httpserver` is present in each student's Library Bundle
  folder — this is new starting this Class. `wheel_odometry.py`'s tick counting uses only the
  built-in `countio` module, so it needs no separate library. (~5 min)
* **1-2 days before:** Confirm classroom WiFi network name/password and test that the venue's
  network allows device-to-device traffic on the local subnet (some guest/school networks block a
  laptop from reaching another device's IP) — this is the single biggest risk to the website
  working at all, and is worth confirming days ahead, not day-of. (~15 min)
* **1-2 days before:** Charge or freshly stock 9V batteries — one per student workstation, plus 2-3
  spares. Confirm each battery clip and 5V buck converter module (if used for other onboard power)
  is present and wired correctly. (~15 min)
* **Day of, before students arrive:**
  * Set out one DRV8833 breakout board, one 9V battery with clip, two Slot Type IR Optocoupler
        modules, and continued access to each workstation's existing breadboard and chassis kit at
        each workstation.
  * Pre-fill each student's `settings.toml` with the classroom WiFi SSID/password (`WIFI_SSID`,
        `WIFI_PASSWORD`) ahead of time, or write them on the board — don't spend Class time on WiFi
        credential typos. (~10 min)
  * Measure and mark a 12-inch square and a 12-inch-diameter circle on the floor or a large sheet
        of paper/tape at 2-3 shared "test tracks" around the room — students calibrate against these
        visually, not on their own workstation surface. (~15 min)
  * Pre-build one reference circuit (DRV8833 + both motors + both optocouplers) at the instructor
        bench and test `class-3-code-1.py` (`motor_driver.py`) through `class-3-code-4.py`
        (`rover_server.py`) end-to-end, including a rough calibration pass on `SPEED`,
        `SECONDS_PER_INCH`, `SECONDS_PER_90_DEGREES`, and `SLOTS_PER_REV` so you know what a
        realistic first attempt — and a realistic wheel-speed reading — look like. Load `/data.json`
        in a browser from a laptop on the same network to confirm the website actually works before
        Class. (~30 min)
  * Have spare DRV8833 boards, motor leads, optocoupler modules, and 9V batteries on hand — a dead
        or weak 9V battery is the single most common "my motors barely move" complaint in this Class.
* **Have ready:** A short list of discussion prompts for "what's missing?" and "does knowing wheel
  speed fix everything?" (see Direct Teaching and Independent Work below), and the shared test-track
  locations communicated to students at the start of Guided Practice.

## 4. Materials & Components

Per-student unless noted. Component names only — see the course Bill of Materials for costs,
quantities, and sourcing.

| Component | Purpose This Class |
| :---------- | :-------------------- |
| Raspberry Pi Pico 2 W (with header) | Microcontroller running CircuitPython |
| DRV8833 Dual H-Bridge DC/Stepper Motor Driver Breakout Board | Drives both DC gearbox motors' speed and direction from PWM logic signals |
| Emo Smart Robot Car Chassis Kit (DC gearbox motors + wheels) | The two motors under test, and the chassis they drive — its wheels' molded-in encoder discs are what today's optocouplers read |
| 9V battery clip and 9V battery | Separate power supply for the motors, independent of the Pico's logic power |
| Slot Type IR Optocoupler for Motor Speed (2 per student) | Reads each driven wheel's built-in encoder disc for wheel-odometry tick counting |
| Breadboard (830-point, from Class 1) | Circuit assembly surface — Class 1 and 2 circuits stay on it, untouched |
| Dupont jumper wires (shared) | Point-to-point wiring |
| USB cable (student-supplied, from Pre-Class) | Power + serial connection to laptop |
| Windows 11 laptop with Mu or Thonny (student-supplied) | Edit and run CircuitPython code, and browse to each Pico's rover status website |
| Classroom WiFi network (shared) | The Pico 2 W joins this network to host the rover status website |
| Shared: tape/marked 12-inch square and circle test tracks | Reference targets for the square/circle milestone |

## 5. Class Timeline

**Pacing note:** This Class packs two new sensors and a first web server into a 120-min slot. If a
group is running behind by the end of Guided Practice, cut from Independent Work's optional
"faster pairs" extensions first (they're bonus, not milestone-required), not from Steps 1-4.

### 5a. Warm-up / Hook — ~5 min

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

### 5b. Introduction — ~5 min

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

### 5c. Direct Teaching — ~15 min

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

**Concept 5 — How the slot IR optocoupler measures wheel speed (Theory of Operation, brief).**
Each optocoupler module is a small IR LED and phototransistor facing each other across a slot,
plus an onboard LM393 comparator. The chassis kit's wheel has an encoder disc with alternating
slots and teeth molded around its rim; as the wheel spins, each tooth interrupts the LED-to-
phototransistor beam once per slot. The LM393 comparator turns that raw analog interruption into a
clean digital HIGH/LOW pulse — no debouncing needed the way the Class 1 switch/encoder needed it,
since this is a much faster, cleaner signal straight off a comparator chip, not a noisy mechanical
contact.

*Step-by-step decomposition of one speed reading:*

1. Count pulses ("ticks") from one optocoupler over a fixed time window (`wheel_odometry.py` uses a
   short sampling interval, not a running total).
2. Divide ticks by `SLOTS_PER_REV` (measured by counting the disc's own slots) to get wheel
   revolutions in that window.
3. Multiply revolutions by the wheel's circumference — `WHEEL_DIAMETER_MM = 67`, so
   circumference ≈ 21.05cm — to get distance traveled by that wheel in the window.
4. Divide by the window's length in seconds to get speed in cm/s.
5. Repeat independently for the other wheel's optocoupler.

**Concept 6 — Why one slotted optocoupler can't tell you direction.**
Ask: "You just counted ticks and got a speed. Can you tell from that alone whether the wheel is
spinning forward or backward?" (No — a tick is a tick either way.) A single-slot optocoupler only
reports *that* the beam was interrupted, not *which way* the disc was moving when it happened. A true
quadrature encoder solves this with a second sensor offset out of phase from the first, so the two
pulse trains' relative timing reveals direction — this course's single-optocoupler-per-wheel setup
doesn't have that. Instead, `wheel_odometry.py` borrows direction from `motor_driver.py`: the code
already knows whether it last told Motor A/B to spin forward or reverse (`motor_driver.drive()`
records this), so pairing that last-commanded direction with the optocoupler's measured tick rate is
a reasonable, if imperfect, stand-in for a true direction sensor — it confirms the wheel is turning
(or not, or slower than commanded), but assumes the wheel is obeying the last command it was given.

**Concept 7 — What it means for the Pico to "host a website" (Theory of Operation, brief).**
The websites students normally visit are hosted on a server in a data center far away, reached over
the internet. Today's website is the opposite: the Pico 2 W's own WiFi radio joins the classroom
network, runs a tiny HTTP server (`adafruit_httpserver`) directly in CircuitPython, and answers
requests at its own local IP address — the server, the sensor, and the thing being measured are all
in the student's hand. `rover_server.py` serves two things at that address: a `/data.json` route
(the current wheel speed/direction, as machine-readable JSON) and a simple HTML page that polls
`/data.json` every fraction of a second and displays it — so any laptop on the same network can watch
live wheel telemetry with no serial cable at all.

### 5d. Guided Practice — ~60 min

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
| Optocoupler A signal out (Motor A wheel) | `GP16` |
| Optocoupler B signal out (Motor B wheel) | `GP17` |
| Both optocouplers `VCC` | Pico `3V3` |
| Both optocouplers `GND` | Pico `GND` |

**Checkpoint 1:** Before writing any code, have every pair trace their own wiring against the
table above out loud to a neighbor, and specifically confirm the Pico's `GND` is jumpered to the
DRV8833's `GND` — this is the wiring mistake that produces the most confusing symptoms later.
Wiring mistakes found now save debugging time later. The two optocouplers can be wired now too, but
leave them unmounted at each wheel until Step 3, once each disc's slots have been counted.

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

# Last-commanded direction per channel: -1 reverse, 0 stopped, 1 forward.
# A single-slot optocoupler can measure tick RATE but not direction (see
# Direct Teaching, Concept 6) -- wheel_odometry.py reads these two values
# to pair with its measured speed.
last_direction_a = 0
last_direction_b = 0


def _clamp(throttle):
    if throttle is None:
        return None
    return max(-MAX_THROTTLE, min(MAX_THROTTLE, throttle))


def _sign(throttle):
    if not throttle:
        return 0
    return 1 if throttle > 0 else -1


def drive(left, right):
    """left/right: -1.0 (full reverse) to 1.0 (full forward), or None to coast."""
    global last_direction_a, last_direction_b
    motor_a.throttle = _clamp(left)
    motor_b.throttle = _clamp(right)
    last_direction_a = _sign(left)
    last_direction_b = _sign(right)


def stop():
    global last_direction_a, last_direction_b
    motor_a.throttle = 0.0  # 0.0 brakes; None coasts
    motor_b.throttle = 0.0
    last_direction_a = 0
    last_direction_b = 0
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

**Step 3 — wheel odometry: mount the optocouplers and read wheel speed.**
Mount each optocoupler so its slotted fork straddles the wheel's encoder disc without rubbing, and
count the disc's slots by hand (turn the wheel slowly and count) to set `SLOTS_PER_REV`. Load
`class-3-code-3.py` (save as `wheel_odometry.py`).

```python
# class-3-code-3.py  (save as wheel_odometry.py)
# Wheel-speed odometry via slot IR optocouplers -- tick RATE from GP16/GP17,
# direction borrowed from motor_driver's last-commanded state (see Concept 6).
import time
import board
import countio
import motor_driver

WHEEL_DIAMETER_MM = 67
SLOTS_PER_REV = 20  # [VERIFY] -- count the encoder disc's slots on your wheel
WHEEL_CIRCUMFERENCE_CM = (WHEEL_DIAMETER_MM / 10) * 3.14159
SAMPLE_SECONDS = 0.25  # sampling window for one speed reading

counter_a = countio.Counter(board.GP16)  # Motor A wheel
counter_b = countio.Counter(board.GP17)  # Motor B wheel


def _ticks_to_cms(ticks):
    revolutions = ticks / SLOTS_PER_REV
    return (revolutions * WHEEL_CIRCUMFERENCE_CM) / SAMPLE_SECONDS


def read_speed():
    """Sample both optocouplers over SAMPLE_SECONDS; return
    (speed_left_cms, dir_left, speed_right_cms, dir_right)."""
    counter_a.count = 0
    counter_b.count = 0
    time.sleep(SAMPLE_SECONDS)
    speed_left = _ticks_to_cms(counter_a.count)
    speed_right = _ticks_to_cms(counter_b.count)
    return (speed_left, motor_driver.last_direction_a,
            speed_right, motor_driver.last_direction_b)
```

Test it with a short scratch loop that drives forward and prints `read_speed()` each cycle:

```python
import motor_driver
import wheel_odometry

motor_driver.drive(0.5, 0.5)
for _ in range(10):
    print(wheel_odometry.read_speed())
motor_driver.stop()
```

**What to watch for:** A speed reading of `0.0` while the wheel is visibly spinning almost always
means the optocoupler's slot isn't actually straddling the disc — remount it, don't assume the code
is wrong first. A reading that's wildly too high or low usually means `SLOTS_PER_REV` was miscounted
— recount the disc's slots by hand.

**Checkpoint 3:** Every pair should see both `speed_left_cms` and `speed_right_cms` rise above zero
while driving forward, and the `dir_left`/`dir_right` values flip from `1` to `-1` when the car is
told to reverse — this is the moment students see measured speed and commanded direction combine.

**Step 4 — first version of the rover status website.**
Load `class-3-code-4.py` (save as `rover_server.py`) and add `WIFI_SSID`/`WIFI_PASSWORD` to
`settings.toml` if not already pre-filled.

```python
# class-3-code-4.py  (save as rover_server.py)
# Pico-hosted rover status website -- joins WiFi, serves /data.json plus a
# minimal page that polls it. First version; Classes 4-6 extend this file.
import os
import wifi
import socketpool
from adafruit_httpserver import Server, Request, Response, JSONResponse
import wheel_odometry

wifi.radio.connect(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"))
print("rover server -- listening at", wifi.radio.ipv4_address)

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool)

STATUS_PAGE = """<!doctype html><html><body>
<h1>Rover Status</h1>
<pre id="data">loading...</pre>
<script>
setInterval(() => fetch('/data.json').then(r => r.json())
    .then(d => document.getElementById('data').textContent =
        JSON.stringify(d, null, 2)), 500);
</script>
</body></html>"""


@server.route("/data.json")
def data_json(request: Request):
    speed_left, dir_left, speed_right, dir_right = wheel_odometry.read_speed()
    return JSONResponse(request, {
        "speed_left_cms": speed_left,
        "dir_left": dir_left,
        "speed_right_cms": speed_right,
        "dir_right": dir_right,
    })


@server.route("/")
def index(request: Request):
    return Response(request, STATUS_PAGE, content_type="text/html")


server.start(str(wifi.radio.ipv4_address))

while True:
    server.poll()
```

**What to watch for:** If the server never connects, double-check `settings.toml`'s WiFi credentials
first, then confirm the laptop is on the *same* network as the Pico. If the page loads but never
updates, the fetch loop is running but the browser may be caching — a hard refresh usually fixes it.

**What "done" looks like for this segment:** Every pair can open a browser to their Pico's printed
IP address, see the `/data.json` fields update live as the car drives, and describe in one sentence
why direction shown on the page is "what we last told it to do," not something separately measured.

### 5e. Independent Work — ~25 min

**What to do:** Students (in pairs where possible) take their car to a shared test track and run
`drive_square()` and `drive_circle()` repeatedly, adjusting `SPEED`, `SECONDS_PER_INCH`, and
`SECONDS_PER_90_DEGREES` between attempts to get closer to the marked 12-inch targets, this time
watching the rover status website on a laptop while the car drives instead of only the serial
console. After each attempt, have them note in their build journal: was the error mostly in the
straight-line distance, the turn angle, or both — and did the website's live speed readings for the
left and right wheel match each other, or reveal one wheel running slower? Faster pairs can:

* Deliberately swap in a weaker or more depleted 9V battery mid-session and observe how much the
  calibration constants drift, and how the website's speed readings drop — a direct, hands-on
  demonstration of voltage sag.
* Try the square/circle attempt on a different floor surface (carpet vs. tile) and discuss wheel
  slip/friction as a distinct cause from voltage sag or timing — watch whether one wheel's website
  speed reading drops relative to the other during a slip.
* Begin sketching (on paper, no code yet) what information — beyond wheel speed — would let the car
  correct its own path instead of just guessing. (Heading/orientation is still missing; that's
  Class 4.)

**What to watch for:** The most common failure at this stage is a car that pulls consistently to one
side even when both throttle values are equal — almost always a real mechanical difference between
the two motors/gearboxes (not a bug), and a good moment to point out that hardware variation is part
of why open-loop control drifts.

**Time check:** At the 15-minute mark, do a quick show-of-hands: "Who has completed at least one
full square and one full circle attempt, regardless of accuracy?" Redirect instructor attention to
pairs still stuck on the basic drive() test.

### 5f. Closing / Wrap-up — ~10 min

**What to do:** Ask 2-3 volunteers to run their best square and circle attempt on a shared test
track for the group, with the rover status website pulled up on the projector so everyone watches
live wheel speed/direction alongside the run. Open the "what is missing?" discussion: have the group
name the specific, separate causes of drift — no wheel/heading feedback, battery voltage sag, wheel
slip/friction — rather than settling for one vague "it's not accurate enough." Then push the
discussion one step further, now that wheel odometry exists: does knowing each wheel's real speed
fix *all* of that drift? Draw out that it catches slip/stall (a wheel spinning slower than commanded,
or not at all) but says nothing about heading/orientation — that gap isn't closed until the Class 4
IMU.

**What to say:** "Every one of you just built a car that can move with real purpose, and now you can
actually watch each wheel's real speed and direction live, on a webpage your Pico is serving all by
itself. But notice what that still doesn't tell you — which way the *car* is pointed. Knowing your
wheels are turning correctly isn't the same as knowing you're heading the right direction. That's
exactly the gap the IMU fills next Class, and it'll show up on this same website."

**Preview next Class:** Class 4 reuses none of today's, Class 1's, or Class 2's pins — it's the
LSM9DS1 9-DOF IMU over I2C on `GP0`/`GP1`, while today's motor driver circuit, both optocouplers, the
rover status website, and both prior circuits stay untouched and running. Class 4 extends
`rover_server.py` with orientation data rather than building a new website — point students to the
Class 4 references in the syllabus if they want to read ahead.

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
| Wheel speed reads `0.0` while the wheel is visibly spinning | Optocoupler's slot isn't straddling the encoder disc, or its wiring is loose | Remount the optocoupler so the disc's teeth pass through the slot; reseat `VCC`/`GND`/signal jumpers |
| Wheel speed reading is wildly too high or too low | `SLOTS_PER_REV` miscounted for that wheel's disc | Recount the disc's slots by hand and update `SLOTS_PER_REV` |
| Direction shown never changes even when the car reverses | Code is reading a stale `motor_driver.last_direction_a`/`_b` value, or `wheel_odometry.py` was saved before `motor_driver.py` was updated with direction tracking | Confirm `motor_driver.py` on the CIRCUITPY drive includes the `last_direction_a`/`_b` tracking shown in `class-3-code-1.py` |
| `wifi.radio.connect()` hangs or raises `ConnectionError` | Wrong SSID/password in `settings.toml`, or the classroom network blocks the device | Double-check `settings.toml`; confirm with the pre-Class network test that device-to-device traffic is allowed |
| Website never loads in the browser, but the Pico prints an IP address | Laptop is on a different network/VLAN than the Pico | Confirm the laptop is joined to the same classroom WiFi network as the Pico |
| Website loads once but never updates | `server.poll()` not being called every loop, or browser is caching the page | Confirm the `while True: server.poll()` loop is running; try a hard refresh |

## 7. Age Differentiation Notes

**Younger students (12-14) and their parent/guardian:** Provide the pin table above pre-printed
and laminated at the workstation so it's a lookup, not a memorization task. Pair a younger
student's fine-wiring work (especially the DRV8833's output-to-motor-lead connections and the
optocoupler mounting) with the parent/guardian's help holding the chassis steady. Start from all
four `class-3-code-*.py` files already loaded as starting points, and have them focus on tuning the
calibration constants (`SPEED`, `SECONDS_PER_INCH`, `SECONDS_PER_90_DEGREES`, `SLOTS_PER_REV`) by
trial and error rather than writing the functions from scratch. For the website, it's enough for
them to type the pre-filled WiFi credentials into `settings.toml` and confirm the page loads —
treat `rover_server.py`'s internals as "trust the library" material this Class.

**Older students (15-18) and adults:** Have them type `motor_driver.py`'s `drive()`/`stop()`
functions themselves from the wiring table and the locked-antiphase explanation, rather than
starting from the provided file. Once the square/circle milestone is met, challenge them to log
each attempt's actual measured dimensions (with a tape measure) against the target, across at least
three battery charge levels, and see if they can predict how far off the next attempt will be. For
wheel odometry, challenge them to explain in their own words (not read from the lesson) why a
quadrature encoder's second, out-of-phase sensor would remove the need to borrow direction from
`motor_driver.py`, and have them add a `/` route to `rover_server.py` that also prints the last
raw tick counts (not just derived speed), as a small extension beyond the provided code.

## 8. Assessment

**Milestone Assignment (per syllabus, Phase 2 / Class 3):** Car reliably drives a 12-inch square and
a 12-inch-diameter circle, with live wheel-speed telemetry visible on the terminal and on the Pico's
own status webpage.

**What "complete" looks like:** The student can run `drive_square(12)` and `drive_circle(12)` on a
shared test track and produce a shape recognizably close to the 12-inch target — this is a
completion-based, "does it work in the real world" check, not a precision measurement. Minor drift
is expected and is itself part of the lesson. In addition, the student can open a browser to their
Pico's status website and point to live-updating wheel speed and direction values while the car
drives.

**How to give feedback without scoring:** Ask the student to point at the marked test track and
narrate, specifically, what's causing the gap between their car's path and the target ("is this a
timing problem, a battery problem, or a slip problem — or all three?") rather than checking a box.
Separately, ask them to explain in their own words why the website's direction reading isn't
measured by the optocoupler itself. If a pair can't get a recognizable square or circle, or a
working website, in the time available, that's fine — have them bring a working version to the
start of Class 4 and note it in their build journal.

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
* Keep all four code files (`class-3-code-1.py`/`motor_driver.py` through
  `class-3-code-4.py`/`rover_server.py`) on a shared drive/USB stick so a student who breaks their
  working file can recover instantly instead of losing class time.
* Pre-fill WiFi credentials in every student's `settings.toml` (or write them on the board) — WiFi
  password typos are a much bigger time sink than any wiring mistake in this Class, and have nothing
  to teach once fixed.
* Confirm the venue's network allows device-to-device traffic *before* Class day (see Preparation
  Checklist) — a network that only allows internet-bound traffic will silently block every laptop
  from reaching a Pico's website, and this is very hard to diagnose live, mid-Class.
* When demonstrating the "does wheel speed fix everything?" discussion at Closing, deliberately pick
  the car up and spin one wheel by hand while the website is open on the projector — students will
  see that wheel's speed jump on the page while the car obviously isn't moving forward, a concrete
  demonstration of what odometry does and doesn't tell you.

## 10. Resources & References

* [DC Motor Examples - Raspberry Pi Pico (CMU Creative Soft Robotics)][01] — worked examples of DC
  motor control from a Pico
* [Driving A DC Motor With CircuitPython][02] — background on PWM-based DC motor speed control
* [Adafruit CircuitPython Motor Library — API Reference][03] — the `adafruit_motor.motor.DCMotor`
  API used in `class-3-code-1.py`
* [Adafruit DRV8833 DC/Stepper Motor Driver Breakout Board][04] — the motor driver used this Class,
  including its locked-antiphase and phase/enable control modes
* [Slot Type IR Optocoupler for Motor Speed Detection - Product Page][05] — the wheel-odometry
  sensor used in `class-3-code-3.py`
* [Using an IR Slotted Optical Switch (Adafruit Learn)][06] — background on how a slotted
  optocoupler/comparator pair encodes motion as a digital pulse train
* [Wheel Encoders and Odometry (ROS/robotics primer)][07] — background on tick-to-speed conversion
  and why a single sensor per wheel can't resolve direction
* [Raspberry Pi Pico W Asynchronous Web Server – MicroPython Code][08] — background on hosting a
  small web server directly from a Pico's WiFi radio
* [`adafruit_httpserver` — API Reference][09] — the `Server`/`Request`/`Response`/`JSONResponse` API
  used in `class-3-code-4.py`

---

[01]:https://courses.ideate.cmu.edu/16-480/s2026/text/code/pico-motor.html
[02]:https://www.woolseyworkshop.com/2022/07/25/driving-a-dc-motor-with-circuitpython/
[03]:https://docs.circuitpython.org/projects/motor/en/latest/api.html
[04]:https://learn.adafruit.com/adafruit-drv8833-dc-stepper-motor-driver-breakout-board
[05]:https://www.amazon.com/dp/B0B2NSQJDL
[06]:https://learn.adafruit.com/ir-breakbeam-sensors
[07]:https://articulatedrobotics.xyz/mobile-robot-8-odometry/
[08]:https://electrocredible.com/raspberry-pi-pico-w-web-server-asynchronous-micropython/
[09]:https://docs.circuitpython.org/projects/httpserver/en/latest/api.html
