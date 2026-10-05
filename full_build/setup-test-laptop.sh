#!/usr/bin/env bash
# setup-test-laptop.sh -- full build: get (or update) the course code on a Linux test laptop,
# then pre-install every laptop script's Python packages so they run on the rover's
# internet-less WiFi later. Safe to run again: the second time it just pulls the latest code.
#
# First time (nothing cloned yet):
#   curl -LsSf https://raw.githubusercontent.com/jeffskinnerbox/physical_computing_for_beginners/main/full_build/setup-test-laptop.sh | bash
# After that:
#   ~/physical_computing_for_beginners/full_build/setup-test-laptop.sh
#
# Clone somewhere else: pass the folder as an argument, or set ROVER_REPO_DIR.

set -euo pipefail

REPO_URL="https://github.com/jeffskinnerbox/physical_computing_for_beginners.git"
DEST="${1:-${ROVER_REPO_DIR:-$HOME/physical_computing_for_beginners}}"
LAPTOP_SCRIPTS=(deploy.py test/system_test.py src/laptop/wireframe.py)

step() { printf '\n==> %s\n' "$*"; }

step "Checking for git"
if ! command -v git >/dev/null 2>&1; then
    if command -v apt-get >/dev/null 2>&1; then
        sudo apt-get update && sudo apt-get install -y git
    else
        echo "git isn't installed and this isn't an apt system -- install git, then rerun." >&2
        exit 1
    fi
fi
git --version

step "Checking for uv"
if ! command -v uv >/dev/null 2>&1; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"  # the installer's PATH change only reaches new shells
else
    uv self update >/dev/null 2>&1 || true  # needs uv 0.6+ for `uv sync --script`; skip if uv came from a package manager
fi
uv --version

step "Getting the code into $DEST"
if [ -d "$DEST/.git" ]; then
    if ! git -C "$DEST" pull --ff-only; then
        echo "Pull failed -- probably a file you edited here. See it with: git -C \"$DEST\" status" >&2
        exit 1
    fi
else
    git clone "$REPO_URL" "$DEST"
fi
git -C "$DEST" log --oneline -1

step "Pre-installing the laptop scripts' Python packages"
cd "$DEST/full_build"
for script in "${LAPTOP_SCRIPTS[@]}"; do
    echo "  $script"
    uv sync --quiet --script "$script"
done

step "Checking serial-port access (needed by system_test.py)"
if id -nG "$USER" | grep -qw dialout; then
    echo "  $USER is in the dialout group"
else
    sudo usermod -aG dialout "$USER"
    echo "  Added $USER to dialout -- log out and back in before using the Pico's serial port."
fi

cat <<EOF

Done. Next, with the rover on its stand and the Pico plugged in by USB:
  cd "$DEST/full_build"
  uv run deploy.py rover          # first time needs internet: circup downloads the Pico libraries
  uv run deploy.py test           # device test runs on the Pico; watch it in the serial console
  uv run deploy.py restore        # put the rover code.py back
  uv run test/system_test.py      # whole-rover test over USB serial
  uv run src/laptop/wireframe.py  # 3D view -- join the rover's WiFi first
EOF
