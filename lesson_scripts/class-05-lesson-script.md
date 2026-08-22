# Lesson Script: Class 5 — Build the Random Rover: Collision Avoidance


* **Class:** 5 of 6 (plus Pre-Class)
* **Duration:** ~2 hours
* **What You'll Need:** see [Section 2](#2-what-youll-need)
* **Before You Start:** Your Class 2 sensor+servo circuit (`GP6`-`GP8`) and Class 3 motor driver
    circuit (`GP9`-`GP12`) should both still be working exactly as you left them. You'll also need
    your Class 3 turn-time calibration notes (`SECONDS_PER_90_DEGREES` or similar) from your build
    journal. Class 1's button/encoder circuit and Class 4's IMU circuit aren't needed today — leave
    them in place or set them aside.

---


## 1. What This Project Is

This is the class where everything you've built so far becomes one robot that makes its own
decisions. You're combining your Class 2 sensor-on-servo sweep with your Class 3 motor driver into
a single program: the car drives forward at a constant speed, periodically stops to sweep the
sensor and look for the clearest direction, and steers that way — with an emergency path that
stops and rescans immediately if something gets too close while driving, instead of waiting for
the next scheduled look.

Most of what you need is already on your breadboard from Class 2 and Class 3 — Today is mostly
about writing the decision-making that connects your car's eyes to its legs. The one new thing
today: a limit switch and an IR obstacle sensor, two fixed safety inputs that give your car a
last-resort "stop no matter what" reflex, backing up the ultrasonic sweep. By the end, your car
should be able to drive around the room on its own and steer around at least one obstacle without
you touching it — the central milestone of the whole course.

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
| Open floor area with soft obstacles | shared | Test space for autonomous driving runs |

**Additional components for the Homework Assignments** (Section 8) — no homework has been written
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

**Pinout summary** (Class 2 and Class 3 pins reconnect exactly as wired; `GP5`/`GP13` are new):

| Pin | What it does | From Class |
| :---- | :--------------- | :----------- |
| `GP6` | HC-SR04 `TRIG` | Class 2 |
| `GP7` | HC-SR04 `ECHO`, through voltage-divider | Class 2 |
| `GP8` | SG90 servo signal | Class 2 |
| `GP9`/`GP10` | DRV8833 `AIN1`/`AIN2` (Motor A) | Class 3 |
| `GP11`/`GP12` | DRV8833 `BIN1`/`BIN2` (Motor B) | Class 3 |
| `GP5` | Limit switch (internal pull-up) | New this Class |
| `GP13` | IR obstacle sensor `OUT` | New this Class |

## 4. Build It: The Collision-Avoidance Program

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

## 5. Troubleshooting Guide

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

## 6. Put It All Together

This is the finished project in one place. It reuses Class 2 and Class 3's circuits without
changes, plus the limit switch and IR sensor added this Class — the only thing new is this single
program.

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

### Complete code

You need **two files** on your `CIRCUITPY` drive: `motor_driver.py` (unchanged from Class 3) and
`code.py` below.

```python
# code.py -- complete Random Rover collision-avoidance project.
import time
import board
import digitalio
import pwmio
import adafruit_hcsr04
from adafruit_motor import servo
import motor_driver

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
    if not bump_switch.value or not ir_sensor.value:
        return True
    return False


print("Random Rover running.")
scan_servo.angle = CENTER_ANGLE
last_scan_time = time.monotonic()

while True:
    motor_driver.drive(DRIVE_SPEED, DRIVE_SPEED)
    while True:
        if safety_override_triggered():
            motor_driver.stop()
            motor_driver.drive(-DRIVE_SPEED, -DRIVE_SPEED)
            time.sleep(0.3)
            motor_driver.stop()
            break
        distance = read_distance()
        if distance is not None and distance < STOP_DISTANCE_CM:
            break
        if time.monotonic() - last_scan_time >= SCAN_INTERVAL:
            break
        time.sleep(0.05)
    motor_driver.stop()
    heading, _readings = scan()
    turn_toward(heading)
    last_scan_time = time.monotonic()
```

## 7. What You Learned

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

Next class isn't new concepts — it's finishing and tuning this exact rover, plus optional stretch
goals that bring back your Class 1 encoder and Class 4 IMU if you want to go further.

## 8. Homework Assignment

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
