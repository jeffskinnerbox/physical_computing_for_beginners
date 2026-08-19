---
File Location: /home/jeff/src/projects/makersmiths/classes/physical_computing_for_beginners/tech_setup_check/install-circuitpython-dev-env-on-windows-11.md
---
# Windows 11 Development Environment for CircuitPython on Raspberry Pi Pico 2W Microcontroller

## Purpose
By the end of this guide, you'll have everything set up on your Windows 11 laptop to write
Python code (specifically CircuitPython code)
that runs directly on a microcontroller, in our case the Raspberry Pi Pico 2W.
With CircuitPython, there is no compiling, no complicated build tools.

What we will do:
1. You'll flash a special firmware onto the board so it understands CircuitPython,
1. install **two** different beginner-friendly editors (so you can see which one you like better),
1. pull in the extra code libraries that most real projects need but CircuitPython doesn't ship with,
1. and prove the whole chain works by making the board's onboard LED blink from code you write yourself.

## What gets installed

| Component | What it does | Why you need it | Instructions source | Official docs |
| ----------- | --------------- | ------------------ | ---------------------- | ---------------- |
| CircuitPython firmware (UF2) | Replaces the Pico 2W's stock firmware with a Python interpreter that runs directly on the board | Without it, the Pico only understands raw machine code — CircuitPython lets you talk to it in Python | [circuitpython.org Pico 2 W page](https://circuitpython.org/board/raspberry_pi_pico2_w/) | [Adafruit: Getting Started with Raspberry Pi Pico and CircuitPython](https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython) |
| Mu Editor | A beginner-focused code editor with a built-in "Serial" console for talking to CircuitPython boards | Lets you write and save code straight to the board, and watch its output live, without wrestling a general-purpose IDE. The Mu project is already archived/unmaintained (no more updates), but the last release still installs and runs fine for this workflow. | [Adafruit: Installing the Mu Editor](https://learn.adafruit.com/welcome-to-circuitpython/installing-mu-editor) | [codewith.mu](https://codewith.mu) |
| Thonny | A second beginner IDE with a built-in CircuitPython/MicroPython file browser, variable inspector, and step-through debugger | Gives you a backup editor if Mu is ever unavailable (it's the actively-maintained alternative), and its file browser makes managing files on CIRCUITPY easier than drag-and-drop alone | [Thonny official site](https://thonny.org) | [thonny.org](https://thonny.org) |
| Adafruit CircuitPython Library Bundle | A collection of ready-made CircuitPython libraries (NeoPixel, sensors, displays, etc.) that aren't built into the firmware | Almost every real tutorial beyond "blink an LED" needs at least one of these — without it you'll hit `ImportError: no module named '...'` the moment you `import neopixel` or similar | [circuitpython.org/libraries](https://circuitpython.org/libraries) | [Adafruit CircuitPython Bundle docs](https://docs.circuitpython.org/projects/bundle/en/latest/) |
| Windows Terminal / File Explorer (built in) | Used to confirm the board shows up as a drive and to inspect files on it | You'll use these throughout to check your work — no separate install needed on Windows 11 | — | [Microsoft Support: Files and storage / File Explorer help](https://support.microsoft.com/en-us/windows/help-in-file-explorer-a2d33543-5242-788d-8994-b0be10ae5bca) |

## Target environment

- **Machine:** Windows 11 laptop (native Windows — not WSL, not a VM)
- **Minimum hardware:** A free USB-A or USB-C port, a **USB data cable** (many cables that came
  with phone chargers are *charge-only* and won't work — check the box or try a known-good cable),
  and a Raspberry Pi Pico 2W board
- **Accounts / access needed:** A **standard (non-admin) Windows user account is fine** for
  everything in this guide. Installing Mu or Thonny may briefly ask for administrator approval —
  see the notes in those sections for what to do if you don't have an admin password handy.
- **Network:** Normal internet access to download four things: the CircuitPython firmware, the
  Mu installer, the Thonny installer, and the CircuitPython Library Bundle zip
- **Before you start, you should already have:** Basic comfort clicking through File Explorer,
  running a downloaded installer, and unzipping a `.zip` file

## Installation

### Part 1 — Flash CircuitPython onto the Pico 2W

Your Pico 2W ships with either no firmware or MicroPython/factory firmware on it. This part
replaces that with CircuitPython, so the board can run the Python files you'll write later. This
whole part happens through File Explorer — no command line needed.

#### Download the CircuitPython firmware

1. Open a browser and go to the official download page for your exact board:
   **<https://circuitpython.org/board/raspberry_pi_pico2_w/>**

   > Double-check you're on the **Pico 2 W** page, not "Pico W" or "Pico 2" (no W). The Pico 2W
   > has Wi-Fi *and* the newer RP2350 chip — the firmware for the other boards won't work on it.

2. Click the big **Download .uf2 Now** button (or similar). This downloads a file named
   something like `adafruit-circuitpython-raspberry_pi_pico2_w-en_US-10.2.1.uf2` into your
   `Downloads` folder. The version number (`10.2.1` here) will likely be higher by the time you
   read this — that's expected, always take the latest stable one offered on the page.

   > Write down the **major version number** (the first number, e.g. `10`) — you'll need it in
   > Part 4 to pick a matching library bundle.

#### Put the Pico 2W into "bootloader" mode and copy the firmware

A `.uf2` file is a special firmware image — you install it by literally dragging it onto the
board like it's a USB flash drive. To make that drive appear, the board has to be started in a
special mode called BOOTSEL.

1. Unplug the Pico 2W from USB if it's currently connected.
2. Find the small white **BOOTSEL** button on top of the Pico 2W.
3. Press and **hold** BOOTSEL, and — while still holding it — plug the USB cable into your
   laptop.
4. Keep holding BOOTSEL for about 2 seconds after plugging in, then release it.
5. Open **File Explorer**. A new removable drive named **RPI-RP2** should appear (usually as
   drive `D:` or `E:`).
6. Drag the `.uf2` file you downloaded onto the **RPI-RP2** drive (or copy-paste it in).
7. The RPI-RP2 drive will disappear on its own within a few seconds — this is normal, it means
   the board is rebooting into CircuitPython.
   If it doesn't disappear, unplug the USB, wait two seconds, and plug it back in **BUT** don't press and hold BOOTSEL.

**Test it**

1. Wait about 5-10 seconds after the RPI-RP2 drive vanishes.
2. Open File Explorer again. A new drive named **CIRCUITPY** should now appear.
3. Double-click into it — you should see a , and a `boot_out.txt` file (and maybe `code.py` file, a `lib` folder).
   Open `boot_out.txt` in Notepad; its first line should say something like
   `Adafruit CircuitPython 10.2.1 on ...` confirming the exact version that's now running on the
   board.

If CIRCUITPY never appears, unplug the board, and repeat the BOOTSEL steps above — it's almost
always a timing issue (BOOTSEL released too early, or the cable is charge-only and can't carry
data).

**Clean up**

Nothing to clean up here — the CIRCUITPY drive and its default files are meant to stay; they're
the board's normal operating state, not test artifacts.

### Part 2 — Install the Mu Editor

Now that the board understands Python, you need an editor on your laptop that can write code to
it and show you what it's doing. Mu is built specifically for CircuitPython/MicroPython beginners
— it auto-detects your board and includes a one-click serial console, which general editors
don't.

#### Download and run the installer

1. Go to **<https://codewith.mu>** and click the **Download** link.

   > The Mu project is **archived — no longer actively maintained**. That's expected: the last
   > release still installs and runs fine today, and this guide keeps it because a lot of
   > CircuitPython tutorials still assume it. Since it won't get further fixes, Part 3 below
   > installs Thonny as a second, actively-maintained editor so you're not stuck if Mu ever stops
   > working for you.

2. Choose the **Windows** installer link. This downloads a file named something like
   `MuEditor-win64-1.2.0.msi` (an `.msi` is a standard Windows installer package).
3. Double-click the downloaded `.msi` file to launch it.

   > **If you don't have an administrator password:** Windows may show a User Account Control
   > (UAC) prompt asking to let the installer make changes. On a standard (non-admin) account you
   > can't approve this yourself — click **No** / **Cancel** on that prompt instead of typing
   > anything. Then open a regular (non-admin) **Windows Terminal** window and try
   > `winget install --scope user -e --id Mu.Mu` — the `--scope user` flag asks winget to install
   > Mu just for your account, which sometimes avoids the UAC prompt entirely. If that still asks
   > for admin approval, you'll need a parent, teacher, or IT admin to type their password into
   > the UAC prompt once — after that, Mu is installed and runs normally under your own account
   > with no further admin access needed.

4. Check the box accepting the license agreement, then click **Install**.
5. Wait for the install to finish (this can take a couple of minutes), then click **Finish**.

**Test it**

1. Click the Windows **Start** button and type `Mu`.
2. Launch the **Mu Editor** app. The very first launch can take a little while to open — that's
   normal, be patient.
3. A dialog appears asking you to pick a mode. Choose **CircuitPython**.
4. Once Mu's main window opens, look at the bottom-right status area — this confirms the
   install succeeded and Mu is ready to talk to a board.

**Clean up**

Nothing to remove — Mu itself is the tool you're keeping.

### Part 3 — Install Thonny and connect it to the Pico 2W

Thonny is your second editor. It isn't a replacement for Mu — it's a backup with a couple of
things Mu doesn't have, like a built-in file browser for the CIRCUITPY drive and a step-through
debugger. Adafruit points beginners to it as the actively-maintained alternative to Mu, so it's
worth having installed even if Mu stays your daily driver.

#### Download and run the installer

1. Go to **<https://thonny.org>** and click the Windows installer link — as of this writing it's
   labeled **"Installer ... for Intel or AMD computers, requires Windows 10 or 11"** and downloads
   a file like `thonny-5.0.0-x64.exe`. (If your laptop uses an ARM chip instead of Intel/AMD,
   there's a separate ARM64 installer link right next to it — check **Settings → System → About**
   under "System type" if you're not sure which you have.)
2. Double-click the downloaded `.exe` file to launch the installer.

   > Same UAC situation as Mu: if you're on a standard account and don't have an admin password,
   > look for a **"For me only"** vs **"All users"** choice in the installer and pick
   > **For me only** (Thonny's installer offers this and it avoids the UAC prompt entirely, since
   > it doesn't touch shared system folders). If that option isn't available, follow the same
   > fallback as the Mu note above — ask a parent/teacher/IT admin to approve the UAC prompt once.

3. Follow the installer's prompts, accepting the defaults, until it finishes and click
   **Finish**.

**Test it**

1. Click the Windows **Start** button and type `Thonny`.
2. Launch the **Thonny** app. First launch can take a few seconds while it sets itself up.
3. You should see Thonny's main window: a code-editing pane on top and a **Shell** pane at the
   bottom. This confirms the install succeeded.

#### Point Thonny at the Pico 2W

Thonny needs to be told to talk to your board using the CircuitPython protocol instead of
whatever it defaults to.

1. Make sure the Pico 2W is plugged in via USB (normal mode — it's already running
   CircuitPython from Part 1, no BOOTSEL needed).
2. In Thonny, go to **Tools → Options...**, then click the **Interpreter** tab.

   > Alternatively, click the interpreter name shown in the bottom-right corner of the Thonny
   > window and choose **Configure interpreter...** — it opens the same dialog.

3. In the top dropdown, select **CircuitPython (generic)**. If you don't see that exact entry,
   **MicroPython (Raspberry Pi Pico)** also works for basic file access and the serial console.
4. In the port dropdown below it, pick the entry that mentions a COM port (e.g.
   `Board CDC (COM5)`) — this is the Pico 2W showing up as a serial device. If nothing shows up,
   unplug and replug the USB cable, then reopen this dropdown.
5. Click **OK**.

**Test it**

1. Look at the **Shell** pane at the bottom of Thonny — it should now show a CircuitPython
   `>>>` prompt (press **Ctrl+C** in the Shell pane first if it looks stuck, to interrupt
   whatever's running and get back to the prompt).
2. Click into the Shell pane and type `print("hello from Thonny")`, then press Enter — you
   should see the text echoed back, confirming Thonny has a live connection to the board.
3. In Thonny's **Files** panel (View → Files if it isn't showing), you should see two sections:
   your laptop's files, and a separate **Raspberry Pi Pico** / **CircuitPython** section listing
   `boot_out.txt` (and maybe code.py` & `lib`) — this is the CIRCUITPY drive,
   browsable without opening File Explorer.

**Clean up**

Nothing to remove — Thonny itself is the tool you're keeping, and no test files were created on
the board in this part.

### Part 4 — Install the Adafruit CircuitPython Library Bundle

CircuitPython only ships with a small set of built-in modules. The moment a tutorial asks you to
`import neopixel` or talk to a sensor/display over I2C, you'll hit an error like:

```text
Traceback (most recent call last):
  File "code.py", line 2, in <module>
ImportError: no module named 'neopixel'
```

That's not a mistake in your code — it means the library exists, but you haven't copied it onto
the board yet. This part fixes that by pulling the right libraries out of Adafruit's bundle and
dragging them onto CIRCUITPY.

#### Download the bundle that matches your CircuitPython version

1. Go to **<https://circuitpython.org/libraries>**.
2. Find the **major version number** you wrote down in Part 1 (e.g. `10`), and click the
   download button for the matching bundle — look for text like **"9.x"** or **"10.x"** next to
   the button. This matters because the compiled `.mpy` library files are only compatible with
   their matching CircuitPython major version; a mismatched bundle will fail to import with a
   confusing error.
3. This downloads a `.zip` file named something like
   `adafruit-circuitpython-bundle-10.x-mpy-20260115.zip` into your `Downloads` folder.
4. Right-click the downloaded `.zip` file and choose **Extract All...**, then **Extract** (the
   default location is fine). This creates a folder with the same name containing the unzipped
   bundle.

#### Copy the libraries a project actually needs

You don't copy the whole bundle onto the board — CIRCUITPY only has a few MB of space, and most
projects need just one or two libraries. Copy only what you're using.

1. Open the extracted bundle folder, then open the **`lib`** folder inside it. This is a big list
   of every available library — files ending in `.mpy` are single-file libraries, and folders
   (like `adafruit_display_text`) are multi-file libraries.
2. Open a **second** File Explorer window and navigate to your **CIRCUITPY** drive, then open its
   own **`lib`** folder.
3. For each library your project needs, drag it from the bundle's `lib` folder into CIRCUITPY's
   `lib` folder. For example, for a NeoPixel LED strip project, drag over:
   - `neopixel.mpy`

   For a common temperature/humidity sensor (AHT20) tutorial, you'd instead need **two** items —
   the sensor library plus a shared helper library it depends on:
   - `adafruit_ahtx0.mpy`
   - the `adafruit_bus_device` folder

   > **How do you know which library name to use?** The tutorial or product guide you're
   > following will say — check its "Wiring and CircuitPython" section, it usually lists an
   > `import` line near the top, e.g. `import adafruit_ahtx0`. That module name (minus `import`)
   > is the file/folder name to drag over.

4. If Windows asks whether to merge/replace when a folder already exists on CIRCUITPY, choose
   **Replace the files in the destination** (or **Merge**) — this is normal the first time you
   copy a multi-file library.

For this guide's own test below, actually drag `neopixel.mpy` onto CIRCUITPY's `lib` folder now
— even if you don't have a NeoPixel LED strip yet, this proves the copy mechanism works, and you
can swap in whichever real library your project needs later using the same steps.

**Test it**

1. In Mu or Thonny, open `code.py` from the CIRCUITPY drive.
2. Add a single import line for the `neopixel` library you just copied:

   ```python
   import neopixel  # if this line errors, the library didn't copy correctly
   print("neopixel library imported OK")
   ```

3. Save the file to CIRCUITPY, then open the **Serial** console (Mu) or **Shell** pane (Thonny).
   Click inside the REPL pane and press `Ctrl+D` — this soft-resets the board and reruns `code.py`.
   You should see `neopixel library imported OK` printed with no `ImportError` traceback.

**Clean up**

Remove the test import line so `code.py` doesn't carry libraries your actual project isn't using
yet:

1. Delete the two lines you added in the **Test it** step above.
2. Save `code.py` again.

You can leave the extracted bundle folder in your `Downloads` folder — you'll come back to it any
time a new project needs a different library, no need to re-download unless CircuitPython itself
gets a major version upgrade later.

### Part 5 — Connect an editor to the Pico 2W and run your first program

This is the payoff: writing a couple of lines of Python, saving them straight to the board, and
watching the board's onboard LED blink because of code you wrote. The steps below use Mu; if
you'd rather use Thonny, the file-saving equivalent is **File → Save As...** and pick the
**Raspberry Pi Pico / CircuitPython** location instead of "This computer."

#### Connect the board and confirm Mu sees it

1. Make sure the Pico 2W is still plugged in via USB (normal mode this time — no BOOTSEL needed,
   since it's already running CircuitPython from Part 1).
2. In Mu, click the **Serial** button in the toolbar. A console pane opens at the bottom of the
   window.
3. Press **Ctrl+C** inside that console, then press **Enter**. You should see a CircuitPython
   REPL (Read-Eval-Print Loop) prompt appear, looking like `>>>`. This confirms Mu has a live
   serial connection to the board.
4. Type `print("hello from the Pico 2W")` at the `>>>` prompt and press Enter — you should see
   the text echoed back immediately. That's Python running *on the board*, not your laptop.
5. Press **`Ctrl+D`** to exit the REPL back to normal running mode (this "soft-reboots" the board).

#### Write and save a blink program

1. In Mu, click **New**, then paste in this short program:

 ```python
# blink.py - makes the Pico 2W's onboard LED blink once per second
import board          # gives us names for the board's physical pins
import digitalio      # lets us treat a pin as a simple on/off switch
import time            # gives us sleep(), to pause between blinks

led = digitalio.DigitalInOut(board.LED)   # grab the onboard LED pin
led.direction = digitalio.Direction.OUTPUT  # tell it we want to control it (not read it)

while True:            # loop forever
  led.value = True    # turn the LED on
  time.sleep(0.5)     # wait half a second
  led.value = False   # turn the LED off
  time.sleep(0.5)     # wait half a second
   ```

1. Click **Save**. In the file-save dialog, navigate to the **CIRCUITPY** drive and save the file
   as exactly `code.py` (overwriting the default one that's already there). CircuitPython only
   auto-runs a file named exactly `code.py` — anything else just sits there unused.

**Test it**

1. Watch the Pico 2W itself: within a second or two of saving, the onboard LED should start
   blinking on and off once per second.
2. Back in Mu, click **Serial** again to reopen the console — you should see CircuitPython
   printing a soft-reboot message, confirming it detected the new `code.py` and restarted to run
   it.

If the LED doesn't blink, click **Serial** in Mu (or check the **Shell** pane in Thonny) and read
the output — CircuitPython prints a Python traceback (error message) there if `code.py` has a
mistake, which tells you exactly which line to fix.

**Clean up**

This blink program is just a test — remove it so the board is back to a clean starting point for
your own projects:

1. In Mu, open `code.py` from the CIRCUITPY drive again (if it isn't already open).
2. Select all the text (**Ctrl+A**) and delete it.
3. Click **Save** to write the now-empty `code.py` back to the board. The LED will stop blinking,
   confirming the cleanup took effect.

## Manual verification checklist

This guide covers Windows software and physical hardware, so it was **manually verified** by
careful step-by-step trace-through rather than sandbox-executed (unlike a Linux/server guide,
this content can't run inside an automated test container). If you're the first person running
through this guide on real hardware, it's worth confirming:

- [ ] The Mu `.msi` installs on a standard (non-admin) account, and the `winget install --scope
      user -e --id Mu.Mu` fallback still works if UAC blocks the installer.
- [ ] Thonny's installer still shows a **"For me only"** vs **"All users"** choice (installer UIs
      change between versions).
- [ ] Mu's first-launch dialog still offers **CircuitPython** as a mode option.
- [ ] `Settings → Apps → Installed apps` is still the correct Windows 11 path for uninstalling
      (Microsoft has moved this before across feature updates).
- [ ] Skipping the "hold BOOTSEL for 2 seconds" timing in Part 1 reproduces the documented
      "CIRCUITPY never appears" failure, confirming the troubleshooting note is accurate.
- [ ] Thonny's interpreter dropdown still offers **CircuitPython (generic)**; if not, confirm the
      **MicroPython (Raspberry Pi Pico)** fallback still lets you browse `lib` and use the Shell.
- [ ] The Part 4 `import neopixel` test throws `ImportError` *before* you drag `neopixel.mpy`
      onto CIRCUITPY, and prints `neopixel library imported OK` *after* — confirming the copy
      step is required, not optional.
- [ ] The provided `blink.py`, saved verbatim as `code.py`, actually blinks the onboard LED on a
      real Pico 2W using `board.LED` — the Pico W family routes its onboard LED through the
      wireless chip rather than a plain GPIO pin, so this is the one line most likely to be
      board/firmware-version-sensitive.
- [ ] Ctrl+C / Ctrl+D REPL behavior matches the doc in both Mu's Serial console and Thonny's
      Shell pane (interrupt → `>>>` prompt; Ctrl+D → soft-reboot message).

## Uninstalling everything (optional)

If you ever need to remove this setup entirely:

- **Mu Editor:** Open **Settings → Apps → Installed apps**, find **Mu**, click the **⋯** menu,
  and choose **Uninstall**. This doesn't need admin rights if Mu was installed per-user; if it was
  installed by an admin for all users, you'll need that same admin to remove it.
- **Thonny:** Open **Settings → Apps → Installed apps**, find **Thonny**, click the **⋯** menu,
  and choose **Uninstall**. Same per-user/admin rule as Mu above.
- **CircuitPython Library Bundle:** Just delete the folders you copied out of `lib` on the
  CIRCUITPY drive, and/or delete the extracted bundle folder from your `Downloads` — there's no
  installer to undo, it's plain files.
- **CircuitPython firmware:** There's no "uninstall" for board firmware — to go back to a blank
  board, put it back into BOOTSEL mode (same steps as Part 1) and drag on a different `.uf2`. To
  install [MicroPython](https://micropython.org/download/RPI_PICO2_W/) instead of CircuitPython,
  grab its `.uf2` from that page. To truly erase the board back to blank/no-firmware, use the
  `nuke.uf2` flash-eraser from the [pico-sdk-prebuilts releases](https://github.com/raspberrypi/pico-sdk/releases)
  (search that page for a `nuke_universal.uf2` or matching RP2350 nuke image), then reflash
  whichever firmware you actually want afterward.
<br>

---

## Homework Assignment

Everything above got your dev environment running and proved the chain works with a one-line
blink. The exercises below are **homework, not required class content** — optional problems that
push you past "blink an LED" into territory that starts to look like real projects: web servers,
wireless networking, and introspecting the hardware itself. Each one builds directly on the Pico
2W setup you already have; only new hardware required is the [TFT display](https://www.proculustech.com/tft-vs-lcd).

Do them in any order. For each one you'll find: what the code does and why it's useful, the full
commented code to save as `code.py` on your CIRCUITPY drive, and a couple of real-world examples
of where this exact technique shows up outside of a classroom.

### Homework 1 — Turn the Pico 2W into a WiFi Captive Portal Access Point

**What this teaches:** The Pico 2W has a WiFi radio built in (that's what the "W" means), and
CircuitPython can turn it into its own tiny WiFi network — an **access point** — instead of just
joining someone else's. This exercise builds on the `blink.py` program from Part 5: instead of
only blinking the LED, the board also runs a small web server that any phone or laptop can connect
to and see the LED's current on/off status on a webpage, live, with no laptop cable required.

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
> you copied `neopixel.mpy` in Part 4 — grab it from the same Adafruit CircuitPython Library
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

- This is exactly how a smart plug, WiFi light bulb, or new WiFi router gets set up for the first
  time — you connect to a small network the device broadcasts, then configure it from a webpage,
  before it ever joins your real home network.
- Field sensors deployed somewhere without existing WiFi (a garden, a remote enclosure) use this
  same pattern to let a technician walk up, connect directly, and check status without carrying a
  laptop cable or router.

### Homework 2 — Print the Pico 2W's Pin Map to the Console

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
print("https://datasheets.raspberrypi.com/pico2/pico-2-w-pinout.pdf")
```

**Test it:** Save as `code.py`, then open the Serial console (Mu) or Shell pane (Thonny) and press
`Ctrl+D` to soft-reboot and rerun it. You should see every `board.GP*` name printed along with its
underlying pin, followed by the special-function table.

**Real-world examples:**

- Any time you pick up someone else's project code and it says `import board` then
  `board.GP1` — this script is how you'd confirm, on your *own* board, whether `GP1` is
  actually the I2C clock line before you go wire a sensor to it.
- Professional embedded engineers do this same kind of self-check ("pin introspection") when
  debugging a new board revision, to catch cases where a pin's silkscreen label, chip datasheet
  name, and framework name have drifted out of sync — exactly the confusion this exercise
  prevents.

### Homework 3 — Log the Pico 2W's Own Internal Temperature

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

- Laptops, phones, and game consoles all read an internal chip temperature sensor like this one to
  decide when to spin up a fan or throttle performance before overheating causes damage.
- Server rooms and data centers log exactly this kind of self-reported chip temperature across
  thousands of machines to catch a failing cooling system before it causes an outage.

### Homework 4 — Bouncing Shape Animation on the TFT Display

**What this teaches:** *(Requires the TFT display used later in this course — see the "1.14"
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

- This exact bounce-and-reverse-velocity pattern is the starting point for real game physics
  engines — Pong, Breakout, and any game with objects that ricochet off walls all extend this same
  idea.
- Digital signage and kiosk displays use idle "screensaver" animations like this one to avoid
  burning a static image into the screen during long periods with no user interaction.

---

