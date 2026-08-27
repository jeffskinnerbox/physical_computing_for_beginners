
# README

Everything a student needs to get a Windows 11 laptop ready for CircuitPython development before
Pre-Class, plus a few reference links for topics that come up along the way (WSL, SSH, Python
virtual environments, git worktrees). Some files here are full step-by-step guides; others are
just a bookmark to an external source, kept for whoever's setting up a laptop to find quickly.


## Contents

```text
.
├── check-for-windows-11-and-wsl.md                  # confirm the laptop is Windows 11 and WSL-capable
├── install-wsl-on-windows-11.md                     # full WSL install walkthrough
├── install-python-on-windows-11-and-linux.md         # link out to a Python install guide
├── install-circuitpython-dev-env-on-windows-11.md    # full CircuitPython dev environment setup (editor, libraries, board)
├── python-virtual-environments.md                    # venv reference notes
├── set-up-ssh-key-authentication.md                  # link out to an SSH key setup guide
├── git-worktree-multitasking.md                      # link out to git worktree reference material
└── setup-github.sh                                    # interactive script: init local git repo + optional GitHub repo via `gh`
```


## Purpose / Role in Repository

This is the `/teen-install-instructions`-generated output location per the root [README][01]'s
generation table — the install guides a student works through before
Pre-Class so class time goes to building, not troubleshooting a broken toolchain. The two fuller
guides (`install-wsl-on-windows-11.md`, `install-circuitpython-dev-env-on-windows-11.md`) are the
actual generated walkthroughs; the shorter files are reference links kept alongside them for
convenience rather than full guides in their own right.


## Usage

Work through these roughly in order: confirm Windows 11 + WSL capability, install WSL if needed,
install Python, then set up the CircuitPython dev environment. `setup-github.sh` is a standalone
helper, not part of that sequence — run it from whatever directory you want turned into a git repo:

```bash
./setup-github.sh
```

It detects existing git/GitHub state and only acts on what you confirm, so it's safe to run more
than once.


## Notes

- `install-python-on-windows-11-and-linux.md`, `set-up-ssh-key-authentication.md`, and
  `git-worktree-multitasking.md` are single external links, not full guides — treat them as
  bookmarks, not as `/teen-install-instructions` output.
- See the root [README][01] for how install instructions fit into the course's overall generation
  pipeline.


[01]:../README.md
</content>
