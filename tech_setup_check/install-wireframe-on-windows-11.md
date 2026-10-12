# Install and Run wireframe.py on a Windows 11 Laptop


## Purpose
This guide tells you how to install and run `wireframe.py` on your Windows 11 laptop.
`wireframe.py` is a Python program that shows a 3D box on your laptop screen. The box turns when you turn the Pico.

In Class 4, the Pico reads its IMU. An IMU (Inertial Measurement Unit) is a motion sensor.
The Pico calculates its orientation from the IMU data. Orientation is three angles: roll, pitch, and yaw.
The Pico sends these three angles to your laptop through the USB cable, approximately 50 times each second.

This diagram shows how the data goes from the IMU to the 3D box:

```text
 +-----------+     +-------------+     USB cable    +----------------+     +------------+
 | LSM9DS1   +---->| Pico 2 W    +----------------->| wireframe.py   +---->| 3D box on  |
 | IMU       |     | (code.py)   |    roll, pitch,  | on your laptop |     | the screen |
 +-----------+     +-------------+    yaw (text)    +----------------+     +------------+
```

At the end of this guide, you have these items:

* `wireframe.py` on your laptop.
* A tool with the name **uv**, which runs `wireframe.py`.
* A 3D box on your screen that turns when the Pico turns.

You do not install Python packages yourself. You do not make a virtual environment. uv does these tasks for you.

> **Why use uv and not `pip install`?** Each laptop can have a different version of Python, or no Python.
> At the top of `wireframe.py`, there is a short list. The list says: "I need Python 3.10 or newer, and the packages `numpy`, `matplotlib`, and `pyserial`."
>
> uv reads this list. uv finds a correct version of Python, or downloads one.
> Then uv installs the packages into a private, hidden folder and runs the program.
> uv does these steps the same way each time, on each laptop.

This diagram shows what uv does when you type `uv run wireframe.py`:

```text
        uv run wireframe.py
               |
               v
 +------------------------------+
 | 1. Read the list at the top  |
 |    of wireframe.py           |
 +--------------+---------------+
                |
                v
 +------------------------------+    no     +---------------------------+
 | 2. Is Python 3.10 or newer   +---------->| Download a private Python |
 |    on the laptop?            |           +-------------+-------------+
 +--------------+---------------+                         |
                | yes                                     |
                v                                         |
 +------------------------------+                         |
 | 3. Install numpy, matplotlib,|                         |
 |    pyserial in a private     |<------------------------+
 |    cache (first run only)    |
 +--------------+---------------+
                |
                v
 +------------------------------+
 | 4. Run wireframe.py          |
 +------------------------------+
```


## What You Install

| Component | What it does | Why you need it | Instructions source | Official docs |
| :-------- | :----------- | :-------------- | :------------------ | :------------ |
| uv | A fast Python tool. It installs Python versions and packages, and it runs Python programs. | It runs `wireframe.py` with the correct Python and packages. You do not set up Python yourself. | [Installing uv][01] | [uv documentation][02] |
| `wireframe.py` | The Class 4 laptop program. It shows a live 3D box from the roll, pitch, and yaw of the Pico. | This is the program that you run in this guide. | [Course GitHub repository][03] | [Class 4 lesson script][04] |
| Python 3.10 or newer (automatic) | The Python interpreter. | `wireframe.py` is a Python program. If your Python is new enough, uv uses it. If not, uv downloads a private Python. | [Running scripts with uv][05] | [Python on Windows][06] |
| `numpy`, `matplotlib`, `pyserial` (automatic) | Fast math, graphs, and access to the USB serial port. | `wireframe.py` uses these three packages. uv installs them the first time that the program runs. | [Running scripts with uv][05] | [NumPy][07], [Matplotlib][08], [pySerial][09] |


## Target Environment
* **Laptop:** Windows 11, 64-bit (Intel, AMD, or ARM).
* **Minimum hardware:**
  * Approximately 300 MB of free disk space for uv, a private Python (if necessary), and the three packages.
  * One free USB port for the Pico.
* **Account:** Your usual Windows account. A standard account (not administrator) is correct. This guide does not need an administrator password.
* **Network:** You need internet access the first time, to download uv, `wireframe.py`, and the packages. After that, `wireframe.py` runs without internet access.
* **Before you start, make sure you have these items:**
  * Windows Terminal. It is part of Windows 11. To open it, right-click **Start** and select **Terminal**.
  * Thonny, set up for your Pico (from the Pre-Class setup).
  * Your Pico 2 W, connected to the LSM9DS1 IMU. Its `code.py` must be the Class 4 `class-4-phase-1-code.py` (or `class-4-phase-3-code.py`).


## Installation


### On Your Windows 11 Laptop - Install uv
You do all the steps in this guide in Windows Terminal on your laptop. Windows Terminal uses PowerShell, a command language for Windows.
First, install uv. uv installs into your user folder, thus you do not need an administrator password.

Obey these rules for Terminal:

* Use a usual Terminal window. Do not use "Run as administrator".
* You can copy each gray block and paste it into Terminal, with the comments. PowerShell ignores lines that start with `#`.
* If Terminal shows the warning "you are about to paste multiple lines", click **Paste anyway**.


#### Install uv

```powershell
# This line downloads the official uv installer script and runs it.
#   powershell                  = start a new PowerShell only for this installation
#   -ExecutionPolicy ByPass     = let this ONE installer script run, also if your laptop blocks scripts
#                                 (this setting applies only to this command)
#   irm                         = Invoke-RestMethod: download the text at this web address
#   | iex                       = Invoke-Expression: run the downloaded text as a script
# The installer copies uv into  C:\Users\<you>\.local\bin
# The installer also adds that folder to your PATH.
# PATH is the list of folders where Windows looks for a command name that you type.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

When the installer shows `everything's installed!`, do these steps:

1. Close this Terminal window.
2. Open a new Terminal window.

Note: A Terminal window that was open before the installation has the old PATH. It cannot find `uv`.

> **Did your school or your antivirus program block the script?** Use the Windows Package Manager. It installs the same uv:
>
> ```powershell
> # winget = the Windows Package Manager (part of Windows 11)
> #   --id astral-sh.uv  = the official uv package
> #   -e                 = "exact": use only this ID, so that winget does not select a different package
> #   --accept-source-agreements / --accept-package-agreements
> #                      = say "yes" to the winget questions about the terms
> #                        (so that the installation does not stop to wait for you)
> winget install --id astral-sh.uv -e --accept-source-agreements --accept-package-agreements
> ```
>
> Then close Terminal and open a new Terminal window, as above.

**Test It**

```powershell
# Show the uv version number.
# Expected output: a line similar to  uv 0.12.20 (....)  -- each version number is correct.
uv --version

# Do a real test: tell uv to run a one-line Python program that needs numpy.
#   --with numpy    = "make numpy available for this run" (uv puts it in its private cache)
#   python -c "..." = run the Python code in the quotes
# If you do not have a correct Python, uv downloads one first.
# Thus the first run can take one minute.
# Expected output:  [0 2 4 6 8]
uv run --with numpy python -c "import numpy; print(numpy.arange(5) * 2)"
```

**Clean Up**

Do not delete anything. The test did not make files in your folders.
uv keeps the downloaded numpy in its private cache. A cache is a folder where a program keeps files to use again.
Later, `wireframe.py` uses this numpy again.


### On Your Windows 11 Laptop - Download wireframe.py
Next, make a folder for your Class 4 laptop files. Then download `wireframe.py` from the course GitHub repository into this folder.

> **CAUTION:** Keep `wireframe.py` on your laptop. Do not put it on the `CIRCUITPY` drive. This program runs on your laptop, not on the Pico.


#### Make a Folder and Download the File

```powershell
# Make a folder with the name class-4 in your user folder: C:\Users\<you>\class-4
# Do not put it in Documents. On many laptops, Documents is a OneDrive folder in a different location.
#   $HOME               = your user folder, C:\Users\<you>
#   -ItemType Directory = make a folder, not a file
#   -Force              = do not show an error if the folder exists
#   | Out-Null          = do not show the table that New-Item usually shows for a new folder
New-Item -ItemType Directory -Force "$HOME\class-4" | Out-Null

# Go into the folder. The next command saves the file here.
Set-Location "$HOME\class-4"

# Download wireframe.py from GitHub.
#   Invoke-WebRequest  = the PowerShell command that downloads a web page or a file
#   -Uri               = the web address to download from
#                        "raw.githubusercontent.com" gives only the file, without the GitHub web page
#   -OutFile           = the name of the saved file, in the current folder
#   -UseBasicParsing   = save the file only. Do not process it as a web page.
#                        Windows PowerShell 5.1 is the default in Windows 11.
#                        Without this flag, PowerShell 5.1 shows a "Script Execution Risk" warning.
#                        If you then push Enter, the download stops.
#                        PowerShell 7 ignores this flag. Thus the command is safe in both versions.
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/jeffskinnerbox/physical_computing_for_beginners/main/lesson_scripts/wireframe.py" -OutFile "wireframe.py" -UseBasicParsing
```

**Test It**

```powershell
# Show the first 5 lines of the downloaded file.
#   -TotalCount 5 = stop after 5 lines
# Expected output. These lines tell uv what the program needs:
#   #!/usr/bin/env -S uv run --script
#   # /// script
#   # requires-python = ">=3.10"
#   # dependencies = ["numpy", "matplotlib", "pyserial"]
#   # ///
Get-Content wireframe.py -TotalCount 5
```

If you see HTML (lines that start with `<`) or `404: Not Found`, the web address is not correct.
Copy the `Invoke-WebRequest` line again, exactly as it is above.

**Clean Up**

Do not delete anything. You must keep `wireframe.py`.


### On Your Pico and in Thonny - Prepare the Pico
`wireframe.py` does not use Thonny. It gets data directly from the Pico through the USB cable.
The USB connection to the Pico is a serial port. On Windows, a serial port has a COM name, for example `COM5`.
Only one program at a time can use the serial port of the Pico. Thus, Thonny must release the serial port first.

This diagram shows the two possible owners of the serial port:

```text
 BEFORE (Thonny has the serial port)      AFTER (wireframe.py has the serial port)

 +-------+   COM5   +--------+            +-------+   COM5   +--------------+
 | Pico  +--------->| Thonny |            | Pico  +--------->| wireframe.py |
 +-------+          +--------+            +-------+          +--------------+
                    wireframe.py: error                      Thonny: closed
```


#### Release the Serial Port from Thonny
1. Connect the Pico to the laptop.
2. Make sure its `code.py` is `class-4-phase-1-code.py` (or `class-4-phase-3-code.py`).
   In the Thonny Shell, you see lines similar to `-1.9, 2.6, -167.0` that move up the screen.
3. Close Thonny. This is the best method to release the serial port.
   If you cannot close Thonny, click the red **Stop** button in Thonny. Then select **Run → Disconnect**.
   After this, do not click **Stop** or **Run** again while `wireframe.py` runs. If you do, Thonny takes the serial port again.
4. Disconnect the USB cable from the Pico. Then connect it again.
   This starts `code.py` again, and the Pico sends data again. (The Thonny **Stop** button stopped your program.)
5. If your `code.py` is `class-4-phase-3-code.py`, do not move the Pico for some seconds after you connect it.
   During this time, the Pico measures the drift of its gyroscope.
   The gyroscope is the part of the IMU that measures rotation. Drift is a small error that increases with time.

**Test It**

```powershell
# Tell pyserial to show a list of the serial ports that it can find.
#   --with pyserial             = make pyserial available for this run
#   -m serial.tools.list_ports  = run the port list tool that is part of pyserial
#   -v                          = "verbose": also show the description and USB ID of each port
# Expected output includes your Pico, similar to this:
#   COM5
#       desc: USB Serial Device (COM5)
#       hwid: USB VID:PID=239A:8162 SER=... LOCATION=...
#   1 ports found
# If your laptop has other ports (for example, Bluetooth), the number can be larger. This is correct.
# VID is the USB vendor ID. The VID of your Pico is 239A or 2E8A.
# wireframe.py looks for these two VID numbers to find your Pico automatically.
uv run --with pyserial python -m serial.tools.list_ports -v
```

Your COM number can be different (for example, `COM3` or `COM7`). This is correct.

**Clean Up**

Do not delete anything. This test only showed a list of ports.


### On Your Windows 11 Laptop - Run wireframe.py
Now run `wireframe.py` with uv. The program finds the serial port of the Pico automatically. Then it opens a window with a 3D box.


#### Run the Program

```powershell
# Go to the folder that has wireframe.py. (If you are in this folder, you can skip this line.)
Set-Location "$HOME\class-4"

# Run the program.
#   uv run = read the list at the top of wireframe.py, prepare a correct Python and the packages,
#            then run the program
# The FIRST run downloads matplotlib and the other packages. Thus it can take one minute.
# Later runs start in approximately two seconds.
uv run wireframe.py
```

The first time only, you can also see these two messages. Both are usual:

* `Installed ... packages in ...`
* `Matplotlib is building the font cache; this may take a moment.`

Expected output in Terminal:

```text
Class 4, Phase 2 -- 3D box display starting, reading from COM5
Close the window or press Ctrl-C to stop.
```

A window with the title **Figure 1** opens. The window shows these items:

* A blue wireframe box.
* Red **Front** and **Right** labels.
* A title similar to `roll=-2 pitch=3 yaw=-167`.

> **Tip:** Name the serial port yourself in these conditions:
>
> * You connect more than one CircuitPython board to the laptop.
> * `wireframe.py` finds the wrong serial port.
>
> ```powershell
> # Replace COM5 with the COM number from the port list test above.
> uv run wireframe.py COM5
> ```

**Test It**

1. Tilt the Pico forward and back. The **Front** end of the box goes down and up. The `pitch` number in the window title changes.
2. Roll the Pico to the left and to the right. The box rolls in the same direction. The `roll` number changes.
3. Put the Pico flat on the table and turn it, as you turn a steering wheel. The box turns. The `yaw` number changes.

**Clean Up - Stop the Program**

1. Do one of these steps:
    * Close the **Figure 1** window.
    * Click in Terminal and push **Ctrl-C**.
2. Make sure Terminal shows this message:

    ```text
    Stopped -- serial port closed.
    ```

    This message tells you that the serial port is free again.
3. To connect Thonny to the Pico again, open Thonny (or click the red **Stop** button in Thonny). Then you can continue to work on the code.


## Troubleshooting

| Problem | Possible cause | Fix |
| :------ | :------------- | :-- |
| `The term 'uv' is not recognized...` | Terminal was open before you installed uv. | Close Terminal. Open a new Terminal window. |
| `Couldn't find a Pico. Check the USB cable...` | The Pico is not connected, the USB cable is charge-only, or the Pico does not run CircuitPython. | Connect the Pico again with a data cable. Make sure the Pico shows in the port list test. Or name the serial port: `uv run wireframe.py COM5` |
| `Couldn't open COM5: ... PermissionError ... Access is denied`, then `Is Thonny still connected?...` | Thonny (or a different program) has the serial port. | Close Thonny (or click **Stop**, then select **Run → Disconnect**). Close all other serial monitor programs. Then try again. |
| `Couldn't open COM9: ... FileNotFoundError ...` | The COM port that you named does not exist. | Do the port list test again. Use the COM number that it shows. Or do not name a port, and let `wireframe.py` find it. |
| The window opens, but the box does not move. | The Pico does not send roll, pitch, and yaw lines. Usually, Thonny **Stop** left it at the REPL (the prompt). | Stop `wireframe.py`. Connect the Pico again. Run it again. If the box does not move, look for numbers in the Thonny Shell. |
| No window opens (possibly with a warning about `FigureCanvasAgg is non-interactive`). | Your Python does not have its "tcl/tk" part. Matplotlib needs this part to show windows. | Tell uv to use its own complete Python: `uv run --managed-python wireframe.py` |
| The box moves, but it is late. | The laptop has too much work. | Close other programs. The box always goes to the newest data, thus it gets back to the correct position. |
| `Invoke-WebRequest` shows `404: Not Found`. | The web address is not correct. | Copy the download command again, exactly as it is. |
| Your school IT or antivirus program blocks the installer. | The laptop does not let downloaded scripts run. | Use the `winget install --id astral-sh.uv -e` method, or speak to your instructor. |


## Remove All Installed Items (Optional)
Do these steps only after the course, if you want to remove uv and all the files that it downloaded.

```powershell
# Delete the uv cache. The cache has the packages (numpy, matplotlib, pyserial) and the script environments.
uv cache clean

# Delete the private Python versions that uv downloaded.
#   $(uv python dir)              = get the name of the folder where uv keeps its Python versions
#   -Recurse                      = delete the folder and all the items in it
#   -ErrorAction SilentlyContinue = do not show an error if uv did not download a Python
Remove-Item -Recurse -Force "$(uv python dir)" -ErrorAction SilentlyContinue

# Delete uv. These are the three program files that the installer added.
Remove-Item "$HOME\.local\bin\uv.exe", "$HOME\.local\bin\uvx.exe", "$HOME\.local\bin\uvw.exe" -ErrorAction SilentlyContinue

# Delete your Class 4 folder. Do this only if you do not want to keep wireframe.py.
Remove-Item -Recurse -Force "$HOME\class-4"
```

If you installed uv with `winget`, do not use the "Delete uv" line above. Use this command:

```powershell
# Remove uv with the Windows Package Manager.
winget uninstall --id astral-sh.uv -e
```

Note: The installer also added `C:\Users\<you>\.local\bin` to your PATH. You can keep it there. It does not cause problems.



[01]:https://docs.astral.sh/uv/getting-started/installation/
[02]:https://docs.astral.sh/uv/
[03]:https://github.com/jeffskinnerbox/physical_computing_for_beginners
[04]:../lesson_scripts/class-04-lesson-script.md
[05]:https://docs.astral.sh/uv/guides/scripts/
[06]:https://docs.python.org/3/using/windows.html
[07]:https://numpy.org/doc/stable/
[08]:https://matplotlib.org/stable/
[09]:https://pyserial.readthedocs.io/
