# Lesson Script: Class 2 — Ultrasonic Distance Sensor + Servo Motor


* **Class:** 2 of 6 (plus Pre-Class)
* **Duration:** ~2 hours
* **What You'll Need:** see [Section 2](#2-what-youll-need)
* **Before You Start:** Your Class 1 circuit (pushbutton on `GP2`, rotary encoder on `GP3`/`GP4`,
    two LEDs on `GP14`/`GP15`) should still be working and stay exactly as it is on your
    breadboard — you won't touch it today, just build next to it.

---


## 1. What This Project Is

Today you're giving your board two new senses: one that measures distance by "listening" for an
echo, and one that can point itself at a precise angle. Wired together — sensor riding on top of
the motor — they let your board scan a room the way you'd sweep a flashlight left and right,
reading how far away things are at every angle.

You'll build this in three steps: get the distance sensor working alone, get the servo motor
sweeping alone, then physically tape the sensor onto the servo and combine them into one
scan-and-report circuit. That combined circuit is not a simplified preview of something later — it
is, unchanged, the exact "look around for open space" behavior your Random Rover uses to avoid
obstacles starting in Class 5.

## 2. What You'll Need

| Component | Quantity | Purpose This Project |
| :---------- | :--------: | :---------------------- |
| Raspberry Pi Pico 2 W (with header) | 1 | Runs your CircuitPython code |
| HC-SR04 ultrasonic distance sensor | 1 | Measures distance via a timed sound echo |
| SG90 micro servo motor | 1 | Sweeps the sensor across an angle range via PWM |
| Voltage-divider resistor pair (e.g. 1k/2k ohm) | 1 pair | Steps the sensor's 5V `ECHO` signal down to a safe 3.3V |
| Double-sided tape or small mount | 1 | Fastens the sensor to the servo shaft/horn |
| Breadboard (from Class 1) | 1 | Your Class 1 circuit stays on it, untouched |
| Dupont jumper wires | ~8 | Point-to-point connections |
| USB cable | 1 | Powers the Pico and carries the serial console |
| Laptop with Mu or Thonny | 1 | Where you write/save code and read the serial console |

**Additional components for the Homework Assignments** (Section 10) — no homework has been written
for this class yet; this section will be filled in when that content is added.

## 3. Meet the Hardware

**HC-SR04 ultrasonic distance sensor.** This sensor has four pins: `VCC`, `GND`, `TRIG`, and
`ECHO`. You send it a short pulse on `TRIG`, and it fires an ultrasonic "chirp" — a sound above
human hearing — out of one of its two round eyes. Its other eye listens for that chirp to bounce
off whatever's in front of it and come back, and it holds `ECHO` high for exactly as long as that
round trip took. Because sound travels at a known, constant speed, that timing converts directly
to a distance. This is the same principle bats and dolphins use to navigate in the dark. In
CircuitPython, the `adafruit_hcsr04` library handles the timing and the math for you — you just
ask it for `.distance` and get back centimeters.

**SG90 micro servo motor.** Unlike a normal motor that just spins, a servo holds a specific shaft
angle and stays there. It reads that target angle from the *width* of a repeating electrical
pulse on its signal wire — a pulse near 1.5 milliseconds means "center, 90 degrees," shorter
pulses sweep it toward 0 degrees, longer pulses sweep it toward 180 degrees. This encoding scheme
is called **PWM** (pulse-width modulation) — you already used a form of PWM in Class 1 to control
LED brightness; here the same underlying technique encodes a position instead. The
`adafruit_motor.servo` library turns this into a simple `.angle = 90` style interface so you never
have to compute pulse widths by hand.

**Why the voltage divider matters.** The HC-SR04 is a 5V device — its `ECHO` pin can output up to
5 volts. The Pico 2 W's GPIO pins are only rated for 3.3 volts, and feeding 5V directly into one
risks damaging it permanently. A **voltage divider** — two resistors in series, tapped at the
midpoint — steps that 5V signal down to a safe ~3.3V before it reaches the Pico. This only matters
for `ECHO` (a signal coming *from* the sensor *into* the Pico); the servo's signal pin doesn't
need this protection because the Pico is the one driving that line, not the other way around.

**Pinout summary** (Raspberry Pi Pico 2 W — new pins only; Class 1's circuit is unaffected):

| Pin | What we use it for |
| :---- | :-------------------- |
| `GP6` | HC-SR04 `TRIG` |
| `GP7` | HC-SR04 `ECHO`, through the voltage-divider resistors |
| `GP8` | SG90 servo signal |
| `5V` (VBUS) | HC-SR04 `VCC` and SG90 servo power |
| `GND` | HC-SR04 `GND` and SG90 `GND` |

## 4. Build It: Phase 1 — Read the Distance Sensor Alone

### Wiring for this phase

| Component | Pico 2 W Pin |
| :---------- | :------------- |
| HC-SR04 `TRIG` | `GP6` |
| HC-SR04 `ECHO`, through voltage-divider resistors | `GP7` |
| HC-SR04 `VCC` | `5V` (VBUS) |
| HC-SR04 `GND` | `GND` |

Your Class 1 circuit stays exactly where it is on the breadboard — leave it alone. Before writing
any code, trace this new wiring out loud, and double-check the voltage-divider resistors sit on
the `ECHO` line, not `TRIG` — this is the single easiest wiring mistake to make this class, and
the least forgiving one, since it protects the Pico's GPIO pin.

### What this code does

This program pulses `TRIG`, waits for the sensor to time the echo, and prints the resulting
distance in centimeters, over and over, forever.

### The code

Save this as `code.py` on your `CIRCUITPY` drive.

```python
# class-2-code-1.py
# Phase 1: HC-SR04 alone -- prints live distance readings.

import time
import board
import adafruit_hcsr04

# HCSR04() wraps the trigger/echo timing and speed-of-sound math for you.
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP6, echo_pin=board.GP7)

print("Class 2, Phase 1 -- HC-SR04 distance readings starting...")

while True:
    try:
        # .distance triggers a chirp, times the echo, and returns centimeters.
        print("distance_cm:", sonar.distance)
    except RuntimeError:
        # An occasional missed/garbled echo is normal -- this just retries
        # on the next loop instead of crashing the program.
        print("distance_cm: reading error, retrying")
    time.sleep(0.2)
```

### Try it / what you should see

You should see `distance_cm:` print roughly five times a second. Move your hand toward and away
from the sensor and watch the number change sensibly — smaller as your hand gets closer, larger
as it moves away. An occasional `reading error, retrying` line is normal; that's a single missed
echo, not a bug. If *every* line is an error, that's a wiring problem, not a fluke.

### Checkpoint

Confirm you can watch `distance_cm` change in a way that matches where you actually move your
hand, roughly between 2cm and 4m from the sensor (its usable range — much closer or farther than
that and readings become unreliable).

## 5. Build It: Phase 2 — Sweep the Servo Alone

### Wiring for this phase

| Component | Pico 2 W Pin |
| :---------- | :------------- |
| SG90 servo signal | `GP8` |
| SG90 servo `+`/power | `5V` (VBUS) |
| SG90 `GND` | `GND` |

Add this alongside Phase 1's sensor wiring — you're not removing anything, just adding the servo.

### What this code does

This program sweeps the servo shaft continuously from 0 to 180 degrees and back, in 5-degree
steps, printing the current angle at each step.

### The code

Save this as `code.py`, replacing Phase 1's version for now (you'll combine both in Phase 3).

```python
# class-2-code-2.py
# Phase 2: SG90 alone -- continuous sweep, no sensor yet.

import time
import board
import pwmio
from adafruit_motor import servo

# A servo needs a 50Hz PWM signal -- that's a fixed requirement of the part.
pwm = pwmio.PWMOut(board.GP8, duty_cycle=0, frequency=50)
# min_pulse/max_pulse define the pulse widths (in microseconds) that
# correspond to 0 and 180 degrees. Cheap SG90 units vary -- if yours
# twitches or won't reach a true 0/180, adjust these in small steps.
my_servo = servo.Servo(pwm, min_pulse=500, max_pulse=2500)

print("Class 2, Phase 2 -- SG90 sweep starting...")

while True:
    # Sweep up from 0 to 180 degrees.
    for angle in range(0, 181, 5):
        my_servo.angle = angle
        print("servo_angle:", angle)
        time.sleep(0.02)
    # Sweep back down from 180 to 0 degrees.
    for angle in range(180, -1, -5):
        my_servo.angle = angle
        print("servo_angle:", angle)
        time.sleep(0.02)
```

### Try it / what you should see

The servo shaft should sweep smoothly from one side to the other and back, continuously, with
`servo_angle:` counting up and down in the console to match. If it twitches or buzzes at the
extremes without actually reaching them, your `min_pulse`/`max_pulse` values need calibrating for
your specific servo — try nudging them in small steps (`500` -> `600`, `2500` -> `2400`) and
re-test.

### Checkpoint

The servo should sweep end to end with no grinding or stalling sound at either extreme, and the
printed `servo_angle` should track what you visually see the shaft doing.

## 6. Build It: Phase 3 — Combine Them: Sweep and Report

### Wiring for this phase

No new wiring — this phase uses the exact same pins as Phase 1 and Phase 2 combined (`GP6`/`GP7`
for the sensor, `GP8` for the servo). What changes is physical: mount the HC-SR04 onto the servo
horn/shaft with double-sided tape, leaving the sensor's wires with enough slack to follow the
sweep without snagging or pulling loose.

### What this code does

This program sweeps the servo just like Phase 2, but pauses briefly at each stop and reads the
distance sensor before moving on — printing an `angle`/`distance_cm` pair at every step. That
short pause matters: without it, you might read the sensor while the servo is still mid-swing, so
the distance wouldn't actually match the angle you think you're pointed at.

### The code

Save this as `code.py`, replacing Phase 2's version.

```python
# class-2-code-3.py
# Phase 3: HC-SR04 mounted on SG90 -- sweeps and prints angle + distance pairs.

import time
import board
import pwmio
import adafruit_hcsr04
from adafruit_motor import servo

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP6, echo_pin=board.GP7)
pwm = pwmio.PWMOut(board.GP8, duty_cycle=0, frequency=50)
my_servo = servo.Servo(pwm, min_pulse=500, max_pulse=2500)  # recalibrate per servo if needed

# How long to wait after each move before trusting the sensor reading --
# without this, we might read mid-swing and get a distance that doesn't
# actually correspond to the angle we just printed.
SETTLE_TIME = 0.15  # seconds

print("Class 2, Phase 3 -- angle/distance sweep starting...")

while True:
    # Sweep up, reading distance at every 10-degree stop.
    for angle in range(0, 181, 10):
        my_servo.angle = angle
        time.sleep(SETTLE_TIME)
        try:
            print("angle:", angle, "distance_cm:", sonar.distance)
        except RuntimeError:
            print("angle:", angle, "distance_cm: reading error")
    # Sweep back down, same pattern.
    for angle in range(180, -1, -10):
        my_servo.angle = angle
        time.sleep(SETTLE_TIME)
        try:
            print("angle:", angle, "distance_cm:", sonar.distance)
        except RuntimeError:
            print("angle:", angle, "distance_cm: reading error")
```

### Try it / what you should see

Place an object — a water bottle, your hand, a notebook — somewhere in front of your setup. You
should see the console print a steady stream of `angle: X distance_cm: Y` lines as the sensor
visibly sweeps back and forth, and you should be able to spot the object as a noticeable *dip* in
`distance_cm` at the specific angle it's sitting at.

### Checkpoint

Run the combined sweep and confirm the console prints a clean `angle:`/`distance_cm:` line at
every stop, with the sensor visibly tracking a hand or object you move in front of it as a
distance dip at the matching angle.

## 7. Troubleshooting Guide

| Problem | Likely Cause | Fix |
| :-------- | :------------- | :---- |
| `distance_cm` never prints, only errors | `TRIG`/`ECHO` swapped, or the voltage divider is missing from `ECHO` | Confirm `TRIG` on `GP6`, `ECHO` on `GP7` through the divider resistors |
| `distance_cm` reads a fixed, unchanging number | Sensor aimed at something too close or too far outside its usable range | Re-aim the sensor at an object roughly 2cm-4m away |
| Servo doesn't move at all | Servo power wired to `3V3` instead of `5V`/VBUS, or the signal wire is on the wrong pin | Confirm signal on `GP8`, power on `5V`, ground on `GND` |
| Servo twitches or buzzes but never reaches 0/180 | `min_pulse`/`max_pulse` not calibrated for this specific servo | Adjust both values in small steps and retest |
| Servo resets or the board browns out when it moves | Servo is drawing power from a weak/shared source instead of `5V`/VBUS | Confirm servo power comes from `5V`/VBUS with a solid connection, not a thin shared jumper |
| Combined sweep's distance looks "stale" or mismatched to the angle | `SETTLE_TIME` too short — reading taken mid-move | Increase `SETTLE_TIME` in small steps (`0.15` -> `0.2` -> `0.3`) |
| `ImportError: no module named 'adafruit_hcsr04'` (or `adafruit_motor`) | Library file missing from `/lib` on your `CIRCUITPY` drive | Copy the missing `.mpy` file(s) from the Library Bundle into `/lib` |
| Sensor wobbles or falls off the servo horn mid-sweep | Tape not fully adhered, or wires pulling on the sensor | Press the tape firmly onto a clean, dry surface; add slack to the sensor's wires |

## 8. Put It All Together

This is the finished project in one place — build straight to the combined sensor+servo sweep
without going through the individual phases above.

### Complete wiring

| Component | Pico 2 W Pin |
| :---------- | :------------- |
| HC-SR04 `TRIG` | `GP6` |
| HC-SR04 `ECHO`, through voltage-divider resistors | `GP7` |
| SG90 servo signal | `GP8` |
| HC-SR04 `VCC` | `5V` (VBUS) |
| SG90 servo `+`/power | `5V` (VBUS) |
| HC-SR04 `GND`, SG90 `GND` | `GND` |

(Class 1's button/encoder circuit stays untouched on the breadboard alongside this.)

### Complete code

Save as `code.py`. Mount the HC-SR04 onto the servo horn/shaft with double-sided tape before
running this.

```python
# class-2-code-3.py -- complete sweep-and-report project: HC-SR04 mounted on SG90.
import time
import board
import pwmio
import adafruit_hcsr04
from adafruit_motor import servo

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP6, echo_pin=board.GP7)
pwm = pwmio.PWMOut(board.GP8, duty_cycle=0, frequency=50)
my_servo = servo.Servo(pwm, min_pulse=500, max_pulse=2500)  # recalibrate per servo if needed

SETTLE_TIME = 0.15  # seconds; let the servo stop moving before trusting the reading

print("Class 2 project running -- sensor-on-servo sweep.")

while True:
    for angle in range(0, 181, 10):
        my_servo.angle = angle
        time.sleep(SETTLE_TIME)
        try:
            print("angle:", angle, "distance_cm:", sonar.distance)
        except RuntimeError:
            print("angle:", angle, "distance_cm: reading error")
    for angle in range(180, -1, -10):
        my_servo.angle = angle
        time.sleep(SETTLE_TIME)
        try:
            print("angle:", angle, "distance_cm:", sonar.distance)
        except RuntimeError:
            print("angle:", angle, "distance_cm: reading error")
```

## 9. What You Learned

You gave your board two new ways to sense the physical world and combined them into a single
scanning behavior. Specifically, you now know:

* How the HC-SR04 measures distance by timing a sound echo, and why that requires a voltage
    divider to protect the Pico's 3.3V logic from its 5V `ECHO` signal
* How the SG90 servo reads a target angle from a PWM pulse width, and how to calibrate
    `min_pulse`/`max_pulse` for a specific unit
* Why a short settle time after moving the servo matters before trusting a sensor reading taken
    at that position
* How two very different devices — one encoding information as a timed echo, one as a pulse
    width — can both talk to the same microcontroller through the same breadboard

This exact circuit — sensor riding on the servo, sweeping and reporting — is not a simplified
stand-in for something later; it's the unchanged "look around" behavior your Random Rover uses
starting in Class 5. Next class, you add the piece that's still missing: a motor driver that can
actually act on what the sensor sees.

----
## 10. Homework Assignment

No homework assignments have been written for this class yet. This section will be filled in with
optional take-home exercises, following the same format as the Pre-Class homework in
[`class-00-lesson-script.md`](class-00-lesson-script.md#10-homework-assignment) (what the code
does, full commented code, and real-world examples).

## References

* [Python & CircuitPython — Ultrasonic Sonar Distance Sensors][01] — Adafruit's official guide to
    wiring and reading the HC-SR04, including the voltage-divider caveat
* [adafruit/Adafruit_CircuitPython_HCSR04][02] — the `adafruit_hcsr04` library used in this script
* [CircuitPython Servo | CircuitPython Essentials][03] — PWM and `adafruit_motor.servo` basics
* [DC, Servo, Stepper Motors and Solenoids with the Pico][04] — broader background on motor/servo
    control from the Pico

---

[01]:https://learn.adafruit.com/ultrasonic-sonar-distance-sensors/python-circuitpython
[02]:https://github.com/adafruit/Adafruit_CircuitPython_HCSR04
[03]:https://learn.adafruit.com/circuitpython-essentials/circuitpython-servo
[04]:https://learn.adafruit.com/use-dc-stepper-servo-motor-solenoid-rp2040-pico
