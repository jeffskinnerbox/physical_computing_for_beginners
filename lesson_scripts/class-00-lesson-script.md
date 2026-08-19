# Lesson Script: Pre-Class — Prepare Your Laptop and Pico


* **Class:** Pre-Class (Phase 0 — Setup), before Class 1 of 6
* **Duration:** ~2 hours
* **What You'll Need:** see [Section 2](#2-what-youll-need)
* **Before You Start:** Nothing — this is the very first session. Bring your own Windows 11
    laptop and, if it's already been handed to you, your Raspberry Pi Pico 2 W. No prior
    CircuitPython or electronics experience is assumed.

---


## 1. What This Project Is

Tonight you're not building a circuit — you're proving that your laptop, your editor, and your
board can all talk to each other. By the end, you'll have a tiny Raspberry Pi Pico 2 W blinking
its own onboard LED and printing a running count ("heartbeat") to your laptop's screen, with
nothing else wired up at all.

That sounds small, but it's the foundation every single later class depends on. Right now, your
Pico doesn't even know how to run Python — it has no operating system on it at all. Tonight fixes
that: you'll install your code editor, flash **CircuitPython** (the software that turns the raw
chip into something you can program) onto the board, download the library of pre-written code
you'll draw from all course long, and write, save, and run your first real program.

This is also where you learn a habit you'll use for the rest of the course, and probably the rest
of your maker life: this entire project — the one you're building over the next six classes — was
put together the same way real makers build things, by reading documentation and adapting
examples from sites like Adafruit, GitHub, Instructables, and SparkFun. Whenever you get stuck
later, those same sites are where you go, not just where the instructor goes.

## 2. What You'll Need

| Component | Quantity | Purpose This Project |
| :---------- | :--------: | :---------------------- |
| Raspberry Pi Pico 2 W (with header) | 1 | The board you're setting up — no other hardware is wired tonight |
| USB cable (data cable, not charge-only) | 1 | Powers the Pico, flashes firmware, and carries the serial console |
| Windows 11 laptop (standard, non-admin account is fine) | 1 | Runs your editor and holds your toolchain for the whole course |

**Software you'll install tonight** (all free): the [Mu Editor][01] and [Thonny][02] (two code
editors — you'll pick a favorite, but it's good to have both), the [CircuitPython firmware][03]
for the Pico 2 W, and the [Adafruit CircuitPython Library Bundle][05] (a giant folder of
pre-written code for sensors and motors you'll use starting in Class 1). Section 4 below walks
through every install step in order — you don't need to go anywhere else tonight.

## 3. Meet the Hardware

**Raspberry Pi Pico 2 W.** This is a full microcontroller — a tiny, self-contained computer —
small enough to sit on a breadboard. Out of the box, though, it's blank: no operating system, no
Python interpreter, nothing that understands a `.py` file. That's exactly like a laptop with no OS
installed; it can't run a Word document either. **Firmware** is the low-level software that fixes
this — flashing CircuitPython firmware onto the Pico is what turns "a raw chip" into "a computer
that understands CircuitPython." You only have to do this once (or occasionally, to update it).

**The `CIRCUITPY` drive.** Once CircuitPython is running on the board, it shows up on your laptop
as an ordinary-looking USB drive named `CIRCUITPY`. Saving a `.py` file onto it is literally just a
file copy — there's no special upload tool. CircuitPython watches for changes and automatically
re-runs whatever is saved as `code.py` (or `main.py`) the instant you finish saving. That means the
moment you hit "save" in your editor, your program restarts on the board — no separate "upload" or
"run" button to press.

**Key CircuitPython modules you'll use tonight:**

* `board` — gives you names for the Pico's physical pins and built-in parts (like `board.LED` for
    the onboard LED), so your code doesn't need to know raw pin numbers.
* `digitalio` — lets you treat a pin as a simple digital input or output. Tonight you'll use it in
    `OUTPUT` mode to turn the onboard LED on and off. You'll use this same module for a pushbutton
    switch (as an `INPUT`) in Class 1.
* `time` — gives you `time.sleep()` to pause your program for a set number of seconds, which is
    how you control how fast the LED blinks.

You won't wire anything to external pins tonight — everything you need (the LED, the USB
connection, the `CIRCUITPY` drive) is already built into the board.

## 4. Build It: Write, Save, and Run Your First Program

### Wiring for this phase

None — nothing external is wired tonight. The only hardware is the Pico itself, plugged into your
laptop by USB.

### Install your software

Do these four steps in order. Each one has its own quick test so you know it worked before moving
to the next.

#### Step 1 — Flash CircuitPython onto the Pico 2 W

Your Pico 2 W ships with no firmware, or with factory-test firmware — either way, it doesn't
understand Python yet. This step replaces that with CircuitPython. It all happens through File
Explorer, no command line needed.

1. Open a browser and go to the [CircuitPython firmware page for the Pico 2 W][03]. Double-check
    you're on the **Pico 2 W** page, not "Pico W" or "Pico 2" (no W) — the Pico 2 W has WiFi *and*
    the newer RP2350 chip, so firmware for the other boards won't work on it.
1. Click **Download .uf2 Now**. This saves a file like
    `adafruit-circuitpython-raspberry_pi_pico2_w-en_US-10.2.1.uf2` to your `Downloads` folder.
    Write down the **major version number** (the `10` in `10.2.1`) — you'll need it in Step 4.
1. Unplug the Pico 2 W if it's connected. Find the small white **BOOTSEL** button on top of the
    board.
1. Press and **hold** BOOTSEL, and — while still holding it — plug the USB cable into your
    laptop. Keep holding for about 2 seconds after plugging in, then release.
1. Open File Explorer. A removable drive named **RPI-RP2** should appear.
1. Drag the `.uf2` file onto the **RPI-RP2** drive. The drive disappears on its own within a few
    seconds — that's normal, it means the board is rebooting into CircuitPython. If it doesn't
    disappear, unplug the USB, wait two seconds, and plug it back in without holding BOOTSEL this
    time.

**Test it:** Wait 5-10 seconds, then check File Explorer again — a drive named **CIRCUITPY**
should now appear. Open `boot_out.txt` inside it in Notepad; its first line should say something
like `Adafruit CircuitPython 10.2.1 on ...`, confirming the version now running on the board. If
CIRCUITPY never appears, repeat the BOOTSEL steps — it's almost always a timing issue (BOOTSEL
released too early) or a charge-only cable that can't carry data.

>**NOTE:** **BOOTSEL** (short for boot selection)
>is a hardware mechanism, usually a physical button or pin connection,
>used on microcontrollers to force the chip into a special programming mode at startup.
>When activated, it lets you load new firmware via USB without needing an external programmer.

#### Step 2 — Install the Mu Editor

Mu is built specifically for CircuitPython beginners — it auto-detects your board and includes a
one-click serial console.

1. Go to [codewith.mu][08] and click **Download**, then the **Windows** installer link. This saves
    a file like `MuEditor-win64-1.2.0.msi`.
1. Double-click the `.msi` to launch it.

    > If you don't have an administrator password and Windows shows a User Account Control (UAC)
    > prompt, click **No**/**Cancel** instead of typing anything. Open a regular (non-admin)
    > Windows Terminal and run `winget install --scope user -e --id Mu.Mu` — the `--scope user`
    > flag installs Mu just for your account and often skips the UAC prompt. If it still asks for
    > admin approval, a parent, teacher, or IT admin can type their password into the UAC prompt
    > once — after that Mu runs normally under your own account.

1. Accept the license agreement and click **Install**, then **Finish** once it completes.

> The Mu project is **archived** (no longer actively maintained), but its last release still
> installs and runs fine, and a lot of CircuitPython tutorials still assume it. That's exactly why
> Step 3 installs Thonny too — a second, actively-maintained editor so you're never stuck if Mu
> stops working someday.

**Test it:** Click **Start**, type `Mu`, and launch it (first launch can take a moment — be
patient). A dialog asks you to pick a mode — choose **CircuitPython**. Once the main window opens,
Mu is ready to talk to a board.

#### Step 3 — Install Thonny and connect it to the Pico 2 W

Thonny isn't a replacement for Mu — it's your backup, with a built-in file browser for the
`CIRCUITPY` drive and a step-through debugger.

1. Go to [thonny.org][16] and click the Windows installer link (as of this writing, labeled for
    "Intel or AMD computers"). This saves a file like `thonny-5.0.0-x64.exe`. If your laptop uses
    an ARM chip, use the ARM64 installer link next to it instead — check **Settings → System →
    About → System type** if you're unsure.
1. Double-click the `.exe` to launch the installer.

    > Same UAC situation as Mu: if you're on a standard account without an admin password, look
    > for a **"For me only"** vs **"All users"** choice and pick **For me only** — it avoids the
    > UAC prompt entirely. Otherwise, follow the same admin-approval fallback as the Mu note above.

1. Accept the defaults and click **Finish**.

**Test it:** Click **Start**, type `Thonny`, and launch it. You should see a code-editing pane on
top and a **Shell** pane at the bottom.

Now point Thonny at your board:

1. With the Pico 2 W plugged in (normal mode — no BOOTSEL needed, it's already running
    CircuitPython from Step 1), go to **Tools → Options... → Interpreter** in Thonny (or click the
    interpreter name in the bottom-right corner and choose **Configure interpreter...**).
1. In the top dropdown, pick **CircuitPython (generic)**. If that's not listed, **MicroPython
    (Raspberry Pi Pico)** also works for file access and the console.
1. In the port dropdown, pick the entry mentioning a COM port (e.g. `Board CDC (COM5)`). If
    nothing shows up, unplug and replug the USB cable and reopen the dropdown.
1. Click **OK**.

**Test it:** The Shell pane should now show a CircuitPython `>>>` prompt (press **Ctrl+C** first
if it looks stuck). Click into the Shell and type `print("hello from Thonny")`, press Enter, and
confirm the text echoes back. In Thonny's **Files** panel (**View → Files** if hidden), you should
see a separate **Raspberry Pi Pico**/**CircuitPython** section listing `boot_out.txt` — that's the
`CIRCUITPY` drive, browsable without File Explorer.

#### Step 4 — Install the Adafruit CircuitPython Library Bundle

CircuitPython only ships with a small set of built-in modules. The moment a tutorial has you
`import neopixel` or talk to a sensor over I2C, you'll hit an error like:

```text
Traceback (most recent call last):
  File "code.py", line 2, in <module>
ImportError: no module named 'neopixel'
```

That's not a mistake — it means the library exists, you just haven't copied it onto the board yet.

1. Go to [circuitpython.org/libraries][17]. Find the **major version number** you wrote down in
    Step 1 (e.g. `10`), and download the bundle matching it — mismatched major versions fail to
    import with a confusing error, since compiled `.mpy` files are version-specific.
1. This saves a `.zip` like `adafruit-circuitpython-bundle-10.x-mpy-20260115.zip`. Right-click it,
    choose **Extract All... → Extract**, to unzip it.
1. Open the extracted folder's **`lib`** subfolder — this lists every available library. Files
    ending `.mpy` are single-file libraries; folders (like `adafruit_display_text`) are
    multi-file libraries. You only ever copy the specific libraries a project needs, never the
    whole bundle — `CIRCUITPY` only has a few MB of space.
1. Open a second File Explorer window to your `CIRCUITPY` drive's own `lib` folder, and drag over
    what you need. For tonight's test, drag `neopixel.mpy` onto CIRCUITPY's `lib` folder — even
    without a NeoPixel strip yet, this proves the copy mechanism works.

    > **How do you know which library name to use?** The tutorial you're following will say —
    > check its "Wiring and CircuitPython" section for an `import` line near the top (e.g.
    > `import adafruit_ahtx0`). That module name is the file/folder to drag over. Some libraries
    > need a shared helper too, e.g. an AHT20 temperature sensor needs both `adafruit_ahtx0.mpy`
    > and the `adafruit_bus_device` folder.

1. If Windows asks to merge/replace when a folder already exists on CIRCUITPY, choose **Replace**
    or **Merge** — normal the first time you copy a multi-file library.

**Test it:** In Mu or Thonny, open `code.py` from CIRCUITPY and add:

```python
import neopixel  # if this line errors, the library didn't copy correctly
print("neopixel library imported OK")
```

Save, then open the Serial console (Mu) or Shell pane (Thonny), click inside it, and press
**Ctrl+D** to soft-reset the board and rerun `code.py`. You should see
`neopixel library imported OK` with no traceback. Then delete those two lines and save again —
this was just a test, and the next section will replace `code.py` with the real program for
tonight.

### What this code does

This program does two things in an endless loop: it flips the onboard LED between on and off, and
it prints a growing "heartbeat" count to the serial console every time it does. Watching both the
physical LED and the on-screen count change together is how you'll confirm the whole chain —
laptop, editor, USB, firmware, board — is actually working end to end.

### The code

Once `CIRCUITPY` is visible, save this file as exactly `code.py` on that drive's root — not
`class-0-code.py`, not `code.txt`. CircuitPython only automatically runs a file named `code.py`
(or `main.py`); anything else just sits there unused.

```python
# class-0-code.py
# Save as code.py on the CIRCUITPY drive. No external parts required.

import time
import board
import digitalio

# board.LED refers to the Pico's built-in LED -- no wiring needed.
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# We'll increase this by 1 every time through the loop, so the printed
# count going up is visible proof the program is actually still running.
heartbeat = 0

print("Pre-Class -- CircuitPython heartbeat starting...")

while True:
    # Flip the LED's state: on becomes off, off becomes on.
    led.value = not led.value
    heartbeat += 1
    print("heartbeat:", heartbeat)
    # Pause half a second before the next flip -- this sets the blink rate.
    time.sleep(0.5)
```

### Try it / what you should see

The instant you finish saving, the onboard LED should start blinking roughly twice a second. Open
the serial console in Mu or Thonny (see [Connecting to the Serial Console][09]) and you should see
lines like:

```text
Pre-Class -- CircuitPython heartbeat starting...
heartbeat: 1
heartbeat: 2
heartbeat: 3
```

counting up once per second (twice per blink cycle, since each `time.sleep(0.5)` only covers half
a blink). If you see the LED blinking but nothing in the console, you're looking at the wrong COM
port, or your cable is charge-only (no data lines) — see Troubleshooting below.

### Checkpoint

Point at your own onboard LED blinking, and on the same screen, watch the `heartbeat:` count
climbing in the serial console. If both of those are true at the same time, your whole toolchain —
laptop, editor, USB, firmware, and board — is confirmed working, and you're ready for Class 1.

## 5. Try It Yourself

Once your heartbeat is running, make a few small, deliberate changes and watch what happens each
time — this "change one thing, test it, see the result" habit is the same one you'll use to build
every project for the rest of the course:

* Change `time.sleep(0.5)` to a different number (try `0.1`, then `2`) and watch the blink rate
    change.
* Change the text inside `print("Pre-Class -- ...")` and confirm the new text shows up after you
    save.
* On purpose, delete the colon at the end of the `while True:` line, save, and read the error
    message (called a **traceback**) that shows up in the serial console. This is CircuitPython
    telling you exactly what's wrong and on which line — a skill you'll rely on constantly.
    Afterward, put the colon back and confirm the heartbeat resumes.
* Browse the course GitHub repository and [Adafruit Learn][13] to get comfortable finding your way
    around both — you'll need them for real troubleshooting starting in Class 1.

## 6. Troubleshooting Guide

| Problem | Likely Cause | Fix |
| :-------- | :------------- | :---- |
| Pico never shows a mass-storage drive when plugged in while holding `BOOTSEL` | Charge-only USB cable, or `BOOTSEL` wasn't held the whole time | Swap to a known-good data cable; hold `BOOTSEL` continuously through the plug-in |
| `CIRCUITPY` drive never appears after flashing | Firmware file didn't fully copy before being ejected, or the wrong `.uf2` for this board | Re-flash from the start; confirm the firmware is specifically for "Raspberry Pi Pico 2 W" |
| Mu or Thonny installer asks for an admin password you don't have | Standard (non-admin) Windows account | For Mu, try `winget install --scope user -e --id Mu.Mu`; for Thonny, pick the **"For me only"** install option; otherwise ask a parent/teacher/IT admin to approve the UAC prompt once |
| Thonny's Shell pane won't show a `>>>` prompt | Wrong interpreter/port selected in **Tools → Options → Interpreter** | Re-select **CircuitPython (generic)** (or **MicroPython (Raspberry Pi Pico)**) and the COM port that appears when the Pico is plugged in |
| `ImportError: no module named '...'` | The library was never copied into CIRCUITPY's `lib` folder | Find the matching file/folder in the extracted Library Bundle and drag it into CIRCUITPY's `lib` folder |
| LED never blinks after saving | File saved as `class-0-code.py` instead of renamed to `code.py` | Rename it to exactly `code.py`, sitting directly on the `CIRCUITPY` drive root |
| Serial console shows nothing at all | Wrong COM port selected, or the cable/port is charge-only | Reselect the correct port in Mu/Thonny; try a different cable or USB port |
| Editor won't install | Laptop is locked down by school/parental controls | Try a portable/no-install version if available, or ask your instructor about IT support |
| Edits to `code.py` don't seem to take effect | Editor hadn't finished writing before the drive was ejected, or you edited a copy somewhere else | Close and reopen the file directly from the `CIRCUITPY` drive to confirm what's actually saved |
| A traceback appears after an edit | Likely a real syntax error you introduced (e.g. the missing-colon exercise above) | Read the traceback's line number and message — this is expected, not a failure; fix the line and save again |

## 7. Put It All Together

There's no separate "combined" build for the Pre-Class — the single program below already is the
complete project. It's repeated here so you have everything in one place if you're building from
scratch.

### Complete wiring

None. Only the Pico 2 W and a USB cable to your laptop — no breadboard, no external components.

### Complete code

Save as `code.py` on the `CIRCUITPY` drive root.

```python
# class-0-code.py -- CircuitPython heartbeat: blink the onboard LED and
# print a running count to the serial console. No external parts required.
import time
import board
import digitalio

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

heartbeat = 0

print("Pre-Class -- CircuitPython heartbeat starting...")

while True:
    led.value = not led.value
    heartbeat += 1
    print("heartbeat:", heartbeat)
    time.sleep(0.5)
```

## 8. What You Learned

You didn't wire a single external component tonight, but you proved the entire foundation the
rest of the course stands on. Specifically, you now know:

* What firmware is, and why a microcontroller can't run any of your code until it's flashed
* How to flash CircuitPython onto a Raspberry Pi Pico 2 W and find the resulting `CIRCUITPY` drive
* How to install and connect two different CircuitPython editors (Mu and Thonny), and why having a
    backup editor matters
* How to pull the specific libraries a project needs out of the Adafruit CircuitPython Library
    Bundle, instead of copying the whole thing
* That saving a `.py` file to `CIRCUITPY` is just a file copy — CircuitPython auto-runs whatever is
    saved as `code.py`, restarting it the instant you save
* How to use `board`, `digitalio`, and `time` together to control an output (the onboard LED) and
    pace a loop
* How to open the serial console and read printed output — and read a traceback without panicking
    when something's wrong
* Where working makers actually find and adapt code: Instructables, GitHub, Adafruit Learn, and
    SparkFun — sites you'll lean on for the rest of this course and beyond

Next class, this same chain gets its first real test with actual hardware: a pushbutton switch and
a rotary encoder, wired to real GPIO pins for the first time. Nothing from tonight needs to be
undone — tonight's `code.py` simply gets replaced by Class 1's.
<br>
## 9. Homework Assignment

Everything above got your dev environment running and proved the chain works with a one-line
blink. The exercises below are **homework, not required class content** — optional problems that
push you past "blink an LED" into territory that starts to look like real projects: web servers,
wireless networking, and introspecting the hardware itself. Each one builds directly on the Pico
2 W setup you already have; the only new hardware required is the [TFT display][19].

Do them in any order. For each one you'll find: what the code does and why it's useful, the full
commented code to save as `code.py` on your CIRCUITPY drive, and a couple of real-world examples
of where this exact technique shows up outside of a classroom.

### Homework 1 — Log the Pico 2W's Own Internal Temperature

**What this teaches:** The RP2350 chip inside your Pico 2W has a built-in temperature sensor —
not for measuring the room, but for measuring itself. Reading it introduces the **ADC**
(analog-to-digital converter), the piece of hardware every sensor in this course from here on
(ultrasonic distance, IMU) ultimately relies on to turn a real-world analog voltage into a number
Python can use. This is the gentlest possible first taste of that idea, since it needs no wiring
at all — the sensor is already inside the chip.

```python
# code.py - logs the Pico 2W's internal chip temperature once per second
import time
import microcontroller   # gives access to chip-level features, including the internal temp sensor

def celsius_to_fahrenheit(c):
    # Simple unit conversion — same formula you'd use for any Celsius reading
    return (c * 9 / 5) + 32

print("Logging Pico 2W internal chip temperature. Press Ctrl+C to stop.")
print("Note: this reads the CHIP's temperature, which runs a few degrees warmer")
print("than the room because of the chip's own power use — that's expected.")

reading_count = 0
while True:
    temp_c = microcontroller.cpu.temperature   # built-in property, no sensor wiring needed
    temp_f = celsius_to_fahrenheit(temp_c)
    reading_count += 1

    print(f"Reading #{reading_count}: {temp_c:.1f} C  /  {temp_f:.1f} F")

    time.sleep(1)  # wait a second between readings so the console stays readable
```

**Test it:** Save as `code.py`, open the Serial console (Mu) or Shell pane (Thonny), and watch
readings print once per second. Try cupping your hand around the board (without touching any
pins) for a minute — the reading should climb slightly, confirming the sensor is live and
responsive, not a fixed/fake number.

**Real-world examples:**

* Laptops, phones, and game consoles all read an internal chip temperature sensor like this one to
    decide when to spin up a fan or throttle performance before overheating causes damage.
* Server rooms and data centers log exactly this kind of self-reported chip temperature across
    thousands of machines to catch a failing cooling system before it causes an outage.

### Homework 2 — Bouncing Shape Animation on the TFT Display

**What this teaches:** *(Requires the [TFT display][19] used later in this course — see the "1.14"
240x135 Color TFT Display" in the course's bill of materials, Class 6's stretch goal.)* This
exercise draws a simple shape on the TFT and makes it bounce off the screen's edges, like the
classic "DVD logo" screensaver. It introduces `displayio` (CircuitPython's graphics framework),
a coordinate system with an X/Y origin, and the core game-physics idea of updating a position by a
velocity every frame and reversing that velocity on collision with a boundary.

This uses the same TFT and the same pins (`GP18`-`GP22`) documented for the Class 6 stretch goal,
so if you've already wired the display for that class, this program will run on it as-is with no
rewiring.

**Wiring — Pico 2W to ST7789 1.14" 240x135 TFT:**

| Pico 2W Pin | TFT Pin | Signal / Function |
| ------------- | --------- | -------------------- |
| `3V3(OUT)` | `VIN` | 3.3V power to the display |
| `GND` | `GND` | Common ground |
| `GP18` | `SCK` | SPI clock |
| `GP19` | `MOSI` | SPI data, Pico → display (there is no MISO line — the display never talks back) |
| `GP20` | `CS` | Chip select (tells the display when the Pico is talking to *it*, not some other SPI device) |
| `GP21` | `DC` | Data/Command select (tells the display whether an incoming byte is a drawing command or pixel data) |
| `GP22` | `RST` | Reset (lets CircuitPython force the display back to a known state on startup) |

> Double-check your specific TFT board's silkscreen labels against this table — some boards
> label the reset pin `RESET` or `RST`, and the data/command pin `DC` or `A0`, but they're the
> same signal either way.

```python
# code.py - bounces a square around the TFT display, DVD-logo style
import time
import board
import busio
import displayio
import fourwire
import vectorio
from adafruit_st7789 import ST7789   # matches the TFT used later in this course (Class 6)

# --- Wire up and initialize the TFT display over SPI ---
# Pin assignments match the wiring table above (and the Class 6 stretch-goal wiring).
displayio.release_displays()  # frees up the display in case code.py has run before
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19)
display_bus = fourwire.FourWire(spi, chip_select=board.GP20, command=board.GP21, reset=board.GP22)
display = ST7789(display_bus, width=240, height=135, rotation=270)

# --- Build the shape we'll bounce: a small filled square ---
main_group = displayio.Group()
display.root_group = main_group

palette = displayio.Palette(1)
palette[0] = 0x00AAFF  # a bright cyan-blue square

square_size = 20
square = vectorio.Rectangle(
    pixel_shader=palette,
    width=square_size,
    height=square_size,
    x=0,
    y=0,
)
main_group.append(square)

# --- Position and velocity, in pixels and pixels-per-frame ---
x, y = 10, 10
dx, dy = 2, 2  # positive = moving right/down; flips sign on each bounce

while True:
    x += dx
    y += dy

    # Bounce off the left/right edges
    if x <= 0 or x + square_size >= display.width:
        dx = -dx
        x = max(0, min(x, display.width - square_size))  # clamp so it can't slide off-screen

    # Bounce off the top/bottom edges
    if y <= 0 or y + square_size >= display.height:
        dy = -dy
        y = max(0, min(y, display.height - square_size))

    square.x = x
    square.y = y

    time.sleep(0.02)  # ~50 frames per second — fast enough to look smooth
```

**Test it:** Save as `code.py` with the TFT wired per Class 6's wiring notes. The square should
glide around the screen and visibly change direction each time it touches an edge, without ever
disappearing off the side.

**Real-world examples:**

* This exact bounce-and-reverse-velocity pattern is the starting point for real game physics
    engines — Pong, Breakout, and any game with objects that ricochet off walls all extend this same
    idea.
* Digital signage and kiosk displays use idle "screensaver" animations like this one to avoid
    burning a static image into the screen during long periods with no user interaction.

### Homework 3 — Turn the Pico 2W into a WiFi Captive Portal Access Point

**What this teaches:** The Pico 2W has a WiFi radio built in (that's what the "W" means), and
CircuitPython can turn it into its own tiny WiFi network — an **access point** — instead of just
joining someone else's. This exercise builds on the `blink.py`-style program from Section 4:
instead of only blinking the LED, the board also runs a small web server that any phone or laptop
can connect to and see the LED's current on/off status on a webpage, live, with no laptop cable
required.

Before running this, you need to create a **second file** on CIRCUITPY named `env.yaml` — this
keeps your network name and password out of your actual code, which is good practice for any
project you might later share or post online:

```yaml
# env.yaml — save this on CIRCUITPY, next to code.py
# WiFi credentials for the Pico's own access point (not your home WiFi)
ap_ssid: "<your-name>"
ap_password: "blinkblink"   # must be at least 8 characters — WiFi requirement, not a suggestion
```

> `env.yaml` needs the `adafruit_yaml` library copied into CIRCUITPY's `lib` folder the same way
> you copied `neopixel.mpy` in Section 4 — grab it from the same Adafruit CircuitPython Library
> Bundle you already downloaded. This board also needs `adafruit_httpserver` in `lib` for the web
> server piece.

```python
# code.py - WiFi Captive Portal Access Point showing onboard LED status on a webpage
import time
import board
import digitalio
import wifi                      # controls the Pico 2W's WiFi radio directly
import socketpool                # lets CircuitPython open network sockets over that radio
import yaml                      # reads our env.yaml file so credentials aren't hardcoded here
from adafruit_httpserver import Server, Request, Response

# --- Load WiFi credentials from env.yaml instead of hardcoding them in this file ---
with open("/env.yaml", "r") as f:
    creds = yaml.safe_load(f)

# --- Set up the onboard LED, same as blink.py ---
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# --- Turn the Pico's WiFi radio into its OWN network (an access point) ---
# Anyone nearby can now see and join "<your-name>" like any other WiFi network.
wifi.radio.start_ap(ssid=creds["ap_ssid"], password=creds["ap_password"])
print("Access point started. Connect to:", creds["ap_ssid"])
print("Then visit http://" + str(wifi.radio.ipv4_address_ap) + "/ in a browser")

# --- Start a tiny web server on the Pico itself ---
pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)

led_is_on = False  # tracks LED state so the webpage always shows the current truth

@server.route("/")
def base(request: Request):
    # Every time someone loads the page, build fresh HTML showing the LED's real status.
    status_word = "ON" if led_is_on else "OFF"
    status_color = "limegreen" if led_is_on else "crimson"
    html = f"""
    <html>
      <head>
        <title>Pico 2W LED Status</title>
        <meta http-equiv="refresh" content="1">
      </head>
      <body style="font-family: sans-serif; text-align: center; margin-top: 3em;">
        <h1>Onboard LED is currently:</h1>
        <h1 style="color: {status_color};">{status_word}</h1>
        <p>This page auto-refreshes once a second.</p>
      </body>
    </html>
    """
    return Response(request, html, content_type="text/html")

server.start(str(wifi.radio.ipv4_address_ap))

# --- Main loop: blink the LED AND keep answering webpage requests ---
last_blink = time.monotonic()
while True:
    server.poll()  # check if a browser is asking for the page; answer if so

    # Blink once per second, without using time.sleep() (which would freeze the web server)
    if time.monotonic() - last_blink >= 0.5:
        led_is_on = not led_is_on
        led.value = led_is_on
        last_blink = time.monotonic()
```

**Test it:** Save this as `code.py` on CIRCUITPY, wait for it to reboot, then on your phone or
laptop open WiFi settings and connect to the `<your-name>` network using the password from
`env.yaml`. Open a browser and go to the address printed in the serial console (something like
`http://192.168.4.1/`) — the page should show ON/OFF and flip once a second, matching the physical
LED on the board.

**Real-world examples:**

* This is exactly how a smart plug, WiFi light bulb, or new WiFi router gets set up for the first
    time — you connect to a small network the device broadcasts, then configure it from a webpage,
    before it ever joins your real home network.
* Field sensors deployed somewhere without existing WiFi (a garden, a remote enclosure) use this
    same pattern to let a technician walk up, connect directly, and check status without carrying a
    laptop cable or router.

### Homework 4 — Print the Pico 2W's Pin Map to the Console

**What this teaches:** Every pin you can wire something to has *four different names* depending on
what you're looking at: the physical position on the board (silkscreen label), the RP2350 chip's
internal GPIO number, the CircuitPython `board.` name your Python code actually imports, and the
special function(s) that pin supports (I2C, SPI, PWM, ADC, etc.). Mixing these up is one of the
most common beginner wiring mistakes. This program has the board introspect itself and print out
its own pin map, so instead of memorizing it, you can always ask the board directly.

```python
# code.py - prints the Pico 2W's pin mapping to the serial console
import board
import microcontroller

# Official pinout references for the Raspberry Pi Pico 2 W:
# https://datasheets.raspberrypi.com/pico2/pico-2-w-pinout.pdf
# https://circuitpython.org/board/raspberry_pi_pico2_w/
print("=" * 60)
print("Raspberry Pi Pico 2 W — Pin Map")
print("See official pinout diagram: https://datasheets.raspberrypi.com/pico2/pico-2-w-pinout.pdf")
print("=" * 60)

# `dir(board)` lists every name CircuitPython's `board` module knows about —
# this is the same module you `import board` and then write `board.LED`, `board.GP0`, etc.
board_pins = [name for name in dir(board) if not name.startswith("_")]

for name in sorted(board_pins):
    pin_obj = getattr(board, name)

    # Not every name in `board` is an actual physical pin (some are bus objects like I2C/SPI
    # helpers) — skip anything that isn't a real microcontroller.Pin.
    if not isinstance(pin_obj, microcontroller.Pin):
        continue

    # CircuitPython pin objects don't carry a human-readable "function" label on their own,
    # so we build one from what we know: the GP number tells us which physical/chip pin this
    # is, and a short lookup table below fills in the special functions for pins that have them.
    print(f"board.{name:10s} -> {pin_obj}")

print("=" * 60)
print("Pins with special hardware functions on the Pico 2 W:")
print("=" * 60)

# A short reference table of notable special-function pins — cross-check the full picture
# against the official pinout PDF linked above, which also shows physical pin *numbers*
# (1-40) printed on the board's silkscreen, not just GP names.
special_functions = {
    "GP0":  "I2C0 SDA / UART0 TX",
    "GP1":  "I2C0 SCL / UART0 RX",
    "GP2":  "SPI0 SCK",
    "GP3":  "SPI0 TX (MOSI)",
    "GP4":  "SPI0 RX (MISO)",
    "GP5":  "SPI0 CSn",
    "GP26": "ADC0 (analog input)",
    "GP27": "ADC1 (analog input)",
    "GP28": "ADC2 (analog input)",
    "LED":  "Onboard LED (routed through the wireless chip on Pico W boards, not a plain GPIO)",
}

for pin_name, function in special_functions.items():
    print(f"{pin_name:6s} : {function}")

print("Done. For the full official mapping (including physical pin numbers), see:")
print("https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html")
print("https://pip-assets.raspberrypi.com/categories/1088-raspberry-pi-pico-2-w/documents/RP-008305-DS-1-pico-2-w-pinout.pdf")
```

**Test it:** Save as `code.py`, then open the Serial console (Mu) or Shell pane (Thonny) and press
`Ctrl+D` to soft-reboot and rerun it. You should see every `board.GP*` name printed along with its
underlying pin, followed by the special-function table.

**Real-world examples:**

* Any time you pick up someone else's project code and it says `import board` then
    `board.GP1` — this script is how you'd confirm, on your *own* board, whether `GP1` is
    actually the I2C clock line before you go wire a sensor to it.
* Professional embedded engineers do this same kind of self-check ("pin introspection") when
    debugging a new board revision, to catch cases where a pin's silkscreen label, chip datasheet
    name, and framework name have drifted out of sync — exactly the confusion this exercise
    prevents.

## References

* Raspberry Pi Pico 2W Microcontroller
  * [GPIO pinout and pin function guide for the Raspberry Pi Pico 2 W][20]
  * [Raspberry Pi Pico 2W Datasheet][21]
  * [Raspberry Pi Pico 2 W with Header — Product Page][14] — the board used throughout the course
* CircuitPython
  * [What is CircuitPython?][15] — background on CircuitPython vs. MicroPython vs. Arduino C++
  * [CircuitPython Firmware for the Raspberry Pi Pico 2 W][03] — the firmware flashed onto the board tonight
  * [CircuitPython.org — Libraries download][17] — where to get the version-matched Library Bundle
  * [CircuitPython Libraries][06] — what the Library Bundle is and how `/lib` gets used starting Class 1
  * [The CIRCUITPY Drive][04] — what the `CIRCUITPY` drive is and how it behaves
  * [The REPL][11] — using the interactive REPL prompt
* Mu / Thonny Editors
  * [codewith.mu — Mu Editor download][08] — where the Mu installer comes from
  * [Installing the Mu Editor][01] — step-by-step Mu install guide
  * [Creating and Editing Code][07] — saving and editing `code.py`
  * [Connecting to the Serial Console][09] — how to open the serial console in Mu/Thonny
  * [Thonny — official site and download][16] — where the Thonny installer comes from
  * [Thonny setup for CircuitPython][02] — step-by-step Thonny install guide
* Sources Components & Projects
  * [Instructables][12] — maker-community tutorials referenced throughout the course
  * [Adafruit Learn][13] — primary source for CircuitPython guides used across the course
  * [SparkFun Tutorials][22] — step-by-step guide on how to build with SparkFun products

---



[01]:https://learn.adafruit.com/welcome-to-circuitpython/installing-mu-editor
[02]:https://learn.adafruit.com/circuitpython-libraries-on-micropython-using-the-raspberry-pi-pico/thonny-setup
[03]:https://circuitpython.org/board/raspberry_pi_pico2_w/
[04]:https://learn.adafruit.com/welcome-to-circuitpython/the-circuitpy-drive
[05]:https://circuitpython.org/downloads
[06]:https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-libraries
[07]:https://learn.adafruit.com/welcome-to-circuitpython/creating-and-editing-code
[08]:https://codewith.mu
[09]:https://learn.adafruit.com/welcome-to-circuitpython/kattni-connecting-to-the-serial-console
[11]:https://learn.adafruit.com/welcome-to-circuitpython/the-repl
[12]:https://www.instructables.com/
[13]:https://learn.adafruit.com/
[14]:https://www.adafruit.com/product/6315
[15]:https://learn.adafruit.com/welcome-to-circuitpython/what-is-circuitpython
[16]:https://thonny.org
[17]:https://circuitpython.org/libraries
[19]:https://www.proculustech.com/tft-vs-lcd
[20]:https://pico2w.pinout.xyz/
[21]:https://pip-assets.raspberrypi.com/categories/1088-raspberry-pi-pico-2-w/documents/RP-008304-DS-3-pico-2-w-datasheet.pdf
[22]:https://learn.sparkfun.com/tutorials

