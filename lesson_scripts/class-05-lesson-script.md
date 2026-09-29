# Lesson Script: Class 5 — Build the Random Rover: Collision Avoidance


* **Class:** 5 of 6 (plus Pre-Class)
* **Duration:** ~2 hours
* **What You'll Need:** see [Section 2](#2-what-youll-need)
* **Before You Start:** Your Class 2 sensor+servo circuit (`GP6`-`GP8`), Class 3 motor driver
    circuit (`GP9`-`GP12`), and Class 4 IMU (`GP0`/`GP1`) should all still be working exactly as you
    left them. Today the IMU does real work: its magnetometer steers every turn. Class 3's
    wheel-odometry optocouplers (`GP19`/`GP17`) must also stay wired and powered, because the rover
    status website still reports wheel speed/direction from them. Class 1's button/encoder circuit
    isn't needed today, but leave it in place — Class 6 reconnects it. Your Class 4 `rover_server.py`
    should still broadcast the Pico's own WiFi network (access point mode) and serve `/data.json`
    with all seven existing fields — a quick spot-check, not a rebuild. You **won't** need your Class
    3 turn-time calibration notes anymore; you'll see why.

---


## 1. What This Project Is

This is the class where everything you've built so far becomes one robot that makes its own
decisions. You're combining your Class 2 sensor-on-servo sweep, your Class 3 motor driver, and your
Class 4 IMU into a single program: the car drives forward at a constant speed, periodically stops to
sweep the sensor and look for the clearest direction, and turns that way — with an emergency path
that stops and rescans immediately if something gets too close while driving. Two new fixed safety
sensors, a limit switch and an IR obstacle sensor, give your car a last-resort "stop no matter what"
reflex. By the end, your car should drive around the room on its own and steer around at least one
obstacle without you touching it — the central milestone of the whole course.

Today your IMU also gets its missing third sensor. In Class 4 you fused only the accelerometer and
gyroscope, and you watched `yaw` slowly drift even with the board sitting still. Today you'll
calibrate the LSM9DS1's **magnetometer** — a compass built into the same chip — and add it to the
Mahony filter. That anchors yaw to magnetic north, so the rover finally knows which way it's facing
and keeps knowing it. Then you'll put that to work: instead of Class 3's timed turns ("spin for 0.4
seconds and hope that was 90°"), your rover turns **until its compass says it got there**.

The rover status website keeps growing too, and it hits a real turning point. Classes 3 and 4 had to
present the website as a separate, alternative `code.py`, because `rover_server.py` ended in its own
blocking `while True: server.poll()` loop and nothing else could run at the same time. Today's rover
genuinely needs to keep driving, scanning, and checking safety sensors **while** the website stays
live. So `rover_server.py` changes shape — from a self-contained script into a small library that
your rover's own main loop imports and calls each cycle.

## 2. What You'll Need

| Component | Quantity | Purpose This Project |
| :---------- | :--------: | :---------------------- |
| Raspberry Pi Pico 2 W (with header) | 1 | Runs your CircuitPython code |
| HC-SR04 ultrasonic distance sensor (from Class 2) | 1 | Measures distance at each scan angle |
| SG90 micro servo motor (from Class 2) | 1 | Sweeps the sensor across the scan angles |
| DRV8833 dual H-bridge motor driver (from Class 3) | 1 | Drives forward and spins the rover in place for compass-steered turns |
| IR optocoupler wheel-speed sensors (from Class 3) | 2 | Still feed wheel speed/direction to the rover website |
| Adafruit 9-DOF LSM9DS1 IMU breakout (from Class 4) | 1 | Accelerometer + gyroscope + (new today) magnetometer, fused into a drift-free compass heading |
| Micro limit switch | 1 | Physical bumper on the chassis front — last-resort stop-and-reverse on contact |
| IR obstacle avoidance sensor | 1 | Fixed forward-facing near-field detector — stop-and-reverse between ultrasonic scans |
| Emo Smart Robot Car Chassis Kit | 1 | Your completed (or near-complete) car |
| 9V battery clip and 9V battery (from Class 3) | 1 each | Powers the motors (raw, via `VM`) and, through the buck converter, your Pico's own logic power |
| 5V Buck Converter Module (from Class 3) | 1 | Steps the 9V battery down to a regulated 5V for your Pico's `VSYS` power input |
| Breadboard (from prior classes) | 1 | Circuit assembly surface |
| USB cable | 1 | Saving code and reading the serial console — unplug it for floor runs; the rover runs on its 9V battery |
| Laptop with Mu or Thonny | 1 | Where you write/save code and read the serial console |
| Phone with a compass app | shared | Checking your magnetometer's axes and your rover's `heading` |
| (none — the Pico broadcasts its own WiFi network) | — | No classroom WiFi needed: the rover status website runs on the network your Pico creates itself (access point mode, from Class 3) |
| Open floor area with soft obstacles | shared | Test space for autonomous driving runs |

**Homework Assignments** (Section 10) — coming soon; no additional components are needed for this
class yet.

## 3. Meet the Hardware

The only new *parts* today are the two small safety sensors. The one new *sensor* is already on your
rover: the magnetometer inside the LSM9DS1. Here's what each piece contributes.

**From Class 2: the sensor+servo "eyes."** Your HC-SR04, mounted on the SG90 servo, sweeps a small
fixed set of angles (`SCAN_ANGLES`) each time the rover stops to look, then the code picks whichever
angle had the most open space.

**From Class 3: the motor driver "legs."** Your `motor_driver.py` library's `drive(left, right)` and
`stop()` functions move the car. Driving the two wheels in opposite directions spins it in place,
which is how it turns.

**From Class 4, upgraded: the IMU's new sense of direction.** The LSM9DS1 has three sensors, and in
Class 4 you used two. The accelerometer knows which way is *down*, which pins roll and pitch. But
spinning the rover flat on the floor doesn't change which way is down, so nothing corrected yaw, and
the gyro's leftover bias slowly walked it away. The **magnetometer** measures Earth's magnetic field,
which points roughly north. Add it to the Mahony filter and yaw gets its own anchor, exactly the way
gravity anchors roll and pitch: trust the gyro moment-to-moment, nudge toward north over time. The
[IMU and Mahony filter explainer][05] covers this in more depth.

**Why the magnetometer needs calibrating — on the finished rover.** A magnetometer can't tell Earth's
field from any other magnetic field, and your rover carries its own: the motors' permanent magnets,
steel screws, the battery. That extra field is fixed to the rover and turns with it (engineers call
it *hard-iron* distortion). The fix is simple: turn the rover through every orientation while
recording each axis's lowest and highest reading. Earth's field makes each axis swing evenly around a
center point — and that center is your rover's own magnetic junk, which the code then subtracts. That
only works if you calibrate with everything bolted in its final place. Calibrate on the bare
breadboard, then mount it next to a motor, and the numbers are wrong.

**Closed-loop turning.** Class 3's turns were *open-loop*: command a spin, wait a calibrated time,
stop, and never check the result. That's why they drifted as the battery drained or the floor changed
from tile to carpet. Today's turns are *closed-loop*: pick a target heading, spin, check the compass
every 20 ms, and stop when you're within a few degrees. The measurement corrects for the battery, the
floor, and wheel slip automatically. The cost is one new way to fail — if the heading never arrives
(stuck wheel, backwards turn), the rover would spin forever — so the code has a timeout.

**The logic connecting it all: stop-look-go.** Drive straight, and periodically (or immediately, if
something gets too close) stop, sweep, pick the clearest direction, turn to it by compass, and resume.
Stopping to scan is simple and safe, since the sensor never has to interpret a reading taken while the
whole robot is moving — but it's slower than continuously sensing while driving would be.

**Pinout summary** (Class 2, 3, and 4 pins reconnect exactly as wired; `GP5`/`GP13` are new; the
magnetometer uses the same `GP0`/`GP1` I2C wires as the rest of the IMU):

| Pin | What it does | From Class |
| :---- | :--------------- | :----------- |
| `GP0`/`GP1` | LSM9DS1 IMU `SDA`/`SCL` — accelerometer, gyro, and magnetometer | Class 4 |
| `GP6` | HC-SR04 `TRIG` | Class 2 |
| `GP7` | HC-SR04 `ECHO`, through voltage-divider | Class 2 |
| `GP8` | SG90 servo signal | Class 2 |
| `GP9`/`GP10` | DRV8833 `AIN1`/`AIN2` (Motor A) | Class 3 |
| `GP11`/`GP12` | DRV8833 `BIN1`/`BIN2` (Motor B) | Class 3 |
| `GP19`/`GP17` | Wheel-odometry optocouplers (website) | Class 3 |
| `GP5` | Limit switch (internal pull-up) | New this Class |
| `GP13` | IR obstacle sensor `OUT` | New this Class |

## 4. Build It: Phase 1 — Safety Sensors and Magnetometer Calibration

### Wiring for this phase

Reconnect (or simply confirm) your Class 2, 3, and 4 circuits exactly as they were left wired —
except two power wires, below — then add the two new safety sensors:

>**NOTE — move two power wires:** in Class 2 the HC-SR04 `VCC` and the servo's red `+` wire went to
>`VBUS`, which only has power while a USB cable is plugged in. Today the rover drives untethered on
>its 9V battery, so move both of those wires from `VBUS` to the `VSYS` rail (the buck converter's 5V
>output). Same 5V, same signal pins — but now it's there with the USB cable unplugged. Skip this and
>the rover drives off the laptop cable and immediately goes blind: every scan reads an error and the
>servo stops moving.

| Component | Pico 2 W Pin |
| :---------- | :------------- |
| HC-SR04 `TRIG` | `GP6` |
| HC-SR04 `ECHO`, through voltage-divider resistors | `GP7` |
| SG90 servo signal | `GP8` |
| HC-SR04 `VCC` and SG90 `+` (red) | `VSYS` — buck converter 5V rail (**moved** from `VBUS`) |
| Limit switch `NO` (normally-open) terminal | `GP5` (internal pull-up) |
| Limit switch `COM` (common) terminal | `GND` |
| IR obstacle sensor `OUT` | `GP13` |
| IR obstacle sensor `VCC` / `GND` | `3V3` / `GND` (3.3V keeps `OUT` safe for the Pico) |

Mount the limit switch as a physical bumper on the chassis front (lever arm leading, so any contact
presses it), and the IR sensor fixed and forward-facing, low on the chassis, aimed at ground-level
obstacles the ultrasonic sweep might miss between scans.

Then check where your IMU sits. Mount it where it will stay for the rest of the course, as far from
the motors and battery as the chassis allows. **Every calibration from here on assumes the IMU never
moves relative to the motors.** If you remount it later, rerun this phase's calibration.

Before any new code, re-verify each older circuit independently: a quick sensor sweep, a quick motor
forward/reverse, and the Class 4 website's roll/pitch/yaw. Catching a regression now is far easier
than debugging it once it's buried inside the combined rover logic.

### Software for this phase

One new, one-time program. It only reads the IMU, so it doesn't need any of your other files.

| Software component | New, modified, or unchanged | What it does |
| :------------------- | :-------------------------- | :----------- |
| `code.py` | **New** — `class-5-mag-calibration.py` | Records the magnetometer's lowest and highest reading on each axis while you tumble the rover, prints the `MAG_OFFSET` line to paste into `rover_server.py`, then prints live corrected readings for the axis check. |
| `adafruit_lsm9ds1.mpy` (in `/lib`) | **Unchanged** — from Class 4 | The IMU driver; its `magnetic` property returns the magnetometer reading in gauss. |

### What this code does

For 30 seconds, the program reads the magnetometer every 20 ms and remembers each axis's lowest and
highest value. While you tumble the rover, Earth's field swings each axis up and down by the same
amount, so the midpoint `(low + high) / 2` is whatever field the rover itself adds. That midpoint is
the offset, printed as a ready-to-paste `MAG_OFFSET = (...)` line. It also prints each axis's
*span* (`high - low`): if you tumbled properly, the three spans come out roughly equal.

Then it switches to an **axis check**. On the LSM9DS1, the magnetometer's X axis points the opposite
way from the accelerometer's and gyroscope's X axis. The filter needs all three sensors to agree on
which way X, Y, and Z point, so the code multiplies each magnetometer axis by `MAG_AXIS_SIGN`
(`-1` flips it). The axis check lets you confirm those signs with a phone compass instead of taking
them on faith.

### The code

Save this as `code.py`. It replaces whatever was there, just for this one-time step — you'll put the
rover code back in Phase 2.

```python
# class-5-mag-calibration.py -- save as code.py, run ONCE on the fully assembled rover.
# Finds the rover's own magnetic offset (hard-iron calibration), then prints
# corrected readings so you can check the magnetometer's axis directions.
import time
import board
import busio
import adafruit_lsm9ds1

CAL_SECONDS = 30               # how long to turn and tumble the rover
MAG_AXIS_SIGN = (-1, 1, 1)     # [VERIFY] LSM9DS1 mag X axis points opposite the accel/gyro X axis

i2c = busio.I2C(board.GP1, board.GP0)  # SCL, SDA -- same wiring as Class 4
imu = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

lows = [float("inf")] * 3
highs = [float("-inf")] * 3

print("Magnetometer calibration starts in 3 s -- pick up the rover.")
time.sleep(3)
print("GO: slowly turn and tumble the rover through every orientation for", CAL_SECONDS, "s")
end_time = time.monotonic() + CAL_SECONDS
while time.monotonic() < end_time:
    for axis, value in enumerate(imu.magnetic):  # gauss
        lows[axis] = min(lows[axis], value)
        highs[axis] = max(highs[axis], value)
    time.sleep(0.02)

# The center of each axis's swing is the rover's own magnetic offset.
offset = tuple(round((low + high) / 2, 3) for low, high in zip(lows, highs))
spans = tuple(round(high - low, 3) for low, high in zip(lows, highs))
print("Done. Copy this line into rover_server.py:")
print("MAG_OFFSET =", offset)
print("Spans (gauss) -- should be roughly equal:", spans)

print("Axis check: corrected mx, my, mz every half second (Ctrl-C to stop)")
while True:
    corrected = [sign * (raw - off)
                 for raw, off, sign in zip(imu.magnetic, offset, MAG_AXIS_SIGN)]
    print("mx {:+.2f}  my {:+.2f}  mz {:+.2f}".format(*corrected))
    time.sleep(0.5)
```

### Try it / what you should see

Take the fully assembled rover — battery in, everything mounted — to a spot away from big steel:
not a metal desk, not next to desk legs, radiators, or a pile of laptops. Anything magnetic nearby
gets baked into your offsets. Save the file and pick up the rover. When the console says `GO`,
slowly turn and tumble it through every orientation for the full 30 seconds: spin it flat, roll it
onto each side, tip it nose-up and nose-down, and even upside down. Then you'll see something like:

```text
Done. Copy this line into rover_server.py:
MAG_OFFSET = (0.142, -0.071, 0.058)
Spans (gauss) -- should be roughly equal: (0.98, 1.02, 0.95)
```

Copy your `MAG_OFFSET` line into your build journal — you'll paste it into `rover_server.py` in
Phase 2. Your numbers will be different; every rover's magnetic junk is its own.

Now the **axis check**. Lay the rover flat and use a phone compass to find north:

* Point the board's printed **X** arrow north → `mx` should be clearly positive (its largest value).
* Point the board's printed **Y** arrow north → `my` should be clearly positive.
* Lying flat, anywhere in the northern hemisphere → `mz` should be negative. Earth's field doesn't
    run level; it dips steeply down into the ground.

If one check comes out backwards, flip that entry of `MAG_AXIS_SIGN` (for example `(-1, 1, 1)` →
`(1, 1, 1)`) here and in `rover_server.py` in Phase 2, then rerun this program.

If the spans come out very unequal, like `(0.9, 0.9, 0.1)`, you only spun the rover flat and never
rolled it onto its sides. Run it again with a bigger tumble.

### Checkpoint

You have a `MAG_OFFSET = (...)` line in your build journal, three roughly equal spans, and an axis
check that passes all three tests. Be able to say, in one sentence, why you calibrated with the rover
fully assembled instead of on the bare breadboard. Finally, check the two new safety sensors with a
multimeter or by eye: the limit switch lever should click when pressed, and the IR sensor's onboard
LED should light when you hold your hand a few centimeters in front of it.

## 5. Build It: Phase 2 — Upgrade `rover_server.py`: 9-DOF Filter, Compass Heading, Library Mode

### Wiring for this phase

No new wiring. The magnetometer is inside the same LSM9DS1, on the same `GP0`/`GP1` I2C wires you
connected in Class 4. This phase edits software only.

### Software for this phase

`rover_server.py` gets three upgrades at once, plus a tiny temporary `code.py` to test it.

| Software component | New, modified, or unchanged | What it does |
| :------------------- | :-------------------------- | :----------- |
| `rover_server.py` | **Modified** — edits `class-4-phase-4-rover_server.py` | Mahony filter now fuses the magnetometer (9-DOF) and starts at the compass heading; new `latest_heading` and `/data.json` fields `heading`, `scan_heading`, `drive_state`, `stop_reason`; its `while True: server.poll()` loop is removed so other code can import it. |
| `code.py` | **New (temporary)** — Phase 2 test loop | Four lines that keep the filter and website running without driving, so you can test the new heading before the rover code exists. |
| `wheel_odometry.py` | **Unchanged** — `class-3-phase-3-wheel_odometry.py` | Still supplies the wheel speed and direction fields. |
| `motor_driver.py` | **Unchanged** — `class-3-phase-1-motor-driver.py` | Imported by `wheel_odometry` for each wheel's direction. |
| `adafruit_lsm9ds1.mpy`, `adafruit_httpserver` (in `/lib`) | **Unchanged** — from Classes 3-4 | The IMU driver and the web server library. |
| `settings.toml` | **Unchanged** — from Class 3 | Same network name and password for the Pico's WiFi network. |

### What this code does

**1. The magnetometer joins the filter.** In Class 4, every loop `_mahony_update()` asked, "Given the
orientation I think I have, where *should* gravity be?" It compared that with where the accelerometer
says gravity actually is, and the mismatch became the error that `MAHONY_KP` and `MAHONY_KI` nudge
out. Now it asks the same question twice: once about gravity, and once about north. The magnetometer
half is a bit more math — it first figures out what "north" looks like in the world (level with the
floor, plus its downward dip), then where that north should appear to the rover — but the idea is
identical: predicted vs. measured, and the mismatch is error. The two errors simply add. Everything
from the error down is unchanged from Class 4. Because the filter still keeps orientation as a
quaternion (`q0..q3`), adding a third sensor doesn't change anything about how it's stored — see
[What Are Quaternions, and Why Use Them?][06].

**2. It starts facing the right way.** The filter used to start at `q = (1, 0, 0, 0)`, meaning "facing
wherever yaw 0 is." With a magnetometer, it would slowly swing around onto north — but slowly means 30
seconds or more. So `_start_at_compass_heading()` reads the compass once at boot and starts the
filter already pointed the right way. It assumes the rover boots sitting flat, which is why you now
boot it still *and* flat.

**3. A compass heading.** Yaw from the filter grows counter-clockwise, the math convention. A real
compass grows clockwise: 0 is north, 90 is east. `latest_heading = (-yaw) % 360` flips the direction
and wraps it into 0-360, and `/data.json` reports it as `heading`.

**4. Library mode.** Class 4's file ended in `while True: server.poll()`, which owned the Pico
forever. Your Phase 3 rover needs its own loop, and two blocking loops can't run at once. So this file
now stops after `server.start(...)` and hands out three things instead: the `server` object (the rover
calls `server.poll()`), an `update()` function (one filter step — the job Class 4's loop did every 20
ms), and a `scan_status` dict (the rover writes its latest decision there for the website). `/data.json`
gains four fields:

* `heading` — compass degrees, 0-360, clockwise from magnetic north
* `scan_heading` — the last chosen **scan angle** (servo degrees, 90 = straight ahead) — not a
    compass direction
* `drive_state` — `"driving"`, `"scanning"`, or `"stopped"` (`"stopped"` the instant the bump switch
    or IR sensor fires)
* `stop_reason` — `"none"`, `"ultrasonic"`, `"ir"`, or `"limit_switch"`, naming whichever signal most
    recently forced a stop

### The code

Open your existing `rover_server.py` (from Class 4) and edit it into the version below — or save this
file over it directly. **Then replace `MAG_OFFSET = (0.0, 0.0, 0.0)` with your own line from Phase 1**,
and match `MAG_AXIS_SIGN` to whatever passed your axis check.

```python
# rover_server.py -- edited again (same file since Class 3, no new filename).
# Class 5 changes: (1) the Mahony filter also fuses the magnetometer (9-DOF),
# so yaw is anchored to magnetic north; (2) a compass heading, published as a
# new "heading" field; (3) library mode -- no loop of its own. code.py calls
# update() to keep the filter running and server.poll() to answer the browser.
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

i2c = busio.I2C(board.GP1, board.GP0)  # SCL, SDA -- same wiring as Class 4
imu = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

MAHONY_KP = 2.0   # unchanged from Class 4
MAHONY_KI = 0.05  # unchanged from Class 4

# Gyro bias settings -- unchanged from Class 4.
CAL_SAMPLES = 200  # startup calibration: about 2 seconds of readings
STILL_GYRO = 0.02  # rad/s: below this on every axis counts as "still"
STILL_ACCEL = 0.3  # m/s^2: total acceleration this close to 1 g counts as "still"
BIAS_ALPHA = 0.01  # while still, move the bias 1% of the way toward each reading
GRAVITY = 9.81     # m/s^2

# Magnetometer calibration -- new in Class 5.
MAG_OFFSET = (0.0, 0.0, 0.0)  # gauss -- paste YOUR line from class-5-mag-calibration.py
MAG_AXIS_SIGN = (-1, 1, 1)    # [VERIFY] same signs that passed the Phase 1 axis check

q0, q1, q2, q3 = 1.0, 0.0, 0.0, 0.0
integral_fbx = integral_fby = integral_fbz = 0.0
last_time = time.monotonic()


def _mahony_update(ax, ay, az, gx, gy, gz, mx, my, mz, dt):
    """Class 4's filter plus a second reference: north from the magnetometer."""
    global q0, q1, q2, q3, integral_fbx, integral_fby, integral_fbz
    norm = (ax * ax + ay * ay + az * az) ** 0.5
    mag_norm = (mx * mx + my * my + mz * mz) ** 0.5
    if norm == 0 or mag_norm == 0:
        return
    ax, ay, az = ax / norm, ay / norm, az / norm
    mx, my, mz = mx / mag_norm, my / mag_norm, mz / mag_norm

    # Where the filter thinks gravity points (unchanged from Class 4).
    vx = 2 * (q1 * q3 - q0 * q2)
    vy = 2 * (q0 * q1 + q2 * q3)
    vz = q0 * q0 - q1 * q1 - q2 * q2 + q3 * q3

    # Turn the measured field into a world-frame "north" (bx) with its downward
    # dip (bz), then work out where that north should appear to the rover (w).
    hx = 2 * (mx * (0.5 - q2 * q2 - q3 * q3) + my * (q1 * q2 - q0 * q3) + mz * (q1 * q3 + q0 * q2))
    hy = 2 * (mx * (q1 * q2 + q0 * q3) + my * (0.5 - q1 * q1 - q3 * q3) + mz * (q2 * q3 - q0 * q1))
    bx = (hx * hx + hy * hy) ** 0.5
    bz = 2 * (mx * (q1 * q3 - q0 * q2) + my * (q2 * q3 + q0 * q1) + mz * (0.5 - q1 * q1 - q2 * q2))
    wx = 2 * (bx * (0.5 - q2 * q2 - q3 * q3) + bz * (q1 * q3 - q0 * q2))
    wy = 2 * (bx * (q1 * q2 - q0 * q3) + bz * (q0 * q1 + q2 * q3))
    wz = 2 * (bx * (q0 * q2 + q1 * q3) + bz * (0.5 - q1 * q1 - q2 * q2))

    # Error = gravity mismatch (Class 4) + north mismatch (new).
    ex = (ay * vz - az * vy) + (my * wz - mz * wy)
    ey = (az * vx - ax * vz) + (mz * wx - mx * wz)
    ez = (ax * vy - ay * vx) + (mx * wy - my * wx)

    # From here down: identical to Class 4.
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
    """Unchanged from Class 4: average the gyro while the rover sits still."""
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
    """Unchanged from Class 4: tiny rotation AND only gravity on the accelerometer."""
    accel_mag = (ax * ax + ay * ay + az * az) ** 0.5
    return (
        abs(gx) < STILL_GYRO
        and abs(gy) < STILL_GYRO
        and abs(gz) < STILL_GYRO
        and abs(accel_mag - GRAVITY) < STILL_ACCEL
    )


def _read_magnetometer():
    """Calibrated magnetometer reading, axes lined up with the accel/gyro."""
    return tuple(sign * (raw - off)
                 for raw, off, sign in zip(imu.magnetic, MAG_OFFSET, MAG_AXIS_SIGN))


def _start_at_compass_heading():
    """Start the filter already facing the way the compass says. From (1, 0, 0, 0)
    the filter would need 30+ seconds to swing around onto north by itself.
    Assumes the rover boots sitting flat."""
    global q0, q1, q2, q3
    mx, my, _ = _read_magnetometer()
    yaw = math.atan2(-my, mx)
    q0, q1, q2, q3 = math.cos(yaw / 2), 0.0, 0.0, math.sin(yaw / 2)


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
    mx, my, mz = _read_magnetometer()                    # new in Class 5
    if _is_still(ax, ay, az, gx, gy, gz):  # still: leftover reading is bias -- refine it
        bias_x += BIAS_ALPHA * gx
        bias_y += BIAS_ALPHA * gy
        bias_z += BIAS_ALPHA * gz
        integral_fbx = integral_fby = integral_fbz = 0.0  # clear integral windup
    _mahony_update(ax, ay, az, gx, gy, gz, mx, my, mz, dt)
    roll = math.degrees(math.atan2(2 * (q0 * q1 + q2 * q3), 1 - 2 * (q1 * q1 + q2 * q2)))
    pitch = math.degrees(math.asin(max(-1.0, min(1.0, 2 * (q0 * q2 - q3 * q1)))))
    yaw = math.degrees(math.atan2(2 * (q0 * q3 + q1 * q2), 1 - 2 * (q2 * q2 + q3 * q3)))
    return roll, pitch, yaw


# At startup the rover must sit still (gyro bias) AND flat (compass heading).
bias_x, bias_y, bias_z = _calibrate_gyro_bias()
_start_at_compass_heading()
last_time = time.monotonic()

latest_orientation = (0.0, 0.0, 0.0)
latest_heading = 0.0  # compass degrees: 0 = magnetic north, increasing clockwise

# The collision-avoidance decision -- code.py fills these in each cycle.
scan_status = {
    "scan_heading": 90,        # last chosen SCAN angle (servo degrees, 90 = straight ahead)
    "drive_state": "driving",  # "driving" | "scanning" | "stopped"
    "stop_reason": "none",     # "none" | "ultrasonic" | "ir" | "limit_switch"
}


def _update_orientation():
    """Advance the filter one step and remember the results for /data.json."""
    global latest_orientation, latest_heading
    latest_orientation = _read_orientation()
    # yaw grows counter-clockwise; a compass grows clockwise -- flip and wrap to 0-360.
    latest_heading = (-latest_orientation[2]) % 360


def update():
    """One filter step. Class 4's own loop did this every 20 ms; that loop is
    gone, so code.py calls update() instead (through its wait() helper)."""
    _update_orientation()


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
    roll, pitch, yaw = latest_orientation
    return JSONResponse(request, {
        "speed_left_cms": speed_left,
        "dir_left": dir_left,
        "speed_right_cms": speed_right,
        "dir_right": dir_right,
        "roll": roll,
        "pitch": pitch,
        "yaw": yaw,
        "heading": latest_heading,
        "scan_heading": scan_status["scan_heading"],
        "drive_state": scan_status["drive_state"],
        "stop_reason": scan_status["stop_reason"],
    })


@server.route("/")
def index(request: Request):
    return Response(request, STATUS_PAGE, content_type="text/html")


# Port 5000, not 80 -- CircuitPython's Web Workflow may already be using port 80.
server.start(str(ap_ip), port=5000)
print(f"HTTP Server running at http://{ap_ip}:5000")
# No "while True: server.poll()" loop here anymore -- code.py's own main loop
# calls server.poll() and update(), so it can keep driving at the same time.
```

Then, to test it, save this as `code.py` (temporarily — Phase 3 replaces it):

```python
# Phase 2 test only -- keeps the filter and website running without driving.
import time
import rover_server  # boot the rover still and flat: gyro calibration + compass start

while True:
    rover_server.update()
    rover_server.server.poll()
    time.sleep(0.02)
```

### Try it / what you should see

Set the rover down flat and don't touch it while it boots: you'll see the WiFi lines, then
`Calibrating gyro -- keep the rover perfectly still...`, then
`HTTP Server running at http://192.168.4.1:5000`. Join your Pico's WiFi network and open
`http://192.168.4.1:5000` (type the `http://` and the `:5000`). You should see **eleven** fields: the
seven from Classes 3-4, plus `heading`, `scan_heading`, `drive_state`, and `stop_reason`. The last
three won't change yet — nothing is driving.

Now three quick tests:

1. **Does it point north?** Put the phone compass next to the rover. If the board's X arrow points
    along the rover's nose, `heading` should roughly match the phone (within 10-20° is fine — the
    phone has its own errors). If your IMU is mounted sideways, `heading` will be off by a fixed 90°
    or so; that's fine, because the rover only uses heading *changes* to turn.
2. **Does it follow a turn?** Turn the rover clockwise by hand about a quarter turn. `heading` should
    go *up* by about 90.
3. **Does it hold still?** Leave it untouched for a minute. `heading` should stay within a few degrees.
    Compare that with how far `yaw` drifted in Class 4.

### Checkpoint

All eleven fields update live; `heading` goes up about 90 when you turn the rover clockwise a quarter
turn, and holds steady when it sits still for a minute. Be able to explain in one sentence why the
magnetometer fixes yaw drift when the accelerometer couldn't.

## 6. Build It: Phase 3 — The Random Rover With Compass-Steered Turns

### Wiring for this phase

No new wiring — everything from Phase 1 is in place. Put the rover's USB cable aside for floor runs;
it runs on its 9V battery.

### Software for this phase

The rover program replaces Phase 2's temporary test loop. It uses every file you've built so far.

| Software component | New, modified, or unchanged | What it does |
| :------------------- | :-------------------------- | :----------- |
| `code.py` | **New** — `class-5-code.py` | The stop-look-go loop: drive, stop for the timer, an obstacle, the bump switch, or the IR sensor, sweep for the most open direction, turn to it by compass, and repeat — while keeping the website live and `scan_status` up to date. |
| `rover_server.py` | **Unchanged** — from Phase 2 | Supplies `update()`, `latest_heading`, `server`, and `scan_status`. |
| `motor_driver.py` | **Unchanged** — `class-3-phase-1-motor-driver.py` | Drives, stops, reverses, and spins the rover. |
| `wheel_odometry.py` | **Unchanged** — `class-3-phase-3-wheel_odometry.py` | Wheel speed and direction for the website. |
| `adafruit_hcsr04.mpy`, `adafruit_motor` folder (in `/lib`) | **Unchanged** — from Class 2 | Read the ultrasonic sensor and position the scanning servo. |

### What this code does

This is the "stop-look-go" cycle, running forever:

1. Drive forward at `DRIVE_SPEED`, calling `server.poll()` so the website stays live.
2. Keep checking three things: the bump switch or IR sensor (stop, reverse for `BACKOFF_S`, then
    scan), an obstacle closer than `STOP_DISTANCE_CM` (stop and scan), or `SCAN_INTERVAL` running out
    (routine scan).
3. `scan()` sweeps `SCAN_ANGLES`, settling at each one, and returns the angle with the largest
    distance.
4. `turn_toward()` turns that scan angle into a compass target. If the best angle was 150 — 60° right
    of straight ahead — and the rover's heading is 200, the target is 260. It spins toward the target,
    checking the heading every 20 ms, and stops within `HEADING_TOLERANCE_DEG`.
5. Resume driving. Repeat.

Three details in `turn_toward()` are worth a closer look:

* **`heading_error()` handles the wrap-around.** Going from heading 350 to heading 10 is a 20° turn
    right, not a 340° turn left. `(target - heading + 180) % 360 - 180` always gives the short way
    around, as a number from -180 to 180. It's the same 359°-to-1° problem from the
    [quaternion explainer][06], solved for a single angle.
* **Overshoot fixes itself.** If the rover spins past the target, the error changes sign and the next
    loop spins it back. A timed turn can't do that.
* **The website waits during a turn.** `turn_toward()` calls `wait()` but never `server.poll()`,
    because answering a browser request pauses about 0.25 s — long enough to spin well past the
    target. The website catches up as soon as the turn finishes.

Every pause uses `wait()` instead of `time.sleep()`. `wait()` calls `rover_server.update()` every 20
ms, so the filter never misses a turn.

### The code

Save this as `code.py`, replacing Phase 2's test loop. `motor_driver.py`, `wheel_odometry.py`, and
your Phase 2 `rover_server.py` should already be on `CIRCUITPY`.

```python
# class-5-code.py -- save as code.py
# Random Rover: drives forward, rescans on a timer or on proximity, turns toward
# the clearest direction by compass (closed-loop), and reports its decisions on
# the rover status website.
import time
import board
import digitalio
import pwmio
import adafruit_hcsr04
from adafruit_motor import servo
import motor_driver  # from Class 3, must already be on CIRCUITPY
import rover_server  # Phase 2 library version -- importing it calibrates the gyro
                     # and reads the compass, so boot the rover still and flat

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP6, echo_pin=board.GP7)
pwm = pwmio.PWMOut(board.GP8, duty_cycle=0, frequency=50)
scan_servo = servo.Servo(pwm, min_pulse=500, max_pulse=2500)  # recalibrate per servo if needed

# The two fixed safety sensors -- both are digital, LOW when triggered.
bump_switch = digitalio.DigitalInOut(board.GP5)
bump_switch.direction = digitalio.Direction.INPUT
bump_switch.pull = digitalio.Pull.UP  # switch pulls the pin LOW when pressed

ir_sensor = digitalio.DigitalInOut(board.GP13)
ir_sensor.direction = digitalio.Direction.INPUT  # module drives its own LOW-on-detect output

# Tune these for your specific robot -- start conservative and adjust.
DRIVE_SPEED = 0.6                     # same as Class 3's Phase 2 SPEED -- lower it for safer autonomous runs
TURN_SPEED = 0.45                     # spin-in-place speed -- slow enough to stop near the target
SCAN_ANGLES = [30, 60, 90, 120, 150]  # servo degrees, left to right
CENTER_ANGLE = 90                     # servo angle that looks straight ahead
SETTLE_TIME = 0.15                    # seconds -- let the servo stop before trusting a reading
STOP_DISTANCE_CM = 25                 # distance that triggers an immediate rescan
SCAN_INTERVAL = 3.0                   # seconds -- rescan on this timer even if nothing is close
HEADING_TOLERANCE_DEG = 5             # "close enough" to the target heading
TURN_TIMEOUT_S = 3.0                  # give up on a turn whose heading never arrives
BACKOFF_S = 0.3                       # reverse time after a safety stop


def wait(seconds):
    """Drop-in for time.sleep() that keeps rover_server's IMU filter running
    about every 20 ms -- otherwise the heading would miss motion made while sleeping."""
    end_time = time.monotonic() + seconds
    while time.monotonic() < end_time:
        rover_server.update()
        time.sleep(0.02)


def read_distance():
    """Distance in cm, or None if the sensor missed its echo."""
    try:
        return sonar.distance
    except RuntimeError:
        return None


def scan():
    """Sweep SCAN_ANGLES and return the angle with the most open space."""
    readings = {}
    for angle in SCAN_ANGLES:
        scan_servo.angle = angle
        wait(SETTLE_TIME)
        readings[angle] = read_distance()
        print("scan: angle", angle, "distance_cm", readings[angle])
    scan_servo.angle = CENTER_ANGLE
    valid = {a: d for a, d in readings.items() if d is not None}
    best_angle = max(valid, key=valid.get) if valid else CENTER_ANGLE
    print("scan: chosen angle", best_angle)
    return best_angle


def heading_error(target):
    """Signed degrees from the current heading to target, -180..180 (+ = turn right).
    The +180 / % 360 / -180 trick makes 350 -> 10 a 20-degree turn, not 340."""
    return (target - rover_server.latest_heading + 180) % 360 - 180


def turn_toward(angle):
    """Spin in place until the compass heading points where the scan angle did."""
    degrees_off_center = angle - CENTER_ANGLE  # + = right of straight ahead
    if abs(degrees_off_center) < HEADING_TOLERANCE_DEG:
        print("drive: no turn needed")
        return
    target = (rover_server.latest_heading + degrees_off_center) % 360
    print("drive: turning", degrees_off_center, "deg to heading", round(target))
    start = time.monotonic()
    while True:
        error = heading_error(target)
        if abs(error) <= HEADING_TOLERANCE_DEG:
            break
        if time.monotonic() - start > TURN_TIMEOUT_S:
            print("drive: turn timed out, still off by", round(error), "deg")
            break
        if error > 0:
            motor_driver.drive(TURN_SPEED, -TURN_SPEED)   # spin right (clockwise)
        else:
            motor_driver.drive(-TURN_SPEED, TURN_SPEED)   # spin left -- also fixes overshoot
        wait(0.02)  # no server.poll() during a turn: its 0.25 s pause would overshoot
    motor_driver.stop()
    print("drive: heading now", round(rover_server.latest_heading))


def safety_override_triggered():
    """Check the bump switch and IR sensor; return which one fired, or "none"."""
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
    rover_server.server.poll()  # answer any pending website request
    rover_server.scan_status["drive_state"] = "driving"
    print("drive: forward, heading", round(rover_server.latest_heading))
    motor_driver.drive(DRIVE_SPEED, DRIVE_SPEED)

    stop_reason = "none"
    while True:
        rover_server.server.poll()
        stop_reason = safety_override_triggered()
        if stop_reason != "none":
            rover_server.scan_status["drive_state"] = "stopped"
            motor_driver.stop()
            print("drive: emergency stop-and-reverse (safety override)")
            motor_driver.drive(-DRIVE_SPEED, -DRIVE_SPEED)
            wait(BACKOFF_S)  # back off enough to clear whatever triggered it
            motor_driver.stop()
            break
        distance = read_distance()
        if distance is not None and distance < STOP_DISTANCE_CM:
            print("drive: obstacle close, distance_cm", distance)
            stop_reason = "ultrasonic"
            break
        if time.monotonic() - last_scan_time >= SCAN_INTERVAL:
            break
        wait(0.05)

    rover_server.scan_status["stop_reason"] = stop_reason
    rover_server.scan_status["drive_state"] = "scanning"
    motor_driver.stop()
    print("drive: stopped for scan" if stop_reason == "none" else "drive: emergency stop for scan")
    best_angle = scan()
    rover_server.scan_status["scan_heading"] = best_angle
    turn_toward(best_angle)
    last_scan_time = time.monotonic()
```

### Try it / what you should see

**First, a turn test.** Compass turns need real rotation, so do this on the floor. Temporarily set
`SCAN_ANGLES = [150]` so every scan picks "60° right." Boot the rover still and flat, then watch the
console: every cycle should print `drive: turning 60 deg to heading ...` followed by
`drive: heading now ...` within about 5 of the target, and never `turn timed out`. Put `SCAN_ANGLES`
back when it passes.

**Then the real run.** Set the rover down and watch the console: `drive: forward, heading ...`, then
either `drive: stopped for scan` (timer) or `drive: emergency stop for scan` (something got close), a
`scan: angle ... distance_cm ...` line for each angle, `scan: chosen angle ...`, then the turning and
`heading now` lines (or `drive: no turn needed`), and back to `drive: forward`. On the floor you should
see the car drive, pause, sweep, turn crisply to the new direction, and continue — on its own.

Open the website on your laptop: `drive_state` flips between `"driving"` and `"scanning"` as the rover
cycles, `scan_heading` shows the chosen angle, `heading` swings with each turn, and `stop_reason` names
whatever last forced a stop.

A first run doesn't need to be perfect. A turn that wiggles a little before stopping, or an overly
cautious `STOP_DISTANCE_CM`, is normal before you tune it. Things to try once it works:

* **Timed vs. compass showdown.** Run the `[150]` turn test five times on a hard floor and five times
    on carpet or a rug, noting `heading now` each time. Compare with how Class 3's timed turn did on
    two different surfaces.
* **Motor interference.** With the rover still and the website open, watch `heading`, then run the
    motors with the wheels lifted off the ground. How much does it jump? Does it recover when they
    stop? That jump is the field from the motor *current*, which calibration can't remove.

### Checkpoint

Your rover completes at least one full stop-look-go cycle — drive, stop, scan with printed readings,
compass turn with `heading now` printed, resume driving — without you touching it once it starts.
Place an obstacle in its path while it's driving and confirm it stops immediately (an `emergency stop
for scan` line), not waiting for the timer. Press the limit switch by hand and confirm `SAFETY: bump
switch contact` and a stop-and-reverse; wave your hand in front of the IR sensor and confirm `SAFETY:
IR sensor near-field obstacle`. On the website, confirm all eleven fields update, with `stop_reason`
naming each of those.

>**NOTE — known limitation:** each time the browser asks for `/data.json`, `read_speed()` spends
>about 0.25 s counting wheel ticks, and it does that *inside* `rover_server.server.poll()`. So while
>the status page is open, the drive loop — including the bump-switch and IR checks — can pause for
>up to 0.25 s about twice a second. Turns are protected (they never poll), but for the quickest
>reflexes while driving, close the browser tab. Removing the pause for real means counting wheel
>ticks without blocking, a redesign of `wheel_odometry.py` left for a future version of the course.

## 7. Troubleshooting Guide

| Problem | Likely Cause | Fix |
| :-------- | :------------- | :---- |
| Calibration spans very unequal, e.g. `(0.9, 0.9, 0.1)` | Rover only spun flat, never tumbled onto its sides | Rerun `class-5-mag-calibration.py`; roll the rover onto every side and tip it nose-up/nose-down |
| Calibration spans all tiny (under ~0.2), or `magnetic` never changes | IMU not responding on I2C, or you calibrated on top of a big steel surface | Check `SDA`/`SCL` (does roll/pitch still work?); move to a wooden or plastic table |
| Axis check: `mx` or `my` negative when its arrow points north, or `mz` positive lying flat | That magnetometer axis is flipped relative to the accel/gyro | Flip that entry in `MAG_AXIS_SIGN`, in both the calibration program and `rover_server.py` |
| `heading` disagrees with the phone compass from boot, and creeps back after a hand turn | `MAG_AXIS_SIGN` wrong, so the magnetometer and gyro disagree | Redo the Phase 1 axis check |
| `heading` was fine, now wrong by the same amount everywhere | IMU remounted, or moved closer to the motors/battery, after calibration | Rerun the Phase 1 calibration with the IMU in its final position |
| `heading` a few degrees off at boot, slowly correcting for a minute | Rover booted on a tilt, so the starting compass reading was skewed | Restart it sitting flat and still; turns still work meanwhile, since they use heading changes |
| `heading` jumps 10-20° when the motors start | Magnetic field from the motor current — calibration can't remove it | Mount the IMU farther from the motors and battery (higher, on a standoff); small jumps are expected and the filter smooths them |
| `heading` wrong only near certain furniture or spots on the floor | Steel desks, cabinets, radiators, or rebar bending the local field | Test in a clearer area — a real-world limitation, not a bug |
| Rover spins until `drive: turn timed out` | Turn direction and heading disagree, or `TURN_SPEED` too low to move the car | Turn the rover clockwise by hand: `heading` must go up. If it does, swap the two `motor_driver.drive()` calls in `turn_toward()`; if the wheels barely move, raise `TURN_SPEED` |
| Turn overshoots and wiggles back and forth before stopping | `TURN_SPEED` too high, or `HEADING_TOLERANCE_DEG` too tight | Lower `TURN_SPEED` in 0.05 steps, or raise the tolerance to 8 |
| Rover doesn't drive at all | `motor_driver.py` missing from `CIRCUITPY`, or the 9V battery is dead | Confirm `motor_driver.py` is present alongside `code.py`; check battery voltage |
| `ImportError` for `rover_server` or `wheel_odometry` | File missing from `CIRCUITPY` | Copy your Phase 2 `rover_server.py` and Class 3's `wheel_odometry.py` back onto the drive |
| Works on the laptop cable, but unplugged every scan reads `None` and the servo stops moving | HC-SR04 and servo still powered from `VBUS`, which is dead without USB | Move HC-SR04 `VCC` and servo `+` from `VBUS` to the `VSYS` rail (buck converter 5V) |
| Pico doesn't power on when running off battery (no USB) | Buck converter miswired, or its output isn't reaching `VSYS` | Verify buck converter IN from 9V battery, OUT to Pico `VSYS`/`GND`; confirm its output trimpot (if adjustable) is set to 5V |
| Rover drives but never stops to scan | `SCAN_INTERVAL` too long, or `STOP_DISTANCE_CM` too small to ever trigger | Lower `SCAN_INTERVAL` and/or raise `STOP_DISTANCE_CM` and re-test |
| Rover stops constantly, barely drives | `STOP_DISTANCE_CM` set too large, triggering on normal sensor noise | Lower `STOP_DISTANCE_CM` in small steps |
| Rover always chooses angle 90, whatever is around it | Scan readings all coming back `None`, falling back to `CENTER_ANGLE` every time | Check the Class 2 sensor wiring; confirm `read_distance()` isn't always returning `None` |
| Console floods with `None` distances during a scan | Servo moved before the sensor settled, or the sensor is aimed at an out-of-range surface | Increase `SETTLE_TIME`; re-aim the test area to stay within the sensor's usable range |
| Bump switch never triggers even on a hard hit | Lever arm not leading the chassis edge, or `GP5` wiring loose | Reposition the switch so the lever leads the chassis edge; check wiring with a multimeter continuity test |
| Rover constantly emergency-stops with nothing nearby | IR sensor's sensitivity trimmer set too high, or aimed at a reflective floor | Turn the trimmer down; re-aim slightly upward off the floor |
| Rover backs into something behind it after a safety stop | `BACKOFF_S` too long for the available clearance | Shorten `BACKOFF_S` |
| Website's new fields never appear or never change | Old Class 4 `rover_server.py` still on `CIRCUITPY`, or its old `while True: server.poll()` loop wasn't removed | Confirm only one `rover_server.py` exists and it's the Class 5 version |
| Website hangs once the rover starts driving | Both files have their own blocking loop calling `server.poll()` | Delete the old `while True: server.poll()` block from `rover_server.py` entirely |
| `NameError` or `AttributeError` mentioning `scan_status`, `server`, or `latest_heading` | `code.py` references them directly instead of through `rover_server.` | Prefix each with `rover_server.` everywhere `code.py` reads or updates it |
| Rover reacts late to the bump switch/IR sensor only while the status page is open | Each `/data.json` request blocks ~0.25 s in `read_speed()` (see the known-limitation note) | Expected with the page open; close the browser tab for the quickest reflexes |
| Website's wheel-speed or orientation fields stopped updating | `GP19`/`GP17` or `GP0`/`GP1` wiring bumped while wiring the safety sensors | Re-verify those circuits — they're unrelated to today's `GP5`/`GP13` wiring |

## 8. Put It All Together

This is the finished project in one place. Unlike Classes 3 and 4, there's no Option A/B split:
because `rover_server.py` is now a library, one `code.py` runs the rover *and* keeps the website
alive. The magnetometer calibration program from Phase 1 is a one-time tool; rerun it only if you
move the IMU or change what's mounted near it.

### Complete wiring

| Component | Pico 2 W Pin |
| :---------- | :------------- |
| LSM9DS1 IMU `SDA`/`SCL` (accelerometer, gyro, magnetometer) | `GP0`/`GP1` |
| Limit switch `NO` (normally-open) terminal | `GP5` (internal pull-up) |
| Limit switch `COM` (common) terminal | `GND` |
| HC-SR04 `TRIG` | `GP6` |
| HC-SR04 `ECHO`, through voltage-divider resistors | `GP7` |
| SG90 servo signal | `GP8` |
| HC-SR04 `VCC` and SG90 `+` (red) | `VSYS` (buck converter 5V rail) |
| DRV8833 `AIN1`/`AIN2` (Motor A) | `GP9`/`GP10` |
| DRV8833 `BIN1`/`BIN2` (Motor B) | `GP11`/`GP12` |
| IR obstacle sensor `OUT` | `GP13` |
| IR obstacle sensor `VCC` / `GND` | `3V3` / `GND` (3.3V keeps `OUT` safe for the Pico) |
| Wheel-odometry optocouplers (left / right) | `GP19`/`GP17` |

### Complete code

You need **four files** on your `CIRCUITPY` drive: `motor_driver.py` and `wheel_odometry.py`
(unchanged from Class 3), `rover_server.py`, and `code.py` below. Remember to put your own
`MAG_OFFSET` (and, if you changed it, `MAG_AXIS_SIGN`) into `rover_server.py`.

`rover_server.py` — the file you've grown since Class 3, now a 9-DOF library:

```python
# rover_server.py -- edited again (same file since Class 3, no new filename).
# Class 5 changes: (1) the Mahony filter also fuses the magnetometer (9-DOF),
# so yaw is anchored to magnetic north; (2) a compass heading, published as a
# new "heading" field; (3) library mode -- no loop of its own. code.py calls
# update() to keep the filter running and server.poll() to answer the browser.
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

i2c = busio.I2C(board.GP1, board.GP0)  # SCL, SDA -- same wiring as Class 4
imu = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

MAHONY_KP = 2.0   # unchanged from Class 4
MAHONY_KI = 0.05  # unchanged from Class 4

# Gyro bias settings -- unchanged from Class 4.
CAL_SAMPLES = 200  # startup calibration: about 2 seconds of readings
STILL_GYRO = 0.02  # rad/s: below this on every axis counts as "still"
STILL_ACCEL = 0.3  # m/s^2: total acceleration this close to 1 g counts as "still"
BIAS_ALPHA = 0.01  # while still, move the bias 1% of the way toward each reading
GRAVITY = 9.81     # m/s^2

# Magnetometer calibration -- new in Class 5.
MAG_OFFSET = (0.0, 0.0, 0.0)  # gauss -- paste YOUR line from class-5-mag-calibration.py
MAG_AXIS_SIGN = (-1, 1, 1)    # [VERIFY] same signs that passed the Phase 1 axis check

q0, q1, q2, q3 = 1.0, 0.0, 0.0, 0.0
integral_fbx = integral_fby = integral_fbz = 0.0
last_time = time.monotonic()


def _mahony_update(ax, ay, az, gx, gy, gz, mx, my, mz, dt):
    """Class 4's filter plus a second reference: north from the magnetometer."""
    global q0, q1, q2, q3, integral_fbx, integral_fby, integral_fbz
    norm = (ax * ax + ay * ay + az * az) ** 0.5
    mag_norm = (mx * mx + my * my + mz * mz) ** 0.5
    if norm == 0 or mag_norm == 0:
        return
    ax, ay, az = ax / norm, ay / norm, az / norm
    mx, my, mz = mx / mag_norm, my / mag_norm, mz / mag_norm

    # Where the filter thinks gravity points (unchanged from Class 4).
    vx = 2 * (q1 * q3 - q0 * q2)
    vy = 2 * (q0 * q1 + q2 * q3)
    vz = q0 * q0 - q1 * q1 - q2 * q2 + q3 * q3

    # Turn the measured field into a world-frame "north" (bx) with its downward
    # dip (bz), then work out where that north should appear to the rover (w).
    hx = 2 * (mx * (0.5 - q2 * q2 - q3 * q3) + my * (q1 * q2 - q0 * q3) + mz * (q1 * q3 + q0 * q2))
    hy = 2 * (mx * (q1 * q2 + q0 * q3) + my * (0.5 - q1 * q1 - q3 * q3) + mz * (q2 * q3 - q0 * q1))
    bx = (hx * hx + hy * hy) ** 0.5
    bz = 2 * (mx * (q1 * q3 - q0 * q2) + my * (q2 * q3 + q0 * q1) + mz * (0.5 - q1 * q1 - q2 * q2))
    wx = 2 * (bx * (0.5 - q2 * q2 - q3 * q3) + bz * (q1 * q3 - q0 * q2))
    wy = 2 * (bx * (q1 * q2 - q0 * q3) + bz * (q0 * q1 + q2 * q3))
    wz = 2 * (bx * (q0 * q2 + q1 * q3) + bz * (0.5 - q1 * q1 - q2 * q2))

    # Error = gravity mismatch (Class 4) + north mismatch (new).
    ex = (ay * vz - az * vy) + (my * wz - mz * wy)
    ey = (az * vx - ax * vz) + (mz * wx - mx * wz)
    ez = (ax * vy - ay * vx) + (mx * wy - my * wx)

    # From here down: identical to Class 4.
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
    """Unchanged from Class 4: average the gyro while the rover sits still."""
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
    """Unchanged from Class 4: tiny rotation AND only gravity on the accelerometer."""
    accel_mag = (ax * ax + ay * ay + az * az) ** 0.5
    return (
        abs(gx) < STILL_GYRO
        and abs(gy) < STILL_GYRO
        and abs(gz) < STILL_GYRO
        and abs(accel_mag - GRAVITY) < STILL_ACCEL
    )


def _read_magnetometer():
    """Calibrated magnetometer reading, axes lined up with the accel/gyro."""
    return tuple(sign * (raw - off)
                 for raw, off, sign in zip(imu.magnetic, MAG_OFFSET, MAG_AXIS_SIGN))


def _start_at_compass_heading():
    """Start the filter already facing the way the compass says. From (1, 0, 0, 0)
    the filter would need 30+ seconds to swing around onto north by itself.
    Assumes the rover boots sitting flat."""
    global q0, q1, q2, q3
    mx, my, _ = _read_magnetometer()
    yaw = math.atan2(-my, mx)
    q0, q1, q2, q3 = math.cos(yaw / 2), 0.0, 0.0, math.sin(yaw / 2)


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
    mx, my, mz = _read_magnetometer()                    # new in Class 5
    if _is_still(ax, ay, az, gx, gy, gz):  # still: leftover reading is bias -- refine it
        bias_x += BIAS_ALPHA * gx
        bias_y += BIAS_ALPHA * gy
        bias_z += BIAS_ALPHA * gz
        integral_fbx = integral_fby = integral_fbz = 0.0  # clear integral windup
    _mahony_update(ax, ay, az, gx, gy, gz, mx, my, mz, dt)
    roll = math.degrees(math.atan2(2 * (q0 * q1 + q2 * q3), 1 - 2 * (q1 * q1 + q2 * q2)))
    pitch = math.degrees(math.asin(max(-1.0, min(1.0, 2 * (q0 * q2 - q3 * q1)))))
    yaw = math.degrees(math.atan2(2 * (q0 * q3 + q1 * q2), 1 - 2 * (q2 * q2 + q3 * q3)))
    return roll, pitch, yaw


# At startup the rover must sit still (gyro bias) AND flat (compass heading).
bias_x, bias_y, bias_z = _calibrate_gyro_bias()
_start_at_compass_heading()
last_time = time.monotonic()

latest_orientation = (0.0, 0.0, 0.0)
latest_heading = 0.0  # compass degrees: 0 = magnetic north, increasing clockwise

# The collision-avoidance decision -- code.py fills these in each cycle.
scan_status = {
    "scan_heading": 90,        # last chosen SCAN angle (servo degrees, 90 = straight ahead)
    "drive_state": "driving",  # "driving" | "scanning" | "stopped"
    "stop_reason": "none",     # "none" | "ultrasonic" | "ir" | "limit_switch"
}


def _update_orientation():
    """Advance the filter one step and remember the results for /data.json."""
    global latest_orientation, latest_heading
    latest_orientation = _read_orientation()
    # yaw grows counter-clockwise; a compass grows clockwise -- flip and wrap to 0-360.
    latest_heading = (-latest_orientation[2]) % 360


def update():
    """One filter step. Class 4's own loop did this every 20 ms; that loop is
    gone, so code.py calls update() instead (through its wait() helper)."""
    _update_orientation()


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
    roll, pitch, yaw = latest_orientation
    return JSONResponse(request, {
        "speed_left_cms": speed_left,
        "dir_left": dir_left,
        "speed_right_cms": speed_right,
        "dir_right": dir_right,
        "roll": roll,
        "pitch": pitch,
        "yaw": yaw,
        "heading": latest_heading,
        "scan_heading": scan_status["scan_heading"],
        "drive_state": scan_status["drive_state"],
        "stop_reason": scan_status["stop_reason"],
    })


@server.route("/")
def index(request: Request):
    return Response(request, STATUS_PAGE, content_type="text/html")


# Port 5000, not 80 -- CircuitPython's Web Workflow may already be using port 80.
server.start(str(ap_ip), port=5000)
print(f"HTTP Server running at http://{ap_ip}:5000")
# No "while True: server.poll()" loop here anymore -- code.py's own main loop
# calls server.poll() and update(), so it can keep driving at the same time.
```

`code.py` — the complete Random Rover:

```python
# code.py -- complete Random Rover, identical to Phase 3's class-5-code.py.
# Random Rover: drives forward, rescans on a timer or on proximity, turns toward
# the clearest direction by compass (closed-loop), and reports its decisions on
# the rover status website.
import time
import board
import digitalio
import pwmio
import adafruit_hcsr04
from adafruit_motor import servo
import motor_driver  # from Class 3, must already be on CIRCUITPY
import rover_server  # Phase 2 library version -- importing it calibrates the gyro
                     # and reads the compass, so boot the rover still and flat

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP6, echo_pin=board.GP7)
pwm = pwmio.PWMOut(board.GP8, duty_cycle=0, frequency=50)
scan_servo = servo.Servo(pwm, min_pulse=500, max_pulse=2500)  # recalibrate per servo if needed

# The two fixed safety sensors -- both are digital, LOW when triggered.
bump_switch = digitalio.DigitalInOut(board.GP5)
bump_switch.direction = digitalio.Direction.INPUT
bump_switch.pull = digitalio.Pull.UP  # switch pulls the pin LOW when pressed

ir_sensor = digitalio.DigitalInOut(board.GP13)
ir_sensor.direction = digitalio.Direction.INPUT  # module drives its own LOW-on-detect output

# Tune these for your specific robot -- start conservative and adjust.
DRIVE_SPEED = 0.6                     # same as Class 3's Phase 2 SPEED -- lower it for safer autonomous runs
TURN_SPEED = 0.45                     # spin-in-place speed -- slow enough to stop near the target
SCAN_ANGLES = [30, 60, 90, 120, 150]  # servo degrees, left to right
CENTER_ANGLE = 90                     # servo angle that looks straight ahead
SETTLE_TIME = 0.15                    # seconds -- let the servo stop before trusting a reading
STOP_DISTANCE_CM = 25                 # distance that triggers an immediate rescan
SCAN_INTERVAL = 3.0                   # seconds -- rescan on this timer even if nothing is close
HEADING_TOLERANCE_DEG = 5             # "close enough" to the target heading
TURN_TIMEOUT_S = 3.0                  # give up on a turn whose heading never arrives
BACKOFF_S = 0.3                       # reverse time after a safety stop


def wait(seconds):
    """Drop-in for time.sleep() that keeps rover_server's IMU filter running
    about every 20 ms -- otherwise the heading would miss motion made while sleeping."""
    end_time = time.monotonic() + seconds
    while time.monotonic() < end_time:
        rover_server.update()
        time.sleep(0.02)


def read_distance():
    """Distance in cm, or None if the sensor missed its echo."""
    try:
        return sonar.distance
    except RuntimeError:
        return None


def scan():
    """Sweep SCAN_ANGLES and return the angle with the most open space."""
    readings = {}
    for angle in SCAN_ANGLES:
        scan_servo.angle = angle
        wait(SETTLE_TIME)
        readings[angle] = read_distance()
        print("scan: angle", angle, "distance_cm", readings[angle])
    scan_servo.angle = CENTER_ANGLE
    valid = {a: d for a, d in readings.items() if d is not None}
    best_angle = max(valid, key=valid.get) if valid else CENTER_ANGLE
    print("scan: chosen angle", best_angle)
    return best_angle


def heading_error(target):
    """Signed degrees from the current heading to target, -180..180 (+ = turn right).
    The +180 / % 360 / -180 trick makes 350 -> 10 a 20-degree turn, not 340."""
    return (target - rover_server.latest_heading + 180) % 360 - 180


def turn_toward(angle):
    """Spin in place until the compass heading points where the scan angle did."""
    degrees_off_center = angle - CENTER_ANGLE  # + = right of straight ahead
    if abs(degrees_off_center) < HEADING_TOLERANCE_DEG:
        print("drive: no turn needed")
        return
    target = (rover_server.latest_heading + degrees_off_center) % 360
    print("drive: turning", degrees_off_center, "deg to heading", round(target))
    start = time.monotonic()
    while True:
        error = heading_error(target)
        if abs(error) <= HEADING_TOLERANCE_DEG:
            break
        if time.monotonic() - start > TURN_TIMEOUT_S:
            print("drive: turn timed out, still off by", round(error), "deg")
            break
        if error > 0:
            motor_driver.drive(TURN_SPEED, -TURN_SPEED)   # spin right (clockwise)
        else:
            motor_driver.drive(-TURN_SPEED, TURN_SPEED)   # spin left -- also fixes overshoot
        wait(0.02)  # no server.poll() during a turn: its 0.25 s pause would overshoot
    motor_driver.stop()
    print("drive: heading now", round(rover_server.latest_heading))


def safety_override_triggered():
    """Check the bump switch and IR sensor; return which one fired, or "none"."""
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
    rover_server.server.poll()  # answer any pending website request
    rover_server.scan_status["drive_state"] = "driving"
    print("drive: forward, heading", round(rover_server.latest_heading))
    motor_driver.drive(DRIVE_SPEED, DRIVE_SPEED)

    stop_reason = "none"
    while True:
        rover_server.server.poll()
        stop_reason = safety_override_triggered()
        if stop_reason != "none":
            rover_server.scan_status["drive_state"] = "stopped"
            motor_driver.stop()
            print("drive: emergency stop-and-reverse (safety override)")
            motor_driver.drive(-DRIVE_SPEED, -DRIVE_SPEED)
            wait(BACKOFF_S)  # back off enough to clear whatever triggered it
            motor_driver.stop()
            break
        distance = read_distance()
        if distance is not None and distance < STOP_DISTANCE_CM:
            print("drive: obstacle close, distance_cm", distance)
            stop_reason = "ultrasonic"
            break
        if time.monotonic() - last_scan_time >= SCAN_INTERVAL:
            break
        wait(0.05)

    rover_server.scan_status["stop_reason"] = stop_reason
    rover_server.scan_status["drive_state"] = "scanning"
    motor_driver.stop()
    print("drive: stopped for scan" if stop_reason == "none" else "drive: emergency stop for scan")
    best_angle = scan()
    rover_server.scan_status["scan_heading"] = best_angle
    turn_toward(best_angle)
    last_scan_time = time.monotonic()
```

## 9. What You Learned

You built the course's central milestone: a car that senses its surroundings, knows which way it's
facing, and decides where to go, entirely on its own. Specifically, you now know:

* Why yaw drifts with only an accelerometer and gyro, and how a magnetometer gives it an anchor —
    the same "trust the gyro short-term, nudge toward a reference long-term" idea as Class 4, with
    north added to gravity
* Why a magnetometer has to be calibrated on the finished robot: the robot's own magnets and steel
    add a fixed field that turns with it, and the center of each axis's swing is that field
* The difference between an open-loop turn (command it and hope) and a closed-loop turn (measure
    until you get there) — and why every closed-loop controller needs a timeout
* How `heading_error()` finds the short way around a circle, so 350 → 10 is a 20° turn, not 340°
* What "stop-look-go" means as a control pattern, and why it uses two independent triggers (a timer
    and a proximity threshold) to rescan rather than just one
* Why "steer toward the largest reading" is a reasonable default but can pick a bad direction — a
    narrow-but-passable gap and a wide-but-shallow dead end can look alike to a sweep that compares
    single numbers
* Why a safety-critical decision like "stop the car" is stronger backed by multiple independent
    signals (ultrasonic, IR, physical bump) than by one
* Why the rover's need to keep driving *and* keep the website alive finally forced `rover_server.py`
    to become a library instead of a script with its own loop

Next class isn't new concepts — it's finishing and tuning this exact rover, plus optional stretch
goals that bring back your Class 1 encoder. Today's magnetometer calibration, compass turns, website
fields, and the library shape of `rover_server.py` all carry forward into Class 6 unchanged.

---
## 10. Homework Assignment

**Coming soon.** This section will be filled in with
optional take-home exercises, following the same format as the Pre-Class homework in
[`class-00-lesson-script.md`](class-00-lesson-script.md#10-homework-assignment) (what the code
does, full commented code, and real-world examples).

## References

* [What Is an IMU, and What Does a Mahony Filter Do?][05] — the course explainer on the gyro,
    accelerometer, and magnetometer, why yaw drifts, and how Mahony compares to other filters
* [What Are Quaternions, and Why Use Them?][06] — the course explainer on the filter's `q0..q3` and
    the angle wrap-around problem `heading_error()` solves
* [Python & CircuitPython — Adafruit LSM9DS1 9-DOF Breakout][08] — Adafruit's guide, including the
    `magnetic` property used today
* [LSM9DS1 AHRS: Mahony filter and calibration for the LSM9DS1][07] — a reference 9-DOF Mahony
    implementation for this exact chip, with its axis realignment and a more thorough (ellipsoid)
    magnetometer calibration, if you want to go deeper
* [IR Obstacle Avoidance Module][04] — documentation of the breakout board layout and operating principles
* [Raspberry Pi Pico W taught this car to avoid objects][01] — a real-world example of Pico-based obstacle avoidance, similar in spirit to this project
* [How to make an obstacle avoidance robot using Raspberry Pi Pico board][02] — a step-by-step obstacle-avoidance build guide, useful as a cross-reference
* [Obstacle Avoidance Robot Using Raspberry Pi Pico][03] — another worked example combining a distance sensor and motor driver for collision avoidance

---



[01]:https://www.raspberrypi.com/news/raspberry-pi-pico-w-taught-this-car-to-avoid-objects/
[02]:https://srituhobby.com/how-to-make-an-obstacle-avoidance-robot-using-raspberry-pi-pico-board/
[03]:https://circuitdiagrams.in/obstacle-avoidance-robot-using-raspberry-pi/
[04]:https://osoyoo.com/2018/12/21/ir-obstacle-avoidance-module/
[05]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/blob/main/explainers/what-is-an-imu-and-mahony-filter.md
[06]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/blob/main/explainers/what-are-quaternion-and-why-use-them.md
[07]:https://github.com/jremington/LSM9DS1-AHRS
[08]:https://learn.adafruit.com/adafruit-lsm9ds1-accelerometer-plus-gyro-plus-magnetometer-9-dof-breakout/python-circuitpython
