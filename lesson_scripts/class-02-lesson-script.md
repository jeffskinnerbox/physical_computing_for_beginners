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

Outside of class, Homework 1 (Section 11) has you start assembling the Random Rover chassis kit at
home — the mechanical platform tonight's sensor+servo rig, and everything after it, will eventually
ride on. It stays unwired until Class 5, so there's nothing to bring together with tonight's
breadboard build yet.

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

**Additional components for the Homework Assignments** (Section 11) — not needed for tonight's
class itself, only if you choose to do Homework 1, Homework 4, or Homework 5 at home:

| Component | Quantity | Purpose (Homework #) |
| :---------- | :--------: | :---------------------- |
| EMOZNY Smart Car Chassis Kit | 1 | Random Rover chassis assembly, unwired for now (Homework 1) — wired up starting in Class 5 |
| 1.14" 240x135 Color TFT Display (ST7789) | 1 | Live angle/distance readout (Homework 4) — also used in the Pre-Class and Class 1 homework and Class 6's stretch goal |
| IR Obstacle Avoidance Sensor | 1 | Fixed, forward-facing cross-check against the sweeping HC-SR04 (Homework 5) — also used on the Random Rover in Class 5 |

Homework 2, Homework 3, Homework 6, Homework 7, and Homework 8 need no additional hardware beyond
tonight's sensor+servo circuit (Homework 7 and Homework 8 also reuse the WiFi access-point pattern
from the Pre-Class homework, so no new hardware there either).

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
* [Raspberry Pi Pico 2w Pinout][20]
* [HC-SR04 Pinout][37]

| Component | Pico 2 W Pin |
| :---------- | :------------- |
| HC-SR04 `TRIG` | `GP6` |
| HC-SR04 `ECHO`, through voltage-divider resistors | `GP7` |
| HC-SR04 `VCC` | `5V` (VBUS) |
| HC-SR04 `GND` | `GND` |

Your Class 1 circuit stays exactly where it is on the breadboard — leave it alone.
Before writing any code, trace this new wiring out loud.

>**NOTE:** Double-check the voltage-divider resistors sit on the `ECHO` line, not `TRIG` — this is
>the single easiest wiring mistake to make this class, and the least forgiving one, since it
>protects the Pico's GPIO pin.

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
* [Raspberry Pi Pico 2w Pinout][20]
* [SG90 Servo Pinout][38]

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
`servo_angle:` counting up and down in the console to match.

>**NOTE:** If the servo twitches or buzzes at the extremes without actually reaching them, your
>`min_pulse`/`max_pulse` values need calibrating for your specific servo — try nudging them in
>small steps (`500` -> `600`, `2500` -> `2400`) and re-test.

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

## 7. Try It Yourself

Once Phase 3 is passing its checkpoint, make a few small, deliberate changes and watch what
happens each time — this "change one thing, test it, see the result" habit is the same one you
used in the Pre-Class and Class 1, and will keep using for the rest of the course:

* Lower `SETTLE_TIME` toward `0.02` in the Phase 3 code and rerun the sweep — watch `distance_cm`
    start looking "stale" or mismatched to the angle you see printed, the same problem the
    Troubleshooting table below calls out. Raise it back to `0.15` and confirm the readings line
    up again.
* Change the sweep's step size from `10` degrees to `30` in both `range()` calls — the sweep gets
    faster but coarser, and it's easier to miss a narrow object between stops.
* Temporarily swap the `trigger_pin` and `echo_pin` arguments in `adafruit_hcsr04.HCSR04(...)` and
    watch the console fill with `reading error` on every line — this is the exact wiring mistake
    Section 4 warned you about, deliberately reproduced in code instead of on the breadboard, so
    you recognize the symptom either way. Swap them back afterward.
* Nudge `min_pulse`/`max_pulse` in the `servo.Servo(...)` line by a large, obviously-wrong amount
    (e.g. `min_pulse=200`) and watch the servo twitch or stall at the extremes instead of sweeping
    smoothly — then restore the original values.

## 8. Troubleshooting Guide

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

## 9. Build It: Put It All Together

This is the finished project in one place — build straight to the combined sensor+servo sweep
without going through the individual phases above.

### Complete wiring
* [Raspberry Pi Pico 2w Pinout][20]
* [SG90 Servo Pinout][38]
* [HC-SR04 Pinout][37]

| Component | Pico 2 W Pin |
| :---------- | :------------- |
| HC-SR04 `TRIG` | `GP6` |
| HC-SR04 `ECHO`, through voltage-divider resistors | `GP7` |
| HC-SR04 `VCC` | `5V` (VBUS) |
| HC-SR04 `GND`, SG90 `GND` | `GND` |
| SG90 servo signal | `GP8` |
| SG90 servo `+`/power | `5V` (VBUS) |

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

## 10. What You Learned

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
actually act on what the sensor sees. If you build the chassis for Homework 1, that's the third and
final piece — sensor, motor driver, and now a rolling platform to carry them — all coming together
starting in Class 5.

---

## 11. Homework Assignment

Tonight's circuit and code stay on your breadboard — the exercises below are **homework, not
required class content**, and each one builds directly on the HC-SR04 + SG90 sensor-on-servo
circuit you just finished tonight. Do them in any order. For each one you'll find: what the code
teaches and why it's useful, the full commented code to save as `code.py` on your `CIRCUITPY`
drive, what to expect when you test it, and a couple of real-world examples of where this exact
technique shows up outside a classroom. Only Homework 4 and Homework 5 need a part beyond tonight's
circuit — see [Section 2](#2-what-youll-need).

### Homework 1 — Random Rover: Assemble the Chassis of Our Autonomous Robot

**What this teaches:** This is the one homework in the course that's mechanical, not code — you're
assembling the physical chassis the Random Rover will eventually drive around on, following the
same "read the instructions, adapt as you go" habit called out in the Pre-Class as how real makers
build things. Getting the chassis built now, ahead of Class 5, means class time later goes to
wiring and code instead of screws and standoffs.

Assemble the EMOZNY Smart Car Chassis Kit by following the included instruction sheet (there are
helpful videos below).
**BUT** also do the following:
* **do not** attach any wiring (we will do this together in class)
* **do not** attach the battery holder (we will be using a 9 volt battery instead)

Assembly Videos:
* [How to assemble the 2WD Smart Robot Car Chassis Kit for Arduino][35]
* [Complete Assembly And Review Of A DIY Robot Smart Car Chassis Kit For Arduino or Raspberry Pi][36]

#### What You Observe
**Test it:** When you're done, confirm the chassis rolls freely on a flat surface when pushed by
hand (both wheels turn, nothing binds or drags), and that no wiring or battery holder is attached
yet — those get added together in Class 5, once the motor driver and sensors are ready to go on.

#### Real World Examples

* Commercial robot kits (vacuum robots, hobby rovers, competition robotics kits like FIRST or
    VEX) are almost always sold as a bare mechanical chassis first, with electronics added in a
    separate step — exactly the order this course follows.
* Real engineering teams build and test a mechanical platform before finalizing the electronics
    that will ride on it, since a chassis problem (binding wheels, a warped frame) is far easier to
    fix before it's carrying a battery and a live motor driver.

### Homework 2 — Manual Aim: Drive the Servo With the Rotary Encoder

**What this teaches:** Tonight's Phase 2/3 code always drives the servo through a fixed,
automatic sweep. This exercise reuses the KY-040 rotary encoder from Class 1 — already sitting on
your breadboard, unchanged — to set the servo's target angle directly and live: turn the knob
clockwise and the sensor-on-servo rig turns with it, printing the distance at wherever you're
currently pointed. This is a genuinely new combination: Class 1 used the encoder to increment a
counter, tonight's class drove the servo from a fixed loop, and this is the first time one live
input directly commands the other device's position.

### Complete wiring
* [Raspberry Pi Pico 2w Pinout][20]
* [SG90 Servo Pinout][38]
* [HC-SR04 Pinout][37]

No new wiring — this reuses the encoder (`GP3`/`GP4`, from Class 1) and tonight's sensor+servo
circuit (`GP6`/`GP7`/`GP8`) exactly as they already sit on your breadboard.

### Complete code

```python
# code.py - Homework 2: drive the servo directly from the rotary encoder --
# turn the knob, the sensor-on-servo rig points wherever you turn it, and
# distance at that angle prints live. Unlike tonight's auto-sweep, position
# is now a live command from the encoder, not a fixed loop.
import time
import board
import pwmio
import digitalio
import adafruit_hcsr04
from adafruit_motor import servo

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP6, echo_pin=board.GP7)
pwm = pwmio.PWMOut(board.GP8, duty_cycle=0, frequency=50)
my_servo = servo.Servo(pwm, min_pulse=500, max_pulse=2500)  # recalibrate per servo if needed

encoder_clk = digitalio.DigitalInOut(board.GP3)
encoder_clk.direction = digitalio.Direction.INPUT
encoder_clk.pull = digitalio.Pull.UP

encoder_dt = digitalio.DigitalInOut(board.GP4)
encoder_dt.direction = digitalio.Direction.INPUT
encoder_dt.pull = digitalio.Pull.UP

angle = 90  # start centered, the servo's natural rest position
my_servo.angle = angle
last_clk_state = encoder_clk.value

print("Class 2 Homework 2 -- turn the knob to aim the sensor. Distance prints live.")

while True:
    clk_state = encoder_clk.value
    if clk_state != last_clk_state:
        if encoder_dt.value != clk_state:
            angle += 5
        else:
            angle -= 5
        angle = max(0, min(180, angle))
        my_servo.angle = angle
        # Same reasoning as tonight's SETTLE_TIME -- let the servo actually
        # arrive before trusting the reading.
        time.sleep(0.15)
        try:
            print("angle:", angle, "distance_cm:", sonar.distance)
        except RuntimeError:
            print("angle:", angle, "distance_cm: reading error")
    last_clk_state = clk_state

    time.sleep(0.001)
```

#### What You Observe
**Test it:** Turn the knob slowly, one detent at a time. The sensor-on-servo rig should visibly
turn to match, in 5-degree steps, and `angle:`/`distance_cm:` should print once per detent — not a
continuous stream like tonight's auto-sweep. Point it at an object and confirm `distance_cm` tracks
what you're actually pointed at.

#### Real World Examples

* A manually-steered security camera or telescope mount works exactly this way — a human-turned
    dial commands the motor's position directly, rather than the camera sweeping on its own.
* Robotic camera gimbals used in film production are often "dialed in" by an operator the same way
    before switching over to an automated tracking mode.

### Homework 3 — One-Shot Scan on Button Press, With a Blink-Rate Report

**What this teaches:** Tonight's sweep runs forever in a `while True` loop. This exercise instead
waits for the Class 1 pushbutton, runs exactly *one* sweep when pressed, finds the single closest
object seen during that sweep, and then blinks an LED at a rate that reports how close it was —
fast blink means "something's close," slow blink means "mostly clear." This is your first
event-triggered (rather than continuous) sensor behavior, and your first time mapping a sensor
reading onto an output *rate* instead of a fixed on/off or brightness value.

### Complete wiring
* [Raspberry Pi Pico 2w Pinout][20]
* [SG90 Servo Pinout][38]
* [HC-SR04 Pinout][37]
No new wiring — this reuses the pushbutton and its LED (`GP2`/`GP15`, from Class 1) and tonight's
sensor+servo circuit.

### Complete code

```python
# code.py - Homework 3: ONE sweep per button press (not a forever loop),
# then blink an LED at a rate that reports how close the nearest object
# was -- fast blink means close, slow blink means clear.
import time
import board
import pwmio
import digitalio
import adafruit_hcsr04
from adafruit_motor import servo
from adafruit_debouncer import Debouncer

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP6, echo_pin=board.GP7)
pwm = pwmio.PWMOut(board.GP8, duty_cycle=0, frequency=50)
my_servo = servo.Servo(pwm, min_pulse=500, max_pulse=2500)

button_pin = digitalio.DigitalInOut(board.GP2)
button_pin.direction = digitalio.Direction.INPUT
button_pin.pull = digitalio.Pull.UP
button = Debouncer(button_pin)

report_led = digitalio.DigitalInOut(board.GP15)
report_led.direction = digitalio.Direction.OUTPUT

SETTLE_TIME = 0.15

def run_one_sweep():
    # Sweeps once, 0 to 180, and returns the closest distance seen and the
    # angle it was seen at -- a single "scan," not a forever loop.
    closest_distance = None
    closest_angle = None
    for angle in range(0, 181, 10):
        my_servo.angle = angle
        time.sleep(SETTLE_TIME)
        try:
            distance = sonar.distance
        except RuntimeError:
            continue
        if closest_distance is None or distance < closest_distance:
            closest_distance = distance
            closest_angle = angle
    return closest_distance, closest_angle

def blink_period_for(distance_cm):
    # Closer objects blink faster. Clamp so the rate stays sane even for
    # very close, very far, or missing readings.
    if distance_cm is None:
        return 1.0  # slow "nothing found" blink
    distance_cm = max(5, min(200, distance_cm))
    return distance_cm / 200 * 0.9 + 0.1  # 0.1s (close) to 1.0s (far)

print("Class 2 Homework 3 -- press the button to run one scan.")

while True:
    button.update()
    if button.fell:
        print("-- scanning --")
        closest_distance, closest_angle = run_one_sweep()
        if closest_distance is None:
            print("no object found")
        else:
            print("closest_cm:", closest_distance, "at angle:", closest_angle)

        blink_period = blink_period_for(closest_distance)
        print("reporting for 5 seconds, blink period:", round(blink_period, 2), "s")
        report_until = time.monotonic() + 5
        while time.monotonic() < report_until:
            report_led.value = not report_led.value
            time.sleep(blink_period / 2)
        report_led.value = False

    time.sleep(0.01)
```

#### What You Observe
**Test it:** Place an object somewhere in front of the sensor, then press the button. The rig
should sweep once (not forever), print the closest distance and angle it found, then blink
`report_led` for about 5 seconds at a rate that matches how close that object was. Move the object
closer and press again — the blink should speed up.

#### Real World Examples

* Parking-assist sensors in cars beep faster and faster as your bumper gets closer to an obstacle
    — the same "closer means faster" mapping, just sound instead of light.
* Geiger counters click faster the more radiation they detect — a rate-encoded reading is often
    easier to react to instantly than a number you'd have to read and interpret.

### Homework 4 — Live Radar Readout on the TFT

**What this teaches:** *(Requires the [TFT display][19] used in the Pre-Class and Class 1 homework
— see [Section 2](#2-what-youll-need).)* Tonight's angle/distance sweep only ever printed to the
serial console. This exercise draws the exact same sweep live on the ST7789 TFT instead — the first
time in the course the TFT shows sensor data that changes every single loop, rather than a canned
bounce animation (Pre-Class homework) or a value set once and left alone.

### Complete wiring
**Wiring — same TFT pins as the Pre-Class and Class 1 homework:**
* [Raspberry Pi Pico 2w Pinout][20]
* [Adafruit 1.14" 240x135 Color Newxie TFT Display Pinout][33]

| Pico 2 W Pin | TFT Pin | Signal / Function |
| :------------- | :-------- | :-------------------- |
| `3V3 OUT` | `VIN` / `V+` | Power |
| `GND` | `GND` / `G` | Common ground |
| `GP18` | `SCK` / `CL` | SPI clock |
| `GP19` | `MOSI` / `DA` | SPI data, Pico → display |
| `GP20` | `CS` | Chip select |
| `GP21` | `DC` | Data/Command select |
| `GP22` | `RST` / `BL` | Reset |


### Complete code

```python
# code.py - Homework 4: the angle/distance sweep from tonight, now drawn
# live on the TFT instead of only printed to the console -- the first time
# in the course the TFT shows sensor data that changes every loop, not a
# canned animation or a static message.
import time
import board
import busio
import pwmio
import displayio
import fourwire
import terminalio
import adafruit_hcsr04
from adafruit_motor import servo
from adafruit_display_text import label
from adafruit_st7789 import ST7789

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP6, echo_pin=board.GP7)
pwm = pwmio.PWMOut(board.GP8, duty_cycle=0, frequency=50)
my_servo = servo.Servo(pwm, min_pulse=500, max_pulse=2500)

displayio.release_displays()
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19)
display_bus = fourwire.FourWire(spi, chip_select=board.GP20, command=board.GP21, reset=board.GP22)
display = ST7789(display_bus, width=240, height=135, rotation=270, rowstart=40, colstart=53)

main_group = displayio.Group()
display.root_group = main_group

readout = label.Label(terminalio.FONT, text="Class 2, HW4", color=0xFFFFFF)
readout.scale = 2
readout.anchor_point = (0.5, 0.5)
readout.anchored_position = (display.width // 2, display.height // 2)
main_group.append(readout)

SETTLE_TIME = 0.15

print("Class 2 Homework 4 -- sweeping, readout on the TFT.")

while True:
    for angle in range(0, 181, 10):
        my_servo.angle = angle
        time.sleep(SETTLE_TIME)
        try:
            distance = sonar.distance
            readout.text = f"angle {angle}\n{distance:.1f} cm"
        except RuntimeError:
            readout.text = f"angle {angle}\nreading error"
    for angle in range(180, -1, -10):
        my_servo.angle = angle
        time.sleep(SETTLE_TIME)
        try:
            distance = sonar.distance
            readout.text = f"angle {angle}\n{distance:.1f} cm"
        except RuntimeError:
            readout.text = f"angle {angle}\nreading error"
```

#### What You Observe
**Test it:** With the TFT wired per the table above, you should see the current angle and distance
update on screen at every stop of the sweep, changing live as the rig sweeps back and forth — no
serial console needed to watch it work. You'll need `adafruit_display_text` and `adafruit_st7789`
copied into `CIRCUITPY`'s `lib` folder, the same libraries used for the Pre-Class and Class 1 TFT
homework.

#### Real World Examples

* A car's backup-camera distance readout updates live as you get closer to an obstacle, the same
    "redraw the display every reading" pattern used here.
* A simple radar screen shows range-to-target updating in real time as the antenna sweeps — this
    project is a tiny, literal version of that idea.

### Homework 5 — Sensor Cross-Check: HC-SR04 Sweep vs. Fixed IR Sensor

**What this teaches:** *(Requires the IR Obstacle Avoidance Sensor — already in the course's bill
of materials for the Random Rover in Class 5, see [Section 2](#2-what-youll-need).)* This exercise
mounts the IR obstacle sensor fixed and forward-facing — not on the servo — right alongside the
sweeping HC-SR04, and flags moments where both sensors agree something is close near the forward
(90-degree) angle versus moments where only one does. This is the course's first taste of **sensor
fusion**: using two different sensing technologies (a timed sound echo vs. an IR threshold) to
catch a reading one sensor alone might get wrong. It's exactly why the Random Rover carries both
sensors starting in Class 5.

### Complete wiring
**Wiring — add the IR sensor, fixed and forward-facing, alongside tonight's circuit:**
* [Raspberry Pi Pico 2w Pinout][20]
* [IR Obstacle Avoidance Sensor Pinout][34]

| Pico 2 W Pin | Sensor Pin | Signal / Function |
| :------------- | :----------- | :-------------------- |
| `3V3 Out` (or `VBUS 5V`) | `VCC` | Power (most of these modules accept 3.3-5V) |
| `GND` | `GND` | Common ground |
| `GP13` | `OUT` | Digital output — LOW when an obstacle is detected |


### Complete code

```python
# code.py - Homework 5: cross-check the sweeping HC-SR04 against a FIXED,
# forward-facing IR obstacle sensor -- flags when both sensors agree
# something is close near the forward (90 degree) angle, versus when only
# one does. This is the course's first sensor-fusion / cross-validation
# exercise, exactly why the Random Rover eventually carries both sensors.
import time
import board
import pwmio
import digitalio
import adafruit_hcsr04
from adafruit_motor import servo
from adafruit_debouncer import Debouncer

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP6, echo_pin=board.GP7)
pwm = pwmio.PWMOut(board.GP8, duty_cycle=0, frequency=50)
my_servo = servo.Servo(pwm, min_pulse=500, max_pulse=2500)

# Fixed, forward-facing -- NOT mounted on the servo, unlike the HC-SR04.
ir_pin = digitalio.DigitalInOut(board.GP13)
ir_pin.direction = digitalio.Direction.INPUT
ir_sensor = Debouncer(ir_pin)

SETTLE_TIME = 0.15
FORWARD_WINDOW = range(80, 101, 10)  # angles we consider "forward-facing"
CLOSE_THRESHOLD_CM = 30

def read_and_compare(angle):
    ir_sensor.update()
    ir_says_close = not ir_sensor.value  # LOW means "something's there"

    try:
        sonar_distance = sonar.distance
        sonar_says_close = sonar_distance < CLOSE_THRESHOLD_CM
    except RuntimeError:
        sonar_distance = None
        sonar_says_close = False

    if angle in FORWARD_WINDOW:
        if sonar_says_close and ir_says_close:
            print("angle:", angle, "distance_cm:", sonar_distance, "-- BOTH sensors agree: close")
        elif sonar_says_close or ir_says_close:
            print("angle:", angle, "distance_cm:", sonar_distance, "-- sensors DISAGREE (possible false reading)")
        else:
            print("angle:", angle, "distance_cm:", sonar_distance, "-- clear")
    else:
        print("angle:", angle, "distance_cm:", sonar_distance)

print("Class 2 Homework 5 -- sweeping HC-SR04 cross-checked against a fixed IR sensor.")

while True:
    for angle in range(0, 181, 10):
        my_servo.angle = angle
        time.sleep(SETTLE_TIME)
        read_and_compare(angle)
    for angle in range(180, -1, -10):
        my_servo.angle = angle
        time.sleep(SETTLE_TIME)
        read_and_compare(angle)
```

#### What You Observe
**Test it:** Place an object directly in front of the rig (within the forward window, near 90
degrees) and confirm you see `BOTH sensors agree: close`. Now place something within HC-SR04 range
but off to the side where the fixed IR sensor can't see it (or vice versa) and confirm you get a
`sensors DISAGREE` line instead — proof the two sensors are genuinely being compared, not just
both printed side by side.

#### Real World Examples

* Self-driving cars combine radar, camera, and lidar because no single sensor is trusted alone —
    each has different blind spots and failure modes, the same idea behind this exercise.
* Industrial safety systems (light curtains, presence sensors on machinery) often require two
    independent sensing technologies to agree before treating a reading as real, to guard against a
    single sensor's false negative.

### Homework 6 — Non-Blocking Sweep You Can Pause Mid-Motion

**What this teaches:** Tonight's sweep code uses `time.sleep(SETTLE_TIME)` inside the loop, which
freezes the *entire* program for that pause — there's no way to interrupt it mid-sweep except
unplugging the board. This exercise rewrites the sweep using `time.monotonic()` timing instead, so
the main loop keeps running and stays responsive, and lets the Class 1 pushbutton pause and resume
the sweep at whatever angle it's currently at — not just at the end of a cycle. This is your first
non-blocking loop and your first simple two-state (running/paused) state machine layered on top of
a loop.

### Complete wiring
No new wiring — this reuses the pushbutton (`GP2`, from Class 1) and tonight's sensor+servo
circuit.

### Complete code

```python
# code.py - Homework 6: the same sweep-and-report project as tonight, but
# rewritten with time.monotonic() timing instead of time.sleep(), so the
# main loop stays responsive -- and the pushbutton pauses/resumes the sweep
# wherever it currently is, not just at the end of a cycle.
import time
import board
import pwmio
import digitalio
import adafruit_hcsr04
from adafruit_motor import servo
from adafruit_debouncer import Debouncer

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP6, echo_pin=board.GP7)
pwm = pwmio.PWMOut(board.GP8, duty_cycle=0, frequency=50)
my_servo = servo.Servo(pwm, min_pulse=500, max_pulse=2500)

button_pin = digitalio.DigitalInOut(board.GP2)
button_pin.direction = digitalio.Direction.INPUT
button_pin.pull = digitalio.Pull.UP
button = Debouncer(button_pin)

SETTLE_TIME = 0.15
STEP_DEGREES = 10

angle = 0
direction = 1  # +1 sweeping up, -1 sweeping down
paused = False
last_step_time = time.monotonic()

print("Class 2 Homework 6 -- sweeping. Press the button to pause/resume mid-sweep.")

while True:
    button.update()
    if button.fell:
        paused = not paused
        print("-- paused --" if paused else "-- resumed --")

    now = time.monotonic()
    # Non-blocking: only take a step once SETTLE_TIME has passed, instead of
    # freezing the whole program inside time.sleep() -- the button above
    # keeps getting checked every loop, even mid-settle.
    if not paused and (now - last_step_time) >= SETTLE_TIME:
        my_servo.angle = angle
        try:
            print("angle:", angle, "distance_cm:", sonar.distance)
        except RuntimeError:
            print("angle:", angle, "distance_cm: reading error")

        angle += direction * STEP_DEGREES
        if angle >= 180:
            angle = 180
            direction = -1
        elif angle <= 0:
            angle = 0
            direction = 1
        last_step_time = now
```

#### What You Observe
**Test it:** Watch the rig sweep normally, then press the button mid-swing — it should stop exactly
where it is, not finish the current cycle first. Press again to resume from that same angle. Notice
the button itself never feels sluggish to respond, even though the sweep is still "running" behind
the scenes — that's the non-blocking loop at work.

#### Real World Examples

* A security camera's automatic pan-scan can usually be frozen on demand by a guard who wants to
    look closer at something suspicious, then resumed — the same pause-in-place behavior.
* Any responsive user interface (a game, a web app) relies on non-blocking loops so a button click
    or keypress never has to wait for some unrelated animation to finish first.

### Homework 7 — Sweep Results Published to a WiFi Dashboard

**What this teaches:** *(Reuses the Pico's built-in WiFi radio and `adafruit_httpserver` — no new
part, but reuses the WiFi access-point pattern from the Pre-Class homework.)* The Pre-Class WiFi
homework only reported a single on/off LED flag over the web. This exercise instead publishes real
sensor *data*: the Pico becomes its own WiFi access point and serves a live table of the most
recent full sweep's angle/distance pairs, auto-refreshing every couple of seconds — the first time
in the course a whole set of sensor readings, not just one flag, is exposed to a browser.

### Complete code

```python
# code.py - Homework 7: the Pico becomes its own WiFi access point and
# serves a live table of the most recent full sweep's angle/distance pairs
# -- the first time sensor DATA (not just an on/off flag) is published over
# the web, reusing the WiFi AP pattern from the Pre-Class homework.
import time
import board
import pwmio
import wifi
import socketpool
import os
import adafruit_hcsr04
from adafruit_motor import servo
from adafruit_httpserver import Server, Request, Response

ap_ssid = os.getenv("CIRCUITPY_WIFI_AP_SSID")
ap_password = os.getenv("CIRCUITPY_WIFI_AP_PASSWORD")

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP6, echo_pin=board.GP7)
pwm = pwmio.PWMOut(board.GP8, duty_cycle=0, frequency=50)
my_servo = servo.Servo(pwm, min_pulse=500, max_pulse=2500)

wifi.radio.start_ap(ssid=ap_ssid, password=ap_password)
print("Access point started. Connect to:", ap_ssid)
print("Then visit http://" + str(wifi.radio.ipv4_address_ap) + "/ in a browser")

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)

latest_sweep = []  # list of (angle, distance_cm) from the most recently finished sweep

@server.route("/")
def base(request: Request):
    rows = "".join(
        f"<tr><td>{a}</td><td>{d:.1f} cm</td></tr>" for a, d in latest_sweep
    )
    html = f"""
    <html>
      <head>
        <title>Class 2 Sweep Dashboard</title>
        <meta http-equiv="refresh" content="2">
      </head>
      <body style="font-family: sans-serif; text-align: center; margin-top: 2em;">
        <h1>Latest Sweep</h1>
        <table style="margin: 0 auto;" border="1" cellpadding="6">
          <tr><th>Angle</th><th>Distance</th></tr>
          {rows}
        </table>
      </body>
    </html>
    """
    return Response(request, html, content_type="text/html")

server.start(str(wifi.radio.ipv4_address_ap))

SETTLE_TIME = 0.15
print("Class 2 Homework 7 -- sweeping and publishing results to the dashboard.")

while True:
    server.poll()

    sweep = []
    for angle in range(0, 181, 10):
        my_servo.angle = angle
        time.sleep(SETTLE_TIME)
        server.poll()  # keep answering browser requests even mid-sweep
        try:
            sweep.append((angle, sonar.distance))
        except RuntimeError:
            pass
    latest_sweep = sweep
```

#### What You Observe
**Test it:** Connect a phone or laptop to the `<your-name>` network (same `settings.toml` as the
Pre-Class WiFi homework) and load the printed address. You should see a table of angle/distance
pairs that updates every couple of seconds as new sweeps finish, with no serial console or cable
needed.

#### Real World Examples

* A home weather station publishes a live table of temperature, humidity, and wind readings to a
    local webpage the same way this dashboard publishes sweep data.
* Warehouse and greenhouse environmental-monitoring systems expose remote dashboards so a manager
    can check current sensor readings from anywhere on the network without walking the floor.

### Homework 8 — Remote-Controlled Servo Aim With Live Feedback (WiFi)

**What this teaches:** *(Reuses the Pico's built-in WiFi radio and `adafruit_httpserver`, combining
the ideas from Homework 2 and Homework 7 — no new part.)* A webpage served by the Pico has a slider
that sets the servo's target angle over WiFi, and that same page shows the distance reading at
wherever the servo is currently pointed. This is the most advanced exercise in tonight's homework
because it merges actuation (the servo), sensing (the HC-SR04), and networking (the WiFi access
point) into one interactive, closed-loop system controlled entirely from a browser — no laptop
cable to the Pico required. It's a real step toward the kind of remote monitoring the Random Rover
takes further as a stretch goal in Class 6.

### Complete code

```python
# code.py - Homework 8: combines Homework 2 and Homework 7 -- a webpage
# sets the servo's target angle over WiFi, and the same page shows the
# distance reading at wherever the servo is currently pointed. Full
# closed-loop remote control and feedback through a browser, no laptop
# cable needed -- a step toward Class 6's remote-monitoring stretch goal.
import board
import pwmio
import wifi
import socketpool
import os
import adafruit_hcsr04
from adafruit_motor import servo
from adafruit_httpserver import Server, Request, Response, GET

ap_ssid = os.getenv("CIRCUITPY_WIFI_AP_SSID")
ap_password = os.getenv("CIRCUITPY_WIFI_AP_PASSWORD")

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP6, echo_pin=board.GP7)
pwm = pwmio.PWMOut(board.GP8, duty_cycle=0, frequency=50)
my_servo = servo.Servo(pwm, min_pulse=500, max_pulse=2500)

current_angle = 90
my_servo.angle = current_angle

wifi.radio.start_ap(ssid=ap_ssid, password=ap_password)
print("Access point started. Connect to:", ap_ssid)
print("Then visit http://" + str(wifi.radio.ipv4_address_ap) + "/ in a browser")

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)

def current_distance():
    try:
        return f"{sonar.distance:.1f} cm"
    except RuntimeError:
        return "reading error"

@server.route("/", GET)
def base(request: Request):
    html = f"""
    <html>
      <body style="font-family: sans-serif; text-align: center; margin-top: 2em;">
        <h1>Angle: {current_angle} deg</h1>
        <h2>Distance: {current_distance()}</h2>
        <form action="/set" method="get">
          <input type="range" name="angle" min="0" max="180" value="{current_angle}"
                 onchange="this.form.submit()">
        </form>
      </body>
    </html>
    """
    return Response(request, html, content_type="text/html")

@server.route("/set", GET)
def set_angle(request: Request):
    # The Pico is being COMMANDED by the browser here, same pattern as the
    # Class 1 remote-dimmer homework, but now moving a servo instead of
    # setting an LED's brightness.
    global current_angle
    current_angle = int(request.query_params.get("angle", current_angle))
    my_servo.angle = current_angle
    return base(request)

server.start(str(wifi.radio.ipv4_address_ap))

print("Class 2 Homework 8 -- open the printed address and drag the slider to aim.")

while True:
    server.poll()
```

#### What You Observe
**Test it:** Connect to the `<your-name>` network and load the printed address. Drag the slider —
the physical servo should turn to match, and the page should reload showing the new angle and the
distance reading from that new position, all without touching a button on the breadboard.

#### Real World Examples

* Pan-tilt WiFi security cameras are commonly controlled from a web-based joystick panel exactly
    like this — drag a control, the camera physically moves, and the live feed confirms it worked.
* Remote-operated telescopes and weather instruments let an operator aim the hardware and read back
    a live measurement from across a network, the same request-then-feedback loop built here.

---

## References

* HC-SR04 / Servo Documentation
  * [Python & CircuitPython — Ultrasonic Sonar Distance Sensors][01] — Adafruit's official guide to
    wiring and reading the HC-SR04, including the voltage-divider caveat
  * [adafruit/Adafruit_CircuitPython_HCSR04][02] — the `adafruit_hcsr04` library used in this script
  * [CircuitPython Servo | CircuitPython Essentials][03] — PWM and `adafruit_motor.servo` basics
  * [DC, Servo, Stepper Motors and Solenoids with the Pico][04] — broader background on motor/servo
    control from the Pico
* Pinout References
  * [GPIO pinout and pin function guide for the Raspberry Pi Pico 2 W][20] — used throughout the
    Homework Assignments' wiring tables
  * [Adafruit 1.14" 240x135 Color Newxie TFT Display Pinout][33] — TFT pinout reference for
    Homework 4
  * [IR Obstacle Avoidance Sensor Pinout][34] — sensor pinout reference for Homework 5
* Random Rover Chassis
  * [How to assemble the 2WD Smart Robot Car Chassis Kit for Arduino][35] — assembly video for
    Homework 1
  * [Complete Assembly And Review Of A DIY Robot Smart Car Chassis Kit For Arduino or Raspberry Pi][36]
    — a second assembly walkthrough for Homework 1

---



[01]:https://learn.adafruit.com/ultrasonic-sonar-distance-sensors/python-circuitpython
[02]:https://github.com/adafruit/Adafruit_CircuitPython_HCSR04
[03]:https://learn.adafruit.com/circuitpython-essentials/circuitpython-servo
[04]:https://learn.adafruit.com/use-dc-stepper-servo-motor-solenoid-rp2040-pico
[19]:https://www.proculustech.com/tft-vs-lcd
[20]:https://pico2w.pinout.xyz/
[33]:https://cdn-learn.adafruit.com/downloads/pdf/adafruit-1-14-240x135-color-newxie-tft-display.pdf
[34]:https://docs.sunfounder.com/projects/umsk/en/latest/01_components_basic/08-component_ir_obstacle.html
[35]:https://www.youtube.com/watch?v=H78t6dnSoG0
[36]:https://www.youtube.com/watch?v=Q4UmbjXwoZ4
[37]:https://howtomechatronics.com/tutorials/arduino/ultrasonic-sensor-hc-sr04/
[38]:https://www.hackster.io/chip-pk/sg90-servo-motor-interfacing-with-arduino-complete-beginner-849eef
