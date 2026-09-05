# Lesson Script: Class 6 — Finish the Random Rover + Stretch Goals


* **Class:** 6 of 6 (plus Pre-Class)
* **Duration:** ~2 hours
* **What You'll Need:** see [Section 2](#2-what-youll-need)
* **Before You Start:** Your Class 5 Random Rover should be working, even if imperfectly —
    Class 2's sensor+servo circuit (`GP6`-`GP8`), Class 3's motor driver circuit (`GP9`-`GP12`), and
    Class 5's limit switch/IR sensor (`GP5`/`GP13`) combined into `class-5-code.py`'s stop-look-go
    loop, with `motor_driver.py` present on your `CIRCUITPY` drive. Class 1's encoder circuit should
    still be intact on your breadboard, even though unused since Class 1 — you'll reconnect it today
    if you attempt Stretch 1. Class 4's IMU circuit should also still be intact, but it's not
    actually idle: `rover_server.py` has kept reading it every request since Class 4, since the
    website has carried orientation data all along — Stretch 2 below just adds a history chart on
    top of readings the site is already serving.

---


## 1. What This Project Is

This is the last class of the course, and it has two parts. First: finish and tune the rover you
built in Class 5 — no new concepts, just calibration and debugging until it reliably avoids
obstacles. Second: three completely optional stretch goals, each one reconnecting a circuit you
already built in an earlier class rather than introducing new hardware:

* **Stretch 1** — bring back your Class 1 rotary encoder to control the rover's drive speed live,
    while it's driving.
* **Stretch 2** — add a rolling-history chart to the rover status website that's been running since
    Class 3, so recent trends in tilt and wheel speed scroll by instead of only the current instant.
* **Stretch 3** — add a small screen right on the robot showing its distance/heading/speed status,
    readable without a laptop attached at all.

You pick which one(s) to attempt, based on interest and time — doing zero of them with a great
core rover is a completely valid outcome today. The class ends with every student demonstrating
their working rover to the group.

## 2. What You'll Need

| Component | Quantity | Purpose This Project |
| :---------- | :--------: | :---------------------- |
| Raspberry Pi Pico 2 W (with header) | 1 | Runs your CircuitPython code |
| Complete Class 5 rover circuit | 1 | The rover you're finishing and tuning |
| KY-040 rotary encoder (from Class 1, already wired) | 1 | Stretch 1: live speed control |
| LSM9DS1 9-DOF IMU (from Class 4, already wired) | 1 | Stretch 2: source of the roll/pitch history plotted on the already-running rover website |
| 1.14" 240x135 color TFT display | 1 | Stretch 3: on-board status display (new wiring) |
| Breadboard (from prior classes) | 1 | All prior circuits stay on it |
| Dupont jumper wires | as needed | New wiring for stretch 3 only |
| USB cable or portable battery | 1 | Power, or untethered floor runs |
| Laptop with Mu or Thonny | 1 | Where you write/save code |
| Laptop with a web browser | 1 | Views the stretch 2 rolling-history chart on the already-running rover website |

**Additional components for the Homework Assignments** (Section 11) — no homework has been written
for this class yet; this section will be filled in when that content is added.

## 3. Meet the Hardware

**Core rover:** no new hardware — you're tuning the exact circuit from Class 5.

**Stretch 1 — rotary encoder (recap from Class 1).** No new wiring at all. The same debounced
`CLK`/`DT` reading technique from Class 1 now feeds a live `current_speed` value into
`motor_driver.drive()` instead of a fixed constant — this is a change to the *control loop*, not a
new input concept. Driving slower doesn't make the rover's scan-and-choose decisions any smarter;
it just gives the decision loop more distance-per-scan margin, which can make a fixed
`SCAN_INTERVAL` behave more safely without touching the scanning code itself.

**Stretch 2 — growing the same website again, not building a new one.** The rover status website
has been running continuously since Class 3: that class gave it live wheel speed/direction and the
first version of `rover_server.py`, Class 4 added IMU orientation, and Class 5 refactored it into a
library and added the collision-avoidance decision. All three edited the *same* file and the *same*
`/data.json` route — nothing was ever rebuilt from scratch. Today's stretch does the same thing
again: it `import`s `rover_server` (Class 5's library version), adds a rolling history buffer (the
last ~150 readings of roll/pitch and wheel speed) to the page that's already running, and draws a
hand-drawn HTML5 canvas chart of it. No new WiFi join, no new web server, no new `settings.toml` —
that plumbing has been live since Class 3.

**Stretch 3 — TFT display over SPI (new wiring, new protocol).** The ST7789 TFT connects over
**SPI**, a different protocol from the I2C used for the IMU and the PWM/GPIO used for the servo
and motors — this is the only genuinely new wiring in Class 6. The display's content, though, is
just the same distance/heading/speed values your rover already computes; SPI is simply a fast,
dedicated protocol for pushing pixel data to a screen.

**Pinout summary** (only stretch 3 uses new pins; stretches 1 and 2 reuse existing wiring exactly):

| Pin | What we use it for | Status |
| :---- | :--------------------- | :------- |
| `GP3`/`GP4` | Rotary encoder `CLK`/`DT` | Reused from Class 1 |
| `GP0`/`GP1` | LSM9DS1 `SDA`/`SCL` | Reused from Class 4 |
| `GP18` | TFT `SCK` | New |
| `GP19` | TFT `MOSI` | New |
| `GP20` | TFT `CS` | New |
| `GP21` | TFT `DC` | New |
| `GP22` | TFT `RST` | New |

## 4. Build It: Tune Your Core Rover

### Wiring for this phase

No wiring changes. Confirm your Class 5 rover circuit is intact — if it regressed (loose sensor
mount, dead 9V battery, a missing `motor_driver.py`), restore it to a known-working Class 5 state
before attempting any stretch goal.

### What to do

Revisit `class-5-code.py`'s constants — `DRIVE_SPEED`, `STOP_DISTANCE_CM`, `SCAN_INTERVAL`,
`SCAN_ANGLES`, `TURN_SECONDS_PER_DEGREE` — and adjust them based on what you observed in Class 5.
This is debugging and tuning, not new code: treat it as a continuation of Class 5's Independent
Work. Aim for a rover that reliably completes a full stop-look-go cycle and avoids at least one
obstacle without you touching it.

### Checkpoint

Run your rover on the open floor area and confirm it drives, stops to scan, turns toward open
space, and resumes — repeatedly, without intervention — before moving on to any stretch goal.

## 5. Stretch Goal 1 — Live Encoder Speed Control

### Wiring for this stretch goal

No new wiring — reconnect Class 1's encoder exactly as it was wired:

| Component | Pico 2 W Pin |
| :---------- | :------------- |
| Rotary encoder `CLK` | `GP3` |
| Rotary encoder `DT` | `GP4` |

### What this code does

This demonstrates the *pattern* for live speed control: it reads the encoder the same debounced
way Class 1 did, and raises or lowers a `current_speed` variable within `MIN_SPEED`/`MAX_SPEED`
bounds as you turn the knob, printing the new speed each time it changes.

### The code

Run this standalone first (as `code.py`) to see the pattern work on its own:

```python
# class-6-code-1.py
# Stretch 1: live encoder speed control -- demonstrates the pattern standalone.

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

print("Class 6, Stretch 1 -- encoder speed control starting, current_speed:", current_speed)

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

    # To fully integrate: replace class-5-code.py's DRIVE_SPEED constant with
    # this current_speed value, updated inside the main drive loop, instead
    # of running this file standalone.
    time.sleep(0.001)
```

### Try it / what you should see

Turn the knob one direction and watch `current_speed` climb in steps of `0.05`, capped at
`MAX_SPEED`. Turn it the other way and watch it fall, capped at `MIN_SPEED`.

### Checkpoint, and how to fully integrate

Running this file standalone only demonstrates the pattern. To actually use it, merge it into
`class-5-code.py`: replace the `DRIVE_SPEED` constant with a `current_speed` variable that this
encoder-reading code updates inside the main drive loop, and use `current_speed` everywhere
`class-5-code.py` currently uses `DRIVE_SPEED` in its `motor_driver.drive()` calls.

## 6. Stretch Goal 2 — Rover Website History Chart

### Wiring for this stretch goal

None. No new WiFi join, no new `settings.toml`, no new IMU wiring — everything this stretch needs
(the classroom WiFi connection, `adafruit_httpserver`, the Class 4 IMU on `SDA` `GP0`/`SCL` `GP1`)
has been running since Class 3 and is already on your board.

### What this code does

This does **not** join WiFi or start a server — it `import`s the already-running `rover_server`
module (the same file since `class-3-code-4.py`, extended in Classes 4-5) and edits it in place: a
rolling ~150-sample history buffer, plus a hand-drawn HTML5 canvas chart added to the existing
status page, polling the existing `/data.json` route every 200ms and plotting `roll`/`pitch`
(already in the response since Class 4) and wheel speed (already in the response since Class 3)
over time. You're not building a new website — you're adding to the one that's been running since
Class 3.

### The code

`class-6-code-2.py` is a small module imported *alongside* `class-5-code.py` (or
`class-6-code-1.py`, if you merged Stretch 1) — it is not saved as `code.py` on its own, since it
has no main loop of its own to run.

```python
# class-6-code-2.py
# Stretch 2: add a rolling-history chart to the rover website already running
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

### Try it / what you should see

Open your Pico's status webpage in a browser on the classroom WiFi, the same page you've had
running since Class 3 — you should now see the same wheel-speed/orientation/scan-state numbers as
before, plus a new "Recent History" chart below them that scrolls as the rover drives: an orange
line for roll, a blue line for pitch, and a green line for left wheel speed.

If the chart never appears, confirm `class-6-code-2.py` actually ran (it must be imported by
`code.py` alongside the Class 5 rover code, not run standalone in place of it) and that it ran
*after* `rover_server` was imported, so `rover_server.STATUS_PAGE` exists to edit. If the chart
appears but never scrolls, the rover's main loop has stopped calling
`rover_server.server.poll()` — the same failure mode Class 5 already taught you to check for.

### Checkpoint

Confirm the chart appears below the existing status fields and scrolls live as the rover drives,
plotting roll, pitch, and left wheel speed, while the Classes 3-5 fields above it keep updating
too.

## 7. Stretch Goal 3 — On-Board TFT Status Display

### Wiring for this stretch goal

This is the only genuinely new wiring in Class 6:

| Component | Pico 2 W Pin |
| :---------- | :------------- |
| TFT `SCK` | `GP18` |
| TFT `MOSI` | `GP19` |
| TFT `CS` | `GP20` |
| TFT `DC` | `GP21` |
| TFT `RST` | `GP22` |
| TFT `VIN`/power | `3V3` |
| TFT `GND` | `GND` |

### What this code does

This sets up the ST7789 TFT display over SPI and shows three lines of large text: distance,
heading, and speed. It ships with placeholder demo values that count up on their own — swapping
those for your rover's real values is the integration step.

### The code

Save as `code.py`.

```python
# class-6-code-3.py
# Stretch 3: ST7789 TFT status display -- distance/heading/speed on-board, no laptop needed.

import time
import board
import displayio
import busio
from fourwire import FourWire
from adafruit_st7789 import ST7789
import terminalio
from adafruit_display_text import label

# Always release any previously-active display before creating a new one --
# skipping this is the most common cause of a blank/garbled screen.
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

print("Class 6, Stretch 3 -- TFT status display starting...")

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

### Try it / what you should see

The TFT should light up showing three lines of text, with the distance number counting up on its
own as a placeholder. If the screen is blank or garbled, double-check the SPI pins against the
table above and confirm `displayio.release_displays()` ran before the display was created.

### Checkpoint

Confirm the screen displays readable text for all three lines. Full integration — replacing the
demo values with your rover's real distance/heading/speed — is the natural next step if time
allows.

## 8. Troubleshooting Guide

| Problem | Likely Cause | Fix |
| :-------- | :------------- | :---- |
| Core rover regressed since Class 5 | Loose connection, dead 9V battery, or a missing `motor_driver.py`/`class-5-code.py` file | Restore to the known-working Class 5 state before attempting any stretch goal |
| Stretch 1: `current_speed` never changes | Encoder wiring drifted since Class 1, or the code wasn't actually merged into the drive loop | Verify `CLK`/`DT` on `GP3`/`GP4`; confirm the merge step was done, not just run standalone |
| Stretch 1: speed changes but the rover jerks or stalls at low speed | `MIN_SPEED` set below the DRV8833's usable stall threshold from Class 3 | Raise `MIN_SPEED` closer to the value found usable in Class 3 |
| Stretch 2: chart never shows up on the page at all | `class-6-code-2.py` never ran, or ran before `rover_server` was imported so `STATUS_PAGE` didn't exist yet | Confirm `code.py` imports `rover_server` first, then runs `class-6-code-2.py`'s edit |
| Stretch 2: chart appears but is flat/frozen, other fields on the page also stopped updating | Rover's main loop stopped calling `rover_server.server.poll()` (same failure mode Class 5 introduced) | Confirm the main drive loop still calls `rover_server.server.poll()` every cycle |
| Stretch 2: other fields (Classes 3-5) keep updating but the chart alone never appears/grows | `/` route re-registration didn't take effect, or the browser is caching an old page | Hard-refresh the browser page; confirm only one `@rover_server.server.route("/")` handler is defined |
| Stretch 2: chart plots roll/pitch but not wheel speed (or vice versa) | `drawSeries` called with a field name that doesn't match `/data.json`'s actual key (e.g. `speed_left_cms`) | Check the exact field names already established in Classes 3-5's `/data.json` response |
| Stretch 3: blank/garbled TFT screen | SPI pins mismatched, or `displayio.release_displays()` was omitted | Verify pins against the table; always call `release_displays()` before creating a new display object |
| Stretch 3: TFT shows only demo values | Demo variables never replaced with the real rover variables | Expected unless full integration was completed — not a bug, just an unfinished integration step |
| `ImportError` for `adafruit_httpserver`, `adafruit_st7789`, `fourwire`, or `adafruit_display_text` | Library not copied to `/lib` on your `CIRCUITPY` drive | Copy the missing library file(s) from the Library Bundle into `/lib` |

## 9. Put It All Together

There's no single "complete" combined build this class — the core rover and each stretch goal are
independent add-ons, and you choose which to include. Below is each piece's full wiring and code
in one place, so you can build straight to whichever combination you want.

### Complete wiring (all pieces)

| Component | Pico 2 W Pin | Needed for |
| :---------- | :------------- | :----------- |
| HC-SR04 `TRIG` | `GP6` | Core rover |
| HC-SR04 `ECHO`, through voltage-divider | `GP7` | Core rover |
| SG90 servo signal | `GP8` | Core rover |
| DRV8833 `AIN1`/`AIN2` | `GP9`/`GP10` | Core rover |
| DRV8833 `BIN1`/`BIN2` | `GP11`/`GP12` | Core rover |
| Limit switch (internal pull-up) | `GP5` | Core rover |
| IR obstacle sensor `OUT` | `GP13` | Core rover |
| Rotary encoder `CLK`/`DT` | `GP3`/`GP4` | Stretch 1 |
| LSM9DS1 `SDA`/`SCL` | `GP0`/`GP1` | Stretch 2 |
| TFT `SCK`/`MOSI`/`CS`/`DC`/`RST` | `GP18`-`GP22` | Stretch 3 |

### Complete code

Your core rover's finished code is `class-5-code.py` (from Class 5) plus `motor_driver.py` (from
Class 3) and `rover_server.py` (Class 5's library version) — this class is about tuning that
code's constants, not replacing it. Each stretch goal's complete, ready-to-run code is exactly what's
shown in its own section above: `class-6-code-1.py` (Stretch 1), `class-6-code-2.py` (Stretch 2),
and `class-6-code-3.py` (Stretch 3). Full integration of Stretch 1 or Stretch 3 means merging its
logic into `class-5-code.py` rather than running it standalone — the specific merge points are
called out in each section above. Stretch 2 is different: `class-6-code-2.py` is never merged into
`class-5-code.py`'s logic — it's simply imported alongside it (after `rover_server`) so its
one-time `STATUS_PAGE` edit and route re-registration take effect before the rover's existing main
loop starts calling `rover_server.server.poll()`.

## 10. What You Learned

You finished the course by making your own rover more reliable and, if you chose to, pushing it
further with genuinely new capabilities. Specifically, you now know:

* How to debug and tune an existing autonomous system based on real-world observation, rather than
    building it fresh
* (If attempted) How reusing an existing input (the encoder) to drive a *live* control-loop value,
    instead of a fixed constant, changes a system's behavior without changing its core logic
* (If attempted) Why a system built so each addition is a small, additive edit to the same file —
    like the rover website's `/data.json` route, grown once each Class since Class 3 — scales a lot
    further than rebuilding from scratch every time
* (If attempted) How SPI, a third communication protocol alongside the I2C and PWM/GPIO you've
    already used, drives a display — and that a display is only as useful as the data it's fed

More broadly, you built a complete physical computing system from a bare microcontroller, one
working piece at a time, over six classes: a debounced switch, a servo-swept sensor, a motor
driver, an IMU, and finally a robot that senses, decides, and acts on its own. That's the whole
discipline of physical computing, and you've now done it for real, with your own hands.

----
## 11. Homework Assignment

No homework assignments have been written for this class yet. This section will be filled in with
optional take-home exercises, following the same format as the Pre-Class homework in
[`class-00-lesson-script.md`](class-00-lesson-script.md#10-homework-assignment) (what the code
does, full commented code, and real-world examples).

## References

* [Adafruit 1.14" 240x135 Color Newxie TFT Display][01] — wiring and CircuitPython usage for the
  TFT used in Stretch 3
* [Raspberry Pi Pico W Asynchronous Web Server – MicroPython Code][02] — background on running a
  web server from the Pico W, referenced for Stretch 2's design
* [Raspberry Pi Pico W Soft Access Point Web Server Example][03] — an alternative WiFi setup
  (Pico W as its own access point), worth knowing about if classroom WiFi proves unreliable
* [Cerberus: Obstacle Avoiding Robot With Mecanum Wheels][04] - alternative physical design
  for the same type of robot

---



[01]:https://learn.adafruit.com/adafruit-1-14-240x135-color-newxie-tft-display/circuitpython
[02]:https://electrocredible.com/raspberry-pi-pico-w-web-server-asynchronous-micropython/
[03]:https://microcontrollerslab.com/raspberry-pi-pico-w-soft-access-point-web-server-example/
[04]:https://www.instructables.com/Cerberus-Obstacle-Avoiding-Robot-With-Mecanum-Whee
