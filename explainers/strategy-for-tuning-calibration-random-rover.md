# Strategy for Tuning and Calibrating the Random Rover

Your Random Rover works — it drives, stops, sweeps its sensor, turns, and drives again. But
"works" and "works *well*" are different things. Maybe its turns overshoot and wiggle back. Maybe
it taps walls before it stops. Maybe it prints `turn timed out` on carpet. None of that means the
code is wrong. It means the rover is still running on *starting guesses* — numbers somebody picked
before your particular motors, battery, servo, and floor ever existed.

This document shows you how to replace those guesses with numbers that fit *your* rover. The first
half explains what tuning is, which numbers matter, and what to expect. The second half is a
step-by-step procedure you can follow from a freshly built rover to a tuned one.


## Part 1 — Understanding the Job


### What are tuning, calibration, and setting parameters — and why bother?

**Status quo.** Every program you wrote for the rover has a block of `ALL_CAPS` constants near the
top: `DRIVE_SPEED = 0.6`, `STOP_DISTANCE_CM = 25`, `MAG_OFFSET = (0.0, 0.0, 0.0)`, and so on.
Each one is a knob that controls how the rover behaves. The lesson scripts gave you sensible
starting values.

**Problem.** Starting values are written for an *average* rover. Yours isn't average. Its IMU sits
a particular distance from a particular motor. Its servo's gears are a little off center. Its 9V
battery is fresher or more tired than someone else's. Its test floor is tile, or carpet. Each of
those differences nudges the rover away from what the default numbers expected, and the
differences add up.

**Solution.** Measure your actual rover and adjust the knobs to match. There are three flavors of
this work, and it helps to keep them apart:

1. **Calibration** — measuring a fixed fact about your hardware and typing it in. There is one
   right answer; you're finding it. Example: `MAG_OFFSET`, the magnetic "junk" your own rover
   carries around. You measure it once and paste it in.
2. **Tuning** — adjusting a number that trades one good thing against another, by testing and
   watching. There's a *best* answer for your rover, not a single correct one. Example:
   `TURN_SPEED` — too slow and the rover can't turn on carpet, too fast and it overshoots.
3. **Setting preferences** — choosing a number purely by taste. Nothing breaks either way.
   Example: `SCAN_INTERVAL`, how often the rover stops to look around when nothing is in its way.

Why it matters: a rover with good code and bad numbers behaves like a rover with bad code. Tuning is
where your robot stops being a copy of the class demo and starts being *yours*.


### Every parameter that needs your attention

The table below lists every knob on the finished rover, where it lives, its starting value, and
how much it matters. The **Importance** column uses five levels:

* **Critical** — get this wrong and the rover misbehaves badly, or hardware can be damaged.
* **Important** — noticeably changes how well the rover avoids obstacles.
* **Useful** — a small improvement; worth doing once the important ones are done.
* **Taste** — your preference; nothing breaks either way.
* **Leave alone** — already tuned in class, or doesn't affect driving. Don't touch it today.

| Parameter | Where it lives | Start value | What it controls | Importance | Step |
| :-------- | :------------- | :---------- | :--------------- | :--------- | :--- |
| 9V battery charge | the battery | fresh | Motor strength, and the Pico's power through the buck converter | **Critical** | 1 |
| Buck converter output | buck converter trimpot (if it has one) | 5 V | Power to the Pico's `VSYS`, the servo, and the HC-SR04 | **Critical** (can damage parts) | 1 |
| Part mounting | the chassis | — | Whether the IMU, sensor, servo, bumper, and IR sensor stay put | **Critical** | 2 |
| `min_pulse` / `max_pulse` | `class-5-code.py`, `servo.Servo(...)` line | `500` / `2500` | How accurately a commanded servo angle matches the real angle | **Important** | 3 |
| `CENTER_ANGLE` | `class-5-code.py` | `90` | Which servo angle means "straight ahead" | **Important** | 3 |
| `MAG_OFFSET` | `rover_server.py` | `(0.0, 0.0, 0.0)` | Removes your rover's own magnetic field from the compass | **Critical** | 4 |
| `MAG_AXIS_SIGN` | `rover_server.py` (and the calibration program) | `(-1, 1, 1)` | Makes the compass axes agree with the gyro's axes | **Critical** | 4 |
| Boot still and flat | how you power on | — | Gyro bias and starting compass heading, measured at every boot | **Critical** (a habit, not a number) | 4 |
| `MAX_THROTTLE` | `motor_driver.py` | `0.6` | Hard ceiling on every motor command, including `DRIVE_SPEED` and `TURN_SPEED` | **Critical** (can damage parts) | 5 |
| `TURN_SPEED` | `class-5-code.py` | `0.45` | How hard the rover spins during a compass turn | **Critical** | 6 |
| `HEADING_TOLERANCE_DEG` | `class-5-code.py` | `5` | How close to the target heading counts as "arrived" | **Important** | 6 |
| `TURN_TIMEOUT_S` | `class-5-code.py` | `3.0` | When to give up on a turn that never arrives | **Useful** (a safety limit) | 6 |
| `SETTLE_TIME` | `class-5-code.py` | `0.15` | How long the servo gets to stop before a distance reading | **Important** | 7 |
| `SCAN_ANGLES` | `class-5-code.py` | `[30, 60, 90, 120, 150]` | Which directions the rover looks in each scan | **Useful** / **Taste** | 7 |
| `DRIVE_SPEED` | `class-5-code.py` | `0.6` | Forward speed — and, hidden inside, reverse speed after a safety stop | **Important** / **Taste** | 8 |
| `STOP_DISTANCE_CM` | `class-5-code.py` | `25` | How close an obstacle gets before an emergency stop and rescan | **Critical** | 8 |
| `SCAN_INTERVAL` | `class-5-code.py` | `3.0` | How often the rover stops to look when nothing is close | **Taste** | 8 |
| IR sensor trimmer | small screw on the IR module | — | How far away the IR sensor triggers | **Important** | 9 |
| `BACKOFF_S` | `class-5-code.py` | `0.3` | How long the rover reverses after a bump or IR stop | **Important** | 9 |
| Stretch 1: `MIN_SPEED` / `MAX_SPEED` / `SPEED_STEP` | `class-6-code-1.py` | `0.3` / `0.9` / `0.05` | The knob's speed range and step size | **Taste** (with limits) | 10 |
| Status page refresh | `rover_server.py`, `STATUS_PAGE` (`500` ms) | `500` | How often the website asks for new data — each request pauses the drive loop | **Useful** | 8 |
| Stretch 2 chart refresh | `class-6-code-2.py`, `setTimeout(pollHistory, 200)` | `200` ms | How often the history chart asks for new data — each request pauses the drive loop | **Important** (only if Stretch 2 is installed) | 8 |
| Stretch 3: `REFRESH_S` | `class-6-code-3.py` | `0.2` | How often the TFT screen redraws | **Taste** | 10 |
| `MAHONY_KP`, `MAHONY_KI` | `rover_server.py` | `2.0`, `0.05` | How the IMU filter blends gyro, gravity, and compass | **Leave alone** | — |
| `CAL_SAMPLES`, `STILL_GYRO`, `STILL_ACCEL`, `BIAS_ALPHA`, `GRAVITY` | `rover_server.py` | as set in Class 4 | Automatic gyro bias correction | **Leave alone** | — |
| `SLOTS_PER_REV`, `WHEEL_DIAMETER_MM` | `wheel_odometry.py` | `20`, `67` | Wheel speed shown on the website | **Leave alone** (set in Class 3; website only) | — |
| `SAMPLE_SECONDS` | `wheel_odometry.py` | `0.25` | How long each website request counts wheel ticks — which is also how long the drive loop goes blind per request | **Leave alone** (raising it makes the blind pause longer) | — |
| `KI`, `MAX_TRIM`, `BASE_THROTTLE` | `straight_drive.py` | from Class 3 | Straight-line wheel balancing | **Leave alone** — `class-5-code.py` doesn't use it | — |
| `SECONDS_PER_90_DEGREES`, `SECONDS_PER_CM` | Class 3 timed-move code | — | Class 3's timed turns | **Leave alone** — replaced by compass turns | — |

Notice that the list of things that really matter is shorter than the table looks. Most of the
bottom rows are either already tuned or aren't used by the rover at all.


### The strategy: build from the ground up

A rover is a stack of layers, and each layer depends on the ones below it. Tuning a high layer
before the low ones are right is like leveling a picture frame on a crooked wall — you'll just have
to do it again.

```text
                +------------------------------+
   Step 10      |  PREFERENCES (taste)         |  speed knob, refresh rates
                +------------------------------+
   Steps 8-9    |  BEHAVIOR                    |  drive speed, stop distance,
                |                              |  scan timer, IR range, backoff
                +------------------------------+
   Steps 6-7    |  TURNING and SEEING          |  turn speed, heading tolerance,
                |                              |  servo settle time, scan angles
                +------------------------------+
   Steps 3-5    |  SENSORS and MOTORS          |  servo aim, compass calibration,
                |                              |  motor stall points
                +------------------------------+
   Steps 1-2    |  POWER and MECHANICS         |  battery, 5 V rail, everything
                |                              |  bolted down
                +------------------------------+
```

Five rules make this work:

1. **Bottom up.** Finish each step before starting the next. The step order below is chosen so
   that nothing you tune later can undo something you tuned earlier — with the few exceptions
   called out as **Ripple effects**.
2. **One change at a time.** Change one number, test, write the result down. Change two numbers at
   once and you can't tell which one helped.
3. **Repeat each test three times.** One good run can be luck. Three good runs is a result.
4. **Write everything down.** Your tuning log (below) is your memory. When something breaks
   tomorrow, it tells you what worked today.
5. **Know when to stop.** Each step has a **Done when** line. When you hit it, move on — chasing
   perfection on one step wastes time the next steps need.

Here's how the knobs map onto the rover's stop-look-go loop, so you can see what each one touches:

```text
   +--> DRIVE forward at DRIVE_SPEED (capped by MAX_THROTTLE)
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


### What improvement should you expect?

Be realistic. Tuning makes the rover *reliable at what it already does*; it doesn't make it smarter.
It is still a reactive, insect-brained robot (see [What Is the Random Rover?][01]).

Here's a fair before-and-after for a typical rover:

| Behavior | Untuned (typical) | Well tuned (target) |
| :------- | :---------------- | :------------------ |
| Compass turns | Overshoot and wiggle, sometimes `turn timed out` | Land within about ±5° of target, one clean stop, no timeouts |
| Heading on the website | Off by tens of degrees, creeps | Follows a hand turn by about +90 per quarter turn; holds within a few degrees for a minute |
| Stopping for a box in its path | Sometimes touches it | Stops with a visible gap, every time, at your chosen speed |
| Bump switch contacts in a 5-minute run | Several | 0 to 2 |
| Times you have to rescue it in 5 minutes | Several | 0 to 1 |

What tuning **won't** fix — these are limits of the hardware and design, not your numbers:

* **Thin, soft, or angled things.** The HC-SR04 hears echoes. Thin chair legs, fabric, and walls hit
  at a steep angle can reflect sound away, so the sensor doesn't see them. The IR sensor and bump
  switch are the backups for exactly this.
* **Drop-offs.** Nothing on the rover looks *down*. It will drive off a table edge or down a stair.
  Always test on the floor.
* **Dead ends.** If every direction is blocked, the rover picks the "least blocked" one, drives a
  few centimeters, stops again, and repeats. That's the design, not a tuning problem.
* **Magnetic trouble spots.** Steel desks, radiators, and rebar in the floor bend Earth's field.
  Turns may land off target near them no matter how well you calibrated.
* **The browser pause.** While the rover's website is open, each page refresh can freeze the drive
  loop for about 0.25 s (see the note at the end of [Class 5, Phase 3][02]). You'll test with the
  page closed *and* open so your numbers work either way.
* **Battery fade.** A 9V battery weakens as it drains. Closed-loop compass turns shrug this off, but
  straight-line speed and stopping distance slowly change.


## Part 2 — The Step-by-Step Procedure


### How to use this procedure

Start at Step 0 and go in order. Each step has the same layout:

* **Parameters** — what you're setting, and how much it matters
* **Time** — a realistic estimate for one student
* **Do this** — the numbered actions
* **Done when** — the exact test that tells you the step is finished
* **Ripple effects** — what else this step can change, and when to come back

**Total time: about 4 to 4.5 hours**, which is more than one class. A good split:

| Session | Steps | Time |
| :------ | :---- | :--- |
| Session A | 0 – 5 (power, mounting, servo, compass, motors) | about 1.75 hours |
| Session B | 6 – 11 (turning, seeing, behavior, safety nets, preferences, final test) | about 2 to 2.5 hours |

If you have to stop partway, stop *between* steps, and write down which step you finished.

**Warning labels used below:**

> **⚠ DANGER TO HARDWARE** — getting this wrong can permanently damage a part.
>
> **⚠ CAUTION** — the rover can move unexpectedly, fall, or hit something.


### Step 0 — Get Ready: tools, test space, tuning log

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
| A "rover stand" — a cup, box, or block that lifts the wheels off the table | 2, 3, 4 | Lets you run code on the bench without the rover driving away |
| 4-6 cardboard boxes (shoebox size or bigger) | 7, 8, 11 | Obstacles the ultrasonic sensor can see well |
| Laptop with Mu or Thonny, USB cable | all | Edit code, read the serial console |
| Laptop or phone with a browser | 4, 8 | The rover status website, `http://192.168.4.1:5000` |
| Paper and pen (or your build journal) | all | Your tuning log |

**Do this:**

1. **Back up your working code.** Copy `code.py`, `rover_server.py`, `motor_driver.py`, and
   `wheel_odometry.py` from `CIRCUITPY` to a folder on your laptop named `rover-before-tuning`. If
   tuning goes wrong, you can always go back.
2. **Set up a test space** on the floor, at least 2 m × 2 m, away from table edges, stairs, and big
   steel furniture. Use a wall or a row of boxes as a boundary.
3. **Start a tuning log.** One row every time you change a number:

   | Step | Parameter | Old value | New value | Test | Result (3 runs) | Keep? |
   | :--- | :-------- | :-------- | :-------- | :--- | :-------------- | :---- |
   | 6 | `TURN_SPEED` | 0.45 | 0.40 | `[150]` turn test | +3, +4, +2 | yes |

4. **Learn the two safety habits** you'll use all day:
    * > **⚠ CAUTION** — saving `code.py` restarts your program *immediately*. If the rover code is
      > on the board and the rover is on the table, it will drive off the edge. **Put the rover on
      > its stand before you save any file.**
    * Know where the battery clip is. Pulling the 9V battery clip is your emergency stop.

**Done when:** your code is backed up, your log page is ready, you have your tools, and the test
space is clear.


### Step 1 — Power: a strong battery and a correct 5 V rail

**Parameters:** 9V battery charge (**Critical**), buck converter output (**Critical**).
**Time:** 10 minutes.

Everything above this step depends on steady power. A tired battery makes motors weak, makes the
Pico brown out (reset) when the motors start, and changes how far the rover coasts. You can't tune
around bad power.

**Do this:**

1. With the battery clip unplugged, set the multimeter to DC volts and measure the 9V battery.
   Write it in your log. A fresh alkaline 9V reads about 9 V or a little more. If it reads under
   about 8 V, use a fresh one for tuning.
2. Plug the battery back in, USB cable unplugged. Put the rover on its stand.
3. Measure between the Pico's `VSYS` pin and `GND` (the buck converter's output). It should read
   close to 5 V — roughly 4.8 V to 5.2 V.
4. Now watch the meter while the motors run (the rover code will run the wheels in the air on the
   stand). The reading should stay above about 4.7 V. If it dips hard, or the Pico resets when the
   motors start, the battery is too weak — swap it. If a fresh battery still dips, add the 470-1000
   µF capacitor across `VM`/`GND` at the DRV8833 described in the [Class 3 troubleshooting guide][03].

> **⚠ DANGER TO HARDWARE** — the Pico's `VSYS` input is rated for **5.5 V at most** (see the
> [Pico 2 W datasheet][04]). The servo and HC-SR04 share that same 5 V rail, and they're 5 V parts
> too (see [Class 2][08]), so too much voltage can damage all three at once. If your buck converter reads
> **above 5.5 V**, unplug the battery right away and don't reconnect the Pico until it's fixed. If
> your buck converter has an adjustment screw (a trimpot), **disconnect its output from the Pico
> before turning it**, set it to 5.0 V with the meter, then reconnect. Turning a trimpot while the
> Pico is attached can spike the voltage and destroy the board.

**Done when:** battery reads about 9 V at rest, `VSYS` reads 4.8-5.2 V at rest and stays above about
4.7 V with the motors spinning, and the Pico doesn't reset when motors start.

**Ripple effects:** every motor-related number you tune later (Steps 5, 6, 8, 9) was tuned *on this
battery*. When you swap batteries, re-run the quick checks in Step 11.


### Step 2 — Mechanics: bolt everything down where it will stay

**Parameters:** part mounting (**Critical**). **Time:** 15 minutes.

Calibration measures where things *are*. If a part moves after you calibrate it, the calibration is
wrong. So first, put every part in its final position and make it stay there.

**Do this:**

1. **IMU:** mounted where it will live for good, as far from the motors and battery as the chassis
   allows, firmly stuck down. Press on it — it must not shift.
2. **Battery:** in its final spot, held down. (The battery counts as "magnetic junk" for the
   compass. If it moves, the compass calibration in Step 4 goes stale.)
3. **Ultrasonic sensor on the servo:** the sensor is firm on the servo horn, and the horn is firm on
   the servo shaft.
4. **Bump switch:** the lever sticks out past the front of the chassis, so any contact presses it.
   Press it with a finger: it should click.
5. **IR sensor:** fixed, facing forward, low on the chassis, tilted slightly up so it doesn't see
   the floor.
6. **Wires:** nothing dangles near a wheel. Nothing is loose on the breadboard. Blu Tack holds the
   breadboard, DRV8833, buck converter, and battery firmly.
7. **Wheels:** spin each wheel by hand. It should turn freely without rubbing.
8. **Quick function check** with the rover code running on the stand: press the bump switch and see
   `SAFETY: bump switch contact`; wave a hand in front of the IR sensor and see
   `SAFETY: IR sensor near-field obstacle`.

**Done when:** you can pick up the rover and gently shake it, and nothing moves, rattles, or comes
loose — and both safety sensors fire when triggered by hand.

**Ripple effects:** if you ever remount the IMU, move the battery, or add steel near the IMU, go
back to Step 4 and recalibrate the compass. If you reseat the servo horn, redo Step 3.


### Step 3 — Servo aim: make "90" mean straight ahead

**Parameters:** `CENTER_ANGLE` (**Important**), `min_pulse` / `max_pulse` (**Important**).
**Time:** 20 minutes.

This matters more than it looks. When the scan picks angle `150`, the rover turns `150 - 90 = 60`
degrees right. That math assumes the servo *really* points 60° right when told `150`. If the servo
is off by 10°, every turn is off by 10° — and no amount of compass tuning fixes it, because the
compass is carefully steering toward the wrong target.

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
2. Save this short test program as `code.py` (temporarily — your rover code is backed up from
   Step 0):

   ```python
   # servo-check.py -- save as code.py TEMPORARILY; put class-5-code.py back when done.
   # Points the scan servo at the rover's own scan range so you can check its aim.
   import time
   import board
   import pwmio
   from adafruit_motor import servo

   MIN_PULSE = 500    # copy the values from your class-5-code.py servo.Servo(...) line
   MAX_PULSE = 2500
   CHECK_ANGLES = [90, 30, 90, 150]  # only the rover's range -- no need to push to 0 or 180

   pwm = pwmio.PWMOut(board.GP8, duty_cycle=0, frequency=50)
   scan_servo = servo.Servo(pwm, min_pulse=MIN_PULSE, max_pulse=MAX_PULSE)

   while True:
       for angle in CHECK_ANGLES:
           scan_servo.angle = angle
           print("servo at", angle)
           time.sleep(3)
   ```

3. **Check center first.** When it prints `servo at 90`, does the sensor point straight along the
   nose? If it's off by more than about 5°, the best fix is mechanical: pull the horn off the shaft
   and push it back on one tooth over, so 90 lands as close to straight as possible. Only if you
   can't get it close that way, change `CENTER_ANGLE` in `class-5-code.py` to the angle that *does*
   look straight (for example `95`), and shift every value in `SCAN_ANGLES` by the same amount. If
   you do, also change `CHECK_ANGLES` in the test program to `CENTER_ANGLE` and `CENTER_ANGLE` ± 60
   (for example `[95, 35, 95, 155]`) for the rest of this step.
4. **Check the span.** At `30` and `150` (or `CENTER_ANGLE` ± 60), the sensor should point about 60° to each side of
   straight ahead. If both sides fall short (for example, only 50° each way), widen the pulse range
   a little — `MIN_PULSE` down by 50 and `MAX_PULSE` up by 50. If both sides go too far, narrow it
   the same way. Change them in steps of 50, test after each change.
5. When the aim is right, copy the final `min_pulse=` and `max_pulse=` values into the
   `servo.Servo(...)` line of `class-5-code.py`, and put `class-5-code.py` back as `code.py`.

> **⚠ DANGER TO HARDWARE** — if the servo **buzzes, grinds, or strains** at any angle, it's being
> pushed past its physical stop. Unplug the battery right away and narrow the pulse range. A servo
> left straining will overheat and strip its plastic gears. This is why the test only visits 30 to
> 150, the range the rover actually uses.

**Done when:** at `CENTER_ANGLE` (normally `90`) the sensor points straight ahead within about 5°,
at `CENTER_ANGLE` ± 60 (normally `30` and `150`) it points about 60° left and right within about 5°,
and the servo is silent (no buzzing) at every stop.

**Ripple effects:** if you later change `SCAN_ANGLES` to include angles outside 30-150 (Step 7),
re-check the aim at those new angles.


### Step 4 — Compass: calibrate the magnetometer and check the heading

**Parameters:** `MAG_OFFSET` (**Critical**), `MAG_AXIS_SIGN` (**Critical**), boot still and flat
(**Critical** habit). **Time:** 25 minutes.

The compass steers every turn. If it's wrong, turns are wrong, and nothing you tune later can make
up for it. You already did this once in [Class 5, Phase 1][02]; now you're doing it again with the
rover in its *final* shape, because Step 2 may have moved things. (Why the rover's own magnets
matter at all is explained in [What Is an IMU, and What Does a Mahony Filter Do?][05].)

**Do this:**

1. Take the fully assembled rover — battery in, everything mounted — to a spot away from steel: not
   on a metal desk, not near desk legs, radiators, or piles of laptops.
2. Save `class-5-mag-calibration.py` as `code.py`. When it says `GO`, slowly turn and tumble the
   rover through every orientation for the full 30 seconds: spin it flat, roll it onto each side,
   tip it nose-up and nose-down, even upside down.
3. Copy the printed `MAG_OFFSET = (...)` line into your log. Check the **spans**: the three numbers
   should be roughly equal (for example `(0.98, 1.02, 0.95)`). If one is much smaller, you didn't
   tumble enough — run it again.
4. Do the **axis check** with a phone compass (the program keeps printing `mx my mz`):
    * X arrow on the board pointing north → `mx` clearly positive
    * Y arrow pointing north → `my` clearly positive
    * lying flat (northern hemisphere) → `mz` negative

   If one comes out backwards, flip that entry of `MAG_AXIS_SIGN` in *both* files and rerun.
5. Paste your `MAG_OFFSET` (and `MAG_AXIS_SIGN`, if you changed it) into `rover_server.py`. Put
   `class-5-code.py` back as `code.py`.
6. **Boot the rover sitting still and flat on the stand.** At every power-up, `rover_server.py`
   spends about 2 seconds measuring the gyro's bias and reads the compass once to set its starting
   heading. If the rover is moving or tilted during those seconds, the heading starts out wrong.
   Make this a habit: *set it down, then power it on, then hands off for 3 seconds.*
7. Do the **heading check** from [Class 6][06] with the rover website open:
    * turn the rover clockwise by hand about a quarter turn → `heading` goes **up** by about 90
    * leave it still for a minute → `heading` holds within a few degrees
    * phone compass next to it → roughly matches (within 10-20° is fine; if your IMU is mounted
      sideways it may be off by a fixed 90° or so, which is also fine — turns only use *changes* in
      heading)
8. **Motor-interference check.** Still on the stand, watch `heading` as the wheels start spinning.
   A jump of a few degrees that settles back is normal. A jump of more than about 15-20° means the
   IMU is too close to the motors — move it farther away (higher, on a standoff) and **restart this
   step from item 1**.

**Done when:** spans are roughly equal, all three axis checks pass, a clockwise quarter turn raises
`heading` by about 90, `heading` holds steady for a minute, and motor start-up moves it by less
than about 15°.

**Ripple effects:** this calibration is only good while *nothing magnetic moves* relative to the
IMU. Moving the IMU, the battery, or the motors — or adding a steel screw or bracket near the IMU —
means redoing this step. Changing code or speed does **not** require recalibrating.


### Step 5 — Motors: find the stall points and measure your real speed

**Parameters:** `MAX_THROTTLE` (**Critical**), and measurements you'll use later: the
straight-drive stall point, the spin stall point, and your speed in cm/s. **Time:** 20 minutes.

A motor needs a minimum push just to start moving — below that, it hums and sits still (the
"stall point", explained in [Class 3][03]). Spinning in place takes *more* push than driving
straight, especially on carpet. You need both numbers before you can pick `TURN_SPEED` and
`DRIVE_SPEED`.

There's also a hidden cap to know about. `motor_driver.py` clamps **every** command to
`MAX_THROTTLE = 0.6`. So `DRIVE_SPEED = 0.6` is already at the ceiling: setting `DRIVE_SPEED = 0.8`
does *nothing* unless you also raise `MAX_THROTTLE`.

> **⚠ DANGER TO HARDWARE** — `MAX_THROTTLE` is there to protect the small TT gearbox motors, which
> are running from a 9V battery. **Leave it at `0.6` for tuning.** If you ever raise it, go up in
> steps of 0.05, and after a 1-minute run touch the motor cans: warm is fine, too hot to hold a
> finger on is not — lower it again. Too much current can also trip the DRV8833's overcurrent
> protection, which shuts off *both* motors until you unplug and replug the battery.

**Do this:**

1. Mark a start line on the floor with masking tape, with at least 2 m of clear floor ahead.
2. Save this test as `code.py` (temporarily). It uses your unchanged `motor_driver.py`:

   ```python
   # motor-check.py -- save as code.py TEMPORARILY; put class-5-code.py back when done.
   # Steps the throttle up to find the stall points, then does timed runs to measure speed.
   import time
   import motor_driver

   THROTTLES = [0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60]  # never above MAX_THROTTLE
   STEP_SECONDS = 0.7         # short bursts, so a stalled motor isn't pushed for long
   SPEED_RUN_THROTTLES = [0.5, 0.6]
   SPEED_RUN_SECONDS = 2.0

   def burst(left, right, seconds):
       motor_driver.drive(left, right)
       time.sleep(seconds)
       motor_driver.stop()
       time.sleep(1.5)        # pause so you can see (and write down) what happened

   print("Set the rover on the floor -- starting in 5 s")
   time.sleep(5)
   print("--- straight: when do the wheels start rolling? ---")
   for throttle in THROTTLES:
       print("straight throttle", throttle)
       burst(throttle, throttle, STEP_SECONDS)
   print("--- spin in place: when does it start turning? ---")
   for throttle in THROTTLES:
       print("spin throttle", throttle)
       burst(throttle, -throttle, STEP_SECONDS)
   for throttle in SPEED_RUN_THROTTLES:
       print("--- speed run at", throttle, "-- put the rover on the start line; 8 s ---")
       time.sleep(8)
       burst(throttle, throttle, SPEED_RUN_SECONDS)
       print("measure the distance from the start line now")
   print("done")
   ```

3. Keep the USB cable plugged in and follow along, carrying the laptop or letting the cable trail.
   Watch the rover and the console together.
4. Write down:
    * **Straight stall point** — the lowest throttle where the rover actually rolls forward
    * **Spin stall point** — the lowest throttle where it actually spins in place (on the floor you
      will test on — carpet needs more than tile)
    * **Speed** at 0.5 and 0.6 — distance traveled in cm ÷ 2 s = cm/s. For example, 70 cm in 2 s is
      35 cm/s.
5. Put `class-5-code.py` back as `code.py`.

**Done when:** your log has a straight stall point, a spin stall point, and a cm/s speed for 0.5
and 0.6, all measured on your test floor — and `MAX_THROTTLE` is still `0.6`.

**Ripple effects:** these numbers change with the battery and with the floor surface. If you move
from tile to carpet, redo this step and Step 6.


### Step 6 — Turning: clean, accurate compass turns

**Parameters:** `TURN_SPEED` (**Critical**), `HEADING_TOLERANCE_DEG` (**Important**),
`TURN_TIMEOUT_S` (**Useful** — a safety limit). **Time:** 30 minutes.

Turns are where most untuned rovers look bad. The compass turn spins toward the target and checks
the heading every 20 ms. Too little spin and the wheels can't move the rover; too much and it flies
past the target before the next check, then has to spin back.

```text
   TURN_SPEED too low          TURN_SPEED about right        TURN_SPEED too high
   --------------------        ----------------------        -------------------
   wheels hum, rover barely    one smooth spin, stops        spins past, reverses,
   moves -> "turn timed out"   within +/-5 of target         spins past again ->
                                                             wiggles, sometimes times out
```

**Do this:**

1. **Set a starting point.** `TURN_SPEED` = your spin stall point from Step 5, plus about `0.1`
   (for example, stall at `0.35` → start at `0.45`). Keep `HEADING_TOLERANCE_DEG = 5`.
2. **Run the turn test** from [Class 5][02]: temporarily set `SCAN_ANGLES = [150]`, so every scan
   picks "60° right." Also temporarily set `SCAN_INTERVAL = 1.0` so the rover turns often, and set
   `DRIVE_SPEED = 0.5` — a gentler, provisional value you'll finalize in Step 8. Set the rover on
   the floor, boot it still and flat, and watch the console for
   `drive: turning 60 deg to heading ...` followed by `drive: heading now ...`.

   > **⚠ CAUTION** — stopping distance isn't tuned yet (that's Step 8). Run this in the middle of
   > your open test space, walk alongside, and be ready to pick the rover up or pull the battery clip.
3. For five turns, write down how far `heading now` is from the target (for example, target 260,
   heading now 263 → +3).
4. **Adjust one number at a time** based on what you see:

   | What you see | Change |
   | :----------- | :----- |
   | `turn timed out`, and the wheels barely move | Raise `TURN_SPEED` by 0.05 |
   | Overshoots, wiggles back and forth before stopping | Lower `TURN_SPEED` by 0.05 |
   | Stops smoothly but misses by 6-8° | Lower `TURN_SPEED` by 0.05 (it's coasting past) |
   | Can't find a `TURN_SPEED` that both moves and stops cleanly | Raise `HEADING_TOLERANCE_DEG` to 8 |
   | `turn timed out` while the rover spins the *wrong way* forever | Not a tuning problem — see [Class 5 troubleshooting][02] (heading must go up on a clockwise turn) |

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

**Ripple effects:** `TURN_SPEED` is independent of `DRIVE_SPEED` — changing drive speed later
doesn't touch your turns. But a new floor surface, or a much weaker battery, can push the spin stall
point up; if timeouts come back, redo this step.


### Step 7 — Seeing: trustworthy scans

**Parameters:** `SETTLE_TIME` (**Important**), `SCAN_ANGLES` (**Useful** / **Taste**).
**Time:** 20 minutes.

A scan is only as good as each reading. The servo needs a moment to stop wobbling before the
ultrasonic reading means anything; `SETTLE_TIME` is that moment. Too short and readings are random.
Too long and each scan is slow. With 5 angles, `SETTLE_TIME = 0.15` makes a scan take about 0.75 s.

**Do this:**

1. **Make the rover scan without moving.** For this step only, set these in `class-5-code.py`
   (write the old values in your log so you can put them back):

   ```python
   DRIVE_SPEED = 0       # TEMPORARY (Step 7) -- no driving, no reversing
   TURN_SPEED = 0        # TEMPORARY (Step 7) -- no turning
   SCAN_INTERVAL = 1.0   # TEMPORARY (Step 7) -- scan often
   ```

   Now the rover sits still on the floor and scans over and over, so you can put boxes around it.
   Each cycle ends with `drive: turn timed out` after `TURN_TIMEOUT_S` — **that's expected** here,
   because the wheels have zero speed and the heading never changes. Just read the `scan:` lines.

   > **⚠ CAUTION** — don't hold a rover with spinning wheels to keep it still. Zero speeds are the
   > safe way to do this. Double-check both are `0` before you save.

2. **Check the sensor itself.** Put a cardboard box squarely in front at 50 cm, measured with the tape measure. Watch
   the `scan: angle 90 distance_cm ...` lines: they should read about 50 (within a couple of cm).
   Try 25 cm and 100 cm too. The HC-SR04 is good from about 2 cm to a few meters, and doesn't need
   calibrating — this just confirms it's healthy.
3. **Check the scan picks correctly.** Put boxes 30 cm away at every direction *except* one (say,
   the `120` direction). Five scans in a row should print `scan: chosen angle 120`. Move the gap to
   another angle and repeat.
4. **Tune `SETTLE_TIME`.** Lower it by `0.05` at a time and repeat item 3. When readings start
   coming back `None`, or the chosen angle becomes wrong or random, go back *up* by `0.05` from that
   point and keep that value. Don't go below about `0.1` for the SG90.
5. **Choose your `SCAN_ANGLES` (taste).** The default five angles are a good balance. Options:
    * **More angles** — for example `[30, 50, 70, 90, 110, 130, 150]` — finer choices, slower scans.
    * **Fewer angles** — for example `[45, 90, 135]` — faster, but coarser turns.

   Keep these rules: include `90` (straight ahead); keep the list symmetric around `CENTER_ANGLE`;
   stay inside the range you checked in Step 3; and keep the list ordered left to right.
6. **Restore** `DRIVE_SPEED`, `TURN_SPEED`, and `SCAN_INTERVAL` from your log. Put the rover on
   its stand before you save — with real speeds back, it drives off the moment `code.py` saves.

**Done when:** the ultrasonic reads within about 2 cm of your tape measure at 25, 50, and 100 cm,
and the scan chooses the one open gap correctly five times in a row, at every gap position you
tried. **The rover should now:** reliably look toward open space, not random directions.

**Ripple effects:** if you add angles outside 30-150, recheck servo aim (Step 3) at those angles.
More angles or a longer `SETTLE_TIME` make every stop longer, which you'll feel in Step 8.


### Step 8 — Behavior: speed, stopping distance, and how often to look

**Parameters:** `DRIVE_SPEED` (**Important** / **Taste**), `STOP_DISTANCE_CM` (**Critical**),
`SCAN_INTERVAL` (**Taste**). **Time:** 30 minutes.

This is the step that decides whether the rover hits things. The three knobs are linked by simple
math:

* **Stopping gap.** The rover checks distance about every 0.05 s, but it's moving the whole time,
  and it coasts a little after the motors stop. So it always stops a bit *closer* than
  `STOP_DISTANCE_CM`. Faster means a bigger overshoot. With the website open, a page refresh can
  add up to 0.25 s of blind driving — at 35 cm/s, that's about 9 cm more.
* **Distance between routine scans** = speed × `SCAN_INTERVAL`. At 35 cm/s and 3 s, that's about
  1 m of driving between looks.

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
   `MAX_THROTTLE` ceiling). Slower is more reliable — more time to react, smaller compass jumps from
   motor current. For first tuning runs, `0.5` is a good, safe choice. You can come back and speed up
   once everything else works.
2. **Stopping test.** Temporarily set `SCAN_INTERVAL = 30.0` so the rover doesn't stop to scan on
   its own. Close the website tab. Aim the rover straight at a cardboard box from about 1.5 m away,
   boot it still and flat, and let it drive. When it stops (you'll see
   `drive: obstacle close, distance_cm ...`), measure the gap from its front bumper to the box.
   Three runs; write down the smallest gap.
3. **Slow the website down first (only if you installed Stretch 2).** Every website request freezes
   the drive loop for about 0.25 s. The Stretch 2 history chart asks for data every 0.2 s — so with
   it open, the rover is blind *most of the time*, and no stop distance can fix that. In
   `class-6-code-2.py`, change `setTimeout(pollHistory, 200)` to `setTimeout(pollHistory, 1000)`
   (or higher). Also consider slowing the status page itself: the `500` in `rover_server.py`'s
   `setInterval(..., 500)` can become `1000`. (Rover on its stand before you save.)
4. Repeat item 2 **with the website open** on your laptop, three more runs — with the history chart
   page open, if you have Stretch 2.
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
   2 to 6 s is fine because the stop distance check protects the rover between scans. A good
   starting rule: speed × `SCAN_INTERVAL` of about 1 m.

> **⚠ CAUTION** — the rover only looks *forward*. Nothing on it sees a table edge or a stair. Run
> every test on the floor.

**Done when:** in six stopping runs (three with the browser closed, three open), the rover stops
with at least about 8 cm of gap every time and the bump switch never fires. **The rover should
now:** drive, see a box ahead, stop short of it, scan, turn away, and carry on — without touching
it.

**Ripple effects:**

* **Changing `DRIVE_SPEED` means redoing this step's stopping test** — overshoot grows with speed.
* `DRIVE_SPEED` is also the **reverse** speed after a safety stop, so changing it changes how far
  the rover backs up (Step 9).
* `STOP_DISTANCE_CM` sets how close the IR sensor should trigger (Step 9).


### Step 9 — Safety nets: IR range and back-off distance

**Parameters:** IR sensor trimmer (**Important**), `BACKOFF_S` (**Important**). **Time:** 20
minutes.

The IR sensor and bump switch catch what the ultrasonic sweep misses — chair legs, soft things,
objects that appear between checks. When either fires, the rover stops, reverses for `BACKOFF_S`
seconds at `DRIVE_SPEED`, then scans. The IR sensor should be a *backup*, triggering closer than
`STOP_DISTANCE_CM`, not a second, jumpy primary sensor.

```text
   distance from the front of the rover:

   0 cm       ~10 cm                     STOP_DISTANCE_CM (e.g. 25)
   |-- bump --|-- IR sensor zone --|------ ultrasonic stops here ------>
     (contact)   (backup, close)          (main, farther out)
```

**Do this:**

1. **IR range.** With the rover stationary and its code running, slowly move a piece of white paper
   toward the IR sensor and note where it triggers (the module's LED lights, and
   `SAFETY: IR sensor near-field obstacle` prints). Turn the trimmer screw with the small
   screwdriver until it triggers at about **8-12 cm** — clearly less than your `STOP_DISTANCE_CM`.
   (Most modules: counter-clockwise shortens the range; check yours, as described in the
   [Pre-Class IR sensor notes][07].)
2. Repeat with a dark object. Dark things reflect less IR, so they trigger closer. That's normal —
   just make sure it still triggers at all.
3. **Floor check.** Drive the rover around the test space for a minute with nothing in front of it.
   If it emergency-stops with nothing nearby, the IR sensor is seeing the floor: turn the trimmer
   down, or tilt the sensor up a little.
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

**Ripple effects:** changing `DRIVE_SPEED` later changes the back-off distance — recheck item 4.
Changing `STOP_DISTANCE_CM` may mean resetting the IR range to stay below it.


### Step 10 — Preferences: make it yours (optional)

**Parameters:** **Taste**, plus a few firm limits called out below. **Time:** 15-30 minutes, only
if you want to.

Chosen within the limits below, these have little effect on how well the rover avoids obstacles.
Change them for fun, or to match a stretch goal. (The website and chart refresh rates *do* affect
safety, which is why they were set back in Step 8.)

* **`DRIVE_SPEED`, `SCAN_INTERVAL`, `SCAN_ANGLES`** — the rover's "personality": cautious and
  twitchy, or bold and sweeping. Remember the ripple effects in Steps 7-9 if you change them.
* **Stretch 1 speed knob (`class-6-code-1.py`):** `MIN_SPEED`, `MAX_SPEED`, `SPEED_STEP`. Two firm
  limits, not taste: keep `MIN_SPEED` **above your straight stall point** from Step 5 (or the rover
  stalls at the bottom of the knob), and remember `MAX_SPEED` above `0.6` does nothing unless
  `MAX_THROTTLE` is raised. At high speeds, watch that turns still land on target (see
  [Class 6][06]). Also: the knob speed only changes forward and reverse — rerun the Step 8 stopping
  test at your fastest knob setting.
* **Website and chart refresh** — already handled in Step 8, item 3, because they affect safety.
  If you change them again here, remember: faster refresh = more blind time for the rover, so redo
  the Step 8 page-open stopping test.
* **Stretch 3 TFT `REFRESH_S`** — `0.2` is smooth; don't go much lower, since redrawing the screen
  is slow.

**Done when:** you like how it looks and feels — and if you changed `DRIVE_SPEED`, you've redone the
Step 8 stopping test and the Step 9 back-off check.


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

4. If you missed a target, find the matching step and revisit only that one:

   | Symptom | Go back to |
   | :------ | :--------- |
   | Turns miss, wiggle, or time out | Step 6 (and Step 4 if heading looks wrong on the website) |
   | Turns go the wrong direction by a fixed amount every time | Step 3 (servo aim) |
   | Hits boxes head-on | Step 8 |
   | Hits boxes at an angle, or thin/soft things | Step 9 (IR range), or accept it as a sensor limit |
   | Backs into things | Step 9 (`BACKOFF_S`) |
   | Stops constantly with nothing near | Step 9 (IR floor check), then Step 8 (`STOP_DISTANCE_CM` too big) |
   | Everything got worse after a while | Step 1 (battery) |

5. Copy your final values into your log, and save a copy of your tuned `code.py` and
   `rover_server.py` to your laptop in a folder named `rover-tuned`.

**Done when:** the rover completes a 5-minute arena run meeting all four targets. **The rover is
tuned.** It should drive with purpose, stop short of obstacles, look, turn crisply to open space,
and keep going for minutes at a time without you.


### When do I have to re-tune?

| Something changed | Redo |
| :---------------- | :--- |
| New battery | Step 1, then a 5-minute Step 11 run |
| New floor (tile ↔ carpet) | Steps 5, 6, 8 |
| IMU, battery, or motors moved; steel added near the IMU | Step 4, then Step 11 |
| Servo horn reseated, or sensor bumped | Step 3, then Step 7 |
| `DRIVE_SPEED` changed | Step 8 stopping test, Step 9 back-off |
| `TURN_SPEED` or `HEADING_TOLERANCE_DEG` changed | Step 6 turn test |
| Only code logic changed, no constants | Nothing — but run Step 11 to be sure |


## Going Deeper

Want to understand *why* these knobs behave the way they do? The Class 3 lesson script's straight-
drive tuning section is a complete worked example of disciplined tuning — baselines, noise floors,
sweeps, and knowing when to stop ([Class 3][03]). The IMU explainer covers why the compass needs
calibrating and why the filter gains are best left alone ([IMU and Mahony filter][05]). And the
lesson scripts for [Class 2][08] (servo and sensor), [Class 4][09] (the IMU filter), [Class 5][02]
(the rover), and [Class 6][06] (finishing it) explain where every parameter in this guide came from.


[01]:what-is-the-random-rover.md
[02]:../lesson_scripts/class-05-lesson-script.md
[03]:../lesson_scripts/class-03-lesson-script.md
[04]:https://datasheets.raspberrypi.com/picow/pico-2-w-datasheet.pdf
[05]:what-is-an-imu-and-mahony-filter.md
[06]:../lesson_scripts/class-06-lesson-script.md
[07]:../lesson_scripts/class-00-lesson-script.md
[08]:../lesson_scripts/class-02-lesson-script.md
[09]:../lesson_scripts/class-04-lesson-script.md
