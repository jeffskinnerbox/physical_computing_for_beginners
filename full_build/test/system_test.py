#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyserial"]
# ///
# system_test.py -- full build: whole-rover test. Runs on your LAPTOP, against the REAL,
# unchanged rover code.py running on the Pico. From the full_build folder:
#
#   uv run test/system_test.py                    (finds the Pico's USB port itself)
#   uv run test/system_test.py COM5               (or /dev/ttyACM0 -- name the port)
#   uv run test/system_test.py --url http://192.168.4.1:5000 --show-log
#
# Before you start: rover ON ITS STAND, USB plugged in, battery switch ON, laptop joined to
# the rover's WiFi network, and Mu/Thonny's serial console CLOSED (only one program can use
# the port). It listens to the rover's log over USB, reads /data.json over WiFi, and coaches
# you through triggering each behavior. Its checks use wide ranges, so it passes the same
# way before and after tuning. Exit code 0 = no FAIL, 1 = something failed.

import argparse
import json
import re
import sys
import threading
import time
import urllib.request

import serial
import serial.tools.list_ports

PICO_VENDOR_IDS = {0x239A, 0x2E8A}  # Adafruit (CircuitPython) and Raspberry Pi
DEFAULT_URL = "http://192.168.4.1:5000"
DRIVE_STATES = {"driving", "scanning", "stopped"}
STOP_REASONS = {"none", "ultrasonic", "ir", "limit_switch"}
CLOSE_HAND_LIMIT_CM = 40  # STOP_DISTANCE_CM is somewhere in 20-40; your hand is at ~10 cm

# The rover's log lines (exact formats from code.py, rover_server.py, speed_knob.py).
PATTERNS = {
    "ssid": re.compile(r"Connect to SSID: '(.*)'"),
    "gyro_cal": re.compile(r"Calibrating gyro"),
    "http": re.compile(r"HTTP Server running at (\S+)"),
    "boot": re.compile(r"Full build -- Random Rover starting"),
    "drive": re.compile(r"drive: forward, heading (-?\d+) speed (-?[\d.]+)"),
    "stop": re.compile(r"drive: (stopped|emergency stop) for scan"),
    "scan_angle": re.compile(r"scan: angle (-?[\d.]+) distance_cm (\S+)"),
    "chosen": re.compile(r"scan: chosen angle (-?[\d.]+)"),
    "turning": re.compile(r"drive: turning (-?[\d.]+) deg to heading (-?\d+)"),
    "no_turn": re.compile(r"drive: no turn needed"),
    "timed_out": re.compile(r"drive: turn timed out, still off by (-?\d+) deg"),
    "heading_now": re.compile(r"drive: heading now (-?\d+)"),
    "obstacle": re.compile(r"drive: obstacle close, distance_cm (-?[\d.]+)"),
    "bump": re.compile(r"SAFETY: bump switch contact"),
    "ir": re.compile(r"SAFETY: IR sensor near-field obstacle"),
    "knob": re.compile(r"knob: current_speed (-?[\d.]+)"),
    "traceback": re.compile(r"Traceback \(most recent call last\)"),
    "device_test": re.compile(r"Device test -- "),
}
# CircuitPython also sends terminal escape codes (e.g. its title-bar status) -- strip them.
ESCAPE_CODES = re.compile(r"\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)|\x1b\[[0-9;?]*[A-Za-z]")

# Never send rover requests through a web proxy -- 192.168.4.1 is only on the rover's WiFi.
WEB = urllib.request.build_opener(urllib.request.ProxyHandler({}))


# ---------- the rover's USB log ----------

class RoverLog:
    """Reads the rover's serial log in the background and keeps every line with a timestamp."""

    def __init__(self, port, show_log):
        self.port = port
        self.show_log = show_log
        self.lines = []  # (time.monotonic(), text)
        self.lock = threading.Lock()
        self.error = None
        threading.Thread(target=self._read_forever, daemon=True).start()

    def _read_forever(self):
        pending = b""
        while True:
            try:
                pending += self.port.read(256)
            except (serial.SerialException, OSError) as err:
                self.error = err  # USB unplugged, most likely
                return
            *complete, pending = pending.split(b"\n")
            for raw in complete:
                text = ESCAPE_CODES.sub("", raw.decode(errors="replace")).strip()
                if text:
                    with self.lock:
                        self.lines.append((time.monotonic(), text))
                    if self.show_log:
                        print("    rover|", text)

    def find(self, name, since=0.0, until=float("inf")):
        """All (time, match) for lines matching PATTERNS[name] between since and until."""
        pattern = PATTERNS[name]
        with self.lock:
            lines = list(self.lines)
        found = []
        for stamp, text in lines:
            match = pattern.search(text)
            if match and since < stamp <= until:
                found.append((stamp, match))
        return found

    def wait_for(self, name, since, timeout):
        """The first (time, match) for `name` after `since`, waiting up to timeout s -- or None."""
        end_time = time.monotonic() + timeout
        while time.monotonic() < end_time:
            found = self.find(name, since)
            if found:
                return found[0]
            if self.error:
                raise SystemExit(f"Lost the USB connection to the rover: {self.error}")
            time.sleep(0.1)
        return None

    def send(self, data):
        self.port.write(data)


# ---------- the rover's website ----------

def fetch(url, timeout):
    with WEB.open(url, timeout=timeout) as reply:
        return reply.read().decode(errors="replace")


def read_data(base_url, patience=20.0):
    """GET /data.json, retrying for up to `patience` s (the rover doesn't answer while it
    scans or turns). Returns (dict, arrival time) or (None, last error)."""
    end_time = time.monotonic() + patience
    error = "no answer"
    while True:
        try:
            data = json.loads(fetch(base_url + "/data.json", timeout=6))
            return data, time.monotonic()
        except (OSError, ValueError) as err:  # URLError and timeouts are OSErrors
            error = err
        if time.monotonic() >= end_time:
            return None, error
        time.sleep(1)


def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def problems_in_data(data):
    """Check /data.json's fields and ranges; return a list of problems (empty = good)."""
    problems = []
    for key in ("speed_left_cms", "speed_right_cms", "roll", "pitch", "yaw", "heading", "scan_heading"):
        if not is_number(data.get(key)):
            problems.append(f"{key} missing or not a number ({data.get(key)!r})")
    for key in ("dir_left", "dir_right"):
        if data.get(key) not in (-1, 0, 1):
            problems.append(f"{key} should be -1, 0 or 1 ({data.get(key)!r})")
    if data.get("drive_state") not in DRIVE_STATES:
        problems.append(f"drive_state {data.get('drive_state')!r} not one of {sorted(DRIVE_STATES)}")
    if data.get("stop_reason") not in STOP_REASONS:
        problems.append(f"stop_reason {data.get('stop_reason')!r} not one of {sorted(STOP_REASONS)}")
    if problems:
        return problems
    if not 0 <= data["heading"] < 360:
        problems.append(f"heading {data['heading']} not in 0-360")
    if not (-180 <= data["roll"] <= 180 and -90 <= data["pitch"] <= 90 and -180 <= data["yaw"] <= 180):
        problems.append("roll/pitch/yaw out of range")
    if abs(angle_change(data["heading"], -data["yaw"])) > 1:
        problems.append("heading doesn't match yaw (heading should be -yaw, wrapped to 0-360)")
    if not (0 <= data["speed_left_cms"] < 500 and 0 <= data["speed_right_cms"] < 500):
        problems.append("wheel speeds out of range")
    return problems


# ---------- helpers ----------

def angle_change(start, end):
    """Signed degrees from start to end, -180..180 (+ = clockwise for compass headings)."""
    return (end - start + 180) % 360 - 180


def classify(text):
    """Return (pattern name, match) for a rover log line, or (None, None)."""
    for name, pattern in PATTERNS.items():
        match = pattern.search(text)
        if match:
            return name, match
    return None, None


def follow_cycle(lines):
    """Walk log lines through one drive -> stop -> scan -> turn -> drive cycle.
    The returned dict's "stage" is what it's still waiting for ("done" = full cycle)."""
    cycle = {"stage": "drive", "angles": [], "distances": [], "timed_out": False}
    for text in lines:
        name, match = classify(text)
        stage = cycle["stage"]
        if stage == "drive" and name == "drive":
            cycle["speed"] = float(match.group(2))
            cycle["stage"] = "stop"
        elif stage == "stop" and name == "stop":
            cycle["stage"] = "scan"
        elif stage == "scan" and name == "scan_angle":
            cycle["angles"].append(float(match.group(1)))
            cycle["distances"].append(match.group(2))
        elif stage == "scan" and name == "chosen":
            cycle["chosen"] = float(match.group(1))
            cycle["stage"] = "turn"
        elif stage == "turn" and name == "timed_out":
            cycle["timed_out"] = True
        elif stage == "turn" and name in ("no_turn", "heading_now"):
            cycle["stage"] = "drive again"
        elif stage == "drive again" and name == "drive":
            cycle["stage"] = "done"
            break
    return cycle


def ask_yes_no(question, default=True):
    hint = "Y/n" if default else "y/N"
    while True:
        answer = input(f"{question} ({hint}) ").strip().lower()
        if not answer:
            return default
        if answer[0] in "yn":
            return answer[0] == "y"


def find_pico_port():
    """Return the serial port of the first plugged-in CircuitPython board, or None."""
    ports = sorted(
        (p for p in serial.tools.list_ports.comports() if p.vid in PICO_VENDOR_IDS),
        key=lambda p: p.device,
    )
    return ports[0].device if ports else None


def open_port(name):
    try:
        return serial.Serial(name, 115200, timeout=0.1, exclusive=True)
    except (serial.SerialException, OSError, ValueError) as err:
        sys.exit(
            f"Couldn't open {name}: {err}\n"
            "Only one program can use the port. Close Mu's serial panel, or in Thonny click\n"
            "Stop, then Run > Disconnect -- then run this test again. (Linux: are you in the\n"
            "'dialout' group?)"
        )


# ---------- the checks ----------
# Each check returns (status, note) with status "PASS", "FAIL", or "WARN".

class SystemTest:
    def __init__(self, log, base_url):
        self.log = log
        self.url = base_url
        self.ssid = None

    def wifi_hint(self, error):
        network = f"'{self.ssid}'" if self.ssid else "your rover's network (settings.toml)"
        return (f"no answer from {self.url} ({error}) -- is the laptop joined to WiFi {network}? "
                "(The rover's WiFi has no internet; tell your laptop to stay connected anyway.)")

    def check_boot(self):
        """Soft-reboot the rover (Ctrl-C, Ctrl-D) and watch its start-up messages."""
        print("  Restarting the rover... keep it STILL and FLAT (it calibrates the gyro).")
        mark = time.monotonic()
        self.log.send(b"\x03")
        time.sleep(0.3)
        self.log.send(b"\x03")
        time.sleep(1.0)
        self.log.send(b"\x04")
        http = self.log.wait_for("http", mark, 40)
        boot = self.log.wait_for("boot", mark, 20)
        ssid = self.log.find("ssid", mark)
        if ssid:
            self.ssid = ssid[-1][1].group(1)
            print(f"  Rover WiFi network: '{self.ssid}'")
        if self.log.find("device_test", mark):
            return "FAIL", "the device test is running as code.py -- run `uv run deploy.py restore` first"
        if not (http and boot):
            missing = "HTTP Server line" if not http else "'Full build -- Random Rover starting...'"
            return "FAIL", f"no {missing} -- run with --show-log to see what it printed"
        if not self.log.find("gyro_cal", mark):
            return "WARN", "started, but no 'Calibrating gyro' line seen"
        rover_url = http[1].group(1).rstrip("/")
        print("  Your laptop may need a few seconds to rejoin the rover's WiFi after the restart.")
        if rover_url != self.url:
            return "WARN", f"rover says {rover_url}, testing {self.url} -- use --url {rover_url}?"
        return "PASS", f"WiFi, gyro calibration, and server at {rover_url} all started"

    def watch_one_cycle(self, timeout=45):
        """Follow the log through drive -> stop -> scan -> turn -> drive. Returns a dict."""
        start = time.monotonic()
        while True:
            with self.log.lock:
                lines = [text for stamp, text in self.log.lines if stamp > start]
            cycle = follow_cycle(lines)
            if cycle["stage"] == "done" or time.monotonic() - start > timeout:
                break
            time.sleep(0.2)
        cycle["safety"] = len(self.log.find("bump", start)) + len(self.log.find("ir", start))
        cycle["obstacles"] = len(self.log.find("obstacle", start))
        return cycle

    def check_cycle(self):
        print("  Watching the log for one full drive -> scan -> turn -> drive cycle (up to 45 s)...")
        cycle = self.watch_one_cycle()
        if self.log.find("device_test"):
            return "FAIL", "the device test is running as code.py -- run `uv run deploy.py restore` first"
        if cycle["stage"] != "done":
            return "FAIL", f"cycle stalled waiting for '{cycle['stage']}' -- run with --show-log to see the log"
        angles = ", ".join(f"{angle:g}" for angle in cycle["angles"])
        print(f"  Drove at speed {cycle['speed']:g}, scanned at [{angles}], chose {cycle['chosen']:g}.")
        if cycle["timed_out"]:
            print("  'turn timed out' is EXPECTED on the stand: the wheels spin but the rover can't")
            print("  actually turn, so the compass never reaches the target heading.")
        if cycle["chosen"] not in cycle["angles"] and any(d != "None" for d in cycle["distances"]):
            return "FAIL", f"chose {cycle['chosen']:g}, which wasn't one of the scanned angles"
        if all(d == "None" for d in cycle["distances"]):
            return "WARN", "cycle ran, but the ultrasonic sensor got no echo at any angle"
        if cycle["safety"]:
            return "WARN", "cycle ran, but bump/IR fired with nobody touching -- IR seeing the stand or table?"
        if cycle["obstacles"]:
            return "WARN", "cycle ran, but 'obstacle close' with nothing near -- point the rover at open space"
        if cycle["speed"] == 0:
            return "WARN", "cycle ran, but drive speed is 0 (DRIVE_SPEED or the knob) -- wheels won't turn"
        return "PASS", "drive -> stop -> scan -> turn -> drive"

    def check_data(self):
        print("  Reading /data.json three times...")
        samples = []
        for _ in range(3):
            data, arrived = read_data(self.url)
            if data is None:
                return "FAIL", self.wifi_hint(arrived)
            samples.append(data)
            time.sleep(1)
        problems = [problem for data in samples for problem in problems_in_data(data)]
        if problems:
            return "FAIL", "; ".join(sorted(set(problems)))
        last = samples[-1]
        print(f"  heading {last['heading']:.0f}, roll {last['roll']:.0f}, pitch {last['pitch']:.0f}, "
              f"drive_state {last['drive_state']}, wheels {last['speed_left_cms']:.0f} / "
              f"{last['speed_right_cms']:.0f} cm/s")
        driving = [d for d in samples if d["drive_state"] == "driving" and d["dir_left"] == 1]
        if driving and not any(d["speed_left_cms"] > 0 and d["speed_right_cms"] > 0 for d in driving):
            return "WARN", "fields OK, but a wheel shows 0 cm/s while driving -- wheel sensor, or speed below stall?"
        return "PASS", "all fields present, right types, sane ranges"

    def check_page(self):
        try:
            page = fetch(self.url + "/", timeout=8)
        except OSError as err:
            return "FAIL", self.wifi_hint(err)
        missing = [text for text in ("Rover Status", "/data.json", "Recent History", "<canvas")
                   if text not in page]
        if missing:
            return "FAIL", f"status page is missing: {', '.join(missing)} (history_chart imported?)"
        return "PASS", "status page with the Recent History chart"

    def stop_reason_after(self, event_time, expected):
        """After a stop at event_time, read stop_reason as soon as the rover drives again."""
        drive = self.log.wait_for("drive", event_time, 20)
        if drive is None:
            return "FAIL", "the rover never drove again after stopping"
        data, arrived = read_data(self.url, patience=8)
        if data is None:
            return "WARN", f"log line seen, but couldn't read the website: {self.wifi_hint(arrived)}"
        if data.get("stop_reason") == expected:
            return "PASS", f"log line seen, website stop_reason = {expected!r}"
        if self.log.find("stop", drive[0], arrived):
            return "WARN", "log line seen; the rover moved on before the website answered -- try again"
        return "FAIL", f"log line seen, but website stop_reason = {data.get('stop_reason')!r}, not {expected!r}"

    def check_safety_sensor(self, name, expected, how):
        print(f"  When you press Enter you have 20 s to: {how}")
        print("  (The rover only checks it while driving, so a quick tap during a scan is missed.)")
        input("  Press Enter, then do it: ")
        event = self.log.wait_for(name, time.monotonic(), 20)
        if event is None:
            return "FAIL", f"no '{PATTERNS[name].pattern}' line in the log"
        print("  Seen in the log! Let go / move away now.")
        return self.stop_reason_after(event[0], expected)

    def check_bump(self):
        return self.check_safety_sensor("bump", "limit_switch", "press and HOLD the bump switch lever until told.")

    def check_ir(self):
        return self.check_safety_sensor("ir", "ir", "hold your hand 3-5 cm in front of the IR sensor until told.")

    def check_obstacle(self):
        print("  When you press Enter, hold your hand flat about 10 cm in front of the ultrasonic")
        print("  sensor (it points straight ahead while driving). Keep it HIGH, out of the IR")
        print("  sensor's view. Hold it there until told (up to 25 s).")
        input("  Press Enter, then hold your hand there: ")
        mark = time.monotonic()
        event = self.log.wait_for("obstacle", mark, 25)
        if event is None:
            if self.log.find("ir", mark):
                return "FAIL", "the IR sensor saw your hand first -- hold it higher and try again"
            return "FAIL", "no 'drive: obstacle close' line -- hand straight in front of the sensor?"
        print("  Seen in the log! Take your hand away.")
        distance = float(event[1].group(1))
        if not 0 < distance < CLOSE_HAND_LIMIT_CM:
            return "FAIL", f"stopped at {distance:.0f} cm -- your hand was at ~10 cm"
        status, note = self.stop_reason_after(event[0], "ultrasonic")
        return status, f"stopped with your hand at {distance:.0f} cm; {note}"

    def turn_knob(self, direction):
        """Ask for 3 clicks; return the knob speeds logged (after the rover applies them)."""
        mark = time.monotonic()
        input(f"  Turn the knob {direction} 3 clicks, slowly, then press Enter: ")
        print("  Waiting for the rover to drive again (it reads the knob while driving)...")
        drive = self.log.wait_for("drive", time.monotonic(), 20)
        until = drive[0] if drive else float("inf")
        return [float(match.group(1)) for _, match in self.log.find("knob", mark, until)]

    def check_knob(self):
        down = self.turn_knob("COUNTER-CLOCKWISE")
        up = self.turn_knob("CLOCKWISE")
        print(f"  Knob speeds logged: counter-clockwise {down}, clockwise {up}")
        if not down and not up:
            return "FAIL", "no 'knob: current_speed' lines -- run the device test's knob step"
        if not (down and up):
            return "FAIL", "the knob answered one direction only -- turn it firmly, one click at a time"
        if up[-1] > down[-1]:
            return "PASS", f"clockwise = faster ({down[-1]:g} -> {up[-1]:g})"
        if up[-1] < down[-1]:
            return "WARN", "clockwise = SLOWER -- swap board.GP3 and board.GP4 in speed_knob.py"
        return "WARN", f"speed stayed at {up[-1]:g} -- check MIN_SPEED / SPEED_STEP in speed_knob.py"

    def check_heading(self):
        print("  Keep the rover still on its stand...")
        first = self.log.wait_for("drive", time.monotonic(), 20)
        if first is None:
            return "FAIL", "no 'drive: forward' line in 20 s"
        start = int(first[1].group(1))
        print(f"  Heading now {start}. Lift the rover WITH its stand and turn it CLOCKWISE (seen")
        print("  from above) a quarter turn, about 90 deg. Keep it flat and set it down.")
        input("  Press Enter when it's set down: ")
        after = self.log.wait_for("drive", time.monotonic(), 20)
        if after is None:
            return "FAIL", "no 'drive: forward' line in 20 s"
        end = int(after[1].group(1))
        change = angle_change(start, end)
        print(f"  Heading {start} -> {end}: changed {change:+d} deg (expect about +90)")
        if 45 <= change <= 135:
            return "PASS", f"heading went up {change} deg for a clockwise quarter turn"
        hint = "check MAG_AXIS_SIGN (build Step 7)" if change < 0 else "calibrate the compass (MAG_OFFSET)"
        return "WARN", f"heading changed {change:+d} deg -- {hint}, boot still and flat"

    def check_no_crash(self):
        with self.log.lock:
            lines = [text for _, text in self.log.lines]
        for number, text in enumerate(lines):
            if not PATTERNS["traceback"].search(text):
                continue
            # The error is the first line after the "File ..." lines. KeyboardInterrupt
            # just means Ctrl-C (our own restart), not a crash.
            error = next((line for line in lines[number + 1:] if not line.startswith("File ")), "")
            if not error.startswith("KeyboardInterrupt"):
                return "FAIL", f"the rover code crashed: {error} -- run with --show-log to see where"
        return "PASS", "no errors in the rover's log"

def main():
    parser = argparse.ArgumentParser(description="Whole-rover test for the full-build Random Rover.")
    parser.add_argument("port", nargs="?", help="serial port, e.g. COM5 or /dev/ttyACM0 (found automatically)")
    parser.add_argument("--url", default=DEFAULT_URL, help=f"rover website (default {DEFAULT_URL})")
    parser.add_argument("--show-log", action="store_true", help="also print every rover log line")
    args = parser.parse_args()

    port_name = args.port or find_pico_port()
    if port_name is None:
        sys.exit("Couldn't find a Pico. Check the USB cable, or name the port: uv run test/system_test.py COM5")
    print("Full build -- Random Rover system test, on", port_name)
    print("Rover ON ITS STAND, battery ON, laptop on the rover's WiFi, Mu/Thonny closed.")
    log = RoverLog(open_port(port_name), args.show_log)
    test = SystemTest(log, args.url.rstrip("/"))

    checks = [
        ("Running cycle", "Hands off -- just watch.", test.check_cycle),
        ("Website data", "Laptop on the rover's WiFi.", test.check_data),
        ("Website page", "Laptop on the rover's WiFi.", test.check_page),
        ("Bump switch", "Get ready to press the bump switch.", test.check_bump),
        ("IR sensor", "Get ready to hold your hand in front of the IR sensor.", test.check_ir),
        ("Close obstacle", "Get ready to hold your hand in front of the ultrasonic sensor.", test.check_obstacle),
        ("Speed knob", "Get ready to turn the encoder knob.", test.check_knob),
        ("Heading (optional)", "Get ready to lift and turn the rover with its stand.", test.check_heading),
        ("No crashes", "Checks the whole log for errors.", test.check_no_crash),
    ]
    results = []
    try:
        if ask_yes_no("Restart the rover first to check its start-up? (rover still and flat)"):
            checks.insert(0, ("Start-up", "Rover still and flat on its stand.", test.check_boot))
        for number, (name, intro, check) in enumerate(checks, 1):
            print(f"\n--- Check {number} of {len(checks)}: {name} ---\n  {intro}")
            if input("  Press Enter to start (s = skip): ").strip().lower() == "s":
                results.append((name, "SKIP", "skipped"))
                continue
            while True:
                status, note = check()
                print(f"  -> {status}: {note}")
                if status == "PASS" or not ask_yes_no("  Try this check again?", default=False):
                    break
            results.append((name, status, note))
    except (KeyboardInterrupt, EOFError):
        print("\nStopped early.")

    print("\n=== System test summary ===")
    for name, status, note in results:
        print(f"{status:5} {name:19} {note}")
    failed = [name for name, status, _ in results if status == "FAIL"]
    print("Failed:", ", ".join(failed) if failed else "none -- the whole rover works!")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
