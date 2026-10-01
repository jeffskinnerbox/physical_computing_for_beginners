# README

Laptop-side Python for Physical Computing for Beginners: `wireframe.py`, the Class 4 live 3D
orientation viewer, which runs on the student's computer, not on the Pico. Everything Pico-side is
CircuitPython embedded in the lesson scripts; this directory is a small `uv` project (Python 3.14)
for the one program that needs a desktop Python instead.


## Contents

```text
.
├── wireframe.py      # Class 4 live 3D orientation viewer (reads roll,pitch,yaw CSV over USB serial)
├── main.py           # `uv init` stub, unused
├── pyproject.toml    # project metadata; declares numpy, matplotlib, pyserial
├── uv.lock           # locked dependency versions
└── .python-version   # pins Python 3.14 for uv
```


## Purpose / Role in Repository

`wireframe.py` is Class 4 Phase 2's `class-4-phase-2-wireframe.py`. Its canonical copy lives
embedded in [`lesson_scripts/class-04-lesson-script.md`][01] (and the Class 4 lesson plan) — when
you change one, change the other so they stay identical. It draws the orientation streamed by the
Pico running `class-4-phase-1-code.py` or `class-4-phase-3-code.py`.

Students don't clone this directory; they download `wireframe.py` and run it by following
[Install and Run wireframe.py on a Windows 11 Laptop][02].

A separate variant, [`full_build/src/laptop/wireframe.py`][03], is a test tool for the finished
rover: it reads the rover website's `/data.json` over WiFi instead of CSV over USB (the finished
rover never prints CSV). It isn't part of this project; see [`full_build/`][04]. See
[`src/`][05] for the rest of the laptop-side folders.


## Installation

Nothing to install beyond [`uv`][06]. `wireframe.py` carries PEP 723 inline dependencies (the
`# /// script` block: numpy, matplotlib, pyserial), so `uv` fetches what it needs on first run
(internet needed once).


## Usage

It finds the Pico's serial port by itself (USB vendor ID of an Adafruit/CircuitPython or Raspberry
Pi board); pass a port only if it picks the wrong board.

```bash
cd src/wireframe
uv run wireframe.py               # auto-detect the Pico
uv run wireframe.py /dev/ttyACM0  # or name the port (COM5 on Windows)
```

Close Mu/Thonny first — only one program can hold the serial port.


## Testing

No automated tests. Lint with ruff:

```bash
cd src/wireframe
uv run ruff check                 # or one file: uv run ruff check wireframe.py
```


## Notes

- `flask` and `ruff` are installed in `.venv` but not declared in `pyproject.toml`, so `uv sync`
    removes them. Add new dependencies with `uv add <package>`, not `uv pip install`.
- Pico-side CircuitPython can't run here — it needs the board.
- See the root [README][07] for the course map and [`CLAUDE.md`][08] for repo conventions.


[01]:../../lesson_scripts/class-04-lesson-script.md
[02]:../../tech_setup_check/install-wireframe-on-windows-11.md
[03]:../../full_build/src/laptop/wireframe.py
[04]:../../full_build/README.md
[05]:../README.md
[06]:https://docs.astral.sh/uv/
[07]:../../README.md
[08]:../../CLAUDE.md
