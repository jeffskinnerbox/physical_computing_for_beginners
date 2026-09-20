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
chassis kit, running them off their own 9V battery instead of your Pico's power — that same 9V
battery, stepped down through a 5V buck converter, now also powers your Pico's own `VSYS` input.

First you'll get both wheels spinning forward, reverse, and stopped on command — that part will
feel easy. Then you'll try to drive your car in an exact 35 cm square and a 35 cm-diameter
circle, using nothing but timed moves. That part won't feel easy, and that's on purpose: you're
about to discover, firsthand, why "driving blind" — no way to check your actual position against
where you meant to be — drifts. By the end, you'll be able to name the specific reasons why, not
just say "it's not accurate."

Once you've named "no wheel feedback" as one of those reasons, you'll close part of that gap
yourself: mount a Slot Type IR Optocoupler at each driven wheel to read the wheel-speed encoder disc
already molded into your chassis kit's wheels, and write `wheel_odometry.py` to turn counted ticks
into a real wheel speed in cm/s — while learning why that same sensor, on its own, can't tell you
which way the wheel is turning. Finally, you'll stand up the first version of a Pico-hosted rover
status website, `rover_server.py`, so live wheel speed and direction show up on a laptop browser
with no serial cable at all. This website is built small on purpose — later classes will each add
more to this same site rather than you building a new one.

If you finish early, there's a Phase 5 section too: your car will curve on a "straight" run, because
no two motors are identical — and you'll use the wheel-speed readings you built to fix it. Phase 6 then shows
you how to tune that fix, step by step, until it performs as well as your car can manage.

## 2. What You'll Need

| Component | Quantity | Purpose This Project |
| :---------- | :--------: | :---------------------- |
| Raspberry Pi Pico 2 W (with header) | 1 | Runs your CircuitPython code |
| DRV8833 dual H-bridge motor driver breakout | 1 | Drives both DC gearbox motors from PWM logic signals |
| Emo Smart Robot Car Chassis Kit | 1 | The two motors under test and the chassis they drive |
| 9V battery clip and 9V battery | 1 each | Powers the motors (raw, via `VM`) and, through the buck converter, your Pico's own logic power |
| 5V Buck Converter Module | 1 | Steps the 9V battery down to a regulated 5V for your Pico's `VSYS` power input |
| Slot Type IR Optocoupler for Motor Speed | 2 | Reads each driven wheel's built-in encoder disc for wheel-odometry tick counting |
| Breadboard (from Classes 1-2) | 1 | Your existing circuits stay on it, untouched |
| Dupont jumper wires | ~10 | Point-to-point connections |
| USB cable | 1 | Powers the Pico and carries the serial console |
| Laptop with Mu or Thonny | 1 | Where you write/save code and read the serial console |
| (none — Pico broadcasts its own WiFi network) | — | No classroom WiFi needed: the Pico hosts the rover status website on a network it creates itself (AP mode) |
| Marked 35 cm square / 35 cm-diameter circle test track | 1 (shared) | Your target for the calibration exercise |
| Masking tape and a tape measure | 1 each | Phases 5-6: a straight start line, and measuring how far the car drifts sideways |

**Additional components for the Homework Assignments** (Section 13) — no homework has been written
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
direction and speed, while a separate 9V battery — also, through a buck converter, your Pico's own
power — supplies the actual driving current.

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

**Why two power sources still need a common ground.** The motors run off the 9V battery's raw,
unregulated voltage (`VM` on the DRV8833) — separate from your Pico's own power, which now comes
through a 5V buck converter (`VSYS`) or USB, either regulated to a clean 5V. Keeping the motors on
the raw, unregulated rail protects your Pico's logic from motor electrical noise and current
spikes. But the DRV8833's logic pins
still receive PWM signals measured relative to the Pico's 0V (ground). If the two power supplies
don't share a common ground, the DRV8833 has no consistent "zero" to measure the Pico's signal
against, and the logic won't behave reliably even though each supply is individually fine. This is
why the wiring table below includes a Pico-to-DRV8833 ground jumper even though the motors have
their own separate battery.

**Why `nSLEEP` needs its own jumper.** The DRV8833 has a chip-enable pin, `nSLEEP`, that must be
held HIGH for the chip to respond to any PWM input at all — pulled LOW (or left floating), it stays
in a low-power sleep state and silently ignores everything on `AIN1`/`AIN2`/`BIN1`/`BIN2`. The
Adafruit breakout used in this project has **no onboard pull-up resistor** on this pin, so it must
be wired to a HIGH source explicitly. Tying it straight to Pico `3V3` is enough for this project,
since nothing here needs to put the driver to sleep from code. Skipping this jumper produces a
distinctive symptom: your code runs and prints normally, but the motors never move at all — as if
the Pico were disconnected from the DRV8833 entirely.

One tradeoff of tying `nSLEEP` permanently to `3V3`: the DRV8833 also uses this same pin's LOW→HIGH
transition to clear a **latched fault**. Both H-bridges on the chip share one overcurrent/thermal
protection circuit — if either motor draws an excessive current spike (for example, a jammed or
mechanically stalled wheel), the chip disables *both* channels at once and leaves them disabled
until the fault is cleared. With `nSLEEP` hardwired high, there's no code-level way to cycle it, so
a latched fault shows up as *both* motors suddenly going dead — even a motor that was working fine
moments earlier — and the only fix is to power-cycle the DRV8833 itself (unplug and reseat the 9V
battery, or briefly disconnect and reconnect the `nSLEEP` jumper).

**Slot Type IR Optocoupler (wheel-speed sensor).** Each optocoupler module is a small IR LED and
phototransistor facing each other across a slot, plus an onboard LM393 comparator chip. Your
chassis kit's wheel already has an encoder disc with alternating slots and teeth molded around its
rim; as the wheel spins, each tooth interrupts the LED-to-phototransistor beam once per slot. The
LM393 comparator turns that raw interruption into a clean digital HIGH/LOW pulse — no debouncing
needed the way your Class 1 switch/encoder needed it, since this is a much faster, cleaner signal
straight off a comparator chip, not a noisy mechanical contact.

**Why the optocouplers land on `GP17`/`GP19`, not `GP16`.** The RP2040/RP2350 chip has no dedicated
pulse-counter peripheral, so CircuitPython's `countio.Counter` is implemented using the chip's PWM
hardware in an edge-counting mode — and that mode only works on a PWM **Channel B** pin. Pico GPIO
pins alternate PWM channel in pairs: even-numbered GPIOs (`GP16`, `GP18`, ...) are Channel A, and
odd-numbered GPIOs (`GP17`, `GP19`, ...) are Channel B. Trying `countio.Counter` on an even/Channel-A
pin like `GP16` raises `RuntimeError: Pin must be on PWM Channel B` — that's why this project uses
`GP17` and `GP19` (both odd/Channel B) for the two optocouplers instead of the more obvious
consecutive pair `GP16`/`GP17`.

Turning a pulse train into a speed is a short chain of math: count pulses ("ticks") from one
optocoupler over a fixed time window, divide by `SLOTS_PER_REV` (how many slots you counted on the
disc by hand) to get revolutions in that window, multiply by the wheel's circumference
(`WHEEL_DIAMETER_MM = 67`, so circumference ≈ 21.05cm) to get distance traveled, then divide by the
window's length in seconds to get speed in cm/s. `wheel_odometry.py` does exactly this, once per
wheel, in Phase 3 below.

Here's the catch: a single-slot optocoupler can only tell you *that* the beam was interrupted, not
*which way* the disc was moving when it happened — a tick is a tick either way. A true quadrature
encoder solves this with a second sensor offset out of phase from the first, so the two pulse
trains' relative timing reveals direction; this project's one-optocoupler-per-wheel setup doesn't
have that. Instead, `wheel_odometry.py` borrows direction from `motor_driver.py`: the library
already knows whether it last told Motor A/B to spin forward or reverse (`drive()` records this in
`last_direction_a`/`last_direction_b`), so pairing that last-commanded direction with the measured
tick rate is a reasonable, if imperfect, stand-in for a real direction sensor — it confirms the
wheel is turning (or not, or slower than commanded), but assumes the wheel is actually obeying the
last command it was given.

**Hosting your own website.** The websites you normally visit are hosted on a server somewhere far
away, reached over the internet, and your laptop *joins* an existing network to reach it. Today's
website flips that: your Pico 2 W's own WiFi radio broadcasts its *own* WiFi network (this is called
**access point mode**, or AP mode) that your laptop connects to directly — there's no classroom
router or internet connection involved at all. Once your laptop joins the Pico's network, the Pico
runs a tiny HTTP server (`adafruit_httpserver`) directly in CircuitPython and answers requests at
its own local IP address — the network, the server, the sensor, and the thing being measured are
all in your hand. `rover_server.py` serves two things at that address: a `/data.json` route (current
wheel speed/direction, as machine-readable JSON) and a simple HTML page that polls `/data.json`
every fraction of a second and displays it — so any laptop connected to the Pico's own network can
watch live wheel telemetry with no serial cable at all.

**Pinout summary** (Raspberry Pi Pico 2 W — new pins only; Classes 1-2 are unaffected):

| Pin | What we use it for |
| :---- | :-------------------- |
| `GP9` | DRV8833 `AIN1` (Motor A) |
| `GP10` | DRV8833 `AIN2` (Motor A) |
| `GP11` | DRV8833 `BIN1` (Motor B) |
| `GP12` | DRV8833 `BIN2` (Motor B) |
| Pico `3V3` | DRV8833 `nSLEEP` (must be tied HIGH — no onboard pull-up) |
| `GP19` | Optocoupler A signal out (Motor A wheel) — must be a PWM Channel B (odd) pin, see note below |
| `GP17` | Optocoupler B signal out (Motor B wheel) |
| 9V battery `+` | DRV8833 `VM` (motor power) |
| 9V battery `-` and Pico `GND` | DRV8833 `GND` (common ground) |
| 9V battery `+`/`-` | Buck converter IN+/IN− |
| Buck converter OUT+/OUT− | Pico `VSYS` / `GND` |
| Pico `3V3` | Both optocouplers `VCC` |
| Pico `GND` | Both optocouplers `GND` |


## 4. Build It: Phase 1 — Motor Driver Library and Basic Test - DONE

### Wiring for this phase

This is the complete wiring for the whole project, including the two optocouplers you'll mount and
use starting in Phase 3 — nothing changes for Phase 2, 3, or 4. You can wire the optocouplers now
too, but leave them unmounted at each wheel until Phase 3, once you've counted each disc's slots.
* [Raspberry Pi Pico 2w Pinout][20]
* [SG90 Servo Pinout][38]
* [HC-SR04 Pinout][37]
* [Adafruit DRV8833 DC/Stepper Motor Driver Pinout][39]
* [Slot Type IR Optocoupler][40]

| Component | Pico 2 W Pin | Notes |
| :---------- | :------------- | :---------- |
| Buck converter `IN+`/`IN−` | 9V battery `+`/`−` | |
| Buck converter `OUT+`/`OUT−` | Pico `VSYS` / `GND` | make sure this is a common `GND` |
| DRV8833 `AIN1` (Motor A) | `GP9` | |
| DRV8833 `AIN2` (Motor A) | `GP10` | |
| DRV8833 `BIN1` (Motor B) | `GP11` | |
| DRV8833 `BIN2` (Motor B) | `GP12` | |
| DRV8833 `SLP` | Pico `3V3` or `5V` | must be tied HIGH, see Adafruit documentation |
| DRV8833 `VM` (motor power, `+` green post) | 9V battery `+` | |
| DRV8833 `GND` (motor power, `-` green post) | 9V battery `-` **and** Pico `GND` | make sure this is a common `GND` |
| DRV8833 `AOUT1`/`AOUT2` | Motor A leads | |
| DRV8833 `BOUT1`/`BOUT2` | Motor B leads | |
| Optocoupler Motor A wheel `DO` | `GP19` | must be a PWM Channel B (odd-numbered) pin, see Section 3 |
| Optocoupler Motor B wheel `DO` | `GP17` | |
| Both Slot Type IR Optocoupler `VCC` | Pico `3V3` or `VSYS 5V` | |
| Both Slot Type IR Optocoupler `GND` | Pico `GND` | make sure this is a common `GND` |
| 1000uF electrolytic capacitor `+` on DRV8833 `VM` | does not apply | optional to reduce current spike from motors |
| same capacitor `-` on `GND` | does not apply | make sure this is a common `GND` |

Before writing any code, trace this wiring out loud, and specifically confirm two things:
1. The Pico's `GND` is jumpered to the DRV8833's `GND`.
1. DRV8833 `SLP` isjumpered to Pico `3V3`

>**NOTE:** Make sure to create a commond ground (aka `GND`).
>A missing common ground produces logic that "sort of" works, or works intermittently.<br>
>**NOTE:** Make sure you have the DRV8833 `SLP`/`nSLEEP` jumpered to Pico `3V3`.
>A missing `SLP`/`nSLEEP` jumper produces code that runs and prints normally while the motors never move at all.

### What this code does

This phase is two files. First, `motor_driver.py` — a small library, not something you run
directly — that wraps the DRV8833's raw PWM control behind simple `drive(left, right)` and `stop()`
functions, capping current draw with `MAX_THROTTLE`. It also remembers, in `last_direction_a` and
`last_direction_b`, whichever direction each motor was last told to spin (`-1` reverse, `0` stopped,
`1` forward) — Phase 3's `wheel_odometry.py` will read these two values, since a single optocoupler
can measure tick *rate* but not direction (see Section 3 above). Second, a short scratch script
that imports the library and exercises it: forward, reverse, a turn, and stop, printing each move
as it happens.

### The code

Save this first file as `motor_driver.py` on your `CIRCUITPY` drive (not `code.py` — other code
imports this one).

```python
# class-3-phase-1-motor-driver.py -- save as motor_driver.py
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

# DC Motor wraps the pin pair behind a simple .throttle property:
# -1.0 (full reverse) to 1.0 (full forward), 0.0 brakes, None coasts.
motor_a = motor.DCMotor(pwm_ain1, pwm_ain2)
motor_b = motor.DCMotor(pwm_bin1, pwm_bin2)

# Last-commanded direction per channel: -1 reverse, 0 stopped, 1 forward.
# A single-slot optocoupler can measure tick RATE but not direction (see
# Section 3 above) -- wheel_odometry.py reads these two values to pair
# with its own measured speed.
last_direction_a = 0
last_direction_b = 0


def _clamp(throttle):
    """Limit a throttle value to +/- MAX_THROTTLE, passing None through unchanged."""
    if throttle is None:
        return None
    return max(-MAX_THROTTLE, min(MAX_THROTTLE, throttle))


def _sign(throttle):
    """Return -1, 0, or 1 for the direction a throttle value represents."""
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
    """Actively brake both motors (0.0 brakes; None would coast instead)."""
    global last_direction_a, last_direction_b
    motor_a.throttle = 0.0
    motor_b.throttle = 0.0
    last_direction_a = 0
    last_direction_b = 0
```

Now save this second file as `code.py`, replacing whatever was there before, to test the library:

```python
# class-3-phase-1-code.py -- save as code.py
# Scratch test script for motor_driver.py -- exercises forward/reverse/turn/stop.

import time
import motor_driver

print("Class 3, Phase 1 -- motor driver test starting...")

# both motors half speed forward for 2 seconds
print("both wheels forward")
motor_driver.drive(0.5, 0.5)
time.sleep(2)

# both motors half speed reverse for 2 seconds
print("both wheels reverse")
motor_driver.drive(-0.5, -0.5)
time.sleep(2)

# left wheel A backward, right wheel B forward,both wheels half speed reverse for 2 seconds
print("turn (left wheel A backward, right wheel B forward)")
motor_driver.drive(-0.5, 0.5)
time.sleep(2)

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

## 5. Build It: Phase 2 — Attempt the Square and Circle - DONE

### Wiring for this phase

No wiring changes — same circuit as Phase 1.

### What this code does

This program builds two higher-level moves — `drive_straight(cm)` and `turn_90()` — purely
out of *timing*: drive at a fixed speed for a calculated number of seconds, then stop. It chains
those into `drive_square(35)` (four straight-and-turn segments) and `drive_circle(35)` (many short
straight segments with small turns between them, approximating a circle). There's no way for the
car to check whether it actually went 35 cm or turned exactly 90 degrees — it's just trusting
the clock. This approach is called **open-loop control**, or "dead reckoning," and the gap between
what it *should* do and what it *actually* does is the whole point of today's Independent Work.

**Open loop, in a picture.** Here's what `drive_straight(35)` really does. The only thing the
code "knows" is the clock; everything to the right of `time.sleep()` is out of its sight:

```text
   OPEN LOOP -- drive_straight(35) with timed moves

   your code                          the real world (code can't see this)
   ---------                          ------------------------------------
   drive(0.5, 0.5)  ---- PWM ------>  motors spin, wheels roll, car moves
        |                                  |   |   |
   time.sleep(35 * 0.035)                  |   |   +-- battery sags -> slower
        |   (= 1.23 s, and that's          |   +------ left/right motors differ
        |    ALL the code knows)           +---------- floor grip, wheel slip
        v
   stop()  ----------------------->  car coasts to a halt somewhere...

   What the code ASSUMES:   went 35.0 cm, straight ahead
   What actually happened:  went 30.5 cm (say), drifted 4 cm left

   Nothing flows back from the car to the code -- no arrow points left.
```

Errors don't cancel between moves — they *stack*. Here's a square where each side and each turn is
just a little off (exaggerated so you can see it):

```text
   COMMANDED square                 ACTUAL path (errors accumulate)

   start/end                        start                 end (never closes)
   +-----------+                    +----------.           .
   |           |                    |            `.         |  <- gap between
   |           |                    |              \        |     start and end
   |  35 cm    |                    |               `--+    |     = accumulated
   |           |                    |                   |   |       error
   +-----------+                    +-------------------+   '
                                    side 1 long, turn 1 short, side 2 curves...
                                    each move starts from where the LAST one ended up
```

That gap is the price of never checking. Phase 3 gives the car a way to *sense* wheel motion, and
Phase 5 uses it to close a loop.

### The code

Save this as `code.py`, replacing Phase 1's scratch test script. `motor_driver.py` stays on the
drive unchanged — this new file imports it.

```python
# class-3-phase-2-code.py -- save as code.py
# Phase 2: attempt a 35 cm square and a 35 cm-diameter circle -- open-loop, timed moves only.

import time
import math
import motor_driver

# These three constants MUST be calibrated for your specific robot -- they
# will not be correct as-is. Time a measured straight run and a measured
# 90-degree turn on your own car, then adjust these until your car's actual
# movement matches what you told it to do.
SPEED = 0.5                    # throttle used for all moves
SECONDS_PER_CM = 0.035        # calibrate: time a measured straight run, divide by cm
SECONDS_PER_90_DEGREES = 0.4   # calibrate: time a measured 90-degree turn


# drive straight forward
def drive_straight(cm):
    print("move: straight", cm, "cm")
    motor_driver.drive(SPEED, SPEED)
    time.sleep(cm * SECONDS_PER_CM)
    motor_driver.stop()


# turn 90 degrees left
def turn_90():
    print("move: turn 90 deg")
    motor_driver.drive(-SPEED, SPEED)
    time.sleep(SECONDS_PER_90_DEGREES)
    motor_driver.stop()


# drive in a square
def drive_square(side_cm=35):
    print("attempt: square, side", side_cm, "cm")
    for _ in range(4):
        drive_straight(side_cm)
        time.sleep(0.2)  # brief pause so moves don't blur together
        turn_90()
        time.sleep(0.2)
    print("attempt: square complete")


# drive in a circle
def drive_circle(diameter_cm=35):
    # Approximate a circle as many short straight segments, each followed
    # by a small turn -- like walking a circle by taking short steps and
    # pivoting slightly after each one.
    print("attempt: circle, diameter", diameter_cm, "cm")
    circumference = math.pi * diameter_cm
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
drive_square(35)
time.sleep(1)
drive_circle(35)
```

### Try it / what you should see

Your car should complete a full attempted square and a full attempted circle without you touching
anything, printing a status line for each individual move as it happens. The shape it traces will
almost certainly *not* be a clean 35 cm square or circle — corners may not be square, sides may
be different lengths, the circle may be lopsided. That's expected.

Ask yourself: you told it to go exactly 35 cm.
What did it actually do, and why might that be?

Notice too whether your "straight" sides actually went straight. If the car curves even with equal
throttle, that's real hardware, not a bug — and there's a way to fix it in the Phase 5 (Section 8).

### Checkpoint

Run `drive_square(35)` and `drive_circle(35)` on your test track and confirm the car completes
both attempts start to finish without help, tracing a recognizable (even if imperfect) square and
circle shape.

## 6. Build It: Phase 3 — Wheel Odometry - DONE

### Wiring for this phase

No new wiring if you already wired both optocouplers back in Phase 1 — what's new is mounting them.
Mount each optocoupler so its slotted fork straddles the wheel's built-in encoder disc without
rubbing against it, then turn each wheel slowly by hand and count the disc's slots — you'll need
that count in a moment.

| Component | Pico 2 W Pin |
| :---------- | :------------- |
| Optocoupler A signal out (Motor A wheel) | `GP19` |
| Optocoupler B signal out (Motor B wheel) | `GP17` |
| Both optocouplers `VCC` | Pico `3V3` |
| Both optocouplers `GND` | Pico `GND` |

### What this code does

`wheel_odometry.py` is a second library file, saved alongside `motor_driver.py` — it doesn't run on
its own either. It uses the built-in `countio` module to count optocoupler pulses on `GP19`/`GP17`
over a short sampling window (`SAMPLE_SECONDS`), converts that tick count to a wheel speed in cm/s
using `SLOTS_PER_REV` and the 67mm wheel diameter (see Section 3's math walkthrough), and pairs each
wheel's speed with `motor_driver`'s last-commanded direction for that same wheel — since, as Section
3 explained, the optocoupler alone can't tell you which way the wheel is turning.

Before this will read correctly, set `SLOTS_PER_REV` below to the number of slots you counted by
hand on your own wheel's disc — the value shown is a placeholder, not a measurement.

### The code
You will use `motor_driver.py` from the previous phase.
It stays on the `CIRCUITPY` drive unchanged.
Save this as `wheel_odometry.py` on your `CIRCUITPY` drive and it will import `motor_driver.py`.

```python
# class-3-phase-3-wheel_odometry.py -- save as wheel_odometry.py
# Wheel-speed odometry via slot IR optocouplers -- tick RATE from GP19/GP17,
# direction borrowed from motor_driver's last-commanded state.

import time
import board
import countio            # library for counting slots in IR optocouplers
import motor_driver       # imports the file you created in phase 1

WHEEL_DIAMETER_MM = 67    # 67 millimetres measure this with calipers
SLOTS_PER_REV = 20        # count your own wheel's encoder disc slots by hand and set this
SAMPLE_SECONDS = 0.25     # sampling window for one speed reading
WHEEL_CIRCUMFERENCE_CM = (WHEEL_DIAMETER_MM / 10) * 3.14159            # wheel circumference in centimeters = 21.05
WHEEL_CIRCUMFERENCE_PER_SLOT = WHEEL_CIRCUMFERENCE_CM / SLOTS_PER_REV  # centimeters of wheel travel per slot = 1.05
CMS_PER_TICK = WHEEL_CIRCUMFERENCE_PER_SLOT / SAMPLE_SECONDS           # cm/s of speed per counted tick = 4.21

counter_a = countio.Counter(board.GP19)  # slot counter for Motor A wheel -- must be a PWM Channel B pin
counter_b = countio.Counter(board.GP17)  # slot counter for Motor B wheel

# Derivation of Formula
# revolutions = ticks / SLOTS_PER_REV
# ticks_to_cms = (revolutions * WHEEL_CIRCUMFERENCE_CM) / SAMPLE_SECONDS
#              = ((ticks / SLOTS_PER_REV) * WHEEL_CIRCUMFERENCE_CM) / SAMPLE_SECONDS
#              = ticks * (WHEEL_CIRCUMFERENCE_CM / SLOTS_PER_REV) / SAMPLE_SECONDS
def _ticks_to_cms(ticks):
    """Convert a wheel's tick count, taken over SAMPLE_SECONDS, to a speed in cm/s."""
    revolutions = ticks / SLOTS_PER_REV
    return (revolutions * WHEEL_CIRCUMFERENCE_CM) / SAMPLE_SECONDS
    # return ticks * CMS_PER_TICK


def read_speed():
    """Sample both optocouplers over SAMPLE_SECONDS; return
    (speed_left_cms, dir_left, speed_right_cms, dir_right)."""

    # initialize slot count
    counter_a.count = 0
    counter_b.count = 0

    # sleep and let slot count accumulate
    time.sleep(SAMPLE_SECONDS)

  # get the counts and convert to centimeters per second (speed)
    speed_left = _ticks_to_cms(counter_a.count)
    speed_right = _ticks_to_cms(counter_b.count)
    return (speed_left, motor_driver.last_direction_a,
            speed_right, motor_driver.last_direction_b)
```

Test it with a short scratch `code.py` that drives forward and prints `read_speed()` each cycle:

```python
# class-3-phase-3-code.py -- save as code.py
# Scratch test script for wheel_odometry.py.

import motor_driver
import wheel_odometry

print("Output format:\n( left_wheel_cm_per_sec,  left_wheel_dir,  right_wheel_cm_per_sec,  right_wheel_dir )")

# set motors to half speed, moving forward
motor_driver.drive(0.5, 0.5)
for _ in range(10):
    print(wheel_odometry.read_speed())

# set motors to half speed, moving backward
print("\n")  # skill a line
motor_driver.drive(-0.5, -0.5)
for _ in range(10):
    print(wheel_odometry.read_speed())

motor_driver.stop()
```

### Try it / what you should see

You should see ten printed tuples of
`(left_wheel_cm_per_sec,  left_wheel_dir,  right_wheel_cm_per_sec,  right_wheel_dir)`,
with both speeds rising above `0.0` while the car drives forward and `left_wheel_dir`/`right_wheel_dir`
both reading `1`.
Stop the car (`motor_driver.stop()`), then try `motor_driver.drive(-0.5, -0.5)` and rerun the
loop — the direction values should flip to `-1` while the speeds stay positive (speed is always a
magnitude; direction is a separate value).

A speed reading of `0.0` while the wheel is visibly spinning almost always means the optocoupler's
slot isn't actually straddling the disc — remount it before assuming the code is wrong. A reading
that's wildly too high or low usually means `SLOTS_PER_REV` was miscounted — recount the disc's
slots by hand.

### Checkpoint

Confirm both `speed_left_cms` and `speed_right_cms` rise above zero while driving forward, and that
`dir_left`/`dir_right` flip from `1` to `-1` when you tell the car to reverse — this is the moment
measured speed and commanded direction combine into one reading.

## 7. Build It: Phase 4 — Rover Status Website - DONE

### Wiring for this phase

No new wiring — this phase is all software. Add `CIRCUITPY_WIFI_AP_SSID` and
`CIRCUITPY_WIFI_AP_PASSWORD` to your `settings.toml` file if they aren't already filled in. Unlike
Phases 1-3, these aren't your classroom's existing WiFi credentials — they're the name and password
*you're choosing* for the Pico's own broadcast network (pick a name nobody else in the room is
using, since everyone's Pico broadcasts at once; the password must be at least 8 characters for
CircuitPython's `start_ap()` to accept it).

### What this code does

`rover_server.py` puts the Pico's WiFi radio into **access point (AP) mode** — it broadcasts its own
WiFi network named `CIRCUITPY_WIFI_AP_SSID` instead of joining an existing one — then starts an
`adafruit_httpserver` HTTP server that answers two routes: `/data.json` (the current wheel speed and
direction from `wheel_odometry.read_speed()`, as machine-readable JSON) and `/` (a bare HTML page
with a bit of JavaScript that polls `/data.json` twice a second and displays it). Unlike Phase 2's
`code.py`, which ran the square/circle attempt directly, this file is saved under its own stable
name, `rover_server.py`, so Classes 4-6 can keep extending it under that same name. It still ends in
its own `while True:` loop that keeps answering requests forever — it just isn't `code.py` itself
anymore. A separate, one-line `code.py` runs it (see below).

**The mission for this phase, and why spinning a wheel by hand isn't the end goal.** Spinning a
wheel by hand (below, in "Try it") only proves the plumbing works — that the sensor reading, the
JSON route, and the web page are all wired together correctly. That's a necessary first check, but
it's not the point of building a rover status website. The actual mission is for the website to
update on its own *while the rover drives itself* — no hand ever touching a wheel, no human in the
loop at all. Once a script is commanding the motors (Phase 2's `drive_square`/`drive_circle`, or
free driving), this same `rover_server.py`, unmodified, should show that motion live on the page:
speeds rising and falling as the car moves, direction flipping as it reverses or turns — entirely
from the car's own behavior. Getting there for real means the motor-driving code and the server's
`while True: server.poll()` loop have to run *together*, without one blocking the other (a
`time.sleep()`-based drive command, like Phase 2 uses, would freeze the website for as long as it
sleeps) — that's a real design problem worth sitting with, and it's exactly the kind of thing
Classes 5-6 build toward as this website keeps growing.

### The code

Save this as `rover_server.py` on your `CIRCUITPY` drive. `motor_driver.py` and `wheel_odometry.py`
stay on the drive unchanged — this file imports `wheel_odometry` (which in turn imports
`motor_driver`).

```python
# class-3-phase-4-rover_server.py -- save as rover_server.py
# Pico-hosted rover status website -- broadcasts its own WiFi network (AP
# mode), serves /data.json plus a minimal page that polls it.

import os
import wifi
import socketpool
from adafruit_httpserver import Server, Request, Response, JSONResponse
import wheel_odometry

# AP_PASSWORD must be at least 8 characters -- start_ap() rejects shorter ones.
wifi.radio.start_ap(
    os.getenv("CIRCUITPY_WIFI_AP_SSID"), os.getenv("CIRCUITPY_WIFI_AP_PASSWORD")
)
print("rover server -- broadcasting WiFi network:", os.getenv("CIRCUITPY_WIFI_AP_SSID"))
print("rover server -- listening at", wifi.radio.ipv4_address_ap)

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool)
# server = Server(pool, debug=True)    # use for debugging

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
    return JSONResponse(
        request,
        {
            "speed_left_cms": speed_left,
            "dir_left": dir_left,
            "speed_right_cms": speed_right,
            "dir_right": dir_right,
        },
    )


@server.route("/")
def index(request: Request):
    return Response(request, STATUS_PAGE, content_type="text/html")


server.start(str(wifi.radio.ipv4_address_ap), port=80)

print("Class 3, Phase 4 -- rover status website starting...")
while True:
    server.poll()
```

Then save this second, one-line file as `code.py`, replacing Phase 3's scratch test script. All
`code.py` does is import `rover_server` so it actually runs — CircuitPython only auto-runs
`code.py`, so this thin wrapper is what makes `rover_server.py` start on boot, while keeping the
real logic under a name Classes 4-6 can `import rover_server` by:

```python
# code.py -- runs the rover status website
import rover_server
```

### Try it / what you should see

Watch the serial console for a line like `rover server -- broadcasting WiFi network: <your-name>`
followed by `rover server -- listening at 192.168.4.1`. On your laptop, open its WiFi settings and
connect to that same network name (`CIRCUITPY_WIFI_AP_SSID` from `settings.toml`) using the password you set —
this is a normal WiFi join, just to the Pico's network instead of the classroom's. Once connected,
open a browser and go to the printed IP address (typically `192.168.4.1`) — you should see
`Rover Status` and a block of JSON that updates itself twice a second.

#### Step 1 — verify the plumbing (manual check)
Spin a wheel by hand and watch that wheel's
`speed_left_cms` or `speed_right_cms` jump on the page, even though nothing told the motor to move
— a concrete reminder that this reading is measured, independent of whatever the motor was last
commanded to do, while direction is not. This step only confirms the sensor, the route, and the
page are correctly wired together — it is not the mission.

#### Step 2 — the actual mission
Now drive the car with code instead of your hand. You can't
do this from the REPL: `code.py` imports `rover_server`, which ends in `while True: server.poll()`
and never returns, so there's no prompt while the server runs (and Ctrl+C to get one kills the
server). Instead, start the motors *before* the server starts. Put the car on blocks with the wheels
off the ground, make sure the battery pack is on (USB alone won't power the motors), and temporarily
replace `code.py` with:

```python
# code.py -- TEMPORARY Phase 4 mission test: motors run while the website serves

import motor_driver

# sets the PWM and returns; the motors keep spinning on their own
motor_driver.drive(0.5, 0.5)

# blocks in server.poll() forever -- the motors keep running
import rover_server
```

Save, reconnect to the Pico's WiFi network, and reload the page. Watch it show steady, nonzero wheel
speeds *while the car moves under its own power*, with no one touching a wheel. That's the behavior
this phase is actually building toward: a website that reports what the rover is doing
autonomously, not what a person did to it by hand.

To stop the motors, press Ctrl+C in the serial console or unplug the battery pack. Then put `code.py`
back to the one-line `import rover_server` version above.

This test only shows *constant* speed — `drive()` is called once and never again. Speeds rising and
falling and direction flipping need drive code that runs alongside `server.poll()`, which is the
design problem Classes 5-6 tackle.

>***NOTE:** While your laptop is connected to the Pico's network, it will likely lose its regular
>internet connection — the Pico's AP doesn't route traffic anywhere else, it just serves this one page.
>If the server never starts, double-check `settings.toml`'s `CIRCUITPY_WIFI_AP_PASSWORD` is at least 8 characters.
>If the page loads but never updates,
>try a hard refresh — your browser may be caching an old copy of the page.

### Checkpoint

Connect your laptop to the Pico's own broadcast WiFi network and open a browser to its printed IP
address. First confirm the `/data.json` fields update live when you spin a wheel by hand (the
plumbing check) — then confirm the same fields update live while the car is driven by code, not by
hand (the actual mission of this phase). Be able to say in one sentence why the direction shown on
the page is "what we last told the car to do," not something the optocoupler itself measured.

## 8. Build It: Phase 5 — Drive Straight with Wheel Feedback

Complete Phase 3 first — this phase needs both optocouplers mounted, `SLOTS_PER_REV` set, and
`wheel_odometry.read_speed()` showing both wheels above `0.0`.

> **[VERIFY — bench test pending]** This whole section has not yet been run on a real car. Still to
> validate: the starting values `KI`, `MAX_TRIM`, `BASE_THROTTLE`, `RUN_SECONDS`, and `RESET_SECONDS`;
> the suggested fixes (`KI` of `0.01` or `0.003`, `SAMPLE_SECONDS` of `0.5`); the claim that `trim`
> settles within about a second; and that feedback drift is clearly smaller than open-loop drift.
> Replace the placeholders with measured values and delete this note once validated.

### Why your car curves

Put your car on the floor, point it down a long straight line, and run `drive(0.5, 0.5)`. Equal
throttle, so it should go straight — and it doesn't. It curves, and you can't fix that by choosing a
"better" throttle number. Here's why: two motors are never identical. Brush wear, gearbox
friction, and tiny differences in the windings mean the *same* PWM duty cycle spins one wheel a bit
faster than the other, and that's the same lesson as "duty cycle isn't the same as speed" from
Section 3. Your code told both wheels the same thing; it has no idea they aren't doing the same
thing back.

Phase 2's dead reckoning can't see this, and the only fix so far has been to hand-tune the left and
right throttle until it looks straight. That works until the battery sags or you change floors, and
then it's wrong again. The real fix is to stop guessing and *measure*: your car can already read
each wheel's actual speed (Phase 3), so let it compare the two and correct itself. Measuring the
result, comparing it to what you wanted, and adjusting is called **closed-loop control** (or
**feedback control**) — the opposite of the open-loop control you used in Phase 2. It's how a car's
cruise control holds 65 mph up a hill, and how a thermostat holds a room at 70 degrees.

### Open Loop vs. Closed loop, in Pictures

**Open loop** is what Phases 1-2 did: decide on a command, send it, and never look at the result.
Information flows one way only.

```text
   OPEN LOOP  (Phase 2 -- "fire and forget")
     GOAL: nothing measured, nothing corrected
     Result: car curves.  The code has no way to know, so it can't fix it.


   +-----------+   throttle    +---------+   PWM    +--------+   wheels
   |  your     |  0.5 , 0.5    | motor_  |--------->|        |-----------> car
   |  code     |-------------->| driver  |          | motors |   turn at
   |           |               |         |          |        |   DIFFERENT
   +-----------+               +---------+          +--------+   speeds
                                                        ^
                                                        |
                              worn brushes, gearbox friction, weak battery,
                              carpet ... (disturbances the code never sees)

```

**Closed loop** adds one thing: a feedback path.
The car's *actual* result (the optocoupler speeds)
is measured, compared to the goal, and fed back to change the next command.

```text
   CLOSED LOOP  (Phase 5 -- "measure, compare, correct")
     GOAL: both wheels the SAME speed  (error = 0)
     Result: car curving is suppressed.  The code makes corrections.


                       +-------------------------<-------------------------------+
                       |             the loop repeats ~4x / second               ^
                       |                                                         |
   +-----------+       v                                                         |
   | 3. NUDGE  |   +----------+    drive (left, right)     +--------+     +--------------+
   |           |   | motor_   |--------------------------->| motors |---->|  wheels turn |
   | trim +=   |   |  driver  |                            +--------+     +--------------+
   |  KI*error |   +----------+                                 ^                |
   |           |        ^                                       |                | slots pass
   | slow the  |        | new throttles:                  disturbances           | the sensors
   | FASTER    |        |  left  = BASE - max(trim,0)    (motor mismatch,        |
   | wheel     |--------+  right = BASE + min(trim,0)     battery sag)           |
   |           |                                                                 v
   +-----------+                                                          +--------------+
        ^                                                                 | 1. MEASURE   |
        |                                                                 | read_speed() |
        |  error = speed_left - speed_right                               | -> L cm/s    |
        |                                                                 |    R cm/s    |
        |                                                                 +------+-------+
        |                                                                        |
   +----+-------+                                                                v
   | 2. COMPARE |<---------------------------<-----------------------------------+
   |  L - R     |            speed_left, speed_right
   +------------+

```

Read the closed-loop picture as a circle, starting at **1. MEASURE** and going around: measure
each wheel's speed, **2. COMPARE** them, **3. NUDGE** the throttles, drive the motors with the new
numbers, and the wheels' new speeds come back around to be measured again. The disturbances still
happen — the loop doesn't prevent them, it *notices their effect and cancels it*.

### How the correction works, step by step

Everything hangs on one number, `trim`. It's the car's running memory of "how much slower the faster
wheel needs to go." Its sign says which wheel:

```text
   trim > 0   left wheel is the fast one   -> slow the LEFT  wheel:  left  = BASE - trim
   trim = 0   wheels match                 -> both wheels at BASE
   trim < 0   right wheel is the fast one  -> slow the RIGHT wheel:  right = BASE + trim
                                                                     (trim is negative,
                                                                      so this subtracts)
```

Each pass of the loop does three small things:

1. `error = speed_left - speed_right` — a single number: positive if left is faster, negative if
   right is faster, zero if they match.
2. `trim += KI * error` — **add** a small fraction of the error to `trim`. The `+=` matters: `trim` is
   never recomputed from scratch, it *accumulates*, so a steady error keeps pushing `trim` further
   in the same direction until the error disappears. `KI` is how big a fraction.
3. `trim = max(-MAX_TRIM, min(MAX_TRIM, trim))` — a safety clamp, so one bad reading can never slow a
   wheel by more than `MAX_TRIM`.

Then the throttles are set from `BASE_THROTTLE` and `trim`, and the loop goes around again.

Here is the same loop with made-up but plausible numbers (`BASE_THROTTLE = 0.5`, `KI = 0.005`).
Speeds move in steps of about 4 cm/s because the sensor counts whole slots, as explained below:

```text
 cycle | speed L | speed R | error (L-R) | trim change | trim  | left thr | right thr
-------+---------+---------+-------------+-------------+-------+----------+----------
   0   |    -    |    -    |      -      |      -      | 0.000 |   0.50   |   0.50    <- start equal
   1   |   24    |   16    |     +8      |   +0.040    | 0.040 |   0.46   |   0.50    <- left faster
   2   |   20    |   16    |     +4      |   +0.020    | 0.060 |   0.44   |   0.50    <- still a bit
   3   |   16    |   16    |      0      |    0.000    | 0.060 |   0.44   |   0.50    <- matched!
   4   |   16    |   16    |      0      |    0.000    | 0.060 |   0.44   |   0.50    <- holds steady
```

Three things to notice in that table:

* **The error shrinks each cycle** because the previous nudge already slowed the fast wheel.
  That shrinking is the feedback working.
* **When the error hits zero, `trim` stops changing but does not go back to zero.** It stays at
  `0.060` — the amount of slowdown the left motor needs to keep pace. That leftover number *is* the
  motor mismatch, learned by the car. (It's why the Try-it section says to watch `trim` settle.)
* **If something changes** — the battery sags, one wheel hits carpet — the error becomes non-zero
  again and the same loop quietly re-learns a new `trim`. Hand-tuned throttles from Phase 2 can't
  do that.

Why `KI` is small, in one more picture. A big `KI` reacts to every sensor blip; a small one waits
for a *steady* difference:

```text
   KI too big (0.05)                 KI about right (0.005)         KI too small (0.0005)
   trim                              trim                           trim
    |   /\    /\                      |       ____________           |        ______
    |  /  \  /  \  /\  <- snakes      |     /   settles              |      /  crawls, car
    | /    \/    \/                   |    /                         |     /   still curves
    +-----------------> time          +-----------------> time       +--------------------> time
```

### Wiring for this phase

No new wiring — same circuit as Phase 3, with both optocouplers mounted and working.

### What this code does

`straight_drive.py` is a small library with one function, `drive_straight_feedback(seconds)`. It
starts both wheels at the same throttle, then repeats this loop about four times a second until the
time is up:

1. **Measure** — call `wheel_odometry.read_speed()` to get each wheel's real speed in cm/s.
2. **Compare** — `error = speed_left - speed_right`. Positive means the left wheel is running
   faster; negative means the right is.
3. **Nudge** — add a small amount, `KI * error`, to a running `trim` value. Then slow down the
   *faster* wheel by that trim (and leave the other wheel alone).
4. **Repeat** — with the next reading, the error should be a little smaller, so the nudge is a little
   smaller, until the two wheels match and the trim stops changing.

Two design choices are worth understanding, because they're the difference between a car that
drives straight and one that snakes:

* **It slows the faster wheel instead of speeding up the slower one.** `motor_driver` caps
  throttle at `MAX_THROTTLE`. If the code sped up the slow wheel, it could run into that cap and
  stop correcting. Slowing the fast wheel always has room to work.
* **The nudges are small (`KI` is small).** Look at how `read_speed()` counts: one tick is
  one slot of a 20-slot disc, which works out to about 4 cm/s in a quarter-second window. So even
  a perfectly matched pair of wheels will sometimes read one tick apart — a fake "error" of 4 cm/s.
  A big correction would chase that noise and make the car wobble. Many small nudges average the
  noise out and respond only to a *steady* difference, which is the real motor mismatch.

Since this loop adds up its nudges over time (`trim += KI * error`), engineers call the pattern an
**integral controller** — that's why the gain is named `KI`, not `KP`. It's one of the simple building
blocks behind the feedback control in nearly every robot and drone. `KI` is the "gain" — how hard
each nudge is — and choosing it is the tuning part of the exercise.

**What's next: PID.** Real controllers often mix three terms: **P**roportional (react to the error
*right now*), **I**ntegral (react to the error *added up over time* — what you built), and
**D**erivative (react to how *fast* the error is changing). Together that's a "PID" controller. We
stop at I because a D term needs a clean, fast signal, and ours is neither: the sensor reads in
4 cm/s steps and the loop runs only about four times a second. D would amplify that jitter instead of
smoothing it. Keep the idea in your back pocket — it shows up again once you have a smoother
measurement.

One important limit: `read_speed()` is also what the rover status website calls, and both use the
same tick counters. Two callers would keep resetting each other's counts, so this Phase 5 runs *by
itself* as `code.py`, not alongside the website — the same "run one or the other" pattern as Options
A and B in Section 11.

### The code

Save this as `straight_drive.py` on your `CIRCUITPY` drive, next to `motor_driver.py` and
`wheel_odometry.py`, which stay unchanged.

```python
# class-3-phase-5-straight_drive.py -- save as straight_drive.py
# Drive straight by nudging the faster wheel down until both wheels turn at the same speed.

import time
import motor_driver
import wheel_odometry

BASE_THROTTLE = 0.5   # throttle both wheels start at
KI = 0.005            # [VERIFY] nudge per cm/s of speed difference -- tune on your own car
MAX_TRIM = 0.2        # [VERIFY] never slow a wheel by more than this, so a bad reading can't stall it


def drive_straight_feedback(seconds):
    """Drive forward for `seconds`, evening out the two wheels' speeds as it goes."""
    trim = 0.0        # positive slows the left wheel, negative slows the right wheel
    end_time = time.monotonic() + seconds
    motor_driver.drive(BASE_THROTTLE, BASE_THROTTLE)

    while time.monotonic() < end_time:
        # read_speed() waits SAMPLE_SECONDS while it counts ticks, so this loop runs ~4 times a second
        speed_left, _, speed_right, _ = wheel_odometry.read_speed()

        error = speed_left - speed_right   # positive: left wheel is faster
        trim += KI * error                 # small nudge, remembered from cycle to cycle
        trim = max(-MAX_TRIM, min(MAX_TRIM, trim))

        # slow only the faster wheel: max(trim, 0) is the trim when left is fast, min(trim, 0) when right is
        left = BASE_THROTTLE - max(trim, 0)
        right = BASE_THROTTLE + min(trim, 0)
        motor_driver.drive(left, right)

        print(" L:", round(speed_left, 1), " R:", round(speed_right, 1), " E:", round(error, 1), " trim:", round(trim, 3))

    motor_driver.stop()
```

Now save this as `code.py`, replacing whatever was there before. It runs the same straight line two
ways — once with no feedback and once with — so you can compare them on the floor:

```python
# class-3-phase-5-code.py -- save as code.py
# Compare driving straight with no feedback (open loop) vs. with wheel feedback (closed loop).

import time
import motor_driver
import straight_drive

RUN_SECONDS = 4       # [VERIFY] about 16 correction cycles: long enough to show a clear curve without leaving the tape
RESET_SECONDS = 15    # [VERIFY] time to measure the drift and carry the car back to the start line

print("\nRun 1 -- open loop: equal throttle, no feedback")
motor_driver.drive(straight_drive.BASE_THROTTLE, straight_drive.BASE_THROTTLE)
time.sleep(RUN_SECONDS)
motor_driver.stop()

print("\nPut the car back on the start line, pointed down the line...")
time.sleep(RESET_SECONDS)

print("\nRun 2 -- closed loop: wheel feedback")
straight_drive.drive_straight_feedback(RUN_SECONDS)

print("done")
```

### Try it / what you should see

Lay a long strip of masking tape on the floor as a straight line, and mark a start point on it.
Use a fresh 9V battery, and set your car on the start point pointing down the tape.

1. Save the files and let `code.py` run. **Run 1** (no feedback) drives for four seconds. Note
   how far the car has drifted sideways from the tape, measured with a tape measure at its
   furthest point — write it down.
2. Carry the car back to the start point before the countdown ends. **Run 2** (feedback) drives
   the same four seconds, and prints each cycle's left speed, right speed, and `trim`. Measure the
   sideways drift the same way.
3. Repeat the pair of runs three times and average each. Use the same battery and floor for all six.

You should see the car end much closer to the tape with feedback than without. In the printed
lines, watch `trim`: it should start at `0.0`, move away from zero in the first second or so as
the code discovers which wheel is faster, and then settle near a steady value — that number *is*
your car's motor mismatch, discovered by the car itself.

**If it doesn't work the way you expect:**

* **The car curves as much as before, and `trim` stays near `0.0`.** The correction is too weak or
  not happening. Raise `KI` (try `0.01`), and check that both wheels' speeds print above `0.0` —
  a `0.0` means that optocoupler isn't reading (see Troubleshooting).
* **The car snakes left and right, and `trim` jumps around.** The nudges are too big. Lower `KI`
  (try `0.003`), or increase `SAMPLE_SECONDS` in `wheel_odometry.py` from `0.25` to `0.5` so each
  reading counts more ticks and is less jumpy.
* **The car curves *more* than before, and `trim` runs to `MAX_TRIM`.** The correction is going the
  wrong way. Check that Motor A's optocoupler is on `GP19` and Motor B's is on `GP17`, and that
  Motor A is the left wheel — if the two are swapped, the code slows the wrong wheel.

### Checkpoint

Run the open-loop and feedback runs three times each on the same battery and floor. Confirm the
average sideways drift with feedback is clearly smaller than without, and be able to explain in one
sentence why the code slows the faster wheel instead of speeding up the slower one.

### What this doesn't fix

Wheel feedback makes the two wheels *turn at the same speed*. That's not quite the same as *going
straight*: if one wheel slips on a patch of dust or a carpet edge, both wheels can still report the
same speed while the car veers. Nothing here measures which way the car is actually *pointing*. That
gap is the same one the last section of this script points at, and it's what next class's IMU is
built to close.

**How the IMU fits in (a preview of Class 4).** Phase 5 has one loop, and it watches the *wheels*.
The missing piece is a second measurement that watches the *car's heading* — which way it's actually
pointing. The IMU's gyroscope provides exactly that: it reports how fast the car is rotating, and
adding that up over time gives the heading angle (yaw). Picture the two loops nested, the fast one
inside the slow one:

```text
   TODAY (Class 3, Phase 5): one loop, watches the WHEELS

      goal: wheels match --> [ nudge throttles ] --> motors --> wheels --+
                                    ^                                    |
                                    +------ optocouplers: L speed, R speed

   CLASS 4 TIE-IN (preview): add an outer loop, watches the HEADING

      goal: heading = 0 deg (straight ahead)
        |
        v
      +----------------+  "wheels should differ by X"  +--------------------+
      | OUTER loop     |------------------------------>| INNER loop         |
      | compare heading|                               | (today's Phase 5)  |
      | to goal, ask   |                               | make the wheels    |
      | for a correction                               | match that request |
      +-------^--------+                               +----------+---------+
              |                                                   |
              |  yaw angle                                  motors, wheels
              |                                                   |
      +-------+--------+                                          v
      | IMU (LSM9DS1)  |<--------------- car rotates (or slips!) --+
      | gyro -> yaw    |
      +----------------+

   Wheel slips on dust?  Wheel speeds still match (inner loop is happy),
   but the car veers -> yaw changes -> the OUTER loop sees it and corrects.
```

Two honest caveats. First, in Class 4 the IMU is only *measured and displayed* — building the outer
loop into the rover's driving is a stretch beyond what that class covers. Second, Class 4's filter
uses the accelerometer and gyroscope but not the magnetometer, and gravity can't tell the filter
which way is "north," so its yaw slowly drifts over time. That's fine for a straight run of a few
seconds; it's the reason a long run would need something more.

## 9. Build It: Phase 6 — Tuning KI and MAX_TRIM for Optimal Performance

Complete Phase 5 first — this phase needs `straight_drive.py` and the open-loop vs. closed-loop
`code.py` already working, and a car that visibly drives straighter with feedback than without.

> **[VERIFY — bench test pending]** This whole section has not yet been run on a real car. Still to
> validate: the `KI ≈ 0.3 / k` starting rule; the sweep values; the "keep `KI × 4` under `0.02`"
> noise limit; the `MAX_TRIM ≈ 1.5-2 × trim` rule; and the run and reset times in the sweep script.
> Replace the placeholders with measured values and delete this note once validated.

### Why tune, and what each knob does

Phase 5 gave you two numbers to guess at: `KI` and `MAX_TRIM`. Your car works with the defaults,
but "works" is not "best". Tuning means running the same test over and over, changing *one* number
at a time, and keeping whatever measurably wins. Here is what each knob controls:

* **`KI` — how hard each nudge is.** Every cycle the code adds `KI * error` to `trim`. A small `KI`
  is calm but slow: the car keeps curving while `trim` creeps toward the right value. A large `KI`
  is quick but jumpy: it chases the one-tick sensor noise (about 4 cm/s) and the car snakes. You
  want the biggest `KI` that is still calm.
* **`MAX_TRIM` — the safety clamp.** It caps how much slower the faster wheel can ever be made. Too
  small, and it caps the correction before the wheels match, so the car still curves. Too large,
  and one bad reading can slow a wheel by so much that the car lurches or stalls. You want it a
  little above what your car actually needs, so it is a guard rail, not part of normal driving.

Tune them in that order: `KI` first (with `MAX_TRIM` left loose), then `MAX_TRIM` from what the
correction really needed, then a quick re-check of `KI`. The two interact only weakly, so one pass
of each is enough.

**The scorecard.** Score every run with the same three numbers, and average three runs per setting:

| Measurement | How to get it | Lower is better? |
| :------------ | :--------------- | :----------------- |
| **Drift** | Sideways distance from the tape at the end of the run, in cm, with a tape measure | Yes |
| **Settle cycles** | The first printed line where `E` is `4` or less and `trim` stops changing (one cycle is 0.25 s) | Yes |
| **Trim jitter** | Highest minus lowest `trim` over the last 8 printed lines | Yes |

Keep a log as you go, one row per setting:

| `KI` | `MAX_TRIM` | Drift, runs 1-3 (cm) | Mean drift | Settle cycles | Trim jitter | Notes |
| :----- | :----------- | :--------------------- | :----------- | :--------------- | :------------ | :------ |
| | | | | | | |

### Wiring for this phase

No new wiring — same circuit as Phase 5. You are only changing two constants and reading the same
serial output.

### What this code does

You need two small scratch programs. Both `import straight_drive` and `wheel_odometry` unchanged, so
**`straight_drive.py` is not edited while tuning** — the sweep script overrides `straight_drive.KI`
and `straight_drive.MAX_TRIM` from outside, which works because `drive_straight_feedback()` looks
those two names up each time it runs.

1. **`class-3-phase-6-measure-k.py`** measures `k`, how many cm/s of wheel speed you gain per
   `1.0` of throttle. `k` tells you where to start `KI`: each cycle, the correction removes about
   `KI * k` of the current error, and `0.2` to `0.5` is a good fraction.
2. **`class-3-phase-6-code.py`** runs the feedback drive several times in a row for each
   `(KI, MAX_TRIM)` pair in a list, printing a banner before each run so your serial log shows which
   setting produced which numbers. It stops the car and waits between runs, so you can measure the
   drift and carry the car back to the start line.

### The code

Save this first one as `code.py`, and run it on a clear stretch of floor. It drives the car for
about ten seconds in total, so keep a hand near the power switch.

```python
# class-3-phase-6-measure-k.py -- save as code.py
# Measure k: how many cm/s of wheel speed you gain per 1.0 of throttle.

import time
import motor_driver
import wheel_odometry

LOW_THROTTLE = 0.4
HIGH_THROTTLE = 0.5
SETTLE_SECONDS = 1.0   # let the wheels reach steady speed before measuring
READINGS = 4           # readings averaged per throttle (each takes SAMPLE_SECONDS)


def average_speed(throttle):
    """Drive both wheels at `throttle`; return the average of both wheels' speeds in cm/s."""
    motor_driver.drive(throttle, throttle)
    time.sleep(SETTLE_SECONDS)
    total = 0.0
    for _ in range(READINGS):
        speed_left, _, speed_right, _ = wheel_odometry.read_speed()
        total += (speed_left + speed_right) / 2
    motor_driver.stop()
    return total / READINGS


slow_speed = average_speed(LOW_THROTTLE)
time.sleep(1)          # coast to a stop between the two runs
fast_speed = average_speed(HIGH_THROTTLE)

# speed gained per 1.0 of throttle
k = (fast_speed - slow_speed) / (HIGH_THROTTLE - LOW_THROTTLE)

print("speed at", LOW_THROTTLE, ":", round(slow_speed, 1), "cm/s")
print("speed at", HIGH_THROTTLE, ":", round(fast_speed, 1), "cm/s")
print("k:", round(k, 1), "cm/s per 1.0 throttle")
print("suggested starting KI:", round(0.3 / k, 4))
```

Save this second one as `code.py` (replacing the first), with `straight_drive.py` from Phase 5
already on the board:

```python
# class-3-phase-6-code.py -- save as code.py
# Run the feedback drive several times for each (KI, MAX_TRIM) setting, so you can score each one.

import time
import straight_drive

# Each pair is (KI, MAX_TRIM). Edit this list between sweeps -- change one column at a time.
SETTINGS = (
    (0.0025, 0.2),
    (0.005, 0.2),
    (0.01, 0.2),
    (0.02, 0.2),
)
RUNS_PER_SETTING = 3
RUN_SECONDS = 4        # about 16 correction cycles -- long enough to see trim settle
RESET_SECONDS = 15     # time to measure the drift and carry the car back to the start line

for ki, max_trim in SETTINGS:
    # override the constants in straight_drive.py without editing that file
    straight_drive.KI = ki
    straight_drive.MAX_TRIM = max_trim

    for run in range(1, RUNS_PER_SETTING + 1):
        print("\n=== KI", ki, " MAX_TRIM", max_trim, " run", run, "of", RUNS_PER_SETTING, "===")
        straight_drive.drive_straight_feedback(RUN_SECONDS)
        print("STOPPED -- measure the drift now, then put the car back on the start line")
        time.sleep(RESET_SECONDS)

print("sweep complete")
```

### Try it / what you should see

Work through these steps in order. Do not skip ahead — each step uses a number from the one before.

**Step 0 — Control the test.** Use a fresh 9V battery. Use one floor, one tape line, and one start
mark, with the car pointed the same way each time. Keep `BASE_THROTTLE` fixed for the whole phase.

**Step 1 — Get a baseline.**

1. Run the Phase 5 `code.py` and score its **Run 1** (open loop) three times.
2. Write down the mean drift *and* how much the three runs differ from each other. That spread is
   your **noise floor**: any change smaller than it is not real, just luck.
3. Repeat this baseline every 5 or 6 tests. If it has crept away from the earlier baselines, the
   battery is sagging — swap it before going on.

**Step 2 — Pick a starting `KI`.**

1. Run `class-3-phase-6-measure-k.py` and note the printed `k` and the suggested `KI`. For example,
   `k` of about `60` suggests `KI` of about `0.005`, the value Phase 5 already uses.
2. Use that `KI` as the middle of your sweep in the next step.

**Step 3 — Sweep `KI`.**

1. In `class-3-phase-6-code.py`, set `SETTINGS` to your starting `KI` times `0.5`, `1`, `2` and `4`,
   all with `MAX_TRIM = 0.2` (loose, so it can't interfere yet).
2. Run it. For each setting, score all three runs: drift, settle cycles, trim jitter.
3. Read the printed `trim` values:
    * **`KI` too low:** `trim` creeps slowly, the car still curves at the end, and settle cycles
        are high.
    * **`KI` about right:** `trim` moves away from `0.0` within about a second, then stays flat.
    * **`KI` too high:** `trim` flips sign or jumps each cycle, and the car snakes.
4. Pick the **highest** `KI` that still shows flat `trim` with no sign flips, then back it off by
   about 30%. Faster settling always costs some jitter, so you are choosing a trade-off.
5. Check the noise ceiling: one tick moves `trim` by about `KI * 4` per cycle. Keep that at `0.02`
   or less, or the car will wobble no matter how the rest looks.

**Step 4 — Set `MAX_TRIM` from data.**

1. From your good `KI` runs, average the printed `trim` over the last 8 lines. Call that `T*`. It
   is the car's real motor mismatch, discovered by the car itself.
2. Set `MAX_TRIM` to about `1.5` to `2` times `|T*|`, with a floor of `0.05`.
3. Check that `BASE_THROTTLE - MAX_TRIM` stays above the throttle where a wheel stalls — you found
   that in Phase 1. If it doesn't, lower `BASE_THROTTLE` or accept a smaller `MAX_TRIM`.

**Step 5 — Verify the clamp.**

1. Edit `SETTINGS` to one line with your chosen `KI` and `MAX_TRIM`, and run it. `trim` should
   never sit on `+MAX_TRIM` or `-MAX_TRIM` during normal driving.
    * If it sits on the limit, raise `MAX_TRIM`.
    * If it grows steadily in one direction until it hits the limit, `KI` is too low or the wheels
        are swapped (see Troubleshooting).
2. Try tightening `MAX_TRIM` to `1.2 * |T*|`. If drift and jitter don't change, keep the tighter
   value: it limits how far one bad reading can slow a wheel.

**Step 6 — Re-check `KI` with the final `MAX_TRIM`.**

1. Set `SETTINGS` to three values: your chosen `KI` minus 30%, the chosen `KI`, and plus 30%, all
   with the final `MAX_TRIM`.
2. If the middle one is still the best, you are done tuning. If a neighbour wins by more than the
   noise floor, move to it and repeat this step once.

**Step 7 — Test robustness.** Repeat your best setting with a different `BASE_THROTTLE` (try `0.4`
and `0.6`), a half-drained battery, and a second floor surface. `T*` changes with throttle, so if
drift gets much worse away from your tuning point, choose a `MAX_TRIM` that covers the whole range.

**Step 8 — Know when to stop.** Stop when two changes in a row improve drift by less than your
noise floor. An optional third knob is `SAMPLE_SECONDS` in `wheel_odometry.py`: raising it from
`0.25` to `0.5` roughly halves the sensor noise and lets you use a higher `KI`. Try it only after
Step 6, and if you change it, redo Steps 3 and 6.

When you finish, type your final `KI` and `MAX_TRIM` into `straight_drive.py` itself, so every
later program that imports it uses the tuned values.

### Checkpoint

Confirm the tuned `KI` and `MAX_TRIM` are saved in `straight_drive.py`, and that the three-run
average drift with them beats the Phase 5 defaults by more than your noise floor. Be able to say,
in one sentence each, why you picked that `KI` and why you set `MAX_TRIM` where you did.

### What this doesn't fix

Tuning finds the *best* wheel-speed correction, not a perfect one. Whatever drift is left after
Step 8 — the car veering when a wheel slips on dust, or a slow heading error that both wheels
agree on — is invisible to wheel feedback, and no value of `KI` or `MAX_TRIM` can fix it. That
gap needs a sensor that knows which way the car is *pointing*, which is what next class's IMU is
for.

## 10. Troubleshooting Guide

| Problem | Likely Cause | Fix |
| :-------- | :------------- | :---- |
| Neither motor spins | `VM` not connected to the 9V battery, or the battery is dead | Check battery voltage; confirm `VM` and battery `GND` wiring |
| Neither motor spins, but the serial console prints `forward`/`reverse`/`turn`/`stop` normally | DRV8833 `nSLEEP` pin is floating — the Adafruit breakout has no onboard pull-up, so the chip stays asleep and ignores all PWM input even though the Pico is sending correct signals | Jumper `nSLEEP` to Pico `3V3` |
| One motor doesn't spin | Loose wire on a DRV8833 output pin, or a dead motor | Reseat jumper wires; swap in a spare motor to isolate the fault |
| Both motors spin but the car barely moves | `MAX_THROTTLE` set too low, or wheels aren't touching the floor | Raise `MAX_THROTTLE` in small steps; confirm the chassis is set down properly |
| A motor spins the wrong direction | Its leads are swapped at `AOUT1`/`AOUT2` (or `BOUT1`/`BOUT2`) | Swap the two leads, or swap that motor's throttle sign in code |
| Both motors spin the same direction on a "turn" command | Motor B's leads are wired with opposite polarity convention from Motor A | Swap Motor B's leads (or throttle sign) so `+1` means the same physical direction for both |
| One motor goes dead on a specific command (e.g. reverse), then a *previously-working* motor also goes dead on the next command | A latched DRV8833 fault — a current spike on one motor (jammed wheel, shorted output leads) tripped the chip's shared overcurrent/thermal protection, which disables both H-bridges at once until cleared | Check the failing motor for mechanical binding and shorted `AOUT`/`BOUT` leads, then power-cycle the DRV8833 (reseat the 9V battery, or briefly disconnect/reconnect the `nSLEEP` jumper) before retesting |
| Logic behaves erratically even though wiring looks right | Missing common ground between the 9V circuit and the Pico | Add a jumper from DRV8833 `GND` to Pico `GND` |
| Pico doesn't power on when running off battery (no USB) | Buck converter miswired, or its output isn't reaching `VSYS` | Verify buck converter IN from 9V battery, OUT to Pico `VSYS`/`GND`; confirm buck converter's output trimpot (if adjustable) is set to 5V |
| Works fine over USB, but fails and the optocoupler LED flickers when running off the 9V battery alone | Voltage sag/brownout on the shared battery: motor startup current spikes drag down the 9V battery's own voltage, which drags down the buck converter's output feeding the Pico's `VSYS`/`3V3` rail (the optocoupler LED runs off `3V3`, so its flicker is really the Pico's logic power dipping) | Try a fresh 9V battery first; if flicker persists, measure the buck converter's output with a multimeter while the motors run, and add a bulk capacitor (470-1000uF electrolytic) across `VM`/`GND` at the DRV8833 to buffer motor current spikes |
| Square/circle drifts wildly between runs on the same settings | Battery voltage sagging as it depletes | Swap in a fresh 9V battery and re-calibrate the timing constants |
| Car pulls to one side even at equal throttle | Real mechanical difference between the two gearbox motors — equal throttle isn't equal speed | Hand-tune left/right throttle as a quick fix, or use wheel feedback to fix it properly (see Section 8, Phase 5) |
| Phase 5: car snakes left and right, and `trim` jumps around | `KI` too large, so the code chases one-tick measurement noise (about 4 cm/s) | Lower `KI` (try `0.003`), or raise `SAMPLE_SECONDS` in `wheel_odometry.py` to `0.5` |
| Phase 5: car curves more than before, and `trim` runs to `MAX_TRIM` | Correction is slowing the wrong wheel — Motor A/B optocouplers or motors are swapped relative to left/right | Confirm the Motor A optocoupler is on `GP19`, Motor B's on `GP17`, and Motor A is the left wheel |
| Phase 6: run-to-run drift varies as much as the differences between settings | Noise floor too high — battery sagging, floor or start mark changing, car not pointed the same way each run | Use a fresh battery, one start mark, more runs per setting; rerun the open-loop baseline every 5-6 tests |
| Phase 6: `trim` sits on `MAX_TRIM` during normal runs | `MAX_TRIM` too tight for this car's motor mismatch, `KI` too low, or Motor A/B swapped | Raise `MAX_TRIM` to 1.5-2 times the settled `trim`, or raise `KI`; confirm the A/B wiring as in Phase 5 |
| `ImportError: no module named 'motor_driver'` | The library file wasn't saved with the right name | Confirm the first file is saved as exactly `motor_driver.py`, not `class-3-phase-1-motor-driver.py` |
| `ImportError: no module named 'adafruit_motor'` | The `adafruit_motor` library isn't installed in `lib/` on `CIRCUITPY` — it's not built into CircuitPython | Download the Adafruit CircuitPython Bundle matching your CircuitPython version from circuitpython.org/libraries, then copy the `adafruit_motor` folder from the bundle's `lib/` into `CIRCUITPY/lib/` |
| `RuntimeError: Pin must be on PWM Channel B` when `wheel_odometry.py` runs | `countio.Counter` is implemented using the RP2040/RP2350's PWM edge-counting hardware, which only works on a PWM Channel B (odd-numbered) GPIO — `GP16` is Channel A and will always raise this | Use `GP19` (or another unused odd-numbered GPIO) instead of `GP16` for the Motor A optocoupler, both in wiring and in `wheel_odometry.py`'s `counter_a = countio.Counter(board.GP19)` |
| Wheel speed reads `0.0` while the wheel is visibly spinning | Optocoupler's slot isn't straddling the encoder disc, or its wiring is loose | Remount the optocoupler so the disc's teeth pass through the slot; reseat `VCC`/`GND`/signal jumpers |
| Wheel speed reading is wildly too high or too low | `SLOTS_PER_REV` miscounted for that wheel's disc | Recount the disc's slots by hand and update `SLOTS_PER_REV` |
| Direction shown never changes even when the car reverses | `wheel_odometry.py` was saved before `motor_driver.py` was updated with direction tracking | Confirm `motor_driver.py` on your `CIRCUITPY` drive includes the `last_direction_a`/`last_direction_b` tracking shown in Phase 1 |
| `ImportError: no module named 'wifi'` | The board is running the non-WiFi build of CircuitPython — `wifi` is only compiled into the build made for "Raspberry Pi Pico 2 W", not the plain "Raspberry Pi Pico 2" build, even on genuine Pico 2 W hardware | Download the correct `.uf2` for "Raspberry Pi Pico 2 W" from circuitpython.org, hold `BOOTSEL` while plugging in USB to mount `RPI-RP2`, drag the `.uf2` on to reflash, then re-copy `motor_driver.py`, `wheel_odometry.py`, `rover_server.py`, `code.py`, `settings.toml`, and `lib/` (including `adafruit_httpserver`) back onto `CIRCUITPY` |
| Browser shows "This site can't be reached" / `curl` says "failed to connect" to the Pico's IP, even though the laptop is joined to the Pico's WiFi network and can `ping` it | `adafruit_httpserver`'s `Server.start()` defaults to port 5000 (visible if you add `debug=True` to `Server(pool, debug=True)`, which prints `Started development server on http://<ip>:5000`), but a browser typing a bare IP address assumes port 80 | Pass `port=80` explicitly: `server.start(str(wifi.radio.ipv4_address_ap), port=80)` |
| `ImportError: no module named 'rover_server'` | The website code was saved as `code.py` directly instead of `rover_server.py`, so `code.py`'s `import rover_server` fails | Confirm the website code is saved as exactly `rover_server.py`, and `code.py` is only the one-line `import rover_server` wrapper |
| `wifi.radio.start_ap()` raises an error or the network never appears | `CIRCUITPY_WIFI_AP_PASSWORD` in `settings.toml` is shorter than 8 characters — CircuitPython's `start_ap()` requires it | Set `CIRCUITPY_WIFI_AP_PASSWORD` to at least 8 characters in `settings.toml` |
| Website never loads in the browser, but the Pico prints an IP address | Your laptop hasn't joined the Pico's own broadcast WiFi network yet | In your laptop's WiFi settings, connect to the network named by `CIRCUITPY_WIFI_AP_SSID` (not your classroom's network) before opening the browser |
| Website loads once but never updates | `server.poll()` not being called every loop, or the browser is caching the page | Confirm the `while True: server.poll()` loop is running; try a hard refresh |

## 11. Put It All Together

This is the finished project in one place — a calibrated square/circle attempt, wheel-speed
odometry, and your own rover status website, without going through the individual phases above.

### Complete wiring

| Component | Pico 2 W Pin |
| :---------- | :------------- |
| DRV8833 `AIN1` (Motor A) | `GP9` |
| DRV8833 `AIN2` (Motor A) | `GP10` |
| DRV8833 `BIN1` (Motor B) | `GP11` |
| DRV8833 `BIN2` (Motor B) | `GP12` |
| DRV8833 `nSLEEP` | Pico `3V3` (must be tied HIGH — no onboard pull-up) |
| DRV8833 `VM` (motor power) | 9V battery `+` |
| DRV8833 `GND` | 9V battery `-` **and** Pico `GND` (common ground) |
| DRV8833 `AOUT1`/`AOUT2` | Motor A leads |
| DRV8833 `BOUT1`/`BOUT2` | Motor B leads |
| Buck converter IN+/IN− | 9V battery `+`/`−` |
| Buck converter OUT+/OUT− | Pico `VSYS` / `GND` (common ground) |
| Optocoupler A signal out (Motor A wheel) | `GP19` |
| Optocoupler B signal out (Motor B wheel) | `GP17` |
| Both optocouplers `VCC` | Pico `3V3` |
| Both optocouplers `GND` | Pico `GND` |

(Classes 1-2's circuits stay untouched on the breadboard alongside this.)

### Complete code

You need `motor_driver.py` and `wheel_odometry.py` on your `CIRCUITPY` drive either way (both
libraries, unchanged from Phases 1 and 3), plus either Option A's `code.py`, Option B's
`rover_server.py` and a thin `code.py` wrapper, or the Phase 5's Option C (`straight_drive.py` plus
its `code.py`). Unlike Phase 2, where `code.py` was the square/circle
attempt outright, this Class actually finishes with *two different things* your car could be
running — the square/circle attempt (Phase 2) or the rover status website (Phase 4) — since
nothing here makes them run at the same time. Pick one to run and swap between them by replacing
`code.py` (and, for Option B, `rover_server.py`). Both are shown below so you have the complete,
final version of each in one place.

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
    global last_direction_a, last_direction_b
    motor_a.throttle = _clamp(left)
    motor_b.throttle = _clamp(right)
    last_direction_a = _sign(left)
    last_direction_b = _sign(right)


def stop():
    global last_direction_a, last_direction_b
    motor_a.throttle = 0.0
    motor_b.throttle = 0.0
    last_direction_a = 0
    last_direction_b = 0
```

```python
# wheel_odometry.py -- wheel-speed odometry via slot IR optocouplers.
import time
import board
import countio
import motor_driver

WHEEL_DIAMETER_MM = 67
SLOTS_PER_REV = 20  # count your own wheel's encoder disc slots by hand and set this
SAMPLE_SECONDS = 0.25
WHEEL_CIRCUMFERENCE_CM = (WHEEL_DIAMETER_MM / 10) * 3.14159
WHEEL_CIRCUMFERENCE_PER_SLOT = WHEEL_CIRCUMFERENCE_CM / SLOTS_PER_REV
CMS_PER_TICK = WHEEL_CIRCUMFERENCE_PER_SLOT / SAMPLE_SECONDS   # cm/s of speed per counted tick

counter_a = countio.Counter(board.GP19)  # must be a PWM Channel B pin
counter_b = countio.Counter(board.GP17)


def _ticks_to_cms(ticks):
    revolutions = ticks / SLOTS_PER_REV
    return (revolutions * WHEEL_CIRCUMFERENCE_CM) / SAMPLE_SECONDS


def read_speed():
    counter_a.count = 0
    counter_b.count = 0
    time.sleep(SAMPLE_SECONDS)
    speed_left = _ticks_to_cms(counter_a.count)
    speed_right = _ticks_to_cms(counter_b.count)
    return (speed_left, motor_driver.last_direction_a,
            speed_right, motor_driver.last_direction_b)
```

**Option A — `code.py` as the square/circle attempt** (same as Phase 2, unchanged):

```python
# code.py -- complete project, option A: attempt a 35 cm square and 35 cm-diameter circle.

import time
import math
import motor_driver

SPEED = 0.5                    # calibrate per robot
SECONDS_PER_CM = 0.035        # calibrate per robot
SECONDS_PER_90_DEGREES = 0.4   # calibrate per robot


def drive_straight(cm):
    motor_driver.drive(SPEED, SPEED)
    time.sleep(cm * SECONDS_PER_CM)
    motor_driver.stop()


def turn_90():
    motor_driver.drive(-SPEED, SPEED)
    time.sleep(SECONDS_PER_90_DEGREES)
    motor_driver.stop()


def drive_square(side_cm=35):
    print("square, side", side_cm, "cm")
    for _ in range(4):
        drive_straight(side_cm)
        time.sleep(0.2)
        turn_90()
        time.sleep(0.2)


def drive_circle(diameter_cm=35):
    print("circle, diameter", diameter_cm, "cm")
    circumference = math.pi * diameter_cm
    segments = 24
    seg_length = circumference / segments
    seg_turn = SECONDS_PER_90_DEGREES / 9
    for _ in range(segments):
        drive_straight(seg_length)
        motor_driver.drive(-SPEED, SPEED)
        time.sleep(seg_turn)
        motor_driver.stop()


print("Class 3 project running -- square/circle attempt.")
drive_square(35)
time.sleep(1)
drive_circle(35)
```

**Option B — `rover_server.py` plus a thin `code.py` wrapper** (same as Phase 4, unchanged):

```python
# rover_server.py -- complete project, option B: rover status website (AP mode).

import os
import wifi
import socketpool
from adafruit_httpserver import Server, Request, Response, JSONResponse
import wheel_odometry

# AP_PASSWORD must be at least 8 characters -- start_ap() rejects shorter ones.
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

```python
# code.py -- runs the rover status website
import rover_server
```

**Option C — the Phase 5: `straight_drive.py` plus its `code.py`** (same as Section 8, unchanged):

```python
# straight_drive.py -- complete project, option C: drive straight with wheel feedback.
import time
import motor_driver
import wheel_odometry

BASE_THROTTLE = 0.5   # tune per robot
KI = 0.005            # [VERIFY] tune per robot
MAX_TRIM = 0.2        # [VERIFY]


def drive_straight_feedback(seconds):
    trim = 0.0        # positive slows the left wheel, negative slows the right wheel
    end_time = time.monotonic() + seconds
    motor_driver.drive(BASE_THROTTLE, BASE_THROTTLE)

    while time.monotonic() < end_time:
        speed_left, _, speed_right, _ = wheel_odometry.read_speed()
        error = speed_left - speed_right
        trim += KI * error
        trim = max(-MAX_TRIM, min(MAX_TRIM, trim))
        left = BASE_THROTTLE - max(trim, 0)
        right = BASE_THROTTLE + min(trim, 0)
        motor_driver.drive(left, right)
        print(" L:", round(speed_left, 1), " R:", round(speed_right, 1), " E:", round(error, 1), " trim:", round(trim, 3))

    motor_driver.stop()
```

```python
# code.py -- runs the open-loop vs. closed-loop straight-line comparison
import time
import motor_driver
import straight_drive

RUN_SECONDS = 4
RESET_SECONDS = 15

print("\nRun 1 -- open loop: equal throttle, no feedback")
motor_driver.drive(straight_drive.BASE_THROTTLE, straight_drive.BASE_THROTTLE)
time.sleep(RUN_SECONDS)
motor_driver.stop()

print("\nPut the car back on the start line, pointed down the line...")
time.sleep(RESET_SECONDS)

print("\nRun 2 -- closed loop: wheel feedback")
straight_drive.drive_straight_feedback(RUN_SECONDS)
print("done")
```

To satisfy this Class's milestone (a square/circle attempt *and* live wheel-speed telemetry
visible somewhere), run Option A first to demonstrate the drive, then swap in Option B (both
`rover_server.py` and its `code.py` wrapper) and spin a wheel by hand to show the website
updating — the two don't need to run at the same instant to prove both work.

## 12. What You Learned

You made your car move with real force for the first time, discovered exactly why moving it
*precisely* is harder than it sounds, then closed part of that gap yourself by giving your car a
way to measure its own wheel speed and publish it to a website it hosts. Specifically, you now
know:

* How an H-bridge lets a single motor spin both forward and reverse from simple logic-level
    signals, and why the DRV8833 needs two logic pins per motor (locked-antiphase control)
* Why PWM duty cycle isn't the same thing as motor speed — stall torque, friction, and voltage sag
    all eat into it
* Why the motors' raw 9V supply and your Pico's regulated 5V power (now from the same battery, via
    the buck converter) still need a shared ground reference to work together reliably
* What "open-loop control" (dead reckoning) means, and — from direct experience — why it drifts:
    no wheel/heading feedback to check against, battery voltage sag over time, and wheel slip or
    friction differences between the two motors
* How a slot IR optocoupler and its onboard LM393 comparator turn a spinning encoder disc into a
    clean digital pulse train your Pico can count directly, with no debouncing needed
* How to turn a tick count into a real wheel speed in cm/s, and why a single optocoupler per wheel
    can't tell you direction — and why borrowing the last-commanded direction from
    `motor_driver.py` is a reasonable, if imperfect, stand-in
* What it means for your Pico to host its own website: broadcasting its own WiFi network (access
    point mode), running `adafruit_httpserver`, and serving both a machine-readable `/data.json`
    route and a simple page that polls it, viewable from any laptop that joins the Pico's network
    with no serial cable
* (Phase 5) Why a car curves at equal throttle — no two motors are identical — and how closed-loop
    control fixes it: measure both wheels, compare, and nudge the faster one down until they match,
    using small corrections so measurement noise doesn't make the car wobble
* (Phase 6) How to tune a feedback loop by experiment: score each setting with the same measurements,
    change one number at a time, and stop when improvements fall below your noise floor

Knowing each wheel's real speed catches slip or stall — a wheel spinning slower than commanded, or
not at all — and, as the Phase 5 showed, lets the car even out its own wheels. But it still says
nothing about which way the *car* is pointed: two wheels can match speed while the car veers. That
gap — no way to check your heading against where you meant to be pointed — is exactly what an IMU
(inertial measurement unit) starts to address. That's next class, and it'll show up on this same
website.

---
## 13. Homework Assignment

No homework assignments have been written for this class yet. This section will be filled in with
optional take-home exercises, following the same format as the Pre-Class homework in
[`class-00-lesson-script.md`](class-00-lesson-script.md#10-homework-assignment) (what the code does, full commented code, and real-world examples).

Add the following:
* watchdog timer - [CircuitPython Watchdog Module](https://learn.adafruit.com/circuitpython-watchdog-module)

## References

* [Adafruit CircuitPython Motor Library — API Reference][01] — the `adafruit_motor.motor.DCMotor`
    API used in this script
* [Adafruit DRV8833 DC/Stepper Motor Driver Breakout Board][02] — the motor driver used this
    project, including its locked-antiphase and phase/enable control modes
* [Driving A DC Motor With CircuitPython][03] — background on PWM-based DC motor speed control
* [Slot Type IR Optocoupler for Motor Speed Detection - Product Page][04] — the wheel-odometry
    sensor used in `wheel_odometry.py`
* [Using an IR Slotted Optical Switch (Adafruit Learn)][05] — background on how a slotted
    optocoupler/comparator pair encodes motion as a digital pulse train
* [Wheel Encoders and Odometry (ROS/robotics primer)][06] — background on tick-to-speed conversion
    and why a single sensor per wheel can't resolve direction
* [Raspberry Pi Pico W Asynchronous Web Server – MicroPython Code][07] — background on hosting a
    small web server directly from a Pico's WiFi radio
* [`adafruit_httpserver` — API Reference][08] — the `Server`/`Request`/`Response`/`JSONResponse` API
    used in `rover_server.py`

---



[01]:https://docs.circuitpython.org/projects/motor/en/latest/api.html
[02]:https://learn.adafruit.com/adafruit-drv8833-dc-stepper-motor-driver-breakout-board
[03]:https://www.woolseyworkshop.com/2022/07/25/driving-a-dc-motor-with-circuitpython/
[04]:https://www.amazon.com/dp/B0B2NSQJDL
[05]:https://learn.adafruit.com/ir-breakbeam-sensors
[06]:https://articulatedrobotics.xyz/mobile-robot-8-odometry/
[07]:https://electrocredible.com/raspberry-pi-pico-w-web-server-asynchronous-micropython/
[08]:https://docs.circuitpython.org/projects/httpserver/en/latest/api.html

[20]:https://pico2w.pinout.xyz/
[37]:https://howtomechatronics.com/tutorials/arduino/ultrasonic-sensor-hc-sr04/
[38]:https://www.hackster.io/chip-pk/sg90-servo-motor-interfacing-with-arduino-complete-beginner-849eef
[39]:https://learn.adafruit.com/adafruit-drv8833-dc-stepper-motor-driver-breakout-board/pinouts
[40]:https://www.handsontec.com/dataspecs/sensor/Slot%20IR%20Detector.pdf

