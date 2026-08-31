# Lesson Script: Class 1 — Push Button Switch and Rotary Encoder

* **Class:** 1 of 6 (plus Pre-Class)
* **Duration:** ~2 hours
* **What You'll Need:** see [Section 2](#2-what-youll-need)
* **Before You Start:** Your Pico 2 W should already have CircuitPython flashed on it, the Mu or
    Thonny editor installed, the Adafruit CircuitPython Library Bundle downloaded somewhere on your
    laptop, and you should have already gotten the onboard LED blinking with a heartbeat count in
    the serial console (that was the Pre-Class). If any of that isn't working yet, fix it before
    starting this script — everything here builds on it.

---


## 1. What This Project Is

Today you build your first "real" circuit — up to now you've only proven your board, your
firmware, and your editor can talk to each other. You're going to wire up a pushbutton switch and
a rotary encoder (the kind of knob you can spin forever, like a volume dial), and use them to
control two LEDs: one turns on when you press the button, the other gets brighter or dimmer as
you turn the knob.

Here's the twist: you're going to build it *wrong* first, on purpose. You'll write code that reads
the button and encoder in the simplest, most naive way possible, and you'll watch it produce
garbage — a single button press registering as five, seven, twelve presses. That garbage has a
name (**switch bounce**) and a fix (**debouncing**), and by the end of this script you'll have
added that fix yourself and watched the same button press turn into exactly one clean reading.

This circuit doesn't get torn down at the end of class — it stays on your breadboard for the rest
of the course. The rotary encoder comes back, completely unchanged, as a live speed control for
your robot car in Class 6.

## 2. What You'll Need

| Component | Quantity | Purpose This Project |
|:----------|:--------:|:---------------------|
| Raspberry Pi Pico 2 W (with header) | 1 | Runs your CircuitPython code |
| Momentary Push Button Tactile Switch | 1 | Digital input — the thing you press |
| KY-040 rotary encoder module | 1 | Rotational input — the knob you turn |
| LED | 2 | One lights up on button press, one dims/brightens with the knob |
| Current-limiting resistor (220-330 ohm) | 2 | Protects each LED from too much current |
| Breadboard (830-point) | 1 | Where you build the circuit |
| Dupont jumper wires | ~10 | Point-to-point connections |
| USB cable | 1 | Powers the Pico and carries the serial console |
| Laptop with Mu or Thonny | 1 | Where you write/save code and read the serial console |

**Additional components for the Homework Assignments** (Section 10) — not needed for tonight's class
itself, only if you choose to do Homework 4 or Homework 6 at home:

| Component | Quantity | Purpose (Homework #) |
|:----------|:--------:|:---------------------|
| IR Obstacle Avoidance Sensor | 1 | Digital proximity detection run through the same `Debouncer` pattern as the button (Homework 4) — also used on the Random Rover in Class 5 |
| 1.14" 240x135 Color TFT Display (ST7789) | 1 | Live bar-gauge display driven by the rotary encoder (Homework 6) — also used in the Pre-Class homework and Class 6's stretch goal |

Homework 1 (long-press detection), Homework 2 (encoder acceleration), Homework 3 (persistent press
counter), Homework 5 (combination lock), Homework 7 (remote dimmer), Homework 8 (countdown timer),
and Homework 9 (NVM event log) need no additional hardware beyond the button + rotary encoder
circuit already on your breadboard.

## 3. Meet the Hardware

**Pushbutton switch.** A push-button is just two metal contacts that touch when you press it and
separate when you release it. It has no "smarts" — it's a plain on/off switch. In CircuitPython
you read it with the `digitalio` module, which lets you treat any GPIO pin as a simple input or
output. We wire the button so one leg goes to a GPIO pin and the other leg goes to `GND`
(ground), and we turn on the Pico's **internal pull-up resistor** on that pin. That means the pin
reads `True` (high) when the button is *not* pressed, and `False` (low) when it *is* pressed —
this wiring style is called **active-low**, and it's the standard, recommended way to wire a
simple switch to a microcontroller because it needs no external resistor for the switch itself.

>**NOTE:** Momentary Push Button Tactile Switch work best in a printed circuit board (PCB)
>but can be used on a solderless breadboard as shown in [this tutorial][36].

**KY-040 rotary encoder.** This looks like a volume knob, and internally it's two switches (called
`CLK` and `DT`) arranged so that as you turn the shaft, they trip in a specific order — `CLK`
then `DT` if you turn one way, `DT` then `CLK` if you turn the other. Reading which one changes
first tells you which direction the knob turned. This pattern is called **quadrature encoding**,
and like the pushbutton, both `CLK` and `DT` are just digital signals you read with `digitalio`,
wired active-low with internal pull-ups. The KY-040 module also has a `+`/VCC pin (power) and a
`GND` pin, separate from its `SW` pin (a built-in pushbutton you get by pressing the knob itself —
we aren't using `SW` in this project).

**LEDs.** An LED (light-emitting diode) only lets current flow one direction, and it needs a
current-limiting resistor in series or it will burn out almost instantly. The button's LED is
wired for simple on/off control via `digitalio`. The encoder's LED is wired to a **PWM**
(pulse-width modulation) pin instead, controlled with the `pwmio` module — PWM switches the pin on
and off very fast (thousands of times per second) and varies how *long* it's on each cycle, which
your eye perceives as brightness. You'll use PWM again for the servo motor in Class 2 and the
motor driver in Class 3, so this is your first look at a pattern you'll reuse all course.

**Pinout summary** (Raspberry Pi Pico 2 W):

| Pin | What we use it for |
| :---- | :-------------------- |
| `GP2` | Button input |
| `GP3` | Encoder `CLK` input |
| `GP4` | Encoder `DT` input |
| `GP14` | Encoder brightness LED output (PWM) |
| `GP15` | Button LED output (plain on/off) |
| `VSYS 5V` | Encoder `+`/VCC power |
| `GND` | Encoder `GND`, button's second leg, both LED cathodes |

## 4. Build It: Phase 1 — See the Bounce

### Wiring for this phase

This is the complete wiring for this whole build — nothing changes between Phase 1 and Phase 2,
only the code does.
**Wiring — Raspberry Pi Pico 2W to push-button switch, rotary encoder, LED, resistor:**
* [Raspberry Pi Pico 2w Pinout][20] - turn-off SPI/I2C/UART/Custom/Advanced/Flip/Rotate buttons at the top
* [Tactile Push Button Switch PINOUT][35]
* [KY-040 Rotary Encoder PINOUT][38]
* [LED PINOUT][39]

[35]:https://components101.com/switches/push-button
[36]:https://learn.adafruit.com/adafruit-arduino-lesson-6-digital-inputs
[37]:https://www.electronics-tutorials.ws/logic/pull-up-resistor.html
[38]:https://www.datasheethub.com/ky-040-rotary-encoder-sensor-module/
[39]:https://www.build-electronic-circuits.com/what-is-an-led/


| Component | Pico 2 W Pin |
| :---------- | :------------- |
| Pushbutton switch, one leg | `GP2` |
| Pushbutton switch, other leg | `GND` |
| Rotary encoder `CLK` | `GP3` |
| Rotary encoder `DT` | `GP4` |
| Rotary encoder `SW` | not used |
| Rotary encoder `+` / `VCC` | `VSYS 5V` |
| Rotary encoder `GND` | `GND` |
| Button LED anode, through resistor | `GP15` |
| Button LED cathode | `GND` |
| Encoder brightness LED anode, through resistor | `GP14` |
| Encoder brightness LED cathode | `GND` |

>**NOTE:** Identifying an LED Anode** The positive anode is always the longer wire leg.
>The short leg, near the flat notch on the plastic rim, is the negative cathode.

Before writing any code, trace your own wiring against this table out loud — wiring mistakes are
much faster to catch now than after you're staring at confusing code output.

### Understanding Pull-Up & Pull-Down Resistors
[Pull-up and pull-down resistors][37] are basic electronic components used in digital circuits
to give an input pin a clear, default voltage state and prevent a "floating" (unpredictable) condition

**Why Are They Important?**
* **Prevents Floating Inputs:** Without these resistors,
  an unconnected pin picks up stray electrical noise from the air,
  causing random and false logic switching.
* **Limits Current:** They provide high resistance (commonly 10 kΩ) so that when a button is pressed,
  it does not create a dangerous direct short circuit between power and ground.

>**NOTE:** You can use internal pull-up or pull-down resistors on the Raspberry Pi Pico 2W via software configuration,
>though early hardware revisions require caution with pull-downs due to an errata chip bug.

### Important Hardware Note for Pico 2W
* **RP2350 Errata Bug:**
  The initial RP2350 silicon revision has an internal pull-down bug (RP2350-E9) that can cause
  pins configured with internal pull-downs to falsely read HIGH.

### What this code does

This first version reads the button and encoder in the most straightforward way possible: check
the pin, and if it changed, count it. No filtering, no waiting, nothing fancy. It's deliberately
naive so you can see exactly what goes wrong.

### The code - No Debouncing

Save this as `code.py` on your `CIRCUITPY` drive.

```python
# class-1-code-1.py
# Phase 1: read the button and rotary encoder with NO debouncing at all.
# Goal: watch a single physical press/turn produce multiple, erratic readings.

import time
import board
import digitalio
import pwmio

# --- Button setup ---
# digitalio.DigitalInOut turns a GPIO pin into a simple digital input or output.
button = digitalio.DigitalInOut(board.GP2)
button.direction = digitalio.Direction.INPUT
# Pull.UP means the pin reads True when nothing is pressed, and False when
# the button connects it to GND. This is "active-low" wiring.
button.pull = digitalio.Pull.UP

# --- Rotary Encoder setup ---
# Both CLK and DT are wired the same way as the button: active-low with a pull-up.
encoder_clk = digitalio.DigitalInOut(board.GP3)
encoder_clk.direction = digitalio.Direction.INPUT
encoder_clk.pull = digitalio.Pull.UP

encoder_dt = digitalio.DigitalInOut(board.GP4)
encoder_dt.direction = digitalio.Direction.INPUT
encoder_dt.pull = digitalio.Pull.UP

# --- Button LED setup ---
# A plain digital output: fully on or fully off, no in-between.
button_led = digitalio.DigitalInOut(board.GP15)
button_led.direction = digitalio.Direction.OUTPUT

# --- Rotary Encoder LED setup ---
# pwmio.PWMOut lets us control brightness instead of just on/off.
# frequency=5000 means the pin switches on/off 5000 times per second -- fast
# enough that your eye only sees the average brightness, not any flicker.
# duty_cycle starts at 0 (fully off) and ranges up to 65535 (fully on).
encoder_led = pwmio.PWMOut(board.GP14, frequency=5000, duty_cycle=0)

# Running totals we update as we detect changes.
press_count = 0
encoder_position = 0
# We need to remember the encoder's last CLK reading so we can tell when it changes.
last_clk_state = encoder_clk.value

print("Class 1, Phase 1 -- raw (bouncy) readings starting...")
print("Press the button and turn the knob. Watch the counts jump around.")

while True:
    # --- Push Button: count every time the pin reads "pressed" (False) ---
    if not button.value:
        press_count += 1
        button_led.value = True
        print("RAW push count:", press_count)
    else:
        button_led.value = False

    # --- Rotary Encoder: naive quadrature read ---
    clk_state = encoder_clk.value
    if clk_state != last_clk_state:
        # If DT differs from the NEW clk_state, we turned one direction;
        # if DT matches it, we turned the other direction.
        if encoder_dt.value != clk_state:
            encoder_position += 1
        else:
            encoder_position -= 1
        # Clamp so duty_cycle math below never goes out of range.
        encoder_position = max(0, min(100, encoder_position))
        # Convert our 0-100 position into a 0-65535 PWM duty cycle.
        encoder_led.duty_cycle = int(encoder_position / 100 * 65535)
        print("RAW encoder_position:", encoder_position)
    last_clk_state = clk_state

    # Sample very fast on purpose -- this is what exposes the bounce.
    # A slower loop would accidentally hide some of the bouncing.
    time.sleep(0.001)
```

### Try it / what you should see

Press the button once, slowly and normally — not a special "bad" press, just a normal one. Watch
the serial console. You should see `RAW press_count:` print out **more than once** for that single
press — maybe 3, maybe 12, and it'll be different every time. Turn the knob one detent (one
"click") and watch `RAW encoder_position:` — it may jump by more than 1, or briefly move the wrong
direction before settling.

This is switch bounce: the metal contacts inside the button and encoder don't touch cleanly. They
physically bounce apart and re-touch several times over a few milliseconds — like a dropped ball
that doesn't stop on its first bounce. Your Pico reads its pins fast enough to see every one of
those bounces as a separate event.

### Checkpoint

Before moving on, confirm: pressing the button turns `button_led` on, turning the knob changes
`encoder_led`'s brightness, and both actions print erratic, multi-count output to the console. If
nothing prints at all when you press/turn, check your wiring against the table above before
touching the code — a miswired pin is far more likely than a code bug at this stage.

## 5. Build It: Phase 2 — Fix It With Debouncing

### Wiring for this phase

No wiring changes — same circuit as Phase 1.

### What this code does

This version fixes the bounce two different ways for two different kinds of input:

* For the **button**, we use the `adafruit_debouncer` library's `Debouncer` class, which tracks
    the pin's state over time and only reports a press once it's been stable.
* For the **encoder**, we use a simpler technique: ignore any change that happens less than
    `MIN_STEP_INTERVAL` seconds after the last accepted change. Bounces happen within a couple of
    milliseconds of each other, so a small time window filters them out without slowing down a
    real, deliberate turn.

You'll need the `adafruit_debouncer` library for this. It comes from the Adafruit CircuitPython
Library Bundle you downloaded in the Pre-Class — copy the `adafruit_debouncer.mpy` file into the
`/lib` folder on your `CIRCUITPY` drive before running this code.

### The code

Save this as `code.py`, replacing Phase 1's version.

```python
# class-1-code-2.py
# Phase 2: same wiring as Phase 1, now with debouncing on both the button and the encoder.
# Goal: watch a single physical press/turn produce exactly ONE clean reading.

import time
import board
import digitalio
import pwmio
from adafruit_debouncer import Debouncer

# --- Button setup ---
# Debouncer wraps a DigitalInOut and tracks its state over time so we can
# ask "did this JUST change?" instead of "what is it right now?"
button_pin = digitalio.DigitalInOut(board.GP2)
button_pin.direction = digitalio.Direction.INPUT
button_pin.pull = digitalio.Pull.UP
button = Debouncer(button_pin)

# --- Rotary encoder setup (unchanged from Phase 1) ---
encoder_clk = digitalio.DigitalInOut(board.GP3)
encoder_clk.direction = digitalio.Direction.INPUT
encoder_clk.pull = digitalio.Pull.UP

encoder_dt = digitalio.DigitalInOut(board.GP4)
encoder_dt.direction = digitalio.Direction.INPUT
encoder_dt.pull = digitalio.Pull.UP

# --- Button LED setup (unchanged from Phase 1) ---
button_led = digitalio.DigitalInOut(board.GP15)
button_led.direction = digitalio.Direction.OUTPUT

# --- Encoder LED setup (unchanged from Phase 1) ---
encoder_led = pwmio.PWMOut(board.GP14, frequency=5000, duty_cycle=0)

press_count = 0
encoder_position = 0
last_clk_state = encoder_clk.value
last_step_time = 0.0
# Ignore encoder edges that arrive less than this many seconds after the last
# accepted one. Raise this if your encoder is still jittery; lower it if fast
# turns feel like they're getting missed.
#MIN_STEP_INTERVAL = 0.02
MIN_STEP_INTERVAL = 0.5

print("Class 1, Phase 2 -- debounced readings starting...")
print("Press the button and turn the knob. Each action should now print exactly once.")

while True:
    # --- Button: Debouncer.update() must be called every single loop, ---
    # --- unconditionally, or it can't track the pin's state over time. ---
    button.update()
    # .fell is True for exactly one loop iteration: the moment a debounced
    # press is detected (pin went from "not pressed" to "pressed").
    if button.fell:
        press_count += 1
        print("DEBOUNCED press_count:", press_count)
    # button.value is the debounced value now: True = not pressed, False = pressed.
    button_led.value = not button.value

    # --- Encoder: same quadrature read as Phase 1, but gated by a time filter ---
    clk_state = encoder_clk.value
    now = time.monotonic()
    if clk_state != last_clk_state and (now - last_step_time) >= MIN_STEP_INTERVAL:
        if encoder_dt.value != clk_state:
            encoder_position += 1
        else:
            encoder_position -= 1
        encoder_position = max(0, min(100, encoder_position))
        encoder_led.duty_cycle = int(encoder_position / 100 * 65535)
        last_step_time = now
        print("DEBOUNCED encoder_position:", encoder_position)
    last_clk_state = clk_state

    time.sleep(0.001)
```

### Try it / what you should see

Press the button once. You should see `DEBOUNCED press_count:` print **exactly once**, increasing
by exactly 1. Turn the knob one detent. You should see `DEBOUNCED encoder_position:` print
**exactly once**, changing by exactly 1, in the direction you actually turned it.

If the encoder still feels jittery — occasional double-counts or wrong-direction jumps — try
raising `MIN_STEP_INTERVAL` in small steps (`0.02` -> `0.03` -> `0.05`) and re-testing. Cheap
KY-040 modules vary quite a bit in quality.

### Checkpoint

Press the button five separate times, one at a time. `press_count` should read exactly 5
afterward — not 4, not 11. Turn the knob three detents in the same direction. `encoder_position`
should have changed by exactly 3. If both of those hold, Phase 2 is working correctly.

## 6. Build It: Try Making Modifications Yourself

Once Phase 2 is passing its checkpoint, make a few small, deliberate changes and watch what
happens each time — this "change one thing, test it, see the result" habit is the same one you
used in the Pre-Class and will keep using for the rest of the course:

* Swap the `encoder_clk` and `encoder_dt` wires at the breadboard (or swap the `+1`/`-1` lines in
    the code) and confirm the knob now counts backward from what it did before.
* Lower `MIN_STEP_INTERVAL` toward `0.0` and turn the knob at a normal pace — watch the debounced
    reading start jittering again, the same multi-count problem Phase 1 had. This proves the filter
    is doing real work, not just always agreeing with what you'd expect.
* Comment out `button.update()` (or move it inside the `if button.fell:` block) and confirm
    `Debouncer` stops working correctly — this is the exact bug called out in the Troubleshooting
    table below, deliberately reproduced so you recognize it if you hit it by accident later.
* Temporarily add `print(time.monotonic())` inside the loop and watch how fast it climbs — this is
    the same running clock Homework 1 and Homework 8 build on later.

## 7. Troubleshooting Guide

| Problem | Likely Cause | Fix |
| :-------- | :------------- | :---- |
| Nothing prints when you press the button | Button wired to the wrong pin, or its `GND` leg isn't connected | Check both legs — one must reach `GP2`, the other must reach `GND` |
| `press_count` still jumps by more than 1 in Phase 2 | `button.update()` isn't being called every loop, or it's inside an `if` | Move `button.update()` so it runs unconditionally, once per loop, before any `if button.fell` check |
| Encoder LED never changes brightness | `encoder_led` on the wrong pin, or that pin doesn't support PWM | Double-check `GP14` wiring; if the pin itself is suspect, try a different PWM-capable GPIO |
| Encoder counts backward from the direction you turned | `CLK`/`DT` wires swapped | Swap the two wires at the encoder, or swap the `+1`/`-1` lines in the code |
| Encoder still jittery after adding debouncing | `MIN_STEP_INTERVAL` too small for this particular encoder | Raise it gradually (`0.02` -> `0.03` -> `0.05`) and retest after each change |
| `ImportError: no module named 'adafruit_debouncer'` | The library file isn't on your `CIRCUITPY` drive | Copy `adafruit_debouncer.mpy` from the Library Bundle into the `/lib` folder on `CIRCUITPY` |
| Serial console shows nothing at all | Wrong COM/serial port selected, or a charge-only USB cable/port | Reselect the correct port in Mu/Thonny; try a different cable or USB port |
| Button LED stays on permanently | Wiring assumes active-low but the switch's other leg is on `3V3` instead of `GND` | Move that leg to `GND`; confirm `pull = digitalio.Pull.UP` in the code |

## 8. Build It: Put It All Together

This is the finished project in one place — everything you need to build it from scratch without
following the phase-by-phase walkthrough above.

### Complete wiring

| Component | Pico 2 W Pin |
| :---------- | :------------- |
| Pushbutton switch, one leg | `GP2` |
| Pushbutton switch, other leg | `GND` |
| Rotary encoder `CLK` | `GP3` |
| Rotary encoder `DT` | `GP4` |
| Rotary encoder `SW` | not used |
| Rotary encoder `+` / `VCC` | `VSYS 5V` |
| Rotary encoder `GND` | `GND` |
| Button LED anode, through resistor | `GP15` |
| Button LED cathode | `GND` |
| Encoder brightness LED anode, through resistor | `GP14` |
| Encoder brightness LED cathode | `GND` |

### Complete code

Save as `code.py`. This is the debounced (Phase 2) version — the working, finished state this
project should be in when you're done. Print statements are trimmed to the essentials so the
console stays readable.

```python
# class-1-code-2.py -- complete, debounced button + rotary encoder project.
import time
import board
import digitalio
import pwmio
from adafruit_debouncer import Debouncer

# --- Button ---
button_pin = digitalio.DigitalInOut(board.GP2)
button_pin.direction = digitalio.Direction.INPUT
button_pin.pull = digitalio.Pull.UP
button = Debouncer(button_pin)

# --- Rotary encoder ---
encoder_clk = digitalio.DigitalInOut(board.GP3)
encoder_clk.direction = digitalio.Direction.INPUT
encoder_clk.pull = digitalio.Pull.UP

encoder_dt = digitalio.DigitalInOut(board.GP4)
encoder_dt.direction = digitalio.Direction.INPUT
encoder_dt.pull = digitalio.Pull.UP

# --- LEDs ---
button_led = digitalio.DigitalInOut(board.GP15)
button_led.direction = digitalio.Direction.OUTPUT
encoder_led = pwmio.PWMOut(board.GP14, frequency=5000, duty_cycle=0)

press_count = 0
encoder_position = 0
last_clk_state = encoder_clk.value
last_step_time = 0.0
MIN_STEP_INTERVAL = 0.02  # seconds; raise if your encoder is still jittery
#MIN_STEP_INTERVAL = 0.5

print("Class 1 project running -- button + rotary encoder, debounced.")

while True:
    # Button: must call update() every loop.
    button.update()
    if button.fell:
        press_count += 1
        print("press_count:", press_count)
    button_led.value = not button.value

    # Encoder: quadrature read, gated by a minimum time between accepted steps.
    clk_state = encoder_clk.value
    now = time.monotonic()
    if clk_state != last_clk_state and (now - last_step_time) >= MIN_STEP_INTERVAL:
        if encoder_dt.value != clk_state:
            encoder_position += 1
        else:
            encoder_position -= 1
        encoder_position = max(0, min(100, encoder_position))
        encoder_led.duty_cycle = int(encoder_position / 100 * 65535)
        last_step_time = now
        print("encoder_position:", encoder_position)
    last_clk_state = clk_state

    time.sleep(0.001)
```

## 9. What You Learned

You built your first real physical computing circuit and watched a genuine hardware problem show
up on your own screen — not just heard about it. Specifically, you now know:

* How to wire and read a digital input (`digitalio`) with a pull-up resistor, active-low
* How to read a rotary encoder's two-signal quadrature output to detect direction
* How to control an LED's brightness with PWM (`pwmio`), not just turn it on/off
* What switch bounce physically is, and why a microcontroller sees it as many events instead of one
* How to fix it in software two different ways: `adafruit_debouncer.Debouncer` for a simple
  on/off input, and a minimum-time-interval filter for a multi-signal input like an encoder

Leave this circuit on your breadboard — you'll use the rotary encoder again, completely unchanged,
in Class 6 as a live speed control for your robot car. Next class, you'll meet a new kind of
"noisy real-world signal" problem: an ultrasonic distance sensor, wired fresh on brand-new pins,
with today's circuit untouched right next to it.

---
## 10. Homework Assignment

Today's circuit and code stay on your breadboard — the exercises below are **homework, not
required class content**, and each one builds directly on the button + rotary encoder circuit and
the debouncing patterns you just learned tonight. Do them in any order. For each one you'll find:
what the code teaches and why it's useful, the full commented code to save as `code.py` on your
`CIRCUITPY` drive, what to expect when you test it, and a couple of real-world examples of where
this exact technique shows up outside a classroom. Only Homework 4 and Homework 6 need a part
beyond tonight's circuit — see [Section 2](#2-what-youll-need).

### Homework 1 — Long-Press vs. Short-Press Detection

**What this teaches:** So far you've only asked the button one question: "did you just get
pressed?" (`.fell`). Real buttons usually need to answer a second question too: "*how long* were
you held?" This exercise uses `Debouncer.fell` and `Debouncer.rose` together with
`time.monotonic()` to time the gap between the press and the release, then classifies the result as
a quick tap or a long hold.

```python
# code.py - distinguish a quick tap from a held press
import time
import board
import digitalio
from adafruit_debouncer import Debouncer

button_pin = digitalio.DigitalInOut(board.GP2)
button_pin.direction = digitalio.Direction.INPUT
button_pin.pull = digitalio.Pull.UP
button = Debouncer(button_pin)

LONG_PRESS_SECONDS = 0.6  # hold longer than this and it counts as a "long press"
press_started = None

print("Class 1 Homework 1 -- tap the button briefly, then hold it past 0.6s.")

while True:
    button.update()

    if button.fell:
        # Button just went down -- start the clock. We won't know the total
        # hold time until it comes back up.
        press_started = time.monotonic()

    if button.rose and press_started is not None:
        # Button just came back up -- now we know the full hold duration.
        held_for = time.monotonic() - press_started
        if held_for >= LONG_PRESS_SECONDS:
            print(f"LONG PRESS ({held_for:.2f}s)")
        else:
            print(f"short press ({held_for:.2f}s)")
        press_started = None

    time.sleep(0.001)
```

#### What You Observe
**Test it:** Tap the button quickly — you should see `short press`. Hold it down for over half a
second before releasing — you should see `LONG PRESS` instead, with the actual hold time printed.
Try changing `LONG_PRESS_SECONDS` and see how it changes where the line falls.

#### Real World Examples

* Phone and laptop power buttons use exactly this distinction — a tap wakes the screen, a
  multi-second hold force-shuts-down the device.
* Camera shutter buttons: a tap takes one photo, a held press triggers burst mode on many cameras.

### Homework 2 — Encoder Acceleration (Speed-Sensitive Stepping)

**What this teaches:** Tonight's Phase 2 encoder code already measures the time between accepted
steps (`MIN_STEP_INTERVAL`) to filter out bounce. This exercise reuses that same timing measurement
for a second purpose: instead of just accepting or rejecting a step, it scales *how big* each step
is based on how fast you're turning the knob — a fast spin jumps the position by more than a slow,
deliberate turn, exactly like a volume knob or a mouse scroll wheel that speeds up under a fast
flick.

```python
# code.py - rotary encoder that jumps by more than 1
# per detent when spun quickly, like a volume knob or a scroll wheel.
import time
import board
import digitalio
import pwmio

encoder_clk = digitalio.DigitalInOut(board.GP3)
encoder_clk.direction = digitalio.Direction.INPUT
encoder_clk.pull = digitalio.Pull.UP

encoder_dt = digitalio.DigitalInOut(board.GP4)
encoder_dt.direction = digitalio.Direction.INPUT
encoder_dt.pull = digitalio.Pull.UP

encoder_led = pwmio.PWMOut(board.GP14, frequency=5000, duty_cycle=0)

encoder_position = 0
last_clk_state = encoder_clk.value
last_step_time = 0.0
MIN_STEP_INTERVAL = 0.02  # same debounce filter as tonight's Phase 2
#MIN_STEP_INTERVAL = 0.5

print("Class 1 Homework 2 -- turn the knob slowly, then turn it fast, and compare.")

while True:
    clk_state = encoder_clk.value
    now = time.monotonic()
    if clk_state != last_clk_state and (now - last_step_time) >= MIN_STEP_INTERVAL:
        # The faster consecutive steps arrive, the bigger a jump we apply.
        time_since_last_step = now - last_step_time
        if time_since_last_step < 0.05:
            step_size = 5      # very fast turn
        elif time_since_last_step < 0.15:
            step_size = 2      # medium turn
        else:
            step_size = 1      # slow, deliberate turn

        if encoder_dt.value != clk_state:
            encoder_position += step_size
        else:
            encoder_position -= step_size
        encoder_position = max(0, min(100, encoder_position))
        encoder_led.duty_cycle = int(encoder_position / 100 * 65535)
        last_step_time = now
        print("encoder_position:", encoder_position, " step_size:", step_size)
    last_clk_state = clk_state

    time.sleep(0.001)
```

#### What You Observe
**Test it:** Turn the knob one slow detent at a time — `encoder_position` should climb by 1 each
time, same as tonight's Phase 2. Now spin it quickly through several detents — watch
`step_size` jump to 2 or 5 and `encoder_position` (and the LED brightness) race up much faster.

#### Real World Examples

* Mouse and trackpad scroll wheels accelerate the same way — a slow scroll moves a few lines, a
  fast flick jumps a whole page.
* Car radio and thermostat volume/temperature knobs often speed up their response the faster you
  turn them, so a big adjustment doesn't take dozens of individual clicks.

### Homework 3 — Persistent Press Counter (Survives Power-Off)

**What this teaches:** Every variable in your code so far has lived in RAM, which means it resets
to its starting value the instant the board loses power — unplug it and `press_count` goes back to 0.
This exercise introduces `microcontroller.nvm` (aka [non-volatile memory][05]),
a small block of memory built into the chip that
is specifically designed to *keep* its contents across power loss and resets. You'll store
`press_count` there instead of in a normal variable, so the count survives being unplugged.

Let's first initialize the NVM with the value zero
so that we don't get a random value from the NVM memory on the microcontroller:

```python
# use this to initialize the NVM in the microcontroller to the value "0"

import microcontroller  # gives access to microcontroller.nvm, a small chunk of memory
                         # that survives power loss and resets, unlike a normal variable

def save_press_count(value):
    microcontroller.nvm[0:4] = value.to_bytes(4, "big")

save_press_count(0)
```

After you do the initialization with the code above,
load and run the code below:

```python
# code.py - press_count that survives unplugging the board
import time
import board
import digitalio
import microcontroller  # gives access to microcontroller.nvm, a small chunk of memory
                         # that survives power loss and resets, unlike a normal variable
from adafruit_debouncer import Debouncer

button_pin = digitalio.DigitalInOut(board.GP2)
button_pin.direction = digitalio.Direction.INPUT
button_pin.pull = digitalio.Pull.UP
button = Debouncer(button_pin)

# press_count is stored as 4 bytes (a 32-bit integer) at the very start of nvm.
def load_press_count():
    stored = microcontroller.nvm[0:4]
    return int.from_bytes(stored, "big")

def save_press_count(value):
    microcontroller.nvm[0:4] = value.to_bytes(4, "big")

# you must initialise the NVM with this statement

press_count = load_press_count()
print("Class 1 Homework 3 -- press_count loaded from NVM:", press_count)
print("Press a few times, unplug the board, plug it back in, and watch the count pick up where it left off.")

while True:
    button.update()
    if button.fell:
        press_count += 1
        save_press_count(press_count)
        print("press_count:", press_count)

    time.sleep(0.001)
```

#### What You Observe
**Test it:** Note the starting `press_count` printed at boot (it should be 0 the very first run),
press the button a handful of times, then unplug the USB cable and plug it back in. The count
printed at startup should now match the last value you saw before unplugging — not reset to 0.
NVM has a large but finite number of writes (roughly 100,000 cycles), plenty for this exercise, and
it's separate from `code.py` itself — re-flashing CircuitPython firmware does clear it.

#### Real World Examples

* Car odometers and appliance cycle counters (washing machines, coffee makers) use the same idea —
  a small persistent memory that survives being unplugged, separate from the device's main program.
* Video games save your progress to persistent storage (a save file or memory card) for exactly the
  same reason: the console's RAM forgets everything the instant it powers off.

### Homework 4 — Add the IR Obstacle Sensor as a Second Debounced Input

**What this teaches:** *(Requires the IR Obstacle Avoidance Sensor — already in the course's bill
of materials for the Random Rover in Class 5, see [Section 2](#2-what-youll-need).)* Tonight you
learned that debouncing fixes noisy readings from a mechanical switch. This exercise proves the
technique isn't button-specific: the IR sensor is a completely different kind of digital input
(an optical proximity detector, not a mechanical contact), and it gets wired through the exact same
`Debouncer` class as the pushbutton, with no changes to the debouncing logic at all. This is the
same sensor, same pin, and same read pattern you'll reuse on the Random Rover in Class 5.

**Wiring — Pico 2 W to IR Obstacle Avoidance Sensor:**
* [Raspberry Pi Pico 2w Pinout][20]
* [IR Obstacle Avoidance Sensor Pinout][34]

| Pico 2 W Pin | Sensor Pin | Signal / Function |
| :------------- | :----------- | :-------------------- |
| `3V3` (or `VBUS`) | `VCC` | Power (most of these modules accept 3.3-5V) |
| `GND` | `GND` | Common ground |
| `GP13` | `OUT` | Digital output — LOW when an obstacle is detected |

```python
# code.py - run the IR Obstacle Avoidance Sensor through
# the SAME Debouncer pattern used for the pushbutton -- proof that debouncing
# isn't a "button-only" trick, it's a general technique for noisy digital
# inputs. This exact sensor and pin comes back in Class 5 on the Random Rover.
import time
import board
import digitalio
from adafruit_debouncer import Debouncer

# --- Pushbutton (unchanged from tonight's main project) ---
button_pin = digitalio.DigitalInOut(board.GP2)
button_pin.direction = digitalio.Direction.INPUT
button_pin.pull = digitalio.Pull.UP
button = Debouncer(button_pin)

# --- IR obstacle sensor -- the module drives OUT itself, so no pull-up needed ---
ir_pin = digitalio.DigitalInOut(board.GP13)
ir_pin.direction = digitalio.Direction.INPUT
ir_sensor = Debouncer(ir_pin)

press_count = 0
obstacle_count = 0

print("Class 1 Homework 4 -- press the button, then wave your hand in front of the IR sensor.")

while True:
    button.update()
    if button.fell:
        press_count += 1
        print("press_count:", press_count)

    ir_sensor.update()
    # The sensor's OUT pin goes LOW when it sees an obstacle, so a debounced
    # "fell" event means an obstacle just appeared.
    if ir_sensor.fell:
        obstacle_count += 1
        print("obstacle_count:", obstacle_count)

    time.sleep(0.001)
```

#### What You Observe
**Test it:** Press the button a few times and confirm `press_count` still increments cleanly.
Then slowly move your hand toward the IR sensor from about arm's length — `obstacle_count` should
increment by exactly 1 per approach, with no double-counting, the same clean behavior you saw from
the debounced button tonight.

#### Real World Examples

* Automatic doors and elevator door edges use debounced IR/optical sensors so a single person
  walking through registers as one clean "obstacle present" event, not a flickering mess.
* Robot vacuums use several cheap IR proximity sensors around their edge as an always-on backup to
  their main sensors — the same redundancy idea your Random Rover will use in Class 5, pairing
  this sensor with the ultrasonic sensor and a physical bump switch.

### Homework 5 — Combination Lock: Using the KY-040's Built-In `SW` Pushbutton

**What this teaches:** *(Requires one extra jumper wire — no new part.)* Every KY-040 module has a
third signal besides `CLK` and `DT`: `SW`, a built-in pushbutton you get by pressing straight down
on the knob's shaft. You've had it wired since Class 1 started but never used it — tonight's
Section 3 even calls it out as "not used in this project." This exercise wires `SW` to its own
GPIO pin, debounces it with the same `Debouncer` class as the standalone pushbutton, and combines
all three signals (`CLK`/`DT` to pick a digit, `SW` to confirm it, the outer pushbutton to reset)
into a simple sequential state machine — a 3-digit combination lock.

**Wiring — add to tonight's circuit:**
* [Raspberry Pi Pico 2w Pinout][20]

| Pico 2 W Pin | Encoder Pin | Signal / Function |
| :------------- | :------------ | :-------------------- |
| `GP5` | `SW` | Encoder's built-in pushbutton, active-low with internal pull-up — pressing the knob shorts it to `GND` |

```python
# code.py - use the KY-040's built-in SW pushbutton as a
# THIRD independent input (never used until now) to build a simple 3-digit
# combination lock out of the button + rotary encoder already on your board.
import time
import board
import digitalio
import pwmio
from adafruit_debouncer import Debouncer

# --- Rotary encoder CLK/DT (unchanged from tonight's main project) ---
encoder_clk = digitalio.DigitalInOut(board.GP3)
encoder_clk.direction = digitalio.Direction.INPUT
encoder_clk.pull = digitalio.Pull.UP

encoder_dt = digitalio.DigitalInOut(board.GP4)
encoder_dt.direction = digitalio.Direction.INPUT
encoder_dt.pull = digitalio.Pull.UP

# --- NEW: the KY-040's own built-in pushbutton, wired to GP5 ---
# Every KY-040 has this third signal (SW) alongside CLK/DT, wired the same
# active-low way as the standalone pushbutton -- we just haven't used it
# until now. It debounces with the same Debouncer class as any other switch.
encoder_sw_pin = digitalio.DigitalInOut(board.GP5)
encoder_sw_pin.direction = digitalio.Direction.INPUT
encoder_sw_pin.pull = digitalio.Pull.UP
encoder_button = Debouncer(encoder_sw_pin)

# --- Outer pushbutton (unchanged) -- repurposed here as a RESET button ---
reset_pin = digitalio.DigitalInOut(board.GP2)
reset_pin.direction = digitalio.Direction.INPUT
reset_pin.pull = digitalio.Pull.UP
reset_button = Debouncer(reset_pin)

# --- LEDs (unchanged wiring) ---
status_led = digitalio.DigitalInOut(board.GP15)   # steady ON = correct code entered
status_led.direction = digitalio.Direction.OUTPUT
digit_led = pwmio.PWMOut(board.GP14, frequency=5000, duty_cycle=0)  # brightness previews the pending digit

CODE = [3, 1, 4]   # the 3-digit combination to match -- change this to whatever you like
entered = []       # digits confirmed so far this attempt

last_clk_state = encoder_clk.value
current_digit = 0

def show_digit(d):
    digit_led.duty_cycle = int(d / 9 * 65535)

print("Class 1 Homework 5 -- Combination Lock")
print("Turn the knob to pick a digit (0-9), press SW to lock it in.")
print("Press the outer button any time to reset. Code length:", len(CODE))

while True:
    reset_button.update()
    if reset_button.fell:
        entered = []
        status_led.value = False
        print("-- reset --")

    # Turn the knob to change the pending digit, 0-9, wrapping around.
    clk_state = encoder_clk.value
    if clk_state != last_clk_state:
        if encoder_dt.value != clk_state:
            current_digit = (current_digit + 1) % 10
        else:
            current_digit = (current_digit - 1) % 10
        show_digit(current_digit)
        print("pending digit:", current_digit)
    last_clk_state = clk_state

    # SW locks in the pending digit as the next entry in the sequence.
    encoder_button.update()
    if encoder_button.fell:
        entered.append(current_digit)
        print("locked in digit", current_digit, "-- entered so far:", entered)

        if len(entered) == len(CODE):
            if entered == CODE:
                print("CORRECT CODE -- unlocked!")
                status_led.value = True
            else:
                print("wrong code -- try again")
                status_led.value = False
            entered = []

    time.sleep(0.001)
```

#### What You Observe
**Test it:** Turn the knob and watch `digit_led`'s brightness step through 0-9 as the pending
digit changes. Press `SW` to lock in each digit — after three digits, entering `3, 1, 4` in order
should print `CORRECT CODE -- unlocked!` and turn `status_led` on steady; any other sequence should
print `wrong code` and leave it off. Press the outer button at any point to clear a partial entry.

#### Real World Examples

* Bike locks and gym locker locks with a turn-a-dial-then-confirm mechanism work on exactly this
    "set a value, lock it in, repeat" pattern.
* PIN-entry keypads on door locks and ATMs confirm one digit at a time rather than reading the
    whole code at once, so a wrong digit can be caught (or the entry cancelled) before it's complete.

### Homework 6 — Live Bar Gauge: Driving the TFT Display From the Encoder in Real Time

**What this teaches:** *(Requires the [TFT display][19] from the Pre-Class homework — see
[Section 2](#2-what-youll-need).)* The Pre-Class TFT homework drew a shape that animated on its
own, with no sensor input at all. This exercise instead redraws a `vectorio.Rectangle`'s **width**
every single loop, driven directly by the rotary encoder's live position — the same core pattern
behind any on-screen analog gauge: read a live value, then re-render the display to match it.

**Wiring — same TFT pins as the Pre-Class homework, plus tonight's encoder (already wired):**
* [Raspberry Pi Pico 2w Pinout][20]
* [Adafruit 1.14" 240x135 Color Newxie TFT Display Pinout][33]

| Pico 2 W Pin | TFT Pin | Signal / Function |
| :------------- | :-------- | :-------------------- |
| `3V3 OUT` | `VIN` / `V+` | Power |
| `GND` | `GND` / `G` | Common ground |
| `GP18` | `SCK` / `CL` | SPI clock |
| `GP19` | `MOSI` / `DA` | SPI data, Pico → display |
| `GP20` | `CS` | Chip select |
| `GP21` | `DC` | Data/Command select |
| `GP22` | `RST` / `BL` | Reset |

```python
# code.py - draw a live bar gauge on the TFT display,
# redrawn every loop from the rotary encoder's position -- unlike the
# Pre-Class TFT homework's self-running bounce animation, this bar is
# driven directly by live sensor input, the same pattern a real analog
# gauge or meter uses.
import time
import board
import busio
import digitalio
import displayio
import fourwire
import vectorio
import terminalio
from adafruit_display_text import label
from adafruit_st7789 import ST7789

# --- Rotary encoder (unchanged from tonight's main project) ---
encoder_clk = digitalio.DigitalInOut(board.GP3)
encoder_clk.direction = digitalio.Direction.INPUT
encoder_clk.pull = digitalio.Pull.UP

encoder_dt = digitalio.DigitalInOut(board.GP4)
encoder_dt.direction = digitalio.Direction.INPUT
encoder_dt.pull = digitalio.Pull.UP

# --- TFT setup -- same wiring and pins as the Pre-Class TFT homework ---
displayio.release_displays()
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19)
display_bus = fourwire.FourWire(spi, chip_select=board.GP20, command=board.GP21, reset=board.GP22)
display = ST7789(display_bus, width=240, height=135, rotation=270, rowstart=40, colstart=53)

main_group = displayio.Group()
display.root_group = main_group

# --- Numeric label above the bar ---
value_label = label.Label(terminalio.FONT, text="0", color=0xFFFFFF)
value_label.scale = 2
value_label.anchor_point = (0.5, 0.0)
value_label.anchored_position = (display.width // 2, 4)
main_group.append(value_label)

# --- The bar itself: a rectangle whose WIDTH we change every loop ---
BAR_MAX_WIDTH = display.width - 20
BAR_HEIGHT = 30
palette = displayio.Palette(1)
palette[0] = 0x00AAFF
bar = vectorio.Rectangle(pixel_shader=palette, width=1, height=BAR_HEIGHT, x=10, y=70)
main_group.append(bar)

encoder_position = 0
last_clk_state = encoder_clk.value

print("Class 1 Homework 6 -- turn the knob and watch the bar grow/shrink live.")

while True:
    clk_state = encoder_clk.value
    if clk_state != last_clk_state:
        if encoder_dt.value != clk_state:
            encoder_position += 1
        else:
            encoder_position -= 1
        encoder_position = max(0, min(100, encoder_position))

        # Redraw the bar's width AND the numeric label every time the
        # position changes -- read a live value, then re-render to match it.
        bar.width = max(1, int(encoder_position / 100 * BAR_MAX_WIDTH))
        value_label.text = str(encoder_position)
        print("encoder_position:", encoder_position)
    last_clk_state = clk_state

    time.sleep(0.001)
```

#### What You Observe
**Test it:** Turn the knob and watch the bar on the TFT grow and shrink in real time, in step with
the numeric label above it — same live-updating behavior as a volume or battery-level indicator.
You'll need `adafruit_display_text` and `adafruit_st7789` copied into `CIRCUITPY`'s `lib` folder,
the same way you copied libraries for the Pre-Class TFT homework; `displayio`, `fourwire`,
`vectorio`, and `terminalio` all ship with CircuitPython already.

#### Real World Examples

* On-screen volume and brightness bars on TVs and monitors redraw exactly like this — a bar whose
  length tracks a live control value, not a fixed animation.
* Battery-level indicators on phones, laptops, and game controllers are the same live-redrawn-bar
  pattern, just driven by a battery sensor instead of a knob.

### Homework 7 — Remote Dimmer: A Webpage Slider Controls the LED Over WiFi

**What this teaches:** *(Requires the Pico's built-in WiFi radio and `adafruit_httpserver` — no
new part, but reuses the WiFi setup from the Pre-Class homework.)* The Pre-Class WiFi homework
built a webpage that only *reported* the LED's status — a one-way, read-only connection from Pico
to browser. This exercise reverses that: an `<input type="range">` slider on the webpage actually
**sets** the Pico's hardware state, the first two-way (browser-to-Pico) control in the course.

```python
# code.py - a webpage slider sets the encoder LED's
# brightness over WiFi -- the first TWO-WAY control in the course. The
# Pre-Class WiFi homework only reported LED status (read-only); here the
# browser actually changes hardware state on the Pico.
import board
import pwmio
import wifi
import socketpool
import os
from adafruit_httpserver import Server, Request, Response, GET

# --- Load WiFi credentials from settings.toml (same file/pattern as the ---
# --- Pre-Class WiFi homework -- reuse it if you already created one) ---
ap_ssid = os.getenv("CIRCUITPY_WIFI_AP_SSID")
ap_password = os.getenv("CIRCUITPY_WIFI_AP_PASSWORD")

# --- PWM LED (same GP14 wiring as tonight's main project) ---
encoder_led = pwmio.PWMOut(board.GP14, frequency=5000, duty_cycle=0)
brightness_percent = 0  # 0-100, whatever the webpage last set

wifi.radio.start_ap(ssid=ap_ssid, password=ap_password)
print("Access point started. Connect to:", ap_ssid)
print("Then visit http://" + str(wifi.radio.ipv4_address_ap) + "/ in a browser")

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)

@server.route("/", GET)
def base(request: Request):
    html = f"""
    <html>
      <body style="font-family: sans-serif; text-align: center; margin-top: 3em;">
        <h1>LED Brightness: {brightness_percent}%</h1>
        <form action="/set" method="get">
          <input type="range" name="value" min="0" max="100" value="{brightness_percent}"
                 onchange="this.form.submit()">
        </form>
      </body>
    </html>
    """
    return Response(request, html, content_type="text/html")

@server.route("/set", GET)
def set_brightness(request: Request):
    # The slider's value arrives as a query string, e.g. /set?value=42 --
    # this is the Pico being COMMANDED by the browser, not just reporting
    # its own state the way the Pre-Class homework did.
    global brightness_percent
    brightness_percent = int(request.query_params.get("value", brightness_percent))
    encoder_led.duty_cycle = int(brightness_percent / 100 * 65535)
    print("brightness set to:", brightness_percent)
    return base(request)

server.start(str(wifi.radio.ipv4_address_ap))

while True:
    server.poll()
```

#### What You Observe
**Test it:** Connect a phone or laptop to the `<your-name>` network (same `settings.toml` as the
Pre-Class WiFi homework) and load the printed address. Drag the slider — the physical LED's
brightness should change immediately, and the page should reload showing the new percentage.

#### Real World Examples

* Smart-bulb apps like Philips Hue or LIFX work exactly this way — a slider in the app sends a
    command over the local network that actually changes the bulb's brightness.
* Any browser-based device dashboard (a 3D printer's web interface, a smart thermostat's local
    admin page) uses the same request-triggers-hardware-change pattern.

### Homework 8 — Countdown Timer: Encoder Sets Duration, Button Starts, LED Counts Down

**What this teaches:** Homework 1 measured an elapsed duration *after the fact* — you found out how
long a press lasted only once it ended. This exercise runs a live "armed → running → done" state
machine: the encoder sets a duration up front, the button starts the clock, and the PWM LED's
brightness scales down in real time to show *time remaining*, not a value you set once.

```python
# code.py - encoder sets a countdown duration, the
# button starts it, and the PWM LED dims in real time as it counts down --
# a live "armed / running / done" state machine, unlike Homework 1's
# after-the-fact elapsed-time measurement.
import time
import board
import digitalio
import pwmio
from adafruit_debouncer import Debouncer

encoder_clk = digitalio.DigitalInOut(board.GP3)
encoder_clk.direction = digitalio.Direction.INPUT
encoder_clk.pull = digitalio.Pull.UP

encoder_dt = digitalio.DigitalInOut(board.GP4)
encoder_dt.direction = digitalio.Direction.INPUT
encoder_dt.pull = digitalio.Pull.UP

button_pin = digitalio.DigitalInOut(board.GP2)
button_pin.direction = digitalio.Direction.INPUT
button_pin.pull = digitalio.Pull.UP
button = Debouncer(button_pin)

countdown_led = pwmio.PWMOut(board.GP14, frequency=5000, duty_cycle=0)  # dims as time runs out
done_led = digitalio.DigitalInOut(board.GP15)                          # flashes at zero
done_led.direction = digitalio.Direction.OUTPUT

STATE_SET = "set"
STATE_RUNNING = "running"
STATE_DONE = "done"
state = STATE_SET

duration_seconds = 10
last_clk_state = encoder_clk.value
start_time = None

print("Class 1 Homework 8 -- turn the knob to pick seconds (1-60), press the button to start.")

while True:
    button.update()

    if state == STATE_SET:
        clk_state = encoder_clk.value
        if clk_state != last_clk_state:
            if encoder_dt.value != clk_state:
                duration_seconds += 1
            else:
                duration_seconds -= 1
            duration_seconds = max(1, min(60, duration_seconds))
            print("duration set to:", duration_seconds, "seconds")
        last_clk_state = clk_state
        countdown_led.duty_cycle = 65535  # full brightness while armed, not yet running

        if button.fell:
            state = STATE_RUNNING
            start_time = time.monotonic()
            print("-- starting countdown:", duration_seconds, "seconds --")

    elif state == STATE_RUNNING:
        elapsed = time.monotonic() - start_time
        remaining = max(0.0, duration_seconds - elapsed)
        # Brightness scales DOWN as time runs out -- full at the start, off at zero.
        countdown_led.duty_cycle = int((remaining / duration_seconds) * 65535)

        if remaining <= 0:
            state = STATE_DONE

    elif state == STATE_DONE:
        # Flash the done LED a few times, then reset back to STATE_SET.
        for _ in range(5):
            done_led.value = True
            time.sleep(0.15)
            done_led.value = False
            time.sleep(0.15)
        print("-- time's up! --")
        state = STATE_SET

    time.sleep(0.01)
```

#### What You Observe
**Test it:** Turn the knob to set a duration (try something short like 5 seconds first), press the
button to start, and watch `countdown_led` dim smoothly from full brightness to off over exactly
that many seconds. `done_led` should flash five times when it hits zero, then the timer
automatically resets so you can set and start another countdown.

#### Real World Examples

* Microwave and oven countdown timers work the same way: set a duration, start it, watch a visual
    indicator (a display, sometimes a light) track the time remaining until it finishes.
* Classroom or game "time's up" countdown lights use the same set-then-run state machine, often
    dimming or changing color as time runs low before a final alert.

### Homework 9 — NVM Event Log: A Ring Buffer of the Last 10 Events

**What this teaches:** Homework 3 stored a single number in `microcontroller.nvm` — a press count.
This exercise stores a small **ring buffer** of the last 10 button-press and encoder-turn events
instead, a structured log of multiple records rather than one value, printed back out in order at
boot. This is a different, more general use of persistent storage: not "remember one number," but
"remember recent history."

```python
# code.py - store the last 10 button/encoder events as
# a RING BUFFER in NVM -- a structured log of multiple records, not a
# single stored number like Homework 3's press counter.
import time
import board
import digitalio
import microcontroller
from adafruit_debouncer import Debouncer

button_pin = digitalio.DigitalInOut(board.GP2)
button_pin.direction = digitalio.Direction.INPUT
button_pin.pull = digitalio.Pull.UP
button = Debouncer(button_pin)

encoder_clk = digitalio.DigitalInOut(board.GP3)
encoder_clk.direction = digitalio.Direction.INPUT
encoder_clk.pull = digitalio.Pull.UP

encoder_dt = digitalio.DigitalInOut(board.GP4)
encoder_dt.direction = digitalio.Direction.INPUT
encoder_dt.pull = digitalio.Pull.UP

EVENT_PRESS = 1
EVENT_CW = 2
EVENT_CCW = 3
EVENT_NAMES = {EVENT_PRESS: "button press", EVENT_CW: "encoder CW", EVENT_CCW: "encoder CCW"}

# NVM layout: first 4 bytes reserved (e.g. for Homework 3's press counter,
# if you did that one too), then 4 bytes for a running total-events-ever
# count, then 10 one-byte slots -- one event code per slot.
NVM_BASE = 4
TOTAL_WRITES_OFFSET = NVM_BASE
SLOTS_OFFSET = NVM_BASE + 4
SLOT_COUNT = 10

def load_total_writes():
    return int.from_bytes(microcontroller.nvm[TOTAL_WRITES_OFFSET:TOTAL_WRITES_OFFSET + 4], "big")

def save_total_writes(value):
    microcontroller.nvm[TOTAL_WRITES_OFFSET:TOTAL_WRITES_OFFSET + 4] = value.to_bytes(4, "big")

def log_event(event_code):
    # The write position wraps around every SLOT_COUNT events -- once full,
    # each new event overwrites the OLDEST one, which is what makes this a
    # ring buffer instead of a list that eventually runs out of room.
    total = load_total_writes()
    slot = total % SLOT_COUNT
    microcontroller.nvm[SLOTS_OFFSET + slot] = event_code
    save_total_writes(total + 1)
    print("logged:", EVENT_NAMES[event_code])

def print_log():
    total = load_total_writes()
    print("-- event log (oldest to newest), total events ever:", total, "--")
    count_to_show = min(total, SLOT_COUNT)
    oldest_slot = total % SLOT_COUNT if total >= SLOT_COUNT else 0
    for i in range(count_to_show):
        slot = (oldest_slot + i) % SLOT_COUNT
        event_code = microcontroller.nvm[SLOTS_OFFSET + slot]
        print("  " + EVENT_NAMES.get(event_code, "unknown"))

print("Class 1 Homework 9 -- press the button or turn the knob.")
print("Log below is from BEFORE this boot (empty the very first run):")
print_log()

last_clk_state = encoder_clk.value

while True:
    button.update()
    if button.fell:
        log_event(EVENT_PRESS)

    clk_state = encoder_clk.value
    if clk_state != last_clk_state:
        if encoder_dt.value != clk_state:
            log_event(EVENT_CW)
        else:
            log_event(EVENT_CCW)
    last_clk_state = clk_state

    time.sleep(0.001)
```

#### What You Observe
**Test it:** Press the button and turn the knob a handful of times (more than 10 total, to prove
the ring wraps around), then unplug the board and plug it back in. The log printed at boot should
show only the **last 10** events, oldest to newest — earlier ones should have been overwritten, not
kept. Confirm `total events ever` keeps climbing across reboots even though the visible log stays
capped at 10.

#### Real World Examples

* Vehicle "black box" event recorders keep only the most recent stretch of data (crash sensors,
    speed, braking) in a fixed-size buffer, overwriting older data as new events come in.
* Appliance fault-code logs (washing machines, HVAC systems, industrial equipment) store the last N
    error codes for a technician to read later, the same fixed-size, oldest-overwritten pattern.

## References

* [What Is Switch Bounce & How to Implement Debounce][01] — background on the physical cause of
    switch bounce
* [Python Debouncer Library for Buttons and Sensors][02] — overview of `adafruit_debouncer`
* [adafruit_debouncer Advanced Debouncing guide][03] — the `Debouncer.update()` / `.rose` /
    `.fell` pattern used in this script
* [How to Use a Rotary Encoder with the Raspberry Pi (The Pi Hut)][04] — KY-040 wiring and
    quadrature background
* [TFT vs. LCD displays][19] — background on the TFT display used in Homework 6
* [GPIO pinout and pin function guide for the Raspberry Pi Pico 2 W][20] — used throughout the
    Homework Assignments' wiring tables
* [Adafruit 1.14" 240x135 Color Newxie TFT Display Pinout][33] — TFT pinout reference for
    Homework 6
* [IR Obstacle Avoidance Sensor Pinout][34] — sensor pinout reference for Homework 4

---



[01]:https://www.picotech.com/library/articles/blog/what-is-switch-bounce-how-to-implement-debounce
[02]:https://learn.adafruit.com/debouncer-library-python-circuitpython-buttons-sensors/overview
[03]:https://learn.adafruit.com/debouncer-library-python-circuitpython-buttons-sensors/advanced-debouncing
[04]:https://thepihut.com/blogs/raspberry-pi-tutorials/how-to-use-a-rotary-encoder-with-the-raspberry-pi
[05]:https://en.wikipedia.org/wiki/Non-volatile_memory
[19]:https://www.proculustech.com/tft-vs-lcd
[20]:https://pico2w.pinout.xyz/
[33]:https://cdn-learn.adafruit.com/downloads/pdf/adafruit-1-14-240x135-color-newxie-tft-display.pdf
[34]:https://docs.sunfounder.com/projects/umsk/en/latest/01_components_basic/08-component_ir_obstacle.html
