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
motors from their own 9V battery rather than the Pico's logic power — that same 9V battery, stepped
down through a 5V buck converter, also now supplies the Pico's own `VSYS` power input. After a
simple forward/reverse/stop test, students try to drive the car in a 12-inch square and a 12-inch-diameter circle using
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

For pairs who finish early, an optional stretch closes one more piece of the gap: a car driven at
equal throttle curves, because no two motors are identical. Students use their new wheel-speed
readings to make the car correct itself — measure both wheels, compare, and nudge the faster wheel
down (closed-loop control) — and measure the sideways drift with and without feedback. It also sets
up Class 4: matching wheel speeds isn't the same as going straight, which needs a heading sensor.

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
* Wire a Slot Type IR Optocoupler at each driven wheel (`GP19`/`GP17`) and explain how its slotted
  fork and onboard LM393 comparator turn a spinning encoder disc into a clean digital pulse train
  the Pico can count directly, no debouncing required
* Write and use `wheel_odometry.py`, converting counted ticks into real wheel speed in cm/s using
  the 67mm wheel diameter, and explain why a single-slot optocoupler alone cannot tell direction —
  and why pairing tick rate with the last direction commanded through `motor_driver.drive()` is a
  reasonable stand-in
* Stand up `rover_server.py`, the first version of a Pico-hosted rover status website: broadcast
  the Pico's own WiFi network (access point mode), run `adafruit_httpserver`, and serve live wheel
  speed/direction on a `/data.json` route and a simple webpage, viewable from a laptop joined to
  the Pico's network with no serial cable
* (Stretch, optional) Make the car drive straight using wheel-speed feedback — compare the two
  wheels' speeds and nudge the faster one down — measure the sideways drift with and without it, and
  explain what wheel feedback fixes (mismatched motors) and what only a heading sensor can (Class 4)

## 3. Preparation Checklist

* **1-2 days before:** Confirm every student's Class 1 and Class 2 circuits are still intact and
  power up — a quick visual/serial spot-check, not a rebuild. (~15 min)
* **1-2 days before:** Verify `adafruit_motor` (already used in Class 2) is present in each
  student's Library Bundle folder; no new library is required for the DRV8833 itself since
  `motor_driver.py` is course-provided source, not a separate PyPI/Bundle package. (~5 min)
* **1-2 days before:** Verify `adafruit_httpserver` is present in each student's Library Bundle
  folder — this is new starting this Class. `wheel_odometry.py`'s tick counting uses only the
  built-in `countio` module, so it needs no separate library. (~5 min)
* **1-2 days before:** Confirm every Pico 2 W is running the CircuitPython build made for
  "Raspberry Pi Pico 2 W" — the plain "Pico 2" build has no `wifi` module, and `rover_server.py`
  fails with `ImportError: no module named 'wifi'`. Also confirm the `adafruit_httpserver` library
  is present. This replaces the old classroom-network risk: the Pico now creates its own network
  (access point mode), so no venue WiFi is needed — but a laptop joined to it loses regular
  internet access. (~15 min)
* **1-2 days before:** Assign each student a *unique* Pico network name (e.g. `RoverCar-01`,
  `RoverCar-02`, ...) — a dozen Picos broadcasting the same name in one room will collide.
  Passwords must be at least 8 characters or `start_ap()` rejects them. (~10 min)
* **1-2 days before:** Charge or freshly stock 9V batteries — one per student workstation, plus 2-3
  spares. Confirm each battery clip and 5V buck converter module is present and wired: buck
  converter input from the 9V battery, buck converter output to the Pico's `VSYS` pin. (~15 min)
* **Day of, before students arrive:**
  * Set out one DRV8833 breakout board, one 9V battery with clip, one 5V buck converter module,
        two Slot Type IR Optocoupler modules, and continued access to each workstation's existing
        breadboard and chassis kit at each workstation.
  * Pre-fill each student's `settings.toml` with their unique Pico network name and password
        (`CIRCUITPY_WIFI_AP_SSID`, `CIRCUITPY_WIFI_AP_PASSWORD`, password at least 8 characters)
        ahead of time, or write them on the board — don't spend Class time on credential typos.
        (~10 min)
  * Measure and mark a 12-inch square and a 12-inch-diameter circle on the floor or a large sheet
        of paper/tape at 2-3 shared "test tracks" around the room — students calibrate against these
        visually, not on their own workstation surface. (~15 min)
  * Lay one long (about 6 ft) straight masking-tape line on a smooth floor for the stretch, and run
        your reference car through it open-loop and with feedback (`class-3-code-5.py`) so you know
        the realistic sideways drift and a workable `KP` for this model of car. (~15 min)
  * Pre-build one reference circuit (DRV8833 + both motors + both optocouplers) at the instructor
        bench and test `class-3-code-1.py` (`motor_driver.py`) through `class-3-code-4.py`
        (`rover_server.py`) end-to-end, including a rough calibration pass on `SPEED`,
        `SECONDS_PER_INCH`, `SECONDS_PER_90_DEGREES`, and `SLOTS_PER_REV` so you know what a
        realistic first attempt — and a realistic wheel-speed reading — look like. Join a laptop to
        the reference Pico's own network and load `http://192.168.4.1/data.json` in a browser to
        confirm the website actually works before Class. (~30 min)
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
| 9V battery clip and 9V battery | Power supply for the motors (raw, via `VM`) and, through the buck converter, the Pico's own logic power (regulated 5V, via `VSYS`) |
| 5V Buck Converter Module | Steps the 9V battery down to a regulated 5V for the Pico's `VSYS` power input — separate from the motors' raw, unregulated 9V `VM` supply |
| Slot Type IR Optocoupler for Motor Speed (2 per student) | Reads each driven wheel's built-in encoder disc for wheel-odometry tick counting |
| Breadboard (830-point, from Class 1) | Circuit assembly surface — Class 1 and 2 circuits stay on it, untouched |
| Dupont jumper wires (shared) | Point-to-point wiring |
| USB cable (student-supplied, from Pre-Class) | Power + serial connection to laptop |
| Windows 11 laptop with Mu or Thonny (student-supplied) | Edit and run CircuitPython code, and browse to each Pico's rover status website (after joining the Pico's own WiFi network) |
| Masking tape and a tape measure (shared) | Stretch only: a straight start line, and measuring the car's sideways drift |
| (no classroom WiFi needed) | The Pico 2 W broadcasts its own network (access point mode) to host the rover status website |
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
5. The chip's `nSLEEP` pin must be held HIGH or it ignores every PWM signal — the Adafruit
   breakout has **no** onboard pull-up, so it gets a jumper to Pico `3V3`. (Symptom if forgotten:
   code runs and prints normally, motors never move.) Tying it high permanently also means a
   latched overcurrent/thermal fault — shared by both H-bridges — can only be cleared by
   power-cycling the DRV8833, not from code.
6. `class-3-code-1.py` (`motor_driver.py`) wraps this pattern behind a simple `drive(left, right)`
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
The motors run off the 9V battery's raw, unregulated voltage (`VM` on the DRV8833) — separate from
the Pico's own power, which now comes through a 5V buck converter (`VSYS`) or USB, either regulated
to a clean 5V. Keeping the motors on the raw, unregulated rail (rather than sharing the Pico's
regulated 5V) protects the Pico's logic from motor electrical noise and current spikes.
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

*Pin-choice gotcha:* `countio.Counter` on the RP2040/RP2350 is built on the chip's PWM hardware,
which only counts on a PWM **Channel B** pin — the odd-numbered GPIOs. `GP16` is Channel A and
raises `RuntimeError: Pin must be on PWM Channel B`, which is why the optocouplers use `GP17` and
`GP19`, not the "obvious" `GP16`/`GP17` pair.

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
the internet, and a laptop *joins* an existing network to reach them. Today's website flips that:
the Pico 2 W's own WiFi radio broadcasts its *own* network (access point mode) that the laptop joins
directly — no router or internet involved. The Pico then runs a tiny HTTP server
(`adafruit_httpserver`) directly in CircuitPython and answers requests at its own IP address
(typically `192.168.4.1`) — the network, the server, the sensor, and the thing being measured are
all in the student's hand. `rover_server.py` serves two things at that address: a `/data.json` route
(the current wheel speed/direction, as machine-readable JSON) and a simple HTML page that polls
`/data.json` every fraction of a second and displays it — so any laptop joined to the Pico's
network can watch live wheel telemetry with no serial cable at all. Two details to point out: the
server must be started on port 80 explicitly (the library's default is 5000, which a browser typing
a bare IP won't reach), and while joined to the Pico's network the laptop loses normal internet.

**The mission of this phase.** Spinning a wheel by hand only proves the plumbing works. The real
goal is a website that reports what the rover does *on its own* — once code is driving the motors,
the same page should show speed and direction changing with no human touching a wheel. Combining
driving and serving in one program (without a blocking `time.sleep()` freezing the page) is the
design problem Classes 5-6 build toward.

### 5d. Guided Practice — ~60 min

Instructor builds along on the projector; students wire up and test in parallel.

**Wiring — third circuit of the course, alongside (not replacing) Class 1 and 2's.** Leave both
prior circuits exactly as-is on the breadboard; today's wiring uses entirely new pins, plus a 9V
battery that (through a buck converter) now also powers the Pico itself.

| Component | Pico 2 W Pin |
| :---------- | :------------- |
| DRV8833 `AIN1` (Motor A) | `GP9` |
| DRV8833 `AIN2` (Motor A) | `GP10` |
| DRV8833 `BIN1` (Motor B) | `GP11` |
| DRV8833 `BIN2` (Motor B) | `GP12` |
| DRV8833 `nSLEEP` (labelled `SLP` on some boards) | Pico `3V3` (must be tied HIGH — no onboard pull-up) |
| DRV8833 `VM` (motor power) | 9V battery `+` |
| DRV8833 `GND` | 9V battery `-` **and** Pico `GND` (common ground) |
| DRV8833 `AOUT1`/`AOUT2` | Motor A leads |
| DRV8833 `BOUT1`/`BOUT2` | Motor B leads |
| Buck converter IN+/IN− | 9V battery `+`/`−` |
| Buck converter OUT+/OUT− | Pico `VSYS` / `GND` (common ground) |
| Optocoupler A signal out (Motor A wheel) | `GP19` (must be a PWM Channel B / odd-numbered pin) |
| Optocoupler B signal out (Motor B wheel) | `GP17` |
| Both optocouplers `VCC` | Pico `3V3` |
| Both optocouplers `GND` | Pico `GND` |
| (optional) 1000uF electrolytic capacitor across `VM`/`GND` at the DRV8833 | Buffers motor current spikes so battery sag doesn't brown out the Pico |

**Checkpoint 1:** Before writing any code, have every pair trace their own wiring against the
table above out loud to a neighbor, and specifically confirm two things: the Pico's `GND` is
jumpered to the DRV8833's `GND` (a missing common ground causes the most confusing symptoms later),
and `nSLEEP` is jumpered to Pico `3V3` (a missing jumper means code that runs and prints normally
while the motors never move). Wiring mistakes found now save debugging time later. The two optocouplers can be wired now too, but
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

print("both wheels forward")
motor_driver.drive(0.5, 0.5)
time.sleep(2)

print("both wheels reverse")
motor_driver.drive(-0.5, -0.5)
time.sleep(2)

print("turn (left wheel A backward, right wheel B forward)")
motor_driver.drive(-0.5, 0.5)
time.sleep(2)

print("stop")
motor_driver.stop()
```

**What to watch for:** A motor that spins the wrong direction almost always means its two leads are
swapped at `AOUT1`/`AOUT2` (or `BOUT1`/`BOUT2`) — swap the two wires, don't fight it in code, unless
the class wants to practice fixing it in software (swap the `+1`/`-1` sign instead). If *neither*
motor moves but the prints appear, check the `nSLEEP` jumper first. If everything works over USB but
fails or the optocoupler LED flickers on battery alone, the 9V battery is sagging under motor load —
try a fresh battery before anything else.

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
# Wheel-speed odometry via slot IR optocouplers -- tick RATE from GP19/GP17,
# direction borrowed from motor_driver's last-commanded state (see Concept 6).
import time
import board
import countio
import motor_driver

WHEEL_DIAMETER_MM = 67
SLOTS_PER_REV = 20  # [VERIFY] -- count the encoder disc's slots on your wheel
WHEEL_CIRCUMFERENCE_CM = (WHEEL_DIAMETER_MM / 10) * 3.14159
SAMPLE_SECONDS = 0.25  # sampling window for one speed reading

counter_a = countio.Counter(board.GP19)  # Motor A wheel -- must be a PWM Channel B pin
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

Test it with a short scratch loop that drives forward, then reverse, printing `read_speed()` each
cycle:

```python
import motor_driver
import wheel_odometry

motor_driver.drive(0.5, 0.5)
for _ in range(10):
    print(wheel_odometry.read_speed())

motor_driver.drive(-0.5, -0.5)
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
Load `class-3-code-4.py` (save as `rover_server.py`) and add `CIRCUITPY_WIFI_AP_SSID`/
`CIRCUITPY_WIFI_AP_PASSWORD` to `settings.toml` if not already pre-filled — these are the name and
password the student *chooses for the Pico's own network* (unique per student, password at least 8
characters), not the venue's WiFi credentials.

```python
# class-3-code-4.py  (save as rover_server.py)
# Pico-hosted rover status website -- broadcasts its own WiFi network (AP mode),
# serves /data.json plus a minimal page that polls it. First version; Classes 4-6
# extend this file.
import os
import wifi
import socketpool
from adafruit_httpserver import Server, Request, Response, JSONResponse
import wheel_odometry

wifi.radio.start_ap(
    os.getenv("CIRCUITPY_WIFI_AP_SSID"), os.getenv("CIRCUITPY_WIFI_AP_PASSWORD")
)
print("rover server -- broadcasting WiFi network:", os.getenv("CIRCUITPY_WIFI_AP_SSID"))
print("rover server -- listening at", wifi.radio.ipv4_address_ap)

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


server.start(str(wifi.radio.ipv4_address_ap), port=80)

print("Class 3, Phase 4 -- rover status website starting...")
while True:
    server.poll()
```

**What to watch for:** The laptop must first join the Pico's network (named by
`CIRCUITPY_WIFI_AP_SSID`) in its WiFi settings *before* the browser can reach the printed IP address
— and will lose normal internet while joined. If the server never starts, check the password is at
least 8 characters. If the browser reports "site can't be reached" but `ping` to the Pico works,
the server is on the wrong port — confirm `server.start(..., port=80)`. If the page loads but never
updates, the fetch loop is running but the browser may be caching — a hard refresh usually fixes it.

**What "done" looks like for this segment:** Every pair can join their Pico's network, open a
browser to its printed IP address, and see the `/data.json` fields update live. Two levels: (1) the
plumbing check — spin a wheel by hand and watch `speed_left_cms`/`speed_right_cms` respond; (2) the
mission — with the page still open, drive the car with code (e.g. `motor_driver.drive(0.5, 0.5)`
from the REPL) and watch the page update while the car moves under its own power. Each pair should
also describe in one sentence why direction shown on the page is "what we last told it to do," not
something separately measured — so spinning a wheel by hand moves the speeds but never the
direction fields.

### 5e. Independent Work — ~25 min

**What to do:** Students (in pairs where possible) take their car to a shared test track and run
`drive_square()` and `drive_circle()` repeatedly (`code.py` set to the driving code, same as Guided
Practice Step 2), adjusting `SPEED`, `SECONDS_PER_INCH`, and `SECONDS_PER_90_DEGREES` between
attempts to get closer to the marked 12-inch targets, watching the serial console for each move's
status messages the same way as Steps 1-2. After a few attempts, have each pair swap `code.py` to
the rover status website code (Step 4) and, with the car sitting still, spin each wheel by hand to
check the left and right wheel's live speed readings on the website — a quick telemetry check
between driving attempts, not something watched during the drive itself. After each square/circle
attempt, have them note in their build journal: was the error mostly in the straight-line distance,
the turn angle, or both — and, from that separate website check, did the left and right wheel speed
readings match each other, or reveal one wheel running slower? Faster pairs can:

* Deliberately swap in a weaker or more depleted 9V battery between attempts and observe how much
  the calibration constants drift for the driving code, then swap back to the website code and spin
  each wheel by hand to see the speed readings drop too — a direct, hands-on demonstration of
  voltage sag.
* Try the square/circle attempt on a different floor surface (carpet vs. tile) and discuss wheel
  slip/friction as a distinct cause from voltage sag or timing — then swap in the website code and
  spin each wheel by hand to check whether one wheel's speed reading is noticeably weaker than the
  other, consistent with the slip they just observed.
* **Stretch — make the car drive straight.** Once a pair has seen the car curve at equal throttle
  and confirmed (from the website check) that one wheel reads slower, hand them
  `class-3-code-5.py` and the comparison script below. They run the same tape line open-loop and
  then with wheel feedback, measuring the sideways drift each time and averaging three runs each.
  Then have them tune `KP`: too large and the car snakes (it's chasing one-tick measurement noise,
  about 4 cm/s in a quarter-second window); too small and it barely corrects.
* Begin sketching (on paper, no code yet) what information — beyond wheel speed — would let the car
  correct its own path instead of just guessing. (Heading/orientation is still missing; that's
  Class 4.)

```python
# class-3-code-5.py  (save as straight_drive.py)
# Drive straight by nudging the faster wheel down until both wheels turn at the same speed.
import time
import motor_driver
import wheel_odometry

BASE_THROTTLE = 0.5   # throttle both wheels start at
KP = 0.005            # [VERIFY] -- nudge per cm/s of speed difference; tune on your own car
MAX_TRIM = 0.2        # never slow a wheel by more than this


def drive_straight_feedback(seconds):
    trim = 0.0        # positive slows the left wheel, negative slows the right wheel
    end_time = time.monotonic() + seconds
    motor_driver.drive(BASE_THROTTLE, BASE_THROTTLE)

    while time.monotonic() < end_time:
        speed_left, _, speed_right, _ = wheel_odometry.read_speed()   # ~0.25 s per call
        error = speed_left - speed_right   # positive: left wheel is faster
        trim += KP * error                 # small nudge, remembered cycle to cycle
        trim = max(-MAX_TRIM, min(MAX_TRIM, trim))
        left = BASE_THROTTLE - max(trim, 0)    # slow only the faster wheel
        right = BASE_THROTTLE + min(trim, 0)
        motor_driver.drive(left, right)
        print("L:", round(speed_left, 1), "R:", round(speed_right, 1), "trim:", round(trim, 3))

    motor_driver.stop()
```

The comparison `code.py` runs the same line open-loop, gives 15 seconds to carry the car back, then
runs it with feedback:

```python
import time
import motor_driver
import straight_drive

motor_driver.drive(straight_drive.BASE_THROTTLE, straight_drive.BASE_THROTTLE)
time.sleep(4)
motor_driver.stop()
time.sleep(15)                                   # carry the car back to the start line
straight_drive.drive_straight_feedback(4)
```

**What to watch for:** The most common failure at this stage is a car that pulls consistently to one
side even when both throttle values are equal — almost always a real mechanical difference between
the two motors/gearboxes (not a bug), and a good moment to point out that hardware variation is part
of why open-loop control drifts — and to hand pairs that have noticed it the stretch above, which
fixes it properly instead of by hand-tuning throttle values. Note that the stretch and the website
can't run at the same time: both call `read_speed()` and would keep resetting each other's tick
counts, so it runs as its own `code.py`. If a pair's car curves *more* with feedback and `trim` runs
to `MAX_TRIM`, the correction is slowing the wrong wheel — check which optocoupler is on which pin.

**Time check:** At the 15-minute mark, do a quick show-of-hands: "Who has completed at least one
full square and one full circle attempt, regardless of accuracy?" Redirect instructor attention to
pairs still stuck on the basic drive() test.

### 5f. Closing / Wrap-up — ~10 min

**What to do:** Ask 2-3 volunteers to run their best square and circle attempt on a shared test
track for the group (`code.py` set to the driving code, as in Independent Work). Once the attempt
finishes, have that pair swap `code.py` to the rover status website code and, with the website
pulled up on the projector, spin a wheel by hand so everyone watches live wheel speed/direction
respond. Open the "what is missing?" discussion: have the group
name the specific, separate causes of drift — no wheel/heading feedback, battery voltage sag, wheel
slip/friction — rather than settling for one vague "it's not accurate enough." Then push the
discussion one step further, now that wheel odometry exists: does knowing each wheel's real speed
fix *all* of that drift? Draw out that it catches slip/stall (a wheel spinning slower than commanded,
or not at all) but says nothing about heading/orientation — that gap isn't closed until the Class 4
IMU. If a pair finished the stretch, have them run the tape line open-loop and then with feedback
for the group (about 2 minutes), and use it to draw the distinction: feedback made the *wheels*
match, which straightens out a mismatched-motor curve — but a wheel that slips on carpet can still
send a car with two "matching" wheels off course, and only knowing the car's heading would catch
that.

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
| Neither motor spins, but the console prints the moves normally | DRV8833 `nSLEEP` floating — the Adafruit breakout has no onboard pull-up, so the chip stays asleep | Jumper `nSLEEP` to Pico `3V3` |
| One motor doesn't spin | Loose wire on a DRV8833 output pin, or a dead motor | Reseat jumper wires; swap in a spare motor to isolate the fault |
| One motor dies on a command, then a previously-working motor also dies | Latched DRV8833 fault — a current spike (jam, short) tripped the shared overcurrent/thermal protection, disabling both bridges | Check for binding or shorted leads, then power-cycle the DRV8833 (reseat the 9V battery) |
| Both motors spin, but the car doesn't move (or barely moves) | `MAX_THROTTLE` set too low, or wheels not making contact with the floor | Raise `MAX_THROTTLE` in small steps; confirm chassis is set down properly |
| Motor spins the wrong direction | Motor leads swapped at `AOUT1`/`AOUT2` (or `BOUT1`/`BOUT2`) | Swap the two motor leads, or swap the sign of that motor's throttle in code |
| Both motors spin the same direction on a "turn" command | Motor B's leads wired with opposite polarity convention from Motor A | Swap Motor B's leads, or its throttle sign, so `+1` means the same physical direction for both |
| Logic behaves erratically even though wiring looks right | Missing common ground between the 9V battery circuit and the Pico | Add a jumper from DRV8833 `GND` to Pico `GND` |
| Pico doesn't power on when running off battery (no USB) | Buck converter miswired, or its output isn't reaching `VSYS` | Verify buck converter IN from 9V battery, OUT to Pico `VSYS`/`GND`; confirm buck converter's output trimpot (if adjustable) is set to 5V |
| Works over USB, but fails and the optocoupler LED flickers on battery alone | Battery sag: motor current spikes drag down the shared 9V battery and the buck converter feeding the Pico | Try a fresh 9V battery; if it persists, add a 470-1000uF capacitor across `VM`/`GND` |
| Square/circle attempt drifts wildly between runs on the same settings | Battery voltage sagging as it depletes during the session | Swap in a fresh 9V battery and re-calibrate `SPEED`/timing constants |
| Car pulls consistently to one side even at equal throttle | Real mechanical difference between the two gearbox motors — equal throttle isn't equal speed | Hand-tune left/right throttle as a quick fix, or use the wheel-feedback stretch (`class-3-code-5.py`) to fix it properly |
| Stretch: car snakes left and right, and `trim` jumps around | `KP` too large — the code chases one-tick measurement noise (about 4 cm/s) | Lower `KP` (try `0.003`), or raise `SAMPLE_SECONDS` in `wheel_odometry.py` to `0.5` |
| Stretch: car curves more than before, and `trim` runs to `MAX_TRIM` | Correction is slowing the wrong wheel — optocouplers/motors swapped relative to left/right | Confirm Motor A's optocoupler is on `GP19`, Motor B's on `GP17`, and Motor A is the left wheel |
| `ImportError: no module named 'motor_driver'` | `motor_driver.py` not saved to the CIRCUITPY drive alongside `code.py` | Confirm `class-3-code-1.py` was saved as `motor_driver.py` in the CIRCUITPY root, not left named `class-3-code-1.py` |
| `RuntimeError: Pin must be on PWM Channel B` when `wheel_odometry.py` loads | `countio.Counter` only works on PWM Channel B (odd-numbered) pins; `GP16` is Channel A | Use `GP19` (odd) for the Motor A optocoupler, in both wiring and code |
| Wheel speed reads `0.0` while the wheel is visibly spinning | Optocoupler's slot isn't straddling the encoder disc, or its wiring is loose | Remount the optocoupler so the disc's teeth pass through the slot; reseat `VCC`/`GND`/signal jumpers |
| Wheel speed reading is wildly too high or too low | `SLOTS_PER_REV` miscounted for that wheel's disc | Recount the disc's slots by hand and update `SLOTS_PER_REV` |
| Direction shown never changes even when the car reverses | Code is reading a stale `motor_driver.last_direction_a`/`_b` value, or `wheel_odometry.py` was saved before `motor_driver.py` was updated with direction tracking | Confirm `motor_driver.py` on the CIRCUITPY drive includes the `last_direction_a`/`_b` tracking shown in `class-3-code-1.py` |
| `ImportError: no module named 'wifi'` | Board is running the plain "Raspberry Pi Pico 2" CircuitPython build, which has no `wifi` module | Flash the "Raspberry Pi Pico 2 W" `.uf2` (hold `BOOTSEL` while plugging in), then re-copy the code, `settings.toml`, and `lib/` |
| `wifi.radio.start_ap()` raises an error or the network never appears | `CIRCUITPY_WIFI_AP_PASSWORD` is shorter than 8 characters | Use a password of at least 8 characters |
| Website never loads, but the Pico prints an IP address | Laptop hasn't joined the Pico's own network, or the server is on the wrong port | Join the `CIRCUITPY_WIFI_AP_SSID` network; if `ping` works but the browser fails, use `server.start(..., port=80)` (default is 5000) |
| Website loads once but never updates | `server.poll()` not being called every loop, or browser is caching the page | Confirm the `while True: server.poll()` loop is running; try a hard refresh |

## 7. Age Differentiation Notes

**Younger students (12-14) and their parent/guardian:** Provide the pin table above pre-printed
and laminated at the workstation so it's a lookup, not a memorization task. Pair a younger
student's fine-wiring work (especially the DRV8833's output-to-motor-lead connections and the
optocoupler mounting) with the parent/guardian's help holding the chassis steady. Start from all
five `class-3-code-*.py` files already loaded as starting points, and have them focus on tuning the
calibration constants (`SPEED`, `SECONDS_PER_INCH`, `SECONDS_PER_90_DEGREES`, `SLOTS_PER_REV`) by
trial and error rather than writing the functions from scratch. For the website, it's enough for
them to type the pre-filled WiFi credentials into `settings.toml` and confirm the page loads —
treat `rover_server.py`'s internals as "trust the library" material this Class. The stretch is
optional: if they try it, load `straight_drive.py` for them and have them only tune `KP` and
measure the drift.

**Older students (15-18) and adults:** Have them type `motor_driver.py`'s `drive()`/`stop()`
functions themselves from the wiring table and the locked-antiphase explanation, rather than
starting from the provided file. Once the square/circle milestone is met, challenge them to log
each attempt's actual measured dimensions (with a tape measure) against the target, across at least
three battery charge levels, and see if they can predict how far off the next attempt will be. For
wheel odometry, challenge them to explain in their own words (not read from the lesson) why a
quadrature encoder's second, out-of-phase sensor would remove the need to borrow direction from
`motor_driver.py`, and have them add a `/` route to `rover_server.py` that also prints the last
raw tick counts (not just derived speed), as a small extension beyond the provided code. For the
stretch, have them explain why the code slows the faster wheel rather than speeding up the slower
one (it can hit `MAX_THROTTLE`), and predict what a larger `KP` will do before testing it.

## 8. Assessment

**Milestone Assignment (per syllabus, Phase 2 / Class 3):** Car reliably drives a 12-inch square and
a 12-inch-diameter circle, with live wheel-speed telemetry visible on the terminal and on the Pico's
own status webpage.

**What "complete" looks like:** The student can run `drive_square(12)` and `drive_circle(12)` on a
shared test track and produce a shape recognizably close to the 12-inch target — this is a
completion-based, "does it work in the real world" check, not a precision measurement. Minor drift
is expected and is itself part of the lesson. In addition, with `code.py` swapped to the website
code, the student can open a browser to their Pico's status website and point to live-updating
wheel speed and direction values while spinning a wheel by hand.

**How to give feedback without scoring:** Ask the student to point at the marked test track and
narrate, specifically, what's causing the gap between their car's path and the target ("is this a
timing problem, a battery problem, or a slip problem — or all three?") rather than checking a box.
Separately, ask them to explain in their own words why the website's direction reading isn't
measured by the optocoupler itself. The straight-line stretch is optional and isn't
required for the milestone; a pair that does it should be able to show, with a tape measure, that the
car drifts less with feedback than without. If a pair can't get a recognizable square or circle, or a
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
* Keep all five code files (`class-3-code-1.py`/`motor_driver.py` through
  `class-3-code-5.py`/`straight_drive.py`) on a shared drive/USB stick so a student who breaks their
  working file can recover instantly instead of losing class time.
* Pre-fill each student's Pico network name and password in `settings.toml` (or write them on the
  board) — credential typos are a much bigger time sink than any wiring mistake in this Class, and
  have nothing to teach once fixed. Give every student a *unique* network name: a dozen Picos
  broadcasting the same name in one room will collide, and nobody can tell which is theirs.
* Warn students that their laptop loses normal internet while joined to the Pico's network — it's
  expected, not a fault — and that they must join that network *before* opening the browser.
* Run the stretch on your reference car first and note a workable `KP`: the optocoupler reading
  moves in steps of about 4 cm/s per tick, so too large a `KP` chases noise and makes the car snake.
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
