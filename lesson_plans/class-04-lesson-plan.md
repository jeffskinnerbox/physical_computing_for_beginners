# Lesson Plan: Class 4 — Inertial Measurement Unit (IMU)

* **Class:** 4 of 6 (plus Pre-Class)
* **Phase:** Phase 2 — Outputs & Motion (Class 3-4: driving motors and reading orientation)
* **Duration:** ~2 hours (120 min)
* **Prerequisites from prior Classes:** Classes 1-3 completed — every student has a working
  debounced pushbutton/rotary-encoder circuit (`GP2`-`GP4`, `GP14`-`GP15`), a working HC-SR04 + SG90
  sensor-sweep circuit (`GP6`-`GP8`), and a working DRV8833 motor driver circuit (`GP9`-`GP12`) on
  their breadboard, and has just finished Class 3 having directly experienced how open-loop, timed
  moves drift off target. Students should have Python installed on their laptop (from the Pre-Class)
  and be comfortable running a script from a terminal. All three prior circuits stay on the
  breadboard, powered but unused, all Class — nothing from Class 1, 2, or 3 is touched or rewired
  today.

---

## 1. Class Overview

This is the fourth Class of the course and the second of Phase 2 (Outputs & Motion). Class 3 ended
with an open question: the car can move, but it has no way to know whether it actually went where it
was told. Today's Class introduces the LSM9DS1 9-DOF IMU as a first attempt at an answer — a sensor
that reports orientation (which way the car is pointed) rather than distance or position. Students
wire the IMU over I2C, read raw accelerometer and gyroscope values, and then fuse those two noisy,
individually-flawed signals into a single stable roll/pitch/yaw orientation using a Mahony filter —
streaming that orientation to a live 3D box rendered on their laptop, so they can watch their
physical tilt reflected on screen in real time. The Class closes by pushing back on the excitement:
orientation alone still doesn't solve Class 3's square/circle problem, because knowing which way
you're pointed isn't the same as knowing how far you've traveled — a gap the students name explicitly
before Class 5 combines everything into the Random Rover.

## 2. Learning Goals

* Wire the LSM9DS1 9-DOF IMU breakout board to the Pico 2 W over I2C
* Read raw accelerometer (x/y/z) and gyroscope (x/y/z) values and explain, in plain language, what
  each sensor measures and where each one is individually unreliable
* Explain why fusing the accelerometer and gyroscope with a Mahony filter produces a more usable
  orientation than either sensor alone
* Tune the Mahony filter's `MAHONY_KP` gain and observe, live, the tradeoff between orientation drift
  and jitter
* Stream fused roll/pitch/yaw orientation from the Pico to a live 3D visualization running on the
  laptop
* Identify what information is still missing to fully solve Class 3's square/circle challenge, even
  with working orientation data

## 3. Preparation Checklist

* **1-2 days before:** Confirm every student's Class 1, 2, and 3 circuits are still intact and
  power up — a quick visual/serial spot-check, not a rebuild. (~15 min)
* **1-2 days before:** Verify `adafruit_lsm9ds1` is present in each student's Library Bundle folder;
  have a few copies on a USB stick as backup. (~10 min)
* **1-2 days before:** Confirm every student laptop can run `pip install pyserial matplotlib numpy`
  successfully — test on a spare laptop or ask students to pre-install before Class if possible, since
  this is the first Class requiring a Python install on the laptop side rather than just an editor.
  (~15 min)
* **Day of, before students arrive:**
* Set out one LSM9DS1 9-DOF breakout board and a STEMMA QT/Qwiic cable (or Dupont jumpers if not
        using STEMMA QT) at each workstation, alongside continued access to the existing breadboard.
* Pre-build one reference circuit at the instructor bench and test `class-4-code-1.py` (on the
        Pico) together with `class-4-code-2.py` (on a laptop) end-to-end, confirming the 3D box
        responds correctly to physical tilting in all three axes. (~25 min)
* Note which serial port `class-4-code-2.py` needs (e.g. `COM5`) on the instructor's machine so
        you can show students how to find their own port quickly. (~5 min)
* Project the instructor's live 3D box display so the whole class can see it respond to the
        instructor tilting their board. (~5 min)
* Have spare LSM9DS1 boards and STEMMA QT cables on hand.
* **Have ready:** A short list of discussion prompts for "does this solve Class 3's problem?" (see
  Direct Teaching and Closing below).

## 4. Materials & Components

Per-student unless noted. Component names only — see the course Bill of Materials for costs,
quantities, and sourcing.

| Component | Purpose This Class |
| :---------- | :-------------------- |
| Raspberry Pi Pico 2 W (with header) | Microcontroller running CircuitPython |
| IMU: LSM9DS1 9-DOF Breakout Board (STEMMA) | Measures acceleration and rotation rate; fused into orientation |
| STEMMA QT/Qwiic cable | I2C connection between the Pico and the IMU |
| Breadboard (830-point, from Class 1) | Circuit assembly surface — Classes 1-3 circuits stay on it, untouched |
| Dupont jumper wires (shared) | Point-to-point wiring, if not using STEMMA QT directly |
| USB cable (student-supplied, from Pre-Class) | Power + serial connection to laptop |
| Windows 11 laptop with Mu or Thonny (student-supplied) | Edit and run CircuitPython code |
| Windows 11 laptop with Python 3 installed (student-supplied) | Runs `class-4-code-2.py` to display the live 3D box |
| Emo Smart Robot Car Chassis Kit | Optional: continue assembly if time remains |

## 5. Class Timeline

### 5a. Warm-up / Hook — ~10 min

**What to do:** Have every student plug in their Pico 2 W and confirm all three prior circuits still
work. Ask 2-3 students to recap, in their own words, what "open-loop" or "dead reckoning" meant in
Class 3, and why the square/circle attempt drifted.

**What to say:** "Last time, your car moved with confidence and no idea whether it was actually
doing what you told it. Today you're giving it a sense of balance — a way to know which way it's
pointed, moment to moment, the same way your inner ear tells you which way is up with your eyes
closed."

**What to watch for:** Any regressions in the Class 1-3 circuits — fix quickly rather than losing
momentum, since today's build shares breadboard space with all three.

**Time check:** If more than 2-3 boards need real rework, handle it during Guided Practice instead
of holding up the whole class now.

### 5b. Introduction — ~10 min

**What to do:** Introduce the LSM9DS1 IMU and preview today's payoff: a live 3D box on the laptop
screen that tilts exactly as the physical board tilts.

**What to say:**

* "This one sensor actually contains several — an accelerometer, a gyroscope, and a magnetometer,
  which is where the '9-DOF,' nine degrees of freedom, comes from. Today we're using the first two."
* "By the end of today, you'll tilt your board on the table and watch a box on your laptop screen
  tilt the same way, live, over serial."
* "But I want you thinking critically the whole time: does knowing which way you're pointed actually
  solve the problem from last Class?"

**Questions to ask students:** "Close your eyes and tip your head sideways. How do you know you did
that, without looking?" (Sets up the accelerometer-as-inner-ear analogy before the term is used.)

### 5c. Direct Teaching — ~10 min

No code yet — diagrams and discussion only, using the whiteboard or projected diagram.

**Concept 1 — What each sensor actually measures (Theory of Operation, brief).**
An accelerometer measures linear acceleration along three axes (x/y/z) — including, always, the
constant downward pull of gravity. At rest, its reading points straight toward the floor, which is
exactly how it can be used to sense tilt: as the board rotates, gravity's component shifts between
the axes in a predictable way. A gyroscope measures angular *rate* — how fast the board is rotating
around each axis, in degrees per second — not an absolute angle.

**Concept 2 — Why neither sensor alone is good enough.**
Ask: "If the accelerometer can already sense tilt from gravity, why do we need the gyroscope at
all?" Draw out: the accelerometer is *noisy* under vibration or sudden movement — a moving car is
constantly shaking the accelerometer with forces that have nothing to do with tilt, so its instant
reading is unreliable while moving. The gyroscope is smooth and fast to respond, but it only measures
*change* — small measurement errors accumulate ("integrate") into a growing drift over time, so a
gyro-only orientation slowly wanders away from the truth even if the board never moves.

**Concept 3 — Why fusing them works (the Mahony filter, brief).**
A sensor fusion filter combines both signals to get the best of each: it trusts the gyroscope for
fast, moment-to-moment changes, and continuously nudges its estimate back toward what the
accelerometer says over the longer term, correcting the gyro's drift without inheriting the
accelerometer's short-term noise. `class-4-code-1.py` uses a Mahony filter for this — mention that
Kalman and Madgwick filters solve the same problem with different math, but Mahony is what's actually
implemented here. Ask: "If you only trusted the gyroscope forever, what would happen to your
orientation estimate after ten minutes of sitting still?" (It would slowly drift away from level,
even though nothing moved — pure integration error.)

**Concept 4 — What orientation still doesn't tell you.**
Roll/pitch/yaw tells you which way something is pointed, right now — nothing about how far it has
traveled or where it is. Ask: "Would knowing your car's exact heading, every instant, have been
enough to nail the Class 3 square?" Draw out: heading alone still leaves distance unmeasured — you'd
know you turned exactly 90 degrees, but not how far you drove before or after that turn. This sets up
the "what's still missing?" discussion at Closing.

### 5d. Guided Practice — ~40 min

Instructor builds along on the projector; students wire up and test in parallel.

**Wiring — fourth circuit of the course, alongside (not replacing) Classes 1-3.** Leave all three
prior circuits exactly as-is on the breadboard; today's wiring uses entirely new pins and, if
available, a STEMMA QT cable instead of individual jumpers.

| Component | Pico 2 W Pin |
| :---------- | :------------- |
| LSM9DS1 `SDA` | `GP0` |
| LSM9DS1 `SCL` | `GP1` |
| LSM9DS1 `VIN`/power | `3V3` |
| LSM9DS1 `GND` | `GND` |

**Checkpoint 1:** Before writing any code, have every pair trace their own wiring against the
table above out loud to a neighbor — especially confirming `SDA`/`SCL` aren't swapped, since I2C
devices commonly fail silently (no error, just no data) when they are. Wiring mistakes found now
save debugging time later.

**Step 1 — read and fuse, print to serial.**
Load `class-4-code-1.py` (save as `code.py`) onto the Pico. Reads accelerometer and gyroscope data
over I2C, fuses it with a Mahony filter, and prints `roll,pitch,yaw` CSV lines.

```python
# class-4-code-1.py
# LSM9DS1 over I2C -- reads accel+gyro, fuses with a Mahony filter, prints roll,pitch,yaw.
import time
import board
import busio
import adafruit_lsm9ds1

i2c = busio.I2C(board.GP1, board.GP0)  # SCL, SDA
sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

# Mahony filter state and tunable gains
MAHONY_KP = 2.0  # [VERIFY] -- proportional gain; raise/lower live to see drift-vs-jitter tradeoff
MAHONY_KI = 0.05  # [VERIFY] -- integral gain; corrects long-term gyro bias

# quaternion, initialized level
q0, q1, q2, q3 = 1.0, 0.0, 0.0, 0.0
integral_fbx = integral_fby = integral_fbz = 0.0
last_time = time.monotonic()


def mahony_update(ax, ay, az, gx, gy, gz, dt):
    global q0, q1, q2, q3, integral_fbx, integral_fby, integral_fbz

    norm = (ax * ax + ay * ay + az * az) ** 0.5
    if norm == 0:
        return
    ax, ay, az = ax / norm, ay / norm, az / norm

    # estimated gravity direction from current quaternion
    vx = 2 * (q1 * q3 - q0 * q2)
    vy = 2 * (q0 * q1 + q2 * q3)
    vz = q0 * q0 - q1 * q1 - q2 * q2 + q3 * q3

    # error between measured and estimated gravity
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


def quaternion_to_euler():
    import math
    roll = math.degrees(math.atan2(2 * (q0 * q1 + q2 * q3), 1 - 2 * (q1 * q1 + q2 * q2)))
    pitch = math.degrees(math.asin(max(-1.0, min(1.0, 2 * (q0 * q2 - q3 * q1)))))
    yaw = math.degrees(math.atan2(2 * (q0 * q3 + q1 * q2), 1 - 2 * (q2 * q2 + q3 * q3)))
    return roll, pitch, yaw


print("Class 4 -- IMU orientation streaming starting...")

while True:
    now = time.monotonic()
    dt = now - last_time
    last_time = now

    ax, ay, az = sensor.acceleration
    gx, gy, gz = sensor.gyro  # degrees/sec
    import math
    gx, gy, gz = math.radians(gx), math.radians(gy), math.radians(gz)

    mahony_update(ax, ay, az, gx, gy, gz, dt)
    roll, pitch, yaw = quaternion_to_euler()
    print("{:.1f},{:.1f},{:.1f}".format(roll, pitch, yaw))

    time.sleep(0.02)
```

**What to watch for:** A flat line of `0.0,0.0,0.0` (or no output at all) almost always means the I2C
wiring is wrong, not the filter math — check `SDA`/`SCL` before touching `MAHONY_KP`/`MAHONY_KI`.

**Checkpoint 2:** Every pair should see three changing numbers scroll by that respond sensibly when
the board is tilted by hand — roll and pitch changing with tilt, yaw drifting slowly if the board
isn't rotated flat.

**Step 2 — live 3D visualization on the laptop.**
On the laptop (not the Pico), install dependencies once: `pip install pyserial matplotlib numpy`.
Then run `class-4-code-2.py <port>`, substituting the student's actual serial port (e.g. `COM5` on
Windows — visible in Mu's/Thonny's device list or Device Manager).

```python
# class-4-code-2.py
# Runs on the LAPTOP, not the Pico. Reads roll,pitch,yaw CSV over serial, draws a live 3D box.
# Usage: python class-4-code-2.py <port>
import sys
import time
import serial
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

PORT = sys.argv[1] if len(sys.argv) > 1 else "COM5"  # [VERIFY] -- set to your board's port
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=1)

box_vertices = np.array([
    [-1, -0.5, -0.2], [1, -0.5, -0.2], [1, 0.5, -0.2], [-1, 0.5, -0.2],
    [-1, -0.5, 0.2], [1, -0.5, 0.2], [1, 0.5, 0.2], [-1, 0.5, 0.2],
])
edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4),
         (0, 4), (1, 5), (2, 6), (3, 7)]


def rotation_matrix(roll, pitch, yaw):
    r, p, y = np.radians([roll, pitch, yaw])
    rx = np.array([[1, 0, 0], [0, np.cos(r), -np.sin(r)], [0, np.sin(r), np.cos(r)]])
    ry = np.array([[np.cos(p), 0, np.sin(p)], [0, 1, 0], [-np.sin(p), 0, np.cos(p)]])
    rz = np.array([[np.cos(y), -np.sin(y), 0], [np.sin(y), np.cos(y), 0], [0, 0, 1]])
    return rz @ ry @ rx


plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

print("Class 4 -- 3D box display starting, reading from", PORT)

while True:
    line = ser.readline().decode("utf-8", errors="ignore").strip()
    if not line:
        continue
    try:
        roll, pitch, yaw = [float(v) for v in line.split(",")]
    except ValueError:
        continue

    rotated = box_vertices @ rotation_matrix(roll, pitch, yaw).T

    ax.cla()
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    for a, b in edges:
        pts = rotated[[a, b]]
        ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color="C0")
    ax.set_title("roll={:.0f} pitch={:.0f} yaw={:.0f}".format(roll, pitch, yaw))
    plt.pause(0.01)
```

**What to watch for:** A "port not found" or permission error usually means either the wrong `PORT`
was passed, or Mu/Thonny's serial console is still connected to that same port and needs to be
closed first — only one program can hold a serial port open at a time.

**What "done" looks like for this segment:** Tilting the physical board visibly and correctly tilts
the on-screen 3D box in the matching direction, in real time.

### 5e. Independent Work — ~40 min

**What to do:** Students (in pairs where possible) experiment with the live display, then run the
`MAHONY_KP` tuning exercise: raise it in a few steps and describe what happens (faster response, more
jitter), then lower it below the default and describe what happens (smoother, but slower to correct
drift). Capture before/after observations in the build journal. Faster pairs can:

* Try physically shaking the board gently while watching the display, to see the fused output stay
  far steadier than a raw-accelerometer-only version would.
* Mount the IMU off to one side of a straight edge (like a ruler) versus centered, spin it around a
  fixed pivot point, and discuss whether the readings differ — connects to the Talking Points
  question about mounting position and turning.
* Continue assembling the Emo Smart Robot Car Chassis Kit if the orientation milestone is working.

**What to watch for:** The most common failure at this stage is a 3D box that moves but on the wrong
axis, or inverted — usually a sign convention mismatch between the sensor's physical mounting
orientation and the visualization's assumed axes, not a bug in the filter itself. Note it and move
on rather than debugging axis conventions live.

**Time check:** At the 30-minute mark, do a quick show-of-hands: "Who has a live 3D box responding
correctly to tilt?" Redirect instructor attention to pairs still stuck.

### 5f. Closing / Wrap-up — ~10 min

**What to do:** Ask 2-3 volunteers to demo their live 3D box responding to physical tilts. Then run
the "does this solve Class 3's problem?" discussion: ask the group directly whether orientation data
alone would have gotten their square and circle attempts closer to 12 inches, and why or why not.

**What to say:** "You now have a car that can move, and a sensor that knows which way it's pointed.
That's real progress — but notice neither one, alone or together, tells you *how far* you've gone.
That gap is exactly why Class 5 doesn't use the IMU or dead-reckoning distance at all — it solves
navigation a completely different way, using the sensor and servo you built back in Class 2."

**Preview next Class:** Class 5 reuses no new pins — it reconnects exactly the Class 2 sensor+servo
circuit (`GP6`-`GP8`) and the Class 3 motor driver circuit (`GP9`-`GP12`) as they were left wired,
combining them into the Random Rover's collision-avoidance behavior. Today's IMU circuit and Class
1's button/encoder circuit both stay untouched on the breadboard. Point students to the Class 5
references in the syllabus if they want to read ahead.

## 6. Troubleshooting Guide

| Problem | Likely Cause | Fix |
| :-------- | :------------- | :---- |
| No serial output at all from `class-4-code-1.py` | `SDA`/`SCL` swapped, or I2C device not detected | Verify `SDA` on `GP0`, `SCL` on `GP1`; confirm power/ground |
| `roll,pitch,yaw` prints but never changes | Board isn't actually being moved, or a loose connection is producing a flat/stuck reading | Physically tilt the board while watching output; reseat the STEMMA QT cable if still stuck |
| Orientation drifts noticeably even when the board sits still | `MAHONY_KI` too low, or `MAHONY_KP` too low to correct drift | Raise `MAHONY_KP`/`MAHONY_KI` in small steps and re-test |
| Orientation is jittery/noisy even when the board is still | `MAHONY_KP` too high | Lower `MAHONY_KP` in small steps and re-test |
| 3D box moves on the wrong axis or inverted | Sign/axis convention mismatch between physical mounting and `class-4-code-2.py`'s rotation matrix | Note as a known limitation; not worth debugging live — flag as [VERIFY] for later |
| `class-4-code-2.py` can't open the serial port | Wrong `PORT` argument, or Mu/Thonny's serial console still has the port open | Close Mu/Thonny's serial console first; confirm the correct COM port in Device Manager |
| `ModuleNotFoundError` for `serial`, `matplotlib`, or `numpy` | Dependencies not installed on the laptop | Run `pip install pyserial matplotlib numpy` in the same Python environment used to run the script |
| `ImportError: no module named 'adafruit_lsm9ds1'` | Library not copied to `/lib` on CIRCUITPY drive | Copy the `adafruit_lsm9ds1.mpy` file from the Library Bundle into `/lib` |

## 7. Age Differentiation Notes

**Younger students (12-14) and their parent/guardian:** Provide the pin table above pre-printed and
laminated at the workstation so it's a lookup, not a memorization task. Pair a younger student's
STEMMA QT/wiring work with the parent/guardian's help typing the `pip install` command and finding
the correct COM port in Windows. Start from `class-4-code-1.py` and `class-4-code-2.py` already
loaded as starting points, and have them focus on the `MAHONY_KP` tuning exercise (a guided,
observable experiment) rather than reading the quaternion math.

**Older students (15-18) and adults:** Walk them through the quaternion math in `mahony_update()`
line by line rather than treating it as a black box, and have them explain in their own words why
the filter blends a proportional correction (`MAHONY_KP`) with an integral correction (`MAHONY_KI`).
Once the milestone is met, challenge them to log roll/pitch/yaw to a file over a fixed time window
while the board sits still, and quantify residual drift numerically instead of just watching the
on-screen box.

## 8. Assessment

**Milestone Assignment (per syllabus, Phase 2 / Class 4):** Live 3D orientation display driven by the
IMU.

**What "complete" looks like:** The student can run `class-4-code-1.py` on the Pico and
`class-4-code-2.py` on their laptop simultaneously, and show the on-screen 3D box tilting to match
the physical board's roll, pitch, and yaw in real time.

**How to give feedback without scoring:** Ask the student to physically tilt the board along one
axis at a time and narrate which on-screen motion corresponds to which physical motion ("show me
roll, show me pitch, show me yaw") rather than checking a box. If a pair can't get the full 3D
display working in the time available, accepting a working `class-4-code-1.py` with sensible serial
output (without the laptop visualization) is a reasonable partial milestone — have them bring the
full display working to the start of Class 5 and note it in their build journal.

## 9. Instructor Tips

* Run the live 3D box yourself, live, on the projector *before* students touch their own boards —
  watching the box tilt in real time as you tilt the physical board is the single most convincing
  demo in the course so far.
* This is the first Class requiring a Python install on the student's laptop itself, not just an
  editor — budget extra troubleshooting time for `pip install` issues (corporate/school laptop
  restrictions, PATH problems) and have a couple of pre-configured spare laptops ready as a fallback.
* The `MAHONY_KP` tuning exercise (Independent Work) is worth insisting every pair actually do, not
  just discuss — the drift-vs-jitter tradeoff is abstract until you've watched it happen on your own
  board.
* Axis-convention mismatches in the 3D display (Troubleshooting) are common and not worth solving
  live in front of the class — acknowledge it, flag it as a known rough edge, and move on so it
  doesn't eat the whole Independent Work block.
* The "does this solve Class 3's problem?" discussion (Closing) should land as a genuine letdown
  followed by curiosity, not a gotcha — the point is that students feel the gap themselves before
  Class 5 explains how the course actually closes it (via the sensor/servo scan, not the IMU).

## 10. Resources & References

* [Python & CircuitPython — Adafruit LSM9DS1 9-DOF Breakout][01] — Adafruit's official guide for
  wiring and reading the LSM9DS1 over I2C in CircuitPython
* [API Reference — Adafruit LSM9DS1 Library][02] — the `adafruit_lsm9ds1` library API used in
  `class-4-code-1.py`
* [Adafruit Learn — LSM6DSOX/ISM330DHC/LSM6DSO32 6-DoF IMUs (CircuitPython)][03] — a related IMU
  family guide, useful as a cross-reference for students researching independently
* [9-DOF LSM9DS1 Breakout Board — Product Page][04] — the IMU used this Class
* [Inertial Measurement Unit (IMU) — overview video][05] — background on what an IMU is and does

---

[01]:https://learn.adafruit.com/adafruit-lsm9ds1-accelerometer-plus-gyro-plus-magnetometer-9-dof-breakout/python-circuitpython
[02]:https://docs.circuitpython.org/projects/lsm9ds1/en/latest/api.html
[03]:https://learn.adafruit.com/lsm6dsox-and-ism330dhc-6-dof-imu/python-circuitpython
[04]:https://www.adafruit.com/product/4634
[05]:https://www.youtube.com/watch?v=qS9GwaekLW4
