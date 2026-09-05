# Lesson Plan: Class 5 — Build the Random Rover: Collision Avoidance

* **Class:** 5 of 6 (plus Pre-Class)
* **Phase:** Phase 3 — Integration (Class 5-6: combine sensing + motion into an autonomous robot)
* **Duration:** ~2 hours (120 min)
* **Prerequisites from prior Classes:** Classes 1-4 completed — every student has a working
  HC-SR04 + SG90 sensor-sweep circuit (`GP6`-`GP8`, from Class 2) and a working DRV8833 motor driver
  circuit (`GP9`-`GP12`, from Class 3) on their breadboard, calibrated turn timing from Class 3's
  square/circle attempt, and is comfortable wiring, saving `code.py`, and reading streamed serial
  output. Class 1's button/encoder circuit and Class 4's IMU circuit are not needed for this build
  and can stay on the breadboard unused or be set aside — but the Class 3 wheel-odometry
  optocouplers (`GP16`/`GP17`) and Class 4's IMU (`GP0`/`GP1`) must stay wired and powered even
  though today's collision-avoidance code doesn't read them directly, because the growing rover
  status website (`rover_server.py`) still reports wheel speed/direction and orientation from those
  same circuits. The website and its classroom WiFi connection must still be working — a quick
  spot-check, not a rebuild.

---

## 1. Class Overview

This is the fifth Class of the course and the first of Phase 3 (Integration) — the Class where
everything built so far comes together into the "Random Rover." Students combine Class 2's
servo-mounted ultrasonic sensor with Class 3's DRV8833 motor driver into a single autonomous
program: the car drives forward at a constant speed, periodically stops to sweep the sensor across a
set of angles looking for the clearest direction, and steers toward whichever angle had the most
open space — with an interrupt path that stops and rescans immediately if anything gets too close
while driving, instead of waiting for the next scheduled scan. The Class 2 and Class 3 circuits are
reconnected exactly as left wired, with no changes; the only new wiring today is two fixed safety
sensors — a limit switch and an IR obstacle sensor — that back up the ultrasonic sweep with an
immediate stop-and-reverse override, independent of the scan-and-turn logic. This Class is entirely
about writing the decision logic that ties Class 2's "eyes" to Class 3's "legs," with those two new
sensors as a last line of defense. By the end of the Class, students will have a car that drives
around the room on its own and avoids at least one obstacle without instructor intervention — the
course's central milestone.

The rover status website keeps growing too. Class 3 gave it live wheel speed/direction, Class 4 added
IMU orientation, and today `class-5-code.py` adds the collision-avoidance decision itself: the
current scan heading, whether the car is driving/stopped/scanning, and which safety signal (if any)
most recently forced a stop. This is a small, additive edit to the same `rover_server.py` students
already have working — not a new website, and not new wiring.

## 2. Learning Goals

* Reconnect the Class 2 sensor+servo circuit and Class 3 motor driver circuit into one combined
  program, with no new wiring required
* Explain, in plain language, the "stop-look-go" design: drive straight, rescan on a timer, and
  interrupt that timer immediately if an obstacle comes within a stopping distance
* Implement logic that scans a set of angles, compares distance readings, and steers the car toward
  the clearest heading
* Identify a room layout or sensor limitation where "steer toward the largest reading" could pick a
  bad direction, and discuss why
* Propose a way to measure whether the collision-avoidance behavior is actually working, beyond
  eyeballing it
* Wire a limit switch and an IR obstacle sensor as fixed safety inputs, and use them to trigger an
  immediate stop-and-reverse that overrides the normal scan-and-turn logic
* Extend the rover status website (`rover_server.py`) with scan heading, drive state, and
  stop-reason fields, so the collision-avoidance decision is visible on the same webpage as wheel
  speed/direction and orientation

## 3. Preparation Checklist

* **1-2 days before:** Confirm every student's Class 2 (sensor+servo) and Class 3 (motor driver)
  circuits are still intact and power up — a quick visual/serial spot-check, not a rebuild. Class 1
  and Class 4 circuits do not need to be checked today. (~15 min)
* **1-2 days before:** Confirm each student still has their Class 3 turn-time calibration notes
  (`SECONDS_PER_90_DEGREES` or equivalent) from their build journal — today's code reuses that
  calibration rather than re-deriving it from scratch. (~5 min)
* **1-2 days before:** Confirm every student's `rover_server.py` from Class 4 still connects to the
  classroom WiFi and serves `/data.json` with all seven existing fields (wheel speed/direction,
  orientation) — nothing new to set up here this Class, just confirm it still works, since today's
  website change is a small edit to this same file. (~10 min)
* **Day of, before students arrive:**
* Clear a large open floor area (or several smaller zones) for autonomous driving tests, with a
        few soft obstacles (cardboard boxes, foam blocks — nothing that will damage a car or a wall
        on contact) placed at varying distances.
* Pre-build one reference rover (sensor+servo+motor driver, plus the new bump switch and IR
        sensor) at the instructor bench and test `class-5-code.py` end-to-end, tuning
        `DRIVE_SPEED`, `SCAN_ANGLES`, `STOP_DISTANCE_CM`, and the IR sensor's sensitivity trimmer
        so you know what a realistic first run looks like and can spot obviously wrong behavior
        quickly during Guided Practice. (~30 min)
* Also test `class-5-code.py`'s edit to `rover_server.py` end-to-end: load it on the reference
        Pico, confirm the same laptop browser that showed wheel speed/direction and orientation in
        Classes 3-4 now also shows `scan_heading`, `drive_state`, and `stop_reason` fields updating
        live on `/data.json`. (~10 min)
* Project the instructor's serial console output so the whole class can see scan readings, chosen
        headings, and drive state stream by during the reference run. (~5 min)
* Have a few spare 9V batteries charged and ready — today's Class runs motors continuously for
        longer stretches than Class 3 did.
* **Have ready:** A short list of discussion prompts for the "stop-look-go" tradeoff, the "largest
  reading picks a bad direction" scenario, and "how would you measure this?" (see Direct Teaching and
  Closing below).

## 4. Materials & Components

Per-student unless noted. Component names only — see the course Bill of Materials for costs,
quantities, and sourcing.

| Component | Purpose This Class |
| :---------- | :-------------------- |
| Raspberry Pi Pico 2 W (with header) | Microcontroller running CircuitPython |
| HC-SR04 Ultrasonic Distance Sensor (from Class 2) | Measures distance at each scan angle |
| SG90 Micro Servo Motor (from Class 2) | Sweeps the sensor across `SCAN_ANGLES` |
| DRV8833 Dual H-Bridge DC/Stepper Motor Driver Breakout Board (from Class 3) | Drives the car forward and executes steering turns |
| Micro Limit Switch | Physical bumper on the chassis front — last-resort stop-and-reverse override on contact |
| IR Obstacle Avoidance Sensor | Fixed forward-facing near-field detector — stop-and-reverse override between ultrasonic scans |
| Emo Smart Robot Car Chassis Kit | The completed (or near-complete) car chassis and wheels |
| 9V battery clip and 9V battery | Motor power, independent of the Pico's logic power |
| Breadboard (830-point, from Class 1) | Circuit assembly surface — no rewiring needed this Class |
| Dupont jumper wires (shared) | Only if any connection needs reseating |
| USB cable (student-supplied, from Pre-Class) | Power + serial connection to laptop, or portable battery for untethered runs |
| Windows 11 laptop with Mu or Thonny (student-supplied) | Edit and run CircuitPython code |
| Classroom WiFi network (shared, from Class 3) | Already-joined network the growing rover status website runs on; nothing new to set up |
| Shared: open floor area with soft obstacles | Test space for autonomous driving runs |

## 5. Class Timeline

### 5a. Warm-up / Hook — ~10 min

**What to do:** Have every student plug in their Pico 2 W and confirm the Class 2 sensor+servo sweep
and the Class 3 motor forward/reverse/stop test both still work independently. Ask 2-3 students to
recap, in one sentence each, what Class 2's sensor sweep showed them and what Class 3's "what's
missing?" discussion concluded.

**What to say:** "Most of what you need is already on your breadboard from Class 2 and Class 3 —
today's work is mostly about writing the decision-making that connects your car's eyes to its legs.
The one new thing today is two small safety sensors, a bump switch and an IR sensor, that give your
car a last-resort 'stop no matter what' reflex."

**What to watch for:** Any regressions in the Class 2 or Class 3 circuits specifically (loose sensor
mount, weak battery) — fix quickly, since today's build depends on both working correctly at the
same time.

**Time check:** If more than 2-3 boards need real rework, handle it during Guided Practice instead
of holding up the whole class now.

### 5b. Introduction — ~10 min

**What to do:** Introduce the Random Rover concept and preview the "stop-look-go" design pattern:
drive straight, periodically stop and scan, steer toward the clearest direction, repeat — and
interrupt that pattern immediately if something gets close while driving.

**What to say:**

* "This is the moment where Class 2's sensor and Class 3's motors stop being separate demos and
  become one robot that makes its own decisions."
* "The core idea today is called 'stop-look-go': drive forward, pause on a timer to sweep and look
  around, pick the clearest direction, turn, and go again. But if something gets dangerously close
  while you're driving, you don't wait for the next scheduled look — you stop and look right now."
* "By the end of today, your car should be able to drive around this room by itself and steer around
  at least one obstacle without you touching it."

**Questions to ask students:** "Why might 'always be looking' (continuously scanning while driving)
be harder to build than 'stop, look, then go'?" (The sensor is mounted on a servo that has to
physically move and settle — Class 2's `SETTLE_TIME` lesson comes back here.)

### 5c. Direct Teaching — ~10 min

No code yet — diagrams and discussion only, using the whiteboard or projected diagram.

**Concept 1 — The stop-look-go control loop (Theory of Operation, brief).**
The rover's behavior is a repeating cycle: drive straight for a while; when either a scan timer
elapses *or* a close-object reading interrupts driving, stop the motors; sweep the sensor across a
set of angles (`SCAN_ANGLES`), recording a distance at each stop; compare all the readings and pick
the angle with the largest distance (the most open space); turn toward that heading, reusing Class
3's calibrated turn timing; resume driving straight; repeat.

*Step-by-step decomposition of one cycle:*

1. Car drives forward at `DRIVE_SPEED`.
2. Either the scan timer elapses, or a live distance reading drops below `STOP_DISTANCE_CM` — either
   condition triggers the next step.
3. Motors stop.
4. Servo sweeps across `SCAN_ANGLES`, pausing briefly at each (same settle-then-read pattern from
   Class 2) and recording a distance.
5. Code picks the angle with the largest recorded distance.
6. Car turns toward that angle, using the turn-time calibration carried over from Class 3.
7. Car resumes driving straight, and the cycle repeats.

**Concept 2 — Why two separate triggers for rescanning (timer AND proximity), not just one.**
Ask: "What goes wrong if the rover only rescans on a fixed timer?" Draw out: an obstacle could appear
(or the car could approach one fast enough) between scheduled scans, and the car would drive straight
into it before the next timer fires. Then ask: "What goes wrong if it only rescans when something
gets close?" Draw out: without a periodic timer as a backup, a sensor miss-read or an object that
never triggers the proximity threshold (e.g., approached at a shallow angle where the beam misses it)
would never trigger a rescan at all. Two independent triggers cover each other's blind spot.

**Concept 3 — Why "steer toward the largest reading" can pick a bad direction.**
Ask the class to sketch (or imagine) a narrow gap in a wall with wide-open space just beyond it,
versus a wide-open room that's actually a dead end. A sensor sweep comparing raw distances at each
angle can't tell the difference between "this reading is large because the space genuinely continues"
and "this reading is large because the beam is skimming past a nearby edge into background clutter,"
or between a narrow-but-passable gap and a wide-but-shallow alcove. Ask: "What additional information
would help distinguish these cases?" (Multiple close-together scan angles reading consistently open
is a stronger signal than one high reading surrounded by low ones — a preview of thinking about
sensor data as a shape, not just a set of independent numbers.)

**Concept 4 — The stop-look-go tradeoff.**
Stopping to scan is simple and safe — the sensor never has to interpret a reading taken while the
whole robot (and thus the sensor) is also moving. But it's slower and less smooth than continuously
sensing while driving would be. Ask: "What would a car need, that this one doesn't have, to sense
continuously while still moving?" (A sensor that doesn't need to physically sweep — e.g., multiple
fixed sensors at different angles — trading mechanical simplicity for more parts and wiring.)

**Concept 5 — The rover website now shows everything the car "knows" (Theory of Operation, brief).**
Recall the running thread: Class 3's wheel odometry gave real wheel speed and slip; Class 4's IMU
added heading. Both were posted onto the same `rover_server.py` status page rather than a new one.
Today's code does the same thing with the collision-avoidance decision itself — the chosen scan
heading, whether the car is currently driving/stopped/scanning, and which of the three safety signals
(ultrasonic, IR, bump switch) most recently forced a stop. Ask: "Why is it useful to see this on a
webpage instead of only in the serial console?" (Nothing new is being sensed — it's the same data
already printed to serial — but a browser tab doesn't require a USB cable, so an observer can watch
the rover's full internal state — wheels, orientation, and now its own decision-making — from across
the room while it drives untethered.)

### 5d. Guided Practice — ~40 min

**Pacing note:** Two steps fit in 40 min because Step 2 is a brisk, small edit to a file students
already have working (`rover_server.py`), not a new build — the same pattern Class 4 used for its
own website step. If a group is running behind, it is the first thing to shorten — have those
students paste in the finished Step 2 code instead of walking every line, and move on.

Instructor builds along on the projector; students wire up and test in parallel.

**Wiring — Class 2 and Class 3 circuits are reconnect-only, no changes.** The only *new* wiring this
Class is the limit switch and IR sensor. Class 1's button/encoder circuit and Class 4's IMU circuit
are not used and can stay in place or be set aside.

| Component | Pico 2 W Pin | From Class |
| :---------- | :------------- | :----------- |
| HC-SR04 `TRIG` | `GP6` | Class 2 |
| HC-SR04 `ECHO` (through voltage-divider) | `GP7` | Class 2 |
| SG90 servo signal | `GP8` | Class 2 |
| DRV8833 `AIN1`/`AIN2` (Motor A) | `GP9`/`GP10` | Class 3 |
| DRV8833 `BIN1`/`BIN2` (Motor B) | `GP11`/`GP12` | Class 3 |
| Limit switch (common + normally-open, to `GND`) | `GP5` (internal pull-up) | New this Class |
| IR obstacle sensor `OUT` | `GP13` | New this Class |

Mount the limit switch as a physical bumper on the chassis front (lever arm facing forward, so any
contact presses it), and the IR sensor fixed and forward-facing, low on the chassis, aimed at
ground-level obstacles the ultrasonic sweep might miss between scans.

**Checkpoint 1:** Before writing any code, have every pair power up and re-verify both circuits
independently still work (sensor sweep, motor forward/reverse) exactly as they did at the end of
Class 2 and Class 3, before combining them in one program. Catching a regression now is much easier
than debugging it inside the combined rover logic later.

**Step 1 — combined collision-avoidance program.**
Load `class-5-code.py` (save as `code.py`). Combines Class 2's servo-swept HC-SR04 with Class 3's
`motor_driver` module (`motor_driver.py` must still be present on the CIRCUITPY drive from Class 3).

```python
# class-5-code.py
# Random Rover: drives forward, rescans on a timer or on proximity, steers toward clearest heading.
import time
import board
import digitalio
import pwmio
import adafruit_hcsr04
from adafruit_motor import servo
import motor_driver  # from Class 3, must already be on CIRCUITPY

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP6, echo_pin=board.GP7)
pwm = pwmio.PWMOut(board.GP8, duty_cycle=0, frequency=50)
scan_servo = servo.Servo(pwm, min_pulse=500, max_pulse=2500)  # [VERIFY] -- recalibrate per servo

bump_switch = digitalio.DigitalInOut(board.GP5)
bump_switch.direction = digitalio.Direction.INPUT
bump_switch.pull = digitalio.Pull.UP  # switch pulls the pin LOW when pressed

ir_sensor = digitalio.DigitalInOut(board.GP13)
ir_sensor.direction = digitalio.Direction.INPUT  # module drives its own LOW-on-detect output

DRIVE_SPEED = 0.4               # [VERIFY] -- calibrate per robot, lower than Class 3's test speed
SCAN_ANGLES = [30, 60, 90, 120, 150]  # degrees, left to right
SETTLE_TIME = 0.15              # seconds -- let the servo stop moving before trusting a reading
STOP_DISTANCE_CM = 25           # [VERIFY] -- distance that triggers an immediate rescan
SCAN_INTERVAL = 3.0             # seconds -- rescan on this timer even if nothing is close
TURN_SECONDS_PER_DEGREE = 0.4 / 90  # [VERIFY] -- reuse Class 3's SECONDS_PER_90_DEGREES calibration

CENTER_ANGLE = 90


def read_distance():
    try:
        return sonar.distance
    except RuntimeError:
        return None


def scan():
    """Sweep SCAN_ANGLES, return (best_angle, readings dict)."""
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

    close_call = False
    while True:
        if safety_override_triggered():
            motor_driver.stop()
            print("drive: emergency stop-and-reverse (safety override)")
            motor_driver.drive(-DRIVE_SPEED, -DRIVE_SPEED)
            time.sleep(0.3)  # [VERIFY] -- back off far enough to clear the trigger
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

**What to watch for:** This is the moment students should see the rover actually drive, stop, sweep,
and steer on its own for the first time — let a first run be imperfect (a jerky turn, an
overcautious `STOP_DISTANCE_CM`) rather than insisting on a perfect run before moving on.

**Checkpoint 2:** Every pair should see their rover complete at least one full stop-look-go cycle
(drive, stop, scan with printed readings, turn, resume driving) without instructor intervention.

**What "done" looks like for this segment:** The rover drives forward, periodically stops to scan
and print readings/chosen heading to the console, turns toward open space, and resumes — and stops
immediately (not waiting for the timer) when something is placed close in front of it while driving.

**Step 2 — extend the rover status website with the collision-avoidance decision.**
Recall `rover_server.py`'s `/data.json` route: it already returns `speed_left_cms`/`dir_left`/
`speed_right_cms`/`dir_right` (Class 3) and `roll`/`pitch`/`yaw` (Class 4), and the webpage displays
any field the dict has with no HTML/JavaScript changes needed — the same reason Class 4's edit was
small. Today adds three more flat fields, matching that existing style: `scan_heading` (the last
chosen angle, a number), `drive_state` (a string — `"driving"`, `"scanning"`, or `"stopped"`), and
`stop_reason` (a string — `"none"`, `"ultrasonic"`, `"ir"`, or `"limit_switch"`, naming whichever
safety signal most recently forced a stop).

There's one wrinkle Older Students should notice (see Age Differentiation): Class 4's `rover_server.py`
ends in its own blocking `while True: server.poll()` loop, but today's `class-5-code.py` needs to run
its *own* continuous drive/scan loop — two blocking loops can't run at once. So today's edit does the
small refactor Class 4 flagged as an optional stretch: `rover_server.py` stops owning the polling loop
and instead exposes its already-built `server` object and a small `scan_status` dict for
`class-5-code.py` to update and poll each cycle.

```python
# rover_server.py -- edited again (same file from Classes 3-4, no new filename).
# Removes its own "while True: server.poll()" loop -- class-5-code.py's drive
# loop now calls server.poll() itself once per cycle, since only one loop can
# own the CPU at a time. Adds scan_status, a small dict class-5-code.py updates
# each cycle with the collision-avoidance decision, merged into /data.json.
scan_status = {
    "scan_heading": 90,        # degrees -- last chosen heading, starts centered
    "drive_state": "driving",  # "driving" | "scanning" | "stopped"
    "stop_reason": "none",     # "none" | "ultrasonic" | "ir" | "limit_switch"
}


@server.route("/data.json")
def data_json(request: Request):
    speed_left, dir_left, speed_right, dir_right = wheel_odometry.read_speed()
    roll, pitch, yaw = _read_orientation()
    return JSONResponse(request, {
        "speed_left_cms": speed_left,
        "dir_left": dir_left,
        "speed_right_cms": speed_right,
        "dir_right": dir_right,
        "roll": roll,
        "pitch": pitch,
        "yaw": yaw,
        "scan_heading": scan_status["scan_heading"],
        "drive_state": scan_status["drive_state"],
        "stop_reason": scan_status["stop_reason"],
    })


@server.route("/")
def index(request: Request):
    return Response(request, STATUS_PAGE, content_type="text/html")


server.start(str(wifi.radio.ipv4_address))
# NOTE: the old "while True: server.poll()" loop is gone from this file --
# class-5-code.py's own main loop polls it now (see below). [VERIFY]
```

Then a small addition to `class-5-code.py` itself: import the website module, poll it once per
iteration so requests still get answered while the rover drives, and keep `scan_status` updated with
the live decision.

```python
# class-5-code.py -- Step 2 additions (add alongside the Step 1 code above)
import rover_server  # Classes 3-4's website; today's edit removed its own poll() loop


def safety_override_triggered():
    """Check the fixed bump switch and IR sensor; return a stop_reason string
    ("none" if neither is triggered) instead of a bare bool, so the caller can
    publish which signal fired to the rover status website."""
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
    rover_server.server.poll()  # answer any pending website request, non-blocking
    rover_server.scan_status["drive_state"] = "driving"
    print("drive: forward")
    motor_driver.drive(DRIVE_SPEED, DRIVE_SPEED)

    stop_reason = "none"
    while True:
        rover_server.server.poll()
        stop_reason = safety_override_triggered()
        if stop_reason != "none":
            motor_driver.stop()
            print("drive: emergency stop-and-reverse (safety override)")
            motor_driver.drive(-DRIVE_SPEED, -DRIVE_SPEED)
            time.sleep(0.3)  # [VERIFY] -- back off far enough to clear the trigger
            motor_driver.stop()
            break
        distance = read_distance()
        if distance is not None and distance < STOP_DISTANCE_CM:
            print("drive: obstacle close, distance_cm", distance)
            stop_reason = "ultrasonic"
            break
        if time.monotonic() - last_scan_time >= SCAN_INTERVAL:
            break
        time.sleep(0.05)

    rover_server.scan_status["stop_reason"] = stop_reason
    rover_server.scan_status["drive_state"] = "scanning"
    motor_driver.stop()
    print("drive: stopped for scan" if stop_reason == "none" else "drive: emergency stop for scan")
    heading, _readings = scan()
    rover_server.scan_status["scan_heading"] = heading
    turn_toward(heading)
    last_scan_time = time.monotonic()
```

**What to watch for:** If the website's new fields never change, confirm `rover_server.py`'s old
`while True: server.poll()` loop was actually deleted (two competing blocking loops will make the
website hang, not the rover). If `scan_heading`/`drive_state`/`stop_reason` show up but never update,
confirm `class-5-code.py` is importing the edited `rover_server.py`, not a leftover Class 4 copy.

**Checkpoint 3:** Every pair should be able to open their Pico's status webpage and see all ten
fields — the seven from Classes 3-4 plus `scan_heading`, `drive_state`, `stop_reason` — update live,
with `drive_state` flipping between `"driving"` and `"scanning"` as the rover cycles and `stop_reason`
naming whichever safety signal last fired.

**What "done" looks like for this segment:** The same webpage students used in Classes 3-4 now also
shows the rover's live collision-avoidance decision, with no separate page or server — one browser
tab, one growing set of live numbers.

### 5e. Independent Work — ~40 min

**What to do:** Students (in pairs where possible) take their rover to the shared open floor area
and run it for several minutes, adjusting `DRIVE_SPEED`, `STOP_DISTANCE_CM`, `SCAN_INTERVAL`, and
`SCAN_ANGLES` to reduce collisions and smooth out behavior. Have them log at least one full run in
their build journal: how many obstacles did it encounter, how many did it successfully avoid? Faster
pairs can:

* Deliberately set up the "narrow gap with open space beyond it" scenario from Direct Teaching and
  see whether their rover picks the gap or gets confused, then discuss why.
* Add a printed distinction between a "timer rescan" and an "emergency rescan" in their own words if
  the provided code doesn't make it obvious enough on the console.
* Try narrowing or widening `SCAN_ANGLES` and discuss the tradeoff between scan resolution and cycle
  time (a wider, denser sweep takes longer per stop).
* Have a partner watch the rover status website (not the console) during a run and call out
  `drive_state`/`stop_reason` changes out loud as they happen, matching them to what's actually
  happening on the floor in real time.

**What to watch for:** The most common failure at this stage is a rover that turns the wrong
direction relative to what the console prints — almost always a sign convention mismatch between
`degrees_off_center` and which motor throttle sign corresponds to "left" vs. "right" on that
particular car; verify against the Class 3 wiring before assuming the scan logic itself is wrong.

**Time check:** At the 30-minute mark, do a quick show-of-hands: "Whose rover has completed a full
drive-scan-turn cycle and avoided at least one obstacle?" Redirect instructor attention to pairs
still stuck.

### 5f. Closing / Wrap-up — ~10 min

**What to do:** Ask 2-3 volunteers to run their rover live in the shared floor area for the group,
with an obstacle placed in its path, and pull up that same student's rover status website on the
projector alongside the live run so the group watches `scan_heading`/`drive_state`/`stop_reason`
change in real time with what the rover is actually doing. Open the "how would you actually measure
this?" discussion — push past "it didn't hit anything" toward something more specific (number of
successful avoidances per run, distance maintained from obstacles, consistency across repeated runs,
and whether a wheel's website speed reading dropping to near zero mid-run reveals a stuck wheel before
the rover itself reports a collision).

**What to say:** "You just watched a car built entirely from parts and code you wrote yourselves,
across five Classes, make its own decisions about which way to go — and now you can watch it make
those decisions live on a webpage, not just in a scrolling console. Wheel odometry showed you speed
and slip, the IMU added heading, and today's website shows the rover's actual collision-avoidance
choices too — everything the car currently knows about itself and the room around it, in one place.
That's the whole course coming together. Next Class isn't about new concepts — it's about finishing
and tuning this exact rover, and for anyone who wants to go further, there are stretch goals that
bring back your Class 1 encoder and Class 4 IMU."

**Preview next Class:** Class 6 needs no new wiring for its core work — it's tuning today's rover,
including today's bump switch (`GP5`) and IR sensor (`GP13`), both carried forward unchanged. The
optional stretch goals reconnect Class 1's encoder (`GP3`/`GP4`) and Class 4's IMU (`GP0`/`GP1`)
exactly as already wired, alongside today's rover circuit; a TFT display stretch goal is the only new
wiring, on pins not used anywhere else in the course. Today's `scan_heading`/`drive_state`/
`stop_reason` website fields carry forward unchanged into Class 6. Point students to the Class 6
references in the syllabus if they want to read ahead.

## 6. Troubleshooting Guide

| Problem | Likely Cause | Fix |
| :-------- | :------------- | :---- |
| Rover doesn't drive at all | `motor_driver.py` missing from CIRCUITPY, or 9V battery dead | Confirm `motor_driver.py` is present alongside `code.py`; check battery voltage |
| Rover drives but never stops to scan | `SCAN_INTERVAL` too long, or `STOP_DISTANCE_CM` too small to ever trigger | Lower `SCAN_INTERVAL` and/or raise `STOP_DISTANCE_CM` and re-test |
| Rover stops constantly, barely drives | `STOP_DISTANCE_CM` set too large, triggering on normal sensor noise | Lower `STOP_DISTANCE_CM` in small steps |
| Rover scans but always turns the same direction regardless of readings | Scan readings all `None` (sensor errors), falling back to `CENTER_ANGLE` every time | Check Class 2's sensor wiring; confirm `read_distance()` isn't always returning `None` |
| Rover turns the wrong way relative to the printed chosen heading | Motor sign convention doesn't match `degrees_off_center`'s left/right assumption | Swap the sign in `turn_toward()`'s `motor_driver.drive()` calls, or confirm against Class 3's wiring |
| Rover's turns overshoot or undershoot the intended heading | `TURN_SECONDS_PER_DEGREE` not recalibrated from Class 3's actual measured turn time | Recalculate from a fresh measured 90-degree turn, same method as Class 3 |
| Console floods with `distance_cm: reading error` during a scan | Servo moved before the sensor settled, or sensor aimed at an out-of-range surface | Increase `SETTLE_TIME`; re-aim the test area to stay within the sensor's usable range |
| Rover works on the bench but behaves erratically on the floor | Wheels slipping on the test surface, or floor surface interfering with the ultrasonic beam (e.g. thick carpet edges) | Test on a harder, flatter surface; treat as a real-world limitation to discuss, not just a bug |
| Bump switch never triggers even on a hard hit | Lever arm not mounted low/forward enough to actually contact obstacles, or `GP5` wiring loose | Reposition the switch so the lever leads the chassis edge; re-verify wiring with a multimeter continuity check |
| Rover constantly emergency-stops with nothing nearby | IR sensor's onboard sensitivity potentiometer set too high, or aimed at a reflective floor | Turn the sensor's sensitivity trimmer down; re-aim slightly upward off the floor |
| Rover reverses into something behind it after a safety stop | Backoff time too long for the available clearance | Shorten the `time.sleep(0.3)` backoff in `safety_override_triggered()`'s reverse step |
| Website's new fields (`scan_heading`/`drive_state`/`stop_reason`) never appear or never change | Old Class 4 `rover_server.py` still on CIRCUITPY, or its old `while True: server.poll()` loop wasn't removed | Confirm only one `rover_server.py` exists and it's the Class 5 version; confirm `class-5-code.py` calls `rover_server.server.poll()` itself |
| Website hangs/never responds once the rover starts driving | Both `rover_server.py`'s old loop and `class-5-code.py`'s new loop are calling `server.poll()` in separate blocking loops | Delete the old `while True: server.poll()` block from `rover_server.py` entirely — only `class-5-code.py`'s main loop should call it now |
| Website's wheel-speed/orientation fields (Classes 3-4) stopped updating after today's edit | `GP16`/`GP17` or `GP0`/`GP1` wiring bumped while wiring today's limit switch/IR sensor | Re-verify those circuits weren't disturbed; they're unrelated to today's `GP5`/`GP13` wiring |

## 7. Age Differentiation Notes

**Younger students (12-14) and their parent/guardian:** Provide the reconnection pin table above
pre-printed and laminated at the workstation as a lookup for verifying both prior circuits are still
correctly wired. Pair a younger student's floor-testing (holding/retrieving the rover, placing
obstacles) with the parent/guardian's help reading console output aloud. Start from `class-5-code.py`
already loaded, and have them focus on tuning the four constants (`DRIVE_SPEED`, `STOP_DISTANCE_CM`,
`SCAN_INTERVAL`, `SCAN_ANGLES`) through trial and error on the floor rather than reading the full
control-loop logic line by line. For Step 2, it's enough for them to make the edits shown and confirm
the three new fields show up on the webpage — treat the `server.poll()` relocation as "trust the code
you already saw work" material.

**Older students (15-18) and adults:** Walk them through `scan()` and `turn_toward()` line by line
and have them explain, in their own words, how the "largest reading wins" decision is made and why
`TURN_SECONDS_PER_DEGREE` is derived from Class 3's calibration rather than a fresh measurement. Once
the milestone is met, challenge them to design and run the "narrow gap vs. dead-end room" test
scenario from Direct Teaching and document what actually happened versus what they predicted. For
Step 2, have them explain why `rover_server.py`'s old blocking `while True: server.poll()` loop had to
be removed once `class-5-code.py` needed its own continuous loop — this is exactly the stretch-refactor
Class 4 flagged as optional and never required; today it becomes necessary rather than optional.

## 8. Assessment

**Milestone Assignment (per syllabus, Phase 3 / Class 5):** Car drives autonomously and avoids at
least one obstacle without instructor intervention, with the rover's full state visible together on
its status website.

**What "complete" looks like:** The student can set their rover driving in the shared open floor
area, place an obstacle in its path, and show it stop, scan, choose a heading, turn, and continue
driving — without the student touching the car or the keyboard once it starts. One successful
avoidance during a live demo is sufficient; this is a completion-based milestone, not a reliability
benchmark. In addition, the student can open their Pico's rover status website and point to
`scan_heading`, `drive_state`, and `stop_reason` updating live alongside the wheel speed/direction and
orientation fields already there from Classes 3-4.

**How to give feedback without scoring:** Ask the student to narrate what the console printed during
the moment of avoidance — what triggered the stop, what the scan readings were, why that heading was
chosen — rather than checking a box. Separately, ask them to point at the webpage and explain why
adding today's fields didn't require any change to the HTML/JavaScript — only to the dict returned
from `/data.json`, and why `rover_server.py` no longer runs its own `while True: server.poll()` loop.
If a pair can't get a full autonomous avoidance working in the time available, that's fine — have them
bring a working version (and the website extension) to the start of Class 6 and note it in their
build journal; Class 6 is explicitly built around continuing to tune this exact rover.

## 9. Instructor Tips

* Run the reference rover yourself, live, in the shared floor area *before* students touch their own
  cars — watching a fully autonomous stop-look-go cycle happen once, start to finish, sets
  expectations far better than describing it.
* Today's Class is the first time most rovers will run untethered (on battery, off the bench) for
  extended periods — have spare charged 9V batteries in easy reach rather than mid-Class scrambling.
* The "steer toward the largest reading can pick a bad direction" discussion (Direct Teaching) lands
  much better if you can physically demonstrate it with a real narrow-gap-then-open-space setup
  during Independent Work, rather than only discussing it abstractly.
* If a pair's rover consistently turns the wrong direction, check the sign convention mismatch
  (Troubleshooting) before assuming their scan logic itself is broken — it is by far the most common
  root cause of "my rover works backwards."
* Keep `class-5-code.py` and a reminder that `motor_driver.py` (from Class 3) must still be present
  on a shared drive/USB stick, since a student who reformatted or cleaned their CIRCUITPY drive
  between Classes will otherwise get a confusing `ImportError` with no obvious cause.
* Test the bump switch and IR sensor mounts on the reference rover before students arrive — a
  loosely-taped sensor or a switch lever that doesn't lead the chassis edge will silently never
  trigger, and that failure mode is easy to miss until a student's rover actually hits something.
* Step 2's website edit is small on purpose — resist the urge to re-teach `adafruit_httpserver` or
  WiFi setup from scratch; if a pair never got the Class 3/4 website working, point them back to those
  Classes' troubleshooting guides rather than debugging WiFi live during today's Guided Practice. The
  one genuinely new idea is relocating `server.poll()` into the rover's own main loop — walk that part
  once, clearly, since it's the one piece that isn't just "add another field."

## 10. Resources & References

* [Raspberry Pi Pico W taught this car to avoid objects][01] — a real-world example of Pico-based
  obstacle avoidance, similar in spirit to today's build
* [How to make an obstacle avoidance robot using Raspberry Pi Pico board][02] — a step-by-step
  obstacle-avoidance build guide, useful as a cross-reference
* [Obstacle Avoidance Robot Using Raspberry Pi Pico][03] — another worked example of combining a
  distance sensor and motor driver for collision avoidance

---

[01]:https://www.raspberrypi.com/news/raspberry-pi-pico-w-taught-this-car-to-avoid-objects/
[02]:https://srituhobby.com/how-to-make-an-obstacle-avoidance-robot-using-raspberry-pi-pico-board/
[03]:https://circuitdiagrams.in/obstacle-avoidance-robot-using-raspberry-pi/
