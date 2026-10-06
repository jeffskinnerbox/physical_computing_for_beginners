# Full Build Script: The Random Rover, Start to Finish

* **Covers:** Classes 1-6 in one build session, including every Class 6 stretch goal
* **Time:** about 3-4 hours to build and test, plus about 4 hours to tune
* **Before You Start:** your laptop is set up from the Pre-Class: CircuitPython **10.x** on the Pico
    2 W (9 or later is required for the TFT's `fourwire` module), Mu or Thonny, and `uv`. You've
    taken the course, or have the [lesson scripts][01] open for background — this script tells you
    *what* to do, not *why*.

---


## 1. What This Document Is For

This is the shortcut. The lesson scripts build the Random Rover one phase at a time over six
classes, rewiring nothing and explaining everything along the way. This script builds the *finished*
rover — the Class 5 stop-look-go robot plus all three Class 6 stretch goals (encoder speed knob,
website history chart, on-board TFT screen) — in one pass, with the narrative stripped out.

Use it to rebuild your rover after the course, to build a second one, or to recover from a rover
that's been taken apart. It ends with a test that checks every part, then hands you to the
[tuning guide][02] to make it drive *well*.

The code here is the lesson-script code, unchanged, with one exception: Class 6 left the speed knob
and TFT screen as standalone demos, so this build adds a small amount of glue to run them *inside*
the rover (see [The Code][25]). Every tuning value starts at the same placeholder value the
Class 5 and Class 6 lesson scripts use.


## 2. Plan the Breadboard First

Lay out the 830-point breadboard before you place a single wire. Getting power right up front
prevents most of the hard-to-find bugs later.

```text
+5V  rail (top +)       ===========================================================
GND  rail (top -)       ===========================================================
                                           [ TFT ] [ Rotary Encoder ]
USB end of the board -> [ Pico 2W ][ DRV8833 ]                   [ Buck Converter ] <- far end
                                             [ 1K & 2K Resisters ]
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
    9V.

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
| 9V battery + clip | 1 | Class 3 |
| Slot-type IR optocoupler (wheel speed) | 2 | Class 3 |
| 1000 µF electrolytic capacitor | 1 | Class 3 |
| Adafruit LSM9DS1 9-DOF IMU + STEMMA QT-to-male-header cable | 1 | Class 4 |
| * Micro limit switch (bump switch) | 1 | Class 5 |
| * IR obstacle avoidance sensor | 1 | Class 5 Pre-Class homework) |
| * Adafruit 1.14" 240x135 ST7789 TFT display | 1 | Class 6 (Pre-Class homework) |
| Long male and short female Dupont leads (to solder to the motors and switch) | 2 + 2 | Class 3 |
| Blu Tack, soldering iron, multimeter, small screwdriver | — | Class 3 |
| USB cable, laptop | 1 | Pre-Class |
| Rover stand (a cup or box that lifts the wheels off the table) | 1 | Class 3 |
| * Phone with a compass app | 1 | Class 5 |

>**NOTE:** Items with "*" **were not** part of the Class 4 build and need to be added now.


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
| * KY-040 encoder `CLK` / `DT` | `GP3` / `GP4` | Class 1 | |
| * KY-040 encoder `CLK` | `GP3` | Class 1 | |
| * KY-040 encoder `DT` | `GP4` | Class 1 | |
| * KY-040 encoder `+` / `GND` | 3.3V rail / GND rail | Class 1 | **changed** — Class 1 used 5V; see pitfall below |
| * KY-040 encoder `SW` | not connected | Class 1 | |
| * HC-SR04 `TRIG` | `GP6` | Class 2 | |
| * HC-SR04 `ECHO` | 1 kΩ → `GP7`, with 2 kΩ from `GP7` to GND <br>**See NOTE / Diagram below** | Class 2 | **NOTE:** See note below, divider on `ECHO`, never `TRIG` |
| * HC-SR04 `VCC` / `GND` | 5V rail / GND rail | Class 2 | `VSYS` rail, not `VBUS` (moved in Class 5) |
| * SG90 servo (orange) | `GP8` | Class 2 | |
| * SG90 servo `+` (red) / `GND` (brown) | 5V rail / GND rail | Class 2 | `VSYS` rail, not `VBUS` (moved in Class 5) |
| DRV8833 `AIN1` / `AIN2` | `GP9` / `GP10` | Class 3 | Motor A (left) |
| DRV8833 `BIN1` / `BIN2` | `GP11` / `GP12` | Class 3 | Motor B (right) |
| DRV8833 `SLP` (`nSLEEP`) | 3.3V rail | Class 3 | must be HIGH or the motors never move |
| DRV8833 `GND` | GND rail | Class 3 | common ground |
| DRV8833 `AOUT1`/`AOUT2` | Motor A leads | Class 3 | Motor A (left) |
| DRV8833 `BOUT1`/`BOUT2` | Motor B leads | Class 3 | Motor B (right) |
| 1000 µF capacitor `+` / `−` | DRV8833 `VM` / GND | Class 3 | stripe side to GND |
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
| * TFT `BL` or `RST` | `GP22` | Class 6 | |
| * TFT `DC` | `GP21`| Class 6 | |
| * TFT `CS` | `GP20` | Class 6 | |
| * TFT `DA` or `MO` or `MOSI` |`GP27` | Class 6 | second SPI bus — `GP19` is taken |
| * TFT `CL` or `SCK` | `GP26` | Class 6 | second SPI bus — `GP19` is taken |
| * TFT `GND` | GND rail | Class 6 | |
| * TFT `V+` or `VIN` | 3.3V rail | Class 6 | |

>**NOTE:** Items with "*" **were not** part of the Class 4 build and need to be added now.

**Pitfalls to check before power-on:**

* **The encoder runs on 3.3V here.** The KY-040 has its own pull-up resistors to its `+` pin, so on
    5V it puts 5V on `GP3`/`GP4`. It works just as well on 3.3V, and that keeps every signal at the
    Pico's own logic level.
* **5V parts on the 5V rail, everything else on 3.3V.** Only the HC-SR04 and the servo (and the
    Pico's `VSYS`) use 5V. A 3.3V-only part on the 5V rail can damage it *and* the Pico pin it talks to.
* **`VBUS` is not a power source for the rover.** It's only live with USB plugged in. If anything is on
    `VBUS`, the rover goes blind the moment you unplug the cable.
* **Mount everything before you calibrate.** The IMU, battery, and motors must be in their final
    places — the compass calibration measures *this* arrangement. Blu Tack holds the breadboard,
    DRV8833, buck converter, and battery to the chassis.

**Power-on check** (USB unplugged, wheels off the table on a stand): switch on, then measure the 5V
rail (4.8-5.2 V) and the 3.3V rail (3.2-3.4 V) with a multimeter. (The Pico 2 W has no power LED —
the meter is your check.) If either rail is wrong, switch off and recheck the table before going further.

>**NOTE:** Double-check the voltage-divider resistors sit on the `ECHO` line, not `TRIG` — this is
>the single easiest wiring mistake to make this class, and the least forgiving one, since it
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
| `servo_check.py`, `motor_check.py` | Pico (as `code.py`, temporarily) | [Tuning guide][02] Steps 3 and 5 | Servo-aim and motor stall-point checks |
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

**`rover_server.py` — the IMU filter and website.** Unchanged from Class 5. Importing it starts the
rover's WiFi network, calibrates the gyro for about 2 seconds, and reads the compass once — so
**always boot the rover still and flat**. Your compass calibration goes in its `MAG_OFFSET` line.
[rover_server.py][11]

**`motor_driver.py` and `wheel_odometry.py`** — unchanged from Class 3. [motor_driver.py][12],
[wheel_odometry.py][13]

**`history_chart.py` — Stretch 2.** Unchanged from Class 6. It adds a "Recent History" canvas chart
(roll, pitch, heading, left wheel speed) to the existing status page. [history_chart.py][14]

**`speed_knob.py` — Stretch 1.** Class 6's knob pattern (`MIN_SPEED`, `MAX_SPEED`, `SPEED_STEP`),
with two changes. It counts clicks with `rotaryio`, which counts in hardware in the background, so
no click is lost while the rover is scanning or answering the website. And the top of the knob is
capped at `motor_driver.MAX_THROTTLE`, since speeds above it do nothing. Turning clockwise should
speed it up, one `SPEED_STEP` per click — the device test checks both, and the file's comments say
what to change if yours runs backwards or needs two clicks per step. [speed_knob.py][15]

**`tft_status.py` — Stretch 3.** Class 6's ST7789 setup, now showing the rover's *real* distance,
heading, and speed instead of demo values. It redraws at most every `REFRESH_S` seconds.
[tft_status.py][16]

**`settings.toml`** — a template with a placeholder network name and password. Change both to your
own (the password needs at least 8 characters). [settings.toml][17]

**`requirements.txt`** — the library list `deploy.py` hands to `circup`. [requirements.txt][18]

**Calibration tools.** `mag_calibration.py` is Class 5's compass calibration: tumble the rover for 30
seconds, copy the printed `MAG_OFFSET` line into `rover_server.py`. `servo_check.py` and
`motor_check.py` are the tuning guide's servo-aim and motor-stall tests. [tools folder][19]

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

    Do this if your OS is Linux or macOS (MacBook) — in Terminal on a Mac:

    ```bash
    # Linux or macOS (Shell)
    curl -LsSf https://raw.githubusercontent.com/jeffskinnerbox/physical_computing_for_beginners/main/full_build/setup-test-laptop.sh | bash
    ```

    Do this if your OS is Windows:

    ```powershell
    # Windows 11 (PowerShell)
    powershell -ExecutionPolicy ByPass -c "irm https://raw.githubusercontent.com/jeffskinnerbox/physical_computing_for_beginners/main/full_build/setup-test-laptop.ps1 | iex"
    ```

    On a Mac without Apple's Command Line Tools (which provide `git`), the script opens their
    installer and stops — finish that install, then run the command again.

    After that, rerun `full_build/setup-test-laptop.sh` (or `.ps1`) in your copy to pull updates.
    Every command below runs from `~/physical_computing_for_beginners/full_build`.
1. **Install Rover software (Pico 2W)** — while your laptop is still on a normal, internet-connected network.
    Plug in USB, put the rover on its stand (wheels off the table), and from the `full_build` folder
    run `uv run deploy.py rover`. On a first install it pauses after copying `settings.toml`: edit it
    on `CIRCUITPY` (your own network name and password), save, then press Enter.

    > **⚠ CAUTION** — the moment `code.py` is saved, the rover starts driving. **Keep it on its stand
    > whenever you deploy or save a file.** The battery switch is your emergency stop.
1. **Watch it boot.** Open the serial console in Mu or Thonny. With the rover still and flat you
    should see the WiFi lines, `Calibrating gyro -- keep the rover perfectly still...`,
    `HTTP Server running at http://192.168.4.1:5000`, then `Full build -- Random Rover starting...`
    and the `drive:` and `scan:` lines as it runs in the air. The TFT shows `dist`, `head`, and `speed`.
1. **Calibrate the compass** (Class 5, Phase 1). Run `uv run deploy.py tool mag_calibration`, then,
    away from steel furniture, tumble the fully assembled rover through every orientation for 30
    seconds when it says `GO`. Check the three spans are roughly equal, and do the axis check with a
    phone compass (`mx` positive with the X arrow north, `my` positive with Y north, `mz` negative lying
    flat). If an axis check fails, flip that entry of `MAG_AXIS_SIGN` in the running tool (`code.py` on
    `CIRCUITPY`) *and* in `rover_server.py`, save, and let the tool rerun until all three pass. Copy
    the printed `MAG_OFFSET` line into `rover_server.py` on `CIRCUITPY`, then
    `uv run deploy.py restore`. Also paste it into `full_build/src/pico/rover_server.py` on your
    laptop, so a later `deploy.py rover --overwrite` keeps it.
1. **Test** — [Test the Build][27].
1. **Tune** — [Tune the Rover][28].

**Pitfalls during the build:**

* **Motors never move, but the console looks normal** → DRV8833 `SLP` isn't on the 3.3V rail.
* **Everything works on USB, nothing works on battery** → something's on `VBUS`, or the buck output
    doesn't reach `VSYS`.
* **The Pico resets when the motors start** → weak 9V battery; replace it, then add the capacitor.
* **`ImportError`** → run `uv run deploy.py rover` again (with internet) so `circup` fills `/lib`.
* **`RuntimeError: No pull up found on SDA or SCL`** (right after the WiFi lines) → the Pico can't
    see the IMU at all. Check IMU `VIN` is on the 3.3V rail, that rail is fed from `3V3(OUT)`, IMU
    `GND` is on the GND rail, `SDA`/`SCL` are on `GP0`/`GP1`, and the STEMMA QT plug is fully seated.
    `uv run deploy.py test` narrows it down.
* **`heading` wrong or creeping** → booted while moving or tilted, or the IMU moved after
    calibration. Reboot still and flat; recalibrate if anything moved.
* **A browser loads `http://192.168.4.1:5000`, but `wireframe.py` or `system_test.py` can't reach
    the rover** → on a Mac, macOS blocks programs started from Terminal from reaching local-network
    devices until you allow it, even though your browser already has permission. Open **System
    Settings → Privacy & Security → Local Network**, switch on **Terminal** (or the terminal app you
    use), then quit and reopen it. Check the `Last error:` line `wireframe.py` prints for other causes.
* **Blank TFT** → check `GP26`/`GP27`/`GP20`-`GP22` against the table.
* **Knob turns the speed the wrong way, or needs two clicks per step** → see the comments in
    `speed_knob.py` (swap `GP3`/`GP4` in the code, or add `divisor=2`).


## 7. Test the Build

Test before you tune. Both tests use the placeholder tuning values, and both keep working,
unchanged, after you tune.

1. **Part by part.** Rover on its stand, USB plugged in. Run `uv run deploy.py test` and follow the
    prompts in the serial console. Fix any failed part (re-run the test) before going on. Then
    `uv run deploy.py restore`.
2. **The whole rover.** Rover on its stand, USB plugged in, laptop joined to the rover's WiFi
    network. Close Mu/Thonny's serial console (only one program can use the port), then run
    `uv run test/system_test.py` and follow its prompts. (If it can't find the Pico, name the port:
    `COM5` on Windows, `/dev/ttyACM0` on Linux, `/dev/cu.usbmodem...` on macOS.)
3. **Look at it.** Run `uv run src/laptop/wireframe.py`, tilt and turn the rover by hand, and check
    that the box follows and that `heading` goes **up** about 90 for a clockwise quarter turn. Then
    open `http://192.168.4.1:5000` and check the history chart scrolls.
4. **First floor run.** Unplug USB, set the rover on the floor still and flat, switch it on, hands
    off for 3 seconds. It should drive, stop, sweep, turn, and drive on.


## 8. Tune the Rover

Your rover now works on placeholder numbers. Make it work *well* with the
[Strategy for Tuning and Calibrating the Random Rover][02] guide, from Step 0. Where the guide says
`class-5-code.py`, use `code.py` on `CIRCUITPY`; where it says `class-6-code-1.py`, use
`speed_knob.py`; where it says `class-6-code-2.py`, use `history_chart.py`; for `class-6-code-3.py`, use
`tft_status.py`. To run its test programs, use `uv run deploy.py tool servo_check` /
`motor_check` / `mag_calibration`, and `uv run deploy.py restore` afterward. In Step 0, back up all
seven `.py` files on `CIRCUITPY` plus `settings.toml`, not just the four the guide lists. Record
every change in a copy of the guide's tuning log, [`src/tuning-log-template.md`][33]. Two more
full-build notes:
the knob sets the drive speed live, so after Step 8 use it only within the range you tested; and
during Step 7 (`DRIVE_SPEED = 0`), don't touch the knob.


## 9. Checklist

* [ ] Breadboard planned: Pico + DRV8833 at one end, buck converter at the other
* [ ] Top `+` rail labeled 5V, bottom `+` rail labeled 3.3V, both `-` rails jumpered as GND
* [ ] Chassis assembled; motor and switch leads soldered
* [ ] All parts mounted in their final places (IMU far from motors and battery)
* [ ] Buck converter set to 5.0 V *before* connecting it to the 5V rail
* [ ] Power wiring done; 9V only to buck `IN+` and DRV8833 `VM`; common GND everywhere
* [ ] Power-on check: 5V rail 4.8-5.2 V, 3.3V rail 3.2-3.4 V
* [ ] Signal wiring done per the [wiring table][26]; `SLP` on 3.3V; divider on `ECHO`
* [ ] Laptop set up: `setup-test-laptop.sh` / `.ps1` ([setup-test-laptop.sh][31], [setup-test-laptop.ps1][32])
* [ ] Software installed: `uv run deploy.py rover` ([deploy.py][20])
* [ ] `settings.toml` edited with your own network name and password ([settings.toml][17])
* [ ] Rover boots and logs `drive:` / `scan:` lines on its stand
* [ ] Compass calibrated: `uv run deploy.py tool mag_calibration`, `MAG_OFFSET` pasted into `rover_server.py`, `uv run deploy.py restore` ([mag_calibration.py][24])
* [ ] Part-by-part test passed: `uv run deploy.py test`, then `restore` ([device_test.py][22])
* [ ] Whole-rover test passed: `uv run test/system_test.py` ([system_test.py][23])
* [ ] Orientation viewer follows the rover: `uv run src/laptop/wireframe.py` ([wireframe.py][21])
* [ ] First floor run: drive, stop, scan, turn, repeat
* [ ] Tuned with the [tuning guide][02], Steps 0-11
* [ ] Tuned files backed up to your laptop (`rover-tuned` folder)


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

