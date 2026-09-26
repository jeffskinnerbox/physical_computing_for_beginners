# Lesson Plan: Class 4 — Inertial Measurement Unit (IMU)

* **Class:** 4 of 6 (plus Pre-Class)
* **Phase:** Phase 2 — Outputs & Motion (Class 3-4: driving motors and reading orientation)
* **Duration:** ~2 hours (120 min). Gyro bias calibration and extending `rover_server.py` with
  orientation data both fit inside the original 120-min slot as brisk third and fourth Guided
  Practice steps (small edits to code students already have running, not new builds) — see the
  "Class Timeline" pacing note below for what to cut first if a group runs long.
* **Prerequisites from prior Classes:** Classes 1-3 completed — every student has a working
  debounced pushbutton/rotary-encoder circuit (`GP2`-`GP4`, `GP14`-`GP15`), a working HC-SR04 + SG90
  sensor-sweep circuit (`GP6`-`GP8`), and a working DRV8833 motor driver circuit (`GP9`-`GP12`,
  with the wheel optocouplers on `GP19`/`GP17`) on their breadboard, and has just finished Class 3 having directly experienced how
  open-loop, timed moves drift off target. Students should have Python installed on their laptop
  (from the Pre-Class) and be comfortable running a script from a terminal. All three prior circuits
  stay on the breadboard, powered but unused, all Class — except the Class 3 buck converter, which
  keeps actively supplying the Pico's own `VSYS` power all Class — nothing from Class 1, 2, or 3 is
  touched or rewired today. The Class 3 rover status website (`rover_server.py`) and the Pico's own
  WiFi network it broadcasts (access point mode) must still be working — a quick spot-check, not a
  rebuild.

---

## 1. Class Overview

This is the fourth Class of the course and the second of Phase 2 (Outputs & Motion). Class 3 ended
with an open question: the car can move, but it has no way to know whether it actually went where it
was told. Today's Class introduces the LSM9DS1 9-DOF IMU as a first attempt at an answer — a sensor
that reports orientation (which way the car is pointed) rather than distance or position. Students
wire the IMU over I2C, read raw accelerometer and gyroscope values, and then fuse those two noisy,
individually-flawed signals into a single stable roll/pitch/yaw orientation using a Mahony filter —
streaming that orientation — as three separate values, roll, pitch, and yaw — to a live 3D box
rendered on their laptop, so they can watch their physical tilt reflected on screen in real time.
Watching that box also exposes the gyroscope's built-in error (its *bias*): left flat and untouched,
yaw slowly spins away, because the accelerometer can correct roll and pitch but has no way to sense
heading. Students fix most of that drift by measuring the bias at startup and refining it whenever
the board sits still. The same `roll`/`pitch`/`yaw` values are also posted into the Class 3 rover status website —
`rover_server.py`'s `/data.json` route grows three new flat keys, `roll`, `pitch`, and `yaw`,
alongside the wheel-speed/direction fields already there, so a laptop browser can show both
sensors' data together with no new website built. Note that the two halves of today's build —
`class-4-phase-3-code.py`'s IMU-streaming code (with `wireframe.py`'s 3D viewer on the laptop) and
`class-4-phase-4-rover_server.py`'s extended `rover_server.py` website — cannot run on the Pico at the same time: each ends in its own blocking
`while True:` loop, and a single Pico can only run one `code.py` at a time. Students run one or the
other, not both simultaneously, to satisfy today's milestone; a real refactor that lets both run
together doesn't happen until Class 5. The Class closes by pushing back on the excitement:
orientation alone still doesn't solve Class 3's square/circle problem, because knowing which way
you're pointed isn't the same as knowing how far you've traveled — a gap the students name
explicitly before Class 5 combines everything into the Random Rover.

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
* Explain what gyroscope *bias* is and why the accelerometer can't correct it on yaw, then reduce
  yaw drift by measuring the bias at startup and refining it whenever the board sits still
* Extend the Class 3 rover status website (`rover_server.py`) with three new fields, `roll`,
  `pitch`, and `yaw`, on the same `/data.json` route, so wheel speed/direction and orientation are
  both visible on one webpage
* Identify what information is still missing to fully solve Class 3's square/circle challenge, even
  with working orientation data

## 3. Preparation Checklist

* **1-2 days before:** Confirm every student's Class 1, 2, and 3 circuits are still intact and
  power up — a quick visual/serial spot-check, not a rebuild. (~15 min)
* **1-2 days before:** Confirm every student's `rover_server.py` from Class 3 still broadcasts its
  own WiFi network (access point mode, each student's own unique network name from
  `settings.toml`) and serves `/data.json` once a laptop joins it — nothing new to set up here this
  Class, just confirm it still works, since today's website change is a small edit to this same
  file. (~10 min)
* **1-2 days before:** Verify `adafruit_lsm9ds1` is present in each student's Library Bundle folder;
  have a few copies on a USB stick as backup. (~10 min)
* **1-2 days before:** Confirm every student laptop can run `pip install pyserial matplotlib numpy`
  successfully — test on a spare laptop or ask students to pre-install before Class if possible, since
  this is the first Class requiring a Python install on the laptop side rather than just an editor.
  (~15 min)
* **Day of, before students arrive:**
* Set out one LSM9DS1 9-DOF breakout board and a STEMMA QT/Qwiic to male-header cable (or Dupont jumpers if not
        using STEMMA QT) at each workstation, alongside continued access to the existing breadboard.
* Pre-build one reference circuit at the instructor bench and test `class-4-phase-1-code.py`
        (on the Pico) together with `wireframe.py` (on a laptop) end-to-end, confirming the 3D box
        responds correctly to physical tilting in all three axes, and that the red `Front` label
        sits on the board's +X end. Note how many degrees yaw drifts in one minute with the board
        sitting still. (~25 min)
* Then load `class-4-phase-3-code.py` (board lying still at boot) and confirm the serial console
        prints a `Gyro bias (deg/s): ...` line and that yaw now holds within about a degree over a
        minute — this before/after comparison is Step 3's payoff, so know your numbers. (~10 min)
* Also test `class-4-phase-4-rover_server.py`'s edit to `rover_server.py` end-to-end: load it on
        the reference Pico, confirm the same laptop browser that showed wheel speed/direction in Class 3 now also
        shows `roll`, `pitch`, and `yaw` fields on `/data.json` and the webpage. (~10 min)
* Note which serial port `wireframe.py` needs (e.g. `COM5`) on the instructor's machine so
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
| 9V battery, clip, and 5V buck converter (from Class 3) | Powers the Pico's logic (via `VSYS`) all Class — carried forward unwired from Class 3, no new wiring today |
| IMU: LSM9DS1 9-DOF Breakout Board (STEMMA) | Measures acceleration and rotation rate; fused into orientation |
| STEMMA QT/Qwiic to male-header cable | I2C connection between the Pico and the IMU |
| Breadboard (830-point, from Class 1) | Circuit assembly surface — Classes 1-3 circuits stay on it, untouched |
| Dupont jumper wires (shared) | Point-to-point wiring, if not using STEMMA QT directly |
| USB cable (student-supplied, from Pre-Class) | Power + serial connection to laptop |
| Windows 11 laptop with Mu or Thonny (student-supplied) | Edit and run CircuitPython code |
| Windows 11 laptop with Python 3 installed (student-supplied) | Runs `wireframe.py` to display the live 3D box |
| (no classroom WiFi needed) | The Pico 2 W broadcasts its own network (access point mode) for the rover status website, as set up in Class 3; nothing new to set up |
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
accelerometer's short-term noise. `class-4-phase-1-code.py` uses a Mahony filter for this — mention that
Kalman and Madgwick filters solve the same problem with different math, but Mahony is what's actually
implemented here. Ask: "If you only trusted the gyroscope forever, what would happen to your
orientation estimate after ten minutes of sitting still?" (It would slowly drift away from level,
even though nothing moved — pure integration error.)

Then plant the seed for Step 3: most of that gyro error is a small constant offset called *bias* —
the gyro reads a little rotation even when perfectly still (0.5°/s of bias is a 30° error after one
minute). The filter corrects it on roll and pitch because the accelerometer knows which way is
*down*. Ask: "If you spin the board flat on the table, does 'down' change?" (No — so the
accelerometer has no opinion about yaw, and nothing corrects yaw's drift. Students will see this
live in Step 2 and fix most of it in Step 3.)

**Concept 4 — What orientation still doesn't tell you.**
Roll/pitch/yaw tells you which way something is pointed, right now — nothing about how far it has
traveled or where it is. Ask: "Would knowing your car's exact heading, every instant, have been
enough to nail the Class 3 square?" Draw out: heading alone still leaves distance unmeasured — you'd
know you turned exactly 90 degrees, but not how far you drove before or after that turn. Recall Class
3's wheel odometry: it tells you how fast each wheel is spinning, but nothing about which way the car
is pointed — the two sensors solve two different halves of the problem, and neither alone solves it.
That's exactly why today's orientation data is being added to the *same* rover status website Class 3
built, rather than a separate display — so a viewer can see wheel speed and heading side by side and
judge for themselves whether that's enough to explain a square/circle attempt (it isn't quite —
distance/position traveled is still unmeasured). This sets up the "what's still missing?" discussion
at Closing.

### 5d. Guided Practice — ~50 min

**Pacing note:** Four steps fit in 50 min because Steps 3 and 4 are brisk, small edits to code
students already have working (Step 1's `code.py` and Class 3's `rover_server.py`), not new builds.
If a group is running behind, Step 4 is the first thing to shorten — have those students paste in
the finished `class-4-phase-4-rover_server.py` instead of walking every line — then Step 3 (paste
`class-4-phase-3-code.py` and just compare the drift before/after).

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
Load `class-4-phase-1-code.py` (save as `code.py`) onto the Pico. Reads accelerometer and
gyroscope data over I2C, fuses it with a Mahony filter, and prints `roll,pitch,yaw` CSV lines.
Note that the Adafruit library already returns gyro readings in radians/sec — exactly what the
filter expects — so no conversion is needed (converting again shrinks every rotation ~57x and
leaves yaw almost frozen).

```python
# class-4-phase-1-code.py -- save as code.py
# Phase 1: LSM9DS1 over I2C -- reads accel+gyro, fuses with a Mahony filter,
# prints roll,pitch,yaw as a CSV line every loop.

import time
import math
import board
import busio
import adafruit_lsm9ds1

# busio.I2C takes (SCL, SDA) in that order -- easy to get backwards.
i2c = busio.I2C(board.GP1, board.GP0)
sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

# Mahony filter tunable gains.
MAHONY_KP = 2.0   # proportional gain -- raise/lower live to see the drift-vs-jitter tradeoff
MAHONY_KI = 0.05  # integral gain -- corrects long-term gyro bias

# Orientation is tracked internally as a quaternion (q0,q1,q2,q3),
# a compact way to represent 3D rotation without the "gimbal lock"
# problems plain roll/pitch/yaw math can run into. Starts level.
q0, q1, q2, q3 = 1.0, 0.0, 0.0, 0.0
integral_fbx = integral_fby = integral_fbz = 0.0
last_time = time.monotonic()


def mahony_update(ax, ay, az, gx, gy, gz, dt):
    """One step of the Mahony filter: blend accelerometer + gyro into the quaternion."""
    global q0, q1, q2, q3, integral_fbx, integral_fby, integral_fbz

    # Normalize the accelerometer reading to a unit vector -- we only
    # care about its DIRECTION (which way is "down"), not its magnitude.
    norm = (ax * ax + ay * ay + az * az) ** 0.5
    if norm == 0:
        return
    ax, ay, az = ax / norm, ay / norm, az / norm

    # Where the filter currently THINKS gravity points, based on the
    # quaternion's running orientation estimate.
    vx = 2 * (q1 * q3 - q0 * q2)
    vy = 2 * (q0 * q1 + q2 * q3)
    vz = q0 * q0 - q1 * q1 - q2 * q2 + q3 * q3

    # Error between where the accelerometer says "down" is and where
    # the filter currently thinks it is -- this error is what corrects drift.
    ex = ay * vz - az * vy
    ey = az * vx - ax * vz
    ez = ax * vy - ay * vx

    # Integral term: accumulates error over time to correct steady gyro bias.
    integral_fbx += MAHONY_KI * ex * dt
    integral_fby += MAHONY_KI * ey * dt
    integral_fbz += MAHONY_KI * ez * dt

    # Nudge the raw gyro rates using both the proportional and integral
    # correction before integrating them into the quaternion.
    gx += MAHONY_KP * ex + integral_fbx
    gy += MAHONY_KP * ey + integral_fby
    gz += MAHONY_KP * ez + integral_fbz

    # Integrate the corrected rotation rate into the quaternion.
    qa, qb, qc = q0, q1, q2
    q0 += (-qb * gx - qc * gy - q3 * gz) * 0.5 * dt
    q1 += (qa * gx + qc * gz - q3 * gy) * 0.5 * dt
    q2 += (qa * gy - qb * gz + q3 * gx) * 0.5 * dt
    q3 += (qa * gz + qb * gy - qc * gx) * 0.5 * dt

    # Renormalize so the quaternion stays a valid rotation (unit length).
    norm = (q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3) ** 0.5
    q0, q1, q2, q3 = q0 / norm, q1 / norm, q2 / norm, q3 / norm


def quaternion_to_euler():
    """Convert the internal quaternion into the more familiar roll/pitch/yaw degrees."""
    roll = math.degrees(math.atan2(2 * (q0 * q1 + q2 * q3), 1 - 2 * (q1 * q1 + q2 * q2)))
    pitch = math.degrees(math.asin(max(-1.0, min(1.0, 2 * (q0 * q2 - q3 * q1)))))
    yaw = math.degrees(math.atan2(2 * (q0 * q3 + q1 * q2), 1 - 2 * (q2 * q2 + q3 * q3)))
    return roll, pitch, yaw


print("Class 4, Phase 1 -- IMU orientation streaming starting...")

while True:
    now = time.monotonic()
    dt = now - last_time
    last_time = now

    ax, ay, az = sensor.acceleration
    # The library already returns radians/sec -- exactly what the filter math
    # above expects, so no conversion needed (converting again would shrink
    # every rotation ~57x and leave yaw barely moving).
    gx, gy, gz = sensor.gyro

    mahony_update(ax, ay, az, gx, gy, gz, dt)
    roll, pitch, yaw = quaternion_to_euler()
    print(" {:.1f}, {:.1f}, {:.1f}".format(roll, pitch, yaw))

    time.sleep(0.02)
```

**What to watch for:** A flat line of `0.0,0.0,0.0` (or no output at all) almost always means the I2C
wiring is wrong, not the filter math — check `SDA`/`SCL` before touching `MAHONY_KP`/`MAHONY_KI`.

**Checkpoint 2:** Every pair should see three changing numbers scroll by that respond sensibly when
the board is tilted by hand — roll and pitch changing with tilt, yaw following flat turns but
also drifting slowly on its own. Have them keep an eye on that drift: Step 3 fixes it.

**Step 2 — live 3D visualization on the laptop.**
On the laptop (not the Pico), install dependencies once: `pip install pyserial matplotlib numpy`.
Save `class-4-phase-2-wireframe.py` as `wireframe.py` and run `python wireframe.py <port>`,
substituting the student's actual serial port (e.g. `COM5` on Windows — visible in Mu's/Thonny's
device list or Device Manager — or `/dev/ttyACM0` on Linux). The script draws only the newest line
the Pico sent, so the box never falls behind the board; it labels the plot axes X/Y/Z with the
rotation around each, marks the box's `Front` (+X end) and `Right` (−Y side) faces in red, and
negates roll so the box rolls the same way as the physical board.

```python
# class-4-phase-2-wireframe.py -- save as wireframe.py on laptop and execute there, not the pico mcu
# Phase 2: runs on your LAPTOP, not the Pico. Reads roll,pitch,yaw CSV over
# serial from class-4-phase-1-code.py or class-4-phase-3-code.py and draws a live-updating 3D box.
# Windows usage: python wireframe.py <port>     (e.g. python wireframe.py COM5)
# Linux usage:   python wireframe.py <device>   (e.g. python wireframe.py /dev/ttyACM0)

import sys
import serial
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 -- needed to enable 3D projection

# Pass your board's serial port as a command-line argument, e.g. COM5.
# Find it in Mu/Thonny's device list or Windows Device Manager.
PORT = sys.argv[1] if len(sys.argv) > 1 else "COM5"
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=1)

# The 8 corners of a simple rectangular box, and which corners connect
# to which to draw its 12 edges.
box_vertices = np.array([
    [-1, -0.5, -0.2], [1, -0.5, -0.2], [1, 0.5, -0.2], [-1, 0.5, -0.2],
    [-1, -0.5, 0.2], [1, -0.5, 0.2], [1, 0.5, 0.2], [-1, 0.5, 0.2],
])
edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4),
         (0, 4), (1, 5), (2, 6), (3, 7)]

# The 4 corners of the small +X end of the box -- the "front", pointing
# along the IMU's X (roll) axis.
FRONT_FACE = [1, 2, 6, 5]

# The 4 corners of the -Y long side. With X pointing forward and Z up,
# +Y points LEFT (right-hand rule), so -Y is the box's "right" side.
RIGHT_FACE = [0, 1, 5, 4]


def rotation_matrix(roll, pitch, yaw):
    """Build a combined 3D rotation matrix from roll/pitch/yaw degrees."""
    # Roll is negated so the on-screen box rolls the same way as the physical
    # board (display-only fix -- the Pico's roll value itself is unchanged).
    r, p, y = np.radians([-roll, pitch, yaw])
    rx = np.array([[1, 0, 0], [0, np.cos(r), -np.sin(r)], [0, np.sin(r), np.cos(r)]])
    ry = np.array([[np.cos(p), 0, np.sin(p)], [0, 1, 0], [-np.sin(p), 0, np.cos(p)]])
    rz = np.array([[np.cos(y), -np.sin(y), 0], [np.sin(y), np.cos(y), 0], [0, 0, 1]])
    return rz @ ry @ rx


plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(-2, 2)

# Label each plot axis with the IMU axis it stands for, and the rotation
# measured around it: roll spins around X, pitch around Y, yaw around Z.
ax.set_xlabel("X  (roll axis)")
ax.set_ylabel("Y  (pitch axis)")
ax.set_zlabel("Z  (yaw axis)")

# Create the 12 edge lines ONCE, then just move them every frame -- much
# faster than clearing the plot and drawing brand-new lines each time.
edge_lines = [ax.plot([], [], [], color="C0")[0] for _ in edges]

# Red "Front" and "Right" labels, created once and moved to the center of
# their faces every frame so you can always tell which way the box is facing.
front_label = ax.text(0, 0, 0, "Front", color="red", ha="center", va="center")
right_label = ax.text(0, 0, 0, "Right", color="red", ha="center", va="center")
plt.show(block=False)

print("Class 4, Phase 2 -- 3D box display starting, reading from", PORT)

while True:
    # The Pico sends lines faster than we can draw them. Read everything
    # already waiting and keep only the NEWEST line, so the box shows where
    # the board is now -- not where it was several seconds ago.
    raw = ser.readline()
    while ser.in_waiting:
        raw = ser.readline()
    line = raw.decode("utf-8", errors="ignore").strip()
    if not line:
        continue
    try:
        roll, pitch, yaw = [float(v) for v in line.split(",")]
    except ValueError:
        # Skip any partial/garbled line rather than crashing the display.
        continue

    rotated = box_vertices @ rotation_matrix(roll, pitch, yaw).T

    for edge_line, (a, b) in zip(edge_lines, edges):
        pts = rotated[[a, b]]
        edge_line.set_data_3d(pts[:, 0], pts[:, 1], pts[:, 2])
    front_label.set_position_3d(rotated[FRONT_FACE].mean(axis=0))
    right_label.set_position_3d(rotated[RIGHT_FACE].mean(axis=0))
    ax.set_title("roll={:.0f} pitch={:.0f} yaw={:.0f}".format(roll, pitch, yaw))
    # Redraw the window and let it handle events (resize, close, etc.).
    fig.canvas.draw_idle()
    fig.canvas.flush_events()
```

**What to watch for:** A "port not found" or permission error usually means either the wrong `PORT`
was passed, or Mu/Thonny's serial console is still connected to that same port and needs to be
closed first — only one program can hold a serial port open at a time.

**Before students start tilting:** have each pair find their board's +X end — the axis arrows
printed on the IMU breakout, or the dip test (hold flat, dip one short end down: if the on-screen
`Front` end dips too, that's +X) — and mark it with tape or marker so physical and on-screen
orientation line up.

**What "done" looks like for this segment:** Tilting the physical board visibly and correctly tilts
the on-screen 3D box in the matching direction, in real time. Then have each pair leave the board
flat and untouched for one minute and write down how many degrees yaw drifted — that number is the
"before" for Step 3.

**Step 3 — stop the yaw drift: gyro bias calibration.**
Replace the Pico's `code.py` with `class-4-phase-3-code.py` — Step 1's program plus three
additions. At startup, `calibrate_gyro_bias()` averages about 2 seconds of gyro readings while the
board sits still; since nothing is rotating, that average *is* the bias, and it's subtracted from
every reading afterward. While running, `is_still()` checks whether the board looks motionless
(every gyro axis near zero *and* the accelerometer measuring just 1 g); if so, whatever the gyro
still reads is leftover bias, so the code nudges its bias estimate 1% toward it — tracking the slow
change as the chip warms up. One subtle detail worth pointing out: the loop's clock (`last_time`)
starts *after* calibration, or the first loop would integrate a bogus 2-second rotation. The CSV
output is unchanged, so `wireframe.py` keeps working with no edits.

```python
# class-4-phase-3-code.py -- save as code.py (replaces Phase 1's code.py)
# Phase 3: Phase 1's IMU + Mahony filter, plus gyro bias calibration:
#   1. at startup, measure the gyro's bias while the board sits still
#   2. while running, keep refining that bias whenever the board is still
# Still prints roll,pitch,yaw as CSV, so Phase 2's wireframe.py works unchanged.

import time
import math
import board
import busio
import adafruit_lsm9ds1

# busio.I2C takes (SCL, SDA) in that order -- easy to get backwards.
i2c = busio.I2C(board.GP1, board.GP0)
sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

# Mahony filter tunable gains (same as Phase 1).
MAHONY_KP = 2.0   # proportional gain -- drift-vs-jitter tradeoff
MAHONY_KI = 0.05  # integral gain -- corrects long-term gyro bias, but only on roll/pitch

# Gyro bias settings -- NEW in Phase 3.
CAL_SAMPLES = 200  # startup calibration: 200 readings x 10 ms = about 2 seconds
STILL_GYRO = 0.02  # rad/s (about 1 deg/s): below this on EVERY axis counts as "still"
STILL_ACCEL = 0.3  # m/s^2: total acceleration this close to 1 g counts as "still"
BIAS_ALPHA = 0.01  # while still, move the bias 1% of the way toward each new reading
GRAVITY = 9.81     # m/s^2 -- what the accelerometer reads when only gravity acts on it

q0, q1, q2, q3 = 1.0, 0.0, 0.0, 0.0
integral_fbx = integral_fby = integral_fbz = 0.0


def mahony_update(ax, ay, az, gx, gy, gz, dt):
    """Unchanged from Phase 1 -- see Phase 1's code for line-by-line comments."""
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


def quaternion_to_euler():
    """Unchanged from Phase 1: the quaternion as roll/pitch/yaw degrees."""
    roll = math.degrees(math.atan2(2 * (q0 * q1 + q2 * q3), 1 - 2 * (q1 * q1 + q2 * q2)))
    pitch = math.degrees(math.asin(max(-1.0, min(1.0, 2 * (q0 * q2 - q3 * q1)))))
    yaw = math.degrees(math.atan2(2 * (q0 * q3 + q1 * q2), 1 - 2 * (q2 * q2 + q3 * q3)))
    return roll, pitch, yaw


def calibrate_gyro_bias():
    """Average the gyro while the board sits still -- that average IS the bias."""
    print("Calibrating gyro -- keep the board perfectly still...")
    sum_x = sum_y = sum_z = 0.0
    for _ in range(CAL_SAMPLES):
        gx, gy, gz = sensor.gyro  # already radians/sec
        sum_x += gx
        sum_y += gy
        sum_z += gz
        time.sleep(0.01)
    return sum_x / CAL_SAMPLES, sum_y / CAL_SAMPLES, sum_z / CAL_SAMPLES


def is_still(ax, ay, az, gx, gy, gz):
    """True if the board looks motionless: almost no rotation on any axis,
    AND the accelerometer feels only gravity (no pushes or bumps)."""
    accel_mag = (ax * ax + ay * ay + az * az) ** 0.5
    return (
        abs(gx) < STILL_GYRO
        and abs(gy) < STILL_GYRO
        and abs(gz) < STILL_GYRO
        and abs(accel_mag - GRAVITY) < STILL_ACCEL
    )


print("Class 4, Phase 3 -- IMU orientation streaming with gyro bias calibration")
bias_x, bias_y, bias_z = calibrate_gyro_bias()
# No commas in this line, so wireframe.py skips it instead of trying to draw it.
print("Gyro bias (deg/s): x={:.2f} y={:.2f} z={:.2f}".format(
    math.degrees(bias_x), math.degrees(bias_y), math.degrees(bias_z)))

# Start the clock AFTER calibrating -- otherwise the first loop would see a
# 2-second dt and integrate a huge, bogus rotation.
last_time = time.monotonic()

while True:
    now = time.monotonic()
    dt = now - last_time
    last_time = now

    ax, ay, az = sensor.acceleration
    gx, gy, gz = sensor.gyro  # already radians/sec

    # Part 1: subtract the bias, so a still board reads (almost) zero rotation.
    gx, gy, gz = gx - bias_x, gy - bias_y, gz - bias_z

    # Part 2: if the board is still, whatever the gyro STILL reads is leftover
    # bias, not motion -- nudge the bias estimate a little toward it. This
    # tracks the slow bias change as the chip warms up.
    if is_still(ax, ay, az, gx, gy, gz):
        bias_x += BIAS_ALPHA * gx
        bias_y += BIAS_ALPHA * gy
        bias_z += BIAS_ALPHA * gz

    mahony_update(ax, ay, az, gx, gy, gz, dt)
    roll, pitch, yaw = quaternion_to_euler()
    print("{:.1f},{:.1f},{:.1f}".format(roll, pitch, yaw))

    time.sleep(0.02)
```

**What to watch for:** The board must lie still while it boots — if yaw drifts badly from the very
start, it moved during calibration; press reset with the board lying flat. Tradeoff to mention: a
turn slower than `STILL_GYRO` (~1°/s) looks exactly like bias and gets absorbed instead of
measured — fine for a car, which turns far faster. And calibration slows drift, it doesn't
eliminate it; only the magnetometer (a compass) gives an absolute heading — a stretch goal, not
today's work.

**Checkpoint 3:** With the board flat and untouched for one minute, yaw should now hold within about
a degree, versus the Step 2 "before" number. Every pair should be able to say in one sentence why
the accelerometer can correct roll and pitch but not yaw.

**Step 4 — extend the rover status website with orientation.**
This step replaces `code.py` with a different file — `class-4-phase-4-rover_server.py` saved over
`rover_server.py` — not something that runs alongside Step 3's `class-4-phase-3-code.py`. Both scripts
end in their own blocking `while True:` loop, and a Pico only runs one `code.py` at a time, so tell
students plainly: pick one or the other for this step, don't try to run both together. Recall
`rover_server.py`'s `/data.json` route from Class 3: it returns a small dict —
`speed_left_cms`, `dir_left`, `speed_right_cms`, `dir_right` — and the webpage just calls
`JSON.stringify()` on whatever that dict contains, so it already displays any field the dict has,
with no HTML/JavaScript changes needed. Today's edit only touches the Pico side: add the same
sensor-read-and-fuse code from `class-4-phase-3-code.py` (gyro bias calibration included) into
`rover_server.py`, and add three keys to the returned dict. Load `class-4-phase-4-rover_server.py`
and save it over the existing `rover_server.py`. It calibrates the gyro at boot just like Step 3,
so the rover must sit still for those 2 seconds.

```python
# class-4-phase-4-rover_server.py - save over rover_server.py
# Extends the Class 3 rover status website with IMU orientation. Same server,
# same /data.json route -- just three new keys. Reuses the Mahony filter code
# from class-4-phase-3-code.py rather than reinventing it (but as a copy, not an
# import -- see "What this code does" above for why).
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

wifi.radio.start_ap(
    os.getenv("CIRCUITPY_WIFI_AP_SSID"), os.getenv("CIRCUITPY_WIFI_AP_PASSWORD")
)
print("rover server -- broadcasting WiFi network:", os.getenv("CIRCUITPY_WIFI_AP_SSID"))
print("rover server -- listening at", wifi.radio.ipv4_address_ap)

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool)

i2c = busio.I2C(board.GP1, board.GP0)  # SCL, SDA -- same wiring as class-4-phase-3-code.py
imu = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

MAHONY_KP = 2.0  # calibrate: same tuned value as class-4-phase-3-code.py
MAHONY_KI = 0.05  # calibrate: same tuned value as class-4-phase-3-code.py

# Gyro bias settings -- same values and meaning as class-4-phase-3-code.py.
CAL_SAMPLES = 200  # startup calibration: about 2 seconds of readings
STILL_GYRO = 0.02  # rad/s: below this on every axis counts as "still"
STILL_ACCEL = 0.3  # m/s^2: total acceleration this close to 1 g counts as "still"
BIAS_ALPHA = 0.01  # while still, move the bias 1% of the way toward each reading
GRAVITY = 9.81     # m/s^2

q0, q1, q2, q3 = 1.0, 0.0, 0.0, 0.0
integral_fbx = integral_fby = integral_fbz = 0.0
last_time = time.monotonic()


def _mahony_update(ax, ay, az, gx, gy, gz, dt):
    # Identical math to class-4-phase-3-code.py's mahony_update() -- see Direct
    # Teaching Concept 3 for why fusing accel+gyro this way works.
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


def _calibrate_gyro_bias():
    """Same as class-4-phase-3-code.py: average the gyro while the rover sits still."""
    print("Calibrating gyro -- keep the rover perfectly still...")
    sum_x = sum_y = sum_z = 0.0
    for _ in range(CAL_SAMPLES):
        gx, gy, gz = imu.gyro  # already radians/sec
        sum_x += gx
        sum_y += gy
        sum_z += gz
        time.sleep(0.01)
    return sum_x / CAL_SAMPLES, sum_y / CAL_SAMPLES, sum_z / CAL_SAMPLES


def _is_still(ax, ay, az, gx, gy, gz):
    """Same as class-4-phase-3-code.py: tiny rotation AND only gravity on the accelerometer."""
    accel_mag = (ax * ax + ay * ay + az * az) ** 0.5
    return (
        abs(gx) < STILL_GYRO
        and abs(gy) < STILL_GYRO
        and abs(gz) < STILL_GYRO
        and abs(accel_mag - GRAVITY) < STILL_ACCEL
    )


def _read_orientation():
    """Advance the Mahony filter one step and return (roll, pitch, yaw)."""
    global last_time, bias_x, bias_y, bias_z
    now = time.monotonic()
    dt = now - last_time
    last_time = now
    ax, ay, az = imu.acceleration
    gx, gy, gz = imu.gyro  # already radians/sec
    gx, gy, gz = gx - bias_x, gy - bias_y, gz - bias_z  # remove the gyro bias
    if _is_still(ax, ay, az, gx, gy, gz):  # still: leftover reading is bias -- refine it
        bias_x += BIAS_ALPHA * gx
        bias_y += BIAS_ALPHA * gy
        bias_z += BIAS_ALPHA * gz
    _mahony_update(ax, ay, az, gx, gy, gz, dt)
    roll = math.degrees(math.atan2(2 * (q0 * q1 + q2 * q3), 1 - 2 * (q1 * q1 + q2 * q2)))
    pitch = math.degrees(math.asin(max(-1.0, min(1.0, 2 * (q0 * q2 - q3 * q1)))))
    yaw = math.degrees(math.atan2(2 * (q0 * q3 + q1 * q2), 1 - 2 * (q2 * q2 + q3 * q3)))
    return roll, pitch, yaw


# Measure the gyro bias once at startup (the rover must sit still while it
# boots), then start the filter's clock so the first dt isn't the 2 s wait.
bias_x, bias_y, bias_z = _calibrate_gyro_bias()
last_time = time.monotonic()


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
    roll, pitch, yaw = _read_orientation()  # the only new work this route does
    return JSONResponse(request, {
        "speed_left_cms": speed_left,
        "dir_left": dir_left,
        "speed_right_cms": speed_right,
        "dir_right": dir_right,
        "roll": roll,
        "pitch": pitch,
        "yaw": yaw,
    })


@server.route("/")
def index(request: Request):
    return Response(request, STATUS_PAGE, content_type="text/html")


server.start(str(wifi.radio.ipv4_address_ap), port=80)

print("Class 4, Phase 4 -- rover status website now serving orientation too...")
while True:
    server.poll()
```

**What to watch for:** If `roll`/`pitch`/`yaw` show up as `0.0` and never change on the webpage, this
is the same symptom as Step 1's flat-line output — check `SDA`/`SCL` wiring first, not the server
code. If the webpage doesn't pick up the new fields at all, confirm the browser actually reloaded
`rover_server.py`'s new version and not a cached page.

**Checkpoint 4:** Every pair should be able to join their Pico's own WiFi network (same network name
and password as Class 3 — `settings.toml` carries over unchanged), open its status webpage, and see all seven
fields — `speed_left_cms`, `dir_left`, `speed_right_cms`, `dir_right`, `roll`, `pitch`, `yaw` — update
live, with wheel speed responding to driving and orientation responding to tilting the board by hand.

**What "done" looks like for this segment:** The same webpage students used in Class 3 now shows
orientation alongside wheel speed/direction, with no separate page or server — one browser tab, one
set of live numbers.

### 5e. Independent Work — ~30 min

**What to do:** Students (in pairs where possible) experiment with the live display, then run the
`MAHONY_KP` tuning exercise: raise it in a few steps and describe what happens (faster response, more
jitter), then lower it below the default and describe what happens (smoother, but slower to correct
drift). Capture before/after observations in the build journal. Faster pairs can:

* Try physically shaking the board gently while watching the display, to see the fused output stay
  far steadier than a raw-accelerometer-only version would.
* Mount the IMU off to one side of a straight edge (like a ruler) versus centered, spin it around a
  fixed pivot point, and discuss whether the readings differ — connects to the Talking Points
  question about mounting position and turning.
* Drive the car a short distance with a partner watching the rover status website (not the laptop
  3D box) and describe out loud what wheel speed and orientation *together* tell you that either one
  alone wouldn't — and what they still can't tell you (distance/position traveled).
* Continue assembling the Emo Smart Robot Car Chassis Kit if the orientation milestone is working.

**What to watch for:** The most common failure at this stage is a 3D box that turns backwards or on
the wrong axis. First check that the board's +X end is where the red `Front` label is — a board held
end-for-end makes every tilt look reversed. If one motion is still backwards after that, negate just
that angle in `wireframe.py`'s `rotation_matrix()` the same way roll already is — a display fix, not
a filter bug.

**Time check:** At the 20-minute mark, do a quick show-of-hands: "Who has a live 3D box responding
correctly to tilt?" Redirect instructor attention to pairs still stuck.

### 5f. Closing / Wrap-up — ~10 min

**What to do:** Ask 2-3 volunteers to demo their live 3D box responding to physical tilts, then pull
up the same student's rover status website on the projector and show wheel speed/direction and
orientation updating together on one page. Then run the "does this solve Class 3's problem?"
discussion: ask the group directly whether orientation data alone — or orientation plus wheel speed,
now sitting side by side on the same website — would have gotten their square and circle attempts
closer to 35 cm, and why or why not.

**What to say:** "You now have a car that can move, a sensor that knows which way it's pointed, and
one website that shows both at once. That's real progress — but notice neither one, alone or
together, tells you *how far* you've gone or where you actually are. That gap is exactly why Class 5
doesn't use the IMU or dead-reckoning distance at all — it solves navigation a completely different
way, using the sensor and servo you built back in Class 2."

**Preview next Class:** Class 5 reuses no new pins — it reconnects exactly the Class 2 sensor+servo
circuit (`GP6`-`GP8`) and the Class 3 motor driver circuit (`GP9`-`GP12`, with the wheel optocouplers on `GP19`/`GP17`) as they were
left wired, combining them into the Random Rover's collision-avoidance behavior. Today's IMU circuit
and Class 1's button/encoder circuit both stay untouched on the breadboard. The rover status website
keeps growing too — Class 5 adds scan readings, chosen heading, and sensor-stop events to the same
`rover_server.py`, alongside the wheel-speed and orientation fields added in Classes 3 and 4. Point
students to the Class 5 references in the syllabus if they want to read ahead.

## 6. Troubleshooting Guide

| Problem | Likely Cause | Fix |
| :-------- | :------------- | :---- |
| No serial output at all from `class-4-phase-1-code.py` | `SDA`/`SCL` swapped, or I2C device not detected | Verify `SDA` on `GP0`, `SCL` on `GP1`; confirm power/ground |
| `roll,pitch,yaw` prints but never changes | Board isn't actually being moved, or a loose connection is producing a flat/stuck reading | Physically tilt the board while watching output; reseat the STEMMA QT cable if still stuck |
| Roll or pitch drifts noticeably even when the board sits still | `MAHONY_KI` too low, or `MAHONY_KP` too low to correct drift | Raise `MAHONY_KP`/`MAHONY_KI` in small steps and re-test |
| Yaw spins away steadily while the board sits still | Still running Step 1's code (no bias calibration), or the board moved during the 2 s startup calibration | Confirm `code.py` is `class-4-phase-3-code.py`; press reset with the board lying still |
| Yaw still creeps a degree or two over several minutes | Expected — calibration slows drift but can't remove it; only a magnetometer gives an absolute heading | Press reset (with the board still) to re-zero |
| Very slow turns barely register in yaw | A turn slower than `STILL_GYRO` looks like bias and gets absorbed into it | Lower `STILL_GYRO` (e.g. `0.01`) and re-test |
| Yaw barely moves at all when the board is turned flat | Gyro converted to radians twice (the library already returns rad/s) | Remove any `math.radians()` applied to `sensor.gyro`/`imu.gyro` |
| Orientation is jittery/noisy even when the board is still | `MAHONY_KP` too high | Lower `MAHONY_KP` in small steps and re-test |
| 3D box turns backwards or on the wrong axis | Board's +X end isn't where the `Front` label is, or one axis has a display sign mismatch | Line up +X with `Front` first; if one motion is still backwards, negate that angle in `rotation_matrix()` (roll already is) |
| `wireframe.py` can't open the serial port | Wrong `PORT` argument, or Mu/Thonny's serial console still has the port open | Close Mu/Thonny's serial console first; confirm the correct COM port in Device Manager |
| `ModuleNotFoundError` for `serial`, `matplotlib`, or `numpy` | Dependencies not installed on the laptop | Run `pip install pyserial matplotlib numpy` in the same Python environment used to run the script |
| `ImportError: no module named 'adafruit_lsm9ds1'` | Library not copied to `/lib` on CIRCUITPY drive | Copy the `adafruit_lsm9ds1.mpy` file from the Library Bundle into `/lib` |
| Rover status website's `roll`/`pitch`/`yaw` show `0.0` and never change | Same I2C wiring problem as `class-4-phase-1-code.py` — `SDA`/`SCL` swapped or not detected | Verify `SDA` on `GP0`, `SCL` on `GP1` before touching `rover_server.py`'s new code |
| Website loads but is missing `speed_left_cms`/`dir_left`/etc. from Class 3 | `class-4-phase-4-rover_server.py` was saved as a new file instead of over the existing `rover_server.py` | Confirm only one `rover_server.py` exists on CIRCUITPY and it's the Class 4 version with all seven fields |
| Website's orientation fields update, but wheel speed/direction stopped working | `wheel_odometry` import removed or wiring on `GP19`/`GP17` disturbed while adding today's IMU wiring | Confirm `import wheel_odometry` is still present and Class 3's optocoupler wiring wasn't bumped |

## 7. Age Differentiation Notes

**Younger students (12-14) and their parent/guardian:** Provide the pin table above pre-printed and
laminated at the workstation so it's a lookup, not a memorization task. Pair a younger student's
STEMMA QT/wiring work with the parent/guardian's help typing the `pip install` command and finding
the correct COM port in Windows. Start from `class-4-phase-1-code.py` and `wireframe.py` already
loaded as starting points, and have them focus on the `MAHONY_KP` tuning exercise (a guided,
observable experiment) rather than reading the quaternion math. For Step 3, the before/after drift
comparison is the lesson — they can paste in `class-4-phase-3-code.py` and just time a minute of
drift with each version. For Step 4, it's enough for them to save `class-4-phase-4-rover_server.py`
over `rover_server.py` and confirm the new fields show up on the webpage — treat the duplicated
Mahony math inside it as "trust the code you already saw work" material.

**Older students (15-18) and adults:** Walk them through the quaternion math in `mahony_update()`
line by line rather than treating it as a black box, and have them explain in their own words why
the filter blends a proportional correction (`MAHONY_KP`) with an integral correction (`MAHONY_KI`).
Once the milestone is met, challenge them to log roll/pitch/yaw to a file over a fixed time window
while the board sits still, and quantify residual drift numerically instead of just watching the
on-screen box. For Step 3, have them predict the yaw error after one minute from the printed bias
(degrees/sec × 60) before running Phase 1's code, then check the prediction — and experiment with
`STILL_GYRO` and `BIAS_ALPHA` to feel the slow-turn tradeoff. For Step 4, have them notice that
`class-4-phase-4-rover_server.py` duplicates rather than imports `class-4-phase-3-code.py`'s Mahony
and bias functions, and ask them to explain why (`class-4-phase-3-code.py` has its own
blocking `while True` print loop, which can't run at the same time as the server's own loop) — and,
if time allows, have them factor the shared math into a small importable module both files use
instead of a copy-paste duplicate.

## 8. Assessment

**Milestone Assignment (per syllabus, Phase 2 / Class 4):** Live 3D orientation display driven by the
IMU.

**What "complete" looks like:** The student can run `class-4-phase-3-code.py` on the Pico and
`wireframe.py` on their laptop simultaneously, and show the on-screen 3D box tilting to match the
physical board's roll, pitch, and yaw in real time — with yaw holding steady while the board sits
still. In addition, the student can open their
Pico's rover status website and point to live `roll`, `pitch`, and `yaw` readings updating
alongside the wheel speed/direction fields already there from Class 3.

**How to give feedback without scoring:** Ask the student to physically tilt the board along one
axis at a time and narrate which on-screen motion corresponds to which physical motion ("show me
roll, show me pitch, show me yaw") rather than checking a box. Separately, ask them to point at the
webpage and explain why adding orientation didn't require any change to the HTML/JavaScript — only
to the dict returned from `/data.json`. If a pair can't get the full 3D display working in the time
available, accepting a working `class-4-phase-1-code.py` with sensible serial output (without the laptop
visualization) is a reasonable partial milestone — have them bring the full display and the website
extension working to the start of Class 5 and note it in their build journal.

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
* A backwards or mirrored 3D box (Troubleshooting) is almost always a board held with its +X end
  away from the on-screen `Front` label — have pairs mark their +X end in Step 2 before anyone
  debugs code. `wireframe.py` already negates roll; any remaining single-axis flip is a one-sign
  display fix in `rotation_matrix()`, not a reason to stall the Independent Work block.
* Step 3's calibration only works if the board is lying still while it boots — say it out loud
  before every reset, and have students watch for the `Gyro bias (deg/s): ...` line in the serial
  console as proof the calibration ran.
* The "does this solve Class 3's problem?" discussion (Closing) should land as a genuine letdown
  followed by curiosity, not a gotcha — the point is that students feel the gap themselves before
  Class 5 explains how the course actually closes it (via the sensor/servo scan, not the IMU).
* Step 4's website edit is small on purpose — resist the urge to re-teach `adafruit_httpserver` or
  WiFi setup from scratch; if a pair never got the Class 3 website working, point them back to that
  Class's troubleshooting guide rather than debugging WiFi live during today's Guided Practice.

## 10. Resources & References

* [Python & CircuitPython — Adafruit LSM9DS1 9-DOF Breakout][01] — Adafruit's official guide for
  wiring and reading the LSM9DS1 over I2C in CircuitPython
* [API Reference — Adafruit LSM9DS1 Library][02] — the `adafruit_lsm9ds1` library API used in
  `class-4-phase-1-code.py` (note its `gyro` property already returns radians/sec)
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
