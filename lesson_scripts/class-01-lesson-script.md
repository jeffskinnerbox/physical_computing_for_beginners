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
| :---------- | :--------: | :---------------------- |
| Raspberry Pi Pico 2 W (with header) | 1 | Runs your CircuitPython code |
| Tactile push button switch | 1 | Digital input — the thing you press |
| KY-040 rotary encoder module | 1 | Rotational input — the knob you turn |
| LED | 2 | One lights up on button press, one dims/brightens with the knob |
| Current-limiting resistor (220-330 ohm) | 2 | Protects each LED from too much current |
| Breadboard (830-point) | 1 | Where you build the circuit |
| Dupont jumper wires | ~10 | Point-to-point connections |
| USB cable | 1 | Powers the Pico and carries the serial console |
| Laptop with Mu or Thonny | 1 | Where you write/save code and read the serial console |

**Additional components for the Homework Assignments** (Section 9) — not needed for tonight's class
itself, only if you choose to do Homework 4 at home:

| Component | Quantity | Purpose (Homework #) |
| :---------- | :--------: | :---------------------- |
| IR Obstacle Avoidance Sensor | 1 | Digital proximity detection run through the same `Debouncer` pattern as the button (Homework 4) — also used on the Random Rover in Class 5 |

Homework 1 (long-press detection), Homework 2 (encoder acceleration), and Homework 3 (persistent
press counter) need no additional hardware beyond the button + rotary encoder circuit already on
your breadboard.

## 3. Meet the Hardware

**Pushbutton switch.** A pushbutton is just two metal contacts that touch when you press it and
separate when you release it. It has no "smarts" — it's a plain on/off switch. In CircuitPython
you read it with the `digitalio` module, which lets you treat any GPIO pin as a simple input or
output. We wire the button so one leg goes to a GPIO pin and the other leg goes to `GND`
(ground), and we turn on the Pico's **internal pull-up resistor** on that pin. That means the pin
reads `True` (high) when the button is *not* pressed, and `False` (low) when it *is* pressed —
this wiring style is called **active-low**, and it's the standard, recommended way to wire a
simple switch to a microcontroller because it needs no external resistor for the switch itself.

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
| `3V3` | Encoder `+`/VCC power |
| `GND` | Encoder `GND`, button's second leg, both LED cathodes |

## 4. Build It: Phase 1 — See the Bounce

### Wiring for this phase

This is the complete wiring for the whole project — nothing changes between Phase 1 and Phase 2,
only the code does.

| Component | Pico 2 W Pin |
| :---------- | :------------- |
| Pushbutton switch, one leg | `GP2` |
| Pushbutton switch, other leg | `GND` |
| Rotary encoder `CLK` | `GP3` |
| Rotary encoder `DT` | `GP4` |
| Rotary encoder `+`/VCC | `3V3` |
| Rotary encoder `GND` | `GND` |
| Button LED anode, through resistor | `GP15` |
| Button LED cathode | `GND` |
| Encoder brightness LED anode, through resistor | `GP14` |
| Encoder brightness LED cathode | `GND` |

Before writing any code, trace your own wiring against this table out loud — wiring mistakes are
much faster to catch now than after you're staring at confusing code output.

### What this code does

This first version reads the button and encoder in the most straightforward way possible: check
the pin, and if it changed, count it. No filtering, no waiting, nothing fancy. It's deliberately
naive so you can see exactly what goes wrong.

### The code

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

# --- Rotary encoder setup ---
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

# --- Encoder LED setup ---
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
    # --- Button: count every time the pin reads "pressed" (False) ---
    if not button.value:
        press_count += 1
        button_led.value = True
        print("RAW press_count:", press_count)
    else:
        button_led.value = False

    # --- Encoder: naive quadrature read ---
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
MIN_STEP_INTERVAL = 0.02

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

## 6. Troubleshooting Guide

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

## 7. Put It All Together

This is the finished project in one place — everything you need to build it from scratch without
following the phase-by-phase walkthrough above.

### Complete wiring

| Component | Pico 2 W Pin |
| :---------- | :------------- |
| Pushbutton switch, one leg | `GP2` |
| Pushbutton switch, other leg | `GND` |
| Rotary encoder `CLK` | `GP3` |
| Rotary encoder `DT` | `GP4` |
| Rotary encoder `+`/VCC | `3V3` |
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

## 8. What You Learned

You built your first real physical computing circuit and watched a genuine hardware problem show
up on your own screen — not just heard about it. Specifically, you now know:

* How to wire and read a digital input (`digitalio`) with a pull-up resistor, active-low
* How to read a rotary encoder's two-signal quadrature output to detect direction
* How to control an LED's brightness with PWM (`pwmio`), not just turn it on/off
* What switch bounce physically is, and why a microcontroller sees it as many events instead of
    one
* How to fix it in software two different ways: `adafruit_debouncer.Debouncer` for a simple
    on/off input, and a minimum-time-interval filter for a multi-signal input like an encoder

Leave this circuit on your breadboard — you'll use the rotary encoder again, completely unchanged,
in Class 6 as a live speed control for your robot car. Next class, you'll meet a new kind of
"noisy real-world signal" problem: an ultrasonic distance sensor, wired fresh on brand-new pins,
with today's circuit untouched right next to it.

----
## 9. Homework Assignment

Today's circuit and code stay on your breadboard — the exercises below are **homework, not
required class content**, and each one builds directly on the button + rotary encoder circuit and
the debouncing patterns you just learned tonight. Do them in any order. For each one you'll find:
what the code teaches and why it's useful, the full commented code to save as `code.py` on your
`CIRCUITPY` drive, what to expect when you test it, and a couple of real-world examples of where
this exact technique shows up outside a classroom. Only Homework 4 needs a part beyond tonight's
circuit — see [Section 2](#2-what-youll-need).

### Homework 1 — Long-Press vs. Short-Press Detection

**What this teaches:** So far you've only asked the button one question: "did you just get
pressed?" (`.fell`). Real buttons usually need to answer a second question too: "*how long* were
you held?" This exercise uses `Debouncer.fell` and `Debouncer.rose` together with
`time.monotonic()` to time the gap between the press and the release, then classifies the result as
a quick tap or a long hold.

```python
# code.py - Class 1 Homework 1: distinguish a quick tap from a held press
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

**Test it:** Tap the button quickly — you should see `short press`. Hold it down for over half a
second before releasing — you should see `LONG PRESS` instead, with the actual hold time printed.
Try changing `LONG_PRESS_SECONDS` and see how it changes where the line falls.

**Real-world examples:**

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
# code.py - Class 1 Homework 2: rotary encoder that jumps by more than 1
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

**Test it:** Turn the knob one slow detent at a time — `encoder_position` should climb by 1 each
time, same as tonight's Phase 2. Now spin it quickly through several detents — watch
`step_size` jump to 2 or 5 and `encoder_position` (and the LED brightness) race up much faster.

**Real-world examples:**

* Mouse and trackpad scroll wheels accelerate the same way — a slow scroll moves a few lines, a
    fast flick jumps a whole page.
* Car radio and thermostat volume/temperature knobs often speed up their response the faster you
    turn them, so a big adjustment doesn't take dozens of individual clicks.

### Homework 3 — Persistent Press Counter (Survives Power-Off)

**What this teaches:** Every variable in your code so far has lived in RAM, which means it resets
to its starting value the instant the board loses power — unplug it and `press_count` goes back to
0. This exercise introduces `microcontroller.nvm`, a small block of memory built into the chip that
is specifically designed to *keep* its contents across power loss and resets. You'll store
`press_count` there instead of in a normal variable, so the count survives being unplugged.

```python
# code.py - Class 1 Homework 3: press_count that survives unplugging the board
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

**Test it:** Note the starting `press_count` printed at boot (it should be 0 the very first run),
press the button a handful of times, then unplug the USB cable and plug it back in. The count
printed at startup should now match the last value you saw before unplugging — not reset to 0.
NVM has a large but finite number of writes (roughly 100,000 cycles), plenty for this exercise, and
it's separate from `code.py` itself — re-flashing CircuitPython firmware does clear it.

**Real-world examples:**

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

| Component | Pico 2 W Pin |
| :---------- | :------------- |
| IR sensor `VCC` | `3V3` (or `VBUS`) |
| IR sensor `GND` | `GND` |
| IR sensor `OUT` | `GP13` |

```python
# code.py - Class 1 Homework 4: run the IR Obstacle Avoidance Sensor through
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

**Test it:** Press the button a few times and confirm `press_count` still increments cleanly.
Then slowly move your hand toward the IR sensor from about arm's length — `obstacle_count` should
increment by exactly 1 per approach, with no double-counting, the same clean behavior you saw from
the debounced button tonight.

**Real-world examples:**

* Automatic doors and elevator door edges use debounced IR/optical sensors so a single person
    walking through registers as one clean "obstacle present" event, not a flickering mess.
* Robot vacuums use several cheap IR proximity sensors around their edge as an always-on backup to
    their main sensors — the same redundancy idea your Random Rover will use in Class 5, pairing
    this sensor with the ultrasonic sensor and a physical bump switch.

## References

* [What Is Switch Bounce & How to Implement Debounce][01] — background on the physical cause of
    switch bounce
* [Python Debouncer Library for Buttons and Sensors][02] — overview of `adafruit_debouncer`
* [adafruit_debouncer Advanced Debouncing guide][03] — the `Debouncer.update()` / `.rose` /
    `.fell` pattern used in this script
* [How to Use a Rotary Encoder with the Raspberry Pi (The Pi Hut)][04] — KY-040 wiring and
    quadrature background

---

[01]:https://www.picotech.com/library/articles/blog/what-is-switch-bounce-how-to-implement-debounce
[02]:https://learn.adafruit.com/debouncer-library-python-circuitpython-buttons-sensors/overview
[03]:https://learn.adafruit.com/debouncer-library-python-circuitpython-buttons-sensors/advanced-debouncing
[04]:https://thepihut.com/blogs/raspberry-pi-tutorials/how-to-use-a-rotary-encoder-with-the-raspberry-pi
