# Lesson Script: Class 4 — Inertial Measurement Unit (IMU)

* **Class:** 4 of 6 (plus Pre-Class)
* **Duration:** ~2 hours
* **What You'll Need:** see [Section 2](#2-what-youll-need)
* **Before You Start:** Your Class 1-3 circuits (button/encoder, sensor/servo sweep, motor driver)
    should still be working and stay exactly as they are on your breadboard — including the Class 3
    buck converter, which keeps powering your Pico's own `VSYS` all Class. You should also have
    Python 3 installed on your laptop from the Pre-Class — this class is the first one that runs
    code on your laptop as well as your Pico. Your Class 3 rover status website (`rover_server.py`)
    should still broadcast its own WiFi network and serve `/data.json` once your laptop joins it — a
    quick spot-check, not a rebuild, since today's website work is a small edit to that same file.

---

## 1. What This Project Is

Class 3 ended with a real gap: your car can move, but it has no way to know whether it actually
went where you told it to. Today you start closing that gap by giving your board a sense of
balance — the LSM9DS1 IMU (inertial measurement unit), which can tell you which way something is
pointed, the same way your inner ear tells you which way is up with your eyes closed.

You'll wire the IMU over I2C, read its raw acceleration and rotation-rate data, and then combine
("fuse") those two individually-flawed signals into one stable roll/pitch/yaw orientation using a
**Mahony filter**. You'll stream that orientation live from your Pico to a 3D box drawn on your
laptop screen, so you can watch your physical tilt reflected on screen in real time. Next you'll
teach the Pico to measure and cancel its gyroscope's built-in error (its *bias*), so the heading
stops wandering while the board sits still. Then you'll add that same orientation to your Class 3 rover status website — `rover_server.py`'s `/data.json`
route grows three new fields (`roll`, `pitch`, `yaw`) alongside the wheel speed/direction fields
already there, so one browser tab shows both sensors' data together with no new website built. By
the end, you'll also be able to say clearly why this — as exciting as it is — still doesn't solve
Class 3's square-and-circle problem on its own.

## 2. What You'll Need

| Component | Quantity | Purpose This Project |
| :---------- | :--------: | :---------------------- |
| Raspberry Pi Pico 2 W (with header) | 1 | Runs your CircuitPython code |
| 9V battery, clip, and 5V buck converter (from Class 3) | 1 each | Powers your Pico's logic (via `VSYS`) all Class — carried forward unchanged from Class 3, no new wiring today |
| LSM9DS1 9-DOF IMU breakout board (STEMMA) | 1 | Measures acceleration and rotation rate |
| STEMMA QT/Qwiic to male-header cable (or Dupont jumpers) | 1 | I2C connection between the Pico and the IMU |
| Breadboard (from Classes 1-3) | 1 | Your existing circuits stay on it, untouched |
| USB cable | 1 | Powers the Pico and carries the serial data |
| Laptop with Mu or Thonny | 1 | Where you write/save the Pico's code |
| Laptop with Python 3 + `pyserial`, `matplotlib`, `numpy` | 1 | Runs the 3D visualization script (this part runs on your laptop, not the Pico) |
| (none — Pico broadcasts its own WiFi network) | — | No classroom WiFi needed: the Class 3 rover status website runs on the network your Pico creates itself — nothing new to set up |

**Additional components for the Homework Assignments** (Section 11) — no homework has been written
for this class yet; this section will be filled in when that content is added.

## 3. Meet the Hardware

**LSM9DS1 9-DOF IMU.** "9-DOF" means nine degrees of freedom — this one breakout board actually
contains three separate sensors: an accelerometer, a gyroscope, and a magnetometer. Today you use
the first two. It connects to your Pico over **I2C**, a two-wire protocol (`SDA` for data, `SCL`
for clock) that lets multiple sensors share the same two pins — you'll see I2C again if you add
more sensors later, since devices on the same I2C bus don't need their own dedicated pin pair.

**Accelerometer.** Measures linear acceleration along three axes (x/y/z) — and it always includes
the constant downward pull of gravity. At rest, its reading points straight toward the floor,
which is exactly how it senses tilt: as the board rotates, gravity's component shifts between the
axes in a predictable way. Its weakness: it's *noisy* under vibration or sudden movement, since a
moving car constantly shakes it with forces that have nothing to do with tilt.

**Gyroscope.** Measures angular *rate* — how fast the board is rotating around each axis, in
degrees per second — not an absolute angle. Its weakness: small measurement errors accumulate
("integrate") over time into a growing drift, so a gyro-only orientation slowly wanders away from
the truth even if the board never actually moves. Most of that error is a small constant offset
called **bias** — the gyro reads a little rotation even when perfectly still. Phase 3 measures it
and subtracts it out.

**Mahony filter.** Neither sensor alone is good enough, so `class-4-phase-1-code.py` fuses both with a
Mahony filter: it trusts the gyroscope for fast, moment-to-moment changes, and continuously nudges
its estimate back toward what the accelerometer says over the longer term — correcting the gyro's
drift without inheriting the accelerometer's short-term noise. (Kalman and Madgwick filters solve
this same problem with different math; Mahony is what's actually implemented here.) The filter's
`MAHONY_KP` gain controls how strongly it trusts that correction — you'll tune this live and feel
the tradeoff between drift (too low) and jitter (too high).

**Adding to a website that's already running.** Building your Class 3 rover status website from
scratch meant standing up WiFi, an HTTP server, a route, and a page all at once. Adding to one that
already works is a much smaller job: the page already calls `JSON.stringify()` on whatever the
`/data.json` route hands it, so it already displays any field that dict contains — no HTML or
JavaScript changes needed at all. Today's edit only touches the Pico side of `rover_server.py`: read
and fuse the IMU the same way `class-4-phase-3-code.py` does, then add three new keys to the dict the
route already returns. That's the difference between building a website and growing one you already
built.

**Pinout summary** (Raspberry Pi Pico 2 W — new pins only; Classes 1-3 are unaffected):

| Pin | What we use it for |
| :----: | :-------------------- |
| `GP0` | LSM9DS1 `SDA` (I2C data) |
| `GP1` | LSM9DS1 `SCL` (I2C clock) |
| `3V3` | LSM9DS1 `VIN`/power |
| `GND` | LSM9DS1 `GND` |

## 4. Build It: Phase 1 — Read, Fuse, and Print Orientation (on the Pico)

### Wiring for this phase

This is the complete wiring for the whole project — Phases 2-4 add no new hardware, only new code
(Phase 2's runs on your laptop).
* [Raspberry Pi Pico 2w Pinout][20]
* [Adafruit 9-DOF IMU LSM9DS1 Pinout][21]
* [STEMMA 4-Pin I2C Connector Pinout][22]

| Component | STEMMA 4-Pin I2C Connector | Pico 2W Pin | Notes |
| :---------- | :----------------: | :-----------: | :------ |
| LSM9DS1 `SDA` | Blue for `SDA` | `GP0` | |
| LSM9DS1 `SCL` | Yellow for `SCL` | `GP1` | |
| LSM9DS1 `VIN` | Red for `VIN` | `3V3` | use the Pico's 3.3V output, the same logic level as `SDA`/`SCL` |
| LSM9DS1 `GND` | Black for `GND` | `GND` | make sure this is a common `GND` |

Your Class 1-3 circuits stay exactly where they are on the breadboard. Before writing any code,
trace this wiring out loud — especially confirm `SDA`/`SCL` aren't swapped, since I2C devices
commonly fail *silently* (no error, just no data at all) when they are.

### Software for this phase

A new `code.py` and one new library. Class 3's files (`motor_driver.py`, `wheel_odometry.py`, `rover_server.py`) stay on `CIRCUITPY` for Phase 4, but aren't used here.

| Software component | New, modified, or unchanged | What it does |
| :------------------- | :-------------------------- | :----------- |
| `code.py` | **New** — `class-4-phase-1-code.py` | Reads the accelerometer and gyroscope, fuses them with a Mahony filter into roll/pitch/yaw, and prints them as CSV lines about 50 times a second. |
| `adafruit_lsm9ds1.mpy` (in `/lib`) | **New** — copy from the Library Bundle | Driver for the LSM9DS1 IMU over I2C. Its `gyro` property already returns radians/sec. |

### What this code does

This program reads raw acceleration and rotation-rate values from the IMU, feeds them into a
Mahony filter (implemented as a running "quaternion" — a compact way to represent 3D rotation),
converts the result into the more intuitive roll/pitch/yaw angles, and prints them as a CSV line
every loop.

### The code

Save this as `code.py` on your `CIRCUITPY` drive.

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

### Try it / what you should see

You should see a stream of `roll, pitch, yaw` lines, updating fast (about 50 times a second). Tilt
the board by hand and watch roll and pitch change sensibly; yaw may drift slowly on its own even
without rotating the board flat — that's expected gyro drift on the axis the accelerometer can't
correct (it can't tell "which way is North," only "which way is down"). Keep an eye on how fast
it drifts — Phase 3 fixes most of it.

>**NOTE:** If you see a flat `0.0, 0.0, 0.0` (or nothing at all), that's almost always an I2C wiring problem,
>not a filter math problem — double-check `SDA`/`SCL` before touching `MAHONY_KP` or `MAHONY_KI`.

### Checkpoint

Confirm three changing numbers scroll by in the console, and that tilting the board by hand
produces sensible roll/pitch changes you can visually correlate to the motion you just made.

## 5. Build It: Phase 2 — Live 3D Visualization (on Your Laptop)

### Wiring for this phase

No wiring changes — same as Phase 1. This phase is entirely software, and it runs on your
**laptop**, not the Pico. Leave `class-4-phase-1-code.py` running on the Pico; you're adding a second,
separate program on your laptop that reads what the Pico is printing.

### Software for this phase

The first software in the course that runs on your laptop instead of the Pico. The Pico keeps running Phase 1's program unchanged.

| Software component | New, modified, or unchanged | What it does |
| :------------------- | :-------------------------- | :----------- |
| `wireframe.py` (laptop) | **New** — `class-4-phase-2-wireframe.py` | Reads the Pico's roll/pitch/yaw lines over USB serial and draws a live 3D box rotated to match. It labels the X/Y/Z axes and the box's red `Front` and `Right` faces. |
| `pyserial`, `matplotlib`, `numpy` (laptop) | **New** — `pip install pyserial matplotlib numpy` | Python packages for the laptop: `pyserial` reads the USB serial port, `numpy` does the rotation math, and `matplotlib` draws the 3D box. |
| `code.py` (on the Pico) | **Unchanged** — `class-4-phase-1-code.py` | Keeps streaming the roll/pitch/yaw CSV that `wireframe.py` draws. |

### What this code does

This script opens your laptop's serial connection to the Pico, reads each `roll, pitch, yaw` line as
it arrives, and redraws a simple 3D wireframe box rotated to match — live, using `matplotlib`.

### The code

First, install the needed packages once, in a terminal on your laptop:

```bash
pip install pyserial matplotlib numpy
```

Then save this file anywhere on your laptop (not the `CIRCUITPY` drive) as `wireframe.py`:

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

Run it from a terminal, substituting your Pico's actual serial port:

```bash
# Windows - you may need to change COM5
python wireframe.py COM5

# Linux - you may need to change /dev/ttyACM0
python wireframe.py /dev/ttyACM0
```

>**Important:** Mu or Thonny's serial console must be closed before running this — only one program
>can hold a serial port open at a time.

### Try it / what you should see

A window should pop up showing a wireframe box. Tilt your physical board and the on-screen box
should tilt to match, live — roll, pitch, and yaw should all turn the same direction as the board.
(Roll is negated inside `rotation_matrix()` so it turns the right way; the Pico's roll number is
unchanged.) If one motion still looks backwards, first make sure you're holding the board's +X end
where the `Front` label is (see the note below) — a board turned end-for-end makes every tilt look
reversed. If it's still backwards after that, flip that one angle's sign in `rotation_matrix()` the
same way roll is flipped (e.g. `-pitch`) — it's a display fix, not a filter bug.

>**Which end is "Front"?** The red `Front` label marks the end of the box that the IMU's **+X**
>axis points toward — not necessarily the end of the board you'd call the front. Before you tilt
>anything, find your board's +X end: look for the small X/Y arrows printed on the IMU breakout (if
>there's more than one set, use the accelerometer/gyro one, not the magnetometer's). No arrows? Hold
>the board flat, dip one short end down, and watch the screen — if the `Front` end dips too, that's
>+X; if the opposite end dips, +X is the other end. Mark it with a dot of marker or tape so you don't
>have to work it out again.

### Checkpoint

Tilt the board along one axis at a time and confirm the on-screen box responds — roll, pitch, and
yaw should each visibly correspond to a specific physical motion.

## 6. Build It: Phase 3 — Stop the Yaw Drift: Gyro Bias Calibration (on the Pico)

### Wiring for this phase

No wiring changes — same as Phase 1. This phase replaces the Pico's `code.py` with an improved
version; Phase 2's `wireframe.py` on your laptop works with it unchanged.

### Software for this phase

One file changes: the Pico's `code.py` gains gyro bias calibration. Its output format doesn't change, so the laptop side needs no edits.

| Software component | New, modified, or unchanged | What it does |
| :------------------- | :-------------------------- | :----------- |
| `code.py` | **Modified** — `class-4-phase-3-code.py`, replaces `class-4-phase-1-code.py` | Phase 1's program plus a 2-second startup gyro bias measurement, and bias refinement plus a filter integral reset whenever the board is still. Yaw holds steady instead of drifting. |
| `wireframe.py` (laptop) | **Unchanged** — `class-4-phase-2-wireframe.py` | Draws the same CSV stream; it skips the new calibration message lines automatically. |
| `adafruit_lsm9ds1.mpy` (in `/lib`) | **Unchanged** — from Phase 1 | Reads the accelerometer and gyroscope, including the readings averaged during calibration. |

### Why yaw drifts (and why the filter can't fix it)

Leave the board flat and untouched for a minute with the Phase 2 box on screen: roll and pitch stay
put, but yaw slowly spins away on its own. Here's why.

Every gyroscope has a **bias** — a small, nonzero reading even when it isn't rotating at all. It's
different on every chip, and it changes as the chip warms up. The filter integrates (adds up) the
gyro's rotation rate every loop, so a constant bias turns into a steadily growing angle: a bias of
just 0.5°/s becomes a 30° error after one minute.

For roll and pitch, the Mahony filter catches this. The accelerometer knows which way is *down*, so
whenever roll or pitch wanders, the filter sees the mismatch and pulls it back — that's exactly what
`MAHONY_KP` and `MAHONY_KI` do. But turning the board flat on a table doesn't change which way is
down, so the accelerometer has *no opinion* about yaw. Nothing corrects it, and yaw drifts at
whatever rate the Z-axis bias happens to be. (`MAHONY_KI` can't help either — it learns bias only from
the accelerometer's error, which stays at zero for yaw.)

The fix is to stop the bias before it ever reaches the filter, in two parts:

1. **Startup calibration.** When the board powers up, hold it still for about 2 seconds and average
    the gyro readings. The board isn't rotating, so that average *is* the bias. Subtract it from
    every reading from then on.
2. **Keep refining whenever the board is still.** The bias shifts as the chip warms up, so a
    startup snapshot slowly goes stale. Each loop, the code checks whether the board looks
    motionless — every gyro axis reading almost nothing *and* the accelerometer measuring just
    gravity (about 1 g). If so, whatever the gyro still reads must be leftover bias, not motion, so
    the code nudges its bias estimate 1% of the way toward it. A rover that stops often gets its
    bias re-trimmed at every stop.

The tradeoff to know about: a turn slower than the "still" threshold (`STILL_GYRO`, about 1°/s)
looks exactly like bias, so it gets absorbed into the bias instead of measured — a 90° turn made
at half a degree per second would barely register. That's fine for a car, which turns far faster
than that.

This makes yaw drift far slower, but it can't stop it completely — a tiny leftover error still adds
up over many minutes. Fully locking yaw needs an absolute heading reference, which is what the
LSM9DS1's third sensor, the magnetometer (a compass), is for. That's a stretch goal, not today's work.

### What this code does

It's Phase 1's program with three additions: a `calibrate_gyro_bias()` function that averages the
gyro for about 2 seconds at startup, an `is_still()` check, and a few lines in the main loop — one
subtracting the bias from every gyro reading, and, whenever `is_still()` is true, refining the bias
and clearing the filter's integral term (the next subsection explains why). The filter math and the
CSV output are unchanged, so the Phase 2 display keeps working.

One subtle detail: the loop's clock (`last_time`) is started *after* calibration. If it started
before, the first loop would see a 2-second `dt` and integrate a huge bogus rotation on its very
first step.

### One more leak: the filter's integral term (Fix 1 or Fix 2?)

Bias calibration alone leaves one hole, and you'll find it by shaking the board hard for a while,
then setting it down: yaw starts drifting again — sometimes 20-40° a minute — and keeps going no
matter how long the board sits still. The gyro bias isn't the problem this time; the filter's own
**integral term** is.

Look back at `mahony_update()`. Every loop, `MAHONY_KI` adds a little of the accelerometer's
"which way is down" error into `integral_fbx`, `integral_fby`, and `integral_fbz`, and those totals
are added to the gyro rates from then on. At rest that's helpful: it slowly learns and cancels a
steady gyro bias on roll and pitch. But while you're shaking the board, the accelerometer feels your
hand's pushes as well as gravity, so its "down" is wrong, the errors are big, and the integral totals
pile up (engineers call this *windup*). When the board comes to rest, roll and pitch errors shrink
and unwind `integral_fbx`/`integral_fby` — but `integral_fbz` is fed only by the yaw error, and the
accelerometer can't see yaw, so that error stays near zero. Nothing ever unwinds `integral_fbz`, and
it keeps adding a fake rotation rate to Z: a brand-new bias, created by the filter itself, that
Phase 3's bias calibration can't touch (it corrects the raw gyro, not the filter's internals).

There are two fixes:

| | Fix 1: set `MAHONY_KI = 0.0` | Fix 2: clear `integral_fbx/y/z` whenever `is_still()` is true |
| :--- | :--- | :--- |
| Change | One number | One line inside the `is_still()` branch |
| Windup after motion | Can't happen — the integral term is off | Wiped out the moment the board comes to rest |
| While the board keeps moving | Roll/pitch rely on `MAHONY_KP` alone, so a leftover bias can leave a small steady tilt offset | `MAHONY_KI` still trims leftover roll/pitch bias; `integral_fbz` can still wind up, so yaw may wander *during* long motion until the next stop |
| What you give up | `MAHONY_KI` stops doing anything, so there's nothing left to tune | Whatever `MAHONY_KI` learned is thrown away at every stop (fine — the bias estimate takes over at rest) |

In a simulation of 15 seconds of hard shaking followed by rest, both fixes cut the post-motion yaw
drift from 20-40°/min to under 0.5°/min, with the same roll and pitch. This code uses **Fix 2**: it
keeps `MAHONY_KI` doing useful work whenever the board is moving, and hands the job to the bias
estimate the moment it's still — each tool covers the situation it's good at. Fix 1 is the
simpler choice if you'd rather have one less moving part.

One thing neither fix does: put yaw *back*. Any heading error built up while the board was moving
stays as a fixed offset — nothing on the board knows which way it was originally facing (that would
take the magnetometer). What the fix guarantees is that once the board is still, yaw *stops
changing* within a couple of seconds, instead of drifting on forever.

### The code

Save this as `code.py` on your `CIRCUITPY` drive, replacing Phase 1's version.

```python
# class-4-phase-3-code.py -- save as code.py (replaces Phase 1's code.py)
# Phase 3: Phase 1's IMU + Mahony filter, plus gyro bias calibration:
#   1. at startup, measure the gyro's bias while the board sits still
#   2. while running, keep refining that bias whenever the board is still
#   3. whenever the board is still, clear the filter's integral term (see
#      "Fix 1 or Fix 2?" above) so motion can't leave yaw drifting afterward
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
        # Part 3 (Fix 2): the bias estimate now handles gyro error at rest, so
        # throw away whatever the filter's integral term piled up during motion
        # -- on yaw, nothing else would ever unwind it.
        integral_fbx = integral_fby = integral_fbz = 0.0

    mahony_update(ax, ay, az, gx, gy, gz, dt)
    roll, pitch, yaw = quaternion_to_euler()
    print("{:.1f}, {:.1f}, {:.1f}".format(roll, pitch, yaw))

    time.sleep(0.02)
```

### Try it / what you should see

Set the board flat on the table *before* it boots (or press reset with it lying still), and keep your
hands off it. The serial console prints `Calibrating gyro -- keep the board perfectly still...`,
then about 2 seconds later a line like `Gyro bias (deg/s): x=0.61 y=-0.35 z=0.18` — your chip's own
bias, which will differ from your neighbor's. Then the familiar `roll,pitch,yaw` stream starts.

Close the serial console and run `wireframe.py` again. Leave the board still for a full minute and
watch yaw in the window title: it should now hold within a degree or so, instead of spinning away
the way it did in Phase 2. Turn the board flat by 90° and back — yaw should follow the turn and
return close to where it started.

Now stress it: shake and spin the board hard for 10-15 seconds, then set it flat and let go. Within
a couple of seconds yaw should stop changing — probably at a new number rather than where it
started (see "Fix 1 or Fix 2?" above for why it can't return on its own).

If yaw drifts badly from the very start, the board probably moved during those 2 seconds of
calibration: press reset with the board lying still and try again.

### Checkpoint

Write down how many degrees yaw drifted in one minute with Phase 1's code, and how many with Phase
3's. Be able to explain in one sentence why the accelerometer can correct roll and pitch but not
yaw.

## 7. Build It: Phase 4 — Extend the Rover Status Website

### Wiring for this phase

No new wiring — same IMU wiring as Phase 1. This phase edits software only, and it edits your
Class 3 `rover_server.py`, not `class-4-phase-3-code.py`.

### Software for this phase

The Class 3 website file gets three new fields and Phase 3's calibrated IMU code. Every other file it relies on comes from Class 3 unchanged.

| Software component | New, modified, reuse, or unchanged | What it does |
| :------------------- | :-------------------------- | :----------- |
| `rover_server.py` | **Modified** — `class-4-phase-4-rover_server.py`, edits `class-3-phase-4-rover_server.py` | Same WiFi network, server, and webpage, now also reading and fusing the IMU. `/data.json` gains `roll`, `pitch`, and `yaw` next to the wheel fields. |
| `code.py` | **Reuse** — `class-3-phase-4-code.py` | The one-line `import rover_server` that starts the website. It goes back in place of Phase 3's IMU program, since only one program runs at a time. |
| `wheel_odometry.py` | **Reuse** — `class-3-phase-3-wheel_odometry.py` | Still supplies the wheel speed and direction fields. Its optional `while_sampling` argument keeps the IMU filter running during its 0.25 s sampling window. |
| `motor_driver.py` | **Reuse** — `class-3-phase-1-motor-driver.py` | Imported by `wheel_odometry` for each wheel's direction. |
| `adafruit_lsm9ds1.mpy`, `adafruit_httpserver` (in `/lib`) | **Unchanged** — from Phase 1 and Class 3 | The IMU driver and the web server library the website needs. |
| `settings.toml` | **Unchanged** — from Class 3 | Same network name and password for the Pico's WiFi network. |

### What this code does

Recall `rover_server.py`'s `/data.json` route from Class 3: it returns a small dict —
`speed_left_cms`, `dir_left`, `speed_right_cms`, `dir_right` — and the webpage just calls
`JSON.stringify()` on whatever that dict contains, so it already displays any field the dict has,
with no HTML/JavaScript changes needed. Today's edit only touches the Pico side: add the
sensor-read-and-fuse code from `class-4-phase-3-code.py` (including Phase 3's gyro bias
calibration) into `rover_server.py`, and add three keys to the returned dict.

**Keep the filter running.** There's one catch in moving the filter into a website. In Phases 1
and 3, the filter updated every pass of the loop, about 40 times a second. If `/data.json` ran the
filter itself, it would update only when the browser asks — twice a second — and each update would
treat one gyro reading as the rotation rate for the whole half-second, so any turn that speeds up,
slows down, or reverses in between is lost. Worse, `wheel_odometry.read_speed()` blocks for 0.25 s
while it counts wheel ticks. So this version runs the filter in two places: the main loop calls
`_update_orientation()` every pass, and the route passes the same function into
`read_speed(while_sampling=...)`, which calls it about every 20 ms while it samples. The route then
just reports `latest_orientation`. In simulation, running the filter per request left yaw 35-125°
wrong after 15 s of hand-held turning; this version stays within about 15°, close to Phase 3's
standalone program.

This file duplicates rather than imports `class-4-phase-3-code.py`'s Mahony filter code, and that's
deliberate, not sloppy: `class-4-phase-3-code.py` ends in its own blocking `while True:` loop that prints
CSV forever, and `rover_server.py` ends in its own blocking `while True: server.poll()` loop that
answers web requests forever — two different infinite loops that can't run inside the same program
at the same time. Class 3's `rover_server.py` was built the same non-library way — a module whose
own blocking loop runs the moment something imports it, not something another file can call
piecemeal — and today's edit keeps that same shape rather than turning it into a shared library. If
you want to run the live 3D box
(Phases 1-3) and the website (this phase) at once, you'd need a real rewrite that merges both loops
into one — worth thinking about, not worth doing today.
`class-4-phase-3-code.py` and today's edited `rover_server.py` are two different things
`code.py` on your `CIRCUITPY` drive could be — the same way Class 3's square/circle attempt and its
website were two different `code.py` options. You'll only ever have one of them running at a time;
Section 9's "Put It All Together" shows both as complete, final options.

### The code

Open your existing `rover_server.py` (saved during Class 3 Phase 4) and edit it into the version
below — or save this file over it directly.

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

# Configure your Access Point credentials
ap_ssid = os.getenv("CIRCUITPY_WIFI_AP_SSID")
ap_password = os.getenv("CIRCUITPY_WIFI_AP_PASSWORD")   # Minimum 8 characters (or leave as "" for an open network)

print("Starting Wi-Fi Access Point...")
wifi.radio.start_ap(ssid=ap_ssid, password=ap_password)

# The default IP address for a CircuitPython AP is typically 192.168.4.1
ap_ip = wifi.radio.ipv4_address_ap
print(f"AP Active! Connect to SSID: '{ap_ssid}'")
print(f"Server IP Address: {ap_ip}")

# Set up socket pool and HTTP server
pool = socketpool.SocketPool(wifi.radio)
server = Server(pool)
#server = Server(pool, debug=True)

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
    # Identical math to class-4-phase-3-code.py's mahony_update() -- see Section 3's
    # "Mahony filter" explanation for why fusing accel+gyro this way works.
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
    global integral_fbx, integral_fby, integral_fbz
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
        integral_fbx = integral_fby = integral_fbz = 0.0  # Fix 2: clear integral windup
    _mahony_update(ax, ay, az, gx, gy, gz, dt)
    roll = math.degrees(math.atan2(2 * (q0 * q1 + q2 * q3), 1 - 2 * (q1 * q1 + q2 * q2)))
    pitch = math.degrees(math.asin(max(-1.0, min(1.0, 2 * (q0 * q2 - q3 * q1)))))
    yaw = math.degrees(math.atan2(2 * (q0 * q3 + q1 * q2), 1 - 2 * (q2 * q2 + q3 * q3)))
    return roll, pitch, yaw


# Measure the gyro bias once at startup (the rover must sit still while it
# boots), then start the filter's clock so the first dt isn't the 2 s wait.
bias_x, bias_y, bias_z = _calibrate_gyro_bias()
last_time = time.monotonic()

# The filter has to run continuously -- about every 20 ms, like Phase 3 -- not
# just when the browser asks for data (only twice a second). The main loop and
# read_speed() both call this; /data.json just reports the latest result.
latest_orientation = (0.0, 0.0, 0.0)


def _update_orientation():
    """Advance the filter one step and remember the result for /data.json."""
    global latest_orientation
    latest_orientation = _read_orientation()


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
    # read_speed() spends 0.25 s counting wheel ticks; passing the filter update
    # keeps orientation tracking running during that window instead of pausing it.
    speed_left, dir_left, speed_right, dir_right = wheel_odometry.read_speed(
        while_sampling=_update_orientation)
    roll, pitch, yaw = latest_orientation  # kept current by the main loop
    return JSONResponse(request, {
        "speed_left_cms": speed_left,
        "dir_left": dir_left,
        "speed_right_cms": speed_right,
        "dir_right": dir_right,
        "roll": roll,
        "pitch": pitch,
        "yaw": yaw,
    })


# Define the website route for the homepage
@server.route("/")
def index(request: Request):
    return Response(request, STATUS_PAGE, content_type="text/html")


# Start the server on port 5000
# Port 5000 is used to avoid conflicts with CircuitPython's Web Workflow on port 80
server.start(str(ap_ip), port=5000)
print(f"HTTP Server running at http://{ap_ip}:5000")
print("Class 4, Phase 4 -- rover status website now serving data ...")

# Main loop: keep the orientation filter running, and answer web requests
while True:
    _update_orientation()  # every pass, whether or not a browser is asking
    time.sleep(0.02)       # same ~40 Hz pace as Phase 3
    try:
        server.poll()
    except Exception as e:
        print(f"Server error: {e}")

```

### Try it / what you should see

Watch the serial console for `Starting Wi-Fi Access Point...`, `AP Active! Connect to SSID: ...`,
and `Server IP Address: ...`, then the `Calibrating gyro` line — leave the rover untouched for those
2 seconds, since it measures the gyro bias exactly as Phase 3 does — and finally
`HTTP Server running at http://192.168.4.1:5000`. Join your Pico's own WiFi network from your
laptop (same network name and password as Class 3 — `settings.toml` carries over unchanged), then
open `http://192.168.4.1:5000` in a browser. Type the `http://` and the `:5000`: this version
serves on port 5000 because CircuitPython's Web Workflow can already be using port 80, and a
browser that quietly switches to `https://` will report "refused to connect." You should now see seven fields updating live: `speed_left_cms`, `dir_left`, `speed_right_cms`, `dir_right`, `roll`, `pitch`, `yaw`.
Spin a wheel by hand and watch the speed fields jump; tilt the board and watch `roll`/`pitch`/`yaw`
change — all on the one page, with no separate display.

If `roll`/`pitch`/`yaw` show up as `0.0` and never change, that's the same symptom as Phase 1's
flat-line serial output — check `SDA`/`SCL` wiring before touching the server code. If the page is
missing the Class 3 fields (`speed_left_cms`, etc.), you likely saved `class-4-phase-4-rover_server.py` as a new
file instead of over the existing `rover_server.py` — make sure only one such file exists on
`CIRCUITPY`. If the webpage doesn't pick up the new fields at all, try a hard refresh — your browser
may be showing a cached copy of the page.

### Checkpoint

Join your Pico's own WiFi network, open its status webpage, and confirm all seven fields — `speed_left_cms`, `dir_left`,
`speed_right_cms`, `dir_right`, `roll`, `pitch`, `yaw` — update live, with wheel speed responding to
driving and orientation responding to tilting the board by hand. Be able to say in one sentence why
adding orientation didn't require touching any HTML or JavaScript — only the dict returned from
`/data.json`.

## 8. Troubleshooting Guide

| Problem | Likely Cause | Fix |
| :-------- | :------------- | :---- |
| No serial output at all from `class-4-phase-1-code.py` | `SDA`/`SCL` swapped, or the I2C device isn't detected | Verify `SDA` on `GP0`, `SCL` on `GP1`; confirm power/ground |
| `roll,pitch,yaw` prints but never changes | Board isn't actually being moved, or a loose connection is producing a stuck reading | Physically tilt the board while watching output; reseat the STEMMA QT cable |
| Roll or pitch drifts noticeably even when the board sits still | `MAHONY_KI` or `MAHONY_KP` too low to correct drift | Raise both in small steps and re-test |
| Yaw spins away steadily while the board sits still | Still running Phase 1's code (no bias calibration), or the board moved during the 2 s startup calibration | Confirm `code.py` is Phase 3's version; press reset with the board lying still |
| Yaw drifts again after heavy motion, and keeps drifting once set down | The filter's integral term wound up during motion (`integral_fbz` can't unwind on its own) | Confirm the `is_still()` branch clears `integral_fbx`/`integral_fby`/`integral_fbz` (Fix 2), or set `MAHONY_KI = 0.0` (Fix 1) |
| Yaw still creeps a degree or two over several minutes | Expected — calibration slows drift but can't remove it; only a magnetometer gives an absolute heading | Press reset (with the board still) to re-zero |
| Very slow turns barely register in yaw | A turn slower than `STILL_GYRO` looks like bias and gets absorbed into it | Lower `STILL_GYRO` (e.g. `0.01`) and re-test |
| Orientation is jittery/noisy even when the board is still | `MAHONY_KP` too high | Lower `MAHONY_KP` in small steps and re-test |
| 3D box turns backwards or on the wrong axis | Board's +X end isn't where the `Front` label is, or one axis has a display sign mismatch | Line up +X with `Front` first; if one motion is still backwards, negate that angle in `rotation_matrix()` (roll already is) |
| `wireframe.py` can't open the serial port | Wrong `PORT` argument, or Mu/Thonny's serial console still has the port open | Close Mu/Thonny's serial console; confirm the correct COM port in Device Manager |
| `ModuleNotFoundError` for `serial`, `matplotlib`, or `numpy` | Dependencies not installed on your laptop | Run `pip install pyserial matplotlib numpy` in the same Python environment used to run the script |
| `ImportError: no module named 'adafruit_lsm9ds1'` | Library not copied to `/lib` on your `CIRCUITPY` drive | Copy `adafruit_lsm9ds1.mpy` from the Library Bundle into `/lib` |
| Rover status website's `roll`/`pitch`/`yaw` show `0.0` and never change | Same I2C wiring problem as `class-4-phase-1-code.py` — `SDA`/`SCL` swapped or not detected | Verify `SDA` on `GP0`, `SCL` on `GP1` before touching `rover_server.py`'s new code |
| Website's `yaw` lags or ends up far off after turning, though Phase 3 tracks fine | Filter runs only per browser request, or pauses during `read_speed()` | Main loop must call `_update_orientation()`; route must pass `while_sampling=_update_orientation` |
| `TypeError: ... unexpected keyword argument 'while_sampling'` | `wheel_odometry.py` on `CIRCUITPY` is an older copy without the optional argument | Update `read_speed()` to the Class 3 Phase 3 version, which accepts `while_sampling` |
| Browser says "refused to connect" at `192.168.4.1` | Wrong port (this version uses `5000`) or the browser switched to `https://` | Open exactly `http://192.168.4.1:5000` |
| Website loads but is missing `speed_left_cms`/`dir_left`/etc. from Class 3 | `class-4-phase-4-rover_server.py` was saved as a new file instead of over the existing `rover_server.py` | Confirm only one `rover_server.py` exists on `CIRCUITPY` and it's the Class 4 version with all seven fields |
| Website's orientation fields update, but wheel speed/direction stopped working | `wheel_odometry` import removed, or Class 3's optocoupler wiring on `GP19`/`GP17` was disturbed while adding today's IMU wiring | Confirm `import wheel_odometry` is still present and Class 3's optocoupler wiring wasn't bumped |

## 9. Put It All Together

This is the finished project in one place. Unlike Phases 1-3, where `code.py` and the laptop
viewer were the only pieces, this Class actually finishes with *two different things* `code.py`
could be — the IMU-streaming/3D-viewer pair (Phases 1-3) or the extended rover status website
(Phase 4) — since neither runs at the same time as the other (see Phase 4's "What this code does"
for why). Swap between them by replacing `code.py`: Option A's program itself, or Option B's
one-line `import rover_server` wrapper. Both are shown below so you have the complete, final version of each in one place.

### Complete wiring

| Component | Pico 2 W Pin |
| :---------- | :------------- |
| LSM9DS1 `SDA` | `GP0` |
| LSM9DS1 `SCL` | `GP1` |
| LSM9DS1 `VIN`/power | `3V3` |
| LSM9DS1 `GND` | `GND` |

(Classes 1-3's circuits stay untouched on the breadboard alongside this.)

### Complete code

**Option A — `code.py` as the IMU streaming/3D viewer pair** (Phase 3's Pico code + Phase 2's viewer, unchanged):

**On the Pico**, save as `code.py` (unchanged from Phase 3 — this is already the complete,
finished version, gyro bias calibration included):

```python
# class-4-phase-3-code.py -- LSM9DS1 over I2C, gyro-bias-calibrated,
# Mahony-filtered roll/pitch/yaw over serial.
import time
import math
import board
import busio
import adafruit_lsm9ds1

i2c = busio.I2C(board.GP1, board.GP0)
sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

MAHONY_KP = 2.0   # calibrate: drift-vs-jitter tradeoff
MAHONY_KI = 0.05  # calibrate: corrects long-term gyro bias (roll/pitch only)
CAL_SAMPLES = 200  # startup gyro bias calibration: about 2 s of readings
STILL_GYRO = 0.02  # rad/s: below this on every axis counts as "still"
STILL_ACCEL = 0.3  # m/s^2: this close to 1 g counts as "still"
BIAS_ALPHA = 0.01  # how fast the bias follows while the board is still
GRAVITY = 9.81     # m/s^2

q0, q1, q2, q3 = 1.0, 0.0, 0.0, 0.0
integral_fbx = integral_fby = integral_fbz = 0.0


def mahony_update(ax, ay, az, gx, gy, gz, dt):
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
    roll = math.degrees(math.atan2(2 * (q0 * q1 + q2 * q3), 1 - 2 * (q1 * q1 + q2 * q2)))
    pitch = math.degrees(math.asin(max(-1.0, min(1.0, 2 * (q0 * q2 - q3 * q1)))))
    yaw = math.degrees(math.atan2(2 * (q0 * q3 + q1 * q2), 1 - 2 * (q2 * q2 + q3 * q3)))
    return roll, pitch, yaw


def calibrate_gyro_bias():
    print("Calibrating gyro -- keep the board perfectly still...")
    sum_x = sum_y = sum_z = 0.0
    for _ in range(CAL_SAMPLES):
        gx, gy, gz = sensor.gyro
        sum_x += gx
        sum_y += gy
        sum_z += gz
        time.sleep(0.01)
    return sum_x / CAL_SAMPLES, sum_y / CAL_SAMPLES, sum_z / CAL_SAMPLES


def is_still(ax, ay, az, gx, gy, gz):
    accel_mag = (ax * ax + ay * ay + az * az) ** 0.5
    return (
        abs(gx) < STILL_GYRO
        and abs(gy) < STILL_GYRO
        and abs(gz) < STILL_GYRO
        and abs(accel_mag - GRAVITY) < STILL_ACCEL
    )


print("Class 4 project running -- IMU orientation streaming.")
bias_x, bias_y, bias_z = calibrate_gyro_bias()
print("Gyro bias (deg/s): x={:.2f} y={:.2f} z={:.2f}".format(
    math.degrees(bias_x), math.degrees(bias_y), math.degrees(bias_z)))
last_time = time.monotonic()  # start the clock after calibrating

while True:
    now = time.monotonic()
    dt = now - last_time
    last_time = now
    ax, ay, az = sensor.acceleration
    gx, gy, gz = sensor.gyro  # already radians/sec
    gx, gy, gz = gx - bias_x, gy - bias_y, gz - bias_z
    if is_still(ax, ay, az, gx, gy, gz):
        bias_x += BIAS_ALPHA * gx
        bias_y += BIAS_ALPHA * gy
        bias_z += BIAS_ALPHA * gz
        integral_fbx = integral_fby = integral_fbz = 0.0  # Fix 2: clear integral windup
    mahony_update(ax, ay, az, gx, gy, gz, dt)
    roll, pitch, yaw = quaternion_to_euler()
    print("{:.1f},{:.1f},{:.1f}".format(roll, pitch, yaw))
    time.sleep(0.02)
```

**On your laptop**, save as `wireframe.py` and run it with `python wireframe.py <port>` (unchanged from Phase 2):

```python
# class-4-phase-2-wireframe.py -- save as wireframe.py; LAPTOP-side live 3D orientation display.
import sys
import serial
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

PORT = sys.argv[1] if len(sys.argv) > 1 else "COM5"
BAUD = 115200
ser = serial.Serial(PORT, BAUD, timeout=1)

box_vertices = np.array([
    [-1, -0.5, -0.2], [1, -0.5, -0.2], [1, 0.5, -0.2], [-1, 0.5, -0.2],
    [-1, -0.5, 0.2], [1, -0.5, 0.2], [1, 0.5, 0.2], [-1, 0.5, 0.2],
])
edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4),
         (0, 4), (1, 5), (2, 6), (3, 7)]
FRONT_FACE = [1, 2, 6, 5]  # small +X end of the box
RIGHT_FACE = [0, 1, 5, 4]  # -Y long side (+Y points left)


def rotation_matrix(roll, pitch, yaw):
    r, p, y = np.radians([-roll, pitch, yaw])  # roll negated to match physical board
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
ax.set_xlabel("X  (roll axis)")
ax.set_ylabel("Y  (pitch axis)")
ax.set_zlabel("Z  (yaw axis)")
edge_lines = [ax.plot([], [], [], color="C0")[0] for _ in edges]
front_label = ax.text(0, 0, 0, "Front", color="red", ha="center", va="center")
right_label = ax.text(0, 0, 0, "Right", color="red", ha="center", va="center")
plt.show(block=False)

while True:
    raw = ser.readline()
    while ser.in_waiting:  # skip stale lines -- draw only the newest
        raw = ser.readline()
    line = raw.decode("utf-8", errors="ignore").strip()
    if not line:
        continue
    try:
        roll, pitch, yaw = [float(v) for v in line.split(",")]
    except ValueError:
        continue
    rotated = box_vertices @ rotation_matrix(roll, pitch, yaw).T
    for edge_line, (a, b) in zip(edge_lines, edges):
        pts = rotated[[a, b]]
        edge_line.set_data_3d(pts[:, 0], pts[:, 1], pts[:, 2])
    front_label.set_position_3d(rotated[FRONT_FACE].mean(axis=0))
    right_label.set_position_3d(rotated[RIGHT_FACE].mean(axis=0))
    ax.set_title("roll={:.0f} pitch={:.0f} yaw={:.0f}".format(roll, pitch, yaw))
    fig.canvas.draw_idle()
    fig.canvas.flush_events()
```

**Option B — `rover_server.py` plus the one-line `code.py` wrapper** (same as Phase 4, unchanged).
Save this as `rover_server.py`, not `code.py` — Class 5 imports it by that name. `code.py` is the
same one-line `import rover_server` from Class 3. You also need `motor_driver.py` and
`wheel_odometry.py` still on `CIRCUITPY`, unchanged from Class 3:

```python
# rover_server.py -- complete project, option B: rover status website with orientation.
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

# Configure your Access Point credentials
ap_ssid = os.getenv("CIRCUITPY_WIFI_AP_SSID")
ap_password = os.getenv("CIRCUITPY_WIFI_AP_PASSWORD")   # Minimum 8 characters (or leave as "" for an open network)

print("Starting Wi-Fi Access Point...")
wifi.radio.start_ap(ssid=ap_ssid, password=ap_password)

# The default IP address for a CircuitPython AP is typically 192.168.4.1
ap_ip = wifi.radio.ipv4_address_ap
print(f"AP Active! Connect to SSID: '{ap_ssid}'")
print(f"Server IP Address: {ap_ip}")

# Set up socket pool and HTTP server
pool = socketpool.SocketPool(wifi.radio)
server = Server(pool)
#server = Server(pool, debug=True)

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
    # Identical math to class-4-phase-3-code.py's mahony_update() -- see Section 3's
    # "Mahony filter" explanation for why fusing accel+gyro this way works.
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
    global integral_fbx, integral_fby, integral_fbz
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
        integral_fbx = integral_fby = integral_fbz = 0.0  # Fix 2: clear integral windup
    _mahony_update(ax, ay, az, gx, gy, gz, dt)
    roll = math.degrees(math.atan2(2 * (q0 * q1 + q2 * q3), 1 - 2 * (q1 * q1 + q2 * q2)))
    pitch = math.degrees(math.asin(max(-1.0, min(1.0, 2 * (q0 * q2 - q3 * q1)))))
    yaw = math.degrees(math.atan2(2 * (q0 * q3 + q1 * q2), 1 - 2 * (q2 * q2 + q3 * q3)))
    return roll, pitch, yaw


# Measure the gyro bias once at startup (the rover must sit still while it
# boots), then start the filter's clock so the first dt isn't the 2 s wait.
bias_x, bias_y, bias_z = _calibrate_gyro_bias()
last_time = time.monotonic()

# The filter has to run continuously -- about every 20 ms, like Phase 3 -- not
# just when the browser asks for data (only twice a second). The main loop and
# read_speed() both call this; /data.json just reports the latest result.
latest_orientation = (0.0, 0.0, 0.0)


def _update_orientation():
    """Advance the filter one step and remember the result for /data.json."""
    global latest_orientation
    latest_orientation = _read_orientation()


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
    # read_speed() spends 0.25 s counting wheel ticks; passing the filter update
    # keeps orientation tracking running during that window instead of pausing it.
    speed_left, dir_left, speed_right, dir_right = wheel_odometry.read_speed(
        while_sampling=_update_orientation)
    roll, pitch, yaw = latest_orientation  # kept current by the main loop
    return JSONResponse(request, {
        "speed_left_cms": speed_left,
        "dir_left": dir_left,
        "speed_right_cms": speed_right,
        "dir_right": dir_right,
        "roll": roll,
        "pitch": pitch,
        "yaw": yaw,
    })


# Define the website route for the homepage
@server.route("/")
def index(request: Request):
    return Response(request, STATUS_PAGE, content_type="text/html")


# Start the server on port 5000
# Port 5000 is used to avoid conflicts with CircuitPython's Web Workflow on port 80
server.start(str(ap_ip), port=5000)
print(f"HTTP Server running at http://{ap_ip}:5000")
print("Class 4, Phase 4 -- rover status website now serving data ...")

# Main loop: keep the orientation filter running, and answer web requests
while True:
    _update_orientation()  # every pass, whether or not a browser is asking
    time.sleep(0.02)       # same ~40 Hz pace as Phase 3
    try:
        server.poll()
    except Exception as e:
        print(f"Server error: {e}")

```

```python
# code.py -- runs the rover status website (same one-line wrapper as Class 3)
import rover_server
```

To satisfy this Class's milestone (a live 3D orientation display *and* orientation visible on the
rover status website), run Option A first to demo the 3D box, then swap in Option B and open the
webpage to show wheel speed and orientation updating together — the two don't need to run at the
same instant to prove both work.

## 10. What You Learned

You gave your board a sense of orientation and watched it come alive on screen in real time — and
on the same website your car has been publishing to since Class 3. Specifically, you now know:

* What an accelerometer and a gyroscope each measure, and where each one is individually
    unreliable (accelerometer noisy under motion, gyroscope drifts over time)
* Why fusing them with a Mahony filter produces a more usable orientation than either alone —
    trusting the gyro for fast changes, correcting toward the accelerometer over time
* How to tune a filter's proportional gain (`MAHONY_KP`) and feel the tradeoff between drift and
    jitter firsthand
* What gyro *bias* is, why the accelerometer can correct it on roll and pitch but not on yaw, and
    how to cancel it — measure it at startup, then keep refining it whenever the board sits still
* How to stream sensor data from your Pico to a program running on your laptop over serial, and
    turn it into a live visualization
* How to extend an already-running website instead of building a new one — adding fields to a JSON
    dict a page already knows how to display, with no HTML/JavaScript changes needed
* That your rover status website now carries wheel speed/direction *and* orientation together on
    one page — a thread that started in Class 3 and that Class 5 and 6 will keep adding to

And critically: you also confirmed that knowing which way something is pointed still isn't the
same as knowing how far it has traveled — even with both wheel speed and orientation sitting side
by side on the same webpage. That's exactly why Class 5 doesn't use the IMU at all to solve the
navigation problem — it takes a completely different approach, using the sensor and servo you built
back in Class 2.

---
## 11. Homework Assignment

No homework assignments have been written for this class yet. This section will be filled in with
optional take-home exercises, following the same format as the Pre-Class homework in
[`class-00-lesson-script.md`](class-00-lesson-script.md#10-homework-assignment) (what the code
does, full commented code, and real-world examples).

## References

* [Python & CircuitPython — Adafruit LSM9DS1 9-DOF Breakout][01] — Adafruit's official guide for
    wiring and reading the LSM9DS1 over I2C in CircuitPython
* [API Reference — Adafruit LSM9DS1 Library][02] — the `adafruit_lsm9ds1` library API used in this
    script
* [9-DOF LSM9DS1 Breakout Board — Product Page][03] — the IMU used this project
* [`adafruit_httpserver` — API Reference][04] — the `Server`/`Request`/`Response`/`JSONResponse` API
    used to extend `rover_server.py` in Phase 4 (same API Class 3 introduced)
* [Getting Started With Inertial Measurement Units | Exploring Degrees Of Freedom][05] — a friendly
    introduction to accelerometers, gyroscopes, and degrees of freedom

---



[01]:https://learn.adafruit.com/adafruit-lsm9ds1-accelerometer-plus-gyro-plus-magnetometer-9-dof-breakout/python-circuitpython
[02]:https://docs.circuitpython.org/projects/lsm9ds1/en/latest/api.html
[03]:https://www.adafruit.com/product/4634
[04]:https://docs.circuitpython.org/projects/httpserver/en/latest/api.html
[05]:https://core-electronics.com.au/guides/getting-started-with-inertial-measurement-units-exploring-degrees-of-freedom/

[20]:https://pico2w.pinout.xyz/
[21]:https://learn.adafruit.com/adafruit-lsm9ds1-accelerometer-plus-gyro-plus-magnetometer-9-dof-breakout/pinouts
[22]:https://www.adafruit.com/product/4399

