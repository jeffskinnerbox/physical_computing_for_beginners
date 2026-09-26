# Install Python 3 on a Windows 11 Laptop

## Purpose

Most of this course's Python runs on the Pico, inside CircuitPython. But starting in Class 4, you
also run a regular Python program on your *laptop*: `wireframe.py`, which reads your IMU's
orientation over the USB cable and draws a 3D box that tilts when you tilt the board. That needs a
normal Python 3 install on Windows, plus three add-on packages (`pyserial`, `matplotlib`, `numpy`).

When you finish this guide you'll have Python 3.14 installed just for your own Windows account — no
administrator password needed — and you'll have proven it works by installing those same three
packages into a throwaway test folder and drawing a small chart with them.

This is the long version of Step 5 in the [Pre-Class lesson script][01]. If that short version
already worked for you, you don't need this guide.

## What gets installed

| Component | What it does | Why you need it | Instructions source | Official docs |
| :-------- | :----------- | :-------------- | :------------------ | :------------ |
| Python 3.14 | The regular Python interpreter for Windows, plus `pip` (Python's package installer) | Runs laptop-side course programs like Class 4's `wireframe.py` | [winget-pkgs `Python.Python.3.14` manifest][02] | [Using Python on Windows][03] |
| Python Launcher for Windows (`py`) | A small command that finds and starts whichever Python versions you have installed (the classic launcher that comes with this installer) | Gives you a `py` command that works even when `python` doesn't | [winget-pkgs `Python.Python.3.14` manifest][02] | [Python Launcher for Windows][04] |
| `pyserial`, `matplotlib`, `numpy` (test only) | Serial-port access, plotting, and fast math for Python | Class 4's `wireframe.py` imports all three — installing them here proves `pip` works | [Class 4 lesson script][05] | [pySerial][06], [Matplotlib][07], [NumPy][08] |

## Target environment

- **Machine:** Windows 11 laptop (64-bit Intel/AMD, or ARM)
- **Minimum hardware:** about 500 MB of free disk space for Python and the test packages
- **Accounts / access needed:** your normal Windows account — a standard (non-admin) account is fine
- **Network:** normal internet access (to download Python and the packages)
- **Before you start, you should already have:** Windows Terminal (built into Windows 11 — right-click
  **Start** and choose **Terminal**) and `winget` (the Windows Package Manager, also built into
  Windows 11; `winget --version` in Terminal should print a version number)

## Installation

### On your Windows 11 laptop — install Python and prove it works

Everything in this guide happens in Windows Terminal on your laptop, not on the Pico. You'll use
`winget`, Windows' built-in package manager, to download and install Python for your account only,
then check it with a real mini-project.

Use a **regular** Terminal window. You don't need "Run as administrator", and you shouldn't use it —
an admin window can install Python for the wrong account.

You can copy each gray block and paste it straight into Terminal, comments and all (PowerShell
ignores lines starting with `#`). Windows Terminal may show a "you are about to paste multiple
lines" warning — that's expected; click **Paste anyway**.

#### Install Python 3.14

```powershell
# winget = the Windows Package Manager; "install" downloads and installs a package.
#   -e                          = "exact": match the ID below exactly, so winget can't pick a
#                                 similarly named package by mistake
#   --id Python.Python.3.14     = the official python.org Python 3.14 package
#   --scope user                = install for YOUR account only -- this is what avoids needing an
#                                 administrator password
#   --accept-source-agreements  = answer "yes" to winget's one-time "do you agree to the store's
#   --accept-package-agreements   terms" questions, so the install doesn't stop and wait
#   --custom "InstallLauncherAllUsers=0"
#                               = pass one extra setting to Python's own installer: put the `py`
#                                 launcher in YOUR account too, never "for all users" (which would
#                                 need an administrator)
winget install -e --id Python.Python.3.14 --scope user --accept-source-agreements --accept-package-agreements --custom "InstallLauncherAllUsers=0"
```

When it prints `Successfully installed`, **close this Terminal window and open a new one.** The
installer adds Python to your PATH (the list of folders Windows searches when you type a command),
but a window that was already open keeps its old copy of that list.

> If an administrator-password window appears anyway, click **No**, make sure the command includes
> `--scope user` and the `--custom` part exactly, and run it again. If it still asks, a parent,
> teacher, or IT admin can approve it once.

**Test it**

```powershell
# py = the Python Launcher; --version prints the version it would start.
# Expected output: Python 3.14.x   (x is a number, e.g. 3.14.7)
py --version

# -m pip = "run pip as a module of THIS Python", which guarantees pip and Python match.
# Expected output starts with: pip 26.x (or newer) from C:\Users\<you>\AppData\Local\Programs\Python\Python314\...
# (On an ARM laptop the folder is named Python314-arm64 instead.)
py -m pip --version

# The plain "python" command should reach the same install.
# Expected output: Python 3.14.x
python --version
```

If `python --version` opens the Microsoft Store (or prints nothing) instead of a version, that's a
Windows shortcut called an *app execution alias* getting in the way. Either keep using `py` — every
`python ...` command in this course works as `py ...`, and every `pip install ...` works as
`py -m pip install ...` — or turn the shortcut off: **Settings → Apps → Advanced app settings → App
execution aliases**, then switch **off** both **App Installer python.exe** and **App Installer
python3.exe**, and open a new Terminal. (Quick way there: press **Start** and search for "Manage app
execution aliases".) If you see aliases named **Python (default)** instead, you already have the newer
Python install manager; leave those on, or uninstall the install manager first so two tools aren't
sharing the `py` command.

**Clean up**

Nothing to clean up — this block only checked versions. Keep the Windows Terminal window open for the next block.

#### Prove it works: install the Class 4 packages in a throwaway virtual environment

A *virtual environment* ("venv") is a private folder with its own copy of Python's package list, so
test packages don't clutter your main install. You'll create one in your temp folder, install the
three Class 4 packages into it, draw a small chart, and then delete the whole folder.

```powershell
# $env:TEMP is your personal temp folder. Join-Path builds the full folder path we'll use.
$testDir = Join-Path $env:TEMP "python-install-test"

# -3.14 tells the launcher to use Python 3.14 specifically.
# "-m venv <folder>" creates a new virtual environment in that folder.
py -3.14 -m venv $testDir

# We call the venv's own python.exe directly instead of "activating" the venv, because
# activation runs a script that Windows' default security setting (the execution policy) blocks.
$venvPython = Join-Path $testDir "Scripts\python.exe"

# Install the three packages Class 4's wireframe.py needs into the venv only.
# (pip downloads ready-built "wheel" files, so this takes a minute but compiles nothing.
# A "new release of pip is available" notice at the end is harmless -- ignore it.)
& $venvPython -m pip install pyserial matplotlib numpy
```

**Test it**

```powershell
# Set the folder paths again, in case you opened a new Terminal window since the last block
# (variables like $testDir disappear when a Terminal window closes).
$testDir = Join-Path $env:TEMP "python-install-test"
$venvPython = Join-Path $testDir "Scripts\python.exe"

# A tiny program that uses all three packages:
#   numpy draws a sine wave, matplotlib saves it as a PNG file (no window needed),
#   and pyserial lists your computer's serial ports (your Pico shows up here when plugged in).
$testScript = @'
import numpy as np
import matplotlib
matplotlib.use("Agg")  # "Agg" = draw straight to a file, no window
import matplotlib.pyplot as plt
from serial.tools import list_ports

x = np.linspace(0, 2 * np.pi, 100)
plt.plot(x, np.sin(x))
plt.savefig("sine-test.png")
print("numpy", np.__version__, "and matplotlib", matplotlib.__version__, "work -- saved sine-test.png")
print("serial ports found:", [port.device for port in list_ports.comports()])
'@

# Save the program into the test folder and run it with the venv's Python.
# Push-Location moves into the test folder so sine-test.png is saved there too.
$scriptPath = Join-Path $testDir "check_packages.py"
# -Encoding ascii writes plain text that Python reads the same way in any version of PowerShell.
Set-Content -Path $scriptPath -Value $testScript -Encoding ascii
Push-Location $testDir
& $venvPython $scriptPath

# Opens the chart in your default image viewer -- you should see one smooth wave.
Invoke-Item "sine-test.png"
Pop-Location
```

Expected output looks like this (versions and ports will differ; with your Pico plugged in you'll
see something like `COM5` in the list, and with nothing plugged in the list may be empty `[]`):

```text
numpy 2.5.3 and matplotlib 3.11.2 work -- saved sine-test.png
serial ports found: ['COM5']
```

**Clean up**

```powershell
# Set the folder path again, in case this is a new Terminal window.
$testDir = Join-Path $env:TEMP "python-install-test"

# Close the image viewer first, then delete the whole test folder: the venv, the three
# packages inside it, the test program, and sine-test.png.
#   -Recurse = delete everything inside the folder too
#   -Force   = don't stop to ask about each file
Remove-Item -Recurse -Force $testDir

# Should print False, meaning the folder is gone.
Test-Path $testDir
```

If `Remove-Item` complains that a file is "being used by another process" (or `Test-Path` prints
`True`), the image viewer still has `sine-test.png` open — close it and run both lines again.

Your real Python 3.14 install stays — only the test folder is gone. In Class 4 you'll install the
same three packages for real with `pip install pyserial matplotlib numpy`.

### Uninstall (only if you ever need to)

You don't need to do this for the course — Python should stay installed through Class 6. If you
want it gone later (for example, on a borrowed laptop), remove it with `winget` from a regular
Terminal window:

```powershell
# Same exact-match ID and per-user scope as the install.
winget uninstall -e --id Python.Python.3.14 --scope user
```

**Test it**

```powershell
# Open a NEW Terminal window first, then run this. Expected output: an error saying 'py' isn't
# recognized, or a message that no suitable Python runtime was found. (If you have other Python
# versions installed, you'll see one of those instead -- anything but 3.14 means it worked.)
py --version
```

**Clean up**

Nothing else to remove — `winget uninstall` removes Python 3.14 for your account, and the `py`
launcher too unless another Python version on your laptop still uses it.

> **Looking ahead:** Python's developers are moving Windows installs to a new tool called the
> [Python install manager][09]. The installer used here is still produced for Python 3.14 (it's only
> being retired starting with Python 3.16), so nothing in this course needs to change.

## Manual verification checklist (for the instructor)

These steps run on Windows, so they were reviewed on paper, not run in a test sandbox. Before
handing this guide to students, run through it once on a real Windows 11 laptop:

- [ ] On a **standard (non-admin)** account, the install command finishes with no administrator
    prompt, and `py.exe` is in `%LOCALAPPDATA%\Programs\Python\Launcher`.
- [ ] The winget output shows it downloaded `python-3.14.x-amd64.exe` (or `-arm64.exe`), not a `.zip`.
- [ ] In a new Terminal, `py --version`, `py -m pip --version`, and `python --version` all report 3.14.x.
- [ ] The venv block installs all three packages from wheels (no build step), and the Test block
    prints both lines and opens a sine-wave chart.
- [ ] Clean up leaves `Test-Path` printing `False` (and the retry hint works if the viewer is left open).
- [ ] Closing Terminal between blocks doesn't break the Test or Clean up blocks.
- [ ] On a laptop that already has an all-users `py` launcher, the install still needs no admin prompt
    and `py -3.14 --version` works.
- [ ] On a laptop with the Python install manager, note which alias names appear and what
    `py --version` reports.
- [ ] `winget uninstall` needs no admin prompt, and `py --version` afterwards matches the guide.
- [ ] If an ARM64 Windows laptop is available, repeat the install and test there.

## Further reading

- [5 Easy Ways to Install Python on Windows][10] — other install options compared

[01]:../lesson_scripts/class-00-lesson-script.md
[02]:https://github.com/microsoft/winget-pkgs/tree/master/manifests/p/Python/Python/3/14
[03]:https://docs.python.org/3.14/using/windows.html
[04]:https://docs.python.org/3.14/using/windows.html#python-launcher-for-windows-deprecated
[05]:../lesson_scripts/class-04-lesson-script.md
[06]:https://pyserial.readthedocs.io/
[07]:https://matplotlib.org/stable/
[08]:https://numpy.org/doc/stable/
[09]:https://docs.python.org/3/using/windows.html#python-install-manager
[10]:https://www.kdnuggets.com/5-easy-ways-to-install-python-on-windows
