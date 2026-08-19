# Lesson Script: Class 4 — Inertial Measurement Unit (IMU)

* [Getting Started With Inertial Measurement Units | Exploring Degrees Of Freedom](https://core-electronics.com.au/guides/getting-started-with-inertial-measurement-units-exploring-degrees-of-freedom/#bonus)

* **Class:** 4 of 6 (plus Pre-Class)
* **Duration:** ~2 hours
* **What You'll Need:** see [Section 2](#2-what-youll-need)
* **Before You Start:** Your Class 1-3 circuits (button/encoder, sensor/servo sweep, motor driver)
    should still be working and stay exactly as they are on your breadboard. You should also have
    Python 3 installed on your laptop from the Pre-Class — this class is the first one that runs
    code on your laptop as well as your Pico.

---


## 1. What This Project Is

Class 3 ended with a real gap: your car can move, but it has no way to know whether it actually
went where you told it to. Today you start closing that gap by giving your board a sense of
balance — the LSM9DS1 IMU (inertial measurement unit), which can tell you which way something is
pointed, the same way your inner ear tells you which way is up with your eyes closed.

You'll wire the IMU over I2C, read its raw acceleration and rotation-rate data, and then combine
("fuse") those two individually-flawed signals into one stable roll/pitch/yaw orientation using a
**Mahony filter**. You'll stream that orientation live from your Pico to a 3D box drawn on your
laptop screen, so you can watch your physical tilt reflected on screen in real time. By the end,
you'll also be able to say clearly why this — as exciting as it is — still doesn't solve Class 3's
square-and-circle problem on its own.

## 2. What You'll Need

| Component | Quantity | Purpose This Project |
| :---------- | :--------: | :---------------------- |
| Raspberry Pi Pico 2 W (with header) | 1 | Runs your CircuitPython code |
| LSM9DS1 9-DOF IMU breakout board (STEMMA) | 1 | Measures acceleration and rotation rate |
| STEMMA QT/Qwiic cable (or Dupont jumpers) | 1 | I2C connection between the Pico and the IMU |
| Breadboard (from Classes 1-3) | 1 | Your existing circuits stay on it, untouched |
| USB cable | 1 | Powers the Pico and carries the serial data |
| Laptop with Mu or Thonny | 1 | Where you write/save the Pico's code |
| Laptop with Python 3 + `pyserial`, `matplotlib`, `numpy` | 1 | Runs the 3D visualization script (this part runs on your laptop, not the Pico) |

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
the truth even if the board never actually moves.

**Mahony filter.** Neither sensor alone is good enough, so `class-4-code-1.py` fuses both with a
Mahony filter: it trusts the gyroscope for fast, moment-to-moment changes, and continuously nudges
its estimate back toward what the accelerometer says over the longer term — correcting the gyro's
drift without inheriting the accelerometer's short-term noise. (Kalman and Madgwick filters solve
this same problem with different math; Mahony is what's actually implemented here.) The filter's
`MAHONY_KP` gain controls how strongly it trusts that correction — you'll tune this live and feel
the tradeoff between drift (too low) and jitter (too high).

**Pinout summary** (Raspberry Pi Pico 2 W — new pins only; Classes 1-3 are unaffected):

| Pin | What we use it for |
| :---- | :-------------------- |
| `GP0` | LSM9DS1 `SDA` (I2C data) |
| `GP1` | LSM9DS1 `SCL` (I2C clock) |
| `3V3` | LSM9DS1 `VIN`/power |
| `GND` | LSM9DS1 `GND` |

## 4. Build It: Phase 1 — Read, Fuse, and Print Orientation (on the Pico)

### Wiring for this phase

This is the complete wiring for the whole project — Phase 2 adds no new hardware, it just runs a
second program on your laptop.

| Component | Pico 2 W Pin |
| :---------- | :------------- |
| LSM9DS1 `SDA` | `GP0` |
| LSM9DS1 `SCL` | `GP1` |
| LSM9DS1 `VIN`/power | `3V3` |
| LSM9DS1 `GND` | `GND` |

Your Class 1-3 circuits stay exactly where they are on the breadboard. Before writing any code,
trace this wiring out loud — especially confirm `SDA`/`SCL` aren't swapped, since I2C devices
commonly fail *silently* (no error, just no data at all) when they are.

### What this code does

This program reads raw acceleration and rotation-rate values from the IMU, feeds them into a
Mahony filter (implemented as a running "quaternion" — a compact way to represent 3D rotation),
converts the result into the more intuitive roll/pitch/yaw angles, and prints them as a CSV line
every loop.

### The code

Save this as `code.py` on your `CIRCUITPY` drive.

```python
# class-4-code-1.py
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
    gx, gy, gz = sensor.gyro  # degrees/sec
    # Convert gyro readings to radians/sec to match the filter math above.
    gx, gy, gz = math.radians(gx), math.radians(gy), math.radians(gz)

    mahony_update(ax, ay, az, gx, gy, gz, dt)
    roll, pitch, yaw = quaternion_to_euler()
    print("{:.1f},{:.1f},{:.1f}".format(roll, pitch, yaw))

    time.sleep(0.02)
```

### Try it / what you should see

You should see a stream of `roll,pitch,yaw` lines, updating fast (about 50 times a second). Tilt
the board by hand and watch roll and pitch change sensibly; yaw may drift slowly on its own even
without rotating the board flat — that's expected gyro drift on the axis the accelerometer can't
correct (it can't tell "which way is North," only "which way is down").

If you see a flat `0.0,0.0,0.0` (or nothing at all), that's almost always an I2C wiring problem,
not a filter math problem — double-check `SDA`/`SCL` before touching `MAHONY_KP` or `MAHONY_KI`.

### Checkpoint

Confirm three changing numbers scroll by in the console, and that tilting the board by hand
produces sensible roll/pitch changes you can visually correlate to the motion you just made.

## 5. Build It: Phase 2 — Live 3D Visualization (on Your Laptop)

### Wiring for this phase

No wiring changes — same as Phase 1. This phase is entirely software, and it runs on your
**laptop**, not the Pico. Leave `class-4-code-1.py` running on the Pico; you're adding a second,
separate program on your laptop that reads what the Pico is printing.

### What this code does

This script opens your laptop's serial connection to the Pico, reads each `roll,pitch,yaw` line as
it arrives, and redraws a simple 3D wireframe box rotated to match — live, using `matplotlib`.

### The code

First, install the needed packages once, in a terminal on your laptop:

```bash
pip install pyserial matplotlib numpy
```

Then save this file anywhere on your laptop (not the `CIRCUITPY` drive) as `class-4-code-2.py`:

```python
# class-4-code-2.py
# Phase 2: runs on your LAPTOP, not the Pico. Reads roll,pitch,yaw CSV over
# serial from class-4-code-1.py and draws a live-updating 3D box.
# Usage: python class-4-code-2.py <port>   (e.g. python class-4-code-2.py COM5)

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


def rotation_matrix(roll, pitch, yaw):
    """Build a combined 3D rotation matrix from roll/pitch/yaw degrees."""
    r, p, y = np.radians([roll, pitch, yaw])
    rx = np.array([[1, 0, 0], [0, np.cos(r), -np.sin(r)], [0, np.sin(r), np.cos(r)]])
    ry = np.array([[np.cos(p), 0, np.sin(p)], [0, 1, 0], [-np.sin(p), 0, np.cos(p)]])
    rz = np.array([[np.cos(y), -np.sin(y), 0], [np.sin(y), np.cos(y), 0], [0, 0, 1]])
    return rz @ ry @ rx


plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

print("Class 4, Phase 2 -- 3D box display starting, reading from", PORT)

while True:
    line = ser.readline().decode("utf-8", errors="ignore").strip()
    if not line:
        continue
    try:
        roll, pitch, yaw = [float(v) for v in line.split(",")]
    except ValueError:
        # Skip any partial/garbled line rather than crashing the display.
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

Run it from a terminal, substituting your Pico's actual serial port:

```bash
python class-4-code-2.py COM5
```

**Important:** Mu or Thonny's serial console must be closed before running this — only one program
can hold a serial port open at a time.

### Try it / what you should see

A window should pop up showing a wireframe box. Tilt your physical board and the on-screen box
should tilt to match, live. If the box moves but on a different axis than you expect (or
inverted), that's a known rough edge in this visualization's axis assumptions — not a filter bug —
worth noting but not worth chasing down today.

### Checkpoint

Tilt the board along one axis at a time and confirm the on-screen box responds — roll, pitch, and
yaw should each visibly correspond to a specific physical motion.

## 6. Troubleshooting Guide

| Problem | Likely Cause | Fix |
| :-------- | :------------- | :---- |
| No serial output at all from `class-4-code-1.py` | `SDA`/`SCL` swapped, or the I2C device isn't detected | Verify `SDA` on `GP0`, `SCL` on `GP1`; confirm power/ground |
| `roll,pitch,yaw` prints but never changes | Board isn't actually being moved, or a loose connection is producing a stuck reading | Physically tilt the board while watching output; reseat the STEMMA QT cable |
| Orientation drifts noticeably even when the board sits still | `MAHONY_KI` or `MAHONY_KP` too low to correct drift | Raise both in small steps and re-test |
| Orientation is jittery/noisy even when the board is still | `MAHONY_KP` too high | Lower `MAHONY_KP` in small steps and re-test |
| 3D box moves on the wrong axis, or inverted | Axis-convention mismatch between physical mounting and the visualization's rotation matrix | Known rough edge — note it and move on, not worth debugging live |
| `class-4-code-2.py` can't open the serial port | Wrong `PORT` argument, or Mu/Thonny's serial console still has the port open | Close Mu/Thonny's serial console; confirm the correct COM port in Device Manager |
| `ModuleNotFoundError` for `serial`, `matplotlib`, or `numpy` | Dependencies not installed on your laptop | Run `pip install pyserial matplotlib numpy` in the same Python environment used to run the script |
| `ImportError: no module named 'adafruit_lsm9ds1'` | Library not copied to `/lib` on your `CIRCUITPY` drive | Copy `adafruit_lsm9ds1.mpy` from the Library Bundle into `/lib` |

## 7. Put It All Together

This is the finished project in one place — two files, one running on the Pico and one on your
laptop, working together.

### Complete wiring

| Component | Pico 2 W Pin |
| :---------- | :------------- |
| LSM9DS1 `SDA` | `GP0` |
| LSM9DS1 `SCL` | `GP1` |
| LSM9DS1 `VIN`/power | `3V3` |
| LSM9DS1 `GND` | `GND` |

(Classes 1-3's circuits stay untouched on the breadboard alongside this.)

### Complete code

**On the Pico**, save as `code.py` (unchanged from Phase 1 — this is already the complete,
finished version):

```python
# class-4-code-1.py -- LSM9DS1 over I2C, Mahony-filtered roll/pitch/yaw over serial.
import time
import math
import board
import busio
import adafruit_lsm9ds1

i2c = busio.I2C(board.GP1, board.GP0)
sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

MAHONY_KP = 2.0   # calibrate: drift-vs-jitter tradeoff
MAHONY_KI = 0.05  # calibrate: corrects long-term gyro bias

q0, q1, q2, q3 = 1.0, 0.0, 0.0, 0.0
integral_fbx = integral_fby = integral_fbz = 0.0
last_time = time.monotonic()


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


print("Class 4 project running -- IMU orientation streaming.")

while True:
    now = time.monotonic()
    dt = now - last_time
    last_time = now
    ax, ay, az = sensor.acceleration
    gx, gy, gz = sensor.gyro
    gx, gy, gz = math.radians(gx), math.radians(gy), math.radians(gz)
    mahony_update(ax, ay, az, gx, gy, gz, dt)
    roll, pitch, yaw = quaternion_to_euler()
    print("{:.1f},{:.1f},{:.1f}".format(roll, pitch, yaw))
    time.sleep(0.02)
```

**On your laptop**, run this with `python class-4-code-2.py <port>` (unchanged from Phase 2):

```python
# class-4-code-2.py -- LAPTOP-side live 3D orientation display.
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


def rotation_matrix(roll, pitch, yaw):
    r, p, y = np.radians([roll, pitch, yaw])
    rx = np.array([[1, 0, 0], [0, np.cos(r), -np.sin(r)], [0, np.sin(r), np.cos(r)]])
    ry = np.array([[np.cos(p), 0, np.sin(p)], [0, 1, 0], [-np.sin(p), 0, np.cos(p)]])
    rz = np.array([[np.cos(y), -np.sin(y), 0], [np.sin(y), np.cos(y), 0], [0, 0, 1]])
    return rz @ ry @ rx


plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

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

## 8. What You Learned

You gave your board a sense of orientation and watched it come alive on screen in real time.
Specifically, you now know:

* What an accelerometer and a gyroscope each measure, and where each one is individually
    unreliable (accelerometer noisy under motion, gyroscope drifts over time)
* Why fusing them with a Mahony filter produces a more usable orientation than either alone —
    trusting the gyro for fast changes, correcting toward the accelerometer over time
* How to tune a filter's proportional gain (`MAHONY_KP`) and feel the tradeoff between drift and
    jitter firsthand
* How to stream sensor data from your Pico to a program running on your laptop over serial, and
    turn it into a live visualization

And critically: you also confirmed that knowing which way something is pointed still isn't the
same as knowing how far it has traveled. That's exactly why Class 5 doesn't use the IMU at all to
solve the navigation problem — it takes a completely different approach, using the sensor and
servo you built back in Class 2.

## References

* [Python & CircuitPython — Adafruit LSM9DS1 9-DOF Breakout][01] — Adafruit's official guide for
    wiring and reading the LSM9DS1 over I2C in CircuitPython
* [API Reference — Adafruit LSM9DS1 Library][02] — the `adafruit_lsm9ds1` library API used in this
    script
* [9-DOF LSM9DS1 Breakout Board — Product Page][03] — the IMU used this project

---

[01]:https://learn.adafruit.com/adafruit-lsm9ds1-accelerometer-plus-gyro-plus-magnetometer-9-dof-breakout/python-circuitpython
[02]:https://docs.circuitpython.org/projects/lsm9ds1/en/latest/api.html
[03]:https://www.adafruit.com/product/4634
