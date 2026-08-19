# Lesson Plan: Class 2 — Ultrasonic Distance Sensor + Servo Motor

* **Class:** 2 of 6 (plus Pre-Class)
* **Phase:** Phase 1 — Inputs (Class 1-2: reliable sensing)
* **Duration:** ~2 hours (120 min)
* **Prerequisites from prior Classes:** Class 1 completed — every student has a working, debounced
  pushbutton switch (`GP2`) and rotary encoder (`GP3`/`GP4`) circuit on their breadboard, driving
  two LEDs (`GP14`/`GP15`), and is comfortable saving `code.py`, watching the serial console, and
  wiring from a pin table. That circuit stays on the breadboard, powered but unused, all Class —
  nothing from Class 1 is touched or rewired today.

---

## 1. Class Overview

This is the second and final Class of Phase 1 (Inputs). Students wire an HC-SR04 ultrasonic
distance sensor and an SG90 micro servo motor to their Pico 2 W — first separately, each with its
own simple "read a value" or "set a position" test program, then combined into one circuit where
the sensor rides on the servo shaft and sweeps back and forth, printing an angle/distance pair to
the serial console at each stop. This combined circuit — sensor mounted on servo, sweeping and
reporting — is a direct, unchanged preview of the scanning behavior the Random Rover uses to find
open space in Class 5. By the end of the Class, students will have seen two very different ways a
device encodes physical information for a microcontroller (a timed echo vs. a PWM pulse width),
and will have begun the group discussion of how a sweep of distance readings could tell a car
which way is safe to drive.

## 2. Learning Goals

* Wire an HC-SR04 ultrasonic distance sensor to the Pico 2 W, including the voltage-divider needed
  to protect the Pico's 3.3V logic from the sensor's 5V echo signal
* Wire an SG90 micro servo motor to the Pico 2 W and control its shaft angle with PWM
* Explain, in plain language, how the HC-SR04 measures distance (timed sound echo) and how the SG90
  interprets a pulse width as a target angle
* Mount the distance sensor on the servo shaft and read distance at each angle as the servo sweeps
  0-180 degrees and back
* Propose, as a group, an algorithm for using a sweep of angle/distance readings to steer a car away
  from obstacles

## 3. Preparation Checklist

* **1-2 days before:** Confirm every student's Class 1 circuit (button + encoder + 2 LEDs) is still
  intact and powers up — a quick visual/serial spot-check, not a rebuild. (~15 min)
* **1-2 days before:** Verify `adafruit_hcsr04` and `adafruit_motor` are present in the Adafruit
  CircuitPython Library Bundle folder each student is using; have a few copies on a USB stick as
  backup. (~10 min)
* **Day of, before students arrive:**
  * Set out one HC-SR04 ultrasonic distance sensor, one SG90 micro servo motor, a resistor pair
        for the echo voltage divider, double-sided tape or a small mount, and continued access to
        each workstation's existing breadboard. **[VERIFY]** — confirm the specific voltage-divider
        resistor values (e.g. 1k/2k) and the mounting hardware/tape are itemized and stocked; both
        are new to Class 2 and not part of the Class 1 kit.
  * Pre-build one reference circuit (HC-SR04 + SG90, separately and combined) at the instructor
        bench and test `class-2-code-1.py`, `class-2-code-2.py`, and `class-2-code-3.py` end-to-end.
        (~25 min)
  * Project the instructor's serial console output so the whole class can see live distance
        readings and, later, the angle/distance sweep pairs. (~5 min)
  * Have spare HC-SR04 units and SG90 servos on hand — cheap servos in particular vary in their
        center-pulse calibration and are the most likely part to need a swap.
* **Have ready:** A short list of discussion prompts for "how does each device encode information?"
  and "how could a sweep of readings help a car avoid bumping into things?" (see Direct Teaching and
  Closing below).

## 4. Materials & Components

Per-student unless noted. Component names only — see the course Bill of Materials for costs,
quantities, and sourcing.

| Component | Purpose This Class |
| :---------- | :-------------------- |
| Raspberry Pi Pico 2 W (with header) | Microcontroller running CircuitPython |
| HC-SR04 Ultrasonic Distance Sensor | Measures distance via a timed sound echo |
| SG90 Micro Servo Motor | Sweeps the distance sensor across an angle range via PWM |
| Voltage-divider resistor pair **[VERIFY — exact values]** | Steps the HC-SR04's 5V ECHO signal down to a safe 3.3V for the Pico |
| Double-sided tape or small mount **[VERIFY — not itemized]** | Fastens the HC-SR04 to the SG90 shaft/horn for the combined sweep |
| Breadboard (830-point, from Class 1) | Circuit assembly surface — Class 1's circuit stays on it, untouched |
| Dupont jumper wires (shared) | Point-to-point wiring |
| USB cable (student-supplied, from Pre-Class) | Power + serial connection to laptop |
| Windows 11 laptop with Mu or Thonny (student-supplied) | Edit and run CircuitPython code |
| Emo Smart Robot Car Chassis Kit | Optional: finish assembly if time remains |

## 5. Class Timeline

### 5a. Warm-up / Hook — ~10 min

**What to do:** Have every student plug in their Pico 2 W and confirm the Class 1 circuit still
works — press the button, turn the encoder, watch both LEDs respond. Ask 2-3 students what they'd
tell a friend debouncing *is*, in one sentence.

**What to say:** "Your button and encoder stay wired exactly as they are — you won't touch that
circuit again today, it's just going to sit there working while we build something new next to it.
Today you're adding two more senses to your board: one that measures distance by listening, and one
that can point itself at a target angle."

**What to watch for:** Any Class 1 regressions (loose jumper, LED popped out) — fix quickly rather
than losing momentum, since today's build shares breadboard space with Class 1's circuit.

**Time check:** If more than 2-3 boards need real rework, handle it during Guided Practice instead
of holding up the whole class now.

### 5b. Introduction — ~10 min

**What to do:** Introduce today's two new parts (HC-SR04 ultrasonic sensor, SG90 micro servo) and
preview that they'll end the class combined — sensor riding on servo, sweeping and reporting.

**What to say:**

* "These are the two building blocks of 'looking around' for a robot — one measures how far away
  something is, the other points things in a direction. Put together, they let a car scan a room."
* "They talk to the Pico in two totally different ways today: one sends a timed echo, one reads a
  pulse width. Same microcontroller, same breadboard, two different languages."
* "By the end of today, your sensor will be taped to your servo, sweeping back and forth, and your
  console will show you distance at every angle — that's the exact scanning behavior your finished
  Random Rover uses to avoid obstacles in Class 5."

**Questions to ask students:** "How do bats or dolphins figure out what's around them in the dark?"
(echolocation — a close real-world analogy for how the HC-SR04 works.)

### 5c. Direct Teaching — ~10 min

No code yet — diagrams and discussion only, using the whiteboard or projected diagram.

**Concept 1 — How the HC-SR04 encodes distance (Theory of Operation, brief).**
The sensor has two pins beyond power/ground: `TRIG` and `ECHO`. The Pico sends a short pulse on
`TRIG`, which fires an ultrasonic "chirp" from the sensor's transmitter. The sensor's receiver
listens for the chirp to bounce off whatever's in front of it and come back, then holds `ECHO` high
for exactly as long as that round trip took. Since the speed of sound is constant (~343 m/s at room
temperature), that time-high measurement converts directly to a distance: distance = (elapsed time x
speed of sound) / 2 (divide by 2 because the sound traveled to the object *and* back).

*Step-by-step decomposition of a single reading:*

1. Pico pulses `TRIG` high for 10 microseconds.
2. Sensor emits an ultrasonic chirp (40kHz, above human hearing).
3. Sensor's receiver waits for the chirp's echo to return.
4. Sensor holds `ECHO` high for the round-trip duration.
5. `adafruit_hcsr04` times how long `ECHO` stayed high and does the speed-of-sound math for you.
6. Code prints the resulting distance in centimeters.

**Concept 2 — Why the 5V/3.3V voltage divider matters.**
The HC-SR04 is designed for 5V logic (its `ECHO` pin can output up to 5V), but the Pico 2 W's GPIO
pins are only rated for 3.3V. Feeding 5V directly into a 3.3V-only pin risks damaging it. A simple
voltage divider (two resistors) on the `ECHO` line steps that 5V down to a safe ~3.3V before it
reaches the Pico. Ask: "Why doesn't the servo need this same protection?" (Its signal pin is a PWM
*input* the Pico drives, not a sensor output feeding back into the Pico — the Pico is the one
setting the voltage there.)

**Concept 3 — How the SG90 encodes angle (Theory of Operation, brief).**
The servo's signal pin doesn't take an analog voltage or a digital on/off — it reads the *width* of
a repeating pulse. A pulse around 1.5ms means "center, 90 degrees"; shorter pulses (down toward
0.5ms) sweep toward 0 degrees, longer pulses (up toward 2.5ms) sweep toward 180 degrees. This is PWM
(pulse-width modulation) — the same underlying technique that dimmed the encoder LED in Class 1, now
used to encode a position instead of a brightness. Ask: "Why might a designer pick a pulse-width
code instead of, say, 0-100% of a steady voltage?" (Pulse-width signals resist noise better over a
wire and are simple for a cheap analog servo circuit to decode without a precision voltage reference
— ties back to the Class 1 hardware-vs-software protocol discussion.)

**Concept 4 — Why the sensor has both a minimum and a maximum usable range.**
Very close objects don't leave enough time between the chirp going out and the receiver being ready
to listen again — that's the near-field blind spot. Very far or angled objects return an echo too
weak (or too spread out, given the sensor's beam angle) to reliably detect — that's the far-range
limit. Both limits trace back to the same physics: the speed of sound and the shape of the emitted
beam.

### 5d. Guided Practice — ~40 min

Instructor builds along on the projector; students wire up and test in parallel.

**Wiring — second circuit of the course, alongside (not replacing) Class 1's.** Leave Class 1's
button/encoder circuit exactly as-is on the breadboard; today's wiring uses entirely new pins.

| Component | Pico 2 W Pin |
| :---------- | :------------- |
| HC-SR04 `TRIG` | `GP6` |
| HC-SR04 `ECHO` (through voltage-divider resistors) | `GP7` |
| SG90 servo signal | `GP8` |
| HC-SR04 `VCC` | `5V` (VBUS) |
| SG90 servo `+`/power | `5V` (VBUS) |
| HC-SR04 `GND`, SG90 `GND` | `GND` |

**Checkpoint 1:** Before writing any code, have every pair trace their own wiring against the
table above out loud to a neighbor, and double-check the voltage-divider resistors sit on the
`ECHO` line (not `TRIG`). Wiring mistakes found now save debugging time later.

**Step 1 — HC-SR04 alone.**
Load `class-2-code-1.py` (save as `code.py`). Reads and prints live distance in centimeters.

```python
# class-2-code-1.py
# HC-SR04 alone -- prints live distance readings.
import time
import board
import adafruit_hcsr04

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP6, echo_pin=board.GP7)

print("Class 2 -- HC-SR04 distance readings starting...")

while True:
    try:
        print("distance_cm:", sonar.distance)
    except RuntimeError:
        print("distance_cm: reading error, retrying")
    time.sleep(0.2)
```

**What to watch for:** Occasional `RuntimeError` prints are normal (a missed echo) — the `try`/
`except` is there on purpose so one bad reading doesn't crash the loop. Persistent errors on every
loop usually mean a wiring problem, not a fluke.

**Checkpoint 2:** Every pair should see a stable `distance_cm` value that changes sensibly as they
move a hand toward and away from the sensor.

**Step 2 — SG90 alone.**
Load `class-2-code-2.py`. Sweeps the servo continuously from 0 to 180 degrees and back.

```python
# class-2-code-2.py
# SG90 alone -- continuous sweep, no sensor yet.
import time
import board
import pwmio
from adafruit_motor import servo

pwm = pwmio.PWMOut(board.GP8, duty_cycle=0, frequency=50)
my_servo = servo.Servo(pwm, min_pulse=500, max_pulse=2500)  # [VERIFY] -- recalibrate per servo

print("Class 2 -- SG90 sweep starting...")

while True:
    for angle in range(0, 181, 5):
        my_servo.angle = angle
        print("servo_angle:", angle)
        time.sleep(0.02)
    for angle in range(180, -1, -5):
        my_servo.angle = angle
        print("servo_angle:", angle)
        time.sleep(0.02)
```

**What to watch for:** A servo that twitches at the extremes or doesn't reach a true 0/180 usually
needs `min_pulse`/`max_pulse` tuned in small steps (e.g. 500 -> 600, 2500 -> 2400) — cheap SG90 units
vary unit to unit.

**Checkpoint 3:** Servo sweeps smoothly, end to end, with no grinding or stalling sound at either
extreme.

**Step 3 — combined: sensor mounted on servo, sweep-and-report.**
Mount the HC-SR04 to the servo horn/shaft with double-sided tape, keeping wires loose enough to
follow the sweep without snagging. Load `class-2-code-3.py`.

```python
# class-2-code-3.py
# HC-SR04 mounted on SG90 -- sweeps and prints angle + distance pairs.
import time
import board
import pwmio
import adafruit_hcsr04
from adafruit_motor import servo

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP6, echo_pin=board.GP7)
pwm = pwmio.PWMOut(board.GP8, duty_cycle=0, frequency=50)
my_servo = servo.Servo(pwm, min_pulse=500, max_pulse=2500)  # [VERIFY] -- recalibrate per servo

SETTLE_TIME = 0.15  # seconds -- let the servo stop moving before trusting the reading

print("Class 2 -- angle/distance sweep starting...")

while True:
    for angle in range(0, 181, 10):
        my_servo.angle = angle
        time.sleep(SETTLE_TIME)  # this is why we sleep after each move -- see Talking Points
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

**What to watch for:** This is the moment to raise the "how do you know the reading really matches
the angle you think you're at?" question from Talking Points — point at `SETTLE_TIME` as the
answer: without a short pause after each move, the sensor could be read mid-swing.

**What "done" looks like for this segment:** The console prints a clean `angle: X distance_cm: Y`
line at each stop as the sensor visibly sweeps back and forth, tracking a hand or object moved in
front of it.

### 5e. Independent Work — ~40 min

**What to do:** Students (in pairs where possible) run the combined sweep, place an object (a
water bottle, a hand, a notebook) somewhere in front of their setup, and capture a short console
log showing the sweep "finding" it as a dip in distance at a specific angle. Faster pairs can:

* Tune `SETTLE_TIME` down and observe at what point readings start looking wrong or lagged relative
  to the actual servo position.
* Narrow the sweep step (`range(..., 10)` -> `range(..., 5)`) and discuss the tradeoff between
  resolution and sweep speed.
* Begin (or continue) assembling the Emo Smart Robot Car Chassis Kit if both the sensor and servo
  milestone are working.

**What to watch for:** The most common failure at this stage is a servo that jitters or refuses to
hold an angle under load — almost always a power issue (drawing servo current straight from the
Pico's 3.3V rail instead of `5V`/VBUS), not a code bug. Check power before code.

**Time check:** At the 30-minute mark, do a quick show-of-hands: "Who has a clean angle/distance
sweep detecting an object?" Redirect instructor attention to pairs still stuck.

### 5f. Closing / Wrap-up — ~10 min

**What to do:** Ask 2-3 volunteers to demo their live sweep, placing an object in front of the
sensor so the group can watch the distance dip as the servo passes it. Open the group discussion:
"Looking at this angle/distance data scrolling by, how would you turn it into a decision — 'steer
left' or 'steer right'?"

**What to say:** "You just built the exact sensing setup your Random Rover will use in Class 5 to
avoid running into things — nothing about this wiring or mounting changes between now and then. The
only piece missing is a motor to actually act on what the sensor sees, and that's next Class."

**Preview next Class:** Class 3 reuses none of today's or Class 1's pins — it's the DRV8833 dual
H-bridge motor driver, wired fresh on `GP9`-`GP12`, while today's sensor+servo circuit and Class 1's
button+encoder circuit both stay untouched on the breadboard. Point students to the Class 3
references in the syllabus if they want to read ahead.

## 6. Troubleshooting Guide

| Problem | Likely Cause | Fix |
| :-------- | :------------- | :---- |
| `distance_cm` never prints, only errors | `TRIG`/`ECHO` swapped, or missing voltage divider on `ECHO` | Verify `TRIG` on `GP6`, `ECHO` on `GP7` through the divider resistors |
| `distance_cm` reads a fixed, unchanging number | Sensor pointed at a wall/ceiling too close or too far outside its usable range | Re-aim the sensor at an object within roughly 2cm-4m |
| Servo doesn't move at all | Servo power wired to `3V3` instead of `5V`/VBUS, or signal pin wrong | Confirm signal on `GP8`, power on `5V`, ground on `GND` |
| Servo twitches or buzzes but doesn't reach 0/180 | `min_pulse`/`max_pulse` not calibrated for this specific servo | Adjust `min_pulse`/`max_pulse` in small steps and re-test |
| Servo resets/browns out when it moves | Drawing servo current from the same weak 3.3V/5V source as the Pico's logic | Confirm servo power comes from `5V`/VBUS with adequate current, not a shared thin jumper |
| Combined sweep prints angle but distance looks "stale" or mismatched | `SETTLE_TIME` too short, reading taken mid-move | Increase `SETTLE_TIME` in small steps (e.g. `0.15` -> `0.2` -> `0.3`) |
| `ImportError: no module named 'adafruit_hcsr04'` (or `adafruit_motor`) | Library not copied to `/lib` on CIRCUITPY drive | Copy the missing `.mpy` file(s) from the Library Bundle into `/lib` |
| Sensor taped to servo horn wobbles or falls off mid-sweep | Tape not fully adhered, or wires pulling on the sensor | Press tape firmly on a clean, dry surface; add slack to the sensor's wires |

## 7. Age Differentiation Notes

**Younger students (12-14) and their parent/guardian:** Provide the pin table above pre-printed
and laminated at the workstation so it's a lookup, not a memorization task. Pair a younger
student's fine-wiring and taping work with the parent/guardian's help holding components steady
while mounting the sensor on the servo horn. Start from `class-2-code-1.py` and `class-2-code-2.py`
already loaded as starting points rather than typed from scratch, and have them focus on reading
and tuning values (e.g., changing `SETTLE_TIME`) rather than writing the combined script from a
blank file.

**Older students (15-18) and adults:** Have them type `class-2-code-1.py` and `class-2-code-2.py`
themselves from the wiring table and a description of the goal, rather than starting from the
provided files. Once the combined-sweep milestone is met, challenge them to have the servo pause
and print a distinct "object detected!" line whenever a reading drops below a threshold distance —
a direct preview of the collision logic coming in Class 5.

## 8. Assessment

**Milestone Assignment (per syllabus, Phase 1 / Class 2):** Live streamed distance-vs-angle data as
the servo sweeps.

**What "complete" looks like:** The student can run `class-2-code-3.py` and show the servo sweeping
0-180 degrees and back while the serial console prints a clean `angle:`/`distance_cm:` pair at every
stop, with the distance visibly dipping when an object is placed in the sensor's path at a
particular angle.

**How to give feedback without scoring:** Ask the student to narrate what the sweep data would need
to look like for a program to automatically pick "the clearest direction" ("what would you tell the
code to look for in this list of numbers?") rather than checking a box. If a pair can't get a clean
combined sweep in the time available, that's fine — have them bring a working version to the start
of Class 3 and note it in their build journal.

## 9. Instructor Tips

* Run the combined sweep yourself, live, on the projector *before* students touch their own boards —
  watching the sensor physically scan back and forth while numbers stream by builds anticipation
  better than describing it.
* Cheap SG90 servos vary more in their center-pulse calibration than the HC-SR04 units vary in
  accuracy; if one pair's servo won't settle after two or three `min_pulse`/`max_pulse` adjustments,
  swap the unit rather than burning class time chasing a bad part.
* The voltage-divider wiring on `ECHO` is the easiest step to get wrong and the least forgiving to
  get wrong (risking the Pico's GPIO pin) — walk the room and spot-check this specific connection
  before anyone powers on for the first time.
* Keep all three code files (`class-2-code-1.py`, `class-2-code-2.py`, `class-2-code-3.py`) on a
  shared drive/USB stick so a student who breaks their working file can recover instantly instead of
  losing class time.
* The "how would you turn this data into a steering decision?" discussion (Closing) is worth letting
  run a little long here — it's the direct conceptual seed for Class 5's collision-avoidance
  algorithm, and students who reason it out themselves now will recognize the pattern faster later.

## 10. Resources & References

* [HC-SR04 Ultrasonic Module Distance Sensor — Product Page][01] — the sensor used this Class
* [Python & CircuitPython | Ultrasonic Sonar Distance Sensors][02] — Adafruit's official guide to
  wiring and reading the HC-SR04, including the voltage-divider caveat
* [adafruit/Adafruit_CircuitPython_HCSR04][03] — the `adafruit_hcsr04` library source used in
  `class-2-code-1.py` and `class-2-code-3.py`
* [SG90 9g Micro Servo Motor — Product Page][04] — the servo used this Class
* [CircuitPython Servo | CircuitPython Essentials][05] — PWM and `adafruit_motor.servo` basics used
  in `class-2-code-2.py` and `class-2-code-3.py`
* [DC, Servo, Stepper Motors and Solenoids with the Pico][06] — broader background on motor/servo
  control from the Pico, useful for students who want to read ahead into Class 3

---

[01]:https://www.amazon.com/AEDIKO-HC-SR04-Ultrasonic-Distance-Arduino/dp/B09BYWHSMJ
[02]:https://learn.adafruit.com/ultrasonic-sonar-distance-sensors/python-circuitpython
[03]:https://github.com/adafruit/Adafruit_CircuitPython_HCSR04
[04]:https://www.amazon.com/Micro-Helicopter-Airplane-Remote-Control/dp/B072V529YD/?th=1
[05]:https://learn.adafruit.com/circuitpython-essentials/circuitpython-servo
[06]:https://learn.adafruit.com/use-dc-stepper-servo-motor-solenoid-rp2040-pico
