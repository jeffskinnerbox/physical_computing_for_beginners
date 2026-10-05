# README

The one-session build of the finished Random Rover — Classes 1-6 plus all three Class 6 stretch
goals — with ready-to-deploy Pico code, a laptop-side installer, calibration tools, and tests. The
lesson scripts build the rover one phase at a time over six classes; this folder is the shortcut
for rebuilding a rover after the course, building a second one, or recovering one that's been
taken apart. The main document is [`full-build-script.md`][01] — this README only maps the folder
and the commands; it doesn't repeat the build steps.


## Contents

```text
.
├── full-build-script.md        # THE doc: plan, parts, wiring, code overview, build, test, tune, checklist
├── deploy.py                   # laptop: copies libraries + rover code onto CIRCUITPY, runs tools/tests as code.py
├── src/
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
│   │   ├── servo_check.py      # tuning guide Step 3: servo-aim check
│   │   └── motor_check.py      # tuning guide Step 5: motor stall points + speed runs
│   └── laptop/
│       └── wireframe.py        # Class 4 3D viewer reworked as a test tool: reads /data.json over WiFi
└── test/
    ├── device_test.py          # Pico: interactive part-by-part test (runs as code.py)
    └── system_test.py          # laptop: interactive whole-rover test (USB log + WiFi /data.json)
```

`deploy.py` also creates `backup/<date-time>/` here when `--overwrite` replaces files you changed
on `CIRCUITPY`; that folder is gitignored, as are the `*.bak` files.


## Purpose / Role in Repository

This folder sits downstream of [`lesson_scripts/`][02]: it's the course's end state, not a new
curriculum. See the root [README][03] for where it fits in the course.

- **Verbatim from the lesson scripts:** `rover_server.py`, `motor_driver.py`, `wheel_odometry.py`,
    `history_chart.py`, `mag_calibration.py`, and the starting tuning values. When the Class 3, 5,
    or 6 lesson script changes that code, copy the change here too.
- **Full-build glue:** `code.py` (Class 5's `class-5-code.py` plus three hook points for the
    stretch goals), `speed_knob.py`, and `tft_status.py` (Class 6's standalone demos turned into
    libraries), plus `deploy.py`, `wireframe.py`, and both tests. These have no lesson-script
    original to sync against beyond the Class 5/6 code they extend.
- `servo_check.py` and `motor_check.py` come from the
    [Strategy for Tuning and Calibrating the Random Rover][04] explainer, which is the next stop
    after the build.

The class version of the 3D viewer (reads CSV over USB serial) lives in [`lesson_scripts/wireframe.py`][05];
`src/laptop/wireframe.py` here is the WiFi-reading variant for the finished rover, which never
prints CSV.


## Prerequisites

- Raspberry Pi Pico 2 W running CircuitPython **10.x** (9 or later is required for the TFT's
    `fourwire` module), wired per the wiring table in [`full-build-script.md`][01].
- [`uv`][06] on the laptop (Windows 11, Linux, or macOS). Every laptop script carries PEP 723
    inline dependencies (`# /// script`), so `uv` installs `circup`, `numpy`/`matplotlib`, or
    `pyserial` as needed — there's no project file to sync.
- Internet on the laptop for the first `deploy.py rover` (circup downloads libraries into `/lib`)
    and to pre-fetch the laptop tools' packages, because the rover's own WiFi network has no
    internet.
- Mu or Thonny for the serial console.


## Usage

Run everything from this `full_build/` folder. **Keep the rover on its stand whenever you deploy or
save a file** — the moment `code.py` is saved, it starts driving.

```bash
# first install: libraries + every rover file (code.py copied last; pauses so you can edit settings.toml)
uv run deploy.py rover
uv run deploy.py rover --overwrite        # replace files you changed on CIRCUITPY (backs them up first)
uv run deploy.py --drive E:\ rover        # if CIRCUITPY isn't found (Linux: --drive /media/you/CIRCUITPY)

# pre-fetch the laptop tools' packages while you still have internet
uv sync --script src/laptop/wireframe.py
uv sync --script test/system_test.py

# run a calibration/tuning tool as code.py (parks your rover code.py as code_rover.py)
uv run deploy.py tool mag_calibration     # also: servo_check, motor_check
uv run deploy.py restore                  # put your rover code.py back, tuned values and all
```

On a first install, `deploy.py` copies the `settings.toml` template and waits while you change the
network name and password on `CIRCUITPY` to your own. It never overwrites an existing
`settings.toml`.


## Testing

Test before you tune; both tests use wide ranges, so they pass the same way before and after
tuning. Pico-side code (everything in `src/pico/`, `src/tools/`, and `test/device_test.py`) can't
run on the laptop — it needs the board.

```bash
# 1. part by part, on the Pico: follow the prompts in Mu/Thonny's serial console
uv run deploy.py test
uv run deploy.py restore

# 2. whole rover, from the laptop: USB plugged in, laptop joined to the rover's WiFi,
#    Mu/Thonny's serial console CLOSED (only one program can hold the port)
uv run test/system_test.py                # or name the port: uv run test/system_test.py COM5

# 3. look at it: 3D box follows the rover's roll/pitch/yaw, compass heading in the title
uv run src/laptop/wireframe.py
```

`system_test.py` exits 0 when nothing failed, 1 otherwise. See section 7 of
[`full-build-script.md`][01] for the full test procedure and the first floor run.


## Notes

- Always boot the rover still and flat — importing `rover_server` calibrates the gyro and reads
    the compass at start-up.
- After compass calibration, paste the `MAG_OFFSET` line into `src/pico/rover_server.py` here as
    well as on `CIRCUITPY`, so a later `deploy.py rover --overwrite` keeps it.
- No separate READMEs live in `src/` or `test/` subfolders; this file covers them all.
- See [`CLAUDE.md`][07] for repo conventions (the rover website runs on port 5000, not 80).


[01]:full-build-script.md
[02]:../lesson_scripts/README.md
[03]:../README.md
[04]:../explainers/strategy-for-tuning-calibration-random-rover.md
[05]:../lesson_scripts/wireframe.py
[06]:https://docs.astral.sh/uv/
[07]:../CLAUDE.md
