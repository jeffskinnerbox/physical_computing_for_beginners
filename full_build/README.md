# Full Build: The Random Rover, Start to Finish
*Status: active course development — part of [Physical Computing for Beginners][01].*

The one-session build of the finished Random Rover — Classes 1-6 plus all three Class 6 stretch
goals (encoder speed control, rolling-history chart on the rover website, TFT status display) —
with ready-to-deploy Pico code, a laptop-side installer, calibration tools, and tests. The
[lesson scripts][02] build the rover one phase at a time over six classes; this folder is the
shortcut for building the finished robot directly, rebuilding a rover after the course, building a
second one, or recovering one that's been taken apart.

The main document is [`full-build-script.md`][03]: plan the breadboard, wire it, install the code
(sections 2-6), test it (section 7), then tune it (section 8), with a final checklist (section 9).
Section 8 is a self-contained calibration and tuning guide, adapted from the
[tuning and calibration explainer][04] and rewritten for this folder's files and tools — you don't
need the explainer open. This README only maps the folder and the commands; it doesn't repeat the
build steps.


## Table of Contents
- [Features][05]
- [Installation][06]
- [Usage][07]
- [Configuration][08]
- [Project Structure][09]
- [Testing][10]
- [Notes][11]


## Features

Everything here serves one goal: get a finished, tested, tuned rover onto the Pico with as little
hand-copying as possible, without clobbering your calibration or tuning.

- **The finished rover:** Class 5's stop-look-go collision-avoidance rover plus all three Class 6
    stretch goals running inside it, serving the rover status website at
    `http://192.168.4.1:5000` (port 5000, not 80, because CircuitPython's Web Workflow may hold
    port 80).
- **One-command deploy:** `deploy.py` installs the CircuitPython libraries with `circup` and copies
    every rover file onto `CIRCUITPY`, `code.py` last.
- **Protects your work:** never overwrites `settings.toml`; refuses to replace rover files you've
    changed on `CIRCUITPY` (your `MAG_OFFSET`, tuned constants) unless you add `--overwrite`, and
    then backs them up first to `backup/<date-time>/`.
- **Calibration/tuning tools:** compass calibration, servo-aim check, and motor stall-point/speed
    check, each run temporarily as `code.py` while your rover `code.py` is parked as
    `code_rover.py`.
- **Two-level testing:** an interactive part-by-part device test on the Pico, and an interactive
    whole-rover system test from the laptop (exit 0 = pass).
- **Live 3D viewer:** a WiFi variant of the Class 4 wireframe viewer that follows the finished
    rover's roll/pitch/yaw and compass heading.
- **Test-laptop bootstrap:** setup scripts that get a separate laptop ready straight from GitHub.


## Installation

Two parts: get this repo and the laptop tools onto a laptop, then get the rover software onto the
Pico.

**Prerequisites**

- Raspberry Pi Pico 2 W running CircuitPython **10.x** (9 or later is required for the TFT's
    `fourwire` module), wired per the wiring section of [`full-build-script.md`][03].
- [`uv`][12] and `git` on the laptop (Windows 11, Linux, or macOS) — the setup scripts install
    both if they're missing. Every laptop script carries PEP 723 inline dependencies
    (`# /// script`), so `uv` installs `circup`, `numpy`/`matplotlib`, or `pyserial` as needed —
    there's no project file to sync.
- Internet on the laptop for the first `deploy.py rover` (circup downloads libraries into `/lib`)
    and to pre-fetch the laptop tools' packages, because the rover's own WiFi network has no
    internet.
- Mu or Thonny for the serial console.

**Laptop.** On a laptop without the code yet (e.g., a separate test laptop), run the setup script
for its OS while it has internet. It installs `git` and `uv` if missing, clones this repo to
`~/physical_computing_for_beginners`, and pre-fetches the packages for `deploy.py`,
`test/system_test.py`, and `src/laptop/wireframe.py`. On Linux it also adds you to the `dialout`
group for the Pico's serial port (log out and back in once). Rerun it any time to pull updates;
it stops instead of overwriting files you've edited. These scripts are fetched by raw GitHub URL,
so don't move or rename them.

```bash
# Linux or macOS (Terminal)
curl -LsSf https://raw.githubusercontent.com/jeffskinnerbox/physical_computing_for_beginners/main/full_build/setup-test-laptop.sh | bash
```

```powershell
# Windows 11 (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://raw.githubusercontent.com/jeffskinnerbox/physical_computing_for_beginners/main/full_build/setup-test-laptop.ps1 | iex"
```

On a laptop that already has the repo, pre-fetch the laptop tools' packages yourself while you
still have internet:

```bash
uv sync --script src/laptop/wireframe.py
uv sync --script test/system_test.py
```

**Pico.** Run everything from this `full_build/` folder. **Keep the rover on its stand whenever
you deploy or save a file** — the moment `code.py` is saved, it starts driving.

```bash
# first install: libraries + every rover file (code.py copied last; pauses so you can edit settings.toml)
uv run deploy.py rover
uv run deploy.py rover --overwrite        # replace files you changed on CIRCUITPY (backs them up first)
uv run deploy.py --drive /media/$USER/CIRCUITPY rover   # if CIRCUITPY isn't found (macOS: /Volumes/CIRCUITPY)
```

On Windows (PowerShell), give the drive letter:

```powershell
uv run deploy.py --drive E:\ rover
```

`--drive` belongs to `deploy.py` itself, so it goes **before** the subcommand (`rover`, `tool`,
`test`, or `restore`).


## Usage

After the build: test, then calibrate and tune using section 8 of
[`full-build-script.md`][03], recording every change in a copy of
[`src/tuning-log-template.md`][13] (its rows follow the section 8 steps). The tools run on the
Pico, temporarily, as `code.py`:

```bash
# run a calibration/tuning tool as code.py (parks your rover code.py as code_rover.py)
uv run deploy.py tool mag_calibration     # also: servo_check, motor_check
uv run deploy.py restore                  # put your rover code.py back, tuned values and all
```

Watch the live rover from the laptop (join the rover's WiFi network first):

```bash
uv run src/laptop/wireframe.py            # 3D box follows roll/pitch/yaw, compass heading in the title
```

Or open `http://192.168.4.1:5000` in a browser for the rover website and its history chart.


## Configuration

The rover is configured through files on `CIRCUITPY`, not command-line options.

| File | Setting | Description |
| :--- | :------ | :---------- |
| `settings.toml` | `CIRCUITPY_WIFI_AP_SSID`, `CIRCUITPY_WIFI_AP_PASSWORD` | The rover's own WiFi network name and password (8+ characters). On a first install, `deploy.py` copies the template and waits while you edit it on `CIRCUITPY`; it never overwrites an existing one. |
| `rover_server.py` | `MAG_OFFSET` | Compass hard-iron calibration from `mag_calibration`. Paste it here in `src/pico/` as well as on `CIRCUITPY`, so a later `deploy.py rover --overwrite` keeps it. |
| `code.py` and the libraries it imports | `DRIVE_SPEED`, `TURN_SPEED`, `STOP_DISTANCE_CM`, `SCAN_ANGLES`, ... | Tuning constants. They start at the same placeholder values the Class 5 and Class 6 lesson scripts use; section 8 of the build script replaces them with values for your rover. |

Laptop-side options:

| Option | Default | Description |
| :----- | :------ | :---------- |
| `ROVER_REPO_DIR` (env var, setup scripts) | `~/physical_computing_for_beginners` | Where the setup script clones the repo (the `.sh` also takes the folder as an argument). |
| `deploy.py --drive PATH` | auto-detected | Path to `CIRCUITPY` if it isn't found automatically. |
| `system_test.py [PORT]` | auto-detected | Pico's serial port, e.g. `COM5`, `/dev/ttyACM0`, `/dev/cu.usbmodem...`. |
| `system_test.py --url URL` / `--show-log` | `http://192.168.4.1:5000` / off | Rover website address; also print every rover log line. |
| `wireframe.py [URL]` | `http://192.168.4.1:5000` | Rover website address. |

The laptop tools that talk to the rover's WiFi bypass system proxies and use request timeouts
longer than the rover's ~4 s scan+turn silence. On macOS, allow your terminal app under
**System Settings → Privacy & Security → Local Network**, or it can't reach the rover (see
[`full-build-script.md`][03]).


## Project Structure

```text
.
├── full-build-script.md        # THE doc: plan, parts, wiring, code, build, test, tune (section 8), checklist
├── setup-test-laptop.sh        # laptop (Linux/macOS): install git/uv, clone or pull this repo, pre-fetch laptop tools' packages
├── setup-test-laptop.ps1       # laptop (Windows 11): same, in PowerShell
├── deploy.py                   # laptop: copies libraries + rover code onto CIRCUITPY, runs tools/tests as code.py
├── src/
│   ├── tuning-log-template.md  # the tuning log, pre-filled with the starting values, in section 8's step order
│   ├── pico/                   # the rover itself (runs on the Pico)
│   │   ├── code.py             # full build: Class 5 stop-look-go rover + Class 6 stretch glue
│   │   ├── rover_server.py     # Class 5, unchanged: 9-DOF Mahony filter, compass heading, rover website
│   │   ├── motor_driver.py     # Class 3, unchanged: DRV8833 drive()/stop()
│   │   ├── wheel_odometry.py   # Class 3, unchanged: wheel speed/direction
│   │   ├── history_chart.py    # Class 6 Stretch 2, unchanged: rolling-history chart on the website
│   │   ├── speed_knob.py       # full build: Class 6 Stretch 1 as a library (encoder sets drive speed)
│   │   ├── tft_status.py       # full build: Class 6 Stretch 3 as a library (TFT shows distance/heading/speed)
│   │   ├── settings.toml       # template for the rover's WiFi network name + password
│   │   └── requirements.txt    # CircuitPython library list handed to circup
│   ├── tools/                  # one-off programs run temporarily as code.py
│   │   ├── mag_calibration.py  # Class 5 compass (hard-iron) calibration
│   │   ├── servo_check.py      # tuning Step 3: servo-aim check
│   │   └── motor_check.py      # tuning Step 5: motor stall points + speed runs
│   └── laptop/
│       └── wireframe.py        # Class 4 3D viewer reworked as a test tool: reads /data.json over WiFi
└── test/
    ├── device_test.py          # Pico: interactive part-by-part test (runs as code.py)
    └── system_test.py          # laptop: interactive whole-rover test (USB log + WiFi /data.json)
```

None of the subfolders has its own README; this file covers them all:

- **`src/pico/`** — everything that lives on `CIRCUITPY` to make the rover run. `deploy.py rover`
    copies these files (libraries first via `requirements.txt`, `code.py` last, `settings.toml` only
    if missing).
- **`src/tools/`** — Pico programs you run once in a while, not continuously: `deploy.py tool`
    swaps one in as `code.py`, and `deploy.py restore` swaps your rover back.
- **`src/laptop/`** — laptop-side Python. `wireframe.py` is the WiFi-reading variant of the class
    viewer in [`lesson_scripts/wireframe.py`][14] (which reads CSV over USB serial — the finished
    rover never prints CSV).
- **`test/`** — `device_test.py` runs on the Pico (via `deploy.py test`) using the same library
    files the rover drives with; `system_test.py` runs on the laptop against the real, unchanged
    rover `code.py`.

`deploy.py` also creates `backup/<date-time>/` here when `--overwrite` replaces files you changed on
`CIRCUITPY`; that folder is gitignored, as are the `*.bak` files.

**Where the code comes from — and the sync rule.** This folder sits downstream of
[`lesson_scripts/`][02]: it's the course's end state, not a new curriculum.

- **Verbatim from the lesson scripts:** `rover_server.py`, `motor_driver.py`, `wheel_odometry.py`,
    `history_chart.py`, `mag_calibration.py`, and the starting tuning values.
- **Full-build glue:** `code.py` (Class 5's `class-5-code.py` plus three hook points for the
    stretch goals), `speed_knob.py`, and `tft_status.py` (Class 6's standalone demos turned into
    libraries), plus the setup scripts, `deploy.py`, `wireframe.py`, and both tests.
- `servo_check.py` and `motor_check.py` come from Steps 3 and 5 of the
    [tuning and calibration explainer][04].

Code in `src/pico/` copied from the Class 5/6 lesson scripts must be kept in sync with those
scripts (and the Class 3 code likewise). When a lesson script's code changes, copy the change here,
and vice versa — for example, the `poll_website()` `BrokenPipeError` guard lives in both
`src/pico/code.py` and `class-5-code.py` in
[`class-05-lesson-script.md`][15].


## Testing

Test before you tune; both tests use wide ranges, so they pass the same way before and after
tuning. Pico-side code (everything in `src/pico/`, `src/tools/`, and `test/device_test.py`) can't
run on the laptop — it needs the board.

```bash
# 1. part by part, on the Pico: follow the prompts in Mu/Thonny's serial console
uv run deploy.py test
uv run deploy.py restore

# 2. whole rover, from the laptop: USB plugged in, battery switch on, laptop joined to the rover's WiFi,
#    Mu/Thonny's serial console CLOSED (only one program can hold the port)
uv run test/system_test.py                # or name the port: uv run test/system_test.py COM5

# 3. look at it: 3D box follows the rover's roll/pitch/yaw, compass heading in the title
uv run src/laptop/wireframe.py
```

`system_test.py` exits 0 when nothing failed, 1 otherwise. See section 7 of
[`full-build-script.md`][03] for the full test procedure and the first floor run.


## Notes

- Always boot the rover still and flat — importing `rover_server` calibrates the gyro and reads
    the compass at start-up.
- Keep the rover on its stand (wheels off the table) whenever you deploy or edit files on
    `CIRCUITPY`; see the safety notes in the root [README][01].
- Related: the root [README][01] for where this fits in the course, [`lesson_scripts/`][02] for
    the class-by-class version, [`explainers/`][16] for background, and [`CLAUDE.md`][17] for repo
    conventions.


[01]:../README.md
[02]:../lesson_scripts/README.md
[03]:full-build-script.md
[04]:../explainers/strategy-for-tuning-calibration-random-rover.md
[05]:#features
[06]:#installation
[07]:#usage
[08]:#configuration
[09]:#project-structure
[10]:#testing
[11]:#notes
[12]:https://docs.astral.sh/uv/
[13]:src/tuning-log-template.md
[14]:../lesson_scripts/wireframe.py
[15]:../lesson_scripts/class-05-lesson-script.md
[16]:../explainers/README.md
[17]:../CLAUDE.md
