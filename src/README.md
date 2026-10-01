# README

Laptop-side code and rover tuning material — things that run on (or get filled in on) the
student's computer, not on the Pico. There's no project at this level: each subdirectory stands
alone. Pico-side CircuitPython lives inline in the [lesson scripts][01], and the finished rover's
deployable code lives in [`full_build/`][02].


## Contents

```text
.
├── wireframe/                  # uv project (Python 3.14) for wireframe.py, the Class 4 live 3D orientation viewer
├── rover/
│   ├── tuning-log-template.md  # Random Rover tuning log, prefilled with steps/parameters/starting values
│   ├── before_tuning/          # empty so far
│   └── after_tuning/           # empty so far
└── tuning_tools/               # empty so far
```


## Purpose / Role in Repository

- [`wireframe/`][03] holds the class copy of `wireframe.py` (reads roll/pitch/yaw CSV over USB
    serial); its canonical copy is embedded in the Class 4 lesson script, so keep the two in sync.
    Students download it via `tech_setup_check/install-wireframe-on-windows-11.md`. The
    WiFi-reading variant for the finished rover is `full_build/src/laptop/wireframe.py`.
- `rover/tuning-log-template.md` is the log used with
    [Strategy for Tuning and Calibrating the Random Rover][04]: add one row each time you change a
    tuning number.

See the root [README][05] for the course map.


[01]:../lesson_scripts/README.md
[02]:../full_build/README.md
[03]:wireframe/README.md
[04]:../explainers/strategy-for-tuning-calibration-random-rover.md
[05]:../README.md
