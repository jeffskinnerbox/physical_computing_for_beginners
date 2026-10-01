# Install and Run wireframe.py on a Windows 11 Laptop


## Purpose

In Class 4 your Pico reads its IMU (the motion sensor) and prints its orientation — roll, pitch,
and yaw — over the USB cable about 50 times a second. `wireframe.py` is a small Python program that
runs on your **laptop**, reads those numbers, and draws a 3D box on your screen that tilts and
turns exactly the way you tilt and turn the board.

When you finish this guide you'll have `wireframe.py` downloaded, a tool called **uv** installed to
run it, and a live 3D box following your Pico around. You won't need to install any Python packages
by hand, create a virtual environment, or even care which version of Python is on your laptop — uv
takes care of all of that for you.

> **Why uv instead of `pip install`?** Everyone's laptop has a different Python (or none). `uv`
> reads a short list written at the top of `wireframe.py` that says "I need Python 3.10 or newer,
> plus `numpy`, `matplotlib`, and `pyserial`." It finds (or downloads) a matching Python, installs
> those packages into a private hidden folder, and runs the program — every time, the same way, on
> every laptop.


## What gets installed

| Component | What it does | Why you need it | Instructions source | Official docs |
| :-------- | :----------- | :-------------- | :------------------ | :------------ |
| uv | A fast Python tool that installs Python versions and packages and runs Python programs | Runs `wireframe.py` with the right Python and packages without any setup from you | [Installing uv][01] | [uv documentation][02] |
| `wireframe.py` | The Class 4 laptop program that draws a live 3D box from the Pico's roll/pitch/yaw | It's the thing you're here to run | [Course GitHub repository][03] | [Class 4 lesson script][04] |
| Python 3.10 or newer (automatic) | The Python interpreter | `wireframe.py` is a Python program. uv uses the Python you already have if it's new enough, or downloads its own private copy if not | [Running scripts with uv][05] | [Python on Windows][06] |
| `numpy`, `matplotlib`, `pyserial` (automatic) | Fast math, plotting, and USB serial-port access for Python | `wireframe.py` imports all three. uv installs them for you the first time it runs | [Running scripts with uv][05] | [NumPy][07], [Matplotlib][08], [pySerial][09] |


## Target environment

- **Machine:** Windows 11 laptop (64-bit Intel/AMD or ARM)
- **Minimum hardware:** about 300 MB of free disk space (uv, possibly a private Python, and the three
  packages), and a free USB port for the Pico
- **Accounts / access needed:** your normal Windows account — a standard (non-administrator) account
  is fine. Nothing in this guide needs an administrator password.
- **Network:** normal internet access the first time (to download uv, `wireframe.py`, and the
  packages). After that, `wireframe.py` runs offline.
- **Before you start, you should already have:**
  - Windows Terminal (built into Windows 11 — right-click **Start** and choose **Terminal**)
  - Thonny set up for your Pico (from the Pre-Class setup)
  - Your Pico 2 W wired to the LSM9DS1 IMU and running the Class 4 `class-4-phase-1-code.py`
      (or `class-4-phase-3-code.py`) as its `code.py`


## Installation


### On your Windows 11 laptop — install uv

Everything in this guide happens in Windows Terminal on your laptop. First you'll install uv, the
one tool that does all the Python work for you. It installs into your own user folder, so no
administrator password is needed.

Use a **regular** Terminal window, not "Run as administrator". You can copy each gray block and
paste it straight into Terminal, comments and all (PowerShell ignores lines that start with `#`).
If Terminal warns "you are about to paste multiple lines", click **Paste anyway**.


#### Install uv

```powershell
# This one line downloads uv's official installer script and runs it.
#   powershell                  = start a fresh PowerShell just for this install
#   -ExecutionPolicy ByPass     = allow this ONE installer script to run, even if your laptop is set
#                                 to block scripts (it only applies to this single command)
#   irm                         = short for Invoke-RestMethod: download the text at this web address
#   | iex                       = short for Invoke-Expression: run the downloaded text as a script
# uv is copied into  C:\Users\<you>\.local\bin  and that folder is added to your PATH (the list of
# folders Windows searches when you type a command name).
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

When it prints `everything's installed!`, **close this Terminal window and open a new one.** A
window that was already open still has the old PATH, so it won't find `uv` yet.

> **Script blocked by your school or antivirus?** Try Windows' own package manager instead — it
> installs the same uv:
>
> ```powershell
> # winget = the Windows Package Manager (built into Windows 11)
> #   --id astral-sh.uv  = the official uv package
> #   -e                 = "exact": match that ID exactly, so winget can't pick a look-alike
> #   --accept-source-agreements / --accept-package-agreements
> #                      = answer "yes" to winget's one-time "do you agree to the terms?"
> #                        questions, so the install doesn't stop and wait for you
> winget install --id astral-sh.uv -e --accept-source-agreements --accept-package-agreements
> ```
>
> Then close and reopen Terminal, same as above.

**Test it**

```powershell
# Prints uv's version number.
# Expected output: something like  uv 0.12.20 (....)  -- any version number is fine.
uv --version

# A real test: ask uv to run a one-line Python program that needs numpy.
#   --with numpy   = "make numpy available for this run" (uv installs it into its private cache)
#   python -c "..." = run the Python code inside the quotes
# If you have no suitable Python yet, uv downloads one first -- the first run can take a minute.
# Expected output:  [0 2 4 6 8]
uv run --with numpy python -c "import numpy; print(numpy.arange(5) * 2)"
```

**Clean up**

Nothing to delete. The test didn't create any files in your folders — uv keeps the numpy it
downloaded in its private cache, where `wireframe.py` will reuse it later.


### On your Windows 11 laptop — download wireframe.py

Next you'll make a folder for your laptop-side Class 4 files and download `wireframe.py` into it,
straight from the course's GitHub repository. Keep it on your laptop — **not** on the `CIRCUITPY`
drive, because this program runs on your computer, not on the Pico.


#### Make a folder and download the file

```powershell
# Make a folder called class-4 in your user folder, C:\Users\<you>\class-4.
# (Not inside Documents -- on many laptops Documents is really a OneDrive folder somewhere else.)
#   $HOME               = your user folder, C:\Users\<you>
#   -ItemType Directory = make a folder, not a file
#   -Force              = don't complain if the folder already exists
#   | Out-Null          = hide the little table New-Item normally prints about the new folder
New-Item -ItemType Directory -Force "$HOME\class-4" | Out-Null

# Move into that folder, so the next command saves the file there.
Set-Location "$HOME\class-4"

# Download wireframe.py from GitHub.
#   Invoke-WebRequest  = PowerShell's "download a web page or file" command
#   -Uri               = the web address to download. "raw.githubusercontent.com" gives you the
#                        plain file itself, not the GitHub web page around it
#   -OutFile           = the name to save it as, in the current folder
#   -UseBasicParsing   = just save the file, don't treat it as a web page to run. Without it,
#                        Windows PowerShell 5.1 (Windows 11's default) shows a "Script Execution
#                        Risk" warning and cancels the download if you press Enter.
#                        PowerShell 7 ignores this flag, so it's safe either way.
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/jeffskinnerbox/physical_computing_for_beginners/main/src/wireframe/wireframe.py" -OutFile "wireframe.py" -UseBasicParsing
```

**Test it**

```powershell
# Show the first 5 lines of the file you downloaded.
#   -TotalCount 5 = stop after 5 lines
# Expected output -- this is the block that tells uv what the program needs:
#   #!/usr/bin/env -S uv run --script
#   # /// script
#   # requires-python = ">=3.10"
#   # dependencies = ["numpy", "matplotlib", "pyserial"]
#   # ///
Get-Content wireframe.py -TotalCount 5
```

If you see HTML (lines starting with `<`) or `404: Not Found` instead, the address was mistyped —
copy the `Invoke-WebRequest` line again exactly.

**Clean up**

Nothing to delete — `wireframe.py` is the file you want to keep.


### On your Pico and in Thonny — get the board ready

`wireframe.py` doesn't talk to Thonny — it talks straight to the Pico over the USB cable. Only
**one** program at a time can use the Pico's USB serial port, so Thonny has to let go of it first.


#### Hand the serial port over from Thonny

1. Make sure your Pico is plugged in and its `code.py` is `class-4-phase-1-code.py` (or
   `class-4-phase-3-code.py`). In Thonny's Shell you should see lines like `-1.9, 2.6, -167.0`
   scrolling by.
2. **Close Thonny.** That's the surest way to free the port. (Or, in Thonny, click the red **Stop**
   button and then choose **Run → Disconnect** — but don't click Stop or Run again while
   `wireframe.py` is running, or Thonny grabs the port back.)
3. Unplug the Pico and plug it back in. Thonny's Stop left your program stopped; replugging restarts
   `code.py` so it streams numbers again. If you're running `class-4-phase-3-code.py`, keep the board
   **still** for a few seconds after plugging in — it's measuring its gyro drift.

**Test it**

```powershell
# Ask pyserial to list the serial ports it can see.
#   --with pyserial        = make pyserial available for this run
#   -m serial.tools.list_ports = run pyserial's built-in port-listing tool
#   -v                     = "verbose": also print each port's description and USB ID
# Expected output includes your Pico, something like:
#   COM5
#       desc: USB Serial Device (COM5)
#       hwid: USB VID:PID=239A:8162 SER=... LOCATION=...
#   1 ports found
# The count may be higher if your laptop has other ports (like Bluetooth) -- that's fine.
# Your Pico is the one whose VID (USB vendor ID) is 239A or 2E8A. wireframe.py looks for exactly
# those two numbers to find your Pico by itself.
uv run --with pyserial python -m serial.tools.list_ports -v
```

Your COM number may differ (`COM3`, `COM7`, ...) — that's fine.

**Clean up**

Nothing to delete — this only listed ports.


### On your Windows 11 laptop — run wireframe.py

Now the payoff. You'll run `wireframe.py` with uv, which finds the Pico's port by itself and opens a
window with a 3D box in it.


#### Run it

```powershell
# Go to the folder where you saved wireframe.py (skip this if you're already there).
Set-Location "$HOME\class-4"

# Run the program.
#   uv run  = read the requirements block at the top of wireframe.py, get a matching Python and
#             packages ready, then run the program
# The FIRST run downloads matplotlib and friends, so it may take a minute. Later runs start in a
# couple of seconds.
uv run wireframe.py
```

The first time only, you may also see `Installed ... packages in ...` and
`Matplotlib is building the font cache; this may take a moment.` — both are normal.

Expected output in Terminal:

```text
Class 4, Phase 2 -- 3D box display starting, reading from COM5
Close the window or press Ctrl-C to stop.
```

A window titled **Figure 1** opens with a blue wireframe box, red **Front** and **Right** labels,
and a title like `roll=-2 pitch=3 yaw=-167`.

> **Tip:** if you have more than one CircuitPython board plugged in, or auto-detect picks the wrong
> port, name the port yourself:
>
> ```powershell
> # Replace COM5 with the COM number from the port-listing test above.
> uv run wireframe.py COM5
> ```

**Test it**

1. Tilt the Pico forward and back — the box's **Front** end should dip and rise, and the `pitch`
   number in the window's title should change.
2. Roll it left and right — the box should roll the same way, and `roll` should change.
3. Turn it flat on the table like a steering wheel — the box should spin and `yaw` should change.

**Clean up — stop the program**

Either close the **Figure 1** window, or click in Terminal and press **Ctrl-C**. Either way you
should see:

```text
Stopped -- serial port closed.
```

That means the port is free again. Open Thonny (or click its red **Stop** button) to reconnect to
the Pico and keep working on its code.


## Troubleshooting

| Problem | Likely cause | Fix |
| :------ | :----------- | :-- |
| `The term 'uv' is not recognized...` | Terminal was open before uv was installed | Close Terminal and open a new window |
| `Couldn't find a Pico. Check the USB cable...` | Pico not plugged in, a charge-only USB cable, or the board isn't running CircuitPython | Replug the Pico with a data cable; check it shows up in the port-listing test. Or name the port: `uv run wireframe.py COM5` |
| `Couldn't open COM5: ... PermissionError ... Access is denied` then `Is Thonny still connected?...` | Thonny (or another program) still has the port open | Close Thonny (or **Stop**, then **Run → Disconnect**). Close any other serial monitor and try again |
| `Couldn't open COM9: ... FileNotFoundError ...` | You named a COM port that doesn't exist | Run the port-listing test again and use the COM number it shows, or leave the port off and let `wireframe.py` find it |
| Window opens but the box never moves | The Pico isn't printing roll,pitch,yaw lines (often: Thonny's Stop left it at the REPL) | Stop `wireframe.py`, unplug and replug the Pico, and run again. Still stuck? Open Thonny and check its Shell shows numbers scrolling |
| No window appears at all (maybe a warning mentioning `FigureCanvasAgg is non-interactive`) | Your own Python was installed without its "tcl/tk" part, which matplotlib needs to draw windows | Tell uv to use its own complete Python instead: `uv run --managed-python wireframe.py` |
| Box moves but lags behind | Laptop is busy | Close other programs; the box always jumps to the newest reading, so it catches up |
| `Invoke-WebRequest` shows `404: Not Found` | Mistyped address | Copy the download command again exactly |
| Installer is blocked by school IT or antivirus | The laptop doesn't allow downloaded scripts | Use the `winget install --id astral-sh.uv -e` option, or ask your instructor |


## Removing everything (optional)

Only do this after the course, if you want uv and everything it downloaded gone.

```powershell
# Delete uv's cache -- the packages (numpy, matplotlib, pyserial) and script environments.
uv cache clean

# Delete any private Python versions uv downloaded.
#   $(uv python dir) = ask uv where it keeps its Pythons, then use that folder name
#   -Recurse         = delete the folder and everything inside it
#   -ErrorAction SilentlyContinue = don't complain if uv never downloaded one
Remove-Item -Recurse -Force "$(uv python dir)" -ErrorAction SilentlyContinue

# Delete uv itself (the three program files the installer added).
Remove-Item "$HOME\.local\bin\uv.exe", "$HOME\.local\bin\uvx.exe", "$HOME\.local\bin\uvw.exe" -ErrorAction SilentlyContinue

# Delete your Class 4 folder (only if you don't want wireframe.py any more).
Remove-Item -Recurse -Force "$HOME\class-4"
```

If you installed uv with `winget` instead, replace the "Delete uv itself" line with
`winget uninstall --id astral-sh.uv -e`. The installer also added `C:\Users\<you>\.local\bin` to your
PATH; leaving it there is harmless.


[01]:https://docs.astral.sh/uv/getting-started/installation/
[02]:https://docs.astral.sh/uv/
[03]:https://github.com/jeffskinnerbox/physical_computing_for_beginners
[04]:../lesson_scripts/class-04-lesson-script.md
[05]:https://docs.astral.sh/uv/guides/scripts/
[06]:https://docs.python.org/3/using/windows.html
[07]:https://numpy.org/doc/stable/
[08]:https://matplotlib.org/stable/
[09]:https://pyserial.readthedocs.io/
