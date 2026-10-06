# README

Everything a student needs to get a Windows 11 laptop ready for CircuitPython development before
Pre-Class, plus the laptop-side setup for Class 4's 3D viewer, and a few hand-maintained notes and
helpers for topics that come up along the way (git worktrees, Python virtual environments, SSH
keys, GitHub repo setup). The student guides are Windows 11 only — there are no Linux/macOS
student guides yet.


## Contents

```text
.
├── check-for-windows-11-and-wsl.md                 # short checklist: confirm Windows 11, virtualization support, and WSL readiness
├── install-wsl-on-windows-11.md                    # generated guide: WSL + Ubuntu install walkthrough, with troubleshooting
├── install-python-on-windows-11.md                 # generated guide: Python 3 for Windows 11 (laptop-side programs from Class 4)
├── install-circuitpython-dev-env-on-windows-11.md  # generated guide: CircuitPython firmware, Mu + Thonny, libraries, board check
├── install-wireframe-on-windows-11.md              # generated guide: install uv, download + run the Class 4 wireframe.py
├── python-virtual-environments.md                  # hand-maintained notes (work in progress): git with CircuitPython, circup, uv/pyenv venvs
├── git-worktree-multitasking.md                    # hand-maintained notes: links + overview and walkthrough of `git worktree`
├── set-up-ssh-key-authentication.md                # hand-maintained: single link to an SSH key setup guide
└── setup-github.sh                                 # hand-maintained interactive script: init local git repo + optional GitHub repo via `gh`
```

Student guides, in order: [check for Windows 11 + WSL][01], [install WSL][02],
[install Python][03], [CircuitPython dev environment][04], and (before Class 4)
[install and run wireframe.py][05]. Notes and helpers: [Python virtual environments][06],
[git worktrees][07], [SSH key authentication][08], [`setup-github.sh`][09].


## Purpose / Role in Repository

This is the `/teen-install-instructions` output location per the root [README][10]'s generation
table — the guides a student works through before Pre-Class so class time goes to building, not
troubleshooting a broken toolchain. Not everything here came from that skill:

- **Generated guides** (`/teen-install-instructions`): `install-wsl-on-windows-11.md`,
    `install-python-on-windows-11.md`, `install-circuitpython-dev-env-on-windows-11.md`, and
    `install-wireframe-on-windows-11.md`. Regenerate these with the skill rather than hand-editing.
- **Hand-maintained**: `python-virtual-environments.md`, `git-worktree-multitasking.md`,
    `set-up-ssh-key-authentication.md`, and `setup-github.sh` — reference notes and helpers, not
    skill output. `check-for-windows-11-and-wsl.md` is a short standalone checklist.

`install-wireframe-on-windows-11.md` downloads the class version of `wireframe.py` from
[`lesson_scripts/wireframe.py`][11] by GitHub URL — the Class 4 viewer that reads roll/pitch/yaw
over USB serial. The finished-rover variant in [`full_build/src/laptop/wireframe.py`][12] (reads
the rover website over WiFi) is a full-build test tool and isn't covered by these guides; the
full build has its own laptop setup scripts, described in the [`full_build/` README][13].


## Usage

Work through the student guides in order before Pre-Class: confirm Windows 11 + WSL capability,
install WSL if needed, install Python, then set up the CircuitPython dev environment. Do the
wireframe guide before Class 4. Pre-Class itself then continues in the
[Pre-Class lesson script][14].

`setup-github.sh` is a standalone helper, not part of that sequence. It works on the current
directory, so `cd` into the folder you want turned into a git repo and call the script by its path:

```bash
cd /path/to/your/project
/path/to/tech_setup_check/setup-github.sh            # interactive; confirms a summary before acting
/path/to/tech_setup_check/setup-github.sh --dry-run  # prompts + summary only, changes nothing (also -n; -h for help)
```

It detects existing git/GitHub state and only acts on what you confirm, so it's safe to run more
than once.


## Notes

- `python-virtual-environments.md` is unfinished scratch notes (it still has a "FINISH THIS"
    marker) — don't hand it to students as a guide.
- Don't move or rename `lesson_scripts/wireframe.py` without updating the download URL in
    `install-wireframe-on-windows-11.md`.
- Related: root [README][10] for the course map and generation pipeline,
    [`lesson_scripts/`][15] for the class walkthroughs these guides prepare for, and
    [`CLAUDE.md`][16] for repo conventions.


[01]:check-for-windows-11-and-wsl.md
[02]:install-wsl-on-windows-11.md
[03]:install-python-on-windows-11.md
[04]:install-circuitpython-dev-env-on-windows-11.md
[05]:install-wireframe-on-windows-11.md
[06]:python-virtual-environments.md
[07]:git-worktree-multitasking.md
[08]:set-up-ssh-key-authentication.md
[09]:setup-github.sh
[10]:../README.md
[11]:../lesson_scripts/wireframe.py
[12]:../full_build/src/laptop/wireframe.py
[13]:../full_build/README.md
[14]:../lesson_scripts/class-00-lesson-script.md
[15]:../lesson_scripts/README.md
[16]:../CLAUDE.md
