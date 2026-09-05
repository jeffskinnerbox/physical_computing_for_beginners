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

Once you've named "no wheel feedback" as one of those reasons, you'll close part of that gap
yourself: mount a Slot Type IR Optocoupler at each driven wheel to read the wheel-speed encoder disc
already molded into your chassis kit's wheels, and write `wheel_odometry.py` to turn counted ticks
into a real wheel speed in cm/s — while learning why that same sensor, on its own, can't tell you
which way the wheel is turning. Finally, you'll stand up the first version of a Pico-hosted rover
status website, `rover_server.py`, so live wheel speed and direction show up on a laptop browser
with no serial cable at all. This website is built small on purpose — later classes will each add
more to this same site rather than you building a new one.

## 2. What You'll Need

| Component | Quantity | Purpose This Project |
| :---------- | :--------: | :---------------------- |
| Raspberry Pi Pico 2 W (with header) | 1 | Runs your CircuitPython code |
| DRV8833 dual H-bridge motor driver breakout | 1 | Drives both DC gearbox motors from PWM logic signals |
| Emo Smart Robot Car Chassis Kit | 1 | The two motors under test and the chassis they drive |
| 9V battery clip and 9V battery | 1 each | Separate power for the motors, independent of the Pico's logic power |
| Slot Type IR Optocoupler for Motor Speed | 2 | Reads each driven wheel's built-in encoder disc for wheel-odometry tick counting |
| Breadboard (from Classes 1-2) | 1 | Your existing circuits stay on it, untouched |
| Dupont jumper wires | ~10 | Point-to-point connections |
| USB cable | 1 | Powers the Pico and carries the serial console |
| Laptop with Mu or Thonny | 1 | Where you write/save code and read the serial console |
| Classroom WiFi network (shared) | 1 | Your Pico joins this network to host the rover status website |
| Marked 12" square / 12"-diameter circle test track | 1 (shared) | Your target for the calibration exercise |

**Additional components for the Homework Assignments** (Section 11) — no homework has been written
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

**Slot Type IR Optocoupler (wheel-speed sensor).** Each optocoupler module is a small IR LED and
phototransistor facing each other across a slot, plus an onboard LM393 comparator chip. Your
chassis kit's wheel already has an encoder disc with alternating slots and teeth molded around its
rim; as the wheel spins, each tooth interrupts the LED-to-phototransistor beam once per slot. The
LM393 comparator turns that raw interruption into a clean digital HIGH/LOW pulse — no debouncing
needed the way your Class 1 switch/encoder needed it, since this is a much faster, cleaner signal
straight off a comparator chip, not a noisy mechanical contact.

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
away, reached over the internet. Today's website is the opposite: your Pico 2 W's own WiFi radio
joins the classroom network, runs a tiny HTTP server (`adafruit_httpserver`) directly in
CircuitPython, and answers requests at its own local IP address — the server, the sensor, and the
thing being measured are all in your hand. `rover_server.py` serves two things at that address: a
`/data.json` route (current wheel speed/direction, as machine-readable JSON) and a simple HTML page
that polls `/data.json` every fraction of a second and displays it — so any laptop on the same
network can watch live wheel telemetry with no serial cable at all.

**Pinout summary** (Raspberry Pi Pico 2 W — new pins only; Classes 1-2 are unaffected):

| Pin | What we use it for |
| :---- | :-------------------- |
| `GP9` | DRV8833 `AIN1` (Motor A) |
| `GP10` | DRV8833 `AIN2` (Motor A) |
| `GP11` | DRV8833 `BIN1` (Motor B) |
| `GP12` | DRV8833 `BIN2` (Motor B) |
| `GP16` | Optocoupler A signal out (Motor A wheel) |
| `GP17` | Optocoupler B signal out (Motor B wheel) |
| 9V battery `+` | DRV8833 `VM` (motor power) |
| 9V battery `-` and Pico `GND` | DRV8833 `GND` (common ground) |
| Pico `3V3` | Both optocouplers `VCC` |
| Pico `GND` | Both optocouplers `GND` |

## 4. Build It: Phase 1 — Motor Driver Library and Basic Test

### Wiring for this phase

This is the complete wiring for the whole project, including the two optocouplers you'll mount and
use starting in Phase 3 — nothing changes for Phase 2, 3, or 4. You can wire the optocouplers now
too, but leave them unmounted at each wheel until Phase 3, once you've counted each disc's slots.

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

Your Class 1 and Class 2 circuits stay exactly where they are on the breadboard. Before writing
any code, trace this wiring out loud, and specifically confirm the Pico's `GND` is jumpered to the
DRV8833's `GND` — a missing common ground is the wiring mistake that produces the most confusing
symptoms later (logic that "sort of" works, or works intermittently).

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

## 6. Build It: Phase 3 — Wheel Odometry

### Wiring for this phase

No new wiring if you already wired both optocouplers back in Phase 1 — what's new is mounting them.
Mount each optocoupler so its slotted fork straddles the wheel's built-in encoder disc without
rubbing against it, then turn each wheel slowly by hand and count the disc's slots — you'll need
that count in a moment.

| Component | Pico 2 W Pin |
| :---------- | :------------- |
| Optocoupler A signal out (Motor A wheel) | `GP16` |
| Optocoupler B signal out (Motor B wheel) | `GP17` |
| Both optocouplers `VCC` | Pico `3V3` |
| Both optocouplers `GND` | Pico `GND` |

### What this code does

`wheel_odometry.py` is a second library file, saved alongside `motor_driver.py` — it doesn't run on
its own either. It uses the built-in `countio` module to count optocoupler pulses on `GP16`/`GP17`
over a short sampling window (`SAMPLE_SECONDS`), converts that tick count to a wheel speed in cm/s
using `SLOTS_PER_REV` and the 67mm wheel diameter (see Section 3's math walkthrough), and pairs each
wheel's speed with `motor_driver`'s last-commanded direction for that same wheel — since, as Section
3 explained, the optocoupler alone can't tell you which way the wheel is turning.

Before this will read correctly, set `SLOTS_PER_REV` below to the number of slots you counted by
hand on your own wheel's disc — the value shown is a placeholder, not a measurement.

### The code

Save this as `wheel_odometry.py` on your `CIRCUITPY` drive.

```python
# class-3-code-3.py -- save as wheel_odometry.py
# Wheel-speed odometry via slot IR optocouplers -- tick RATE from GP16/GP17,
# direction borrowed from motor_driver's last-commanded state.

import time
import board
import countio
import motor_driver

WHEEL_DIAMETER_MM = 67
SLOTS_PER_REV = 20  # count your own wheel's encoder disc slots by hand and set this
WHEEL_CIRCUMFERENCE_CM = (WHEEL_DIAMETER_MM / 10) * 3.14159
SAMPLE_SECONDS = 0.25  # sampling window for one speed reading

counter_a = countio.Counter(board.GP16)  # Motor A wheel
counter_b = countio.Counter(board.GP17)  # Motor B wheel


def _ticks_to_cms(ticks):
    """Convert a tick count, taken over SAMPLE_SECONDS, to a speed in cm/s."""
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

Test it with a short scratch `code.py` that drives forward and prints `read_speed()` each cycle:

```python
# Scratch test script for wheel_odometry.py.
import motor_driver
import wheel_odometry

motor_driver.drive(0.5, 0.5)
for _ in range(10):
    print(wheel_odometry.read_speed())
motor_driver.stop()
```

### Try it / what you should see

You should see ten printed tuples of `(speed_left_cms, dir_left, speed_right_cms, dir_right)`, with
both speeds rising above `0.0` while the car drives forward and `dir_left`/`dir_right` both reading
`1`. Stop the car (`motor_driver.stop()`), then try `motor_driver.drive(-0.5, -0.5)` and rerun the
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

## 7. Build It: Phase 4 — Rover Status Website

### Wiring for this phase

No new wiring — this phase is all software. Add `WIFI_SSID` and `WIFI_PASSWORD` to your
`settings.toml` file if they aren't already filled in.

### What this code does

`rover_server.py` joins the classroom WiFi network and starts an `adafruit_httpserver` HTTP server
that answers two routes: `/data.json` (the current wheel speed and direction from
`wheel_odometry.read_speed()`, as machine-readable JSON) and `/` (a bare HTML page with a bit of
JavaScript that polls `/data.json` twice a second and displays it). This file *is* your `code.py`
for this phase — it ends in its own `while True:` loop that keeps answering requests forever, the
same way Phase 2's `code.py` ran the square/circle attempt directly rather than being imported by
something else.

### The code

Save this as `code.py` on your `CIRCUITPY` drive, replacing Phase 3's scratch test script.
`motor_driver.py` and `wheel_odometry.py` stay on the drive unchanged — this file imports
`wheel_odometry` (which in turn imports `motor_driver`).

```python
# class-3-code-4.py -- save as code.py
# Pico-hosted rover status website -- joins WiFi, serves /data.json plus a
# minimal page that polls it.

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

print("Class 3, Phase 4 -- rover status website starting...")
while True:
    server.poll()
```

### Try it / what you should see

Watch the serial console for a line like `rover server -- listening at 192.168.1.42`. Open a
browser on a laptop that's on the *same* WiFi network and go to that address — you should see
`Rover Status` and a block of JSON that updates itself twice a second. Spin a wheel by hand and
watch that wheel's `speed_left_cms` or `speed_right_cms` jump on the page, even though nothing told
the motor to move — a concrete reminder that this reading is measured, independent of whatever the
motor was last commanded to do, while direction is not.

If the server never connects, double-check `settings.toml`'s WiFi credentials first, then confirm
your laptop is on the *same* network as the Pico. If the page loads but never updates, try a hard
refresh — your browser may be caching an old copy of the page.

### Checkpoint

Open a browser to your Pico's printed IP address, confirm the `/data.json` fields update live when
you spin a wheel by hand, and be able to say in one sentence why the direction shown on the page is
"what we last told the car to do," not something the optocoupler itself measured.

## 8. Troubleshooting Guide

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
| Wheel speed reads `0.0` while the wheel is visibly spinning | Optocoupler's slot isn't straddling the encoder disc, or its wiring is loose | Remount the optocoupler so the disc's teeth pass through the slot; reseat `VCC`/`GND`/signal jumpers |
| Wheel speed reading is wildly too high or too low | `SLOTS_PER_REV` miscounted for that wheel's disc | Recount the disc's slots by hand and update `SLOTS_PER_REV` |
| Direction shown never changes even when the car reverses | `wheel_odometry.py` was saved before `motor_driver.py` was updated with direction tracking | Confirm `motor_driver.py` on your `CIRCUITPY` drive includes the `last_direction_a`/`last_direction_b` tracking shown in Phase 1 |
| `wifi.radio.connect()` hangs or raises `ConnectionError` | Wrong SSID/password in `settings.toml`, or the classroom network is blocking the connection | Double-check `settings.toml`; ask your instructor whether the network allows device-to-device traffic |
| Website never loads in the browser, but the Pico prints an IP address | Your laptop is on a different network/VLAN than the Pico | Confirm your laptop is joined to the same classroom WiFi network as the Pico |
| Website loads once but never updates | `server.poll()` not being called every loop, or the browser is caching the page | Confirm the `while True: server.poll()` loop is running; try a hard refresh |

## 9. Put It All Together

This is the finished project in one place — a calibrated square/circle attempt, wheel-speed
odometry, and your own rover status website, without going through the individual phases above.

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
| Optocoupler A signal out (Motor A wheel) | `GP16` |
| Optocoupler B signal out (Motor B wheel) | `GP17` |
| Both optocouplers `VCC` | Pico `3V3` |
| Both optocouplers `GND` | Pico `GND` |

(Classes 1-2's circuits stay untouched on the breadboard alongside this.)

### Complete code

You need **three files** on your `CIRCUITPY` drive: `motor_driver.py` and `wheel_odometry.py`
(both libraries, unchanged from Phases 1 and 3), plus `code.py`. Unlike Phase 2, where `code.py`
was the square/circle attempt, this Class actually finishes with *two different things* `code.py`
could be — the square/circle attempt (Phase 2) or the rover status website (Phase 4) — since
nothing here makes them run at the same time. Save whichever one you want running as `code.py`;
swap between them by replacing that one file. Both are shown below so you have the complete,
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
WHEEL_CIRCUMFERENCE_CM = (WHEEL_DIAMETER_MM / 10) * 3.14159
SAMPLE_SECONDS = 0.25

counter_a = countio.Counter(board.GP16)
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
# code.py -- complete project, option A: attempt a 12" square and 12"-diameter circle.
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

**Option B — `code.py` as the rover status website** (same as Phase 4, unchanged):

```python
# code.py -- complete project, option B: rover status website.
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

print("Class 3, Phase 4 -- rover status website starting...")
while True:
    server.poll()
```

To satisfy this Class's milestone (a square/circle attempt *and* live wheel-speed telemetry
visible somewhere), run Option A first to demonstrate the drive, then swap in Option B and spin a
wheel by hand to show the website updating — the two don't need to run at the same instant to
prove both work.

## 10. What You Learned

You made your car move with real force for the first time, discovered exactly why moving it
*precisely* is harder than it sounds, then closed part of that gap yourself by giving your car a
way to measure its own wheel speed and publish it to a website it hosts. Specifically, you now
know:

* How an H-bridge lets a single motor spin both forward and reverse from simple logic-level
    signals, and why the DRV8833 needs two logic pins per motor (locked-antiphase control)
* Why PWM duty cycle isn't the same thing as motor speed — stall torque, friction, and voltage sag
    all eat into it
* Why two separate power supplies (the Pico's logic power and the motors' 9V battery) still need a
    shared ground reference to work together reliably
* What "open-loop control" (dead reckoning) means, and — from direct experience — why it drifts:
    no wheel/heading feedback to check against, battery voltage sag over time, and wheel slip or
    friction differences between the two motors
* How a slot IR optocoupler and its onboard LM393 comparator turn a spinning encoder disc into a
    clean digital pulse train your Pico can count directly, with no debouncing needed
* How to turn a tick count into a real wheel speed in cm/s, and why a single optocoupler per wheel
    can't tell you direction — and why borrowing the last-commanded direction from
    `motor_driver.py` is a reasonable, if imperfect, stand-in
* What it means for your Pico to host its own website: joining WiFi, running
    `adafruit_httpserver`, and serving both a machine-readable `/data.json` route and a simple page
    that polls it, viewable from any laptop on the same network with no serial cable

Knowing each wheel's real speed catches slip or stall — a wheel spinning slower than commanded, or
not at all — but it still says nothing about which way the *car* is pointed. That gap — no way to
check your heading against where you meant to be pointed — is exactly what an IMU (inertial
measurement unit) starts to address. That's next class, and it'll show up on this same website.

----
## 11. Homework Assignment

No homework assignments have been written for this class yet. This section will be filled in with
optional take-home exercises, following the same format as the Pre-Class homework in
[`class-00-lesson-script.md`](class-00-lesson-script.md#10-homework-assignment) (what the code
does, full commented code, and real-world examples).

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
