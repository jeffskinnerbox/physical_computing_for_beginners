# Lesson Plan: Class 5 — Build the Random Rover: Collision Avoidance

* **Class:** 5 of 6 (plus Pre-Class)
* **Phase:** Phase 3 — Integration (Class 5-6: combine sensing + motion into an autonomous robot)
* **Duration:** ~2 hours (120 min)
* **Prerequisites from prior Classes:** Classes 1-4 completed — every student has a working
  HC-SR04 + SG90 sensor-sweep circuit (`GP6`-`GP8`, from Class 2), a working DRV8833 motor driver
  circuit (`GP9`-`GP12`, from Class 3), and a working LSM9DS1 IMU (`GP0`/`GP1`, from Class 4) on their
  rover, and is comfortable wiring, saving `code.py`, and reading streamed serial output. Today the
  IMU is no longer just a website passenger: its magnetometer steers every turn. Class 1's
  button/encoder circuit isn't needed for this build, but leave it in place on the breadboard — Class
  6 reconnects it for Stretch 1. The Class 3 wheel-odometry optocouplers (`GP19`/`GP17`) must stay
  wired and powered because the growing rover status website (`rover_server.py`) still reports wheel
  speed/direction from them. The website and the WiFi network the Pico broadcasts (access point mode)
  must still be working — a quick spot-check, not a rebuild.

---

## 1. Class Overview

This is the fifth Class of the course and the first of Phase 3 (Integration) — the Class where
everything built so far comes together into the "Random Rover." Students combine Class 2's
servo-mounted ultrasonic sensor, Class 3's DRV8833 motor driver, and Class 4's IMU into a single
autonomous program: the car drives forward at a constant speed, periodically stops to sweep the
sensor across a set of angles looking for the clearest direction, and turns toward whichever angle had
the most open space — with an interrupt path that stops and rescans immediately if anything gets too
close while driving. Two new fixed safety sensors — a limit switch and an IR obstacle sensor — back up
the ultrasonic sweep with an immediate stop-and-reverse override.

The IMU gets its missing third sensor today. Class 4 fused only the accelerometer and gyroscope, so
nothing anchored yaw and it slowly drifted. Students calibrate the LSM9DS1's magnetometer *on the
finished rover* and add it to the Mahony filter (full 9-DOF fusion), which anchors yaw to magnetic
north. That stable compass heading then replaces Class 3's timed turns: instead of spinning for a
calibrated number of seconds and hoping, the rover turns until its measured heading reaches the
target (closed-loop turning). The magnetometer needs no new wiring — it is inside the same LSM9DS1
on the same I2C bus.

The rover status website keeps growing too. Class 3 gave it wheel speed/direction, Class 4 added
roll/pitch/yaw, and today adds a compass `heading` plus the collision-avoidance decision itself: the
chosen scan angle, whether the car is driving/scanning/stopped, and which safety signal most recently
forced a stop. By the end of the Class, students will have a car that drives around the room on its
own and avoids at least one obstacle without instructor intervention — the course's central
milestone.

## 2. Learning Goals

* Calibrate the IMU's magnetometer on the finished rover and explain, in one sentence, why it has to
  be calibrated there instead of on the bare breadboard
* Upgrade the Class 4 Mahony filter to 9-DOF fusion and show, on the website, that the rover's compass
  heading no longer drifts when it sits still
* Explain the difference between a timed (open-loop) turn and a compass-steered (closed-loop) turn,
  including the new failure mode closed-loop turning adds and how a timeout covers it
* Explain, in plain language, the "stop-look-go" design: drive straight, rescan on a timer, and
  interrupt that timer immediately if an obstacle comes within a stopping distance
* Wire a limit switch and an IR obstacle sensor as fixed safety inputs that trigger an immediate
  stop-and-reverse, overriding the normal scan-and-turn logic
* Extend the rover status website with `heading`, `scan_heading`, `drive_state`, and `stop_reason`,
  so the rover's full state is visible on one page

## 3. Preparation Checklist

* **1-2 days before:** Confirm every student's Class 2 (sensor+servo), Class 3 (motor driver,
  wheel odometry), and Class 4 (IMU) circuits are still intact and power up — a quick visual/serial
  spot-check, not a rebuild. The IMU matters more today than it did in Class 4. (~15 min)
* **1-2 days before:** Confirm every student's `rover_server.py` from Class 4 still broadcasts the
  Pico's own WiFi network and serves `/data.json` with all seven existing fields (wheel
  speed/direction, roll/pitch/yaw). Today's edits start from that exact file. (~10 min)
* **1-2 days before:** On the reference rover, run the magnetometer axis check (Guided Build Step 1)
  and confirm `MAG_AXIS_SIGN = (-1, 1, 1)` is right for the Adafruit LSM9DS1 breakout as mounted. If
  it isn't, work out the correct signs now so you can hand them out, rather than debugging 12 rovers
  live. **[VERIFY]** (~15 min)
* **Day of, before students arrive:**
  * Pick a **calibration spot** away from big steel: not on a metal desk, not next to desk legs,
      radiators, or a pile of laptops. Anything magnetic nearby during calibration gets baked into
      the offsets. A wooden or plastic table in the middle of the room is ideal. (~5 min)
  * Clear a large open floor area (or several smaller zones) for autonomous driving tests, with a
      few soft obstacles (cardboard boxes, foam blocks) placed at varying distances. Keep it away
      from steel furniture where you can; magnetic distortion bends the compass heading. (~10 min)
  * Pre-build one reference rover (sensor+servo+motor driver+IMU, plus the new bump switch and IR
      sensor), calibrate its magnetometer, and test `class-5-code.py` end-to-end. Tune `DRIVE_SPEED`,
      `TURN_SPEED`, `HEADING_TOLERANCE_DEG`, `STOP_DISTANCE_CM`, and the IR sensor's sensitivity
      trimmer so you know what a realistic first run looks like. (~30 min)
  * Confirm the reference Pico's website shows `heading`, `scan_heading`, `drive_state`, and
      `stop_reason` updating live on `/data.json`. (~5 min)
  * Have a phone with a compass app at the instructor bench for the axis check and for "does
      `heading` point roughly north?" questions.
  * Project the instructor's serial console so the whole class can see calibration output, scan
      readings, target headings, and drive state stream by. (~5 min)
  * Have a few spare 9V batteries ready — today's Class runs motors for longer stretches than
      Class 3 did, and the same battery also powers the Pico via the buck converter.
* **Have ready:** Discussion prompts for "why calibrate on the rover?", "timed vs. compass turns",
  the stop-look-go tradeoff, the "largest reading picks a bad direction" scenario, and "how would you
  measure this?" (see Direct Teaching and Wrap-Up below).

## 4. Materials & Components

Per-student unless noted. Component names only — see the course Bill of Materials for costs,
quantities, and sourcing.

| Component | Purpose This Class |
| :---------- | :-------------------- |
| Raspberry Pi Pico 2 W (with header) | Microcontroller running CircuitPython |
| HC-SR04 Ultrasonic Distance Sensor (from Class 2) | Measures distance at each scan angle |
| SG90 Micro Servo Motor (from Class 2) | Sweeps the sensor across `SCAN_ANGLES` |
| DRV8833 Dual H-Bridge DC/Stepper Motor Driver Breakout Board (from Class 3) | Drives the car forward and spins it in place for compass-steered turns |
| IR optocoupler wheel-speed sensors (from Class 3) | Still feed wheel speed/direction to the rover website |
| Adafruit 9-DOF LSM9DS1 IMU Breakout (from Class 4) | Accelerometer + gyroscope + (new today) magnetometer, fused into a drift-free compass heading |
| Micro Limit Switch | Physical bumper on the chassis front — last-resort stop-and-reverse override on contact |
| IR Obstacle Avoidance Sensor | Fixed forward-facing near-field detector — stop-and-reverse override between ultrasonic scans |
| Emo Smart Robot Car Chassis Kit | The completed (or near-complete) car chassis and wheels |
| 9V battery clip and 9V battery (from Class 3) | Powers the motors (raw, via `VM`) and, through the buck converter, the Pico's own logic power |
| 5V Buck Converter Module (from Class 3) | Steps the 9V battery down to a regulated 5V for the Pico's `VSYS` power input |
| Breadboard (830-point, from Class 1) | Circuit assembly surface |
| Dupont jumper wires (shared) | For the two new safety sensors, and reseating anything loose |
| USB cable (student-supplied, from Pre-Class) | Power + serial connection to laptop |
| Windows 11 laptop with Mu or Thonny (student-supplied) | Edit and run CircuitPython code |
| (no classroom WiFi needed) | The Pico 2 W broadcasts its own network (access point mode) for the rover status website, as set up in Class 3 |
| Shared: phone with a compass app | Axis check and sanity-checking the rover's `heading` |
| Shared: open floor area with soft obstacles | Test space for autonomous driving runs |

## 5. Class Timeline

| Segment | Duration |
| :-------- | :--------: |
| 5a. Warm-up / Hook | ~10 min |
| 5b. Introduction | ~5 min |
| 5c. Direct Teaching | ~15 min |
| 5d. Guided Practice (Steps 1-3) | ~55 min |
| 5e. Independent Work | ~25 min |
| 5f. Closing / Wrap-up | ~10 min |

### 5a. Warm-up / Hook — ~10 min

**What to do:** Have every student plug in their Pico 2 W and confirm the Class 2 sensor+servo sweep,
the Class 3 motor forward/reverse/stop test, and the Class 4 website (roll/pitch/yaw) all still work.
Then the hook: have each pair leave their Class 4 rover sitting perfectly still on the table with the
website open, and read `yaw` now and again at the end of warm-up.

**What to say:** "Your rover has eyes from Class 2, legs from Class 3, and a sense of balance from
Class 4. Today it gets a sense of direction — and we're going to use it to steer. First, look at your
`yaw`. Nobody touched these rovers. Why did it move?"

**What to watch for:** Regressions in any prior circuit (loose sensor mount, weak battery, IMU wires
bumped). Fix quickly — today's build depends on all of them working at once.

**Time check:** If more than 2-3 boards need real rework, handle it during Guided Practice instead of
holding up the whole class now.

### 5b. Introduction — ~5 min

**What to do:** Preview the day's two big ideas: the rover's "stop-look-go" behavior, and turning by
compass instead of by clock.

**What to say:**

* "Stop-look-go: drive forward, pause on a timer to sweep and look around, pick the clearest
  direction, turn, and go again. If something gets dangerously close while driving, don't wait for
  the next scheduled look — stop and look right now."
* "In Class 3 you turned by *time*: 'spin for 0.4 seconds, that's about 90 degrees.' Today the rover
  turns by *measurement*: 'keep turning until the compass says I've turned 90 degrees.'"
* "By the end of today, your car should drive around this room by itself and steer around at least
  one obstacle without you touching it."

### 5c. Direct Teaching — ~15 min

No code yet — diagrams and discussion only.

**Concept 1 — Why yaw drifts, and what the magnetometer adds (~3 min).**
Point back to the warm-up yaw reading. Gravity pins down roll and pitch, but spinning the rover flat
doesn't change which way is down — so the accelerometer can't correct yaw, and the gyro's leftover
bias slowly walks it away. The magnetometer measures Earth's magnetic field, which points roughly
north. Adding it to the Mahony filter gives yaw a second "anchor," the same way gravity anchors roll
and pitch: the filter trusts the gyro moment-to-moment and nudges toward north over time. Point
curious students to the [IMU and Mahony filter explainer][01].

**Concept 2 — Why calibrate on the finished rover (~3 min).**
The magnetometer can't tell Earth's field from any other magnetic field. The rover carries its own:
the motors' permanent magnets, steel screws, the battery. Those add a fixed offset that turns with
the rover (called *hard-iron* distortion). Calibration measures that offset by turning the rover
through every orientation: Earth's field shows up as readings swinging evenly around a center, and the
center is the rover's own magnetic junk, which gets subtracted. Ask: "What happens if you calibrate on
the bare breadboard, then bolt it next to the motors?" (The offset changes and the heading is wrong.)
Also mention what calibration *can't* fix: the field from motor *current* only exists while the motors
run, so expect a small heading wobble when they spin up — the filter smooths most of it out.

**Concept 3 — Timed turns vs. compass-steered turns (~3 min).**
Draw both on the board:

* *Open-loop (Class 3):* command a spin, wait a calibrated time, stop. Nobody checks the result. As
  the battery sags or the floor changes from tile to carpet, the same time produces a different angle.
* *Closed-loop (today):* compute a target heading, spin, check the compass every 20 ms, stop when
  within `HEADING_TOLERANCE_DEG`. The measurement corrects for battery, floor, and wheel slip
  automatically.

Ask: "What new way can the closed-loop turn fail that the timed turn couldn't?" Draw out: if the
heading never arrives (wheel stuck, heading reads wrong, turn direction backwards) the rover would spin
forever. That's why the code has `TURN_TIMEOUT_S`. Closed-loop control always needs an "I give up"
path.

**Concept 4 — The stop-look-go control loop (~3 min).**
One cycle, step by step:

1. Car drives forward at `DRIVE_SPEED`.
2. Either the scan timer elapses, or a live distance reading drops below `STOP_DISTANCE_CM`.
3. Motors stop.
4. Servo sweeps across `SCAN_ANGLES`, settling at each (Class 2's `SETTLE_TIME` lesson) and recording
   a distance.
5. Code picks the angle with the largest recorded distance.
6. Code turns that scan angle into a target compass heading and spins until the heading arrives.
7. Car resumes driving straight, and the cycle repeats.

Ask: "What goes wrong if it only rescans on a timer? Only on proximity?" (Timer only: an obstacle can
appear between scans. Proximity only: a shallow-angle miss never triggers a rescan. Two triggers cover
each other's blind spots.)

**Concept 5 — Limits of "steer toward the largest reading," and the stop-look-go tradeoff (~3 min).**
Sketch a narrow gap with open space beyond it, versus a wide-but-shallow alcove. A sweep comparing raw
distances can't tell "large because the space continues" from "large because the beam skimmed past an
edge." Several neighboring angles reading open is a stronger signal than one spike. Then: stopping to
scan is simple and safe, but slow. Ask: "What would a car need to sense continuously while moving?"
(Several fixed sensors at different angles — more parts, less mechanism.)

### 5d. Guided Practice — ~55 min

Instructor builds along on the projector; students wire up and test in parallel.

**Pacing note:** Step 1 (~15 min) and Step 2 (~15 min) are short and mostly copy-and-check; Step 3
(~25 min) is the rover itself. If a group is running behind, have them paste the finished Step 2
`rover_server.py` rather than editing line by line, and move on.

**Wiring — prior circuits stay put, one power change, two new sensors.** Move the HC-SR04 `VCC` and
servo `+` wires from `VBUS` (dead without a USB cable) to the `VSYS` rail fed by the buck converter, so
the sensor and servo work when the rover runs untethered. The only *new* parts are the limit switch
and IR sensor. The magnetometer needs no wiring — it's already inside the LSM9DS1.

| Component | Pico 2 W Pin | From Class |
| :---------- | :------------- | :----------- |
| LSM9DS1 `SDA` / `SCL` (accel + gyro + magnetometer) | `GP0` / `GP1` | Class 4 |
| HC-SR04 `TRIG` | `GP6` | Class 2 |
| HC-SR04 `ECHO` (through voltage-divider) | `GP7` | Class 2 |
| SG90 servo signal | `GP8` | Class 2 |
| HC-SR04 `VCC` and SG90 `+` (red) | `VSYS` — buck converter 5V rail (**moved** from `VBUS`) | Class 2, re-powered |
| DRV8833 `AIN1`/`AIN2` (Motor A) | `GP9`/`GP10` | Class 3 |
| DRV8833 `BIN1`/`BIN2` (Motor B) | `GP11`/`GP12` | Class 3 |
| Wheel-speed optocouplers (left / right) | `GP19` / `GP17` | Class 3 |
| Limit switch `NO` (normally-open) terminal | `GP5` (internal pull-up) | New this Class |
| Limit switch `COM` (common) terminal | `GND` | New this Class |
| IR obstacle sensor `OUT` | `GP13` | New this Class |
| IR obstacle sensor `VCC` / `GND` | `3V3` / `GND` (3.3V keeps `OUT` safe for the Pico) | New this Class |

Mount the limit switch as a physical bumper on the chassis front (lever arm facing forward), and the
IR sensor fixed and forward-facing, low on the chassis. Mount the IMU where it will stay for the rest
of the course — as far from the motors and battery as the chassis allows. **Every later calibration
depends on the IMU not moving relative to the motors.**

**Checkpoint 1:** Before any new code, every pair re-verifies each prior circuit independently
(sensor sweep, motor forward/reverse, website roll/pitch/yaw).

---

**Step 1 — calibrate the magnetometer on the finished rover (~15 min).**
Save `class-5-mag-calibration.py` as `code.py`. Take the fully assembled rover — battery in, everything
mounted — to the calibration spot. When the countdown starts, slowly turn and tumble the rover through
every orientation for 30 seconds: spin it flat, roll it onto each side, tip it nose-up and nose-down.
Then the program prints the offsets and switches to an axis-check mode.

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

**Axis check (instructor demo on the reference rover, students repeat) [VERIFY]:** Lay the rover flat
and use the phone compass to find north.

* Point the board's printed **X** arrow north → `mx` should be clearly positive (its largest value).
* Point the board's printed **Y** arrow north → `my` should be clearly positive.
* Flat on the table in the northern hemisphere → `mz` should be negative (Earth's field dips down
  into the ground).

If one check comes out backwards, flip that entry of `MAG_AXIS_SIGN` (here *and* in
`rover_server.py`). The magnetometer's axes must point the same way as the accelerometer's and gyro's,
or the filter will fight itself.

**What to watch for:** Spans that are very unequal (for example `(0.9, 0.9, 0.1)`) mean the rover was
only spun flat and never tumbled — rerun and roll it onto its sides. Students calibrating at a steel
desk. Students who calibrate, then remount the IMU — the offsets are now wrong.

**Checkpoint 2:** Every pair has a `MAG_OFFSET = (...)` line written in their build journal, roughly
equal spans, and a passing axis check.

---

**Step 2 — upgrade `rover_server.py`: 9-DOF filter, compass heading, library mode (~15 min).**
Three edits to the Class 4 file, all in one pass:

1. **Magnetometer in the filter.** `_mahony_update()` gains `mx, my, mz`. Alongside Class 4's "where
   should gravity be?" check, it now also asks "where should north be?" and adds that mismatch to the
   error. `MAHONY_KP` and `MAHONY_KI` work exactly as before — they just have a second reference to
   nudge toward.
2. **Compass heading.** A new `latest_heading` (0-360°, 0 = magnetic north, increasing clockwise like a
   real compass) and a new `heading` field on `/data.json`.
3. **Library mode.** Class 4's file ended in its own blocking `while True: server.poll()` loop, but
   `class-5-code.py` needs to run its *own* drive loop — two blocking loops can't run at once. So
   `rover_server.py` stops owning the loop and instead exposes `server`, `update()` (one filter step,
   which Class 4's loop used to do every 20 ms), and a `scan_status` dict. This is the refactor
   Class 4 flagged as optional; today it becomes necessary.

```python
# rover_server.py -- edited again (same file from Classes 3-4, no new filename).
# Class 5 changes: (1) the Mahony filter also fuses the magnetometer (9-DOF), so
# yaw is anchored to magnetic north; (2) new latest_heading + "heading" field;
# (3) library mode -- no loop of its own; class-5-code.py calls update() and
# server.poll(). Everything not shown (WiFi setup, i2c/imu, gyro bias
# calibration, _is_still, STATUS_PAGE) stays exactly as Class 4 left it.

MAHONY_KP = 2.0   # unchanged from Class 4
MAHONY_KI = 0.05  # unchanged from Class 4

# Magnetometer calibration -- new in Class 5.
MAG_OFFSET = (0.0, 0.0, 0.0)  # gauss -- paste YOUR line from class-5-mag-calibration.py
MAG_AXIS_SIGN = (-1, 1, 1)    # [VERIFY] same signs that passed the Step 1 axis check


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
    gx, gy, gz = gx - bias_x, gy - bias_y, gz - bias_z
    mx, my, mz = _read_magnetometer()  # new in Class 5
    if _is_still(ax, ay, az, gx, gy, gz):
        bias_x += BIAS_ALPHA * gx
        bias_y += BIAS_ALPHA * gy
        bias_z += BIAS_ALPHA * gz
        integral_fbx = integral_fby = integral_fbz = 0.0
    _mahony_update(ax, ay, az, gx, gy, gz, mx, my, mz, dt)
    roll = math.degrees(math.atan2(2 * (q0 * q1 + q2 * q3), 1 - 2 * (q1 * q1 + q2 * q2)))
    pitch = math.degrees(math.asin(max(-1.0, min(1.0, 2 * (q0 * q2 - q3 * q1)))))
    yaw = math.degrees(math.atan2(2 * (q0 * q3 + q1 * q2), 1 - 2 * (q2 * q2 + q3 * q3)))
    return roll, pitch, yaw


bias_x, bias_y, bias_z = _calibrate_gyro_bias()  # unchanged: rover must sit still at boot
_start_at_compass_heading()                       # new: rover must also sit flat at boot
last_time = time.monotonic()

latest_orientation = (0.0, 0.0, 0.0)
latest_heading = 0.0  # compass degrees: 0 = magnetic north, increasing clockwise

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
    gone, so class-5-code.py calls update() instead (via its wait() helper)."""
    _update_orientation()


@server.route("/data.json")
def data_json(request: Request):
    # Unchanged from Class 4: keep the filter running during read_speed()'s 0.25 s window.
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


server.start(str(ap_ip), port=5000)  # port 5000, not 80 -- Web Workflow may hold port 80
print(f"HTTP Server running at http://{ap_ip}:5000")
# NOTE: Class 4's "while True: server.poll()" loop is gone -- class-5-code.py polls now.
```

To test Step 2 on its own before the rover code exists, use this three-line `code.py`:

```python
# Step 2 test only -- keeps the filter and website running without driving.
import time
import rover_server  # keep the rover still for the 2 s gyro calibration

while True:
    rover_server.update()
    rover_server.server.poll()
    time.sleep(0.02)
```

**What to watch for:** Boot the rover sitting still *and flat* — the gyro calibration needs still, and
`_start_at_compass_heading()` needs flat. Booted on a tilt, the heading starts several degrees off and
takes a minute to correct itself. If `heading` slowly creeps back after you turn the rover by hand, or
never settles, `MAG_AXIS_SIGN` is wrong (back to the Step 1 axis check).

**Checkpoint 3:** On the website, every pair can show: (a) all eleven fields updating; (b) turning the
rover clockwise by hand 90° raises `heading` by about 90°; (c) left untouched for a minute, `heading`
stays within a few degrees — compare against the Class 4 yaw drift from the warm-up.

---

**Step 3 — the Random Rover with compass-steered turns (~25 min).**
Save `class-5-code.py` as `code.py` (`motor_driver.py`, `wheel_odometry.py`, and the Step 2
`rover_server.py` must all be on `CIRCUITPY`).

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
import rover_server  # Step 2 library version -- importing it calibrates the gyro,
                     # so keep the rover still while it boots

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP6, echo_pin=board.GP7)
pwm = pwmio.PWMOut(board.GP8, duty_cycle=0, frequency=50)
scan_servo = servo.Servo(pwm, min_pulse=500, max_pulse=2500)  # [VERIFY] -- recalibrate per servo

bump_switch = digitalio.DigitalInOut(board.GP5)
bump_switch.direction = digitalio.Direction.INPUT
bump_switch.pull = digitalio.Pull.UP  # switch pulls the pin LOW when pressed

ir_sensor = digitalio.DigitalInOut(board.GP13)
ir_sensor.direction = digitalio.Direction.INPUT  # module drives its own LOW-on-detect output

DRIVE_SPEED = 0.6               # [VERIFY] -- calibrate per robot
TURN_SPEED = 0.45              # [VERIFY] -- slow enough to stop near the target heading
SCAN_ANGLES = [30, 60, 90, 120, 150]  # servo degrees, left to right
CENTER_ANGLE = 90               # servo angle that looks straight ahead
SETTLE_TIME = 0.15              # seconds -- let the servo stop moving before trusting a reading
STOP_DISTANCE_CM = 25           # [VERIFY] -- distance that triggers an immediate rescan
SCAN_INTERVAL = 3.0             # seconds -- rescan on this timer even if nothing is close
HEADING_TOLERANCE_DEG = 5       # [VERIFY] -- "close enough" to the target heading
TURN_TIMEOUT_S = 3.0            # give up on a turn whose heading never arrives
BACKOFF_S = 0.3                 # [VERIFY] -- reverse time after a safety stop


def wait(seconds):
    """Drop-in for time.sleep() that keeps rover_server's IMU filter running
    about every 20 ms -- otherwise the heading would miss motion made while sleeping."""
    end_time = time.monotonic() + seconds
    while time.monotonic() < end_time:
        rover_server.update()
        time.sleep(0.02)


def read_distance():
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
            wait(BACKOFF_S)
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

**Before the obstacle course — the turn test (~5 min).** Compass turns need real rotation, so do
this on the floor, not with the wheels lifted. Temporarily set `SCAN_ANGLES = [150]` so every scan
picks "60° right." Watch the console: each turn should end with `heading now` about 60°
clockwise of where it started, and no `turn timed out` lines. Then restore `SCAN_ANGLES`.

**What to watch for:**

* A turn that spins until `turn timed out` → the turn direction and the heading disagree. Turn the
  rover clockwise by hand: `heading` must go *up*. If it goes down, the IMU is mounted upside down or
  `MAG_AXIS_SIGN` is wrong. If `heading` is right, the motor sign in `turn_toward()` is swapped for this
  car.
* A turn that wiggles back and forth before stopping → `TURN_SPEED` too high or
  `HEADING_TOLERANCE_DEG` too tight for this car. Lower one or raise the other.
* Let a first run be imperfect — a jerky turn or an overcautious `STOP_DISTANCE_CM` is fine for now.

**Checkpoint 4:** Every pair sees their rover complete at least one full stop-look-go cycle (drive,
stop, scan with printed readings, compass turn with `heading now` printed, resume) without
intervention, and the website shows `drive_state` flipping between `"driving"` and `"scanning"`.

**What "done" looks like:** The rover drives, periodically stops to scan, turns to within a few
degrees of the chosen direction by compass, and resumes — and stops immediately when something is
placed close in front of it. The same webpage from Classes 3-4 shows all eleven fields
(`http://192.168.4.1:5000` — type the `http://` and the `:5000`).

>**NOTE — known limitation:** each time the browser asks for `/data.json`, `read_speed()` spends
>about 0.25 s counting wheel ticks inside `rover_server.server.poll()`. So while the status page is
>open, the drive loop — including the bump-switch and IR checks — can pause for up to 0.25 s about
>twice a second. Turns are protected (`turn_toward()` never polls), but for the quickest reflexes
>while driving, close the browser tab. Removing the pause for real means counting wheel ticks
>without blocking, a redesign of `wheel_odometry.py` left for a future version of the course.

### 5e. Independent Work — ~25 min

**What to do:** Pairs take their rover to the shared floor and run it for several minutes, tuning
`DRIVE_SPEED`, `STOP_DISTANCE_CM`, `SCAN_INTERVAL`, `SCAN_ANGLES`, `TURN_SPEED`, and
`HEADING_TOLERANCE_DEG`. Each pair logs at least one full run in their build journal: obstacles
encountered, obstacles avoided, and any `turn timed out` lines. Faster pairs can:

* **Timed vs. compass showdown.** Run five 90° turns on tile, then five on carpet (or a rug), and
  record the final `heading` error each time. Compare with what Class 3's timed turn did on the two
  surfaces. This is the closed-loop payoff made visible.
* **Motor interference.** With the rover still, watch `heading` on the website, then start the motors
  with the wheels lifted. How many degrees does it jump? Does it recover when they stop?
* Set up the "narrow gap with open space beyond it" scenario and see whether the rover picks the gap.
* Have a partner watch the website (not the console) during a run and call out `drive_state`,
  `stop_reason`, and `heading` changes as they happen.

**What to watch for:** Rovers that behave well in one part of the room and badly near a steel cabinet
or a floor vent — that's magnetic distortion, a real-world limitation worth discussing, not a bug.

**Time check:** At the 15-minute mark, show of hands: "Whose rover has completed a full
drive-scan-turn cycle and avoided at least one obstacle?" Redirect instructor attention to pairs still
stuck.

### 5f. Closing / Wrap-up — ~10 min

**What to do:** 2-3 volunteers run their rover live with an obstacle in its path, with that rover's
status website on the projector so the group watches `heading`, `scan_heading`, `drive_state`, and
`stop_reason` change with what the rover is doing. Open the "how would you actually measure this?"
discussion — push past "it didn't hit anything" toward something specific: avoidances per run,
distance kept from obstacles, heading error per turn, and whether a wheel's speed dropping to near zero
mid-run reveals a stuck wheel before the rover reports a collision.

**What to say:** "Your rover now turns by measuring, not guessing. The IMU you built in Class 4 went
from a number on a webpage to the thing that steers the car. Everything it knows — wheel speed, tilt,
compass heading, what it just decided and why — is on one page. Next Class is about finishing and
tuning this exact rover, and for anyone who wants to go further, there are stretch goals that bring
back your Class 1 encoder."

**Preview next Class:** Class 6 needs no new wiring for its core work — it's tuning today's rover,
including today's bump switch (`GP5`), IR sensor (`GP13`), and magnetometer calibration, all carried
forward unchanged. The optional stretch goals reconnect Class 1's encoder (`GP3`/`GP4`) exactly as
already wired; a TFT display stretch goal is the only new wiring, on pins not used anywhere else in
the course. Point students to the Class 6 references in the syllabus if they want to read ahead.

## 6. Troubleshooting Guide

| Problem | Likely Cause | Fix |
| :-------- | :------------- | :---- |
| Calibration spans very unequal, e.g. `(0.9, 0.9, 0.1)` | Rover only spun flat, never tumbled onto its sides | Rerun `class-5-mag-calibration.py`; roll the rover onto every side and tip it nose-up/nose-down |
| Calibration spans all tiny (under ~0.2) or `magnetic` reads the same number forever | IMU not responding on I2C, or calibrating on top of a large steel surface | Check `SDA`/`SCL` (roll/pitch still working?); move to a wooden/plastic table |
| Axis check: one of `mx`/`my` negative when its arrow points north, or `mz` positive lying flat | That magnetometer axis is flipped relative to the accel/gyro | Flip that entry in `MAG_AXIS_SIGN`, in both the calibration program and `rover_server.py` |
| `heading` slowly creeps back after a hand turn, or never settles | `MAG_AXIS_SIGN` wrong, so the magnetometer and gyro disagree | Redo the Step 1 axis check |
| `heading` was fine, now wrong by a fixed amount everywhere | IMU remounted or moved closer to the motors/battery after calibration | Rerun the calibration with the IMU in its final position |
| `heading` jumps 10-20° when the motors start | Magnetic field from the motor current (calibration can't remove it) | Mount the IMU farther from motors and battery (higher, on a standoff); small jumps are expected and the filter smooths them |
| `heading` wrong only near certain furniture or spots on the floor | Steel desks, cabinets, rebar, or floor vents bending the local field | Test in a clearer area; treat as a real-world limitation to discuss |
| Rover spins until `drive: turn timed out` | Turn direction and heading disagree, or `TURN_SPEED` too low to move the car | Turn the rover clockwise by hand — `heading` must rise. If it does, swap the motor signs in `turn_toward()`; if the wheels barely move, raise `TURN_SPEED` |
| Turn overshoots and wiggles back and forth | `TURN_SPEED` too high, or `HEADING_TOLERANCE_DEG` too tight | Lower `TURN_SPEED` in 0.05 steps, or raise the tolerance to 8° |
| `heading` a few degrees off at boot, slowly correcting for a minute | Rover booted on a tilt, so the starting compass heading was skewed | Reset the rover sitting flat and still; relative turns still work meanwhile |
| Rover doesn't drive at all | `motor_driver.py` missing from CIRCUITPY, or 9V battery dead | Confirm `motor_driver.py` is present alongside `code.py`; check battery voltage |
| `ImportError` for `rover_server` or `wheel_odometry` | File missing from CIRCUITPY | Copy the Step 2 `rover_server.py` and Class 3's `wheel_odometry.py` back onto the drive |
| Rover drives but never stops to scan | `SCAN_INTERVAL` too long, or `STOP_DISTANCE_CM` too small to trigger | Lower `SCAN_INTERVAL` and/or raise `STOP_DISTANCE_CM` |
| Rover stops constantly, barely drives | `STOP_DISTANCE_CM` too large, triggering on sensor noise | Lower `STOP_DISTANCE_CM` in small steps |
| Rover always "chooses" 90 regardless of readings | Scan readings all `None`, falling back to `CENTER_ANGLE` | Check Class 2's sensor wiring; confirm `read_distance()` isn't always returning `None` |
| Console floods with `None` distances during a scan | Servo moved before the sensor settled, or aimed at an out-of-range surface | Increase `SETTLE_TIME`; re-aim the test area to stay within the sensor's usable range |
| Works on the laptop cable, but unplugged every scan reads `None` and the servo stops | HC-SR04 and servo still powered from `VBUS` | Move HC-SR04 `VCC` and servo `+` from `VBUS` to the `VSYS` rail |
| Bump switch never triggers even on a hard hit | Lever not leading the chassis edge, or `GP5` wiring loose | Reposition the switch; continuity-check the wiring |
| Rover constantly emergency-stops with nothing nearby | IR sensitivity trimmer too high, or aimed at a reflective floor | Turn the trimmer down; re-aim slightly upward |
| Rover reverses into something behind it after a safety stop | `BACKOFF_S` too long for the available clearance | Shorten `BACKOFF_S` |
| Website's new fields never appear or never change | Old Class 4 `rover_server.py` still on CIRCUITPY, or its old `while True: server.poll()` loop wasn't removed | Confirm only one `rover_server.py` exists and it's the Class 5 version |
| Website hangs once the rover starts driving | Both files still have blocking loops calling `server.poll()` | Delete the old loop from `rover_server.py` entirely |
| Rover reacts late to the bump switch/IR sensor only while the page is open | Each `/data.json` request blocks ~0.25 s in `read_speed()` (see the known-limitation note) | Expected with the page open; close the browser tab for the quickest reflexes |
| Website's wheel-speed or orientation fields stopped updating | `GP19`/`GP17` or `GP0`/`GP1` wiring bumped while adding the safety sensors | Re-verify those circuits; they're unrelated to today's `GP5`/`GP13` wiring |

## 7. Age Differentiation Notes

**Magnetometer calibration (Step 1).**
*Younger students (12-14):* Pair up — one student tumbles the rover while the other reads the
countdown and copies the `MAG_OFFSET` line into the build journal. Run the axis check as a guided
game with the phone compass: "Point the X arrow north. Is `mx` the biggest positive number? Thumbs
up." *Older students (15-18) and adults:* Ask why the *center* of each axis's swing is the offset
(Earth's field is the same strength in every direction, so a clean sensor would swing evenly around
zero). Point out what min/max calibration can't fix: soft-iron distortion that stretches the swing
into an ellipse — see the [LSM9DS1 AHRS reference][02] for a full ellipsoid calibration.

**9-DOF filter (Step 2).**
*Younger students:* Paste the finished `rover_server.py`, fill in their own `MAG_OFFSET`, and focus on
Checkpoint 3's hand-turn test. *Older students and adults:* Compare `_mahony_update()` side by side
with Class 4's: the gravity half is unchanged, and the north half is the same "predicted vs. measured,
cross product = error" idea with a second reference. Have them explain why `latest_heading` flips the
sign of yaw.

**Compass turns and the rover (Step 3).**
*Younger students:* Start from `class-5-code.py` already loaded and focus on tuning the constants on
the floor rather than reading the control logic line by line. *Older students and adults:* Walk
`heading_error()` line by line — it's the same 359°-to-1° wrap-around problem from the
[quaternion explainer][03], solved for one angle. Challenge them to run the "timed vs. compass
showdown" and the "narrow gap vs. dead end" scenario, and document predicted vs. actual.

## 8. Assessment

**Milestone Assignment (per syllabus, Phase 3 / Class 5):** Car drives autonomously and avoids at
least one obstacle without instructor intervention, with the rover's full state visible together on
its status website.

**What "complete" looks like:** The student sets their rover driving on the shared floor, places an
obstacle in its path, and shows it stop, scan, choose a direction, turn by compass, and continue —
without touching the car or keyboard once it starts. One successful avoidance during a live demo is
enough; this is a completion-based milestone, not a reliability benchmark. The student can also open
the status website and point to `heading`, `scan_heading`, `drive_state`, and `stop_reason` updating
live alongside the wheel and orientation fields from Classes 3-4, and show that `heading` holds steady
when the rover sits still.

**How to give feedback without scoring:** Ask the student to narrate what the console printed during
the avoidance — what triggered the stop, the scan readings, why that angle won, and the target vs.
final heading of the turn. Ask them to explain in one sentence why they calibrated the magnetometer on
the rover and not on the bench. If a pair can't get a full autonomous avoidance working in time,
that's fine — have them bring a working version to the start of Class 6 and note it in their build
journal; Class 6 is built around continuing to tune this exact rover.

## 9. Instructor Tips

* Run the magnetometer axis check on the reference rover *before* class. If the default
  `MAG_AXIS_SIGN` is wrong for your boards, you want to announce the right values, not discover them
  twelve times.
* Do the calibration demo live, and exaggerate the tumble — students copying a timid flat spin is the
  most common calibration failure.
* Run the reference rover yourself, live, before students touch their own — watching one full
  stop-look-go cycle with a clean compass turn sets expectations better than describing it.
* The Class 3 turn-time calibration notes aren't needed anymore. That's a teaching moment, not a
  loss: ask students what changed so that the rover no longer needs them.
* If a rover's turns go wrong only in one corner of the room, walk over with the phone compass before
  touching code — you'll often find a steel cabinet or radiator.
* Keep `class-5-code.py`, `class-5-mag-calibration.py`, the Step 2 `rover_server.py`, and Class 3's
  `motor_driver.py`/`wheel_odometry.py` on a shared USB stick — a student who cleaned their CIRCUITPY
  drive will otherwise hit a confusing `ImportError`.
* Test the bump switch and IR sensor mounts on the reference rover before students arrive — a loosely
  taped sensor or a switch lever that doesn't lead the chassis edge silently never triggers.
* Step 2 touches three things at once. Resist re-teaching WiFi or `adafruit_httpserver`; if a pair
  never got the Class 3/4 website working, point them to those Classes' troubleshooting guides.

## 10. Resources & References

* [What Is an IMU, and What Does a Mahony Filter Do?][01] — the course explainer on the gyro,
  accelerometer, and magnetometer, why yaw drifts without a magnetometer, and how Mahony compares to
  Madgwick and Kalman filters
* [LSM9DS1 AHRS: Mahony filter and calibration for the LSM9DS1][02] — a reference 9-DOF Mahony
  implementation for this exact chip, including its axis realignment and a full (ellipsoid)
  magnetometer calibration, for instructors and advanced students
* [What Are Quaternions, and Why Use Them?][03] — the course explainer behind the filter's
  `q0..q3`, and the angle wrap-around problem `heading_error()` solves
* [Python & CircuitPython — Adafruit LSM9DS1 9-DOF Breakout][04] — Adafruit's guide, including the
  `magnetic` property used today
* [Raspberry Pi Pico W taught this car to avoid objects][05] — a real-world example of Pico-based
  obstacle avoidance, similar in spirit to today's build
* [How to make an obstacle avoidance robot using Raspberry Pi Pico board][06] — a step-by-step
  obstacle-avoidance build guide, useful as a cross-reference
* [Obstacle Avoidance Robot Using Raspberry Pi Pico][07] — another worked example of combining a
  distance sensor and motor driver for collision avoidance

---

[01]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/blob/main/explainers/what-is-an-imu-and-mahony-filter.md
[02]:https://github.com/jremington/LSM9DS1-AHRS
[03]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/blob/main/explainers/what-are-quaternion-and-why-use-them.md
[04]:https://learn.adafruit.com/adafruit-lsm9ds1-accelerometer-plus-gyro-plus-magnetometer-9-dof-breakout/python-circuitpython
[05]:https://www.raspberrypi.com/news/raspberry-pi-pico-w-taught-this-car-to-avoid-objects/
[06]:https://srituhobby.com/how-to-make-an-obstacle-avoidance-robot-using-raspberry-pi-pico-board/
[07]:https://circuitdiagrams.in/obstacle-avoidance-robot-using-raspberry-pi/
