# README

Laptop-side Python helpers for Physical Computing for Beginners: code that runs on the student's
computer, not on the Pico. Everything Pico-side is CircuitPython embedded in the lesson scripts;
this directory is a small `uv` project (Python 3.14) for the few programs that need a desktop
Python instead.


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


## Usage

`wireframe.py` carries PEP 723 inline dependencies (the `# /// script` block), so `uv` installs
what it needs on first run. It finds the Pico's serial port by itself; pass a port only if it picks
the wrong board.

```bash
cd src/wireframe
uv run wireframe.py               # auto-detect the Pico
uv run wireframe.py /dev/ttyACM0  # or name the port (COM5 on Windows)
uv run ruff check                 # lint (or: uv run ruff check wireframe.py)
```

Close Mu/Thonny first — only one program can hold the serial port.


## Notes

- `flask` and `ruff` are installed in `.venv` but not declared in `pyproject.toml`, so `uv sync`
    removes them. Add new dependencies with `uv add <package>`, not `uv pip install`.
- Pico-side CircuitPython can't run here — it needs the board.
- See the root [README][03] for the course map and `CLAUDE.md` for repo conventions.


[01]:../lesson_scripts/class-04-lesson-script.md
[02]:../tech_setup_check/install-wireframe-on-windows-11.md
[03]:../README.md
