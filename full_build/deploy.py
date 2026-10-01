#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["circup"]
# ///
# deploy.py -- full build: copies the rover's software onto the Pico's CIRCUITPY drive.
# Runs on your LAPTOP (Windows 11, Linux, or macOS), from the full_build/ folder:
#
#   uv run deploy.py rover              install libraries + the whole rover (first time)
#   uv run deploy.py tool mag_calibration   run a tool as code.py (also: servo_check, motor_check)
#   uv run deploy.py test               run test/device_test.py as code.py
#   uv run deploy.py restore            put your rover code.py back after a tool or test
#
# Add --drive E:\ (Windows) or --drive /media/you/CIRCUITPY if the drive isn't found.
#
# It protects your work:
#   * settings.toml is copied only if CIRCUITPY doesn't have one yet.
#   * `rover` won't overwrite a file you've changed on CIRCUITPY (your MAG_OFFSET,
#     your tuned constants) unless you add --overwrite -- and even then it backs
#     the old file up to full_build/backup/<date-time>/ first.
#   * `tool` and `test` park your rover code.py on CIRCUITPY as code_rover.py (never
#     overwriting one already parked); `restore` puts it back, tuned values and all.

import argparse
import datetime
import filecmp
import os
import platform
import shutil
import string
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PICO_SRC = HERE / "src" / "pico"
TOOLS_SRC = HERE / "src" / "tools"
TEST_SRC = HERE / "test"
PARKED = "code_rover.py"  # where tool/test park the rover's code.py
ROVER_MARKER = "# code.py -- full build: the finished Random Rover"  # first line of the rover's code.py

# Rover files in copy order -- code.py LAST, because saving code.py restarts the Pico.
ROVER_FILES = [
    "motor_driver.py",
    "wheel_odometry.py",
    "rover_server.py",
    "history_chart.py",
    "speed_knob.py",
    "tft_status.py",
    "code.py",
]


def find_circuitpy():
    """Return the CIRCUITPY drive's path, or None."""
    system = platform.system()
    if system == "Windows":
        import ctypes

        for letter in string.ascii_uppercase:
            root = f"{letter}:\\"
            if not os.path.exists(root):
                continue
            label = ctypes.create_unicode_buffer(261)
            ok = ctypes.windll.kernel32.GetVolumeInformationW(
                root, label, len(label), None, None, None, None, 0
            )
            if ok and label.value == "CIRCUITPY":
                return Path(root)
        return None
    user = os.environ.get("USER", "")
    candidates = [Path("/Volumes/CIRCUITPY")] if system == "Darwin" else [
        Path("/media") / user / "CIRCUITPY",
        Path("/run/media") / user / "CIRCUITPY",
        Path("/media/CIRCUITPY"),
    ]
    return next((c for c in candidates if c.is_dir()), None)


def is_rover_code(path):
    return path.exists() and path.read_text(errors="ignore").startswith(ROVER_MARKER)


def install_libraries(drive):
    print("Installing CircuitPython libraries into", drive / "lib", "(needs internet)...")
    subprocess.run(
        # circup has no `python -m circup` entry point, so call its main() directly.
        [sys.executable, "-c", "import sys; from circup import main; sys.argv[0] = 'circup'; sys.exit(main())",
         "--path", str(drive), "install",
         "-r", str(PICO_SRC / "requirements.txt")],
        check=True,
    )


def deploy_rover(drive, overwrite):
    changed = [name for name in ROVER_FILES
               if (drive / name).exists() and not filecmp.cmp(PICO_SRC / name, drive / name, shallow=False)]
    if changed and not overwrite and (drive / PARKED).exists():
        sys.exit("A tool or test is running as code.py. Run `uv run deploy.py restore` first.")
    if changed and not overwrite:
        print("These files on CIRCUITPY differ from full_build/src/pico -- probably your")
        print("calibration or tuning. Nothing was copied:")
        for name in changed:
            print("   ", name)
        print("Run again with --overwrite to replace them (the old ones get backed up first).")
        sys.exit(1)
    if changed:
        backup = HERE / "backup" / datetime.datetime.now().astimezone().strftime("%Y-%m-%d_%H-%M-%S")
        backup.mkdir(parents=True)
        for name in changed:
            shutil.copy2(drive / name, backup / name)
        print("Backed up your changed files to", backup)
    if (drive / PARKED).exists():
        (drive / PARKED).unlink()  # a fresh rover replaces any parked one
        print("Removed the old", PARKED)
    install_libraries(drive)
    if not (drive / "settings.toml").exists():
        shutil.copy2(PICO_SRC / "settings.toml", drive / "settings.toml")
        print("Copied settings.toml. Before the rover starts, EDIT IT on CIRCUITPY: pick your own")
        print("network name (nobody else's) and a password of at least 8 characters.")
        input("Save settings.toml, then press Enter to finish installing... ")
    else:
        print("Kept your existing settings.toml.")
    for name in ROVER_FILES:
        shutil.copy2(PICO_SRC / name, drive / name)
        print("Copied", name)
    print("Done. Put the rover on its stand -- it starts driving as soon as code.py runs.")


def park_rover_code(drive):
    """Move the rover's code.py aside so a tool or test can run as code.py."""
    code = drive / "code.py"
    if (drive / PARKED).exists():
        print(f"Your rover is already parked as {PARKED} -- leaving it alone.")
    elif is_rover_code(code):
        shutil.copy2(code, drive / PARKED)
        print("Parked your rover code.py on CIRCUITPY as", PARKED)
    else:
        print(f"Note: no rover code.py found to park. `restore` will need {PARKED} or a fresh `rover`.")


def run_as_code(drive, source):
    park_rover_code(drive)
    shutil.copy2(source, drive / "code.py")
    print(f"{source.name} is now running as code.py. Open the serial console (Mu/Thonny) to follow it.")
    print("When you're done:  uv run deploy.py restore")


def restore(drive):
    parked = drive / PARKED
    if not parked.exists():
        sys.exit(f"No {PARKED} on CIRCUITPY. Use `uv run deploy.py rover` to install the rover instead.")
    shutil.copy2(parked, drive / "code.py")
    parked.unlink()
    print("Your rover code.py is back. Put the rover on its stand -- it starts driving right away.")


def main():
    parser = argparse.ArgumentParser(description="Copy the full-build rover software onto CIRCUITPY.")
    parser.add_argument("--drive", type=Path, help="path to the CIRCUITPY drive, if not found automatically")
    sub = parser.add_subparsers(dest="command", required=True)
    rover = sub.add_parser("rover", help="install libraries and the whole rover")
    rover.add_argument("--overwrite", action="store_true", help="replace files you changed on CIRCUITPY")
    tool = sub.add_parser("tool", help="run a calibration tool as code.py")
    tool.add_argument("name", choices=sorted(p.stem for p in TOOLS_SRC.glob("*.py")))
    sub.add_parser("test", help="run test/device_test.py as code.py")
    sub.add_parser("restore", help="put your rover code.py back")
    args = parser.parse_args()

    drive = args.drive or find_circuitpy()
    if drive is None or not drive.is_dir():
        sys.exit("Couldn't find the CIRCUITPY drive. Plug in the Pico, or name it with --drive.")
    print("CIRCUITPY drive:", drive)

    if args.command == "rover":
        deploy_rover(drive, args.overwrite)
    elif args.command == "tool":
        run_as_code(drive, TOOLS_SRC / f"{args.name}.py")
    elif args.command == "test":
        run_as_code(drive, TEST_SRC / "device_test.py")
    else:
        restore(drive)


if __name__ == "__main__":
    main()
