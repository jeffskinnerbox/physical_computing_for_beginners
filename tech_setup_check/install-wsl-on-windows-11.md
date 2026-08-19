# Installing WSL (Windows Subsystem for Linux) on Windows 11

## Purpose

WSL lets you run a real Linux system side-by-side with Windows — no dual-boot, no separate
computer, no clunky virtual machine you have to babysit. Once this is set up, you'll have an
Ubuntu terminal you can open any time, right from your Windows 11 Start menu, with real Linux
tools like `bash`, `apt`, `python3`, and `git` — the same environment most servers, embedded
boards, and coding tutorials assume you already have.

This matters for physical computing work specifically: a lot of firmware tools, flashing
scripts, and board SDKs are written assuming a Linux (or Mac) shell. With WSL, you get that shell
without giving up Windows for everything else — you can still use your normal apps, browser, and
files, and just drop into Linux when a project needs it.

By the end of this guide you'll have Ubuntu running inside WSL, a Linux username and password
set up, and you'll have proven it works by running a real command against a real file.

## What gets installed

| Component | What it does | Why you need it | Instructions source | Official docs |
| ----------- | --------------- | ------------------ | ---------------------- | ---------------- |
| Windows Subsystem for Linux (WSL 2) | A Windows feature that runs a real Linux kernel alongside Windows | It's the engine that makes everything else possible | [learn.microsoft.com/windows/wsl/install](https://learn.microsoft.com/en-us/windows/wsl/install) | [learn.microsoft.com/windows/wsl/install](https://learn.microsoft.com/en-us/windows/wsl/install) |
| Ubuntu (Linux distribution) | A full Linux operating system that runs inside WSL | This is the actual Linux environment you'll type commands into | [learn.microsoft.com/windows/wsl/install](https://learn.microsoft.com/en-us/windows/wsl/install) | [ubuntu.com/wsl](https://ubuntu.com/desktop/wsl) |
| Windows Terminal | A modern terminal app for running command lines (PowerShell, WSL, etc.) in tabs | It's the easiest way to open and switch between your Ubuntu and PowerShell sessions | [learn.microsoft.com/windows/wsl/install](https://learn.microsoft.com/en-us/windows/wsl/install) | [learn.microsoft.com/windows/terminal](https://learn.microsoft.com/en-us/windows/terminal/install) |

## Target environment

- **Machine:** Windows 11 laptop (also works on Windows 10 version 2004/Build 19041 or later, but this guide assumes Windows 11).
- **Minimum hardware:** A 64-bit CPU with virtualization support (basically any laptop from the last ~10 years), at least a few GB of free disk space for the Linux filesystem.
- **Accounts / access needed:** Two paths are covered below —
  - **Path A — you have administrator rights** on this laptop (it's your personal machine, or you were given admin access).
  - **Path B — you don't have admin rights** (school-managed or work-managed laptop) — you'll need your school/work IT department to run one step for you.
- **Network:** Normal internet access — the install downloads the Linux kernel and the Ubuntu distribution from Microsoft/Canonical servers.
- **Before you start, you should already have:** Windows 11 fully updated (Settings → Windows Update → Check for updates), since older builds are missing pieces WSL needs.

## Installation

### Path A — On your own Windows 11 laptop (you have administrator rights)

This is the fast path: one command, one restart, and Ubuntu is ready to go. You'll run this from
an **administrator** PowerShell window, because installing a Windows feature (which is what WSL
is) requires elevated permissions — Windows won't let a regular, non-admin process turn features
on or off.

#### Install WSL and Ubuntu

1. Click **Start**, type `PowerShell`, right-click **Windows PowerShell**, and choose
   **Run as administrator**. Click **Yes** on the permission prompt.

```powershell
# This single command does four things for you:
#   1. Turns on the two Windows features WSL needs (Virtual Machine Platform + WSL itself)
#   2. Downloads and installs the Linux kernel that WSL runs on
#   3. Sets WSL 2 (the current, faster architecture) as the default
#   4. Downloads and installs Ubuntu, the default Linux distribution
wsl --install
```

1. When it finishes, restart your laptop — WSL needs a reboot to finish turning on the
   underlying Windows features, the same way installing a new graphics driver does.

```powershell
# Restarts Windows now. Save your work first!
Restart-Computer
```

1. After restarting, click **Start**, type `Ubuntu`, and open it. The first launch takes a
   minute or two while it finishes unpacking the Linux filesystem — every launch after this
   one takes under a second.

2. Ubuntu will ask you to create a **Linux username and password**. This is separate from your
   Windows login — pick anything you'll remember. Note: when you type the password, nothing
   appears on screen (no dots, no asterisks) — that's normal Linux terminal behavior, not a
   broken keyboard. Just type it and press Enter.

**Test it**

```bash
# Run this inside the Ubuntu window that opened.
# Confirms you're actually inside a Linux shell, not PowerShell.
lsb_release -a
# Expect output mentioning "Ubuntu" and a version number like 24.04

# Prove it's a real, working Linux environment by using it on real data:
# create a small text file, count its words, then read it back.
echo "hello from Ubuntu on WSL" > ~/wsl-test.txt
wc -w ~/wsl-test.txt
cat ~/wsl-test.txt
```

You should see `5 /home/<your-username>/wsl-test.txt` from `wc -w` (five words counted), and
your sentence printed back by `cat`.

**Clean up**

```bash
# Remove the test file — nothing about a real project should depend on it.
rm ~/wsl-test.txt
```

#### Check what you installed and keep it updated

```powershell
# Run this in PowerShell (not inside Ubuntu) to list every Linux distro installed
# and which WSL version (1 or 2) each one uses.
wsl --list --verbose

# Run this occasionally to pull the latest WSL engine updates from Microsoft
# (this updates WSL itself, separate from updating Ubuntu's own packages).
wsl --update
```

**Test it**

```powershell
# Confirms the wsl command-line tool itself is installed and reports its version.
wsl --version
```

**Clean up**

Nothing to clean up here — these are read-only checks.

---

### Path B — On a school-managed or work-managed Windows 11 laptop (no admin rights)

Skip this section if you already completed Path A. On a managed laptop, Windows blocks you from
turning on system features yourself — even the "Run as administrator" option may be greyed out,
or entering an admin password may be required and you won't have it. This is a deliberate IT
policy, not a bug, so the fix isn't a workaround — it's asking IT to run the same command Path A
used, but from their side.

#### Step 1: Ask IT to enable WSL

Send your school/work IT department this exact request — it's the same single command from
Path A, just run under their administrator account instead of yours:

```powershell
# What you're asking IT to run, on your laptop, from an administrator PowerShell:
wsl --install
```

If your IT department prefers to enable things individually rather than running `wsl --install`
directly (some managed-device policies do), the equivalent two Windows features are:

```powershell
# Turns on the WSL engine itself
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# Turns on the Virtual Machine Platform, which WSL 2 needs to run its Linux kernel
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

A restart is required after either approach — ask IT to restart the laptop, or do it yourself
once they confirm the features are on.

#### Step 2: Confirm virtualization is allowed

Managed laptops sometimes have virtualization itself locked in the BIOS/firmware, separately
from the Windows feature above. If step 1 finishes but Ubuntu won't launch (see the error check
below), this is usually why — and only IT can unlock BIOS settings on a managed device.

```powershell
# Run this yourself, no admin needed — it just reads current CPU/virtualization status.
# Look for "Virtualization: Yes" and "Hyper-V - VM Monitor Mode Extensions: Yes" in the output.
systeminfo | findstr /i "hyper-v virtualization"
```

If either says "No," ask IT specifically to enable virtualization (Intel VT-x / AMD-V) in the
BIOS — this is a firmware setting they'll need to change, not something fixable from Windows.

#### Step 3: Finish install and set up Ubuntu

Once IT confirms the features are enabled and the laptop has restarted, continue exactly like
Path A from the point Ubuntu is installed:

1. Click **Start**, type `Ubuntu`, open it.
2. Create your Linux username and password when prompted (remember: the password won't show
   characters as you type — that's normal).

**Test it**

```bash
# Same verification as Path A — confirms Ubuntu is really running and usable.
lsb_release -a
echo "hello from Ubuntu on WSL" > ~/wsl-test.txt
wc -w ~/wsl-test.txt
cat ~/wsl-test.txt
```

**Clean up**

```bash
rm ~/wsl-test.txt
```

---

### Both paths — Confirm Windows Terminal is set up (recommended)

Windows Terminal gives you tabs, so you can have PowerShell and Ubuntu open side-by-side instead
of juggling separate windows. Most current Windows 11 laptops already have it preinstalled as
the default terminal app — the command below just makes sure you have it and grabs any update.

```powershell
# Installs (or updates) Windows Terminal via winget, Windows' built-in package manager.
# If it's already installed, this just confirms that and exits — nothing breaks either way.
winget install --id Microsoft.WindowsTerminal -e
```

**Test it**

```powershell
# Opens Windows Terminal — you should see a new window with a tab bar at the top.
wt
```

Click the **v** dropdown next to the `+` tab button — you should now see "Ubuntu" listed as an
option alongside "Windows PowerShell" and "Command Prompt."

**Clean up**

Nothing to clean up — Windows Terminal is meant to stay installed.

## Troubleshooting: virtualization / installation errors

If `wsl --install` (or launching Ubuntu afterward) fails with an error like
`Error 0x80370102` or a message about virtualization or Hyper-V:

```powershell
# Checks whether Windows' boot configuration has virtualization support turned off.
bcdedit /enum | findstr -i hypervisorlaunchtype

# If that showed "Off", this turns it back on (requires admin PowerShell):
bcdedit /set hypervisorlaunchtype Auto
```

Then restart and try `wsl --install` again. If it still fails, virtualization is most likely
disabled in your laptop's BIOS/firmware — on your own laptop (Path A) you can usually enable it
yourself by restarting and pressing the manufacturer's BIOS key (commonly `F2`, `F10`, or `Del`
right at boot) and turning on **Intel VT-x** or **AMD-V/SVM Mode**. On a managed laptop (Path B),
this step has to be done by IT.
