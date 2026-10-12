# Full Build Script: The Random Rover, Start to Finish

* **Covers:** Classes 1-6 in one build session, with all the Class 6 stretch goals and the full tuning procedure.
* **Time:** Approximately 3-4 hours to build and test. Approximately 4-4.5 hours to tune (two sessions).
* **Before you start:** Set up your laptop as the Pre-Class tells you:
  * CircuitPython **10.x** on the Pico 2 W. (The TFT `fourwire` module needs CircuitPython 9 or later.)
  * Mu or Thonny.
  * `uv`.
* **Earlier classes:** You do **not** have to do Classes 1-6 first. This script gives the reason (*why*) for each wiring rule and each tuning value. For the long version, read the [lesson scripts][01].
* **Reference document:** [Strategy for Tuning and Calibrating the Random Rover][48].

---


## 1. What This Document Is For
The lesson scripts build the Random Rover one phase at a time, in six classes, with full explanations.
This script builds the *finished* rover in one session.
The finished rover is the Class 5 stop-look-go robot with all three Class 6 stretch goals:

* An encoder knob that sets the speed.
* A history chart on the rover website.
* A TFT screen on the rover.

Use this script in these conditions:

* You want to go directly to the finished robot.
* You want to build your rover again after the course.
* You want to build a second rover.
* Somebody took your rover apart, and you must put it together again.

This script has three tasks, in this order:

1. **Build the rover** (Sections 2-6). Plan the breadboard, connect the wires, and install the code.
2. **Test the rover** (Section 7). Make sure each part operates correctly.
3. **Tune the rover** (Section 8). Replace the starting guesses in the code with numbers for *your* rover.
   Tuning changes a rover that "works" into a rover that works *well*.

You will see short boxes with the title **Why?** in this script.
Each box gives, in a few sentences, a reason that a lesson script teaches in a full phase.
Read these boxes. They help you repair the rover when a problem occurs.

The code in this script is the lesson-script code, with one exception.
In Class 6, the speed knob and the TFT screen are separate demo programs.
This build adds a small quantity of connection code ("glue") so that they run *inside* the rover program (see [The Code][25]).
Each tuning value starts at the same placeholder value that the Class 5 and Class 6 lesson scripts use.


## 2. Plan the Breadboard First
Plan the layout of the 830-point breadboard before you install the first wire.
Correct power wiring at the start prevents most of the problems that are difficult to find later.

> **Why? Three voltages, one ground.** The rover uses three voltages:
>
> * The motors get 9V directly from the battery. They need the power, and they make electrical noise that must stay away from the Pico.
> * The buck converter changes 9V into a clean 5V for the Pico, the servo, and the ultrasonic sensor. (A buck converter is a module that decreases a DC voltage.)
> * The Pico changes 5V into 3.3V for all the other parts.
>
> Each signal wire is measured as "volts above ground." For example, `GP9` tells the DRV8833 "go."
> If the battery ground and the Pico ground are not connected, the DRV8833 has no common zero for its measurement.
> Then the DRV8833 operates randomly, although each part has power.
> Thus, *each* `GND` connects to one common ground ([Class 3][35]).

This diagram shows where the three voltages go:

```text
 9V battery (+) --> on/off switch --+--> DRV8833 VM ---------> motors (9V)
                                    |
                                    +--> Buck Converter IN+
                                              |
                                         Buck Converter OUT+ = 5V Rail <----- Pico VSYS
                                                                 |
                                                                 v
                                                                 +--> servo +
                                                                 +--> HC-SR04 VCC

                                     Pico 3V3(OUT) = 3.3V Rail --> any other 3.3V parts

 One Common GND for 9V battery (-), buck IN-/OUT-, Pico GND, DRV8833 GND, all parts GND
```

This diagram shows the breadboard layout:

```text
+5V  rail (top +)       ===========================================================
GND  rail (top -)       ===========================================================
                                           [ TFT ] [ Rotary Encoder ]
USB end of the board -> [ Pico 2W ][ DRV8833 ]                   [ Buck Converter ] <- far end
                                             [ 1K & 2K Resistors ]
GND   rail (bottom -)   ===========================================================
+3.3V rail (bottom +)   ===========================================================
```

1. **Put the Pico and the DRV8833 together at one end.**
   Put the Pico 2 W at one end of the breadboard, with its USB port at the edge.
   Put the DRV8833 motor driver directly next to the Pico.
   Short signal wires (`GP9`-`GP12`) give reliable motor control.
2. **Put the buck converter at the other end.**
   The buck converter makes the most electrical noise and the most heat.
   Keep it away from the IMU and the Pico.
3. **Use one rail pair for 5V and the other rail pair for 3.3V.**
   The top `+` rail is **5V**. The buck converter `OUT+` supplies it, and it supplies the Pico `VSYS`.
   The bottom `+` rail is **3.3V**. The Pico `3V3` pin (label `3V3(OUT)`) supplies it.
   Put tape labels on the two rails.
   If you mix up the two rails, you can cause the most expensive damage in this build.
4. **Make each `-` rail GND, and connect all of them to one ground.**
   Connect a jumper wire from the top `-` rail to the bottom `-` rail.
   Connect these to the ground: the Pico `GND`, the DRV8833 `GND`, the buck converter `OUT−` and `IN−`, and the battery `−`.
   Connect the `GND` of each part to a `-` rail.
   If the common ground is missing, the rover works only "partially."
5. **Do not put 9V on a rail.**
   The battery `+` goes through the on/off switch on the chassis.
   After the switch, 9V goes to two places only: the buck converter `IN+` and the DRV8833 `VM`.
   No other part connects to 9V.
   To split the 9V, do these steps:
   1. Put the output wire of the switch into an empty breadboard row (a column of 5 holes).
      Do *not* use a `+`/`-` rail.
   2. Connect one jumper wire from that row to the buck converter `IN+`.
   3. Connect one jumper wire from that row to the DRV8833 `VM`.


> **⚠ CAUTION — HARDWARE DAMAGE:** Set the buck converter to 5.0 V with a multimeter **before** you connect its output to the 5V rail.
> The maximum rating of the Pico `VSYS` is 5.5 V. The servo and the HC-SR04 also use this rail.
> Do not turn the trimpot (the adjustment screw) of the buck converter while the Pico is connected.


## 3. What You Need

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
| 9V battery + clip, and one spare battery for tuning | 1 + 1 | Class 3 |
| Slot-type IR optocoupler (wheel speed) | 2 | Class 3 |
| * 1000 µF electrolytic capacitor, 16 V or higher | 1 | Class 3 (optional in Class 3, necessary here) |
| Adafruit LSM9DS1 9-DOF IMU + STEMMA QT-to-male-header cable | 1 | Class 4 |
| * Micro limit switch (bump switch) | 1 | Class 5 |
| * IR obstacle avoidance sensor | 1 | Class 5 (Pre-Class homework) |
| * Adafruit 1.14" 240x135 ST7789 TFT display | 1 | Class 6 (Pre-Class homework) |
| Long male Dupont leads (2 for each motor) and short female Dupont leads (for the switch) | 4 + 2 | Class 3 |
| Blu Tack, soldering iron, multimeter, small screwdriver | — | Class 3 |
| USB cable, laptop | 1 | Pre-Class |
| Rover stand (a cup or box that lifts the wheels off the table) | 1 | Class 3 |
| * Phone with a compass app | 1 | Class 5 |
| Tuning items: masking tape, tape measure, paper protractor, 4-6 cardboard boxes | — | Tuning (Section 8) |

>**NOTE:** If you start from nothing, you need all the items.
>If you build again from a Class 4 rover, the items with "*" are new or changed since Class 4:
>
>* New parts: the bump switch, the IR sensor, the TFT, and the capacitor (if you did not install it in Class 3).
>* Parts with new wiring: the HC-SR04, the servo, and the encoder. They are already on your breadboard (see the wiring table).


## 4. Wiring
Connect the wires in the order of the table: power first, then each device.
Say each row aloud while you connect it.

**Pinouts:** [Pico 2 W][03], [DRV8833][04], [LSM9DS1][05], [HC-SR04][06], [SG90][07], [IR optocoupler][08], [TFT display][09], [IR Obstacle Avoidance Sensor][30], [DAOKI Micro Limit Switch][29]

| Component | Connects to | First introduced | Notes |
| :-------- | :---------- | :---------------: | :---- |
| Battery `+` | chassis on/off switch | Class 3 | First, solder Dupont leads to the switch and the motors. |
| On/off switch output | buck `IN+` **and** DRV8833 `VM` | Class 3 | 9V. Do not connect to a breadboard rail. |
| Battery `−` | GND rail | Class 3 | Common ground. |
| Buck converter `IN−` | GND rail | Class 3 | |
| Buck converter `OUT+` | 5V rail **and** Pico `VSYS` | Class 3 | Set to 5.0 V *before* you connect it. |
| Buck converter `OUT−` | GND rail | Class 3 | |
| Pico `3V3(OUT)` | 3.3V rail | Class 3 | |
| Pico `GND` (two or more pins) | GND rail | Class 1 | |
| * KY-040 encoder `CLK` | `GP3` | Class 1 | |
| * KY-040 encoder `DT` | `GP4` | Class 1 | |
| * KY-040 encoder `+` / `GND` | 3.3V rail / GND rail | Class 1 | Same as Class 1. If an older build has it on 5V, move it. See the pitfall below. |
| * KY-040 encoder `SW` | not connected | Class 1 | The rover does not use the push button. |
| * HC-SR04 `TRIG` | `GP6` | Class 2 | |
| * HC-SR04 `ECHO` | 1 kΩ → `GP7`, with 2 kΩ from `GP7` to GND <br>**See the NOTE and diagram below** | Class 2 | Put the divider on `ECHO`. Do not put it on `TRIG`. |
| * HC-SR04 `VCC` / `GND` | 5V rail / GND rail | Class 2 | Use the `VSYS` rail, not `VBUS` (moved in Class 5). |
| * SG90 servo signal (orange) | `GP8` | Class 2 | |
| * SG90 servo `+` (red) / `GND` (brown) | 5V rail / GND rail | Class 2 | Use the `VSYS` rail, not `VBUS` (moved in Class 5). |
| DRV8833 `AIN1` / `AIN2` | `GP9` / `GP10` | Class 3 | Motor A (left). |
| DRV8833 `BIN1` / `BIN2` | `GP11` / `GP12` | Class 3 | Motor B (right). |
| DRV8833 `SLP` (`nSLEEP`) | 3.3V rail | Class 3 | Must be HIGH. If not, the motors do not move. |
| DRV8833 `GND` | GND rail | Class 3 | Common ground. |
| DRV8833 `AOUT1`/`AOUT2` | Motor A leads | Class 3 | Motor A (left). |
| DRV8833 `BOUT1`/`BOUT2` | Motor B leads | Class 3 | Motor B (right). |
| * 1000 µF capacitor `+` / `−` | DRV8833 `VM` / GND | Class 3 | Stripe side to GND. See the pitfall below. |
| Optocoupler A `DO` (Motor A wheel) | `GP19` | Class 3 | The fork goes around the encoder disc. |
| Optocoupler B `DO` (Motor B wheel) | `GP17` | Class 3 | |
| Both optocouplers `VCC` / `GND` | 3.3V rail / GND rail | Class 3 | |
| LSM9DS1 IMU `SDA` (blue) | `GP0` | Class 4 | If you swap these wires, no error shows. |
| LSM9DS1 IMU `SCL` (yellow) | `GP1` | Class 4 | If you swap these wires, no error shows. |
| LSM9DS1 IMU `VIN` (red) | 3.3V rail | Class 4 | Install far from the motors and the battery. |
| LSM9DS1 IMU `GND` (black) | GND rail | Class 4 | Install far from the motors and the battery. |
| * Limit switch `NO` / `COM` | `GP5` / GND rail | Class 5 | The lever is in front of the chassis. |
| * IR obstacle sensor `OUT` | `GP13` | Class 5 | |
| * IR obstacle sensor `VCC` / `GND` | 3.3V rail / GND rail | Class 5 | Low, pointed forward, tilted up a small angle. |
| * TFT `RST` | `GP22` | Class 6 | Reset. This is **not** the backlight pin. |
| * TFT `DC` | `GP21` | Class 6 | |
| * TFT `CS` | `GP20` | Class 6 | |
| * TFT `MOSI` (label can be `DA` or `MO`) | `GP27` | Class 6 | Second SPI bus, because `GP19` is in use. |
| * TFT `SCK` (label can be `CL`) | `GP26` | Class 6 | Second SPI bus, because `GP19` is in use. |
| * TFT `BL` / `Lite` (backlight) | not connected | Class 6 | On by default. On a generic board with the label `BLK`, connect it to the 3.3V rail if the screen stays dark. |
| * TFT `GND` | GND rail | Class 6 | |
| * TFT `V+` or `VIN` | 3.3V rail | Class 6 | |

>**NOTE:** The rows with "*" are new or changed since the Class 4 build.
>If you build again from a Class 4 rover, do these tasks:
>
>* **Add** the bump switch, the IR sensor, the TFT, and the capacitor (if you did not install it).
>* **Move** the HC-SR04 `VCC` and the servo `+` from `VBUS` to the 5V rail.
>* If an older build has the encoder `+` on 5V, move it to the 3.3V rail.
>* The rover does not use the encoder `SW` wire on `GP18`. You can remove it or keep it. It causes no problems.

**Pitfalls to check before you turn on the power:**

* **The encoder uses 3.3V in this build.**
  The KY-040 has its own pull-up resistors to its `+` pin. (A pull-up resistor keeps a signal HIGH when nothing pulls it LOW.)
  Thus, on 5V, the encoder puts 5V on `GP3`/`GP4`.
  The encoder works equally well on 3.3V, and then each signal stays at the logic level of the Pico.
* **Put 5V parts on the 5V rail, and all other parts on 3.3V.**
  Only the HC-SR04, the servo, and the Pico `VSYS` use 5V.
  A 3.3V part on the 5V rail can damage the part *and* the Pico pin that it connects to.
* **`VBUS` is not a power source for the rover.**
  `VBUS` has power only when the USB cable is connected.
  If a part uses `VBUS`, that part stops when you disconnect the cable.
* **The rover does not use the Class 1 push button and LEDs (`GP2`, `GP14`, `GP15`).**
  If they are on your breadboard from Class 1, you can keep them or remove them. They cause no problems.
  If you start from nothing, do not install them.
* **The 1000 µF capacitor is necessary in this build.**
  Class 3 tells you that it is optional.
  But this rover uses one 9V battery for the two motors, the servo, the Pico WiFi, and all the sensors.
  The capacitor is a small energy store across the motor supply.
  It supplies the large current that the motors need when they start, so that the Pico does not reset.

  Use a capacitor with a rating of 16 V or higher.
  Connect the `+` leg to `VM` and the `−` leg (with the stripe) to GND.

  > **WARNING:** Do not connect an electrolytic capacitor in the wrong direction. It can burst and cause injury.
* **Install all the parts before you calibrate.**
  The IMU, the battery, and the motors must be in their final positions, because the compass calibration measures *this* arrangement.
  Use Blu Tack to attach the breadboard, the DRV8833, the buck converter, and the battery to the chassis.

> **Why? The four rules that cause most rovers that work "partially."**
>
> 1. **The `ECHO` divider.** The HC-SR04 uses 5V, so its `ECHO` pin sends a 5V pulse.
>    A Pico pin is designed for 3.3V, and 5V slowly damages it.
>    The 1 kΩ / 2 kΩ resistor pair divides the 5V, so `GP7` gets 5 × 2/3 ≈ 3.3V.
>    `TRIG` does not need a divider. The Pico *sends* 3.3V to it, and the sensor accepts 3.3V ([Class 2][40]).
> 2. **`SLP` (`nSLEEP`) connected to HIGH.** The DRV8833 sleeps if this pin is not HIGH.
>    The Adafruit board has no resistor that holds this pin HIGH.
>    If you do not connect it, your code runs correctly and prints each line, but the motors do not move ([Class 3][35]).
> 3. **`VSYS`, not `VBUS`.** `VBUS` is the 5V from the USB cable.
>    It stops when you disconnect the laptop and the rover drives on battery power.
>    The buck converter supplies `VSYS`, so `VSYS` has power in both conditions ([Class 5][34]).
> 4. **The second SPI bus for the TFT.** The first SPI bus of the Pico needs `GP19`, but the left-wheel optocoupler uses `GP19`.
>    The second bus (`GP26`/`GP27`) prevents this conflict, and you do not have to move older wiring ([Class 6][38]).

**Power-on check** (USB cable disconnected, wheels off the table on a stand):

1. Turn on the switch.
2. Measure the 5V rail with a multimeter. The correct range is 4.8-5.2 V.
3. Measure the 3.3V rail. The correct range is 3.2-3.4 V.

The Pico 2 W has no power LED. The multimeter is your check.
If a rail voltage is not correct, turn off the switch. Then examine the table again before you continue.

>**NOTE:** Make sure the voltage-divider resistors are on the `ECHO` line, not on `TRIG`.
>This wiring mistake is the easiest to make in this build.
>It also causes the most damage, because the divider protects the GPIO pin of the Pico.
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
| `code.py` | Pico | **Full build**: `class-5-code.py` + Class 6 stretch glue | The stop-look-go rover, with the speed knob, the history chart, and the TFT screen inside it. |
| `rover_server.py` | Pico | Class 5 (no change) | 9-DOF Mahony filter, compass heading, and the rover status website at `http://192.168.4.1:5000`. |
| `motor_driver.py` | Pico | Class 3 (no change) | `drive(left, right)` and `stop()` for the DRV8833, with a limit of `MAX_THROTTLE`. |
| `wheel_odometry.py` | Pico | Class 3 (no change) | Wheel speed and direction for the website. |
| `history_chart.py` | Pico | Class 6, `class-6-code-2.py` (no change) | Adds the rolling-history chart to the website. |
| `speed_knob.py` | Pico | **Full build**: Class 6 Stretch 1 as a library | Changes encoder clicks into a live drive speed. |
| `tft_status.py` | Pico | **Full build**: Class 6 Stretch 3 as a library | Shows the real distance, heading, and speed on the TFT. |
| `settings.toml` | Pico | Class 3 | The WiFi network name and password of your rover. |
| CircuitPython libraries in `/lib` | Pico | Classes 1-6 | `adafruit_hcsr04`, `adafruit_motor`, `adafruit_debouncer`, `adafruit_ticks`, `adafruit_lsm9ds1`, `adafruit_httpserver`, `adafruit_st7789`, `adafruit_display_text` (+ the libraries that they need). |
| `mag_calibration.py` | Pico (as `code.py`, temporarily) | Class 5, `class-5-mag-calibration.py` | One-time compass calibration. |
| `servo_check.py`, `motor_check.py` | Pico (as `code.py`, temporarily) | [Tuning guide][02] Steps 3 and 5 | Servo-aim check and motor stall-point check (Section 8, Steps 3 and 5). |
| `setup-test-laptop.sh` / `.ps1` | Laptop | **Full build** | Gets (or updates) this code from GitHub, and downloads the packages for the laptop tools before you need them. |
| `deploy.py` | Laptop | **Full build** | Copies all the files to the Pico. |
| `wireframe.py` | Laptop | Class 4, changed into a test tool | A live 3D box that shows the orientation of the rover. It reads the data through WiFi. |
| `device_test.py` | Pico (as `code.py`, temporarily) | **Full build** | Interactive test of each part. |
| `system_test.py` | Laptop | **Full build** | Interactive test of the full rover, with the real rover code. |


### What each piece does
**`code.py` — the rover.**
This file has the Class 5 stop-look-go loop. The loop does these steps again and again:

1. Drive forward.
2. Stop when an object is nearer than `STOP_DISTANCE_CM` (or after each `SCAN_INTERVAL` seconds).
3. Move the sensor across the `SCAN_ANGLES` and measure the distances.
4. Use the compass to turn to the most open angle.

The bump switch and the IR sensor can cause a stop and a reverse at all times.
The Class 6 stretch goals connect to the loop at three points:

* The drive loop reads `speed_knob` in each cycle.
* The drive loop shows each distance on `tft_status`.
* `code.py` imports `history_chart` directly after `rover_server`.

`DRIVE_SPEED` is now the *starting* speed.
The knob changes the speed while the rover runs. This includes the reverse speed after a safety stop.
The log lines are the same as in Class 5, with three changes:

* The start-up line is `Full build -- Random Rover starting...`.
* Each `drive: forward, heading ...` line ends with `speed ...`.
* A `knob: current_speed ...` line prints each time that the knob moves.

While the rover scans or turns (for a maximum of approximately 4 s), it does not answer the website and does not update the TFT.
Both start again when the rover drives again.
[code.py][10]

> **Why? Closed-loop turns.** In Class 3, the rover turns with a simple method.
> It turns for a measured time, then stops, and does not check the result.
> This is an *open-loop* turn. The result changes when the battery becomes weak or the floor changes from tile to carpet.
>
> This rover uses *closed-loop* turns:
>
> 1. It selects a target compass heading.
> 2. It turns, and it checks the compass each 20 ms.
> 3. It stops when the heading is near the target (within a few degrees).
>
> If it turns too far, the error changes sign, and the rover turns back.
> Because the rover measures the result, it automatically corrects for a weak battery, a slippery floor, or a slow motor.
> There is one risk. If the rover never gets to the target heading (for example, a wheel is jammed), it can turn without end.
> Thus, each turn has a time limit, `TURN_TIMEOUT_S` ([Class 5][34]).

**`rover_server.py` — the IMU filter and the website.**
This file is the same as in Class 5.
When `code.py` imports it, it does these steps:

1. It starts the WiFi network of the rover.
2. It calibrates the gyroscope for approximately 2 seconds.
3. It reads the compass one time.

Thus, **always start the rover when it is still and flat**.
Your compass calibration goes in the `MAG_OFFSET` line of this file.
[rover_server.py][11]

> **Why? "Start still and flat."** A gyroscope measures rotation.
> When it does not move, it always shows a very small rotation. This error is its *bias*.
> If the code does not remove the bias, the heading moves a few degrees each minute.
>
> Thus, for the first 2 seconds after power-on, `rover_server.py` calculates the average of the gyroscope readings.
> After that, it subtracts this average from each reading.
> If the rover moves during these 2 seconds, the code measures the movement of your hand as "bias."
> Then the rover steers incorrectly for the full session.
>
> The code also reads the compass one time to set the starting heading. For this reading, the rover must be level.
> Make this a habit: *put the rover down, turn it on, and do not touch it for 3 seconds*.
> For more information, see [Class 4][41] and the [IMU and Mahony filter explainer][37].

**`motor_driver.py` and `wheel_odometry.py`** — these files are the same as in Class 3. [motor_driver.py][12], [wheel_odometry.py][13]

**`history_chart.py`** — this file is the same as in Class 6.
It adds a "Recent History" chart (roll, pitch, heading, left wheel speed) to the status page.
[history_chart.py][14]

**`speed_knob.py`** — this file uses the Class 6 knob method (`MIN_SPEED`, `MAX_SPEED`, `SPEED_STEP`), with two changes:

* It counts the clicks with `rotaryio`. The `rotaryio` hardware counts in the background, so the code does not lose a click while the rover scans or answers the website.
* The maximum knob speed is `motor_driver.MAX_THROTTLE`, because speeds above it have no effect.

A clockwise turn of the knob increases the speed by one `SPEED_STEP` for each click.
The device test checks the direction and the step size.
If your knob turns the wrong direction, or needs two clicks for each step, read the comments in the file.
At each start, the knob starts again from `DRIVE_SPEED`.
[speed_knob.py][15]

**`tft_status.py`** — this file uses the Class 6 ST7789 setup.
It shows the *real* distance, heading, and speed of the rover, not demo values.
It updates the screen one time in each `REFRESH_S` seconds, or less frequently.
[tft_status.py][16]

**`settings.toml`** — a template with a placeholder network name and password.
Change both to your own values. The password must have a minimum of 8 characters.
[settings.toml][17]

**`requirements.txt`** — the list of libraries that `deploy.py` gives to `circup`.
(`circup` is a tool that installs CircuitPython libraries.)
[requirements.txt][18]

**Calibration tools.**
`mag_calibration.py` is the Class 5 compass calibration.
Turn the rover in all directions for 30 seconds, then copy the `MAG_OFFSET` line that it prints into `rover_server.py`.
`servo_check.py` and `motor_check.py` are the servo-aim test and the motor-stall test for Section 8, Steps 3 and 5.
[tools folder][19]

**`setup-test-laptop.sh` / `setup-test-laptop.ps1` — laptop setup.**
Use the `.sh` file on Linux or on a MacBook (macOS). Use the `.ps1` file on Windows 11.
The script does these tasks:

* It installs `git` and `uv` if they are missing.
* It clones the course repository to `~/physical_computing_for_beginners`. If the repository is there, it gets the latest code.
* It downloads the Python packages for `deploy.py`, `system_test.py`, and `wireframe.py`. Thus, these tools run when your laptop is on the rover WiFi, which has no internet.
* On Linux, it adds you to the `dialout` group, so that `system_test.py` can open the USB serial port of the Pico. After this, log out and log in one time.
* macOS needs no serial-port setup.

Run the script again at any time to get updates.
[setup-test-laptop.sh][31], [setup-test-laptop.ps1][32]

**`deploy.py` — the installer (laptop).**
Run it from the `full_build` folder with `uv`. It does these tasks:

* It finds the `CIRCUITPY` drive.
* It installs the libraries with `circup`.
* It copies the rover files. It copies `code.py` last, because when `code.py` is saved, the Pico restarts.

`deploy.py` never overwrites your `settings.toml`.
It also does not overwrite a file that you changed on `CIRCUITPY` (for example, your `MAG_OFFSET` or your tuned numbers).
If you add `--overwrite`, it overwrites these files, but it makes a backup of each old file first.
[deploy.py][20]

| Command | What it does |
| :------ | :----------- |
| `uv run deploy.py rover` | Installs the libraries and the full rover. |
| `uv run deploy.py tool mag_calibration` | Saves your rover `code.py` as `code_rover.py`, and runs a tool as `code.py` (also `servo_check`, `motor_check`). |
| `uv run deploy.py test` | The same, for `test/device_test.py`. |
| `uv run deploy.py restore` | Puts your saved rover `code.py` back. |

If `deploy.py` does not find the drive, add `--drive E:\` (Windows), `--drive /media/you/CIRCUITPY` (Linux), or `--drive /Volumes/CIRCUITPY` (macOS).

**`wireframe.py` — orientation viewer (laptop).**
This is the Class 4 3D box, changed into a test tool.

The finished rover does not print CSV through USB.
Thus, `wireframe.py` reads `/data.json` from the rover website through WiFi, two times each second.
It shows a box that follows the roll, pitch, and yaw of the rover. The compass heading shows in the title.
Connect your laptop to the rover WiFi network, then run `uv run src/laptop/wireframe.py`.

Keep the rover on its stand. Each request stops the drive loop for approximately 0.25 s.

While the rover scans or turns (for a maximum of approximately 4 s), it cannot answer.
Thus, the box stops until the rover drives again. This is normal.
If the title shows `no answer from the rover`, the rover did not answer for more than 6 s.

On a Mac, first give permission to your terminal app in **System Settings → Privacy & Security → Local Network**.
If you do not, the terminal app cannot connect to the rover (see the build pitfalls).
[wireframe.py][21]

> **Why? The website makes the rover blind for short times.** Each time a browser (or `wireframe.py`) asks the rover for `/data.json`, the rover counts wheel-encoder ticks for approximately 0.25 s.
> It uses these ticks to measure the wheel speed.
> During that 0.25 s, the drive loop does not check the bump switch, the IR sensor, or the distance.
>
> When the status page is open, this occurs approximately two times each second.
> Turns are protected, because the rover does not answer the website during a turn. But the rover is not protected when it drives straight.
> This is a known limit of the course design.
> Section 8, Step 8 tunes the rover so that it is safe when the page is open *and* when it is closed ([Class 5][34]).

**`device_test.py` — test of each part (Pico).**
This file runs as `code.py` (with `uv run deploy.py test`).
It uses the same library files as the rover, so it tests the code that you drive with.
It goes through each part, one at a time. For each part, it tells you what to do and what to look for.

Then it waits for you to push Enter, and asks you about the result.
At the end, it shows a pass/fail summary.
[device_test.py][22]

**`system_test.py` — test of the full rover (laptop).**
This file runs with the real rover `code.py`, with no changes.
It reads the rover log through USB, and it reads `/data.json` through WiFi.
It tells you how to start each behavior (bump, IR, near obstacle, knob, a turn). Then it checks that the rover responded correctly.

Its checks use wide ranges, so it gives the same result before and after tuning.
[system_test.py][23]


## 6. Build It
1. **Chassis.** Assemble the chassis (motors, wheels, encoder discs, caster).
   Solder long male Dupont leads to the motors. Solder short female leads to the on/off switch.

   > **WARNING:** The tip of the soldering iron is very hot. Do not touch it, and put the iron in its stand when you do not use it.
1. **Install the parts.** Use Blu Tack to attach the breadboard, the DRV8833, the buck converter, and the battery to the chassis. Then install these parts:
   * The servo, with the HC-SR04 on the servo horn, at the front.
   * The limit switch, with its lever in front of the front edge.
   * The IR sensor, low and pointed forward.
   * Each optocoupler around the encoder disc of its wheel. The disc must not touch the optocoupler.
   * The IMU, as far from the motors and the battery as possible.
   * The TFT, in a position where you can read it. Use tape.
1. **Power, then measure.** Connect the power rows of the [wiring table][26].
   Set the buck converter to 5.0 V *before* you connect its output to the 5V rail.
   Do the power-on check.
1. **Signals.** Connect the remaining rows of the table, one device at a time.
1. **Install the software tools (laptop).** Connect your laptop to a usual network with internet access.
   This step gets the code onto your laptop and downloads the packages for the laptop tools. You must do this now, because the rover WiFi has no internet.
   The first time, run the one-line command for the operating system (OS) of your laptop.

   If your **OS is Linux or macOS (MacBook)**, use this command. On a Mac, use the Terminal app:

    ```bash
    # Linux or macOS (Shell)
    # Download the setup script from GitHub and run it with bash.
    #   curl -LsSf = download quietly (-s), follow redirects (-L), stop on HTTP errors (-f), show errors (-S)
    curl -LsSf https://raw.githubusercontent.com/jeffskinnerbox/physical_computing_for_beginners/main/full_build/setup-test-laptop.sh | bash
    ```

   Apple Command Line Tools supply `git`.
   If your Mac does not have them, the script opens their installer and stops.
   Complete that installation, then run the command again.

   If your **OS is Windows**, use this command:

    ```powershell
    # Windows 11 (PowerShell)
    # Download the setup script from GitHub and run it.
    #   -ExecutionPolicy ByPass = let this one script run, also if your laptop blocks scripts
    #   irm = download the script text, iex = run the text as a script
    powershell -ExecutionPolicy ByPass -c "irm https://raw.githubusercontent.com/jeffskinnerbox/physical_computing_for_beginners/main/full_build/setup-test-laptop.ps1 | iex"
    ```

   Later, to get updates, run `full_build/setup-test-laptop.sh` (or `.ps1`) again in your copy.

   **NOTE:** You run the command above, and each command below, from `~/physical_computing_for_beginners/full_build`.
1. **Install the rover software (Pico 2W).** Keep your laptop on the usual network with internet access.
   1. Connect the USB cable.
   2. Put the rover on its stand (wheels off the table).
   3. From the `full_build` folder, run `uv run deploy.py rover`.
   4. On a first installation, the script stops after it copies `settings.toml`.
      Edit `settings.toml` on `CIRCUITPY` with your own network name and password, and save it.
   5. Push Enter.

   > **⚠ CAUTION — ROVER MOVES:** **Keep the rover on its stand each time you deploy or save a file.**
   > The rover starts to drive immediately when `code.py` is saved.
   > The battery switch is your emergency stop for the motors, because the motors use only the 9V battery.
   > When the USB cable is connected, the Pico, the servo, and the sensors stay on. To turn off all the parts, also disconnect the USB cable.
1. **Look at the start-up.** Open the serial console in Mu or Thonny.
   Keep the rover still and flat. Make sure you see these lines, in this order:
   * The WiFi lines.
   * `Calibrating gyro -- keep the rover perfectly still...`
   * `HTTP Server running at http://192.168.4.1:5000`
   * `Full build -- Random Rover starting...`
   * The `drive:` and `scan:` lines, while the wheels turn in the air.

   The TFT shows `dist`, `head`, and `speed`.
1. **Calibrate the compass** (Class 5, Phase 1).
   1. Run `uv run deploy.py tool mag_calibration`.
   2. Move away from steel furniture.
   3. When the tool shows `GO`, turn the fully assembled rover in all directions for 30 seconds.
      Turn it flat, roll it onto each side, tilt it nose-up and nose-down, and turn it upside down.
   4. **Check the spans.** The tool prints three **spans**. They must be approximately equal (for example `(0.98, 1.02, 0.95)`).
      If one span is much smaller, for example `(0.9, 0.9, 0.1)`, you did not roll the rover onto its sides. Do the calibration again.
   5. **Do the axis check.** Use a phone compass, with the rover flat:
      * `mx` is clearly positive when the X arrow on the board points north.
      * `my` is clearly positive when the Y arrow points north.
      * `mz` is negative when the rover is flat. (This is for the northern hemisphere, where the magnetic field of the Earth goes down into the ground.)
   6. If an axis check fails, change the sign of that value in `MAG_AXIS_SIGN` (for example `(-1, 1, 1)` → `(1, 1, 1)`).
      Change it in the running tool (`code.py` on `CIRCUITPY`) *and* in `rover_server.py`, then save.
   7. When you save, the tool starts again from the beginning.
      Thus, **turn the rover in all directions again for the full 30 seconds** when it shows `GO`.
      Check the spans again and do the axis check again. Continue until all three axis checks pass.
   8. Copy the `MAG_OFFSET` line from the **last** run into `rover_server.py` on `CIRCUITPY`.
   9. Run `uv run deploy.py restore`.
   10. Also paste `MAG_OFFSET` (and `MAG_AXIS_SIGN`, if you changed it) into `full_build/src/pico/rover_server.py` on your laptop.
       Then a later `deploy.py rover --overwrite` keeps these values.

    > **Why? Your rover is a magnet.** A magnetometer (compass) cannot tell the difference between the magnetic field of the Earth and other magnetic fields.
    > Your rover has its own magnetic field, from the permanent magnets in the motors, the steel screws, and the battery.
    > This field turns *with* the rover, so it adds the same error to each reading.
    >
    > When you turn the rover in all directions, the field of the Earth moves each axis up and down equally around a center point.
    > That center point *is* the magnetic field of your rover.
    > The tool finds this point and prints it as `MAG_OFFSET`. Then `rover_server.py` subtracts it from each reading.
    >
    > This method works only when each part is in its final position.
    > If you calibrate on a breadboard alone, and then install it next to a motor, the numbers are wrong.
    > Equal spans show that you turned the rover enough.
    > The axis check shows that the X, Y, and Z axes of the compass agree with the axes of the gyroscope ([Class 5][34]).
1. **Test** — [Test the Build][27].
1. **Tune** — [Tune the Rover][28].

**Pitfalls during the build:**

* **The motors do not move, but the console looks normal** → The DRV8833 `SLP` is not on the 3.3V rail.
* **The two motors stop suddenly, also a motor that worked a moment before** → The DRV8833 overcurrent protection stopped the motors.
  The usual cause is a jammed wheel or motor leads that touch.
  This protection stops *both* motors, and they stay off. Do these steps:
  1. Free the wheel and examine the motor leads.
  2. Turn off the battery.
  3. Wait approximately 5 seconds, so that the capacitor can discharge.
  4. Turn on the battery again.
* **All parts work on USB, but no part works on the battery** → A part uses `VBUS`.
  Or the buck converter output does not connect to `VSYS`.
* **The Pico resets when the motors start** → The 9V battery is weak. Replace it, then make sure the capacitor is installed.
* **`ImportError`** → Run `uv run deploy.py rover` again (with internet access), so that `circup` puts the libraries in `/lib`.
  If it prints `Nothing was copied` and shows a list of your files, those files are different from the laptop copies.
  (For example, your `MAG_OFFSET` or your tuned numbers are different.)
  In this condition, the script stopped before it installed the libraries. Do one of these:
  * Copy your values into `full_build/src/pico/` first, and run the command again.
  * Add `--overwrite`. The script then puts a backup of your old files in `full_build/backup/`.
* **`RuntimeError: No pull up found on SDA or SCL`** (directly after the WiFi lines) → The Pico cannot find the IMU. Check these items:
  * The IMU `VIN` is on the 3.3V rail, and `3V3(OUT)` supplies that rail.
  * The IMU `GND` is on the GND rail.
  * `SDA`/`SCL` are on `GP0`/`GP1`.
  * The STEMMA QT plug is fully in its socket.

  To find the problem, run `uv run deploy.py test`.
* **All calibration spans are very small (less than approximately 0.2)** → You calibrated on a steel desk, or the IMU does not answer. Move to a wood or plastic table.
* **The `heading` is wrong or changes slowly** → The rover moved or was tilted at start-up, or the IMU moved after calibration.
  Start the rover again, still and flat. If a part moved, calibrate again.
* **A browser opens `http://192.168.4.1:5000`, but `wireframe.py` or `system_test.py` cannot connect to the rover** → This is a macOS permission problem.
  macOS blocks local-network access for programs that you start from Terminal.
  It does this until you give permission, also if your browser has permission.
  1. Open **System Settings → Privacy & Security → Local Network**.
  2. Turn on **Terminal** (or the terminal app that you use).
  3. Quit the terminal app and open it again.

  For other causes, read the `Last error:` line that `wireframe.py` prints.
* **The TFT is blank** → Compare `GP26`/`GP27`/`GP20`-`GP22` with the table. Make sure `RST` (not the backlight pin) is on `GP22`.
* **The knob changes the speed in the wrong direction, or needs two clicks for each step** → Read the comments in `speed_knob.py`. (Swap `GP3`/`GP4` in the code, or add `divisor=2`.)


## 7. Test the Build
Test the rover before you tune it.
The two tests use the placeholder tuning values. After you tune, the two tests continue to work with no changes.

1. **Test each part.**
   1. Put the rover on its stand. Connect the USB cable. Turn on the battery switch.
   2. Run `uv run deploy.py test`, and follow the instructions in the serial console.
   3. If a part fails, repair it and run the test again. Do not continue until all parts pass.
   4. Run `uv run deploy.py restore`.
2. **Test the full rover.**
   1. Put the rover on its stand. Connect the USB cable. Turn on the battery switch.
   2. Connect the laptop to the rover WiFi network.
   3. Close the serial console in Mu or Thonny. (Only one program at a time can use the serial port.)
   4. Run `uv run test/system_test.py` and follow its instructions.
      If it cannot find the Pico, give the port name: `COM5` on Windows, `/dev/ttyACM0` on Linux, `/dev/cu.usbmodem...` on macOS.
3. **Look at the orientation.**
   1. Run `uv run src/laptop/wireframe.py`.
   2. Tilt and turn the rover with your hand. Make sure the box follows the rover.
   3. Turn the rover clockwise a quarter turn. Make sure `heading` goes **up** by approximately 90.
   4. Open `http://192.168.4.1:5000`. Make sure the history chart moves.
4. **Do the first floor run.**
   1. Disconnect the USB cable.
   2. Put the rover on the floor, still and flat.
   3. Turn it on, and do not touch it for 3 seconds.
   4. The rover drives, stops, scans, turns, and drives again.

   The movement does not have to be good yet.
   Tuning corrects a turn that moves left and right, or a stop that is too near an obstacle.



## 8. Tune the Rover
Your rover works. It drives, stops, moves its sensor across the scan angles, turns, and drives again.
But a rover that "works" and a rover that works "*well*" are different. For example:

* Its turns go too far, and then it moves back.
* It touches walls before it stops.
* It prints `turn timed out` on carpet.

These problems do not mean that the code is wrong.
They mean that the rover still uses *starting guesses*.
These numbers were selected before anybody knew your motors, battery, servo, and floor.

This section replaces these guesses with numbers for *your* rover.
It comes from the [Strategy for Tuning and Calibrating the Random Rover][02] guide.
This section uses the full-build files and tools, and adds the background from the lesson scripts.
You do not need to open the guide.

Write each change in a copy of the tuning log, [`src/tuning-log-template.md`][33]. The rows of the log are in the same order as the steps below.
The tuning guide uses the same template. Thus, there are two small differences:

* In **Extra rows**, add your own Step 2 row for `SLOTS_PER_REV` (old value `20`).
* On the chart-refresh row, ignore "(only if Stretch 2 is installed)". The full build always has the chart.


### 8.1 What tuning is, and why it is important
**Current condition.** Each Pico program in this build has a block of `ALL_CAPS` constants near the top.
Examples are `DRIVE_SPEED = 0.6`, `STOP_DISTANCE_CM = 25`, and `MAG_OFFSET = (0.0, 0.0, 0.0)`.
Each constant is a control value (a "knob") for one behavior of the rover.

**Problem.** The starting values are for an *average* rover. Your rover is not average:

* Its IMU is at a specific distance from a specific motor.
* The gears of its servo are a small angle off center.
* Its 9V battery is newer or older than the battery of a different rover.
* Its test floor is tile or carpet.

Each difference moves the rover a small amount away from the default numbers, and the differences add together.

**Solution.** Measure your rover, and adjust the values to agree with it.
There are three types of this work. Keep them separate:

1. **Calibration** — measure a fixed fact about your hardware and type it in.
   There is one correct answer, and you find it.
   Example: `MAG_OFFSET`, the magnetic field that your rover carries.
2. **Tuning** — adjust a number that balances two good results. Test and look at the result.
   There is a *best* answer for your rover, not one correct answer.
   Example: `TURN_SPEED`. If it is too slow, the rover cannot turn on carpet. If it is too fast, the rover turns too far.
3. **Preferences** — select a number that you like. Nothing breaks.
   Example: `SCAN_INTERVAL`, the time between the scans when no object is in front of the rover.

A rover with good code and bad numbers operates like a rover with bad code.
When you tune your robot, it stops being a copy of the class demo and becomes *your* robot.


### 8.2 Each knob on the rover
All the files below are on the `CIRCUITPY` drive. The **Importance** column uses five levels:

* **Critical** — if this is wrong, the rover operates very badly, or the hardware can be damaged.
* **Important** — this has a clear effect on how well the rover avoids obstacles.
* **Useful** — a small improvement. Do it after the important items.
* **Taste** — your preference. Nothing breaks.
* **Leave alone** — this is already correct, or it has no effect on the movement. Do not change it.

| Parameter | Where it is | Start value | What it controls | Importance | Step |
| :-------- | :------------- | :---------- | :--------------- | :--------- | :--- |
| 9V battery charge | the battery | fresh | Motor strength, and the power to the Pico through the buck converter | **Critical** | 1 |
| Buck converter output | buck converter trimpot (if it has one) | 5 V | Power to the Pico `VSYS`, the servo, and the HC-SR04 | **Critical** (can damage parts) | 1 |
| Part installation | the chassis | — | Whether the IMU, sensor, servo, bumper, and IR sensor stay in position | **Critical** | 2 |
| `SLOTS_PER_REV` | `wheel_odometry.py` | `20` | Wheel speed on the website and the history chart | **Useful** (website only) | 2 |
| `min_pulse` / `max_pulse` | `code.py`, `servo.Servo(...)` line | `500` / `2500` | How accurately the real servo angle agrees with the commanded angle | **Important** | 3 |
| `CENTER_ANGLE` | `code.py` | `90` | The servo angle that means "straight ahead" | **Important** | 3 |
| `MAG_OFFSET` | `rover_server.py` | `(0.0, 0.0, 0.0)` until you calibrate | Removes the magnetic field of your rover from the compass | **Critical** | 4 |
| `MAG_AXIS_SIGN` | `rover_server.py` (and `mag_calibration.py`) | `(-1, 1, 1)` | Makes the compass axes agree with the gyroscope axes | **Critical** | 4 |
| Start still and flat | how you turn on the rover | — | Gyroscope bias and starting compass heading, measured at each start | **Critical** (a habit, not a number) | 4 |
| `MAX_THROTTLE` | `motor_driver.py` | `0.6` | Maximum limit for each motor command, including `DRIVE_SPEED`, `TURN_SPEED`, and the knob | **Critical** (can damage parts) | 5 |
| `TURN_SPEED` | `code.py` | `0.45` | How fast the rover turns during a compass turn | **Critical** | 6 |
| `HEADING_TOLERANCE_DEG` | `code.py` | `5` | How near to the target heading is "arrived" | **Important** | 6 |
| `TURN_TIMEOUT_S` | `code.py` | `3.0` | When to stop a turn that does not arrive | **Useful** (a safety limit) | 6 |
| `SETTLE_TIME` | `code.py` | `0.15` | The time the servo gets to stop before a distance reading | **Important** | 7 |
| `SCAN_ANGLES` | `code.py` | `[30, 60, 90, 120, 150]` | The directions that the rover looks in each scan | **Useful** / **Taste** | 7 |
| `DRIVE_SPEED` | `code.py` | `0.6` | The *starting* speed of the knob at each start: forward speed, and reverse speed after a safety stop | **Important** / **Taste** | 8 |
| `STOP_DISTANCE_CM` | `code.py` | `25` | How near an obstacle comes before an emergency stop and a new scan | **Critical** | 8 |
| `SCAN_INTERVAL` | `code.py` | `3.0` | How frequently the rover stops to look when no object is near | **Taste** | 8 |
| Status page refresh | `rover_server.py`, `STATUS_PAGE` `setInterval(..., 500)` | `500` ms | How frequently the website asks for new data. Each request stops the drive loop for a short time. | **Useful** | 8 |
| Chart refresh | `history_chart.py`, `setTimeout(pollHistory, 200)` | `200` ms | How frequently the history chart asks for new data. Each request stops the drive loop for a short time. | **Important** | 8 |
| IR sensor trimmer | small screw on the IR module | — | The distance at which the IR sensor triggers | **Important** | 9 |
| `BACKOFF_S` | `code.py` | `0.3` | How long the rover reverses after a bump stop or an IR stop | **Important** | 9 |
| `MIN_SPEED` / `MAX_SPEED` / `SPEED_STEP` | `speed_knob.py` | `0.3` / `0.9` / `0.05` | The speed range and the step size of the knob | **Taste** (with limits) | 10 |
| `REFRESH_S` | `tft_status.py` | `0.2` | How frequently the TFT screen updates | **Taste** | 10 |
| `MAHONY_KP`, `MAHONY_KI` | `rover_server.py` | `2.0`, `0.05` | How the IMU filter mixes the gyroscope, gravity, and compass data | **Leave alone** | — |
| `CAL_SAMPLES`, `STILL_GYRO`, `STILL_ACCEL`, `BIAS_ALPHA`, `GRAVITY` | `rover_server.py` | as set in Class 4 | Automatic correction of the gyroscope bias | **Leave alone** | — |
| `WHEEL_DIAMETER_MM` | `wheel_odometry.py` | `67` | Wheel speed on the website | **Leave alone** (agrees with the kit wheels) | — |
| `SAMPLE_SECONDS` | `wheel_odometry.py` | `0.25` | How long each website request counts wheel ticks. This is also how long the drive loop is blind for each request. | **Leave alone** (a larger value makes the blind time longer) | — |

>**NOTE — two differences from the tuning guide:**
>
>* The guide marks `SLOTS_PER_REV` "Leave alone," because Class 3 students count their encoder discs. You did not count your discs, so Step 2 tells you to count them.
>* The guide includes the Class 3 `straight_drive.py` and the timed-turn constants. This build does not include these files, so you do not tune them.

The list of important items is shorter than the table.
The bottom rows are already correct, or have no effect on the movement.

> **Why leave the IMU filter alone?** `MAHONY_KP` and `MAHONY_KI` control how the filter mixes two types of data.
> The gyroscope is fast, but its value slowly moves away from the correct value (drift). The accelerometer and the compass are slow, but stable.
>
> If the values are too low, the heading drifts. If they are too high, the heading jumps a small amount again and again.
> In Class 4, students change `MAHONY_KP` to see this balance.
> But the default values `2.0` and `0.05` already work well for this IMU, and the rover turns need a smooth heading.
> If you change them, you get a new problem, not a better rover ([Class 4][41]).


### 8.3 The strategy: tune from the bottom up
A rover is a stack of layers. Each layer depends on the layers below it.
If you tune a high layer before the low layers are correct, you must do the work again.
It is like when you level a picture frame on a wall that is not straight.

This diagram shows the layers and the steps that tune each layer:

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

Obey these five rules:

1. **Bottom up.** Complete each step before you start the next step.
   The order makes sure that a later step does not cancel an earlier step. The exceptions have the label **Ripple effects**.
2. **One change at a time.** Change one number, test, and write down the result.
   If you change two numbers at the same time, you cannot know which change helped.
3. **Do each test three times.** One good run can be luck. Three good runs are a result.
4. **Write down each change.** Your tuning log is your memory.
   When a problem occurs tomorrow, the log tells you what worked today.
5. **Know when to stop.** Each step has a **Done when** line. When you get that result, go to the next step.

This diagram shows where each knob is in the stop-look-go loop of the rover:

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
Tuning makes the rover *reliable at the tasks that it already does*. It does not make the rover more intelligent.
The rover is still a simple robot that only reacts, like an insect (see [What Is the Random Rover?][42]).

| Behavior | Not tuned (typical) | Well tuned (target) |
| :------- | :---------------- | :------------------ |
| Compass turns | Turns too far and moves back, sometimes `turn timed out` | Stops within approximately ±5° of the target, one clean stop, no timeouts |
| Heading on the website | Wrong by tens of degrees, changes slowly | Increases by approximately 90 for each quarter turn by hand. Stays within a few degrees for one minute. |
| Stop for a box in front | Sometimes touches the box | Stops with a gap that you can see, each time, at your selected speed |
| Bump switch contacts in a 5-minute run | Several | 0 to 2 |
| Times that you must help the rover in 5 minutes | Several | 0 to 1 |

Tuning does **not** correct these problems. They are limits of the hardware and the design, not of your numbers:

* **Thin, soft, or angled objects.** The HC-SR04 measures echoes.
  Thin chair legs, fabric, and walls at a steep angle can send the sound away, so the sensor does not see them.
  The IR sensor and the bump switch are the backups for these objects.
* **Edges and stairs.** No sensor on the rover looks *down*. The rover can drive off a table edge or down a stair.
  Always test on the floor.
* **Dead ends.** If all directions are blocked, the rover selects the direction with the most space.
  It drives a few centimeters, stops again, and does the same steps again. This is the design.
* **Magnetic problem areas.** Steel desks, radiators, and steel bars in the floor change the magnetic field of the Earth.
  Near these objects, turns can stop off target, also after a good calibration.
* **The browser stop.** When the website is open, each page refresh can stop the drive loop for approximately 0.25 s.
  (See the **Why?** box in [The Code][25].)
  You test with the page closed *and* open, so that your numbers work in both conditions.
* **Magnetic jumps from motor current.** The current in the motors makes its own magnetic field.
  Calibration can remove only fields that are always there. Thus, a small heading jump when the motors start is normal.
* **Weak battery.** A 9V battery becomes weaker as it discharges.
  Closed-loop compass turns are not affected, but the straight-line speed and the stop distance slowly change.


### 8.5 How to use this procedure
Start at Step 0, and do the steps in order. Each step has the same parts:

* **Parameters** — the values that you set, and how important they are.
* **Time** — a realistic estimate.
* **Why** — what occurs, in simple words.
* **Do this** — the numbered actions.
* **Done when** — the test that tells you that the step is complete.
* **Ripple effects** — the other values that this step can change, and when to come back.

**Total time: approximately 4 to 4.5 hours.** Do it in more than one session. This is a good division:

| Session | Steps | Time |
| :------ | :---- | :--- |
| Session A | 0 – 5 (power, installation of parts, servo, compass, motors) | approximately 1.75 hours |
| Session B | 6 – 11 (turns, scans, behavior, safety nets, preferences, final test) | approximately 2 to 2.5 hours |

If you must stop before the end, stop *between* two steps. Write down the last step that you completed.

**How to change numbers.** Except where a step tells you differently, do these steps:

1. Open the file on `CIRCUITPY` in Mu or Thonny.
2. Change the number.
3. Save the file.

When you save a file, the rover program starts again.

**How to start the rover "still and flat" on the floor.** Several steps tell you to *start the rover still and flat* on the floor.

* If the USB cable is disconnected:
  1. Put the rover down.
  2. Turn on the battery.
  3. Do not touch the rover for 3 seconds.
* If the USB cable is connected (so that you can read the console), the battery switch does **not** restart the Pico.
  The laptop supplies power to the Pico. Do these steps:
  1. Put the rover down.
  2. Click in the serial console.
  3. Push Ctrl-C, then Ctrl-D.
  4. Do not touch the rover for 3 seconds.

**Safety labels in this section:**

> **⚠ CAUTION — HARDWARE DAMAGE:** If you do this incorrectly, you can permanently damage a part.
>
> **⚠ CAUTION — ROVER MOVES:** The rover can move when you do not expect it, fall, or hit an object.


### Step 0 — Get ready: tools, test area, tuning log
**Parameters:** none. **Time:** 15 minutes.

**Tools that you need:**

| Tool | Used in steps | Why |
| :--- | :------------ | :-- |
| Multimeter (DC volts) | 1 | Check the battery and the 5 V rail |
| Small screwdriver | 1, 9 | Buck converter trimpot (if it has one), IR sensor trimmer |
| Fresh 9V battery, and one spare | 1, all | Motor strength changes as the battery discharges |
| Masking tape and a pen | 3, 5, 8 | Mark start lines, distances, and a paper protractor |
| Tape measure or meter stick | 5, 7, 8, 9 | Measure stop gaps, run distances, and reverse distance |
| Protractor, or a printed paper protractor | 3 | Check servo angles |
| Phone with a compass app | 4 | Check the heading of the rover |
| Phone stopwatch/timer | 6, 11 | Measure the time of turns and of the final 5-minute run |
| Rover stand: a cup, box, or block that lifts the wheels off the table | 1, 2, 3, 4 | Run the code on the bench, so that the rover does not drive away |
| 4-6 cardboard boxes (shoebox size or larger) | 7, 8, 11 | Obstacles that the ultrasonic sensor sees well |
| Laptop with Mu or Thonny, USB cable, and this repository (`full_build` folder) | all | Edit code, read the serial console, run `deploy.py` |
| Laptop or phone with a browser | 4, 8 | The rover status website, `http://192.168.4.1:5000` |
| Your tuning log ([`src/tuning-log-template.md`][33], printed or copied) | all | Your memory |

**Do this:**

1. **Make a backup of your working code.**
   Copy all seven `.py` files on `CIRCUITPY` and `settings.toml` to a folder on your laptop with the name `rover-before-tuning`.
   The seven files are `code.py`, `rover_server.py`, `motor_driver.py`, `wheel_odometry.py`, `history_chart.py`, `speed_knob.py`, and `tft_status.py`.
   If a problem occurs during tuning, you can always go back to these files.
2. **Prepare a test area** on the floor, a minimum of 2 m × 2 m.
   Keep it away from table edges, stairs, and large steel furniture. Use a wall or a row of boxes as a boundary.
3. **Start your tuning log.** Write one row each time that you change a number. For example:

    | Step | Parameter | Old value | New value | Test | Result (3 runs) | Keep? |
    | :--- | :-------- | :-------- | :-------- | :--- | :-------------- | :---- |
    | 6 | `TURN_SPEED` | 0.45 | 0.40 | `[150]` turn test | +3, +4, +2 | yes |

4. **Learn the three safety habits** that you use during all the tuning:
   * > **⚠ CAUTION — ROVER MOVES:** **Put the rover on its stand before you save a file or run `deploy.py`.**
     > When you save *any* file on `CIRCUITPY`, the program starts again *immediately*.
     > If the rover code is on the board and the rover is on the table, the rover drives off the edge.
   * The battery switch is your emergency stop for the motors. Know where it is.
     When the USB cable is connected, the laptop supplies power to the Pico and the servo. To stop all the parts, also disconnect the USB cable.
   * **Do not touch the speed knob during tuning**, except when a step tells you to turn it.
     The knob immediately replaces `DRIVE_SPEED`. Thus, one accidental click changes the speed that you test.
     Each restart sets the knob back to `DRIVE_SPEED`.

**Done when:** you have a backup of your code, your log is ready, you have your tools, and the test area is clear.


### Step 1 — Power: a strong battery and a correct 5 V rail
**Parameters:** 9V battery charge (**Critical**), buck converter output (**Critical**).
**Time:** 10 minutes.

**Why.** All the steps after this step need stable power.
A motor uses a large current when it starts. A weak battery voltage decreases during this current.
This decrease goes through the buck converter to the Pico. Then the Pico can *brown out* (reset) each time that the motors start.

A weak battery also makes the motors weak and changes how far the rover moves after the motors stop.
Tuning cannot correct bad power.

**Do this:**

1. Disconnect the battery clip. Set the multimeter to DC volts, and measure the 9V battery.
   Write the value in your log.
   A fresh alkaline 9V battery shows approximately 9 V or a little more.
   If it shows less than approximately 8 V, use a fresh battery for tuning.
2. Connect the battery again, with the USB cable disconnected. Put the rover on its stand, and turn it on.
3. Measure between the Pico `VSYS` pin and `GND` (the output of the buck converter).
   The value must be near 5 V: approximately 4.8 V to 5.2 V.
4. Look at the multimeter while the motors run. (The rover code turns the wheels in the air, on the stand.)
   The value must stay above approximately 4.7 V.
   If it decreases much, or the Pico resets when the motors start, replace the battery.
   If a fresh battery also decreases much, make sure the 1000 µF capacitor is tightly across `VM`/`GND` at the DRV8833, with the stripe to GND.
   The capacitor is a small energy store that supplies the start current of the motors ([Class 3][35]).

> **⚠ CAUTION — HARDWARE DAMAGE:** If the buck converter output is **more than 5.5 V**, turn off the power immediately.
> Do not connect the Pico again until you correct the voltage.
> The maximum rating of the Pico `VSYS` input is **5.5 V** (see the [Pico 2 W datasheet][36]).
> The servo and the HC-SR04 use the same 5 V rail. Thus, too much voltage can damage all three parts at the same time.
>
> If your buck converter has an adjustment screw (a trimpot), **disconnect its output from the Pico before you turn the screw**.
> Set the output to 5.0 V with the multimeter, then connect it again.
> If you turn a trimpot while the Pico is connected, a voltage spike can destroy the board.

**Done when:** the battery shows approximately 9 V with no load. `VSYS` shows 4.8-5.2 V with no load, and stays above approximately 4.7 V while the motors turn. The Pico does not reset when the motors start.

**Ripple effects:** you tune all the motor values later (Steps 5, 6, 8, 9) *with this battery*.
When you replace the battery, do the quick checks in Step 11 again.


### Step 2 — Mechanics: attach all the parts tightly, count your slots
**Parameters:** part installation (**Critical**), `SLOTS_PER_REV` (**Useful**). **Time:** 20 minutes.

**Why.** Calibration measures the positions of the parts.
If a part moves after you calibrate, the calibration is wrong.
Thus, first put each part in its final position, and attach it so that it stays there.

**Do this:**

1. **IMU:** Install it in its permanent position, as far from the motors and the battery as the chassis permits. Attach it tightly.
   Push on it. It must not move.
2. **Battery:** Put it in its final position, and attach it.
   (For the compass, the battery is a source of unwanted magnetic field. If the battery moves, the compass calibration becomes incorrect.)
3. **Ultrasonic sensor on the servo:** Make sure the sensor is tight on the servo horn.
   Make sure the horn is tight on the servo shaft.
4. **Bump switch:** The lever must extend past the front of the chassis, so that each contact pushes it.
   Push it with a finger. It must click.
5. **IR sensor:** Attach it low on the chassis. Point it forward, and tilt it up a small angle so that it does not see the floor.
6. **Wires:** Make sure no wire hangs near a wheel, and no wire is loose on the breadboard.
   Make sure the Blu Tack holds the breadboard, the DRV8833, the buck converter, and the battery tightly.
7. **Wheels:** Turn each wheel with your hand.
   It must turn freely and not touch the chassis. Each encoder disc must go through the slot of its optocoupler without contact.
8. **Count your encoder slots.** Count the slots (the gaps, not the teeth) around the encoder disc of one wheel.
   If the number is not `20`, change `SLOTS_PER_REV` in `wheel_odometry.py` to your number. (Put the rover on its stand before you save.)
   This value has an effect only on the wheel speed on the website and the history chart.
   Each slot that goes through the optocoupler is one *tick*.
   The code uses the slot count and the wheel size to change ticks per second into cm/s ([Class 3][35]).

   To check your count, do these steps:
   1. **Turn off the battery, and keep the USB cable connected.**
      The code continues to run and the website continues to answer, but the motors have no power. Thus, you can safely touch the wheels.
   2. If a wheel moves slowly or makes a hum, your buck converter sends USB power back to the motors.
      In this condition, temporarily set `DRIVE_SPEED = 0` and `TURN_SPEED = 0` in `code.py`, as in Step 7. Put the old values back after the check.
   3. Open the website and look at `speed_left_cms`. When you do not touch the wheel, it must show `0`.
   4. Turn the left wheel with your hand at a constant speed of one turn each second. (Say "one-Mississippi" for each turn.)
      It must show approximately **21** cm/s, because a 67 mm wheel moves approximately 21 cm in each turn.
   5. The value changes in steps of approximately 4 cm/s. Thus, values between approximately 17 and 25 are normal.
      A value near 10 or 40 means that your slot count is wrong by a factor of two.
   6. Do the same check for the right wheel with `speed_right_cms`.
   7. If a value is far out of range, or changes when the wheel is still, see the [Class 3 troubleshooting guide][47].
      Read its wheel-speed rows.
9. **Quick function check**, with the rover code running on the stand:
   * Push the bump switch. Make sure you see `SAFETY: bump switch contact`.
   * Move your hand in front of the IR sensor. Make sure you see `SAFETY: IR sensor near-field obstacle`.

**Done when:** you lift the rover and shake it gently, and no part moves, makes noise, or comes loose. The two safety sensors trigger when you trigger them by hand. `SLOTS_PER_REV` agrees with your disc.

**Ripple effects:** if you install the IMU again, move the battery, or add steel near the IMU, do Step 4 again.
This calibrates the compass again.
If you install the servo horn again, do Step 3 again.


### Step 3 — Servo aim: make "90" mean straight ahead
**Parameters:** `CENTER_ANGLE` (**Important**), `min_pulse` / `max_pulse` (**Important**).
**Time:** 20 minutes.

**Why.** When the scan selects angle `150`, the rover turns `150 - 90 = 60` degrees to the right.
This calculation is correct only if the servo points 60° right when the code sends `150`.
If the servo is wrong by 10°, each turn is wrong by 10°.
Compass tuning cannot correct this error, because the compass steers accurately to the wrong target.

Why can the angle be wrong? A servo does not know degrees.
The Pico sends a pulse to the servo each 20 ms, and the *width* of the pulse sets the angle.
Approximately 500 microseconds gives one end, and approximately 2500 microseconds gives the other end.
`min_pulse` and `max_pulse` tell the code which widths *your* servo uses for 0° and 180°.
Each SG90 is a little different, and the horn can be one tooth off on the shaft ([Class 2][40]).

This diagram shows what the scan angles mean, as seen from above:

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

1. Put the rover on its stand.
   Attach a paper protractor with tape under or behind the sensor. (Or draw lines at 30°, 90°, and 150°.)
   The 90° line must point straight along the nose of the rover.
2. Run `uv run deploy.py tool servo_check`.
   This command replaces your rover `code.py` and runs [`servo_check.py`][43] as `code.py`.
   The tool points the servo at 90, 30, 90, and 150, for 3 seconds each. It prints `servo at ...` and does this again and again.
3. **Check the center first.** When the tool prints `servo at 90`, look at the sensor. It must point straight along the nose.
   * If it is wrong by more than approximately 5°, use a mechanical correction.
     Pull the horn off the shaft, and push it on again one tooth over. Make 90 as near to straight as possible.
   * If you cannot get it near enough with this method, write down the angle that *does* look straight (for example `95`).
     Later, set `CENTER_ANGLE` in `code.py` to this value, and move each value in `SCAN_ANGLES` by the same quantity.
     For the remaining part of this step, change `CHECK_ANGLES` in the running tool (`code.py` on `CIRCUITPY`) to `CENTER_ANGLE` and `CENTER_ANGLE` ± 60 (for example `[95, 35, 95, 155]`).
4. **Check the span.** At `30` and `150` (or `CENTER_ANGLE` ± 60), the sensor must point approximately 60° to each side of straight ahead.
   * If the two sides do not go far enough (for example, only 50° on each side), increase the pulse range a little.
     In the running tool, decrease `MIN_PULSE` by 50 and increase `MAX_PULSE` by 50.
   * If the two sides go too far, decrease the range in the same way.
   * Change the values in steps of 50, and save after each change. The tool starts again with the new values.

   > **⚠ CAUTION — HARDWARE DAMAGE:** **Immediately disconnect the USB cable *and* turn off the battery** if the servo buzzes or grinds at an angle.
   > Then decrease the pulse range.
   >
   > The servo pushes against its mechanical stop. If it continues to strain, it becomes too hot and its plastic gears break.
   > It is not enough to turn off only the battery. When the USB cable is connected, the laptop supplies power to the 5V rail and to the servo.
   > For this reason, the test uses only the range 30 to 150, which is the range that the rover uses.
5. Write your final `MIN_PULSE` and `MAX_PULSE` (and `CENTER_ANGLE`, if you changed it) in your log.
6. Run `uv run deploy.py restore` to put the rover code back.
7. With the **rover on its stand**, edit `code.py` on `CIRCUITPY`:
   * Copy the values into the `servo.Servo(pwm, min_pulse=..., max_pulse=...)` line.
   * If necessary, set `CENTER_ANGLE` and `SCAN_ANGLES`.

**Done when:** at `CENTER_ANGLE` (usually `90`), the sensor points straight ahead within approximately 5°.
At `CENTER_ANGLE` ± 60 (usually `30` and `150`), it points approximately 60° left and right, within approximately 5°.
The servo makes no buzz at each stop.

**Ripple effects:** if you later change `SCAN_ANGLES` to include angles outside 30-150 (Step 7), check the aim at the new angles.


### Step 4 — Compass: check the calibration and the heading
**Parameters:** `MAG_OFFSET` (**Critical**), `MAG_AXIS_SIGN` (**Critical**), start still and flat (**Critical** habit). **Time:** 25 minutes.

**Why.** The compass steers each turn.
If the compass is wrong, the turns are wrong, and later tuning cannot correct this.

You calibrated the compass in [Build It][46], step 8.
If *any* part moved in Step 2 (the IMU, the battery, a motor, a steel screw), that calibration is not correct now.
(For the reason, read the **Why? Your rover is a magnet** box in Build It, and the [IMU and Mahony filter explainer][37].)

**Do this:**

1. **Calibrate again if a part moved after Build It step 8, or if you are not sure.**
   Take the fully assembled rover to a place away from steel. Do that step again exactly:
   1. Run `uv run deploy.py tool mag_calibration`.
   2. Turn the rover in all directions for 30 s.
   3. Make sure the spans are equal, and do the axis check.
   4. Paste `MAG_OFFSET` (and `MAG_AXIS_SIGN`, if you changed it) into `rover_server.py` on `CIRCUITPY` *and* into `full_build/src/pico/rover_server.py` on your laptop.
   5. Run `uv run deploy.py restore`.

   If no part moved, go to item 2.
2. **Start the rover still and flat on the stand.**
   The USB cable is still connected from item 1. Thus, the battery switch does not restart the Pico. Do these steps:
   1. Put the rover down.
   2. Click in the serial console, and push Ctrl-C, then Ctrl-D.
   3. Do not touch the rover for 3 seconds.

   (See 8.5, and the **Why? "Start still and flat"** box in [The Code][25].)
3. **Heading check.** Open the rover website (`http://192.168.4.1:5000`, with the laptop on the rover WiFi). Then do these checks:
   * Turn the rover clockwise by hand, approximately a quarter turn. `heading` must go **up** by approximately 90.
   * Do not move the rover for one minute. `heading` must stay within a few degrees.
   * Put a phone compass next to the rover. The two values must be approximately equal (within 10-20°).
     If your IMU is installed at 90° to the rover, the difference can be a fixed 90° or so. This is also correct, because turns use only *changes* in heading.

   If `heading` goes **down** on a clockwise turn, `MAG_AXIS_SIGN` is wrong. Do the axis check in item 1 again.
   If `heading` disagrees with the phone and moves back after a turn by hand, `MAG_AXIS_SIGN` is also wrong.
4. **Motor-interference check.** Keep the rover on the stand. Look at `heading` when the wheels start to turn.
   * A jump of a few degrees that goes back is normal.
     The current in the motor wires makes its own magnetic field.
     Calibration cannot remove this field, because it is there only while the motors run.
   * A jump of more than approximately 15-20° means that the IMU is too near the motors.
     Move the IMU farther away (higher, on a standoff). Then **start this step again from item 1**, and calibrate again.

**Done when:** the spans are approximately equal, and all three axis checks pass.
A clockwise quarter turn increases `heading` by approximately 90, and `heading` stays stable for a minute.
When the motors start, `heading` changes by less than approximately 15°.

**Ripple effects:** this calibration is correct only while *no magnetic part moves* relative to the IMU.
If you move the IMU, the battery, or the motors, or add a steel screw or bracket near the IMU, do this step again.
If you change the code or the speed, you do **not** have to calibrate again.


### Step 5 — Motors: find the stall points and measure your real speed
**Parameters:** `MAX_THROTTLE` (**Critical**). Also three measurements for later steps: the straight-drive stall point, the turn stall point, and your speed in cm/s.
**Time:** 20 minutes.

**Why.** A "throttle" of 0.5 does *not* mean half speed.
The Pico turns the motor on and off very quickly (PWM, Pulse Width Modulation). A throttle of 0.5 means "on for half of the time."

But a motor needs a minimum force to start to turn against friction. Below that minimum, it makes a hum and does not move.
That minimum is the **stall point**.

A turn in place needs *more* force than a straight drive, because the wheels move sideways on the floor. This is especially true on carpet.
You need the two stall points before you can select `TURN_SPEED` and `DRIVE_SPEED` ([Class 3][35]).

There is also a hidden limit. `motor_driver.py` limits **each** motor command to `MAX_THROTTLE = 0.6`.
Thus, `DRIVE_SPEED = 0.6` is already at the maximum.
If you set `DRIVE_SPEED = 0.8`, it has *no effect* unless you also increase `MAX_THROTTLE`.
For the same reason, the maximum knob speed is `MAX_THROTTLE`.

> **⚠ CAUTION — HARDWARE DAMAGE:** **Keep `MAX_THROTTLE` at `0.6` during tuning.**
> `MAX_THROTTLE` protects the small TT gearbox motors, which get power from a 9V battery.
> If you increase it, increase it in steps of 0.05.
> After a 1-minute run, touch the motor cases. If they are warm, this is correct.
> If they are too hot to keep a finger on, decrease `MAX_THROTTLE` again.
>
> Too much current can also start the DRV8833 overcurrent protection.
> The protection stops *both* motors until you turn off the battery, wait approximately 5 seconds, and turn it on again.

**Do this:**

1. Put a start line on the floor with masking tape. Make sure there is a minimum of 2 m of clear floor in front of it.
2. Put the rover on its stand, and run `uv run deploy.py tool motor_check`.
   This command runs [`motor_check.py`][44] as `code.py`, with your `motor_driver.py`.
3. When the tool prints `Set the rover on the floor -- starting in 5 s`, put the rover on the floor.
   If it starts before you are ready, put it back on the stand. Click in the serial console, and push Ctrl-C to stop it. Then push Ctrl-D to start it again.
4. The tool does these tests:
   * Short straight runs at throttle 0.20, 0.25, … 0.60.
   * The same throttle values for turns in place.
   * Two speed runs of 2 seconds, at 0.5 and 0.6. The tool tells you when to put the rover on the start line.
5. Keep the USB cable connected and follow the rover. Carry the laptop, or let the cable move behind the rover.
   Look at the rover and the console at the same time.
6. Write down these values:
   * **Straight stall point** — the lowest throttle at which the rover moves forward.
   * **Turn stall point** — the lowest throttle at which the rover turns in place. Measure it on the floor that you use for the tests, because carpet needs more force than tile.
   * **Speed** at 0.5 and 0.6. Divide the distance in cm by 2 s to get cm/s. For example, 70 cm in 2 s is 35 cm/s.
7. Put the rover on its stand, and run `uv run deploy.py restore`.

**Done when:** your log has a straight stall point, a turn stall point, and a speed in cm/s for 0.5 and 0.6. You measured all of them on your test floor. `MAX_THROTTLE` is still `0.6`.

**Ripple effects:** these numbers change with the battery and with the floor surface.
If you move from tile to carpet, do this step and Step 6 again.



### Step 6 — Turns: clean, accurate compass turns
**Parameters:** `TURN_SPEED` (**Critical**), `HEADING_TOLERANCE_DEG` (**Important**), `TURN_TIMEOUT_S` (**Useful**, a safety limit).
**Time:** 30 minutes.

**Why.** Most rovers that are not tuned look bad when they turn.
A compass turn turns toward the target and checks the heading each 20 ms (see **Why? Closed-loop turns** in [The Code][25]).
If the turn speed is too low, the wheels cannot move the rover.
If the turn speed is too high, the rover goes past the target before the next check, and then must turn back.

This diagram shows the three possible results:

```text
   TURN_SPEED too low          TURN_SPEED about right        TURN_SPEED too high
   --------------------        ----------------------        -------------------
   wheels hum, rover barely    one smooth spin, stops        spins past, reverses,
   moves -> "turn timed out"   within +/-5 of target         spins past again ->
                                                             wiggles, sometimes times out
```

**Do this:**

1. **Set a starting point.** Put the rover on its stand, and edit `code.py`.
   Set `TURN_SPEED` to your turn stall point from Step 5, plus approximately `0.1`. (For example, stall at `0.35` → start at `0.45`.)
   Keep `HEADING_TOLERANCE_DEG = 5`.
2. **Prepare the turn test.** In `code.py`, temporarily make these changes. Write the old values in your log first.
   * Set `SCAN_ANGLES = [150]`, so that each scan selects "60° right."
   * Set `SCAN_INTERVAL = 1.0`, so that the rover turns frequently.
   * Set `DRIVE_SPEED = 0.5`. This is a lower, temporary value. You set the final value in Step 8.

   > **⚠ CAUTION — ROVER MOVES:** The stop distance is not tuned yet (you tune it in Step 8).
   > Do this test in the middle of your open test area. Walk next to the rover, and be ready to lift it or turn it off.

   Put the rover on the floor, and start it still and flat.
   In the console, look for `drive: turning 60 deg to heading ...` and then `drive: heading now ...`.
3. For five turns, write down the difference between `heading now` and the target. (For example, target 260, heading now 263 → +3.)
4. **Adjust one number at a time.** Put the rover on its stand before each save.

    | What you see | Change |
    | :----------- | :----- |
    | `turn timed out`, and the wheels almost do not move | Increase `TURN_SPEED` by 0.05 |
    | Goes past the target, moves back and forth before it stops | Decrease `TURN_SPEED` by 0.05 |
    | Stops smoothly but misses by 6-8° | Decrease `TURN_SPEED` by 0.05 (the rover moves too far after the motors stop) |
    | No `TURN_SPEED` both moves the rover and stops it cleanly | Increase `HEADING_TOLERANCE_DEG` to 8 |
    | `turn timed out` while the rover turns in the *wrong direction* without end | This is not a tuning problem. See below. |

   **If the rover turns in the wrong direction without end**, the motors and the compass do not agree about the clockwise direction. Do these steps:
   1. Open the website. Turn the rover clockwise by hand. `heading` must go **up**.
   2. If `heading` goes down, correct `MAG_AXIS_SIGN` (Step 4).
   3. If `heading` goes up, your motor wiring turns the rover in the direction opposite to what the code expects.
      In `code.py`, in `turn_toward()`, swap the two `motor_driver.drive()` lines.
      The "spin right" line becomes the "spin left" line, and the "spin left" line becomes the "spin right" line ([Class 5][34]).
5. When `[150]` passes, do the test again with `SCAN_ANGLES = [30]` (60° left).
   Left turns and right turns can be different if one motor is stronger.
6. **Set `TURN_TIMEOUT_S`.** Measure the time of a few 60° turns with the stopwatch.
   Set `TURN_TIMEOUT_S` to approximately three times your slowest turn, and to a minimum of 2 s.
   If your turns take one second or less, the default `3.0` is correct.
7. Put `SCAN_ANGLES` and `SCAN_INTERVAL` back to their usual values. Keep `DRIVE_SPEED` at `0.5` for now.

**Rules for these knobs:**

* Keep `TURN_SPEED` **above** your turn stall point.
  If it is below, turns time out on hard floors and always fail on carpet.
* Keep `HEADING_TOLERANCE_DEG` **between 3 and 10**.
  The code also uses this value to decide "no turn needed."
  Thus, it must stay much smaller than the smallest turn that your scan angles ask for.
  The smallest turn is the gap between `CENTER_ANGLE` and its nearest neighbor in `SCAN_ANGLES`.
  This gap is 30 with the defaults, or 20 if you select `[30, 50, 70, 90, ...]` in Step 7.
  If the value is too large, the rover starts to ignore small turns.

> **⚠ CAUTION — HARDWARE DAMAGE:** Do not make `TURN_TIMEOUT_S` very large (for example, 30 s) to stop timeouts.
> The timeout stops the motors when a wheel is jammed against an object.
> A stuck motor uses its highest current, becomes hot, and can start the DRV8833 shutdown.
> Correct the cause (usually `TURN_SPEED`).

**Done when:** five turns right and five turns left each stop within ±5° of the target (or within your `HEADING_TOLERANCE_DEG`).
Each turn has a maximum of one small back-and-forth correction, and there is no `turn timed out`.
**The rover now:** turns quickly toward a new direction and stops there.

**Ripple effects:** `TURN_SPEED` is independent of `DRIVE_SPEED` and the knob. If you change the drive speed later, your turns do not change.
But a new floor surface, or a much weaker battery, can increase the turn stall point. If timeouts start again, do this step again.


### Step 7 — Scans: reliable scans
**Parameters:** `SETTLE_TIME` (**Important**), `SCAN_ANGLES` (**Useful** / **Taste**).
**Time:** 20 minutes.

**Why.** A scan is only as good as each reading.
The HC-SR04 measures distance from the time of an echo.
If the servo still moves, the echo comes back from a different place.

`SETTLE_TIME` is the pause that lets the servo become stable before the reading.
If it is too short, the readings are random. If it is too long, each scan is slow.
With 5 angles, `SETTLE_TIME = 0.15` gives a scan time of approximately 0.75 s ([Class 2][40]).

**Do this:**

1. **Make the rover scan without movement.**
   Put the rover on its stand. Write the old values in your log, so that you can put them back. Then set these values in `code.py`:

    ```python
    # TEMPORARY values for Step 7. Put the old values back at the end of the step.
    DRIVE_SPEED = 0       # TEMPORARY (Step 7) -- no driving, no reversing
    TURN_SPEED = 0        # TEMPORARY (Step 7) -- no turning
    SCAN_INTERVAL = 1.0   # TEMPORARY (Step 7) -- scan often
    ```

   Now the rover stays still on the floor and scans again and again. Thus, you can put boxes around it.
   Most cycles end with `drive: turn timed out` after `TURN_TIMEOUT_S`. **This is correct** here, because the wheel speed is zero and the heading does not change.
   (When the scan selects straight ahead, you see `drive: no turn needed`.)
   Read only the `scan:` lines.

   > **⚠ CAUTION — ROVER MOVES:** **Do not touch the speed knob in this step.**
   > The knob starts at `DRIVE_SPEED = 0`, but one click changes it to `MIN_SPEED` (`0.3`), and the rover drives away.
   > If this occurs, turn off the rover and start it again.
   > Do not hold a rover with turning wheels to keep it still. Zero speeds are the safe method.
   > Before you save, make sure both values are `0`.
2. **Check the sensor.** Put a cardboard box directly in front of the rover, at 50 cm. Measure the distance with the tape measure.
   Look at the `scan: angle 90 distance_cm ...` lines. They must show approximately 50 (within 2 cm).
   Do the same check at 25 cm and 100 cm.
   The HC-SR04 is accurate from approximately 2 cm to a few meters, and it does not need calibration. This check only shows that it operates correctly.
3. **Check that the scan selects correctly.** Put boxes 30 cm away in all directions *except* one (for example, the `120` direction).
   Five scans in sequence must print `scan: chosen angle 120`.
   Move the gap to a different angle, and do the check again.
4. **Tune `SETTLE_TIME`.** Decrease it by `0.05` at a time, and do item 3 again.
   When readings start to show `None`, or the selected angle becomes wrong or random, increase the value by `0.05` from that point. Keep that value.
   For the SG90, do not use a value below approximately `0.1`.
5. **Select your `SCAN_ANGLES` (taste).** The default five angles are a good balance. Options:
   * **More angles** — for example `[30, 50, 70, 90, 110, 130, 150]`. You get more accurate directions, but slower scans.
   * **Fewer angles** — for example `[45, 90, 135]`. You get faster scans, but less accurate turns.

   Obey these rules:
   * Include `CENTER_ANGLE` (straight ahead).
   * Keep the list symmetrical around `CENTER_ANGLE`.
   * Stay inside the range that you checked in Step 3.
   * Keep the list in order, from left to right.
6. **Put back** the old `DRIVE_SPEED`, `TURN_SPEED`, and `SCAN_INTERVAL` values from your log.

   > **⚠ CAUTION — ROVER MOVES:** Put the rover on its stand before you save. With real speeds, the rover drives away immediately when `code.py` is saved.

**Done when:** the ultrasonic sensor shows values within approximately 2 cm of your tape measure at 25, 50, and 100 cm.
The scan selects the one open gap correctly five times in sequence, at each gap position that you tried.
**The rover now:** looks toward open space reliably, not in random directions.

**Ripple effects:** if you add angles outside 30-150, check the servo aim (Step 3) at those angles.
More angles or a longer `SETTLE_TIME` make each stop longer. You will see this effect in Step 8.


### Step 8 — Behavior: speed, stop distance, and how frequently to look
**Parameters:** `DRIVE_SPEED` (**Important** / **Taste**), `STOP_DISTANCE_CM` (**Critical**), `SCAN_INTERVAL` (**Taste**), status page refresh and chart refresh (**Useful** / **Important**).
**Time:** 30 minutes.

**Why.** This step decides if the rover hits objects. Simple calculations connect the knobs:

* **Stop gap.** The rover checks the distance approximately each 0.05 s, but it moves during all of this time.
  It also continues to move a small distance after the motors stop.
  Thus, it always stops a little *nearer* than `STOP_DISTANCE_CM`. A higher speed gives a larger overshoot.

  When the website is open, a page refresh can add a maximum of 0.25 s of blind driving. At 35 cm/s, that is approximately 9 cm more.
* **Distance between usual scans** = speed × `SCAN_INTERVAL`.
  At 35 cm/s and 3 s, the rover drives approximately 1 m between scans.
* **The knob can go faster than `DRIVE_SPEED`.**
  Your stop distance must be safe at the *highest* speed that the knob can set (Step 10), not only at the start speed.

This diagram shows the stop-distance test, as seen from the side:

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

1. **Select a `DRIVE_SPEED`.** Select a value between your straight stall point + `0.1` and `0.6` (the `MAX_THROTTLE` limit).
   A slower speed is more reliable. The rover has more time to react, and the compass jumps from the motor current are smaller.
   For the first tuning runs, `0.5` is a good, safe value. You can increase the speed when all the other items work.
2. **Stop test.**
   1. Temporarily set `SCAN_INTERVAL = 30.0`, so that the rover does not stop to scan by itself.
   2. Close the website tab.
   3. Point the rover directly at a cardboard box from approximately 1.5 m away.
   4. Start the rover still and flat, and let it drive.
   5. When it stops (you see `drive: obstacle close, distance_cm ...`), measure the gap from its front bumper to the box.
   6. Do three runs. Write down the smallest gap.
3. **First, make the website slower.** Each website request stops the drive loop for approximately 0.25 s.
   The history chart asks for data each 0.2 s. Thus, when the chart is open, the rover is blind for *most of the time*, and no stop distance can correct this.
   * In `history_chart.py`, change `setTimeout(pollHistory, 200)` to `setTimeout(pollHistory, 1000)` (or higher).
   * You can also make the status page slower. In `rover_server.py`, change the `500` in `setInterval(..., 500)` to `1000`.
   * Put the rover on its stand before you save.
4. Do item 2 again **with the website open** on your laptop (it shows the history chart). Do three more runs.
5. **Adjust `STOP_DISTANCE_CM`:**
   * If the gap is correct with the browser closed, but too small *only* with the page open, make the page refresh slower again (item 3). Do this before you change `STOP_DISTANCE_CM`.
   * If the smallest gap (in either test) is less than approximately 8 cm, or the bump switch triggered, increase `STOP_DISTANCE_CM` by 5. Then do the test again.
   * If the smallest gap is more than approximately 25 cm, you can decrease it by 5. Then the rover can go through narrower spaces.
   * Keep it between approximately **20 and 40 cm**.
     Below 20, the rover cannot stop in time at the usual speed.
     Above 40, the rover stops for all objects and has problems in hallways and near furniture.
6. **Set `SCAN_INTERVAL` (taste).** Put it back to a usual value.
   * Shorter (2 s): the rover is careful, looks frequently, and moves in short distances.
   * Longer (5 s): the rover is confident, and drives longer distances in a straight line.

   All values from approximately 2 to 6 s are correct, because the stop-distance check protects the rover between scans.
   A good starting rule: speed × `SCAN_INTERVAL` is approximately 1 m.

> **⚠ CAUTION — ROVER MOVES:** Do each test on the floor. The rover looks only *forward*. No sensor on the rover sees a table edge or a stair.

**Done when:** in each of six stop runs, the rover stops with a gap of a minimum of approximately 8 cm.
Three runs have the browser closed, and three runs have it open. The bump switch never triggers.
**The rover now:** drives, sees a box in front of it, stops before the box, scans, turns away, and continues. It does not touch the box.

**Ripple effects:**

* **If you change `DRIVE_SPEED`, or turn the knob to a higher speed than you tested, do the stop test of this step again.** The overshoot increases with the speed.
* The drive speed is also the **reverse** speed after a safety stop. Thus, if you change it, the reverse distance also changes (Step 9).
* `STOP_DISTANCE_CM` sets the distance at which the IR sensor must trigger (Step 9).


### Step 9 — Safety nets: IR range and back-off distance
**Parameters:** IR sensor trimmer (**Important**), `BACKOFF_S` (**Important**). **Time:** 20 minutes.

**Why.** The IR sensor and the bump switch find the objects that the ultrasonic scan does not find.
Examples are chair legs, soft objects, and objects that appear between two checks.
When one of them triggers, the rover stops, reverses for `BACKOFF_S` seconds at the current drive speed, and then scans.

The IR sensor sends invisible light and looks for the light that comes back.
A very small screw (the trimmer) sets how much light must come back to mean "an object is there."
The IR sensor must be a *backup* that triggers nearer than `STOP_DISTANCE_CM`. It must not be a second main sensor that triggers at the wrong times.

This diagram shows the three zones in front of the rover:

```text
   distance from the front of the rover:

   0 cm       ~10 cm                     STOP_DISTANCE_CM (e.g. 25)
   |-- bump --|-- IR sensor zone --|------ ultrasonic stops here ------>
     (contact)   (backup, close)          (main, farther out)
```

**Do this:**

1. **IR range.** Put the rover on its stand, with its code running.
   Slowly move a piece of white paper toward the IR sensor. Write down where it triggers.
   (The LED on the module comes on, and `SAFETY: IR sensor near-field obstacle` prints.)
   Turn the trimmer screw with the small screwdriver until the sensor triggers at approximately **8-12 cm**.
   This must be clearly less than your `STOP_DISTANCE_CM`.
   On most modules, a counter-clockwise turn decreases the range. Check your module ([Pre-Class IR sensor homework][39]).
2. Do the same check with a dark object.
   Dark objects send back less IR light, so they trigger nearer. This is normal. Make sure the sensor still triggers.
3. **Floor check.** Let the rover drive in the test area for a minute, with no object in front of it.
   If it makes an emergency stop with no object near, the IR sensor sees the floor. (Shiny floors cause the most problems.)
   Turn the trimmer to decrease the range, or tilt the sensor up a little.
4. **Back-off distance.** The back-off distance ≈ your speed from Step 5 × `BACKOFF_S`.
   At 35 cm/s and 0.3 s, that is approximately 10 cm.
   Push the bump switch by hand while the rover drives, and measure how far it reverses.
   The target is approximately **5-15 cm**. This is enough to move away fi.rom the obstacle for a turn.
   But it is not so much that the rover hits an object behind it.
   Adjust `BACKOFF_S` in steps of 0.1.

> **⚠ CAUTION — ROVER MOVES:** Keep `BACKOFF_S` short (0.5 s or less is a good rule).
> The rover has **no rear sensor**, so it reverses blind. If `BACKOFF_S` is too long, the rover hits walls and furniture behind it.

**Done when:** the IR sensor triggers at approximately 8-12 cm for a white object, and also triggers for a dark object. It never triggers on an open floor. The rover reverses 5-15 cm after a bump.
**The rover now:** almost never touches an object. When it touches an object, it moves back cleanly and finds a new direction.

**Ripple effects:** if you change `DRIVE_SPEED` (or drive faster with the knob), the back-off distance changes. Do item 4 again.
If you change `STOP_DISTANCE_CM`, you possibly must set the IR range again, so that it stays below `STOP_DISTANCE_CM`.


### Step 10 — Preferences: make the rover yours (optional)
**Parameters:** **Taste**, with a few firm limits. **Time:** 15-30 minutes, only if you want.

If you stay within the limits below, these values have a small effect on how well the rover avoids obstacles.
(The website refresh and the chart refresh *do* have an effect on safety. Thus, you set them in Step 8.)

* **`DRIVE_SPEED`, `SCAN_INTERVAL`, `SCAN_ANGLES`** — these values give the rover its "personality": careful and quick to react, or bold with long movements.
  If you change them, remember the ripple effects in Steps 7-9.
* **Speed knob (`speed_knob.py`): `MIN_SPEED`, `MAX_SPEED`, `SPEED_STEP`.** These have two firm limits. They are not taste:
  1. Keep `MIN_SPEED` **above your straight stall point** from Step 5. If not, the rover stops and makes a hum at the lowest knob position.
  2. The knob already stops at `MAX_THROTTLE` (`0.6`), although `MAX_SPEED` is `0.9`.
     If you increase `MAX_SPEED`, it has no effect unless you also increase `MAX_THROTTLE` (see the Step 5 caution).

  Then test again at the highest knob speed.
  You cannot do this with the knob, because each restart sets the knob back to `DRIVE_SPEED`, and each Step 8 run starts with a restart. Do these steps:
  1. Temporarily set `DRIVE_SPEED = 0.6` (the highest knob speed, `MAX_THROTTLE`).
  2. Do the Step 8 stop test and the Step 9 back-off check again.
  3. If necessary, adjust `STOP_DISTANCE_CM` and `BACKOFF_S`.
  4. Put `DRIVE_SPEED` back to its old value.

  At the highest speed, also look at `heading` on the website when the motors start.
  More motor current gives a larger magnetic jump.
  If turns start to stop off target, set `MAX_SPEED` *below* `MAX_THROTTLE` (for example `0.5`-`0.55`).
  A change from `0.9` to `0.8` has no effect, because the knob already stops at `0.6` ([Class 6][38]).
  If you do not want to test again, do not turn the knob past the speed that you tested in Step 8.
* **Website refresh and chart refresh** — you set these in Step 8, item 3.
  If you change them again, remember: a faster refresh gives more blind time for the rover. Do the Step 8 page-open stop test again.
* **TFT `REFRESH_S` (`tft_status.py`)** — `0.2` is smooth. Do not set it much lower.
  The screen update is slow, and the rover does not look for obstacles while it updates the screen.

**Done when:** you like how the rover looks and moves.
If you changed `DRIVE_SPEED`, or you use the knob above it, make sure you did the Step 8 stop test again at your highest speed.
Also make sure you did the Step 9 back-off check again at that speed.


### Step 11 — Final test: the 5-minute arena run
**Parameters:** none. This step checks all the values together.
**Time:** 15 minutes, and a 5-minute check after each battery replacement.

**Do this:**

1. Make an arena: a 2 m × 2 m area with walls or boxes around it.
   Put 3-4 cardboard boxes inside it as obstacles.
2. Start the rover still and flat in the middle. Start the stopwatch.
3. For 5 minutes, count these events on paper:

    | Event | Count | Target for a tuned rover |
    | :---- | :---- | :----------------------- |
    | Bump-switch contacts (the rover touched an object) | | 0-2 |
    | Rescues (you had to lift the rover or free it) | | 0-1 |
    | Turns that clearly went in the wrong direction | | 0-1 |
    | Stuck in a corner for more than 30 s | | 0 |

4. If you did not get a target, find the matching symptom in [8.7 Tuning troubleshooting][45]. Do only that step again.
5. **Save your tuned numbers in two places:**
   1. Copy `code.py`, `rover_server.py`, `motor_driver.py`, `wheel_odometry.py`, `history_chart.py`, `speed_knob.py`, and `tft_status.py` from `CIRCUITPY` to a laptop folder with the name `rover-tuned`.
   2. Copy your changed values into the matching files in `full_build/src/pico/`.
      Then a later `uv run deploy.py rover --overwrite` does not put the starting guesses back.

**Done when:** the rover completes a 5-minute arena run and gets all four targets. **The rover is tuned.**
It drives with purpose, stops before obstacles, looks, turns quickly to open space, and continues for minutes without your help.


### 8.6 When must I tune again?

| Change | Do again |
| :---------------- | :--- |
| New battery | Step 1, then a 5-minute Step 11 run |
| New floor (tile ↔ carpet) | Steps 5, 6, 8 |
| IMU, battery, or motors moved, or steel added near the IMU | Step 4 (calibrate again), then Step 11 |
| Servo horn installed again, or sensor hit | Step 3, then Step 7 |
| `DRIVE_SPEED` changed, or you drive faster with the knob than you tested | Step 8 stop test, Step 9 back-off |
| `TURN_SPEED` or `HEADING_TOLERANCE_DEG` changed | Step 6 turn test |
| You ran `deploy.py rover --overwrite` | Make sure your tuned values are still in the files on `CIRCUITPY` |
| Only the code logic changed, no constants | Nothing. But do Step 11 to make sure. |


### 8.7 Tuning troubleshooting

| Symptom | Possible cause | Go back to |
| :------ | :----------- | :--------- |
| Turns miss, move back and forth, or print `turn timed out` | `TURN_SPEED` too high or too low, or `HEADING_TOLERANCE_DEG` too small | Step 6 (and Step 4 if `heading` looks wrong on the website) |
| The rover turns in the wrong direction until `turn timed out` | The motor direction and the compass do not agree about clockwise | Step 6, item 4 |
| Turns go in the wrong direction by a fixed angle each time | The servo aim is wrong | Step 3 |
| `heading` disagrees with the phone compass from the start, and moves back after a turn by hand | `MAG_AXIS_SIGN` is wrong | Step 4, axis check |
| `heading` was correct, but now it is wrong by the same angle in all places | The IMU, battery, or motors moved after calibration | Step 4, calibrate again |
| `heading` is a few degrees wrong at start-up, and slowly corrects in one minute | The rover was tilted at start-up | Start the rover again, still and flat. (Turns continue to work, because they use heading *changes*.) |
| `heading` jumps more than approximately 15-20° when the motors start | The magnetic field of the motor current. Calibration cannot remove it. | Step 4, item 4 (move the IMU farther away) |
| `heading` is wrong only near some furniture or in some places | Steel changes the magnetic field of the Earth | Test in a different place. This is a real-world limit. |
| Hits boxes from the front | The stop distance is too small for your speed or page refresh | Step 8 |
| Hits boxes at an angle, or thin/soft objects | The ultrasonic sensor cannot see them | Step 9 (IR range), or accept it as a sensor limit |
| Moves back into objects | `BACKOFF_S` is too long | Step 9 |
| Stops again and again with no object near | The IR sensor sees the floor, or `STOP_DISTANCE_CM` is too large | Step 9 (IR floor check), then Step 8 |
| Drives but never stops to scan | `SCAN_INTERVAL` is still at a test value, or `STOP_DISTANCE_CM` is too small | Step 8 |
| Always selects angle 90, with all objects around it | Each scan reading is `None`, so the code uses `CENTER_ANGLE` | Check the HC-SR04 wiring (divider on `ECHO`, `VCC` on the 5V rail), then Step 7 |
| The console shows many `None` distances during a scan | `SETTLE_TIME` is too short, or the sensor points at an object out of range | Step 7 |
| Reacts late to the bump switch or IR sensor only while the website is open | The 0.25 s website pause | Step 8, item 3 (make the refresh slower), or close the tab |
| The rover jerks or stops at the low end of the knob | `MIN_SPEED` is below your straight stall point | Step 10 |
| At the highest knob speed, `heading` jumps and turns stop off target | More motor current gives a larger magnetic jump | Step 10 (set `MAX_SPEED` below `MAX_THROTTLE`, e.g. `0.5`) |
| The two motors stop suddenly during a run | DRV8833 overcurrent shutdown (jammed wheel) | Free the wheel. Turn off the battery, wait approximately 5 s, and turn it on. Make sure `TURN_TIMEOUT_S` is not very large (Step 6). |
| All behaviors became worse after some time | The battery is weak | Step 1 |


## 9. Checklist
* [ ] Breadboard planned: Pico + DRV8833 at one end, buck converter at the other end.
* [ ] Top `+` rail has the label 5V. Bottom `+` rail has the label 3.3V. The two `-` rails are connected as GND.
* [ ] Chassis assembled. Motor leads and switch leads soldered.
* [ ] All parts installed in their final positions (IMU far from the motors and the battery).
* [ ] Buck converter set to 5.0 V *before* you connect it to the 5V rail.
* [ ] Power wiring done. 9V goes only to buck `IN+` and DRV8833 `VM`. Common GND for all parts.
* [ ] Power-on check: 5V rail 4.8-5.2 V, 3.3V rail 3.2-3.4 V.
* [ ] Signal wiring done as the [wiring table][26] shows. `SLP` on 3.3V. Divider on `ECHO`. TFT `RST` on `GP22`.
* [ ] Laptop set up: `setup-test-laptop.sh` / `.ps1` ([setup-test-laptop.sh][31], [setup-test-laptop.ps1][32]).
* [ ] Software installed: `uv run deploy.py rover` ([deploy.py][20]).
* [ ] `settings.toml` edited with your own network name and password ([settings.toml][17]).
* [ ] Rover starts and shows `drive:` / `scan:` lines on its stand.
* [ ] Compass calibrated: `uv run deploy.py tool mag_calibration`, equal spans, axis check passed, `MAG_OFFSET` pasted into `rover_server.py`, `uv run deploy.py restore` ([mag_calibration.py][24]).
* [ ] Test of each part passed: `uv run deploy.py test`, then `restore` ([device_test.py][22]).
* [ ] Test of the full rover passed: `uv run test/system_test.py` ([system_test.py][23]).
* [ ] Orientation viewer follows the rover: `uv run src/laptop/wireframe.py` ([wireframe.py][21]).
* [ ] First floor run: drive, stop, scan, turn, and again.
* [ ] Tuning Session A done (Steps 0-5): power, installation of parts + `SLOTS_PER_REV`, servo aim, compass, motor stall points.
* [ ] Tuning Session B done (Steps 6-11): turns, scans, stop distance, IR + back-off, preferences, 5-minute arena run.
* [ ] Tuned files saved on your laptop (`rover-tuned` folder) and copied into `full_build/src/pico/`.



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
