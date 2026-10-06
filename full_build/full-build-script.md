# Full Build Script: The Random Rover, Start to Finish

* **Covers:** Classes 1-6 in one build session, including every Class 6 stretch goal, plus the
  complete tuning procedure
* **Time:** about 3-4 hours to build and test, plus about 4-4.5 hours to tune (two sessions)
* **Before You Start:** your laptop is set up from the Pre-Class: CircuitPython **10.x** on the Pico
  2 W (9 or later is required for the TFT's `fourwire` module), Mu or Thonny, and `uv`. You do
  **not** need to have taken Classes 1-6 — this script explains the *why* behind every wiring rule
  and every tuning knob as you go. The [lesson scripts][01] are there if you want the long version.
* Helpful reference document is [Strategy for Tuning and Calibrating the Random Rover][48].

---


## 1. What This Document Is For

The lesson scripts build the Random Rover one phase at a time over six classes, explaining
everything along the way. This script builds the *finished* rover — the Class 5 stop-look-go robot
plus all three Class 6 stretch goals (encoder speed knob, website history chart, on-board TFT
screen) — in one pass.

Use it to build the rover if you're jumping straight to the finished robot, to rebuild your rover
after the course, to build a second one, or to recover from a rover that's been taken apart.

It has three jobs, in order:

1. **Build it** (Sections 2-6) — plan the breadboard, wire it, install the code.
2. **Test it** (Section 7) — prove every part works.
3. **Tune it** (Section 8) — replace the starting guesses in the code with numbers that fit *your*
    rover. This is where a rover that "works" becomes a rover that works *well*.

You'll see short boxes marked **Why?** throughout. Each one gives you, in a few sentences, the
reason a lesson script spent a whole phase teaching. Read them — they're what lets you fix things
when they go wrong.

The code here is the lesson-script code, unchanged, with one exception: Class 6 left the speed knob
and TFT screen as standalone demos, so this build adds a small amount of glue to run them *inside*
the rover (see [The Code][25]). Every tuning value starts at the same placeholder value the
Class 5 and Class 6 lesson scripts use.


## 2. Plan the Breadboard First

Lay out the 830-point breadboard before you place a single wire. Getting power right up front
prevents most of the hard-to-find bugs later.

> **Why? Three power levels, one ground.** The rover has three voltages. The motors get raw 9V
> straight from the battery, because they need the push and they make electrical noise you don't
> want near the Pico. The buck converter turns 9V into a clean 5V for the Pico, servo, and
> ultrasonic sensor. The Pico turns that into 3.3V for everything else. But every signal wire —
> say, `GP9` telling the DRV8833 "go" — is measured as "volts above ground." If the battery's ground
> and the Pico's ground aren't the same wire, the DRV8833 has no shared zero to measure against, and
> it behaves randomly even though every part has power. That's why *every* `GND` lands on one
> connected ground ([Class 3][35]).

```text
+5V  rail (top +)       ===========================================================
GND  rail (top -)       ===========================================================
                                           [ TFT ] [ Rotary Encoder ]
USB end of the board -> [ Pico 2W ][ DRV8833 ]                   [ Buck Converter ] <- far end
                                             [ 1K & 2K Resistors ]
GND   rail (bottom -)   ===========================================================
+3.3V rail (bottom +)   ===========================================================
```

1. **Pico and DRV8833 together at one end.** Put the Pico 2 W at one end of the breadboard with its
    USB port facing off the end, and the DRV8833 motor driver right next to it. Short signal wires
    (`GP9`-`GP12`) make for reliable motor control.
2. **Buck converter at the other end.** It's the noisiest, warmest part — keep it away from the IMU
    and the Pico.
3. **One rail pair is 5V, the other is 3.3V.** The top `+` rail is **5V** (fed by the buck converter's
    `OUT+`, and it feeds the Pico's `VSYS`). The bottom `+` rail is **3.3V** (fed from the Pico's
    `3V3` pin, labeled `3V3(OUT)`). Label them with tape — mixing them up is the costliest mistake in
    this build.
4. **Every `-` rail is GND, and they're all one ground.** Jumper the top `-` rail to the bottom `-`
    rail. Then connect to that ground: the Pico `GND`, the DRV8833 `GND`, the buck converter `OUT−`
    and `IN−`, and the 9V battery `−`. Every device's `GND` goes to a `-` rail. A missing common
    ground gives you a rover that "sort of" works.
5. **9V never goes on a rail.** The battery `+` runs through the chassis on/off switch, then splits
    to exactly two places: the buck converter `IN+` and the DRV8833 `VM`. Nothing else ever touches
    9V. To make the split, plug the switch's output lead into an empty breadboard row (a column of 5
    holes, *not* a `+`/`-` rail), then run one jumper from that row to buck `IN+` and one to DRV8833
    `VM`.


> **⚠ DANGER TO HARDWARE** — set the buck converter to 5.0 V with a multimeter **before** its output
> touches the 5V rail. The Pico's `VSYS` is rated for 5.5 V at most, and the servo and HC-SR04 share
> that rail. Never turn the buck converter's trimpot while the Pico is connected.


## 3. What You'll Need

| Component | Qty | First used |
| :-------- | :-: | :---------: |
| Raspberry Pi Pico 2 W (with header) | 1 | Pre-Class |
| 830-point breadboard, Dupont jumper wires | 1, many | Pre-Class |
| * KY-040 rotary encoder | 1 | Class 1 |
| * HC-SR04 ultrasonic sensor + 1 kΩ and 2 kΩ resistors | 1 | Class 2 |
| * SG90 micro servo | 1 | Class 2 |
| Emo Smart Robot Car Chassis Kit (2 TT motors, wheels with encoder discs, on/off switch) | 1 | Class 3 |
| Adafruit DRV8833 dual H-bridge motor driver | 1 | Class 3 |
| 5V buck converter module | 1 | Class 3 |
| 9V battery + clip, plus one spare battery for tuning | 1 + 1 | Class 3 |
| Slot-type IR optocoupler (wheel speed) | 2 | Class 3 |
| * 1000 µF electrolytic capacitor, 16 V or higher | 1 | Class 3 (optional there; required here) |
| Adafruit LSM9DS1 9-DOF IMU + STEMMA QT-to-male-header cable | 1 | Class 4 |
| * Micro limit switch (bump switch) | 1 | Class 5 |
| * IR obstacle avoidance sensor | 1 | Class 5 (Pre-Class homework) |
| * Adafruit 1.14" 240x135 ST7789 TFT display | 1 | Class 6 (Pre-Class homework) |
| Long male Dupont leads (2 per motor) and short female Dupont leads (for the switch) | 4 + 2 | Class 3 |
| Blu Tack, soldering iron, multimeter, small screwdriver | — | Class 3 |
| USB cable, laptop | 1 | Pre-Class |
| Rover stand (a cup or box that lifts the wheels off the table) | 1 | Class 3 |
| * Phone with a compass app | 1 | Class 5 |
| Tuning extras: masking tape, tape measure, paper protractor, 4-6 cardboard boxes | — | Tuning (Section 8) |

>**NOTE:** Starting from scratch? You need everything. Rebuilding a Class 4 rover? Items with "*"
>are new or changed since Class 4: the bump switch, IR sensor, TFT, and (if you skipped it) the
>capacitor are new parts; the HC-SR04, servo, and encoder are already on your breadboard but get
>rewired (see the wiring table).


## 4. Wiring

Wire in the order of the table: power first, then each device. Trace each row out loud as you go.<br>
**Pinouts:** [Pico 2 W][03], [DRV8833][04], [LSM9DS1][05], [HC-SR04][06], [SG90][07], [IR optocoupler][08],
[TFT display][09], [IR Obstacle Avoidance Sensor][30], [DAOKI Micro Limit Switch][29]

| Component | Connects to | First introduced | Notes |
| :-------- | :---------- | :---------------: | :---- |
| Battery `+` | chassis on/off switch | Class 3 | solder Dupont leads to the switch and motors first |
| On/off switch output | buck `IN+` **and** DRV8833 `VM` | Class 3 | 9V — never on a breadboard rail |
| Battery `−` | GND rail | Class 3 | common ground |
| Buck converter `IN−` | GND rail | Class 3 | |
| Buck converter `OUT+` | 5V rail **and** Pico `VSYS` | Class 3 | set to 5.0 V *before* connecting |
| Buck converter `OUT−` | GND rail | Class 3 | |
| Pico `3V3(OUT)` | 3.3V rail | Class 3 | |
| Pico `GND` (two or more pins) | GND rail | Class 1 | |
| * KY-040 encoder `CLK` | `GP3` | Class 1 | |
| * KY-040 encoder `DT` | `GP4` | Class 1 | |
| * KY-040 encoder `+` / `GND` | 3.3V rail / GND rail | Class 1 | same as Class 1 — move it if an older build has it on 5V; see pitfall below |
| * KY-040 encoder `SW` | not connected | Class 1 | the rover doesn't use the push button |
| * HC-SR04 `TRIG` | `GP6` | Class 2 | |
| * HC-SR04 `ECHO` | 1 kΩ → `GP7`, with 2 kΩ from `GP7` to GND <br>**See NOTE / Diagram below** | Class 2 | divider on `ECHO`, never `TRIG` |
| * HC-SR04 `VCC` / `GND` | 5V rail / GND rail | Class 2 | `VSYS` rail, not `VBUS` (moved in Class 5) |
| * SG90 servo signal (orange) | `GP8` | Class 2 | |
| * SG90 servo `+` (red) / `GND` (brown) | 5V rail / GND rail | Class 2 | `VSYS` rail, not `VBUS` (moved in Class 5) |
| DRV8833 `AIN1` / `AIN2` | `GP9` / `GP10` | Class 3 | Motor A (left) |
| DRV8833 `BIN1` / `BIN2` | `GP11` / `GP12` | Class 3 | Motor B (right) |
| DRV8833 `SLP` (`nSLEEP`) | 3.3V rail | Class 3 | must be HIGH or the motors never move |
| DRV8833 `GND` | GND rail | Class 3 | common ground |
| DRV8833 `AOUT1`/`AOUT2` | Motor A leads | Class 3 | Motor A (left) |
| DRV8833 `BOUT1`/`BOUT2` | Motor B leads | Class 3 | Motor B (right) |
| * 1000 µF capacitor `+` / `−` | DRV8833 `VM` / GND | Class 3 | stripe side to GND; see pitfall below |
| Optocoupler A `DO` (Motor A wheel) | `GP19` | Class 3 | fork straddles the encoder disc |
| Optocoupler B `DO` (Motor B wheel) | `GP17` | Class 3 | |
| Both optocouplers `VCC` / `GND` | 3.3V rail / GND rail | Class 3 | |
| LSM9DS1 IMU `SDA` (blue) | `GP0` | Class 4 | swapped wires fail silently |
| LSM9DS1 IMU `SCL` (yellow) | `GP1` | Class 4 | swapped wires fail silently |
| LSM9DS1 IMU `VIN` (red) | 3.3V rail | Class 4 | mount far from motors and battery |
| LSM9DS1 IMU `GND` (black) | GND rail | Class 4 | mount far from motors and battery |
| * Limit switch `NO` / `COM` | `GP5` / GND rail | Class 5 | lever leads the chassis front |
| * IR obstacle sensor `OUT` | `GP13` | Class 5 | |
| * IR obstacle sensor `VCC` / `GND` | 3.3V rail / GND rail | Class 5 | low, forward-facing, tilted slightly up |
| * TFT `RST` | `GP22` | Class 6 | reset — **not** the backlight pin |
| * TFT `DC` | `GP21` | Class 6 | |
| * TFT `CS` | `GP20` | Class 6 | |
| * TFT `MOSI` (may be labeled `DA` or `MO`) | `GP27` | Class 6 | second SPI bus — `GP19` is taken |
| * TFT `SCK` (may be labeled `CL`) | `GP26` | Class 6 | second SPI bus — `GP19` is taken |
| * TFT `BL` / `Lite` (backlight) | not connected | Class 6 | on by default; on a generic board labeled `BLK`, wire it to the 3.3V rail if the screen stays dark |
| * TFT `GND` | GND rail | Class 6 | |
| * TFT `V+` or `VIN` | 3.3V rail | Class 6 | |

>**NOTE:** Rows with "*" are new or changed since the Class 4 build. Rebuilding a Class 4 rover,
>you **add** the bump switch, IR sensor, TFT, and capacitor (if you skipped it), and **rewire**
>one thing already on your board: move HC-SR04 `VCC` and servo `+` from `VBUS` to the 5V rail. (If an
>older build has the encoder `+` on 5V, move it to the 3.3V rail too.) The encoder `SW` wire on `GP18` is unused —
>unplug it or leave it; it's harmless.

**Pitfalls to check before power-on:**

* **The encoder runs on 3.3V here.** The KY-040 has its own pull-up resistors to its `+` pin, so on
    5V it puts 5V on `GP3`/`GP4`. It works just as well on 3.3V, and that keeps every signal at the
    Pico's own logic level.
* **5V parts on the 5V rail, everything else on 3.3V.** Only the HC-SR04 and the servo (and the
    Pico's `VSYS`) use 5V. A 3.3V-only part on the 5V rail can damage it *and* the Pico pin it talks to.
* **`VBUS` is not a power source for the rover.** It's only live with USB plugged in. If anything is on
    `VBUS`, the rover goes blind the moment you unplug the cable.
* **Class 1's push-button and LEDs (`GP2`, `GP14`, `GP15`) aren't used by the rover.** If they're
    still on your breadboard from Class 1, leave them or remove them — they're harmless either way.
    Starting from scratch, don't add them.
* **The 1000 µF capacitor is required here.** Class 3 called it optional, but this rover runs both
    motors, the servo, the Pico's WiFi, and every sensor from one 9V battery. The capacitor
    is a small reservoir across the motor supply that covers the motors' start-up burst so the Pico
    doesn't reset. Use one rated 16 V or higher, `+` leg to `VM`, striped `−` leg to GND — backwards,
    an electrolytic capacitor can pop.
* **Mount everything before you calibrate.** The IMU, battery, and motors must be in their final
    places — the compass calibration measures *this* arrangement. Blu Tack holds the breadboard,
    DRV8833, buck converter, and battery to the chassis.

> **Why? The four rules that cause most "it sort of works" rovers.**
>
> 1. **The `ECHO` divider.** The HC-SR04 runs on 5V, so its `ECHO` pin answers with a 5V pulse. A
>    Pico pin is built for 3.3V, and 5V slowly damages it. The 1 kΩ / 2 kΩ pair splits the 5V so
>    `GP7` sees 5 × 2/3 ≈ 3.3V. `TRIG` doesn't need one: the Pico *sends* 3.3V to it, and the
>    sensor accepts that ([Class 2][40]).
> 2. **`SLP` (`nSLEEP`) tied HIGH.** The DRV8833 sleeps unless this pin is HIGH, and the Adafruit
>    board has no resistor holding it there. Leave it unwired and your code runs perfectly, prints
>    every line — and the motors never move ([Class 3][35]).
> 3. **`VSYS`, not `VBUS`.** `VBUS` is the USB cable's 5V. It disappears the moment you unplug the
>    laptop and the rover drives off on battery. `VSYS` is fed by the buck converter, so it's there
>    either way ([Class 5][34]).
> 4. **The TFT's second SPI bus.** The Pico's first SPI bus wants `GP19`, but the left-wheel
>    optocoupler already uses it. The second bus (`GP26`/`GP27`) avoids the clash without moving any
>    older wiring ([Class 6][38]).

**Power-on check** (USB unplugged, wheels off the table on a stand): switch on, then measure the 5V
rail (4.8-5.2 V) and the 3.3V rail (3.2-3.4 V) with a multimeter. (The Pico 2 W has no power LED —
the meter is your check.) If either rail is wrong, switch off and recheck the table before going further.

>**NOTE:** Double-check the voltage-divider resistors sit on the `ECHO` line, not `TRIG` — this is
>the single easiest wiring mistake to make in this build, and the least forgiving one, since it
>protects the Pico's GPIO pin.
>
>```text
>Make sure to use this voltage-divider circuit for the GP7 pin on the Pico
>   ECHO
>    |
> 1K ohms
>    |
>    +----------------------- GP7
>    |               ^
> 2K ohms        3.3 volts
>    |
>   GND
>```


## 5. The Code

### Software for this build

| Software component | Target | From | What it does |
| :----------------- | :----- | :--- | :----------- |
| `code.py` | Pico | **Full build** — `class-5-code.py` + Class 6 stretch glue | The stop-look-go rover, with the speed knob, history chart, and TFT screen running inside it |
| `rover_server.py` | Pico | Class 5 (unchanged) | 9-DOF Mahony filter, compass heading, and the rover status website at `http://192.168.4.1:5000` |
| `motor_driver.py` | Pico | Class 3 (unchanged) | `drive(left, right)` and `stop()` for the DRV8833, capped at `MAX_THROTTLE` |
| `wheel_odometry.py` | Pico | Class 3 (unchanged) | Wheel speed and direction for the website |
| `history_chart.py` | Pico | Class 6, `class-6-code-2.py` (unchanged) | Adds the rolling-history chart to the website |
| `speed_knob.py` | Pico | **Full build** — Class 6 Stretch 1 as a library | Turns encoder clicks into a live drive speed |
| `tft_status.py` | Pico | **Full build** — Class 6 Stretch 3 as a library | Shows real distance, heading, and speed on the TFT |
| `settings.toml` | Pico | Class 3 | Your rover's WiFi network name and password |
| CircuitPython libraries in `/lib` | Pico | Classes 1-6 | `adafruit_hcsr04`, `adafruit_motor`, `adafruit_debouncer`, `adafruit_ticks`, `adafruit_lsm9ds1`, `adafruit_httpserver`, `adafruit_st7789`, `adafruit_display_text` (+ their dependencies) |
| `mag_calibration.py` | Pico (as `code.py`, temporarily) | Class 5, `class-5-mag-calibration.py` | One-time compass calibration |
| `servo_check.py`, `motor_check.py` | Pico (as `code.py`, temporarily) | [Tuning guide][02] Steps 3 and 5 | Servo-aim and motor stall-point checks (Section 8, Steps 3 and 5) |
| `setup-test-laptop.sh` / `.ps1` | Laptop | **Full build** | Gets (or updates) this code from GitHub and pre-fetches the laptop tools' packages |
| `deploy.py` | Laptop | **Full build** | Copies everything onto the Pico |
| `wireframe.py` | Laptop | Class 4, reworked as a test tool | Live 3D box of the rover's orientation, read over WiFi |
| `device_test.py` | Pico (as `code.py`, temporarily) | **Full build** | Interactive part-by-part test |
| `system_test.py` | Laptop | **Full build** | Interactive whole-rover test against the real rover code |


### What each piece does

**`code.py` — the rover.** Class 5's stop-look-go loop: drive forward, stop when something is
closer than `STOP_DISTANCE_CM` (or every `SCAN_INTERVAL` seconds), sweep the sensor across
`SCAN_ANGLES`, turn by compass toward the most open angle, and repeat. The bump switch and IR sensor
force a stop-and-reverse at any time. Class 6's stretch goals are wired in at three points: the drive
loop reads `speed_knob` every pass, it shows each distance reading on `tft_status`, and it imports
`history_chart` right after `rover_server`. `DRIVE_SPEED` is now the *starting* speed; the knob
changes it live, including the reverse speed after a safety stop. Its log lines are Class 5's with
three changes: the start-up line reads `Full build -- Random Rover starting...`, each
`drive: forward, heading ...` line ends with `speed ...`, and a `knob: current_speed ...` line
prints each time the knob moves. While it scans or turns (up to about 4 s) it doesn't answer the
website or redraw the TFT — both catch up when it drives again. [code.py][10]

> **Why? Closed-loop turns.** Class 3 turned the rover the simple way: spin for a measured time, then
> stop, and never check the result. That's an *open-loop* turn, and it drifts as the battery drains
> or the floor changes from tile to carpet. This rover turns *closed-loop*: it picks a target compass
> heading, spins, checks the compass every 20 ms, and stops when it's within a few degrees. If it
> overshoots, the error flips sign and it spins back. Because it measures instead of guessing, it
> automatically handles a weak battery, a slippery floor, or a slow motor. The cost: if the heading
> never arrives (a jammed wheel, a backwards turn), it would spin forever — so every turn has a
> timeout, `TURN_TIMEOUT_S` ([Class 5][34]).

**`rover_server.py` — the IMU filter and website.** Unchanged from Class 5. Importing it starts the
rover's WiFi network, calibrates the gyro for about 2 seconds, and reads the compass once — so
**always boot the rover still and flat**. Your compass calibration goes in its `MAG_OFFSET` line.
[rover_server.py][11]

> **Why? "Boot still and flat."** A gyroscope always reads a tiny bit of spin even when it's sitting
> perfectly still — its *bias*. If nothing removed it, the heading would creep a few degrees every
> minute. So for the first 2 seconds after power-on, `rover_server.py` averages the gyro's readings
> and subtracts that average forever after. If the rover is moving during those 2 seconds, it
> measures your hand's motion as "bias" and steers wrong all session. It also reads the compass once
> to set its starting heading, assuming the rover is level. Habit: *set it down, switch it on, hands
> off for 3 seconds* ([Class 4][41], [IMU and Mahony filter explainer][37]).

**`motor_driver.py` and `wheel_odometry.py`** — unchanged from Class 3. [motor_driver.py][12],
[wheel_odometry.py][13]

**`history_chart.py` —** Unchanged from Class 6. It adds a "Recent History" canvas chart
(roll, pitch, heading, left wheel speed) to the existing status page. [history_chart.py][14]

**`speed_knob.py` —** Class 6's knob pattern (`MIN_SPEED`, `MAX_SPEED`, `SPEED_STEP`),
with two changes. It counts clicks with `rotaryio`, which counts in hardware in the background, so
no click is lost while the rover is scanning or answering the website. And the top of the knob is
capped at `motor_driver.MAX_THROTTLE`, since speeds above it do nothing. Turning clockwise should
speed it up, one `SPEED_STEP` per click — the device test checks both, and the file's comments say
what to change if yours runs backwards or needs two clicks per step. Every boot, the knob starts
again from `DRIVE_SPEED`. [speed_knob.py][15]

**`tft_status.py` —** Class 6's ST7789 setup, now showing the rover's *real* distance,
heading, and speed instead of demo values. It redraws at most every `REFRESH_S` seconds.
[tft_status.py][16]

**`settings.toml`** — a template with a placeholder network name and password. Change both to your
own (the password needs at least 8 characters). [settings.toml][17]

**`requirements.txt`** — the library list `deploy.py` hands to `circup`. [requirements.txt][18]

**Calibration tools.** `mag_calibration.py` is Class 5's compass calibration: tumble the rover for 30
seconds, copy the printed `MAG_OFFSET` line into `rover_server.py`. `servo_check.py` and
`motor_check.py` are the servo-aim and motor-stall tests used in Section 8, Steps 3 and 5.
[tools folder][19]

**`setup-test-laptop.sh` / `setup-test-laptop.ps1` — laptop setup.** Use the `.sh` on Linux or a
MacBook (macOS) and the `.ps1` on Windows 11. It installs `git` and `uv` if they're missing, clones this course's
repository to `~/physical_computing_for_beginners` (or pulls the latest code if it's already there),
and pre-fetches the Python packages for `deploy.py`, `system_test.py`, and `wireframe.py` — so they
still run after you join the rover's internet-less WiFi. On Linux it also adds you to the `dialout`
group so `system_test.py` can open the Pico's USB serial port (log out and back in once afterward);
macOS needs no serial-port setup.
Run it again any time to pull updates. [setup-test-laptop.sh][31], [setup-test-laptop.ps1][32]

**`deploy.py` — the installer (laptop).** Run from the `full_build` folder with `uv`. It finds the
`CIRCUITPY` drive, installs the libraries with `circup`, and copies the rover files — `code.py`
last, since saving `code.py` restarts the Pico. It never overwrites your `settings.toml`, and it
won't overwrite a file you've changed on `CIRCUITPY` (your `MAG_OFFSET`, your tuned numbers) unless
you add `--overwrite`, which backs the old file up first. [deploy.py][20]

| Command | What it does |
| :------ | :----------- |
| `uv run deploy.py rover` | Install libraries + the whole rover |
| `uv run deploy.py tool mag_calibration` | Park your rover `code.py` as `code_rover.py` and run a tool as `code.py` (also `servo_check`, `motor_check`) |
| `uv run deploy.py test` | Same, for `test/device_test.py` |
| `uv run deploy.py restore` | Put your parked rover `code.py` back |

Add `--drive E:\` (Windows), `--drive /media/you/CIRCUITPY` (Linux), or `--drive /Volumes/CIRCUITPY`
(macOS) if the drive isn't found.

**`wireframe.py` — orientation viewer (laptop).** Class 4's 3D box, reworked as a test tool. The
finished rover never prints CSV over USB, so instead it reads `/data.json` from the rover website
over WiFi, twice a second, and draws a box that follows roll, pitch, and yaw, with the compass
heading in the title. Join the rover's WiFi network, then `uv run src/laptop/wireframe.py`. Keep the
rover on its stand: every request pauses its drive loop for about 0.25 s. While the rover scans or
turns (up to about 4 s) it can't answer, so the box freezes until it drives again — that's normal.
`no answer from the rover` in the title means it stayed silent for over 6 s. On a Mac, allow your
terminal app under **System Settings → Privacy & Security → Local Network** first, or it can't
reach the rover at all (see the build pitfalls). [wireframe.py][21]

> **Why? The website makes the rover blink.** Each time a browser (or `wireframe.py`) asks the rover
> for `/data.json`, the rover spends about 0.25 s counting wheel-encoder ticks to measure wheel
> speed — and during that quarter second, its drive loop isn't checking the bump switch, IR sensor,
> or distance. With the status page open, that happens about twice a second. Turns are protected
> (they never answer the website), but straight driving isn't. This is a known limit of the course
> design, and Section 8, Step 8 tunes the rover so it's safe with the page open *or* closed
> ([Class 5][34]).

**`device_test.py` — part-by-part test (Pico).** Runs as `code.py` (via `uv run deploy.py test`)
using the same library files as the rover, so it tests the code you'll actually drive with. It walks
through every part one at a time, tells you what to do and what to watch for, waits for you to
press Enter, and asks you to confirm what you saw. It ends with a pass/fail summary.
[device_test.py][22]

**`system_test.py` — whole-rover test (laptop).** Runs against the real rover `code.py` — no
changes to it. It reads the rover's log over USB and its `/data.json` over WiFi, then coaches you
through triggering each behavior (bump, IR, close obstacle, knob, a turn) and checks that the rover
reacted. Its checks use generous ranges, so it passes the same way before and after tuning.
[system_test.py][23]


## 6. Build It

1. **Chassis.** Assemble the chassis (motors, wheels, encoder discs, caster). Solder long male Dupont
    leads to the motors and short female leads to the on/off switch.
1. **Mount.** Blu Tack the breadboard, DRV8833, buck converter, and battery to the chassis. Mount the
    servo with the HC-SR04 on its horn at the front, the limit switch with its lever leading the front
    edge, the IR sensor low and forward-facing, each optocoupler straddling its wheel's encoder disc
    (without rubbing), and the IMU as far from the motors and battery as possible. Tape the TFT where
    you can read it.
1. **Power, then measure.** Wire the power rows of the [wiring table][26]. Set the buck
    converter to 5.0 V *before* its output reaches the 5V rail. Do the power-on check.
1. **Signals.** Wire the rest of the table, one device at a time.
1. **Install the software tools (Laptop)** — on a normal, internet-connected network. This gets the
    code onto your laptop and pre-fetches the laptop tools' packages, because the rover's WiFi has no
    internet. The first time, run the one-line command for your laptop's operating system (OS):

    Do this if your **OS is Linux or macOS (MacBook)** — in Terminal on a Mac:

    ```bash
    # Linux or macOS (Shell)
    curl -LsSf https://raw.githubusercontent.com/jeffskinnerbox/physical_computing_for_beginners/main/full_build/setup-test-laptop.sh | bash
    ```

    On a Mac without Apple's Command Line Tools (which provide `git`), the script opens their
    installer and stops — finish that install, then run the command again.

    Do this if your **OS is Windows**:

    ```powershell
    # Windows 11 (PowerShell)
    powershell -ExecutionPolicy ByPass -c "irm https://raw.githubusercontent.com/jeffskinnerbox/physical_computing_for_beginners/main/full_build/setup-test-laptop.ps1 | iex"
    ```

    After that, rerun `full_build/setup-test-laptop.sh` (or `.ps1`) in your copy to pull updates.<br>

    **NOTE:** Like the command above, every command below is executed from `~/physical_computing_for_beginners/full_build`.
1. **Install Rover software (Pico 2W)** — while your laptop is still on a normal, internet-connected network.
    Plug in USB, put the rover on its stand (wheels off the table), and from the `full_build` folder
    run `uv run deploy.py rover`. On a first install it pauses after copying `settings.toml`: edit it
    on `CIRCUITPY` (your own network name and password), save, then press Enter.

    > **⚠ CAUTION** — the moment `code.py` is saved, the rover starts driving. **Keep it on its stand
    > whenever you deploy or save a file.** The battery switch is your emergency stop for the
    > motors (they run only on the 9V battery). With USB plugged in, the Pico, servo, and sensors
    > stay powered — unplug USB too to shut everything off.
1. **Watch it boot.** Open the serial console in Mu or Thonny. With the rover still and flat you
    should see the WiFi lines, `Calibrating gyro -- keep the rover perfectly still...`,
    `HTTP Server running at http://192.168.4.1:5000`, then `Full build -- Random Rover starting...`
    and the `drive:` and `scan:` lines as it runs in the air. The TFT shows `dist`, `head`, and `speed`.
1. **Calibrate the compass** (Class 5, Phase 1). Run `uv run deploy.py tool mag_calibration`, then,
    away from steel furniture, tumble the fully assembled rover through every orientation for 30
    seconds when it says `GO`: spin it flat, roll it onto each side, tip it nose-up and nose-down, even
    upside down.

    Check the three **spans** it prints are roughly equal (for example
    `(0.98, 1.02, 0.95)`); if one is much smaller, like `(0.9, 0.9, 0.1)`, you didn't roll it onto its
    sides — run it again. Then do the **axis check** with a phone compass, rover flat: `mx` clearly
    positive with the board's X arrow pointing north, `my` clearly positive with the Y arrow north,
    and `mz` negative lying flat (northern hemisphere — Earth's field dips down into the ground).

    If an axis check fails, flip that entry of `MAG_AXIS_SIGN` (for example `(-1, 1, 1)` → `(1, 1, 1)`) in
    the running tool (`code.py` on `CIRCUITPY`) *and* in `rover_server.py`, then save. Saving restarts
    the tool from the beginning, so **tumble the rover again for the full 30 seconds** when it says
    `GO`, recheck the spans, and redo the axis check; repeat until all three pass.

    Copy the `MAG_OFFSET` line from that **last** run into `rover_server.py` on `CIRCUITPY`, then
    `uv run deploy.py restore`. Also paste `MAG_OFFSET` (and `MAG_AXIS_SIGN`, if you flipped one)
    into `full_build/src/pico/rover_server.py` on your laptop, so a later
    `deploy.py rover --overwrite` keeps them.

    > **Why? Your rover is a magnet.** A magnetometer (compass) can't tell Earth's magnetic field from
    > any other one — and your rover carries its own: the motors' permanent magnets, steel screws, the
    > battery. That extra field turns *with* the rover, so it pushes every reading off by the same
    > amount. When you tumble the rover through every direction, Earth's field swings each axis evenly
    > up and down around a center point — and that center *is* your rover's own magnetic junk. The tool
    > finds it and prints it as `MAG_OFFSET`, which `rover_server.py` subtracts from every reading.
    > This only works with every part in its final place: calibrate on a bare breadboard, then mount
    > it next to a motor, and the numbers are wrong. Equal spans prove you tumbled enough; the axis
    > check proves the compass's X, Y, and Z agree with the gyro's ([Class 5][34]).
1. **Test** — [Test the Build][27].
1. **Tune** — [Tune the Rover][28].

**Pitfalls during the build:**

* **Motors never move, but the console looks normal** → DRV8833 `SLP` isn't on the 3.3V rail.
* **Both motors suddenly go dead, even one that was just working** → the DRV8833 tripped its
    overcurrent protection (usually a jammed wheel or touching motor leads), which shuts off *both*
    motors and stays off. Free the wheel, check the motor leads, then switch the battery off, wait about
    5 seconds (the capacitor has to drain), and switch it on again.
* **Everything works on USB, nothing works on battery** → something's on `VBUS`, or the buck output
    doesn't reach `VSYS`.
* **The Pico resets when the motors start** → weak 9V battery; replace it, then check the capacitor
    is in place.
* **`ImportError`** → run `uv run deploy.py rover` again (with internet) so `circup` fills `/lib`.
    If it prints `Nothing was copied` and lists your files, they differ from the laptop copies (your
    `MAG_OFFSET` or tuned numbers) and it stopped before installing libraries. Copy your values into
    `full_build/src/pico/` first and run it again, or add `--overwrite` (it backs up your old files
    to `full_build/backup/`).
* **`RuntimeError: No pull up found on SDA or SCL`** (right after the WiFi lines) → the Pico can't
    see the IMU at all. Check IMU `VIN` is on the 3.3V rail, that rail is fed from `3V3(OUT)`, IMU
    `GND` is on the GND rail, `SDA`/`SCL` are on `GP0`/`GP1`, and the STEMMA QT plug is fully seated.
    `uv run deploy.py test` narrows it down.
* **Calibration spans all tiny (under about 0.2)** → you calibrated on top of a steel desk, or the
    IMU isn't answering. Move to a wooden or plastic table.
* **`heading` wrong or creeping** → booted while moving or tilted, or the IMU moved after
    calibration. Reboot still and flat; recalibrate if anything moved.
* **A browser loads `http://192.168.4.1:5000`, but `wireframe.py` or `system_test.py` can't reach
    the rover** → on a Mac, macOS blocks programs started from Terminal from reaching local-network
    devices until you allow it, even though your browser already has permission. Open **System
    Settings → Privacy & Security → Local Network**, switch on **Terminal** (or the terminal app you
    use), then quit and reopen it. Check the `Last error:` line `wireframe.py` prints for other causes.
* **Blank TFT** → check `GP26`/`GP27`/`GP20`-`GP22` against the table, and that `RST` (not the
    backlight pin) is on `GP22`.
* **Knob turns the speed the wrong way, or needs two clicks per step** → see the comments in
    `speed_knob.py` (swap `GP3`/`GP4` in the code, or add `divisor=2`).


## 7. Test the Build

Test before you tune. Both tests use the placeholder tuning values, and both keep working,
unchanged, after you tune.

1. **Part by part.** Rover on its stand, USB plugged in, battery switch on. Run `uv run deploy.py test` and follow the
    prompts in the serial console. Fix any failed part (re-run the test) before going on. Then
    `uv run deploy.py restore`.
2. **The whole rover.** Rover on its stand, USB plugged in, battery switch on, laptop joined to the rover's WiFi
    network. Close Mu/Thonny's serial console (only one program can use the port), then run
    `uv run test/system_test.py` and follow its prompts. (If it can't find the Pico, name the port:
    `COM5` on Windows, `/dev/ttyACM0` on Linux, `/dev/cu.usbmodem...` on macOS.)
3. **Look at it.** Run `uv run src/laptop/wireframe.py`, tilt and turn the rover by hand, and check
    that the box follows and that `heading` goes **up** about 90 for a clockwise quarter turn. Then
    open `http://192.168.4.1:5000` and check the history chart scrolls.
4. **First floor run.** Unplug USB, set the rover on the floor still and flat, switch it on, hands
    off for 3 seconds. It should drive, stop, sweep, turn, and drive on. It doesn't need to be
    pretty yet — a turn that wiggles, or a stop that's a bit close, is what tuning fixes.


## 8. Tune the Rover

Your rover works — it drives, stops, sweeps its sensor, turns, and drives again. But "works" and
"works *well*" are different things. Maybe its turns overshoot and wiggle back. Maybe it taps walls
before it stops. Maybe it prints `turn timed out` on carpet. None of that means the code is wrong.
It means the rover is still running on *starting guesses* — numbers picked before your particular
motors, battery, servo, and floor existed.

This section replaces those guesses with numbers that fit *your* rover. It's adapted from the
[Strategy for Tuning and Calibrating the Random Rover][02] guide, rewritten for the full-build files
and tools, with the background from the lesson scripts added in. You don't need the guide open.

Record every change in a copy of the tuning log, [`src/tuning-log-template.md`][33] — its rows are
in the same order as the steps below. The template is shared with the tuning guide, so two small
differences: add your own Step 2 row for `SLOTS_PER_REV` (old value `20`) in **Extra rows**, and
ignore "(only if Stretch 2 is installed)" on the chart-refresh row — the full build always has the
chart.


### 8.1 What tuning is, and why bother

**Status quo.** Every Pico program in this build has a block of `ALL_CAPS` constants near the top:
`DRIVE_SPEED = 0.6`, `STOP_DISTANCE_CM = 25`, `MAG_OFFSET = (0.0, 0.0, 0.0)`, and so on. Each one is
a knob that controls how the rover behaves.

**Problem.** Those starting values were written for an *average* rover. Yours isn't average. Its IMU
sits a particular distance from a particular motor. Its servo's gears are a little off center. Its
9V battery is fresher or more tired than someone else's. Its test floor is tile, or carpet. Each
difference nudges the rover away from what the default numbers expected, and they add up.

**Solution.** Measure your actual rover and adjust the knobs to match. There are three kinds of
this work, and it helps to keep them apart:

1. **Calibration** — measuring a fixed fact about your hardware and typing it in. There's one
    right answer; you're finding it. Example: `MAG_OFFSET`, the magnetic field your own rover
    carries around.
2. **Tuning** — adjusting a number that trades one good thing against another, by testing and
    watching. There's a *best* answer for your rover, not a single correct one. Example:
    `TURN_SPEED` — too slow and the rover can't turn on carpet, too fast and it overshoots.
3. **Setting preferences** — choosing a number by taste. Nothing breaks either way. Example:
    `SCAN_INTERVAL`, how often the rover stops to look around when nothing is in its way.

A rover with good code and bad numbers behaves like a rover with bad code. Tuning is where your robot
stops being a copy of the class demo and becomes *yours*.


### 8.2 Every knob on the rover

All files below are on the `CIRCUITPY` drive. **Importance** uses five levels:

* **Critical** — get this wrong and the rover misbehaves badly, or hardware can be damaged.
* **Important** — noticeably changes how well the rover avoids obstacles.
* **Useful** — a small improvement; worth doing once the important ones are done.
* **Taste** — your preference; nothing breaks either way.
* **Leave alone** — already correct, or doesn't affect driving. Don't touch it.

| Parameter | Where it lives | Start value | What it controls | Importance | Step |
| :-------- | :------------- | :---------- | :--------------- | :--------- | :--- |
| 9V battery charge | the battery | fresh | Motor strength, and the Pico's power through the buck converter | **Critical** | 1 |
| Buck converter output | buck converter trimpot (if it has one) | 5 V | Power to the Pico's `VSYS`, the servo, and the HC-SR04 | **Critical** (can damage parts) | 1 |
| Part mounting | the chassis | — | Whether the IMU, sensor, servo, bumper, and IR sensor stay put | **Critical** | 2 |
| `SLOTS_PER_REV` | `wheel_odometry.py` | `20` | Wheel speed shown on the website and history chart | **Useful** (website only) | 2 |
| `min_pulse` / `max_pulse` | `code.py`, `servo.Servo(...)` line | `500` / `2500` | How accurately a commanded servo angle matches the real angle | **Important** | 3 |
| `CENTER_ANGLE` | `code.py` | `90` | Which servo angle means "straight ahead" | **Important** | 3 |
| `MAG_OFFSET` | `rover_server.py` | `(0.0, 0.0, 0.0)` until you calibrate | Removes your rover's own magnetic field from the compass | **Critical** | 4 |
| `MAG_AXIS_SIGN` | `rover_server.py` (and `mag_calibration.py`) | `(-1, 1, 1)` | Makes the compass axes agree with the gyro's axes | **Critical** | 4 |
| Boot still and flat | how you power on | — | Gyro bias and starting compass heading, measured at every boot | **Critical** (a habit, not a number) | 4 |
| `MAX_THROTTLE` | `motor_driver.py` | `0.6` | Hard ceiling on every motor command, including `DRIVE_SPEED`, `TURN_SPEED`, and the knob | **Critical** (can damage parts) | 5 |
| `TURN_SPEED` | `code.py` | `0.45` | How hard the rover spins during a compass turn | **Critical** | 6 |
| `HEADING_TOLERANCE_DEG` | `code.py` | `5` | How close to the target heading counts as "arrived" | **Important** | 6 |
| `TURN_TIMEOUT_S` | `code.py` | `3.0` | When to give up on a turn that never arrives | **Useful** (a safety limit) | 6 |
| `SETTLE_TIME` | `code.py` | `0.15` | How long the servo gets to stop before a distance reading | **Important** | 7 |
| `SCAN_ANGLES` | `code.py` | `[30, 60, 90, 120, 150]` | Which directions the rover looks in each scan | **Useful** / **Taste** | 7 |
| `DRIVE_SPEED` | `code.py` | `0.6` | The knob's *starting* speed at every boot — forward speed, and reverse speed after a safety stop | **Important** / **Taste** | 8 |
| `STOP_DISTANCE_CM` | `code.py` | `25` | How close an obstacle gets before an emergency stop and rescan | **Critical** | 8 |
| `SCAN_INTERVAL` | `code.py` | `3.0` | How often the rover stops to look when nothing is close | **Taste** | 8 |
| Status page refresh | `rover_server.py`, `STATUS_PAGE`'s `setInterval(..., 500)` | `500` ms | How often the website asks for new data — each request pauses the drive loop | **Useful** | 8 |
| Chart refresh | `history_chart.py`, `setTimeout(pollHistory, 200)` | `200` ms | How often the history chart asks for new data — each request pauses the drive loop | **Important** | 8 |
| IR sensor trimmer | small screw on the IR module | — | How far away the IR sensor triggers | **Important** | 9 |
| `BACKOFF_S` | `code.py` | `0.3` | How long the rover reverses after a bump or IR stop | **Important** | 9 |
| `MIN_SPEED` / `MAX_SPEED` / `SPEED_STEP` | `speed_knob.py` | `0.3` / `0.9` / `0.05` | The knob's speed range and step size | **Taste** (with limits) | 10 |
| `REFRESH_S` | `tft_status.py` | `0.2` | How often the TFT screen redraws | **Taste** | 10 |
| `MAHONY_KP`, `MAHONY_KI` | `rover_server.py` | `2.0`, `0.05` | How the IMU filter blends gyro, gravity, and compass | **Leave alone** | — |
| `CAL_SAMPLES`, `STILL_GYRO`, `STILL_ACCEL`, `BIAS_ALPHA`, `GRAVITY` | `rover_server.py` | as set in Class 4 | Automatic gyro bias correction | **Leave alone** | — |
| `WHEEL_DIAMETER_MM` | `wheel_odometry.py` | `67` | Wheel speed on the website | **Leave alone** (matches the kit's wheels) | — |
| `SAMPLE_SECONDS` | `wheel_odometry.py` | `0.25` | How long each website request counts wheel ticks — which is also how long the drive loop goes blind per request | **Leave alone** (raising it makes the blind pause longer) | — |

>**NOTE — two differences from the tuning guide.** The guide marks `SLOTS_PER_REV` "Leave alone"
>because Class 3 students already counted their encoder discs; you haven't, so Step 2 has you do
>it. And the guide lists Class 3's `straight_drive.py` and timed-turn constants; this build doesn't
>include those files at all, so there's nothing to tune.

Notice the list of things that really matter is shorter than the table looks. The bottom rows are
either already right or don't affect driving.

> **Why leave the IMU filter alone?** `MAHONY_KP` and `MAHONY_KI` control how the filter mixes a
> fast-but-drifting gyro with a slow-but-steady accelerometer and compass. Too low and the heading
> drifts; too high and it jitters. Class 4 let students nudge `MAHONY_KP` to feel that trade-off, but
> the defaults `2.0` and `0.05` already work well for this IMU, and the rover's turns depend on the
> heading staying smooth. Changing them gives you a new problem to chase, not a better rover
> ([Class 4][41]).


### 8.3 The strategy: build from the ground up

A rover is a stack of layers, and each layer depends on the ones below it. Tuning a high layer
before the low ones are right is like leveling a picture frame on a crooked wall — you'll just have
to do it again.

```text
                +------------------------------+
   Step 10      |  PREFERENCES (taste)         |  speed knob, screen refresh
                +------------------------------+
   Steps 8-9    |  BEHAVIOR                    |  drive speed, stop distance,
                |                              |  scan timer, IR range, backoff
                +------------------------------+
   Steps 6-7    |  TURNING and SEEING          |  turn speed, heading tolerance,
                |                              |  servo settle time, scan angles
                +------------------------------+
   Steps 3-5    |  SENSORS and MOTORS          |  servo aim, compass check,
                |                              |  motor stall points
                +------------------------------+
   Steps 1-2    |  POWER and MECHANICS         |  battery, 5 V rail, everything
                |                              |  bolted down
                +------------------------------+
```

Five rules make this work:

1. **Bottom up.** Finish each step before starting the next. The order is chosen so nothing you
    tune later can undo something you tuned earlier — except the few cases marked **Ripple effects**.
2. **One change at a time.** Change one number, test, write the result down. Change two at once
    and you can't tell which one helped.
3. **Repeat each test three times.** One good run can be luck. Three good runs is a result.
4. **Write everything down.** Your tuning log is your memory. When something breaks tomorrow, it
    tells you what worked today.
5. **Know when to stop.** Each step has a **Done when** line. When you hit it, move on.

Here's how the knobs map onto the rover's stop-look-go loop:

```text
   +--> DRIVE forward at the knob speed (starts at DRIVE_SPEED, capped by MAX_THROTTLE)
   |       |
   |       |  every 0.05 s, check:
   |       |    bump switch / IR sensor (IR trimmer) --> reverse for BACKOFF_S --+
   |       |    distance < STOP_DISTANCE_CM ---------------------------------+  |
   |       |    SCAN_INTERVAL seconds passed ------------------------------+ |  |
   |       v                                                               | |  |
   |    STOP  <----------------------------------------------------------+-+--+
   |       |
   |    SCAN: for each angle in SCAN_ANGLES, move servo (min_pulse/max_pulse),
   |          wait SETTLE_TIME, read distance --> pick the most open angle
   |       |
   |    TURN: target = heading + (angle - CENTER_ANGLE)     (uses MAG_OFFSET)
   |          spin at TURN_SPEED until within HEADING_TOLERANCE_DEG,
   |          or give up after TURN_TIMEOUT_S
   |       |
   +-------+
```


### 8.4 What improvement to expect

Tuning makes the rover *reliable at what it already does*; it doesn't make it smarter. It's still a
reactive, insect-brained robot (see [What Is the Random Rover?][42]).

| Behavior | Untuned (typical) | Well tuned (target) |
| :------- | :---------------- | :------------------ |
| Compass turns | Overshoot and wiggle, sometimes `turn timed out` | Land within about ±5° of target, one clean stop, no timeouts |
| Heading on the website | Off by tens of degrees, creeps | Follows a hand turn by about +90 per quarter turn; holds within a few degrees for a minute |
| Stopping for a box in its path | Sometimes touches it | Stops with a visible gap, every time, at your chosen speed |
| Bump switch contacts in a 5-minute run | Several | 0 to 2 |
| Times you have to rescue it in 5 minutes | Several | 0 to 1 |

What tuning **won't** fix — these are limits of the hardware and design, not your numbers:

* **Thin, soft, or angled things.** The HC-SR04 hears echoes. Thin chair legs, fabric, and walls
    hit at a steep angle can bounce sound away, so the sensor doesn't see them. The IR sensor and bump
    switch are the backups for exactly this.
* **Drop-offs.** Nothing on the rover looks *down*. It will drive off a table edge or down a stair.
    Always test on the floor.
* **Dead ends.** If every direction is blocked, the rover picks the "least blocked" one, drives a
    few centimeters, stops again, and repeats. That's the design.
* **Magnetic trouble spots.** Steel desks, radiators, and rebar in the floor bend Earth's field.
    Turns may land off target near them no matter how well you calibrated.
* **The browser pause.** With the website open, each page refresh can freeze the drive loop for
    about 0.25 s (see the **Why?** box in [The Code][25]). You'll test with the page closed *and*
    open so your numbers work either way.
* **Magnetic jumps from motor current.** Current flowing through the motors makes its own magnetic
    field. Calibration can only remove fields that are always there, so a small heading jump when the
    motors start is normal.
* **Battery fade.** A 9V battery weakens as it drains. Closed-loop compass turns shrug this off, but
    straight-line speed and stopping distance slowly change.


### 8.5 How to use this procedure

Start at Step 0 and go in order. Each step has the same layout:

* **Parameters** — what you're setting, and how much it matters
* **Time** — a realistic estimate
* **Why** — what's going on, in plain words
* **Do this** — the numbered actions
* **Done when** — the exact test that tells you the step is finished
* **Ripple effects** — what else this step can change, and when to come back

**Total time: about 4 to 4.5 hours**, more than one sitting. A good split:

| Session | Steps | Time |
| :------ | :---- | :--- |
| Session A | 0 – 5 (power, mounting, servo, compass, motors) | about 1.75 hours |
| Session B | 6 – 11 (turning, seeing, behavior, safety nets, preferences, final test) | about 2 to 2.5 hours |

If you have to stop partway, stop *between* steps and write down which step you finished.

**Editing numbers.** Unless a step says otherwise, you change a number by opening the file on
`CIRCUITPY` in Mu or Thonny, editing it, and saving. Saving any file restarts the rover program.

**Booting "still and flat" on the floor.** Several steps say *boot it still and flat* on the floor.
With the USB cable unplugged: set the rover down, switch the battery on, hands off for 3 seconds.
With USB still plugged in (so you can read the console), switching the battery off and on does
**not** restart the Pico — the laptop keeps it powered. Instead, set the rover down, click in the
serial console, press Ctrl-C then Ctrl-D, and keep hands off for 3 seconds.

**Warning labels used below:**

> **⚠ DANGER TO HARDWARE** — getting this wrong can permanently damage a part.
>
> **⚠ CAUTION** — the rover can move unexpectedly, fall, or hit something.


### Step 0 — Get ready: tools, test space, tuning log

**Parameters:** none yet. **Time:** 15 minutes.

**Tools you'll need:**

| Tool | Used in steps | Why |
| :--- | :------------ | :-- |
| Multimeter (DC volts) | 1 | Check the battery and the 5 V rail |
| Small screwdriver | 1, 9 | Buck converter trimpot (if it has one), IR sensor trimmer |
| Fresh 9V battery, plus one spare | 1, all | Motor strength changes as the battery drains |
| Masking tape and a pen | 3, 5, 8 | Mark start lines, distances, and a paper protractor |
| Tape measure or meter stick | 5, 7, 8, 9 | Measure stopping gaps, run distances, reverse distance |
| Protractor, or a printed paper one | 3 | Check servo angles |
| Phone with a compass app | 4 | Check the rover's heading |
| Phone stopwatch/timer | 6, 11 | Time turns and the final 5-minute run |
| Rover stand — a cup, box, or block that lifts the wheels off the table | 1, 2, 3, 4 | Run code on the bench without the rover driving away |
| 4-6 cardboard boxes (shoebox size or bigger) | 7, 8, 11 | Obstacles the ultrasonic sensor can see well |
| Laptop with Mu or Thonny, USB cable, and this repo (`full_build` folder) | all | Edit code, read the serial console, run `deploy.py` |
| Laptop or phone with a browser | 4, 8 | The rover status website, `http://192.168.4.1:5000` |
| Your tuning log ([`src/tuning-log-template.md`][33], printed or copied) | all | Your memory |

**Do this:**

1. **Back up your working code.** Copy all seven `.py` files on `CIRCUITPY` (`code.py`,
    `rover_server.py`, `motor_driver.py`, `wheel_odometry.py`, `history_chart.py`, `speed_knob.py`,
    `tft_status.py`) plus `settings.toml` to a folder on your laptop named `rover-before-tuning`. If
    tuning goes wrong, you can always go back.
2. **Set up a test space** on the floor, at least 2 m × 2 m, away from table edges, stairs, and big
    steel furniture. Use a wall or a row of boxes as a boundary.
3. **Start your tuning log.** One row every time you change a number. For example:

    | Step | Parameter | Old value | New value | Test | Result (3 runs) | Keep? |
    | :--- | :-------- | :-------- | :-------- | :--- | :-------------- | :---- |
    | 6 | `TURN_SPEED` | 0.45 | 0.40 | `[150]` turn test | +3, +4, +2 | yes |

4. **Learn the three safety habits** you'll use all day:
    * > **⚠ CAUTION** — saving *any* file on `CIRCUITPY` restarts the program *immediately*. With the
      > rover code on the board and the rover on the table, it will drive off the edge. **Put the
      > rover on its stand before you save any file or run `deploy.py`.**
    * The battery switch is your emergency stop for the motors. Know where it is. With USB plugged
        in, the Pico and servo stay powered from the laptop — unplug USB too to stop everything.
    * **Leave the speed knob alone during tuning** unless a step tells you to turn it. The knob
        overrides `DRIVE_SPEED` live, so a stray click changes the speed you're testing at. Every
        reboot puts it back to `DRIVE_SPEED`.

**Done when:** your code is backed up, your log is ready, you have your tools, and the test space is
clear.


### Step 1 — Power: a strong battery and a correct 5 V rail

**Parameters:** 9V battery charge (**Critical**), buck converter output (**Critical**).
**Time:** 10 minutes.

**Why.** Everything above this step depends on steady power. A motor draws a big burst of current
when it starts, and a tired battery sags under that burst. The sag travels through the buck
converter to the Pico, which can *brown out* (reset) every time the motors start. A weak battery also
makes motors weak and changes how far the rover coasts. You can't tune around bad power.

**Do this:**

1. With the battery clip unplugged, set the multimeter to DC volts and measure the 9V battery.
    Write it in your log. A fresh alkaline 9V reads about 9 V or a little more. If it reads under
    about 8 V, use a fresh one for tuning.
2. Plug the battery back in, USB cable unplugged. Put the rover on its stand and switch it on.
3. Measure between the Pico's `VSYS` pin and `GND` (the buck converter's output). It should read
    close to 5 V — roughly 4.8 V to 5.2 V.
4. Now watch the meter while the motors run (the rover code runs the wheels in the air on the
    stand). The reading should stay above about 4.7 V. If it dips hard, or the Pico resets when the
    motors start, swap the battery. If a fresh battery still dips, check that the 1000 µF capacitor
    is firmly across `VM`/`GND` at the DRV8833, stripe to GND — it's a small reservoir that covers
    the motors' start-up burst ([Class 3][35]).

> **⚠ DANGER TO HARDWARE** — the Pico's `VSYS` input is rated for **5.5 V at most** (see the
> [Pico 2 W datasheet][36]). The servo and HC-SR04 share that same 5 V rail, so too much voltage can
> damage all three at once. If your buck converter reads **above 5.5 V**, switch off right away and
> don't reconnect the Pico until it's fixed. If your buck converter has an adjustment screw (a
> trimpot), **disconnect its output from the Pico before turning it**, set it to 5.0 V with the
> meter, then reconnect. Turning a trimpot while the Pico is attached can spike the voltage and
> destroy the board.

**Done when:** battery reads about 9 V at rest, `VSYS` reads 4.8-5.2 V at rest and stays above about
4.7 V with the motors spinning, and the Pico doesn't reset when motors start.

**Ripple effects:** every motor-related number you tune later (Steps 5, 6, 8, 9) is tuned *on this
battery*. When you swap batteries, re-run the quick checks in Step 11.


### Step 2 — Mechanics: bolt everything down, count your slots

**Parameters:** part mounting (**Critical**), `SLOTS_PER_REV` (**Useful**). **Time:** 20 minutes.

**Why.** Calibration measures where things *are*. If a part moves after you calibrate it, the
calibration is wrong. So first, put every part in its final position and make it stay there.

**Do this:**

1. **IMU:** mounted where it will live for good, as far from the motors and battery as the chassis
    allows, firmly stuck down. Press on it — it must not shift.
2. **Battery:** in its final spot, held down. (The battery counts as "magnetic junk" for the
    compass. If it moves, the compass calibration goes stale.)
3. **Ultrasonic sensor on the servo:** the sensor is firm on the servo horn, and the horn is firm on
    the servo shaft.
4. **Bump switch:** the lever sticks out past the front of the chassis, so any contact presses it.
    Press it with a finger: it should click.
5. **IR sensor:** fixed, facing forward, low on the chassis, tilted slightly up so it doesn't see
    the floor.
6. **Wires:** nothing dangles near a wheel. Nothing is loose on the breadboard. Blu Tack holds the
    breadboard, DRV8833, buck converter, and battery firmly.
7. **Wheels:** spin each wheel by hand. It should turn freely without rubbing, and each encoder disc
    should pass through its optocoupler's slot without touching it.
8. **Count your encoder slots.** Count the slots (the gaps, not the teeth) around one wheel's encoder
    disc. If it isn't `20`, change `SLOTS_PER_REV` in `wheel_odometry.py` to your count (rover on its
    stand before you save). This only affects the wheel speed on the website and history chart — each
    slot that passes the optocoupler is one "tick," and the code turns ticks per second into cm/s
    using the slot count and the wheel's size ([Class 3][35]). To check your count, **switch the battery off and
    leave USB plugged in** — the code keeps running and the website keeps answering, but the motors
    have no power, so it's safe to handle the wheels. (If a wheel creeps or hums anyway, your buck
    converter is leaking USB power back to the motors: temporarily set `DRIVE_SPEED = 0` and
    `TURN_SPEED = 0` in `code.py`, as in Step 7, and put them back afterward.)
    Open the website and watch `speed_left_cms`. Untouched, it should read `0`. Now turn the left
    wheel by hand at a steady one turn per second (count "one-Mississippi" per turn): it should read
    about **21** cm/s, since a 67 mm wheel travels about 21 cm per turn. The reading moves in steps
    of about 4 cm/s, so hopping between about 17 and 25 is normal. Around 10 or 40 means your slot
    count is off by a factor of two. Repeat for the right wheel with `speed_right_cms`. If a number
    is far outside that range, or ticks while the wheel is still, see the wheel-speed rows in the
    [Class 3 troubleshooting guide][47].
9. **Quick function check** with the rover code running on the stand: press the bump switch and see
    `SAFETY: bump switch contact`; wave a hand in front of the IR sensor and see
    `SAFETY: IR sensor near-field obstacle`.

**Done when:** you can pick up the rover and gently shake it, and nothing moves, rattles, or comes
loose; both safety sensors fire when triggered by hand; and `SLOTS_PER_REV` matches your disc.

**Ripple effects:** if you ever remount the IMU, move the battery, or add steel near the IMU, go
back to Step 4 and recalibrate the compass. If you reseat the servo horn, redo Step 3.


### Step 3 — Servo aim: make "90" mean straight ahead

**Parameters:** `CENTER_ANGLE` (**Important**), `min_pulse` / `max_pulse` (**Important**).
**Time:** 20 minutes.

**Why.** When the scan picks angle `150`, the rover turns `150 - 90 = 60` degrees right. That math
assumes the servo *really* points 60° right when told `150`. If the servo is off by 10°, every turn is
off by 10° — and no amount of compass tuning fixes it, because the compass is carefully steering
toward the wrong target.

Why might it be off? A servo doesn't understand degrees. The Pico sends it a pulse every 20 ms, and
the pulse's *width* sets the angle: about 500 microseconds for one end, about 2500 for the other.
`min_pulse` and `max_pulse` tell the code which widths *your* servo uses for 0° and 180°. Every SG90
is a little different, and the horn can sit one tooth off on the shaft ([Class 2][40]).

```text
   What the scan angles mean (top view, rover facing up the page):

                          90  (straight ahead)
                  60      |      120
                    \     |     /
            30  ---  \    |    /  ---  150
                      \   |   /
                       [ROVER]

   rover turn = angle - CENTER_ANGLE:   30 -> -60 (left)   150 -> +60 (right)
```

**Do this:**

1. Put the rover on its stand. Tape a paper protractor (or draw lines at 30°, 90°, and 150°) under
    or behind the sensor, with 90° pointing straight along the rover's nose.
2. Run `uv run deploy.py tool servo_check`. It swaps your rover `code.py` out and runs
    [`servo_check.py`][43] as `code.py`. It points the servo at 90, 30, 90, 150 for 3 seconds each,
    printing `servo at ...`, and repeats.
3. **Check center first.** When it prints `servo at 90`, does the sensor point straight along the
    nose? If it's off by more than about 5°, the best fix is mechanical: pull the horn off the shaft
    and push it back on one tooth over, so 90 lands as close to straight as possible. Only if you
    can't get it close that way, note the angle that *does* look straight (for example `95`): you'll
    set `CENTER_ANGLE` in `code.py` to it, and shift every value in `SCAN_ANGLES` by the same amount.
    For the rest of this step, change `CHECK_ANGLES` in the running tool (`code.py` on `CIRCUITPY`)
    to `CENTER_ANGLE` and `CENTER_ANGLE` ± 60 (for example `[95, 35, 95, 155]`).
4. **Check the span.** At `30` and `150` (or `CENTER_ANGLE` ± 60), the sensor should point about 60°
    to each side of straight ahead. If both sides fall short (for example, only 50° each way), widen
    the pulse range a little: in the running tool, `MIN_PULSE` down by 50 and `MAX_PULSE` up by 50.
    If both sides go too far, narrow it the same way. Change them in steps of 50 and save after each
    change — the tool restarts with the new values.
5. Write your final `MIN_PULSE` and `MAX_PULSE` (and `CENTER_ANGLE`, if you changed it) in your log.
    Run `uv run deploy.py restore` to put the rover back, then, **rover on its stand**, edit `code.py`
    on `CIRCUITPY`: copy them into the `servo.Servo(pwm, min_pulse=..., max_pulse=...)` line, and set
    `CENTER_ANGLE` and `SCAN_ANGLES` if needed.

> **⚠ DANGER TO HARDWARE** — if the servo **buzzes, grinds, or strains** at any angle, it's being
> pushed past its physical stop. **Unplug the USB cable *and* switch off the battery** right away,
> then narrow the pulse range. Switching off the battery alone isn't enough: with USB plugged in, the
> laptop keeps powering the 5V rail — and the servo on it. A servo left straining will overheat and
> strip its plastic gears. This is why the test only visits 30 to 150,
> the range the rover actually uses.

**Done when:** at `CENTER_ANGLE` (normally `90`) the sensor points straight ahead within about 5°,
at `CENTER_ANGLE` ± 60 (normally `30` and `150`) it points about 60° left and right within about 5°,
and the servo is silent (no buzzing) at every stop.

**Ripple effects:** if you later change `SCAN_ANGLES` to include angles outside 30-150 (Step 7),
re-check the aim at those new angles.


### Step 4 — Compass: confirm the calibration and check the heading

**Parameters:** `MAG_OFFSET` (**Critical**), `MAG_AXIS_SIGN` (**Critical**), boot still and flat
(**Critical** habit). **Time:** 25 minutes.

**Why.** The compass steers every turn. If it's wrong, turns are wrong, and nothing you tune later can
make up for it. You calibrated it in [Build It][46], step 8. If *anything* moved in Step 2 —
the IMU, the battery, a motor, a steel screw — that calibration is stale. (Why the rover's own
magnets matter is in the **Why? Your rover is a magnet** box there, and in the
[IMU and Mahony filter explainer][37].)

**Do this:**

1. **Recalibrate if anything moved since Build It step 8** (or if you're not sure): take the fully
    assembled rover to a spot away from steel and repeat that step exactly —
    `uv run deploy.py tool mag_calibration`, tumble for 30 s, check equal spans, do the axis check,
    paste `MAG_OFFSET` (and `MAG_AXIS_SIGN`, if you flipped one) into `rover_server.py` on `CIRCUITPY`
    *and* in `full_build/src/pico/rover_server.py` on your laptop, then `uv run deploy.py restore`.
    If nothing moved, skip to item 2.
2. **Boot the rover sitting still and flat on the stand.** With USB still plugged in from item 1,
    switching the battery on doesn't restart the Pico: set it down, click in the serial console, press
    Ctrl-C then Ctrl-D, and keep hands off for 3 seconds (see 8.5, and the **Why? "Boot still and
    flat"** box in [The Code][25]).
3. **Heading check**, with the rover website open (`http://192.168.4.1:5000`, laptop on the rover's
    WiFi):
    * turn the rover clockwise by hand about a quarter turn → `heading` goes **up** by about 90
    * leave it still for a minute → `heading` holds within a few degrees
    * phone compass next to it → roughly matches (within 10-20° is fine; if your IMU is mounted
        sideways it may be off by a fixed 90° or so, which is also fine — turns only use *changes*
        in heading)

    If `heading` goes **down** on a clockwise turn, or disagrees with the phone and creeps back after
    a hand turn, `MAG_AXIS_SIGN` is wrong: redo the axis check in item 1.
4. **Motor-interference check.** Still on the stand, watch `heading` as the wheels start spinning.
    A jump of a few degrees that settles back is normal: current through the motor wires makes its
    own magnetic field, which calibration can't remove because it's only there while the motors run.
    A jump of more than about 15-20° means the IMU is too close to the motors — move it farther away
    (higher, on a standoff) and **restart this step from item 1**, recalibrating.

**Done when:** spans are roughly equal, all three axis checks pass, a clockwise quarter turn raises
`heading` by about 90, `heading` holds steady for a minute, and motor start-up moves it by less
than about 15°.

**Ripple effects:** this calibration is only good while *nothing magnetic moves* relative to the
IMU. Moving the IMU, the battery, or the motors — or adding a steel screw or bracket near the IMU —
means redoing this step. Changing code or speed does **not** require recalibrating.


### Step 5 — Motors: find the stall points and measure your real speed

**Parameters:** `MAX_THROTTLE` (**Critical**), and measurements you'll use later: the
straight-drive stall point, the spin stall point, and your speed in cm/s. **Time:** 20 minutes.

**Why.** A "throttle" of 0.5 does *not* mean half speed. The Pico switches the motor on and off very
fast (PWM), and 0.5 means "on half the time." But a motor needs a minimum push just to overcome
friction and start turning — below that, it hums and sits still. That minimum is the **stall
point**. Spinning in place takes *more* push than driving straight, especially on carpet, because
the wheels scrub sideways. You need both numbers before you can pick `TURN_SPEED` and `DRIVE_SPEED`
([Class 3][35]).

There's also a hidden cap. `motor_driver.py` clamps **every** motor command to `MAX_THROTTLE = 0.6`.
So `DRIVE_SPEED = 0.6` is already at the ceiling: setting `DRIVE_SPEED = 0.8` does *nothing* unless
you also raise `MAX_THROTTLE`. The speed knob tops out at `MAX_THROTTLE` for the same reason.

> **⚠ DANGER TO HARDWARE** — `MAX_THROTTLE` is there to protect the small TT gearbox motors, which
> are running from a 9V battery. **Leave it at `0.6` for tuning.** If you ever raise it, go up in
> steps of 0.05, and after a 1-minute run touch the motor cans: warm is fine, too hot to hold a
> finger on is not — lower it again. Too much current can also trip the DRV8833's overcurrent
> protection, which shuts off *both* motors until you switch the battery off, wait
> about 5 seconds, and switch it on again.

**Do this:**

1. Mark a start line on the floor with masking tape, with at least 2 m of clear floor ahead.
2. Rover on its stand, run `uv run deploy.py tool motor_check`. It runs [`motor_check.py`][44] as
    `code.py`, using your unchanged `motor_driver.py`. When it prints
    `Set the rover on the floor -- starting in 5 s`, move it to the floor. (If it starts before
    you're ready, put it back on the stand, click in the serial console, and press Ctrl-C to stop
    it, then Ctrl-D to start it again.) It runs short bursts at throttle 0.20, 0.25, … 0.60 driving straight, then the same spinning
    in place, then two 2-second speed runs at 0.5 and 0.6 — it tells you when to put the rover on
    the start line.
3. Keep the USB cable plugged in and follow along, carrying the laptop or letting the cable trail.
    Watch the rover and the console together.
4. Write down:
    * **Straight stall point** — the lowest throttle where the rover actually rolls forward
    * **Spin stall point** — the lowest throttle where it actually spins in place (on the floor you
        will test on — carpet needs more than tile)
    * **Speed** at 0.5 and 0.6 — distance traveled in cm ÷ 2 s = cm/s. For example, 70 cm in 2 s is
        35 cm/s.
5. Put the rover on its stand and run `uv run deploy.py restore`.

**Done when:** your log has a straight stall point, a spin stall point, and a cm/s speed for 0.5
and 0.6, all measured on your test floor — and `MAX_THROTTLE` is still `0.6`.

**Ripple effects:** these numbers change with the battery and with the floor surface. If you move
from tile to carpet, redo this step and Step 6.


### Step 6 — Turning: clean, accurate compass turns

**Parameters:** `TURN_SPEED` (**Critical**), `HEADING_TOLERANCE_DEG` (**Important**),
`TURN_TIMEOUT_S` (**Useful** — a safety limit). **Time:** 30 minutes.

**Why.** Turns are where most untuned rovers look bad. A compass turn spins toward the target and
checks the heading every 20 ms (see **Why? Closed-loop turns** in [The Code][25]). Too little spin
and the wheels can't move the rover; too much and it flies past the target before the next check,
then has to spin back.

```text
   TURN_SPEED too low          TURN_SPEED about right        TURN_SPEED too high
   --------------------        ----------------------        -------------------
   wheels hum, rover barely    one smooth spin, stops        spins past, reverses,
   moves -> "turn timed out"   within +/-5 of target         spins past again ->
                                                             wiggles, sometimes times out
```

**Do this:**

1. **Set a starting point.** Rover on its stand, edit `code.py`: `TURN_SPEED` = your spin stall
    point from Step 5, plus about `0.1` (for example, stall at `0.35` → start at `0.45`). Keep
    `HEADING_TOLERANCE_DEG = 5`.
2. **Set up the turn test.** In `code.py`, temporarily set `SCAN_ANGLES = [150]`, so every scan
    picks "60° right." Also temporarily set `SCAN_INTERVAL = 1.0` so the rover turns often, and set
    `DRIVE_SPEED = 0.5` — a gentler, provisional value you'll finalize in Step 8. Write the old
    values in your log. Set the rover on the floor, boot it still and flat, and watch the console for
    `drive: turning 60 deg to heading ...` followed by `drive: heading now ...`.

    > **⚠ CAUTION** — stopping distance isn't tuned yet (that's Step 8). Run this in the middle of
    > your open test space, walk alongside, and be ready to pick the rover up or switch it off.
3. For five turns, write down how far `heading now` is from the target (for example, target 260,
    heading now 263 → +3).
4. **Adjust one number at a time** (rover on its stand before every save):

    | What you see | Change |
    | :----------- | :----- |
    | `turn timed out`, and the wheels barely move | Raise `TURN_SPEED` by 0.05 |
    | Overshoots, wiggles back and forth before stopping | Lower `TURN_SPEED` by 0.05 |
    | Stops smoothly but misses by 6-8° | Lower `TURN_SPEED` by 0.05 (it's coasting past) |
    | Can't find a `TURN_SPEED` that both moves and stops cleanly | Raise `HEADING_TOLERANCE_DEG` to 8 |
    | `turn timed out` while the rover spins the *wrong way* forever | Not a tuning problem — see below |

    **Spinning the wrong way forever** means the motors and the compass disagree about which way is
    clockwise. Turn the rover clockwise by hand with the website open: `heading` must go **up**. If
    it goes down, fix `MAG_AXIS_SIGN` (Step 4). If it goes up, your motor wiring spins the rover the
    opposite way the code expects: in `code.py`'s `turn_toward()`, swap the two `motor_driver.drive()`
    lines so the "spin right" line becomes the "spin left" line and the other way around
    ([Class 5][34]).
5. When `[150]` passes, repeat with `SCAN_ANGLES = [30]` (60° left). Left and right can behave
    differently if one motor is stronger.
6. **Set `TURN_TIMEOUT_S`.** Time a few 60° turns with the stopwatch. `TURN_TIMEOUT_S` should be
    about three times your slowest turn, and no less than 2 s. The default `3.0` is fine if your
    turns take a second or less.
7. Put `SCAN_ANGLES` and `SCAN_INTERVAL` back to their normal values. Leave `DRIVE_SPEED` at `0.5`
    for now.

**Rules for these knobs:**

* Keep `TURN_SPEED` **above** your spin stall point, or turns will time out on hard floors and
    always fail on carpet.
* Keep `HEADING_TOLERANCE_DEG` **between 3 and 10**. The code also uses it to decide "no turn
    needed," so it must stay well below the smallest turn your scan angles ask for — the gap between
    `CENTER_ANGLE` and its nearest neighbor in `SCAN_ANGLES` (30 with the defaults, 20 if you pick
    `[30, 50, 70, 90, ...]` in Step 7) — or the rover will start ignoring small turns.

> **⚠ CAUTION** — don't make `TURN_TIMEOUT_S` huge (like 30 s) to "fix" timeouts. The timeout is
> what stops the motors when a wheel is jammed against something. A stuck motor draws its highest
> current, heats up, and can trip the DRV8833's shutdown. Fix the cause (usually `TURN_SPEED`)
> instead.

**Done when:** five turns right and five turns left each land within ±5° of target (or within your
`HEADING_TOLERANCE_DEG`), with at most one small back-and-forth correction, and no `turn timed out`.
**The rover should now:** spin crisply toward a new direction and stop there, like it means it.

**Ripple effects:** `TURN_SPEED` is independent of `DRIVE_SPEED` and the knob — changing drive
speed later doesn't touch your turns. But a new floor surface, or a much weaker battery, can push the
spin stall point up; if timeouts come back, redo this step.


### Step 7 — Seeing: trustworthy scans

**Parameters:** `SETTLE_TIME` (**Important**), `SCAN_ANGLES` (**Useful** / **Taste**).
**Time:** 20 minutes.

**Why.** A scan is only as good as each reading. The HC-SR04 measures distance by timing an echo —
if the servo is still swinging, the echo comes back from somewhere else. `SETTLE_TIME` is the pause
that lets the servo stop wobbling before the reading. Too short and readings are random. Too long and
each scan is slow. With 5 angles, `SETTLE_TIME = 0.15` makes a scan take about 0.75 s ([Class 2][40]).

**Do this:**

1. **Make the rover scan without moving.** Rover on its stand, set these in `code.py` (write the old
    values in your log so you can put them back):

    ```python
    DRIVE_SPEED = 0       # TEMPORARY (Step 7) -- no driving, no reversing
    TURN_SPEED = 0        # TEMPORARY (Step 7) -- no turning
    SCAN_INTERVAL = 1.0   # TEMPORARY (Step 7) -- scan often
    ```

    Now the rover sits still on the floor and scans over and over, so you can put boxes around it.
    Most cycles end with `drive: turn timed out` after `TURN_TIMEOUT_S` — **that's expected** here,
    because the wheels have zero speed and the heading never changes. (When the scan picks straight
    ahead, you'll see `drive: no turn needed` instead.) Just read the `scan:` lines.

    > **⚠ CAUTION** — **don't touch the speed knob in this step.** The knob starts at
    > `DRIVE_SPEED = 0`, but a single click jumps it up to `MIN_SPEED` (`0.3`) and the rover drives
    > off. If that happens, switch off and reboot. And don't hold a rover with spinning wheels to keep
    > it still — zero speeds are the safe way. Double-check both are `0` before you save.

2. **Check the sensor itself.** Put a cardboard box squarely in front at 50 cm, measured with the
    tape measure. Watch the `scan: angle 90 distance_cm ...` lines: they should read about 50 (within
    a couple of cm). Try 25 cm and 100 cm too. The HC-SR04 is good from about 2 cm to a few meters,
    and doesn't need calibrating — this just confirms it's healthy.
3. **Check the scan picks correctly.** Put boxes 30 cm away at every direction *except* one (say,
    the `120` direction). Five scans in a row should print `scan: chosen angle 120`. Move the gap to
    another angle and repeat.
4. **Tune `SETTLE_TIME`.** Lower it by `0.05` at a time and repeat item 3. When readings start
    coming back `None`, or the chosen angle becomes wrong or random, go back *up* by `0.05` from that
    point and keep that value. Don't go below about `0.1` for the SG90.
5. **Choose your `SCAN_ANGLES` (taste).** The default five angles are a good balance. Options:
    * **More angles** — for example `[30, 50, 70, 90, 110, 130, 150]` — finer choices, slower scans.
    * **Fewer angles** — for example `[45, 90, 135]` — faster, but coarser turns.

    Keep these rules: include `CENTER_ANGLE` (straight ahead); keep the list symmetric around
    `CENTER_ANGLE`; stay inside the range you checked in Step 3; and keep the list ordered left to
    right.
6. **Restore** `DRIVE_SPEED`, `TURN_SPEED`, and `SCAN_INTERVAL` from your log. Put the rover on its
    stand before you save — with real speeds back, it drives off the moment `code.py` saves.

**Done when:** the ultrasonic reads within about 2 cm of your tape measure at 25, 50, and 100 cm,
and the scan chooses the one open gap correctly five times in a row, at every gap position you
tried. **The rover should now:** reliably look toward open space, not random directions.

**Ripple effects:** if you add angles outside 30-150, recheck servo aim (Step 3) at those angles.
More angles or a longer `SETTLE_TIME` make every stop longer, which you'll feel in Step 8.


### Step 8 — Behavior: speed, stopping distance, and how often to look

**Parameters:** `DRIVE_SPEED` (**Important** / **Taste**), `STOP_DISTANCE_CM` (**Critical**),
`SCAN_INTERVAL` (**Taste**), status page and chart refresh (**Useful** / **Important**).
**Time:** 30 minutes.

**Why.** This is the step that decides whether the rover hits things. The knobs are linked by simple
math:

* **Stopping gap.** The rover checks distance about every 0.05 s, but it's moving the whole time,
    and it coasts a little after the motors stop. So it always stops a bit *closer* than
    `STOP_DISTANCE_CM`. Faster means a bigger overshoot. With the website open, a page refresh can
    add up to 0.25 s of blind driving — at 35 cm/s, that's about 9 cm more.
* **Distance between routine scans** = speed × `SCAN_INTERVAL`. At 35 cm/s and 3 s, that's about
    1 m of driving between looks.
* **The knob can go faster than `DRIVE_SPEED`.** Your stop distance has to be safe at the *fastest*
    speed the knob can reach (Step 10), not just the speed you boot at.

```text
   Stopping-distance test (side view):

   start line                                            box
   |                                                      |
   [ROVER] ------------->     ...stops here -->  [ROVER]  |
   |<-------------- about 1.5 m ------------->|<- gap ->|
                                                     ^
                             want: gap of at least ~8-10 cm, bumper never touches
```

**Do this:**

1. **Pick a `DRIVE_SPEED`.** Choose between your straight stall point + `0.1` and `0.6` (the
    `MAX_THROTTLE` ceiling). Slower is more reliable — more time to react, and smaller compass jumps
    from motor current. For first tuning runs, `0.5` is a good, safe choice. You can come back and
    speed up once everything else works.
2. **Stopping test.** Temporarily set `SCAN_INTERVAL = 30.0` so the rover doesn't stop to scan on
    its own. Close the website tab. Aim the rover straight at a cardboard box from about 1.5 m away,
    boot it still and flat, and let it drive. When it stops (you'll see
    `drive: obstacle close, distance_cm ...`), measure the gap from its front bumper to the box.
    Three runs; write down the smallest gap.
3. **Slow the website down first.** Every website request freezes the drive loop for about 0.25 s.
    The history chart asks for data every 0.2 s — so with the chart open, the rover is blind *most of
    the time*, and no stop distance can fix that. In `history_chart.py`, change
    `setTimeout(pollHistory, 200)` to `setTimeout(pollHistory, 1000)` (or higher). Also consider
    slowing the status page itself: the `500` in `rover_server.py`'s `setInterval(..., 500)` can
    become `1000`. (Rover on its stand before you save.)
4. Repeat item 2 **with the website open** on your laptop (it shows the history chart), three more
    runs.
5. **Adjust `STOP_DISTANCE_CM`:**
    * If the gap is fine with the browser closed but too small *only* with the page open, slow the
        page refresh further (item 3) before touching `STOP_DISTANCE_CM`.
    * If the smallest gap (either test) is under about 8 cm, or the bump switch ever fired, raise
        `STOP_DISTANCE_CM` by 5 and retest.
    * If the smallest gap is more than about 25 cm, you can lower it by 5 — the rover will squeeze
        through narrower spaces.
    * Keep it between about **20 and 40 cm**. Below 20, the rover can't stop in time at normal
        speed. Above 40, it stops at everything and struggles in hallways and near furniture.
6. **Set `SCAN_INTERVAL` (taste).** Put it back to a normal value. Shorter (2 s) = cautious, looks
    often, moves in short hops. Longer (5 s) = confident, longer straight runs. Any value from about
    2 to 6 s is fine because the stop-distance check protects the rover between scans. A good
    starting rule: speed × `SCAN_INTERVAL` of about 1 m.

> **⚠ CAUTION** — the rover only looks *forward*. Nothing on it sees a table edge or a stair. Run
> every test on the floor.

**Done when:** in six stopping runs (three with the browser closed, three open), the rover stops
with at least about 8 cm of gap every time and the bump switch never fires. **The rover should
now:** drive, see a box ahead, stop short of it, scan, turn away, and carry on — without touching
it.

**Ripple effects:**

* **Changing `DRIVE_SPEED` — or turning the knob faster than you tested — means redoing this step's
    stopping test.** Overshoot grows with speed.
* The drive speed is also the **reverse** speed after a safety stop, so changing it changes how far
    the rover backs up (Step 9).
* `STOP_DISTANCE_CM` sets how close the IR sensor should trigger (Step 9).


### Step 9 — Safety nets: IR range and back-off distance

**Parameters:** IR sensor trimmer (**Important**), `BACKOFF_S` (**Important**). **Time:** 20
minutes.

**Why.** The IR sensor and bump switch catch what the ultrasonic sweep misses — chair legs, soft
things, objects that appear between checks. When either fires, the rover stops, reverses for
`BACKOFF_S` seconds at the current drive speed, then scans. The IR sensor shines invisible light and
watches for it to bounce back; a tiny screw (the trimmer) sets how strong the bounce must be to count
as "something's there." It should be a *backup*, triggering closer than `STOP_DISTANCE_CM` — not a
second, jumpy main sensor.

```text
   distance from the front of the rover:

   0 cm       ~10 cm                     STOP_DISTANCE_CM (e.g. 25)
   |-- bump --|-- IR sensor zone --|------ ultrasonic stops here ------>
     (contact)   (backup, close)          (main, farther out)
```

**Do this:**

1. **IR range.** With the rover on its stand and its code running, slowly move a piece of white paper
    toward the IR sensor and note where it triggers (the module's LED lights, and
    `SAFETY: IR sensor near-field obstacle` prints). Turn the trimmer screw with the small
    screwdriver until it triggers at about **8-12 cm** — clearly less than your `STOP_DISTANCE_CM`.
    On most modules, counter-clockwise shortens the range; check yours ([Pre-Class IR sensor
    homework][39]).
2. Repeat with a dark object. Dark things reflect less IR, so they trigger closer. That's normal —
    just make sure it still triggers at all.
3. **Floor check.** Let the rover drive around the test space for a minute with nothing in front of
    it. If it emergency-stops with nothing nearby, the IR sensor is seeing the floor (shiny floors
    are the worst): turn the trimmer down, or tilt the sensor up a little.
4. **Back-off distance.** Back-off distance ≈ your speed from Step 5 × `BACKOFF_S`. At 35 cm/s and
    0.3 s, that's about 10 cm. Press the bump switch by hand while the rover drives, and measure how
    far it reverses. Aim for about **5-15 cm**: enough to clear the obstacle for a turn, not so much
    that it hits something behind it. Adjust `BACKOFF_S` in steps of 0.1.

> **⚠ CAUTION** — the rover has **no rear sensor**. It reverses blind. Keep `BACKOFF_S` short (0.5 s
> or less is a good rule), or it will back into walls and furniture.

**Done when:** the IR sensor triggers at roughly 8-12 cm for a white target, still triggers for a
dark target, never fires on an open floor, and the rover reverses 5-15 cm after a bump.
**The rover should now:** almost never touch anything, and when it does, back off cleanly and find a
new way.

**Ripple effects:** changing `DRIVE_SPEED` (or driving faster with the knob) changes the back-off
distance — recheck item 4. Changing `STOP_DISTANCE_CM` may mean resetting the IR range to stay below
it.


### Step 10 — Preferences: make it yours (optional)

**Parameters:** **Taste**, plus a few firm limits. **Time:** 15-30 minutes, only if you want to.

Chosen within the limits below, these have little effect on how well the rover avoids obstacles.
(The website and chart refresh rates *do* affect safety, which is why they were set back in Step 8.)

* **`DRIVE_SPEED`, `SCAN_INTERVAL`, `SCAN_ANGLES`** — the rover's "personality": cautious and
    twitchy, or bold and sweeping. Remember the ripple effects in Steps 7-9 if you change them.
* **Speed knob (`speed_knob.py`): `MIN_SPEED`, `MAX_SPEED`, `SPEED_STEP`.** Two firm limits, not
    taste. First, keep `MIN_SPEED` **above your straight stall point** from Step 5, or the rover
    stalls and hums at the bottom of the knob. Second, the knob already stops at `MAX_THROTTLE`
    (`0.6`), even though `MAX_SPEED` says `0.9`; raising `MAX_SPEED` does nothing unless you also
    raise `MAX_THROTTLE` (see the Step 5 warning).

    Then retest at the knob's top speed. Turning the knob up won't work for this, because every
    reboot resets the knob to `DRIVE_SPEED`, and each Step 8 run starts with a reboot. Instead,
    temporarily set `DRIVE_SPEED = 0.6` (the knob's top — `MAX_THROTTLE`), rerun the Step 8 stopping
    test and Step 9 back-off check, adjust `STOP_DISTANCE_CM` and `BACKOFF_S` if needed, then put
    `DRIVE_SPEED` back. At top
    speed, also watch `heading` on the website as the motors start: more motor current means a
    bigger magnetic jump, and if turns start landing off target, set `MAX_SPEED` *below*
    `MAX_THROTTLE` (for example `0.5`-`0.55`) — lowering it from `0.9` to `0.8` changes nothing, since
    the knob already stops at `0.6` ([Class 6][38]).
    If you'd rather not retest, just don't turn the knob past the speed you tested in Step 8.
* **Website and chart refresh** — already handled in Step 8, item 3. If you change them again,
    remember: faster refresh = more blind time for the rover, so redo the Step 8 page-open stopping
    test.
* **TFT `REFRESH_S` (`tft_status.py`)** — `0.2` is smooth; don't go much lower, since redrawing the
    screen is slow and the rover isn't watching for obstacles while it draws.

**Done when:** you like how it looks and feels — and if you changed `DRIVE_SPEED` or use the knob
above it, you've redone the Step 8 stopping test and the Step 9 back-off check at the fastest speed
you'll use.


### Step 11 — Final exam: the 5-minute arena run

**Parameters:** none — this confirms everything together. **Time:** 15 minutes, plus a 5-minute
recheck after every battery swap.

**Do this:**

1. Build an arena: a 2 m × 2 m space bounded by walls or boxes, with 3-4 cardboard boxes as
    obstacles inside.
2. Boot the rover still and flat in the middle. Start the stopwatch.
3. For 5 minutes, keep a tally on paper:

    | Event | Tally | Target for a tuned rover |
    | :---- | :---- | :----------------------- |
    | Bump-switch contacts (rover touched something) | | 0-2 |
    | Rescues (you had to pick it up or free it) | | 0-1 |
    | Turns that clearly missed their direction | | 0-1 |
    | Stuck in a corner for more than 30 s | | 0 |

4. If you missed a target, find the matching symptom in [8.7 Tuning troubleshooting][45] and revisit
    only that step.
5. **Save your tuned numbers in two places.** Copy `code.py`, `rover_server.py`, `motor_driver.py`,
    `wheel_odometry.py`, `history_chart.py`, `speed_knob.py`, and `tft_status.py` from `CIRCUITPY`
    to a laptop folder named `rover-tuned`. Then copy your changed values into the matching files in
    `full_build/src/pico/` too, so a later `uv run deploy.py rover --overwrite` doesn't put the
    starting guesses back.

**Done when:** the rover completes a 5-minute arena run meeting all four targets. **The rover is
tuned.** It should drive with purpose, stop short of obstacles, look, turn crisply to open space,
and keep going for minutes at a time without you.


### 8.6 When do I have to re-tune?

| Something changed | Redo |
| :---------------- | :--- |
| New battery | Step 1, then a 5-minute Step 11 run |
| New floor (tile ↔ carpet) | Steps 5, 6, 8 |
| IMU, battery, or motors moved; steel added near the IMU | Step 4 (recalibrate), then Step 11 |
| Servo horn reseated, or sensor bumped | Step 3, then Step 7 |
| `DRIVE_SPEED` changed, or you drive faster with the knob than you tested | Step 8 stopping test, Step 9 back-off |
| `TURN_SPEED` or `HEADING_TOLERANCE_DEG` changed | Step 6 turn test |
| Ran `deploy.py rover --overwrite` | Check your tuned values are still in the files on `CIRCUITPY` |
| Only code logic changed, no constants | Nothing — but run Step 11 to be sure |


### 8.7 Tuning troubleshooting

| Symptom | Likely cause | Go back to |
| :------ | :----------- | :--------- |
| Turns miss, wiggle, or print `turn timed out` | `TURN_SPEED` too high or too low, or `HEADING_TOLERANCE_DEG` too tight | Step 6 (and Step 4 if `heading` looks wrong on the website) |
| Rover spins the wrong way until `turn timed out` | Motor direction and compass disagree about clockwise | Step 6, item 4 |
| Turns go the wrong direction by a fixed amount every time | Servo aim off | Step 3 |
| `heading` disagrees with the phone compass from boot, and creeps back after a hand turn | `MAG_AXIS_SIGN` wrong | Step 4, axis check |
| `heading` was fine, now wrong by the same amount everywhere | IMU, battery, or motors moved after calibration | Step 4, recalibrate |
| `heading` a few degrees off at boot, slowly correcting for a minute | Booted on a tilt | Reboot still and flat (turns still work meanwhile — they use heading *changes*) |
| `heading` jumps more than about 15-20° when the motors start | Motor current's magnetic field, which calibration can't remove | Step 4, item 4 (move the IMU farther away) |
| `heading` wrong only near certain furniture or spots | Steel bending Earth's field | Test somewhere else — a real-world limit |
| Hits boxes head-on | Stop distance too small for your speed or page refresh | Step 8 |
| Hits boxes at an angle, or thin/soft things | Ultrasonic can't see them | Step 9 (IR range), or accept it as a sensor limit |
| Backs into things | `BACKOFF_S` too long | Step 9 |
| Stops constantly with nothing near | IR sensor seeing the floor, or `STOP_DISTANCE_CM` too big | Step 9 (IR floor check), then Step 8 |
| Drives but never stops to scan | `SCAN_INTERVAL` left at a test value, or `STOP_DISTANCE_CM` too small | Step 8 |
| Always chooses angle 90, whatever is around it | Every scan reading is `None`, so it falls back to `CENTER_ANGLE` | Check the HC-SR04 wiring (divider on `ECHO`, `VCC` on the 5V rail), then Step 7 |
| Console floods with `None` distances during a scan | `SETTLE_TIME` too short, or the sensor aims at something out of range | Step 7 |
| Reacts late to the bump switch or IR only while the website is open | The 0.25 s website pause | Step 8, item 3 (slow the refresh), or close the tab |
| Rover jerks or stalls at the low end of the knob | `MIN_SPEED` below your straight stall point | Step 10 |
| At top knob speed, `heading` jumps and turns land off target | More motor current, bigger magnetic jump | Step 10 (set `MAX_SPEED` below `MAX_THROTTLE`, e.g. `0.5`) |
| Both motors suddenly dead mid-run | DRV8833 overcurrent shutdown (jammed wheel) | Free the wheel, switch the battery off, wait about 5 s, switch it on; check `TURN_TIMEOUT_S` isn't huge (Step 6) |
| Everything got worse after a while | Battery fading | Step 1 |


## 9. Checklist

* [ ] Breadboard planned: Pico + DRV8833 at one end, buck converter at the other
* [ ] Top `+` rail labeled 5V, bottom `+` rail labeled 3.3V, both `-` rails jumpered as GND
* [ ] Chassis assembled; motor and switch leads soldered
* [ ] All parts mounted in their final places (IMU far from motors and battery)
* [ ] Buck converter set to 5.0 V *before* connecting it to the 5V rail
* [ ] Power wiring done; 9V only to buck `IN+` and DRV8833 `VM`; common GND everywhere
* [ ] Power-on check: 5V rail 4.8-5.2 V, 3.3V rail 3.2-3.4 V
* [ ] Signal wiring done per the [wiring table][26]; `SLP` on 3.3V; divider on `ECHO`; TFT `RST` on `GP22`
* [ ] Laptop set up: `setup-test-laptop.sh` / `.ps1` ([setup-test-laptop.sh][31], [setup-test-laptop.ps1][32])
* [ ] Software installed: `uv run deploy.py rover` ([deploy.py][20])
* [ ] `settings.toml` edited with your own network name and password ([settings.toml][17])
* [ ] Rover boots and logs `drive:` / `scan:` lines on its stand
* [ ] Compass calibrated: `uv run deploy.py tool mag_calibration`, equal spans, axis check passed, `MAG_OFFSET` pasted into `rover_server.py`, `uv run deploy.py restore` ([mag_calibration.py][24])
* [ ] Part-by-part test passed: `uv run deploy.py test`, then `restore` ([device_test.py][22])
* [ ] Whole-rover test passed: `uv run test/system_test.py` ([system_test.py][23])
* [ ] Orientation viewer follows the rover: `uv run src/laptop/wireframe.py` ([wireframe.py][21])
* [ ] First floor run: drive, stop, scan, turn, repeat
* [ ] Tuning Session A done (Steps 0-5): power, mounting + `SLOTS_PER_REV`, servo aim, compass, motor stall points
* [ ] Tuning Session B done (Steps 6-11): turns, scans, stopping distance, IR + back-off, preferences, 5-minute arena run
* [ ] Tuned files backed up to your laptop (`rover-tuned` folder) and copied into `full_build/src/pico/`


[01]:../lesson_scripts/README.md
[02]:../explainers/strategy-for-tuning-calibration-random-rover.md
[03]:https://pico2w.pinout.xyz/
[04]:https://learn.adafruit.com/adafruit-drv8833-dc-stepper-motor-driver-breakout-board/pinouts
[05]:https://learn.adafruit.com/adafruit-lsm9ds1-accelerometer-plus-gyro-plus-magnetometer-9-dof-breakout/pinouts
[06]:https://howtomechatronics.com/tutorials/arduino/ultrasonic-sensor-hc-sr04/
[07]:https://www.hackster.io/chip-pk/sg90-servo-motor-interfacing-with-arduino-complete-beginner-849eef
[08]:https://www.handsontec.com/dataspecs/sensor/Slot%20IR%20Detector.pdf
[09]:https://learn.adafruit.com/adafruit-1-14-240x135-color-newxie-tft-display/circuitpython
[10]:src/pico/code.py
[11]:src/pico/rover_server.py
[12]:src/pico/motor_driver.py
[13]:src/pico/wheel_odometry.py
[14]:src/pico/history_chart.py
[15]:src/pico/speed_knob.py
[16]:src/pico/tft_status.py
[17]:src/pico/settings.toml
[18]:src/pico/requirements.txt
[19]:src/tools/
[20]:deploy.py
[21]:src/laptop/wireframe.py
[22]:test/device_test.py
[23]:test/system_test.py
[24]:src/tools/mag_calibration.py
[25]:#5-the-code
[26]:#4-wiring
[27]:#7-test-the-build
[28]:#8-tune-the-rover
[29]:https://www.elecrow.com/blog/everything-you-should-know-about-micro-switch.html
[30]:https://docs.sunfounder.com/projects/umsk/en/latest/01_components_basic/08-component_ir_obstacle.html
[31]:setup-test-laptop.sh
[32]:setup-test-laptop.ps1
[33]:src/tuning-log-template.md
[34]:../lesson_scripts/class-05-lesson-script.md
[35]:../lesson_scripts/class-03-lesson-script.md
[36]:https://datasheets.raspberrypi.com/picow/pico-2-w-datasheet.pdf
[37]:../explainers/what-is-an-imu-and-mahony-filter.md
[38]:../lesson_scripts/class-06-lesson-script.md
[39]:../lesson_scripts/class-00-lesson-script.md
[40]:../lesson_scripts/class-02-lesson-script.md
[41]:../lesson_scripts/class-04-lesson-script.md
[42]:../explainers/what-is-the-random-rover.md
[43]:src/tools/servo_check.py
[44]:src/tools/motor_check.py
[45]:#87-tuning-troubleshooting
[46]:#6-build-it
[47]:../lesson_scripts/class-03-lesson-script.md#10-troubleshooting-guide
[48]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/blob/main/explainers/strategy-for-tuning-calibration-random-rover.md
