# Lesson Script: Class 5 — Build the Random Rover: Collision Avoidance


* **Class:** 5 of 6 (plus Pre-Class)
* **Duration:** ~2 hours
* **What You'll Need:** see [Section 2](#2-what-youll-need)
* **Before You Start:** Your Class 2 sensor+servo circuit (`GP6`-`GP8`) and Class 3 motor driver
    circuit (`GP9`-`GP12`) should both still be working exactly as you left them. You'll also need
    your Class 3 turn-time calibration notes (`SECONDS_PER_90_DEGREES` or similar) from your build
    journal. Class 1's button/encoder circuit isn't needed today — leave it in place or set it
    aside. Class 3's wheel-odometry optocouplers (`GP16`/`GP17`) and Class 4's IMU (`GP0`/`GP1`) are
    also not read by today's code directly, but they **must stay wired and powered** — the rover
    status website (`rover_server.py`) still reports wheel speed/direction and orientation from
    those same circuits, and today's website edit adds to that same page rather than replacing it.
    That website should still connect to the classroom WiFi and serve `/data.json` with all seven
    existing fields from Classes 3-4 — a quick spot-check, not a rebuild.

---


## 1. What This Project Is

This is the class where everything you've built so far becomes one robot that makes its own
decisions. You're combining your Class 2 sensor-on-servo sweep with your Class 3 motor driver into
a single program: the car drives forward at a constant speed, periodically stops to sweep the
sensor and look for the clearest direction, and steers that way — with an emergency path that
stops and rescans immediately if something gets too close while driving, instead of waiting for
the next scheduled look.

Most of what you need is already on your breadboard from Class 2 and Class 3 — Today is mostly
about writing the decision-making that connects your car's eyes to its legs. The one new wiring
today: a limit switch and an IR obstacle sensor, two fixed safety inputs that give your car a
last-resort "stop no matter what" reflex, backing up the ultrasonic sweep. By the end, your car
should be able to drive around the room on its own and steer around at least one obstacle without
you touching it — the central milestone of the whole course.

The rover status website keeps growing too, and today it hits a real turning point. Class 3 gave
it live wheel speed/direction, Class 4 added orientation — but both of those classes had to present
the website as a separate, alternative `code.py` (Option A/B) from that class's other program,
because `rover_server.py` ended in its own blocking `while True: server.poll()` loop and nothing
else could run at the same time. Today's collision-avoidance program is different: it genuinely
needs to keep driving, scanning, and checking safety sensors continuously **while** the website
stays live, so you can watch the rover's decisions from across the room as it drives around
avoiding obstacles. That means today `rover_server.py` finally changes shape — from a
self-contained script into a small library that `class-5-code.py`'s own main loop imports and
polls each cycle. It's a small amount of new code, but a real structural change worth understanding,
not just copying.

## 2. What You'll Need

| Component | Quantity | Purpose This Project |
| :---------- | :--------: | :---------------------- |
| Raspberry Pi Pico 2 W (with header) | 1 | Runs your CircuitPython code |
| HC-SR04 ultrasonic distance sensor (from Class 2) | 1 | Measures distance at each scan angle |
| SG90 micro servo motor (from Class 2) | 1 | Sweeps the sensor across the scan angles |
| DRV8833 dual H-bridge motor driver (from Class 3) | 1 | Drives forward and executes steering turns |
| Micro limit switch | 1 | Physical bumper on the chassis front — last-resort stop-and-reverse on contact |
| IR obstacle avoidance sensor | 1 | Fixed forward-facing near-field detector — stop-and-reverse between ultrasonic scans |
| Emo Smart Robot Car Chassis Kit | 1 | Your completed (or near-complete) car |
| 9V battery clip and 9V battery | 1 each | Motor power, independent of the Pico's logic power |
| Breadboard (from prior classes) | 1 | No rewiring needed today |
| USB cable or portable battery | 1 | Power for untethered floor runs |
| Laptop with Mu or Thonny | 1 | Where you write/save code and read the serial console |
| Classroom WiFi network (shared, from Class 3) | 1 | Already-joined network the growing rover status website runs on — nothing new to set up |
| Open floor area with soft obstacles | shared | Test space for autonomous driving runs |

**Additional components for the Homework Assignments** (Section 9) — no homework has been written
for this class yet; this section will be filled in when that content is added.

## 3. Meet the Hardware

There's no new hardware today — this class is about combining two circuits you've already built
and tested separately. A quick recap of what each one contributes:

**From Class 2: the sensor+servo "eyes."** Your HC-SR04, mounted on the SG90 servo, can sweep
across a range of angles and report a distance at each one. Today, instead of sweeping
continuously back and forth, the rover sweeps a small fixed set of angles (`SCAN_ANGLES`) each
time it stops to look, then picks whichever angle had the most open space.

**From Class 3: the motor driver "legs."** Your `motor_driver.py` library's `drive(left, right)`
and `stop()` functions are what actually move the car and execute turns. Today's code imports that
same file unchanged — the turn-time calibration you found in Class 3 (`SECONDS_PER_90_DEGREES` or
similar) gets reused directly here as `TURN_SECONDS_PER_DEGREE`.

**What's new today is the logic connecting them** — a control pattern called **stop-look-go**:
drive straight, and periodically (or immediately, if something gets too close) stop, sweep, pick
the clearest direction, turn, and resume. That pattern is a genuine design tradeoff: stopping to
scan is simple and safe, since the sensor never has to interpret a reading taken while the whole
robot is also moving — but it's slower than continuously sensing while driving would be.

**From Class 3/4's website, still running: the wheel odometry optocouplers and the IMU.** Your
Class 3 `GP16`/`GP17` optocoupler circuit and Class 4's `GP0`/`GP1` IMU circuit don't get read by
`class-5-code.py` at all — today's collision-avoidance logic only touches `GP6`-`GP13`. But leave
both circuits wired and powered anyway: `rover_server.py` still reads them to report wheel
speed/direction and orientation on the rover status website, and today's website edit (Phase 2
below) adds to that same page rather than replacing it.

**Growing a website into a library.** Building the Class 3 website from scratch meant standing up
WiFi, an HTTP server, a route, and a page all at once. Classes 3 and 4 each grew it by adding a few
more keys to the same `/data.json` dict — small edits, but both classes' `rover_server.py` still
ended in its own blocking `while True: server.poll()` loop, which is why each of those classes had
to offer the website as a separate, alternative `code.py` rather than something that ran alongside
that class's other program. Today's Phase 2 does something new: it turns `rover_server.py` from a
script that owns its own infinite loop into a small library — it exposes the already-built `server`
object and a `scan_status` dict, and lets `class-5-code.py`'s own drive loop call
`rover_server.server.poll()` once per cycle. That's the one genuinely new idea this Class adds to
the website thread; everything else about it (the route, the page, the JSON shape) works exactly
like it did in Classes 3-4.

**Pinout summary** (Class 2 and Class 3 pins reconnect exactly as wired; `GP5`/`GP13` are new; the
Class 3 optocoupler and Class 4 IMU pins below stay wired for the website but aren't read by
`class-5-code.py`'s collision-avoidance logic):

| Pin | What it does | From Class |
| :---- | :--------------- | :----------- |
| `GP6` | HC-SR04 `TRIG` | Class 2 |
| `GP7` | HC-SR04 `ECHO`, through voltage-divider | Class 2 |
| `GP8` | SG90 servo signal | Class 2 |
| `GP9`/`GP10` | DRV8833 `AIN1`/`AIN2` (Motor A) | Class 3 |
| `GP11`/`GP12` | DRV8833 `BIN1`/`BIN2` (Motor B) | Class 3 |
| `GP5` | Limit switch (internal pull-up) | New this Class |
| `GP13` | IR obstacle sensor `OUT` | New this Class |
| `GP16`/`GP17` | Wheel-odometry optocouplers (website only) | Class 3 |
| `GP0`/`GP1` | LSM9DS1 IMU `SDA`/`SCL` (website only) | Class 4 |

## 4. Build It: Phase 1 — The Collision-Avoidance Program

### Wiring for this phase

Reconnect (or simply confirm) Class 2's sensor+servo circuit and Class 3's motor driver circuit
exactly as they were left wired, then add the two new safety sensors:

| Component | Pico 2 W Pin |
| :---------- | :------------- |
| HC-SR04 `TRIG` | `GP6` |
| HC-SR04 `ECHO`, through voltage-divider resistors | `GP7` |
| SG90 servo signal | `GP8` |
| DRV8833 `AIN1`/`AIN2` (Motor A) | `GP9`/`GP10` |
| DRV8833 `BIN1`/`BIN2` (Motor B) | `GP11`/`GP12` |
| Limit switch (common + normally-open, to `GND`) | `GP5` (internal pull-up) |
| IR obstacle sensor `OUT` | `GP13` |

Mount the limit switch as a physical bumper on the chassis front (lever arm leading, so any contact
presses it), and the IR sensor fixed and forward-facing, low on the chassis, aimed at ground-level
obstacles the ultrasonic sweep might miss between scans.

Before writing any new code, power up and re-verify both older circuits independently: run a quick
sensor sweep test and a quick motor forward/reverse test, confirming both still work exactly as
they did at the end of Class 2 and Class 3. Catching a regression now is far easier than debugging
it once it's buried inside the combined rover logic.

### What this code does

This program is the "stop-look-go" cycle described above, running forever. It drives forward,
watches for either a scan timer to elapse, an obstacle to come within `STOP_DISTANCE_CM`, or the
new limit switch/IR sensor to fire, stops (reversing briefly first if it was the switch or IR
sensor), sweeps `SCAN_ANGLES` recording a distance at each one, picks the angle with the largest
distance (the most open space), turns toward it using your Class 3 turn-time calibration, and
resumes driving.

**Important:** `motor_driver.py` from Class 3 must still be present on your `CIRCUITPY` drive —
this code imports it rather than reimplementing motor control.

### The code

Save this as `code.py`, replacing whatever was there before. `motor_driver.py` should already be
sitting alongside it, unchanged since Class 3.

```python
# class-5-code.py
# Random Rover: drives forward, rescans on a timer or on proximity,
# steers toward the clearest heading.

import time
import board
import digitalio
import pwmio
import adafruit_hcsr04
from adafruit_motor import servo
import motor_driver  # from Class 3 -- must already be on CIRCUITPY

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP6, echo_pin=board.GP7)
pwm = pwmio.PWMOut(board.GP8, duty_cycle=0, frequency=50)
scan_servo = servo.Servo(pwm, min_pulse=500, max_pulse=2500)  # recalibrate per servo if needed

# The two new fixed safety sensors -- both are digital, LOW when triggered.
bump_switch = digitalio.DigitalInOut(board.GP5)
bump_switch.direction = digitalio.Direction.INPUT
bump_switch.pull = digitalio.Pull.UP

ir_sensor = digitalio.DigitalInOut(board.GP13)
ir_sensor.direction = digitalio.Direction.INPUT

# Tune these for your specific robot -- start conservative and adjust
# during Independent Work.
DRIVE_SPEED = 0.4                     # lower than Class 3's test speed -- safer for autonomous runs
SCAN_ANGLES = [30, 60, 90, 120, 150]  # degrees, left to right
SETTLE_TIME = 0.15                    # seconds -- let the servo stop moving before trusting a reading
STOP_DISTANCE_CM = 25                 # distance that triggers an immediate rescan
SCAN_INTERVAL = 3.0                   # seconds -- rescan on this timer even if nothing is close
# Reuse Class 3's SECONDS_PER_90_DEGREES calibration here, converted to a
# per-degree rate: replace 0.4 with your own measured 90-degree turn time.
TURN_SECONDS_PER_DEGREE = 0.4 / 90

CENTER_ANGLE = 90


def read_distance():
    """Read the sensor, returning None instead of crashing on a missed echo."""
    try:
        return sonar.distance
    except RuntimeError:
        return None


def scan():
    """Sweep SCAN_ANGLES, print each reading, and return the angle with the most open space."""
    readings = {}
    for angle in SCAN_ANGLES:
        scan_servo.angle = angle
        time.sleep(SETTLE_TIME)  # same settle-then-read pattern from Class 2
        readings[angle] = read_distance()
        print("scan: angle", angle, "distance_cm", readings[angle])
    valid = {a: d for a, d in readings.items() if d is not None}
    # If every reading failed, fall back to driving straight ahead.
    best_angle = max(valid, key=valid.get) if valid else CENTER_ANGLE
    print("scan: chosen heading", best_angle)
    return best_angle, readings


def turn_toward(angle):
    """Turn the car toward the chosen scan angle, using the Class 3 turn-time calibration."""
    degrees_off_center = angle - CENTER_ANGLE
    turn_time = abs(degrees_off_center) * TURN_SECONDS_PER_DEGREE
    if degrees_off_center == 0 or turn_time < 0.02:
        print("drive: no turn needed")
        return
    direction = "right" if degrees_off_center > 0 else "left"
    print("drive: turning", direction, "for", round(turn_time, 2), "s")
    if degrees_off_center > 0:
        motor_driver.drive(DRIVE_SPEED, -DRIVE_SPEED)
    else:
        motor_driver.drive(-DRIVE_SPEED, DRIVE_SPEED)
    time.sleep(turn_time)
    motor_driver.stop()


def safety_override_triggered():
    """Check the fixed bump switch and IR sensor -- either one true means stop NOW."""
    if not bump_switch.value:  # pulled LOW when pressed
        print("SAFETY: bump switch contact")
        return True
    if not ir_sensor.value:  # module drives LOW when it sees an obstacle
        print("SAFETY: IR sensor near-field obstacle")
        return True
    return False


print("Class 5 -- Random Rover starting...")
scan_servo.angle = CENTER_ANGLE
last_scan_time = time.monotonic()

while True:
    print("drive: forward")
    motor_driver.drive(DRIVE_SPEED, DRIVE_SPEED)

    # Drive straight until EITHER the scan timer elapses, something gets too
    # close on the ultrasonic sensor, OR the bump switch/IR sensor fires.
    close_call = False
    while True:
        if safety_override_triggered():
            motor_driver.stop()
            print("drive: emergency stop-and-reverse (safety override)")
            motor_driver.drive(-DRIVE_SPEED, -DRIVE_SPEED)
            time.sleep(0.3)  # back off enough to clear whatever triggered it
            motor_driver.stop()
            close_call = True
            break
        distance = read_distance()
        if distance is not None and distance < STOP_DISTANCE_CM:
            print("drive: obstacle close, distance_cm", distance)
            close_call = True
            break
        if time.monotonic() - last_scan_time >= SCAN_INTERVAL:
            break
        time.sleep(0.05)

    motor_driver.stop()
    print("drive: stopped for scan" if not close_call else "drive: emergency stop for scan")
    heading, _readings = scan()
    turn_toward(heading)
    last_scan_time = time.monotonic()
```

### Try it / what you should see

Set your rover down and watch the console: `drive: forward`, then either `drive: stopped for scan`
(timer) or `drive: emergency stop for scan` (something got close), followed by a `scan: angle ...
distance_cm ...` line for each angle in `SCAN_ANGLES`, then `scan: chosen heading`, then a
`drive: turning left/right for ... s` line (or `drive: no turn needed`), then back to
`drive: forward`. Physically, you should see the car drive, pause, watch the sensor sweep, turn,
and continue — repeating on its own.

A first run doesn't need to be perfect — a jerky turn or an overly cautious `STOP_DISTANCE_CM` is
completely normal to see before you tune it in Independent Work.

### Checkpoint

Confirm your rover completes at least one full stop-look-go cycle — drive, stop, scan with printed
readings, turn, resume driving — without you touching the keyboard once it starts. Then place an
obstacle in its path while it's driving and confirm it stops immediately (an `emergency stop for
scan` line), not waiting for the next scheduled timer scan. Finally, confirm the two new safety
sensors independently: press the limit switch by hand and confirm a `SAFETY: bump switch contact`
line and a stop-and-reverse, then wave your hand close in front of the IR sensor and confirm
`SAFETY: IR sensor near-field obstacle`.

## 5. Build It: Phase 2 — Extend the Rover Status Website With the Collision-Avoidance Decision

### Wiring for this phase

No new wiring. This phase edits software only — the same `rover_server.py` you've been growing
since Class 3, plus a small addition to `class-5-code.py` from Phase 1.

### What this code does

Recall `rover_server.py`'s `/data.json` route: it already returns `speed_left_cms`/`dir_left`/
`speed_right_cms`/`dir_right` (Class 3) and `roll`/`pitch`/`yaw` (Class 4), and the webpage
displays any field that dict has with no HTML/JavaScript changes needed — the same reason Class
4's edit was small. Today adds three more flat fields, matching that same style:

* `scan_heading` — a number, the last chosen scan angle in degrees (starts centered at `90`)
* `drive_state` — a string, one of `"driving"`, `"scanning"`, or `"stopped"`
* `stop_reason` — a string, one of `"none"`, `"ultrasonic"`, `"ir"`, or `"limit_switch"`, naming
    whichever safety signal most recently forced a stop

Here's the wrinkle: Class 4's `rover_server.py` ends in its own blocking `while True:
server.poll()` loop, but Phase 1's `class-5-code.py` needs to run its *own* continuous drive/scan
loop — and two blocking loops can't run at once. So today's edit does a small refactor: instead of
owning the polling loop itself, `rover_server.py` stops after calling `server.start(...)` and
exposes its already-built `server` object and a new `scan_status` dict for `class-5-code.py` to
update and poll each cycle.

### The code

First, edit `rover_server.py` (the same file from Classes 3-4, still saved as `rover_server.py` —
not `code.py`): add the `scan_status` dict, add the three new keys to `/data.json`, and delete its
old `while True: server.poll()` loop.

```python
# rover_server.py -- edited again (same file from Classes 3-4, no new filename).
# Removes its own "while True: server.poll()" loop -- class-5-code.py's drive
# loop now calls server.poll() itself once per cycle, since only one loop can
# own the CPU at a time. Adds scan_status, a small dict class-5-code.py updates
# each cycle with the collision-avoidance decision, merged into /data.json.
scan_status = {
    "scan_heading": 90,        # degrees -- last chosen heading, starts centered
    "drive_state": "driving",  # "driving" | "scanning" | "stopped"
    "stop_reason": "none",     # "none" | "ultrasonic" | "ir" | "limit_switch"
}


@server.route("/data.json")
def data_json(request: Request):
    speed_left, dir_left, speed_right, dir_right = wheel_odometry.read_speed()
    roll, pitch, yaw = _read_orientation()
    return JSONResponse(request, {
        "speed_left_cms": speed_left,
        "dir_left": dir_left,
        "speed_right_cms": speed_right,
        "dir_right": dir_right,
        "roll": roll,
        "pitch": pitch,
        "yaw": yaw,
        "scan_heading": scan_status["scan_heading"],
        "drive_state": scan_status["drive_state"],
        "stop_reason": scan_status["stop_reason"],
    })


@server.route("/")
def index(request: Request):
    return Response(request, STATUS_PAGE, content_type="text/html")


server.start(str(wifi.radio.ipv4_address))
# NOTE: the old "while True: server.poll()" loop is gone from this file --
# class-5-code.py's own main loop polls it now (see below).
```

Then a small addition to `class-5-code.py` itself: import `rover_server`, poll it once per loop
iteration so requests still get answered while the rover drives, and keep `scan_status` updated
with the live decision. This changes `safety_override_triggered()` to return a `stop_reason`
string instead of a bare `True`/`False`, so the website can show *which* signal fired, not just
that one did.

```python
# class-5-code.py -- Phase 2 additions (add alongside the Phase 1 code above)
import rover_server  # Classes 3-4's website; today's edit removed its own poll() loop


def safety_override_triggered():
    """Check the fixed bump switch and IR sensor; return a stop_reason string
    ("none" if neither is triggered) instead of a bare bool, so the caller can
    publish which signal fired to the rover status website."""
    if not bump_switch.value:  # pulled LOW when pressed
        print("SAFETY: bump switch contact")
        return "limit_switch"
    if not ir_sensor.value:  # module drives LOW when it sees an obstacle
        print("SAFETY: IR sensor near-field obstacle")
        return "ir"
    return "none"


print("Class 5 -- Random Rover starting...")
scan_servo.angle = CENTER_ANGLE
last_scan_time = time.monotonic()

while True:
    rover_server.server.poll()  # answer any pending website request, non-blocking
    rover_server.scan_status["drive_state"] = "driving"
    print("drive: forward")
    motor_driver.drive(DRIVE_SPEED, DRIVE_SPEED)

    stop_reason = "none"
    while True:
        rover_server.server.poll()
        stop_reason = safety_override_triggered()
        if stop_reason != "none":
            motor_driver.stop()
            print("drive: emergency stop-and-reverse (safety override)")
            motor_driver.drive(-DRIVE_SPEED, -DRIVE_SPEED)
            time.sleep(0.3)  # back off enough to clear whatever triggered it
            motor_driver.stop()
            break
        distance = read_distance()
        if distance is not None and distance < STOP_DISTANCE_CM:
            print("drive: obstacle close, distance_cm", distance)
            stop_reason = "ultrasonic"
            break
        if time.monotonic() - last_scan_time >= SCAN_INTERVAL:
            break
        time.sleep(0.05)

    rover_server.scan_status["stop_reason"] = stop_reason
    rover_server.scan_status["drive_state"] = "scanning"
    motor_driver.stop()
    print("drive: stopped for scan" if stop_reason == "none" else "drive: emergency stop for scan")
    heading, _readings = scan()
    rover_server.scan_status["scan_heading"] = heading
    turn_toward(heading)
    last_scan_time = time.monotonic()
```

### Try it / what you should see

Open your Pico's status webpage in a browser on the classroom WiFi — you should now see ten
fields: the seven from Classes 3-4 (`speed_left_cms`, `dir_left`, `speed_right_cms`, `dir_right`,
`roll`, `pitch`, `yaw`) plus today's three (`scan_heading`, `drive_state`, `stop_reason`). Set your
rover driving and watch `drive_state` flip between `"driving"` and `"scanning"` as it cycles, and
`stop_reason` name whichever safety signal (or `"ultrasonic"`, or `"none"` on a routine timer scan)
last forced a stop.

If the new fields never appear or never change, the most likely cause is that the old Class 4
`while True: server.poll()` loop is still in `rover_server.py` — two competing blocking loops will
make the website hang, not the rover, so check `class-5-code.py`'s console output first (it should
keep printing `drive:`/`scan:` lines normally even while the website is broken).

### Checkpoint

Open your Pico's status webpage and confirm all ten fields update live, with `drive_state`
flipping between `"driving"` and `"scanning"` as the rover cycles and `stop_reason` naming
whichever safety signal last fired. Confirm the Class 3-4 fields (`speed_left_cms`, `roll`, etc.)
are still updating too — they shouldn't have stopped just because you edited the same file.

## 6. Troubleshooting Guide

| Problem | Likely Cause | Fix |
| :-------- | :------------- | :---- |
| Rover doesn't drive at all | `motor_driver.py` missing from `CIRCUITPY`, or the 9V battery is dead | Confirm `motor_driver.py` is present alongside `code.py`; check battery voltage |
| Rover drives but never stops to scan | `SCAN_INTERVAL` too long, or `STOP_DISTANCE_CM` too small to ever trigger | Lower `SCAN_INTERVAL` and/or raise `STOP_DISTANCE_CM` and re-test |
| Rover stops constantly, barely drives | `STOP_DISTANCE_CM` set too large, triggering on normal sensor noise | Lower `STOP_DISTANCE_CM` in small steps |
| Rover always turns the same direction regardless of readings | Scan readings all coming back `None` (sensor errors), falling back to `CENTER_ANGLE` every time | Check the Class 2 sensor wiring; confirm `read_distance()` isn't always returning `None` |
| Rover turns the wrong way relative to the printed chosen heading | Motor sign convention doesn't match `degrees_off_center`'s left/right assumption | Swap the sign in `turn_toward()`'s `motor_driver.drive()` calls, or check against Class 3's wiring |
| Rover's turns overshoot or undershoot the intended heading | `TURN_SECONDS_PER_DEGREE` not recalibrated from your actual measured turn time | Recalculate from a fresh measured 90-degree turn, same method as Class 3 |
| Console floods with reading errors during a scan | Servo moved before the sensor settled, or the sensor is aimed at an out-of-range surface | Increase `SETTLE_TIME`; re-aim the test area to stay within the sensor's usable range |
| Rover works on the bench but behaves erratically on the floor | Wheels slipping on the test surface, or the floor interfering with the ultrasonic beam | Test on a harder, flatter surface — this is a real-world limitation to note, not just a bug |
| Bump switch never triggers even on a hard hit | Lever arm not mounted low/forward enough to actually contact obstacles, or `GP5` wiring loose | Reposition the switch so the lever leads the chassis edge; check wiring with a multimeter continuity test |
| Rover constantly emergency-stops with nothing nearby | IR sensor's onboard sensitivity trimmer set too high, or aimed at a reflective floor | Turn the sensor's sensitivity trimmer down; re-aim slightly upward off the floor |
| Rover backs into something behind it after a safety stop | Backoff time too long for the available clearance | Shorten the `time.sleep(0.3)` backoff in `safety_override_triggered()`'s reverse step |
| Website's new fields (`scan_heading`/`drive_state`/`stop_reason`) never appear or never change | Old Class 4 `rover_server.py` still on `CIRCUITPY`, or its old `while True: server.poll()` loop wasn't removed | Confirm only one `rover_server.py` exists and it's the Class 5 version; confirm `class-5-code.py` calls `rover_server.server.poll()` itself |
| Website hangs/never responds once the rover starts driving | Both `rover_server.py`'s old loop and `class-5-code.py`'s new loop are calling `server.poll()` in separate blocking loops | Delete the old `while True: server.poll()` block from `rover_server.py` entirely — only `class-5-code.py`'s main loop should call it now |
| Website's wheel-speed/orientation fields (Classes 3-4) stopped updating after today's edit | `GP16`/`GP17` or `GP0`/`GP1` wiring bumped while wiring today's limit switch/IR sensor | Re-verify those circuits weren't disturbed — they're unrelated to today's `GP5`/`GP13` wiring |
| `NameError` or `AttributeError` mentioning `scan_status` or `server` | `class-5-code.py` imports `rover_server` but references `scan_status`/`server` directly instead of `rover_server.scan_status`/`rover_server.server` | Prefix both with `rover_server.` everywhere they're read or updated in `class-5-code.py` |

## 7. Put It All Together

This is the finished project in one place. Unlike Class 3 and Class 4, this Class does **not**
need an Option A/B split — the whole point of today's `rover_server.py` refactor is that one
`code.py` now runs the collision-avoidance logic *and* keeps the website alive at the same time. It
reuses Class 2 and Class 3's circuits without changes, plus the limit switch and IR sensor added
this Class, plus the (now-library) `rover_server.py` this Class refactored.

### Complete wiring

| Component | Pico 2 W Pin |
| :---------- | :------------- |
| HC-SR04 `TRIG` | `GP6` |
| HC-SR04 `ECHO`, through voltage-divider resistors | `GP7` |
| SG90 servo signal | `GP8` |
| DRV8833 `AIN1`/`AIN2` (Motor A) | `GP9`/`GP10` |
| DRV8833 `BIN1`/`BIN2` (Motor B) | `GP11`/`GP12` |
| Limit switch (internal pull-up) | `GP5` |
| IR obstacle sensor `OUT` | `GP13` |
| Wheel-odometry optocouplers (website only, unchanged from Class 3) | `GP16`/`GP17` |
| LSM9DS1 IMU `SDA`/`SCL` (website only, unchanged from Class 4) | `GP0`/`GP1` |

### Complete code

You need **four files** on your `CIRCUITPY` drive: `motor_driver.py` and `wheel_odometry.py`
(unchanged from Class 3), `rover_server.py` (the library version below, edited this Class), and
`code.py` below.

`rover_server.py` — same file you've grown since Class 3, now refactored into a library:

```python
# rover_server.py -- refactored this Class into a library. Same WiFi/server
# setup, same /data.json route, same wheel_odometry + IMU reads as Classes
# 3-4 -- but it no longer owns a "while True: server.poll()" loop, and it
# adds scan_status for code.py to update with the collision-avoidance decision.
import os
import math
import time
import board
import busio
import wifi
import socketpool
import adafruit_lsm9ds1
from adafruit_httpserver import Server, Request, Response, JSONResponse
import wheel_odometry

wifi.radio.connect(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"))
print("rover server -- listening at", wifi.radio.ipv4_address)

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool)

i2c = busio.I2C(board.GP1, board.GP0)  # SCL, SDA -- same wiring as Class 4
imu = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

MAHONY_KP = 2.0   # calibrate: same tuned value as Class 4
MAHONY_KI = 0.05  # calibrate: same tuned value as Class 4

q0, q1, q2, q3 = 1.0, 0.0, 0.0, 0.0
integral_fbx = integral_fby = integral_fbz = 0.0
last_time = time.monotonic()

# New this Class: the collision-avoidance decision, updated each cycle by
# code.py and merged into /data.json alongside wheel speed and orientation.
scan_status = {
    "scan_heading": 90,        # degrees -- last chosen heading, starts centered
    "drive_state": "driving",  # "driving" | "scanning" | "stopped"
    "stop_reason": "none",     # "none" | "ultrasonic" | "ir" | "limit_switch"
}


def _mahony_update(ax, ay, az, gx, gy, gz, dt):
    # Identical math to Class 4's mahony_update() -- see Class 4's "Mahony
    # filter" explanation for why fusing accel+gyro this way works.
    global q0, q1, q2, q3, integral_fbx, integral_fby, integral_fbz
    norm = (ax * ax + ay * ay + az * az) ** 0.5
    if norm == 0:
        return
    ax, ay, az = ax / norm, ay / norm, az / norm
    vx = 2 * (q1 * q3 - q0 * q2)
    vy = 2 * (q0 * q1 + q2 * q3)
    vz = q0 * q0 - q1 * q1 - q2 * q2 + q3 * q3
    ex = ay * vz - az * vy
    ey = az * vx - ax * vz
    ez = ax * vy - ay * vx
    integral_fbx += MAHONY_KI * ex * dt
    integral_fby += MAHONY_KI * ey * dt
    integral_fbz += MAHONY_KI * ez * dt
    gx += MAHONY_KP * ex + integral_fbx
    gy += MAHONY_KP * ey + integral_fby
    gz += MAHONY_KP * ez + integral_fbz
    qa, qb, qc = q0, q1, q2
    q0 += (-qb * gx - qc * gy - q3 * gz) * 0.5 * dt
    q1 += (qa * gx + qc * gz - q3 * gy) * 0.5 * dt
    q2 += (qa * gy - qb * gz + q3 * gx) * 0.5 * dt
    q3 += (qa * gz + qb * gy - qc * gx) * 0.5 * dt
    norm = (q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3) ** 0.5
    q0, q1, q2, q3 = q0 / norm, q1 / norm, q2 / norm, q3 / norm


def _read_orientation():
    """Advance the Mahony filter one step and return (roll, pitch, yaw)."""
    global last_time
    now = time.monotonic()
    dt = now - last_time
    last_time = now
    ax, ay, az = imu.acceleration
    gx, gy, gz = (math.radians(v) for v in imu.gyro)
    _mahony_update(ax, ay, az, gx, gy, gz, dt)
    roll = math.degrees(math.atan2(2 * (q0 * q1 + q2 * q3), 1 - 2 * (q1 * q1 + q2 * q2)))
    pitch = math.degrees(math.asin(max(-1.0, min(1.0, 2 * (q0 * q2 - q3 * q1)))))
    yaw = math.degrees(math.atan2(2 * (q0 * q3 + q1 * q2), 1 - 2 * (q2 * q2 + q3 * q3)))
    return roll, pitch, yaw


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
    roll, pitch, yaw = _read_orientation()
    return JSONResponse(request, {
        "speed_left_cms": speed_left,
        "dir_left": dir_left,
        "speed_right_cms": speed_right,
        "dir_right": dir_right,
        "roll": roll,
        "pitch": pitch,
        "yaw": yaw,
        "scan_heading": scan_status["scan_heading"],
        "drive_state": scan_status["drive_state"],
        "stop_reason": scan_status["stop_reason"],
    })


@server.route("/")
def index(request: Request):
    return Response(request, STATUS_PAGE, content_type="text/html")


server.start(str(wifi.radio.ipv4_address))
# NOTE: no "while True: server.poll()" loop here anymore -- code.py's own
# main loop polls it now, once per cycle, so it can also keep driving.
```

`code.py` — Phase 1's collision-avoidance logic, plus Phase 2's `rover_server` import/polling:

```python
# code.py -- complete Random Rover collision-avoidance project, with the
# rover status website kept alive by this same loop.
import time
import board
import digitalio
import pwmio
import adafruit_hcsr04
from adafruit_motor import servo
import motor_driver
import rover_server  # now a library -- exposes server and scan_status

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP6, echo_pin=board.GP7)
pwm = pwmio.PWMOut(board.GP8, duty_cycle=0, frequency=50)
scan_servo = servo.Servo(pwm, min_pulse=500, max_pulse=2500)  # recalibrate per servo if needed

bump_switch = digitalio.DigitalInOut(board.GP5)
bump_switch.direction = digitalio.Direction.INPUT
bump_switch.pull = digitalio.Pull.UP

ir_sensor = digitalio.DigitalInOut(board.GP13)
ir_sensor.direction = digitalio.Direction.INPUT

DRIVE_SPEED = 0.4
SCAN_ANGLES = [30, 60, 90, 120, 150]
SETTLE_TIME = 0.15
STOP_DISTANCE_CM = 25
SCAN_INTERVAL = 3.0
TURN_SECONDS_PER_DEGREE = 0.4 / 90  # replace 0.4 with your own measured 90-degree turn time

CENTER_ANGLE = 90


def read_distance():
    try:
        return sonar.distance
    except RuntimeError:
        return None


def scan():
    readings = {}
    for angle in SCAN_ANGLES:
        scan_servo.angle = angle
        time.sleep(SETTLE_TIME)
        readings[angle] = read_distance()
        print("scan: angle", angle, "distance_cm", readings[angle])
    valid = {a: d for a, d in readings.items() if d is not None}
    best_angle = max(valid, key=valid.get) if valid else CENTER_ANGLE
    print("scan: chosen heading", best_angle)
    return best_angle, readings


def turn_toward(angle):
    degrees_off_center = angle - CENTER_ANGLE
    turn_time = abs(degrees_off_center) * TURN_SECONDS_PER_DEGREE
    if degrees_off_center == 0 or turn_time < 0.02:
        return
    if degrees_off_center > 0:
        motor_driver.drive(DRIVE_SPEED, -DRIVE_SPEED)
    else:
        motor_driver.drive(-DRIVE_SPEED, DRIVE_SPEED)
    time.sleep(turn_time)
    motor_driver.stop()


def safety_override_triggered():
    """Return a stop_reason string ("none" if neither fired) so the website
    can show which safety signal forced the most recent stop."""
    if not bump_switch.value:
        return "limit_switch"
    if not ir_sensor.value:
        return "ir"
    return "none"


print("Random Rover running.")
scan_servo.angle = CENTER_ANGLE
last_scan_time = time.monotonic()

while True:
    rover_server.server.poll()  # answer any pending website request, non-blocking
    rover_server.scan_status["drive_state"] = "driving"
    motor_driver.drive(DRIVE_SPEED, DRIVE_SPEED)

    stop_reason = "none"
    while True:
        rover_server.server.poll()
        stop_reason = safety_override_triggered()
        if stop_reason != "none":
            motor_driver.stop()
            motor_driver.drive(-DRIVE_SPEED, -DRIVE_SPEED)
            time.sleep(0.3)
            motor_driver.stop()
            break
        distance = read_distance()
        if distance is not None and distance < STOP_DISTANCE_CM:
            stop_reason = "ultrasonic"
            break
        if time.monotonic() - last_scan_time >= SCAN_INTERVAL:
            break
        time.sleep(0.05)

    rover_server.scan_status["stop_reason"] = stop_reason
    rover_server.scan_status["drive_state"] = "scanning"
    motor_driver.stop()
    heading, _readings = scan()
    rover_server.scan_status["scan_heading"] = heading
    turn_toward(heading)
    last_scan_time = time.monotonic()
```

## 8. What You Learned

You built the course's central milestone: a car that senses its surroundings and decides where to
go, entirely on its own. Specifically, you now know:

* How to combine two previously-separate circuits and code modules into one integrated program
* What "stop-look-go" means as a control pattern, and why it uses two independent triggers (a
    timer and a proximity threshold) to rescan, rather than relying on just one
* Why "steer toward the largest reading" is a reasonable default but can pick a bad direction —
    for example, a narrow-but-passable gap next to a wide-but-shallow dead end can look similar to
    a sweep that only compares single numbers, not shapes
* That "it didn't hit anything" isn't a very specific way to measure whether collision avoidance
    is actually working — you can do better with something like avoidances per run, distance
    maintained from obstacles, or consistency across repeated runs
* Why a safety-critical decision like "stop the car" is stronger when backed by multiple
    independent signals (ultrasonic, IR, physical bump) rather than trusting just one
* Why Classes 3 and 4 could only ever offer the rover status website as a separate Option A/B
    `code.py`, never running alongside that class's other program — and why this Class's need to
    keep driving *and* keep the website alive at the same time is exactly what finally forced
    `rover_server.py` to become a library instead of a script with its own loop
* That your rover status website now shows the rover's own collision-avoidance decisions live —
    `scan_heading`, `drive_state`, `stop_reason` — right alongside wheel speed/direction and
    orientation, so an observer across the room can watch the rover think in real time, not just
    watch it move

Next class isn't new concepts — it's finishing and tuning this exact rover, plus optional stretch
goals that bring back your Class 1 encoder and Class 4 IMU if you want to go further. Today's
`scan_heading`/`drive_state`/`stop_reason` website fields, and the library shape of
`rover_server.py`, carry forward into Class 6 unchanged.

----
## 9. Homework Assignment

No homework assignments have been written for this class yet. This section will be filled in with
optional take-home exercises, following the same format as the Pre-Class homework in
[`class-00-lesson-script.md`](class-00-lesson-script.md#10-homework-assignment) (what the code
does, full commented code, and real-world examples).

## References

* [IR Obstacle Avoidance Module][04] - documentation of the breakout board layout and operating principles
* [Raspberry Pi Pico W taught this car to avoid objects][01] — a real-world example of Pico-based obstacle avoidance, similar in spirit to this project
* [How to make an obstacle avoidance robot using Raspberry Pi Pico board][02] — a step-by-step obstacle-avoidance build guide, useful as a cross-reference
* [Obstacle Avoidance Robot Using Raspberry Pi Pico][03] — another worked example combining a distance sensor and motor driver for collision avoidance

---



[01]:https://www.raspberrypi.com/news/raspberry-pi-pico-w-taught-this-car-to-avoid-objects/
[02]:https://srituhobby.com/how-to-make-an-obstacle-avoidance-robot-using-raspberry-pi-pico-board/
[03]:https://circuitdiagrams.in/obstacle-avoidance-robot-using-raspberry-pi/
[04]:https://osoyoo.com/2018/12/21/ir-obstacle-avoidance-module/
