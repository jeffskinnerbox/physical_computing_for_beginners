# README

Everything a student needs to get a Windows 11 laptop ready for CircuitPython development before
Pre-Class, plus the laptop-side setup for Class 4's 3D viewer, and a few hand-maintained notes and
helpers for topics that come up along the way (git worktrees, Python virtual environments, SSH
keys, GitHub repo setup).


## Contents

```text
.
├── check-for-windows-11-and-wsl.md               # short checklist: confirm Windows 11, virtualization support, and WSL
├── install-wsl-on-windows-11.md                  # generated guide: WSL + Ubuntu install walkthrough
├── install-python-on-windows-11.md               # generated guide: Python 3 for Windows 11 (laptop-side programs from Class 4)
├── install-circuitpython-dev-env-on-windows-11.md  # generated guide: CircuitPython dev environment (editor, firmware, libraries, board)
├── install-wireframe-on-windows-11.md            # generated guide: install uv, download + run Class 4 wireframe.py
├── python-virtual-environments.md                # hand-maintained notes (work in progress): git with CircuitPython, circup, uv/pyenv venvs
├── git-worktree-multitasking.md                  # hand-maintained notes: links + overview of `git worktree`
├── set-up-ssh-key-authentication.md              # hand-maintained: single link to an SSH key setup guide
└── setup-github.sh                               # hand-maintained interactive script: init local git repo + optional GitHub repo via `gh`
```


## Purpose / Role in Repository

This is the `/teen-install-instructions` output location per the root [README][01]'s generation
table — the install guides a student works through before Pre-Class so class time goes to
building, not troubleshooting a broken toolchain. Not everything here came from that skill:

- **Generated guides** (`/teen-install-instructions`): `install-wsl-on-windows-11.md`,
    `install-python-on-windows-11.md`, `install-circuitpython-dev-env-on-windows-11.md`, and
    `install-wireframe-on-windows-11.md`. Regenerate these with the skill rather than hand-editing.
- **Hand-maintained**: `python-virtual-environments.md`, `git-worktree-multitasking.md`,
    `set-up-ssh-key-authentication.md`, and `setup-github.sh` — reference notes and helpers, not
    skill output. `check-for-windows-11-and-wsl.md` is a short standalone checklist.

`install-wireframe-on-windows-11.md` downloads the class version of `wireframe.py` from
[`src/wireframe/`][02] — the Class 4 viewer that reads roll/pitch/yaw over USB serial. The
finished-rover variant in [`full_build/src/laptop/wireframe.py`][03] (reads the rover website over
WiFi) is a full-build test tool and isn't covered by these guides; see [`full_build/`][04].


## Usage

Work through these roughly in order before Pre-Class: confirm Windows 11 + WSL capability, install
WSL if needed, install Python, then set up the CircuitPython dev environment. Do the wireframe
guide before Class 4.

`setup-github.sh` is a standalone helper, not part of that sequence — run it from whatever
directory you want turned into a git repo:

```bash
./setup-github.sh            # interactive; confirms a summary before acting
./setup-github.sh --dry-run  # prompts + summary only, changes nothing
```

It detects existing git/GitHub state and only acts on what you confirm, so it's safe to run more
than once.


## Notes

- `python-virtual-environments.md` is unfinished scratch notes (it still has "FINISH THIS"
    markers) — don't hand it to students as a guide.
- See the root [README][01] for how install instructions fit into the course's overall generation
    pipeline, and [`CLAUDE.md`][05] for repo conventions.


[01]:../README.md
[02]:../src/wireframe/README.md
[03]:../full_build/src/laptop/wireframe.py
[04]:../full_build/README.md
[05]:../CLAUDE.md
