# Lesson Plan: Class 6 — Finish the Random Rover + Stretch Goals

* **Class:** 6 of 6 (plus Pre-Class)
* **Phase:** Phase 3 — Integration (Class 5-6: combine sensing + motion into an autonomous robot)
* **Duration:** ~2 hours (120 min)
* **Prerequisites from prior Classes:** Class 5 completed — every student has a working (even if
  imperfect) autonomous Random Rover: Class 2's sensor+servo circuit (`GP6`-`GP8`), Class 3's
  motor driver circuit (`GP9`-`GP12`), and Class 5's limit switch/IR sensor (`GP5`/`GP13`) combined
  into `class-5-code.py`'s stop-look-go collision avoidance loop, with `motor_driver.py` present on
  the CIRCUITPY drive. Class 1's button/encoder circuit (`GP2`-`GP4`, `GP14`-`GP15`) should still be
  intact on the breadboard, even though unused since Class 1 — it's reconnected today for Stretch 1.
  Class 4's IMU circuit (`GP0`/`GP1`) should also still be intact, but it isn't actually idle:
  `rover_server.py` has kept reading it every request since Class 4, since the website has carried
  orientation data all along — Stretch 2 just adds a history chart on top of readings the site is
  already serving.

---

## 1. Class Overview

This is the sixth and final Class of the course. The first half is entirely dedicated to finishing
and tuning the Random Rover from Class 5 — no new concepts, just calibration, debugging, and
polishing whatever each student's rover still needs to reliably avoid obstacles. The second half
offers three independent stretch goals, each reconnecting a circuit from earlier in the course rather
than introducing new hardware concepts: reconnecting Class 1's rotary encoder for live speed control,
adding a rolling-history chart to the rover status website that has been running continuously since
Class 3, and adding an on-board TFT display showing the rover's live status. Students choose which
stretch goal(s) to attempt based on time and interest — none is required. The Class, and the course,
ends with every student demonstrating their working Random Rover to the group in a final showcase,
and a closing discussion connecting what was built here to Makersmiths' future line-following robot
course.

The rover website itself has now grown for four Classes straight without ever being rewritten: Class 3
gave it live wheel speed/direction, Class 4 added IMU orientation, Class 5 added the collision-avoidance
decision (scan heading, drive state, stop reason) and today's stretch #2 adds a scrolling history chart
of that same data — the same `rover_server.py` file, edited in place one more time, not a new server and
not a new WiFi join. Class 5's edit wasn't just new fields, though — it changed the file's *shape*:
`rover_server.py` went from a standalone script that ran its own blocking loop to an importable library
that exposes a `server` object and a `scan_status` dict with no main loop of its own, so `class-5-code.py`'s
collision-avoidance loop calls `rover_server.server.poll()` itself each cycle. Today's `class-6-code-2.py`
depends on that shape: it `import`s `rover_server` and edits its `STATUS_PAGE`/`server` in place rather than
starting anything new. That continuity is itself part of what this Class teaches: a small, additive edit
to a working file beats rebuilding from scratch each time.

## 2. Learning Goals

* Debug and tune a Class 5 Random Rover to more reliably complete a stop-look-go collision-avoidance
  cycle
* (Stretch, optional) Reconnect the Class 1 rotary encoder to control the rover's drive speed live,
  while it drives
* (Stretch, optional) Extend the already-running rover status website (`rover_server.py`, live since
  Class 3) with a rolling-history chart of IMU tilt and wheel speed, so recent trends scroll by
  instead of only the current instant
* (Stretch, optional) Wire and program a TFT display to show the rover's distance/heading/speed
  status directly on the robot
* Reflect on which single improvement would most help the rover's real-world reliability, drawing on
  the "what's missing?" discussions from earlier Classes

## 3. Preparation Checklist

* **1-2 days before:** Confirm every student's Class 5 rover circuit is still intact and their
  `class-5-code.py`/`motor_driver.py` files are present — a quick spot-check, not a rebuild. (~15 min)
* **1-2 days before:** Confirm `adafruit_display_text` + `displayio`-compatible ST7789 support
  (stretch #3) are present in the Library Bundle folder; have copies on a USB stick as backup.
  Not needed unless a student attempts that stretch goal. `adafruit_httpserver` (stretch #2) needs no
  new check — it's the same library already running since Class 3. (~5 min)
* **1-2 days before:** Confirm every student's `rover_server.py` (from Classes 3-5) still connects to
  the classroom WiFi and serves `/data.json` with all ten existing fields (wheel speed/direction,
  orientation, scan/drive/stop state) — nothing new to set up here, since today's stretch #2 edit is a
  small addition to this same already-working file. (~10 min)
* **Day of, before students arrive:**
  * Set out one 1.14" 240x135 color TFT display, its SPI wiring leads, and continued access to each
        workstation's existing breadboard, chassis, and rover circuit at each workstation — needed
        only for students attempting stretch #3.
  * Pre-build and test all three stretch goals at the instructor bench:
        `class-6-code-1.py` (encoder speed control), `class-6-code-2.py` (rover website history
        chart), and `class-6-code-3.py` (TFT status display), so you can speak to each from direct
        experience
        during Guided Practice. (~40 min)
  * Set up 2-3 shared demo/test areas: the open floor space from Class 5 for rover runs, and a
        table with a projector or shared screen for browsing to the stretch #2 chart page.
  * Have spare 9V batteries, TFT displays, and SPI jumper wires on hand.
* **Have ready:** A short list of discussion prompts for the closing "what's missing, looking back
  across all 6 Classes?" reflection and the "what carries forward to the line-following course?"
  discussion (see Closing below).

## 4. Materials & Components

Per-student unless noted. Component names only — see the course Bill of Materials for costs,
quantities, and sourcing.

| Component | Purpose This Class |
| :---------- | :-------------------- |
| Raspberry Pi Pico 2 W (with header) | Microcontroller running CircuitPython |
| Complete Class 5 rover circuit (HC-SR04, SG90, DRV8833, limit switch, IR sensor, chassis, 9V battery) | The rover being finished and tuned |
| KY-040 Rotary Encoder Module (from Class 1, already wired) | Stretch #1: live speed control |
| IMU: LSM9DS1 9-DOF Breakout Board (from Class 4, already wired) | Stretch #2: source of the roll/pitch history plotted on the already-running rover website |
| 1.14" 240x135 Color TFT Display | Stretch #3: on-board status display |
| Breadboard (830-point, from Class 1) | Circuit assembly surface — all prior circuits stay on it |
| Dupont jumper wires (shared) | New wiring for stretch #3 only |
| USB cable (student-supplied, from Pre-Class) | Power + serial connection, or portable battery for untethered runs |
| Windows 11 laptop with Mu or Thonny (student-supplied) | Edit and run CircuitPython code |
| Windows 11 laptop with a web browser | Views the stretch #2 rolling-history chart on the existing rover website |
| Shared: open floor area with obstacles (from Class 5) | Rover tuning and final showcase space |

## 5. Class Timeline

### 5a. Warm-up / Hook — ~10 min

**What to do:** Have every student power up their Class 5 rover and run one quick lap to confirm it
still completes at least a partial stop-look-go cycle. Ask 2-3 students what, specifically, they'd
most like to fix or improve about their rover's behavior today.

**What to say:** "Today has two parts: first, we make your existing rover better — not new code,
just tuning and debugging. Second, if your rover's solid and you want to push further, there are
three optional add-ons, and you get to pick which ones interest you most. Everyone ends today with a
rover to show off."

**What to watch for:** Rovers with a regressed Class 5 circuit (loose sensor mount, dead battery,
missing `motor_driver.py`) — get these back to a Class 5 baseline quickly, since today's time is
better spent tuning than re-debugging Class 5 from scratch.

**Time check:** If more than 2-3 rovers need real rework to get back to Class 5's baseline, handle it
during the first half of Guided Practice rather than holding up the whole class now.

### 5b. Introduction — ~10 min

**What to do:** Frame today's two-part structure and introduce the three stretch goals at a high
level, so students can start thinking about which one(s) they want to attempt.

**What to say:**

* "Every part you need for all three stretch goals is either already wired from an earlier Class, or
  uses pins nothing else in the course touches — so nothing you add today risks breaking your rover."
* "Stretch 1 brings back your Class 1 encoder to control speed live, while driving. Stretch 2 adds a
  scrolling history chart to the same rover website you've had running since Class 3 — no new WiFi
  setup, just a chart layered on top. Stretch 3 adds a screen right on the robot so you can read its
  status without a laptop attached at all."
* "Pick based on what excites you, not what you think you're supposed to do — there's no required
  order, and doing zero of them with a great core rover is a completely valid outcome today."

**Questions to ask students:** "Which of these three would actually change how your rover drives,
versus just how you observe it?" (Only stretch #1 changes drive behavior; stretch #2 and #3 are
purely about visibility/telemetry — a useful distinction to draw out before students choose.)

### 5c. Direct Teaching — ~10 min

No new hardware concepts today — this segment previews the three stretch goals' key ideas so
students can make an informed choice, and reconnects the "what's missing?" thread from earlier
Classes.

**Concept 1 — Stretch #1: live speed control is a control-loop change, not just a new input.**
Class 1's debounced encoder already works; the new part is having `class-5-code.py`'s drive loop read
`current_speed` from the encoder on every cycle instead of using a fixed `DRIVE_SPEED` constant. Ask:
"Does driving slower make the rover's decisions any smarter, or does it just give the decision loop
more time between scans relative to how far the car travels?" (Draw out: it's the latter — slower
driving doesn't improve the scan-and-choose logic itself, but it does reduce how far the car travels
between scans, which can make a fixed `SCAN_INTERVAL` behave more safely without changing the code.)

**Concept 2 — Stretch #2: growing the same website again, not building a new one (Theory of Operation,
brief).** Recall the running thread: Class 3 gave the rover status website live wheel speed/direction
and the first version of `rover_server.py`; Class 4 added IMU orientation; Class 5 added the
collision-avoidance decision. All three edited the *same* file and the *same* `/data.json` route —
nothing was ever rebuilt from scratch. Today's stretch does the same thing again: it adds a rolling
history buffer (the last ~150 readings of roll/pitch and wheel speed) and a hand-drawn HTML5 canvas
chart to the page that's already running, so recent trends scroll by instead of only the current
instant. No new WiFi join, no new web server, no new `settings.toml` — that plumbing has been live
since Class 3. Ask: "If you had to explain to someone who missed Classes 3-5 why this stretch goal
took so little new code, what would you point to?" (Draw out: the design choice made back in Class 3
— one server, one `/data.json` dict that any Class can add fields to — is exactly what makes a
four-Class-long feature additive instead of a rewrite each time.)

**Concept 3 — Stretch #3: why the TFT still needs the same status data, just displayed differently.**
The ST7789 TFT display connects over SPI (a different protocol from the I2C used for the IMU, and
different again from the PWM/GPIO used for the servo and motors) — new wiring, but the display's
actual content is just distance, heading, and speed values the rover already computes in
`class-5-code.py` and (if built) `class-6-code-1.py`. Ask: "Why might a real robot want status
readable on-board, in addition to (or instead of) a laptop connection?" (Draw out: field use without
a tethered laptop, faster debugging without needing a serial console open, and it's simply how most
finished consumer robots communicate status.)

**Concept 4 — Revisiting "what's missing?" across the whole course.**
Briefly recap the course's recurring "what's missing?" thread: Class 3 identified no
wheel/heading feedback, battery voltage sag, and wheel slip as causes of drift; Class 4 established
that orientation isn't the same as distance traveled; Class 5's rover still can't distinguish a
narrow-but-passable gap from a wide-but-shallow dead end. Ask the class to hold onto this thread for
the Closing discussion.

### 5d. Guided Practice — ~40 min

Instructor demonstrates the option students are most interested in on the projector; students work
independently or in pairs on whichever combination of core tuning and stretch goals they choose.

**No required new wiring for most students.** Stretch #1 and #2 reconnect existing circuits exactly
as wired in Class 1 (`GP3`/`GP4`) and Class 4 (`GP0`/`GP1`) — nothing to change. Stretch #3 is the
only new wiring this Class.

**Core work — tuning the Class 5 rover.** Revisit `class-5-code.py`'s constants (`DRIVE_SPEED`,
`STOP_DISTANCE_CM`, `SCAN_INTERVAL`, `SCAN_ANGLES`, `TURN_SECONDS_PER_DEGREE`) and adjust based on
each student's specific Class 5 observations and build-journal notes. This is debugging and tuning,
not new code — treat it like the Independent Work block from Class 5, continued.

**Stretch #1 wiring (all-reused from Class 1):**

| Component | Pico 2 W Pin |
| :---------- | :------------- |
| Rotary encoder `CLK` | `GP3` |
| Rotary encoder `DT` | `GP4` |

Load `class-6-code-1.py`. Reuses the Class 1 encoder to raise/lower a live `current_speed`, feeding
it into `motor_driver.drive()`.

```python
# class-6-code-1.py
# Stretch #1: live encoder speed control for the Class 5 rover.
import time
import digitalio
import board
import motor_driver

encoder_clk = digitalio.DigitalInOut(board.GP3)
encoder_clk.direction = digitalio.Direction.INPUT
encoder_clk.pull = digitalio.Pull.UP
encoder_dt = digitalio.DigitalInOut(board.GP4)
encoder_dt.direction = digitalio.Direction.INPUT
encoder_dt.pull = digitalio.Pull.UP

MIN_SPEED = 0.2
MAX_SPEED = 0.6
SPEED_STEP = 0.05
MIN_STEP_INTERVAL = 0.02  # seconds -- same debounce technique as Class 1

current_speed = 0.4  # starting value, matches class-5-code.py's DRIVE_SPEED
last_clk_state = encoder_clk.value
last_step_time = 0.0

print("Class 6 stretch 1 -- encoder speed control starting, current_speed:", current_speed)

while True:
    clk_state = encoder_clk.value
    now = time.monotonic()
    if clk_state != last_clk_state and (now - last_step_time) >= MIN_STEP_INTERVAL:
        if encoder_dt.value != clk_state:
            current_speed = min(MAX_SPEED, current_speed + SPEED_STEP)
        else:
            current_speed = max(MIN_SPEED, current_speed - SPEED_STEP)
        last_step_time = now
        print("current_speed:", round(current_speed, 2))
    last_clk_state = clk_state

    # In the full integration, replace class-5-code.py's DRIVE_SPEED constant
    # with this current_speed value in each motor_driver.drive(...) call.
    time.sleep(0.001)
```

**What to watch for:** Students should understand this file demonstrates the *pattern* — merging it
into `class-5-code.py` (replacing the `DRIVE_SPEED` constant with `current_speed`, updated inside the
main drive loop) is the actual integration step, not just running this file standalone.

**Stretch #2 wiring:** None. No new WiFi join, no new `settings.toml`, no new IMU wiring — everything
this stretch needs (the classroom WiFi connection, `adafruit_httpserver`, the Class 4 IMU on `SDA`
`GP0`/`SCL` `GP1`) has been running since Class 3 and is already on every student's board.

Load `class-6-code-2.py`. This file does **not** join WiFi or start a server — it imports the
already-running `rover_server` module (same file since `class-3-code-4.py`, extended in Classes 4-5)
and edits it in place: a rolling ~150-sample history buffer, plus a hand-drawn HTML5 canvas chart
added to the existing status page, polling the existing `/data.json` route every 200ms and plotting
roll/pitch (already in the response since Class 4) and wheel speed (already in the response since
Class 3) over time.

```python
# class-6-code-2.py
# Stretch #2: add a rolling-history chart to the rover website already running
# since Class 3. Reuses rover_server's `server` object -- no new WiFi join, no
# new adafruit_httpserver instance. This file only registers one new route and
# appends a small history section to the existing status page's HTML.
import rover_server  # Classes 3-5's website; server/scan_status already exist
from adafruit_httpserver import Request, Response

CHART_PAGE_ADDITION = """
<h2>Recent History</h2>
<canvas id="hist" width="600" height="200" style="border:1px solid #333"></canvas>
<script>
let history = [];
async function pollHistory() {
    const r = await fetch('/data.json');   // same route Classes 3-5 already serve
    const d = await r.json();
    history.push(d);
    if (history.length > 150) history.shift();  // rolling ~150-sample window
    const canvas = document.getElementById('hist');
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawSeries(ctx, canvas, history, p => p.roll, 2, 'orange');    // IMU tilt
    drawSeries(ctx, canvas, history, p => p.pitch, 2, 'blue');     // IMU tilt
    drawSeries(ctx, canvas, history, p => p.speed_left_cms, 10, 'green');  // wheel speed
    setTimeout(pollHistory, 200);
}
function drawSeries(ctx, canvas, hist, getValue, scale, color) {
    ctx.strokeStyle = color;
    ctx.beginPath();
    hist.forEach((p, i) => {
        const x = i * (canvas.width / 150);
        const y = canvas.height / 2 - getValue(p) * scale;
        i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    });
    ctx.stroke();
}
pollHistory();
</script>
"""

# Append CHART_PAGE_ADDITION into rover_server.STATUS_PAGE's existing HTML
# (before the closing </body> tag) rather than replacing the whole page, so
# the wheel-speed/orientation/scan-state numbers Classes 3-5 already show
# keep displaying above the new chart.
rover_server.STATUS_PAGE = rover_server.STATUS_PAGE.replace(
    "</body>", CHART_PAGE_ADDITION + "</body>"
)


@rover_server.server.route("/")
def index(request: Request):
    # Re-registers "/" so it serves the STATUS_PAGE string *after* today's edit
    # above. rover_server.server already exists -- nothing new is started here.
    return Response(request, rover_server.STATUS_PAGE, content_type="text/html")

# No new main loop, no new server.start(), no new server.poll() loop here --
# class-5-code.py's (or class-6-code-1.py's, if merged) existing main loop
# already calls rover_server.server.poll() every cycle; that single call keeps
# answering this new "/" route too.
```

**What to watch for:** If the chart never appears, confirm `class-6-code-2.py` actually ran (it must
be imported by `code.py` alongside the Class 5 rover code, not run standalone in place of it) and that
it ran *after* `rover_server` was imported, so `rover_server.STATUS_PAGE` exists to edit. If the chart
appears but never scrolls, the rover's main loop has stopped calling `rover_server.server.poll()` —
same failure mode Class 5 already taught students to check for.

**Stretch #3 wiring (the only new wiring this Class):**

| Component | Pico 2 W Pin |
| :---------- | :------------- |
| TFT `SCK` | `GP18` |
| TFT `MOSI` | `GP19` |
| TFT `CS` | `GP20` |
| TFT `DC` | `GP21` |
| TFT `RST` | `GP22` |
| TFT `VIN`/power | `3V3` |
| TFT `GND` | `GND` |

Load `class-6-code-3.py`. Shows distance/heading/speed as large on-board text; ships with demo
placeholder values that should be swapped for the real variables from `class-5-code.py` (and
`class-6-code-1.py`, if built) during full integration.

```python
# class-6-code-3.py
# Stretch #3: ST7789 TFT status display -- distance/heading/speed on-board, no laptop needed.
import time
import board
import displayio
import busio
from fourwire import FourWire
from adafruit_st7789 import ST7789
import terminalio
from adafruit_display_text import label

displayio.release_displays()

spi = busio.SPI(clock=board.GP18, MOSI=board.GP19)
display_bus = FourWire(spi, command=board.GP21, chip_select=board.GP20, reset=board.GP22)
display = ST7789(display_bus, width=240, height=135, rotation=270)

group = displayio.Group()
distance_label = label.Label(terminalio.FONT, text="dist: -- cm", x=10, y=20, scale=2)
heading_label = label.Label(terminalio.FONT, text="head: -- deg", x=10, y=55, scale=2)
speed_label = label.Label(terminalio.FONT, text="speed: --", x=10, y=90, scale=2)
group.append(distance_label)
group.append(heading_label)
group.append(speed_label)
display.root_group = group

print("Class 6 stretch 3 -- TFT status display starting...")

# Demo values -- replace with the real variables from class-5-code.py / class-6-code-1.py
demo_distance = 0
demo_heading = 90
demo_speed = 0.4

while True:
    demo_distance = (demo_distance + 1) % 100  # replace with a real sensor reading
    distance_label.text = "dist: {} cm".format(demo_distance)
    heading_label.text = "head: {} deg".format(demo_heading)
    speed_label.text = "speed: {:.2f}".format(demo_speed)
    time.sleep(0.2)
```

**What to watch for:** A blank or garbled screen usually means `MOSI`/`SCK`/`CS`/`DC`/`RST` are
mismatched against the wiring table, or `displayio.release_displays()` was omitted after a previous
run left a display object active — always call it first.

**What "done" looks like for this segment:** Every student has a tuned, working core rover; students
who chose a stretch goal can demonstrate it (encoder changing printed speed live, browser chart
updating, or TFT showing status text) independently of the full rover integration if time ran short.

### 5e. Independent Work — ~40 min

**What to do:** Students continue tuning their core rover and/or their chosen stretch goal(s), aiming
for the closest thing to a full integration time allows (e.g., `class-5-code.py` actually reading
`current_speed` from the encoder loop, or actually displaying real distance/heading/speed on the
TFT instead of demo values). Encourage students to prioritize one thing done well over three things
half-finished. Have them log in their build journal which stretch goal(s) they attempted and what
state each ended in.

**What to watch for:** The most common failure mode today is scope creep — a student attempting all
three stretch goals and finishing none. Redirect early toward picking one (or zero) based on the
40-minute Guided Practice demo and remaining energy/time.

**Time check:** At the 25-minute mark, do a show-of-hands on which stretch goal(s) students are
attempting, so the instructor can circulate toward the specific pairs most likely to need help with
each one. At the 35-minute mark, prompt everyone to lock in their rover for the showcase rather than
making further changes.

### 5f. Closing / Wrap-up — ~10 min

**What to do:** Run the **Final Random Rover Showcase** — each student demonstrates their working
Random Rover navigating the room and avoiding obstacles, plus any stretch goals they completed. This
is a showcase, not a competition; every student with a working demo is recognized, no elimination, no
scoring. Then run the three closing discussions: "looking back across all six Classes' 'what's
missing?' moments, which single improvement would most help the rover's real-world reliability?"; for
anyone who built stretch #2, "the rover website has now grown for four Classes straight — wheel
odometry, then orientation, then collision-avoidance state, and today a scrolling history of all of it
— without ever being rewritten; what design choice made in Class 3 made that possible, and where would
a 'rebuild it each Class' approach have broken down instead?"; and "which skills or parts from this
course carry forward to Makersmiths' future line-following robot course, and what's genuinely new
there?"

**What to say:** "Every one of you built this from a bare microcontroller, over six weeks, one
working piece at a time — a debounced switch, a servo-swept sensor, a motor driver, an IMU, and
finally a robot that makes its own decisions. That's the whole discipline of physical computing:
sensors gather data, a microcontroller decides, actuators act. You've now done that for real,
multiple times, with your own hands. And for anyone who built the rover website — it's the same file, touched in every Class since Class 3
and never rebuilt, and that's a real lesson about software design too: a system built so each addition
is a small, additive edit rather than a fresh start scales a lot further than starting over every
time."

**Preview what's next:** No further Classes in this course — point interested students toward
Makersmiths' future line-following robot course, which reuses the same Pico 2 W platform and motor
driver skills built here, with N20 geared motors and a new competitive line-sensor challenge.

## 6. Troubleshooting Guide

| Problem | Likely Cause | Fix |
| :-------- | :------------- | :---- |
| Core rover regressed since Class 5 | Loose connection, dead 9V battery, or a missing `motor_driver.py`/`class-5-code.py` file | Restore to the known-working Class 5 state before attempting any stretch goal |
| Stretch #1: `current_speed` never changes | Encoder wiring drifted since Class 1, or `class-6-code-1.py` not actually merged into the drive loop | Verify `CLK`/`DT` on `GP3`/`GP4`; confirm the merge step was actually done, not just run standalone |
| Stretch #1: rover speed changes but jerks or stalls at low speed | `MIN_SPEED` set below the DRV8833's usable stall threshold from Class 3 | Raise `MIN_SPEED` closer to the value found usable in Class 3 |
| Stretch #2: chart never shows up on the page at all | `class-6-code-2.py` never ran, or ran before `rover_server` was imported so `STATUS_PAGE` didn't exist yet | Confirm `code.py` imports `rover_server` first, then runs `class-6-code-2.py`'s edit |
| Stretch #2: chart appears but is flat/frozen, other fields on the page also stopped updating | Rover's main loop stopped calling `rover_server.server.poll()` (same failure mode Class 5 introduced) | Confirm the main drive loop still calls `rover_server.server.poll()` every cycle |
| Stretch #2: other fields (Classes 3-5) keep updating but the chart alone never appears/grows | `/` route re-registration didn't take effect, or browser is caching an old page | Hard-refresh the browser page; confirm only one `@rover_server.server.route("/")` handler is defined |
| Stretch #2: chart plots roll/pitch but not wheel speed (or vice versa) | `drawSeries` called with a field name that doesn't match `/data.json`'s actual key (e.g. `speed_left_cms`) | Check the exact field names already established in Classes 3-5's `/data.json` response |
| Stretch #3: blank/garbled TFT screen | `SPI`/`command`/`chip_select`/`reset` pins mismatched, or `displayio.release_displays()` omitted | Verify pins against the table; always call `release_displays()` before creating a new display object |
| Stretch #3: TFT shows only demo values, never real rover data | Demo variables never replaced with the actual `class-5-code.py`/`class-6-code-1.py` variables | This is expected unless full integration was completed — note as a partial-credit milestone, not a bug |
| `ImportError` for `adafruit_httpserver`, `adafruit_st7789`, `fourwire`, or `adafruit_display_text` | Library not copied to `/lib` on CIRCUITPY drive | Copy the missing library file(s) from the Library Bundle into `/lib` |

## 7. Age Differentiation Notes

**Younger students (12-14) and their parent/guardian:** Focus today's time primarily on core rover
tuning, which is accessible and valuable on its own. If attempting a stretch goal, steer toward
stretch #1 (encoder speed control) first — it reuses wiring they already understand from Class 1 and
has the most direct, observable payoff (a printed speed number changing as they turn the knob). For
stretch #2, it's enough for them to load `class-6-code-2.py` as given and confirm the chart appears
and scrolls on the already-familiar webpage — treat the `STATUS_PAGE` string edit as "trust the code
you already saw work," the same way Class 5 treated the `server.poll()` relocation. Provide the
stretch #3 pin table pre-printed and laminated if attempting the TFT.

**Older students (15-18) and adults:** Encourage attempting more than one stretch goal, and challenge
them to fully integrate a stretch goal into `class-5-code.py` (not just run it standalone) — e.g.,
merging stretch #1's `current_speed` into the actual drive loop. For stretch #2, have them explain why
today's edit needed no new WiFi join and no new `Server` object — this is the fourth Class straight
that's added to the same `rover_server.py`/`/data.json` pair, and challenge them to add a fourth
plotted series of their choice (e.g. `dir_left`, or `scan_heading`) to the existing chart on their own,
without instructor help. For the closing "what's missing?" reflection,
challenge them to sketch (on paper, no build required) what hardware addition would be needed to
solve it.

## 8. Assessment

**Milestone Assignment (per syllabus, Phase 3 / Class 6):** Final Random Rover Showcase — each
student demonstrates their working Random Rover navigating the room and avoiding obstacles.

**What "complete" looks like:** The student's rover drives autonomously and avoids at least one
obstacle during the live showcase, matching (or improving on) the Class 5 milestone. Any completed
stretch goals are demonstrated alongside the core rover. This is a showcase, not a competition — a
working core rover alone is a complete and celebrated outcome; stretch goals are bonus, not required.

**How to give feedback without scoring:** During the showcase, ask each student to narrate one thing
they changed or fixed since Class 5, and why. For students who attempted a stretch goal, ask them to
explain what it does in their own words rather than checking a box. Recognize every student who gets
a working demo running — no age brackets, no elimination, no formal scoring, per the syllabus.

## 9. Instructor Tips

* Demo all three stretch goals yourself at the start of Guided Practice, even briefly, so students
  can make an informed choice rather than guessing which one interests them from a text description
  alone.
* Actively discourage scope creep — a student who commits fully to one stretch goal (or none, and
  just polishes the core rover) will have a stronger showcase moment than one who half-starts all
  three.
* For stretch #2, resist the urge to re-teach WiFi setup, `adafruit_httpserver`, or the earlier
  `/data.json` fields from scratch — that's Class 3-5 material. If a pair never got the website
  working in an earlier Class, point them back to that Class's troubleshooting guide rather than
  debugging WiFi live during today's Guided Practice; today's stretch is only the chart addition.
* Keep the showcase celebratory and unhurried — this is the payoff moment for six weeks of work, and
  even a rover that only partially avoids obstacles deserves the same recognition as a flawless one.
* The final two discussion questions (Closing) work best as an open, unhurried conversation rather
  than a rushed wrap-up — consider trimming Independent Work by 5 minutes if the showcase and
  discussion are running long, rather than cutting the reflection short.

## 10. Resources & References

* [Adafruit 1.14" 240x135 Color Newxie TFT Display][01] — wiring and CircuitPython usage for the TFT
  used in stretch #3
* [Raspberry Pi Pico W Asynchronous Web Server – MicroPython Code][02] — background on running a web
  server from the Pico W, referenced for stretch #2's design
* [Raspberry Pi Pico Web Server Control][03] — another worked example of a Pico-hosted web server and
  control page
* [Raspberry Pi Pico W Soft Access Point Web Server Example][04] — an alternative WiFi setup (Pico W
  as its own access point) worth mentioning if classroom WiFi access proves unreliable

---

[01]:https://learn.adafruit.com/adafruit-1-14-240x135-color-newxie-tft-display/circuitpython
[02]:https://electrocredible.com/raspberry-pi-pico-w-web-server-asynchronous-micropython/
[03]:https://github.com/gurgleapps/pico-web-server-control
[04]:https://microcontrollerslab.com/raspberry-pi-pico-w-soft-access-point-web-server-example/
