# Lesson Plan: Class 1 — Push Button Switch and Rotary Encoder

* **Class:** 1 of 6 (plus Pre-Class)
* **Phase:** Phase 1 — Inputs (Class 1-2: reliable sensing)
* **Duration:** ~2 hours (120 min)
* **Prerequisites from prior Classes:** Pre-Class completed — every student has CircuitPython
  flashed on their Raspberry Pi Pico 2 W, the Mu or Thonny editor installed, the Adafruit
  CircuitPython Library Bundle available, and has successfully run a first program (blinking
  LED + heartbeat count over serial). Students should be comfortable finding the CIRCUITPY drive,
  saving a file as `code.py`, and opening the serial console.

---

## 1. Class Overview

This is the first Class of Phase 1 (Inputs) and the first "real" physical computing build of the
course — everything before this was proving the toolchain works. Students wire a pushbutton
switch and a KY-040 rotary encoder to their Pico 2 W, and use them to control two LEDs: one turns
on with the button, the other's brightness is set by the encoder. The twist is pedagogical: the
class first builds the circuit **without** any debouncing, watches the switch and encoder produce
erratic, non-deterministic readings on the serial console, and only then adds a software debounce
routine to fix it. By the end of the Class, students will have seen the exact problem debouncing
solves — not just been told it exists — and will have a working, debounced input circuit that
stays on the breadboard, unchanged, for the rest of the course (it comes back as a live speed
control in Class 6's stretch goal).

## 2. Learning Goals

* Wire a pushbutton switch and a KY-040 rotary encoder to the Pico 2 W, each driving its own LED
* Explain, in plain language, what switch bounce is and why it confuses a microcontroller
* Read raw (bouncy) switch and encoder signals and observe the erratic serial console output
* Apply the `adafruit_debouncer.Debouncer` class to a switch, and a minimum-step-interval
  software debounce to the encoder, and compare the before/after console output
* Propose, as a group, an algorithm for solving switch bounce before being shown the library
  solution

## 3. Preparation Checklist

* **1-2 days before:** Confirm every student's Pico 2 W still boots to the CIRCUITPY drive and
  the serial console connects — spot-check the Pre-Class milestone didn't regress. (~15 min)
* **1-2 days before:** Verify `adafruit_debouncer` is present in the Adafruit CircuitPython
  Library Bundle folder each student installed in the Pre-Class; have a few copies on a USB
  stick as backup. (~10 min)
* **Day of, before students arrive:**
  * Set out one pushbutton switch, one KY-040 rotary encoder, two LEDs, two current-limiting
    resistors, and a breadboard at each workstation (see Materials & Components below).
  * Pre-build one reference circuit (button + encoder + 2 LEDs) at the instructor bench and test
    both `class-1-code-1.py` (no debounce) and `class-1-code-2.py` (debounced) end-to-end.
    (~20 min)
  * Project the instructor's serial console output so the whole class can see the bouncy vs.
    debounced comparison live. (~5 min)
  * Have spare pushbuttons and encoders on hand — these are the two most failure-prone parts in
    this Class (dead switches, encoders with a broken detent).
* **Have ready:** A short list of discussion prompts for the "should we fix this in hardware or
  software?" conversation (see Direct Teaching below).

## 4. Materials & Components

Per-student unless noted. Component names only — see the course Bill of Materials for costs,
quantities, and sourcing.

| Component | Purpose This Class |
| :---------- | :-------------------- |
| Raspberry Pi Pico 2 W (with header) | Microcontroller running CircuitPython |
| Tactile Push Button Switch | Digital input; source of switch-bounce demonstration |
| KY-040 Rotary Encoder Module | Rotational input; source of encoder-bounce demonstration |
| 2x LED | Visual output: one for the button, one (PWM) for the encoder |
| 2x current-limiting resistor (e.g. 220-330 ohm) | Protects the LEDs from the Pico's GPIO pins |
| Breadboard (830-point) | Circuit assembly surface |
| Dupont jumper wires (shared) | Point-to-point wiring |
| USB cable (student-supplied, from Pre-Class) | Power + serial connection to laptop |
| Windows 11 laptop with Mu or Thonny (student-supplied) | Edit and run CircuitPython code |
| Emo Smart Robot Car Chassis Kit | Optional: begin assembly if time remains |

## 5. Class Timeline

### 5a. Warm-up / Hook — ~10 min

**What to do:** Have every student plug in their Pico 2 W and re-run their Pre-Class heartbeat
program to confirm the toolchain still works. Ask 2-3 students to briefly describe what they
built in the Pre-Class and what surprised them about CircuitPython.

**What to say:** "Last time, you got your board and your laptop talking to each other. Today
that connection stops being a demo — you're going to use it to read something physical: a button
press and a knob turn. And you're going to watch, on your own screen, why that's harder than it
sounds."

**What to watch for:** Students whose Pico no longer shows a CIRCUITPY drive (loose cable, wrong
USB port, or firmware got corrupted) — pull them aside and re-flash quickly rather than losing
the room's momentum.

**Time check:** If more than 2-3 boards need re-flashing, do it during Guided Practice instead of
holding up the whole class now.

### 5b. Introduction — ~10 min

**What to do:** Introduce today's two new parts (pushbutton switch, KY-040 rotary encoder) and
the new concept (switch bounce / debouncing). Hold up each part and pass a spare around.

**What to say:**

* "These two parts look simple — a button and a knob. But electrically, they're actually kind of
  messy, and today you'll see that with your own eyes on the serial console."
* "The core idea for today is **debouncing** — cleaning up a noisy digital signal so it means
  what you think it means."
* "Why does this matter beyond an LED? Imagine this switch was telling a motor to stop. A signal
  that flickers on-off-on-off for a few milliseconds isn't just annoying anymore — it's a safety
  problem."

**Questions to ask students:** "Where else, outside of this classroom, do you press a button and
expect exactly one thing to happen?" (elevator buttons, keyboard keys, doorbells — all of these
debounce internally.)

### 5c. Direct Teaching — ~10 min

No code yet — diagrams and discussion only, using the whiteboard or projected diagram.

**Concept 1 — What switch bounce actually is (Theory of Operation, brief).**
A mechanical switch or encoder contact does not close cleanly. When two metal contacts come
together, they physically bounce apart and re-touch several times over a few milliseconds before
settling — the same way a dropped bouncy ball doesn't stop on first contact with the floor. A
microcontroller samples GPIO pins fast enough (microseconds) to see every one of those bounces as
a separate press. One human button press can register as 5, 10, or more electrical transitions.

*Step-by-step decomposition of what happens without debouncing:*

1. Finger presses the button.
2. Metal contact touches, bounces apart, re-touches — repeating for ~5-20 milliseconds (varies
   by switch quality and how hard/fast it's pressed).
3. The Pico's digital input pin samples state every loop iteration (much faster than 1ms).
4. Each bounce transition is read as a distinct press/release event.
5. Code that increments a counter "on each press" instead counts 5-10+ presses per human press.
6. The rotary encoder does the same thing on both its CLK and DT contacts as the shaft turns
   past each detent, so a single "click" can register as several encoder steps, sometimes even
   registering a step in the wrong direction.

**Concept 2 — Where should this be fixed?**
Ask the class: hardware (a capacitor across the switch) or software (code that ignores rapid
repeated transitions)? Both are valid engineering answers — point out the software fix costs
nothing extra in parts and is easy to tune, which is why it's the default for a hobbyist project
like this one. This Class fixes it in software.

**Concept 3 — Same fix, two different devices.**
Ask: "The switch and the encoder are different kinds of devices, but the same 'wait a moment and
see if the signal settles' technique fixes both. What do they have in common that makes one idea
work for both?" (Answer to draw out: both are mechanical contacts producing a digital on/off
signal — bounce is a property of *any* mechanical contact, not something specific to buttons.)

### 5d. Guided Practice — ~40 min

Instructor builds along on the projector; students wire up and test in parallel.

**Wiring — first circuit of the course.** Leave this circuit on the breadboard after today; the
rotary encoder is reused, unchanged, in Class 6's stretch goal as a live speed control.

| Component | Pico 2 W Pin |
| :---------- | :------------- |
| Pushbutton switch (one leg, other leg to GND) | `GP2` |
| Rotary encoder `CLK` | `GP3` |
| Rotary encoder `DT` | `GP4` |
| Button LED (through resistor) | `GP15` |
| Encoder brightness LED (through resistor, PWM) | `GP14` |
| Rotary encoder `+`/VCC | `3V3` |
| Rotary encoder `GND`, switch GND leg, LED cathodes | `GND` |

**Checkpoint 1:** Before writing any code, have every pair trace their own wiring against the
table above out loud to a neighbor. Wiring mistakes found now save debugging time later.

**Step 1 — no debouncing, see the problem.**
Load `class-1-code-1.py` (save as `code.py`). This version reads the raw button and encoder
state every loop and prints counts to the serial console with **no** debouncing at all.

```python
# class-1-code-1.py
# No debouncing -- demonstrates raw switch/encoder bounce.
import time
import board
import digitalio
import pwmio

# Button input, active-low with internal pull-up
button = digitalio.DigitalInOut(board.GP2)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# Rotary encoder CLK/DT, both active-low with internal pull-up
encoder_clk = digitalio.DigitalInOut(board.GP3)
encoder_clk.direction = digitalio.Direction.INPUT
encoder_clk.pull = digitalio.Pull.UP
encoder_dt = digitalio.DigitalInOut(board.GP4)
encoder_dt.direction = digitalio.Direction.INPUT
encoder_dt.pull = digitalio.Pull.UP

# Button LED, plain on/off
button_led = digitalio.DigitalInOut(board.GP15)
button_led.direction = digitalio.Direction.OUTPUT

# Encoder brightness LED, PWM so we can dim/brighten it
encoder_led = pwmio.PWMOut(board.GP14, frequency=5000, duty_cycle=0)

press_count = 0
encoder_position = 0
last_clk_state = encoder_clk.value

print("Class 1 -- raw (bouncy) readings starting...")

while True:
    # --- Button: count every falling edge, no filtering ---
    if not button.value:
        press_count += 1
        button_led.value = True
        print("RAW press_count:", press_count)
    else:
        button_led.value = False

    # --- Encoder: naive quadrature read, no filtering ---
    clk_state = encoder_clk.value
    if clk_state != last_clk_state:
        if encoder_dt.value != clk_state:
            encoder_position += 1
        else:
            encoder_position -= 1
        encoder_position = max(0, min(100, encoder_position))
        encoder_led.duty_cycle = int(encoder_position / 100 * 65535)
        print("RAW encoder_position:", encoder_position)
    last_clk_state = clk_state

    time.sleep(0.001)  # sample fast on purpose -- this is what exposes the bounce
```

**What to watch for:** This is the moment students should see `press_count` jump by 3, 7, even
12 on a single press, and the encoder position jitter or briefly reverse direction on a single
detent click. Let it be messy — that's the point. Ask: "Did you press it once? What did the
console say?"

**Step 2 — add debouncing, fix the problem.**
Load `class-1-code-2.py`. This uses `adafruit_debouncer.Debouncer` on the button (requires
`adafruit_debouncer` in `/lib` from the Library Bundle) and a minimum-step-interval software
debounce on the encoder.

```python
# class-1-code-2.py
# Debounced version -- same wiring as class-1-code-1.py.
import time
import board
import digitalio
import pwmio
from adafruit_debouncer import Debouncer

# Button input + debouncer
button_pin = digitalio.DigitalInOut(board.GP2)
button_pin.direction = digitalio.Direction.INPUT
button_pin.pull = digitalio.Pull.UP
button = Debouncer(button_pin)

# Rotary encoder CLK/DT, both active-low with internal pull-up
encoder_clk = digitalio.DigitalInOut(board.GP3)
encoder_clk.direction = digitalio.Direction.INPUT
encoder_clk.pull = digitalio.Pull.UP
encoder_dt = digitalio.DigitalInOut(board.GP4)
encoder_dt.direction = digitalio.Direction.INPUT
encoder_dt.pull = digitalio.Pull.UP

# Button LED, plain on/off
button_led = digitalio.DigitalInOut(board.GP15)
button_led.direction = digitalio.Direction.OUTPUT

# Encoder brightness LED, PWM so we can dim/brighten it
encoder_led = pwmio.PWMOut(board.GP14, frequency=5000, duty_cycle=0)

press_count = 0
encoder_position = 0
last_clk_state = encoder_clk.value
last_step_time = 0.0
MIN_STEP_INTERVAL = 0.02  # seconds -- ignore encoder edges closer together than this

print("Class 1 -- debounced readings starting...")

while True:
    # --- Button: Debouncer.update() must run every loop ---
    button.update()
    if button.fell:
        press_count += 1
        print("DEBOUNCED press_count:", press_count)
    button_led.value = not button.value  # active-low: pressed == True LED on

    # --- Encoder: same quadrature read, but ignore edges that arrive too fast ---
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

**Checkpoint 2:** Every pair should be able to press the button once and see `press_count`
increase by exactly 1, and turn the encoder one detent and see `encoder_position` change by
exactly 1, in the correct direction.

**What "done" looks like for this segment:** Both LEDs respond correctly, and the console shows
clean, one-per-action counts with `class-1-code-2.py` running.

### 5e. Independent Work — ~40 min

**What to do:** Students (in pairs where possible) run both versions side-by-side (or back to
back) on their own boards, capture a short console log of each, and discuss what they observe.
Faster pairs can:

* Tune `MIN_STEP_INTERVAL` up and down and observe the tradeoff between missed fast turns and
  residual jitter.
* Try disconnecting the debouncer's `update()` call from the loop and observe it breaks again.
* Begin unboxing and dry-fitting the Emo Smart Robot Car Chassis Kit (no wiring yet) if both the
  switch and encoder milestone are working.

**What to watch for:** The most common failure at this stage is a working button but a
non-responsive encoder LED — almost always a `CLK`/`DT` swap or a loose STEMMA/jumper connection,
not a code bug. Check wiring before code.

**Time check:** At the 30-minute mark, do a quick show-of-hands: "Who has clean debounced output
on both the button and the encoder?" Redirect instructor attention to pairs still stuck.

### 5f. Closing / Wrap-up — ~10 min

**What to do:** Ask 2-3 volunteers to demo their side-by-side bouncy-vs-debounced console output
to the group (this is also the Class milestone — see Assessment below).

**What to say:** "You just watched the exact same physical action — one button press — produce
completely different software results depending on whether we handled bounce. That 'clean up a
noisy real-world signal' problem comes back constantly in physical computing — next Class, it's
an ultrasonic sensor instead of a switch."

**Preview next Class:** Class 2 reuses none of today's pins — it's the HC-SR04 ultrasonic
distance sensor and the SG90 servo motor, both wired fresh, while today's circuit stays untouched
on the breadboard. Point students to the Class 2 references in the syllabus if they want to read
ahead.

## 6. Troubleshooting Guide

| Problem | Likely Cause | Fix |
| :-------- | :------------- | :---- |
| `press_count` doesn't change at all | Button wired to wrong pin, or `GND` leg not connected | Verify both button legs — one to `GP2`, the other to `GND` |
| `press_count` jumps by more than 1 even with `class-1-code-2.py` | `button.update()` not called every loop, or called inside an `if` block | `update()` must run unconditionally, once per loop iteration |
| Encoder LED never changes brightness | `encoder_led` on wrong pin, or PWM pin doesn't support PWM output | Confirm `GP14` wiring; try a different PWM-capable GPIO if the pin itself is suspect |
| Encoder counts backward from what's expected | `CLK`/`DT` wires swapped | Swap the two wires, or swap the `+1`/`-1` branches in code |
| Encoder still jittery after debouncing | `MIN_STEP_INTERVAL` too small for this particular encoder | Raise it in small steps (e.g. `0.02` -> `0.03` -> `0.05`) and re-test |
| `ImportError: no module named 'adafruit_debouncer'` | Library not copied to `/lib` on CIRCUITPY drive | Copy the `adafruit_debouncer.mpy` file from the Library Bundle into `/lib` |
| Serial console shows nothing at all | Wrong COM port selected, or board not in a data-capable USB port | Reselect the port in Mu/Thonny; try a different USB cable/port |
| Button LED stays on permanently | Button wired active-high instead of active-low, code assumes active-low | Confirm `pull = digitalio.Pull.UP` and the switch's other leg goes to `GND`, not `3V3` |

## 7. Age Differentiation Notes

**Younger students (12-14) and their parent/guardian:** Provide the pin table above pre-printed
and laminated at the workstation so it's a lookup, not a memorization task. Pair a younger
student's fine-wiring work with the parent/guardian's help holding components steady. Start from
`class-1-code-1.py` already loaded as a starting point rather than typed from scratch, and have
them focus on reading and modifying it (e.g., changing `MIN_STEP_INTERVAL`) rather than writing
it from a blank file.

**Older students (15-18) and adults:** Have them type `class-1-code-1.py` themselves from the
wiring table and a description of the goal, rather than starting from the provided file. Once the
milestone is met, challenge them to add a third state — e.g., print "double press" if two button
presses land within 400ms of each other — as an extension of the debouncing logic they just
learned.

## 8. Assessment

**Milestone Assignment (per syllabus, Phase 1 / Class 1):** Side-by-side terminal output showing
bouncy vs. debounced switch/encoder readings.

**What "complete" looks like:** The student can run `class-1-code-1.py`, show a single button
press or encoder click producing multiple/erratic console lines, then run `class-1-code-2.py` and
show the same physical action producing exactly one clean console line. Both LEDs respond
correctly to their respective input in the debounced version.

**How to give feedback without scoring:** Ask the student to narrate what changed between the two
runs in their own words ("what did debouncing actually do?") rather than checking a box. If a
pair can't get clean output in the time available, that's fine — have them bring a working
version to the start of Class 2 and note it in their build journal.

## 9. Instructor Tips

* Run both code versions yourself, live, on the projector *before* students touch their own
  boards — seeing the instructor's console jump around builds anticipation better than
  describing it.
* Cheap KY-040 modules vary quality-wise more than the pushbuttons do; if one pair's encoder is
  still jittery well above a `MIN_STEP_INTERVAL` of 0.05s, swap the module rather than burning
  class time chasing a bad part.
* The "should we fix this in hardware or software?" discussion (Direct Teaching) tends to run
  long if you let it — cap it at 3-4 student answers and move on; it pays off more once students
  have seen the raw bounce with their own eyes in Guided Practice.
* Keep both code files (`class-1-code-1.py`, `class-1-code-2.py`) on a shared drive/USB stick so
  a student who breaks their working file can recover instantly instead of losing class time.
* If a pair finishes early and both LEDs work, resist the urge to let them start full Chassis Kit
  assembly at their bench mid-Class — it's noisy and distracting for pairs still debugging. Point
  early finishers to the encoder-tuning extension instead, and save Chassis Kit time for the
  Closing segment.

## 10. Resources & References

* [What Is Switch Bounce & How to Implement Debounce][01] — background on the physical cause of
  switch bounce
* [Python Debouncer Library for Buttons and Sensors][02] — `adafruit_debouncer` overview
* [adafruit_debouncer Advanced Debouncing guide][03] — the `Debouncer.update()` / `.rose` /
  `.fell` code pattern used in `class-1-code-2.py`
* [How to Use a Rotary Encoder with the Raspberry Pi (The Pi Hut)][04] — KY-040 wiring and
  quadrature background
* [Hardware Debounced Rotary Encoder (Hackaday.io)][05] — a hardware-side alternative to the
  software debounce used in this Class, useful for the "fix it in hardware or software?"
  discussion
* [MicroPython Rotary Encoder Driver (GitHub)][06] — a MicroPython reference implementation; not
  the CircuitPython API used in this Class's code, but a useful cross-reference for students
  researching independently

---

[01]:https://www.picotech.com/library/articles/blog/what-is-switch-bounce-how-to-implement-debounce
[02]:https://learn.adafruit.com/debouncer-library-python-circuitpython-buttons-sensors/overview
[03]:https://learn.adafruit.com/debouncer-library-python-circuitpython-buttons-sensors/advanced-debouncing
[04]:https://thepihut.com/blogs/raspberry-pi-tutorials/how-to-use-a-rotary-encoder-with-the-raspberry-pi
[05]:https://hackaday.io/project/162207-hardware-debounced-rotary-encoder
[06]:https://github.com/miketeachman/micropython-rotary
