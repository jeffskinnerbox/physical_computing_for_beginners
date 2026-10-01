# device_test.py -- full build: Device test, the part-by-part check of the Random Rover.
# Deploy with `uv run deploy.py test` (it runs as code.py); `uv run deploy.py restore` when done.
# Walks you through every part, one at a time, using the SAME library files the rover
# drives with (motor_driver, wheel_odometry, speed_knob, tft_status, rover_server), so it
# tests the code you'll actually drive with. Type your answers in the serial console
# (Mu or Thonny): Enter to go on, y or n when asked, s to skip a step.
# Keep the rover ON ITS STAND, battery switch ON, USB plugged in.
import sys
import time

import adafruit_hcsr04
import board
import busio
import digitalio
import motor_driver  # the rover's own motor library -- motors stop in the finally: below
import pwmio
import supervisor
from adafruit_motor import servo

print()
print("Device test -- Random Rover part-by-part test")
print("Rover on its stand, battery switch ON, USB plugged in.")


def try_import(name):
    """Import a rover library, or return None (and say why) if it won't load."""
    try:
        return __import__(name)
    except Exception as err:  # noqa: BLE001 -- ImportError, a missing part, a pin in use, ...
        print("Couldn't load", name + ":", err)
        return None


tft_status = try_import("tft_status")  # screen first, like the rover's code.py
wheel_odometry = try_import("wheel_odometry")
speed_knob = try_import("speed_knob")
rover_server = None  # WiFi + IMU library -- started by its own step (it calibrates the gyro)


def rover_setting(name, default):
    """Read a number from your parked rover code (code_rover.py), so tuned values
    like min_pulse=... or CENTER_ANGLE = ... are tested. Falls back to default."""
    try:
        with open("/code_rover.py") as rover_code:
            for line in rover_code:
                start = line.find(name)
                if start < 0 or line.lstrip().startswith("#"):
                    continue
                text = line[start + len(name):].lstrip(" =")
                number = ""
                for char in text:
                    if char not in "-.0123456789":
                        break
                    number += char
                return float(number) if "." in number else int(number)
    except (OSError, ValueError):
        pass
    return default


# The parts code.py creates itself -- same pins and settings as code.py.
SERVO_MIN_PULSE = rover_setting("min_pulse=", 500)
SERVO_MAX_PULSE = rover_setting("max_pulse=", 2500)
CENTER_ANGLE = max(30, min(150, rover_setting("CENTER_ANGLE", 90)))  # stay in the 30-150 scan range

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP6, echo_pin=board.GP7)
pwm = pwmio.PWMOut(board.GP8, duty_cycle=0, frequency=50)
scan_servo = servo.Servo(pwm, min_pulse=SERVO_MIN_PULSE, max_pulse=SERVO_MAX_PULSE)

bump_switch = digitalio.DigitalInOut(board.GP5)
bump_switch.direction = digitalio.Direction.INPUT
bump_switch.pull = digitalio.Pull.UP  # LOW when pressed

ir_sensor = digitalio.DigitalInOut(board.GP13)
ir_sensor.direction = digitalio.Direction.INPUT  # LOW when it sees something

TEST_THROTTLE = min(0.5, motor_driver.MAX_THROTTLE)  # modest -- and never above the cap
KNOB_CLICKS = 6

results = []  # (step name, "PASS" / "FAIL" / "WARN" / "SKIP", note)


# ---------- typing in the serial console without stopping the rover's website ----------

def keep_alive():
    """Keep the website answering and the IMU filter running while we wait for you.
    (Plain input() would freeze both until you pressed Enter.)"""
    if rover_server is None:
        return
    try:
        rover_server.server.poll()
    except OSError:
        pass  # a browser hung up mid-request -- not our problem here
    rover_server.update()


_last_char = ""


def read_line(prompt=""):
    """Like input(), but calls keep_alive() about every 20 ms while you type."""
    global _last_char
    print(prompt, end="")
    typed = ""
    while True:
        if not supervisor.runtime.serial_bytes_available:
            keep_alive()
            time.sleep(0.02)
            continue
        char = sys.stdin.read(1)
        previous, _last_char = _last_char, char
        if not char or (char == "\n" and previous == "\r"):
            continue  # second half of a Windows-style Enter
        if char in "\r\n":
            print()
            return typed.strip().lower()
        if char in "\x08\x7f":  # backspace
            if typed:
                typed = typed[:-1]
                print("\b \b", end="")
        else:
            typed += char
            print(char, end="")  # sys.stdin.read() doesn't echo, so we do


def ask_choice(question, choices):
    """Ask until the answer is one of the letters in choices; return that letter."""
    while True:
        answer = read_line(question + " ")
        if answer and answer[0] in choices:
            return answer[0]
        print("  Please type one of:", ", ".join(choices))


def ask_yes_no(question):
    return ask_choice(question + " (y/n)", "yn") == "y"


def wait_for(condition, seconds):
    """Return True as soon as condition() is True, or False after `seconds`."""
    end_time = time.monotonic() + seconds
    while time.monotonic() < end_time:
        if condition():
            return True
        keep_alive()
        time.sleep(0.01)
    return False


def settle(seconds):
    """Wait, keeping the IMU filter and website running."""
    wait_for(lambda: False, seconds)


def magnitude(vector):
    return sum(axis * axis for axis in vector) ** 0.5


def average_reading(read, samples=50):
    """Average `samples` (x, y, z) readings from read()."""
    total = [0.0, 0.0, 0.0]
    for _ in range(samples):
        for axis, value in enumerate(read()):
            total[axis] += value
        time.sleep(0.01)
    return [value / samples for value in total]


def read_distance():
    try:
        return sonar.distance
    except RuntimeError:  # no echo came back
        return None


# ---------- the steps ----------

def test_power():
    print("Black meter probe on a GND (-) rail, red probe on each + rail.")
    rail_5v = ask_yes_no("Top + rail (5V): between 4.8 and 5.2 V?")
    rail_3v3 = ask_yes_no("Bottom + rail (3.3V): between 3.2 and 3.4 V?")
    if rail_5v and rail_3v3:
        return "PASS", "both rails in range"
    if not rail_5v:
        return "FAIL", "5V rail: set the buck converter to 5.0 V (Pico unplugged!), check its OUT+ / OUT-"
    return "FAIL", "3.3V rail: check the Pico 3V3(OUT) pin feeds the bottom + rail; look for a short"


def test_i2c_scan():
    i2c = busio.I2C(board.GP1, board.GP0)  # SCL, SDA -- same as rover_server.py
    try:
        while not i2c.try_lock():
            pass
        found = i2c.scan()
        i2c.unlock()
    finally:
        i2c.deinit()  # free GP0/GP1 for rover_server
    print("  I2C addresses found:", [hex(address) for address in found])
    accel_gyro = 0x6B in found or 0x6A in found
    compass = 0x1E in found or 0x1C in found
    if not (accel_gyro and compass):
        return "FAIL", "LSM9DS1 not found: SDA -> GP0, SCL -> GP1 (not swapped), VIN -> 3.3V, GND"
    if 0x6B in found and 0x1E in found:
        return "PASS", "accel/gyro 0x6b, compass 0x1e"
    return "WARN", "found at non-default addresses; rover_server.py expects 0x6b and 0x1e"


def test_start_rover_server():
    global rover_server
    print("  Starting WiFi and calibrating the gyro -- DON'T touch the rover...")
    try:
        rover_server = __import__("rover_server")
        __import__("history_chart")  # same website page as the rover
    except Exception as err:  # noqa: BLE001 -- WiFi, IMU, or settings.toml trouble
        return "FAIL", f"rover_server didn't start: {err} (settings.toml? IMU wiring?)"
    return "PASS", f"WiFi network '{rover_server.ap_ssid}' is up, gyro calibrated"


def test_imu():
    imu = rover_server.imu
    bias = (rover_server.bias_x, rover_server.bias_y, rover_server.bias_z)
    accel = average_reading(lambda: imu.acceleration)
    gyro = average_reading(lambda: [raw - offset for raw, offset in zip(imu.gyro, bias)])
    compass = average_reading(lambda: imu.magnetic)
    gravity = magnitude(accel)
    spin = max(abs(axis) for axis in gyro)
    field = magnitude(compass)
    print(f"  gravity {gravity:.2f} m/s^2 (expect about 9.8)")
    print(f"  gyro    {spin:.3f} rad/s on its worst axis (expect near 0)")
    print(f"  compass {field:.2f} gauss (expect about 0.2-0.7, never 0)")
    problems = []
    if not 8.8 <= gravity <= 10.8:
        problems.append("gravity is off -- accelerometer problem")
    if spin > 0.05:
        problems.append("gyro not near 0 -- was the rover still? restart the test with it still")
    if not 0.05 <= field <= 4.0:
        problems.append("compass reads ~0 or maxed out -- magnet or steel nearby?")
    if problems:
        return "FAIL", "; ".join(problems)
    return "PASS", "gravity, gyro, and compass all sane"


def test_heading():
    settle(2)  # let the filter settle on where the rover points now
    start = rover_server.latest_heading
    print(f"  Heading now: {start:.0f} deg.")
    print("  Lift the rover (with its stand) and turn it CLOCKWISE, seen from above,")
    print("  a quarter turn (about 90 deg). Keep it flat, take about 2 s, set it down.")
    read_line("  Press Enter when it's still again: ")
    settle(0.5)
    end = rover_server.latest_heading
    change = (end - start + 180) % 360 - 180  # -180..180, + = clockwise
    print(f"  Heading now: {end:.0f} deg -- changed by {change:+.0f} deg (expect about +90)")
    if 45 <= change <= 135:
        return "PASS", f"heading went up {change:.0f} deg for a clockwise quarter turn"
    hint = "turned the wrong way? check MAG_AXIS_SIGN" if change < 0 else "check you booted still and flat"
    if rover_server.MAG_OFFSET == (0.0, 0.0, 0.0):
        return "WARN", f"changed {change:+.0f}; compass not calibrated yet -- calibrate (build Step 7), then re-run"
    return "FAIL", f"changed {change:+.0f} deg; {hint}"


def test_servo():
    print(f"  min_pulse={SERVO_MIN_PULSE}, max_pulse={SERVO_MAX_PULSE}, straight ahead = {CENTER_ANGLE}")
    problems = []
    for angle, where in ((CENTER_ANGLE, "STRAIGHT AHEAD"), (30, "about 60 deg LEFT"),
                         (150, "about 60 deg RIGHT")):
        scan_servo.angle = angle  # never outside 30-150, the rover's own range
        time.sleep(0.8)
        if not ask_yes_no(f"  Servo at {angle}: is the sensor pointing {where}?"):
            problems.append(where.lower())
    scan_servo.angle = CENTER_ANGLE
    if not problems:
        return "PASS", "points left, ahead, and right"
    if len(problems) == 3:
        return "FAIL", "servo didn't move: signal -> GP8, red -> 5V rail, brown -> GND"
    return "FAIL", "wrong at: {} -- re-aim the horn or tune the pulses (tuning Step 3)".format(", ".join(problems))


def test_sonar():
    scan_servo.angle = CENTER_ANGLE
    print("  Hold a box or book flat-on in front of the ultrasonic sensor and keep it there.")
    answer = read_line("  How far away is it, in cm (10-100)? ")
    try:
        actual = float(answer)
    except ValueError:
        return "FAIL", "that wasn't a number -- try again"
    readings = []
    for _ in range(7):
        distance = read_distance()
        if distance is not None:
            readings.append(distance)
        time.sleep(0.1)
    if not readings:
        return "FAIL", "no echo: TRIG -> GP6, ECHO -> 1k -> GP7 (2k to GND), VCC -> 5V rail"
    measured = sorted(readings)[len(readings) // 2]  # the middle reading ignores odd ones
    print(f"  Sensor says {measured:.0f} cm (you said {actual:.0f} cm)")
    if abs(measured - actual) <= max(5, 0.3 * actual):
        return "PASS", f"{measured:.0f} cm vs {actual:.0f} cm"
    return "FAIL", f"{measured:.0f} cm vs {actual:.0f} cm -- aim straight at a flat surface, recheck wiring"


def spin_one_wheel(side, sign):
    """Drive one wheel for 2 s; return ticks counted by (left, right) wheel sensors."""
    throttle = sign * TEST_THROTTLE
    if side == "LEFT":
        motor_driver.drive(throttle, 0)  # motor A
    else:
        motor_driver.drive(0, throttle)  # motor B
    ticks = [0, 0]
    try:
        for _ in range(8):  # 8 x 0.25 s samples
            speed_left, _, speed_right, _ = wheel_odometry.read_speed()
            ticks[0] += round(speed_left / wheel_odometry.CMS_PER_TICK)
            ticks[1] += round(speed_right / wheel_odometry.CMS_PER_TICK)
    finally:
        motor_driver.stop()
    return ticks


def test_wheel(side):
    """Spin one wheel forward, then backward; you say what moved, the sensors count ticks."""
    if wheel_odometry is None:
        return "FAIL", "wheel_odometry didn't load"
    mine = 0 if side == "LEFT" else 1
    problems = []
    for word, sign in (("FORWARD", 1), ("BACKWARD", -1)):
        read_line(f"  Press Enter to spin the {side} wheel {word} for 2 s: ")
        ticks = spin_one_wheel(side, sign)
        print(f"  Wheel sensor ticks: left {ticks[0]}, right {ticks[1]}")
        seen = ask_choice(f"  What moved? f = {side} wheel forward, b = {side} wheel backward, "
                          "o = the OTHER wheel, n = nothing:", "fbon")
        expected = "f" if sign > 0 else "b"
        if seen == "n":
            problems.append("nothing moved (SLP -> 3.3V? VM -> 9V switch? battery?)")
        elif seen == "o":
            problems.append("wrong wheel -- swap the GP9/GP10 and GP11/GP12 wire pairs")
        elif seen != expected:
            problems.append(f"{side} spins the wrong way -- swap that motor's two leads")
        if seen != "n" and ticks[mine] == 0:
            other_sensor = "GP17" if side == "LEFT" else "GP19"
            if ticks[1 - mine]:
                problems.append(f"ticks on the wrong wheel -- {side} sensor is on {other_sensor}")
            else:
                problems.append("no wheel-sensor ticks -- check the optocoupler fork and DO wire")
    if problems:
        unique = []
        for problem in problems:  # forward and backward often fail the same way
            if problem not in unique:
                unique.append(problem)
        return "FAIL", "; ".join(unique)
    return "PASS", f"{side} wheel spins both ways, sensor counts ticks"


def test_bump():
    if not bump_switch.value:
        return "FAIL", "reads PRESSED before you touched it: NO -> GP5 (not NC), COM -> GND"
    print("  Press and HOLD the bump switch lever (10 s)...")
    if not wait_for(lambda: not bump_switch.value, 10):
        return "FAIL", "press not seen: NO -> GP5, COM -> GND rail"
    print("  Pressed! Now let go.")
    if not wait_for(lambda: bump_switch.value, 10):
        return "FAIL", "release not seen -- lever stuck?"
    return "PASS", "press and release both seen"


def test_ir():
    if not ir_sensor.value:
        return "FAIL", "sees something already: point it at open space, or turn its range screw down"
    print("  Hold your hand about 5 cm in front of the IR sensor (10 s)...")
    if not wait_for(lambda: not ir_sensor.value, 10):
        return "FAIL", "hand not seen: OUT -> GP13, VCC -> 3.3V; turn its range screw up a little"
    print("  Seen! Now take your hand away.")
    if not wait_for(lambda: ir_sensor.value, 10):
        return "FAIL", "still triggered -- something else in view, or range set too far"
    return "PASS", "trigger and clear both seen"


def test_knob():
    if speed_knob is None:
        return "FAIL", "speed_knob didn't load: CLK -> GP3, DT -> GP4"
    speed_knob.update()  # use up any clicks from before this step
    speed_knob.reset(speed_knob.MIN_SPEED)
    start = speed_knob._encoder.position  # speed_knob's own rotaryio counter
    read_line(f"  Turn the knob CLOCKWISE exactly {KNOB_CLICKS} clicks, slowly, then press Enter: ")
    clicks = speed_knob._encoder.position - start
    speed = speed_knob.update()
    expected = min(speed_knob.TOP_SPEED, speed_knob.MIN_SPEED + KNOB_CLICKS * speed_knob.SPEED_STEP)
    print(f"  Counted {clicks} clicks; speed {speed_knob.MIN_SPEED:.2f} -> {speed:.2f} (expect about {expected:.2f})")
    if clicks == 0:
        return "FAIL", "no clicks counted: CLK -> GP3, DT -> GP4, + -> 3.3V rail, GND"
    fixes = []
    if clicks < 0:
        fixes.append("runs backwards -- swap board.GP3 and board.GP4 in speed_knob.py")
    if abs(abs(clicks) - KNOB_CLICKS // 2) <= 1:
        fixes.append("needs 2 clicks per step -- add divisor=2 to IncrementalEncoder(...) in speed_knob.py")
    elif abs(abs(clicks) - KNOB_CLICKS) > 1:
        fixes.append(f"counted {clicks} for {KNOB_CLICKS} clicks -- try again, counting carefully")
    if fixes:
        return "WARN", "; ".join(fixes)
    return "PASS", "clockwise speeds up, one step per click"


def test_tft():
    if tft_status is None:
        return "FAIL", "tft_status didn't load: SCK GP26, MOSI GP27, CS GP20, DC GP21, RST GP22"
    time.sleep(tft_status.REFRESH_S)  # show() skips redraws that come too quickly
    tft_status.show(123, 45, 0.5)
    if ask_yes_no('  Does the screen read "dist: 123 cm", "head: 45 deg", "speed: 0.50"?'):
        return "PASS", "screen shows the test values"
    return "FAIL", "blank: check SCK GP26, MOSI GP27, CS GP20, DC GP21, RST GP22, VIN 3.3V"


def test_website():
    url = f"http://{rover_server.ap_ip}:5000"
    print(f"  On your laptop or phone, join WiFi network '{rover_server.ap_ssid}'")
    print("  then open", url, "and", url + "/data.json")
    read_line("  Press Enter once both have loaded (the website keeps working while you wait): ")
    page = ask_yes_no("  Did the page show Rover Status with numbers updating?")
    data = ask_yes_no("  Did /data.json show heading, roll, pitch, drive_state, ...?")
    if page and data:
        return "PASS", "page and /data.json both load"
    return "FAIL", "joined the right network? URL ends in :5000? settings.toml password 8+ characters?"


# (step name, what to do first, test function, needs rover_server?)
STEPS = (
    ("Power rails", "Switch the battery ON. Have your multimeter ready.", test_power, False),
    ("IMU on I2C", "Checks the LSM9DS1 answers on the I2C bus.", test_i2c_scan, False),
    ("WiFi + gyro start", "Set the rover STILL and FLAT. Don't touch it for 5 s after Enter.",
     test_start_rover_server, False),
    ("IMU readings", "Keep the rover still and flat.", test_imu, True),
    ("Compass heading", "Make room to turn the rover a quarter turn by hand.", test_heading, True),
    ("Scan servo", "Watch the ultrasonic sensor on the servo.", test_servo, False),
    ("Ultrasonic sensor", "Get a box or book and a ruler.", test_sonar, False),
    ("Bump switch", "Get ready to press the bump switch lever.", test_bump, False),
    ("IR sensor", "Point the rover at open space (nothing within 30 cm).", test_ir, False),
    ("Speed knob", "Get ready to turn the encoder knob.", test_knob, False),
    ("TFT screen", "Look at the TFT screen.", test_tft, False),
    ("Left wheel", "!! ROVER ON ITS STAND, wheels off the table, fingers clear !!",
     lambda: test_wheel("LEFT"), False),
    ("Right wheel", "!! ROVER ON ITS STAND, wheels off the table, fingers clear !!",
     lambda: test_wheel("RIGHT"), False),
    ("Website", "Get your laptop or phone.", test_website, True),
)


def run_step(number, name, intro, test, needs_server):
    print()
    print(f"--- Step {number} of {len(STEPS)}: {name} ---")
    if needs_server and rover_server is None:
        print("  Skipped -- needs the 'WiFi + gyro start' step to pass first.")
        results.append((name, "SKIP", "needs WiFi + gyro start"))
        return
    print(" ", intro)
    if read_line("  Press Enter to start (s = skip): ") == "s":
        results.append((name, "SKIP", "skipped"))
        return
    while True:
        try:
            status, note = test()
        except Exception as err:  # noqa: BLE001 -- one broken part shouldn't end the whole test
            status, note = "FAIL", f"error: {err}"
        finally:
            motor_driver.stop()
        print("  ->", status + ":", note)
        if status == "PASS" or test is test_start_rover_server:  # restart (Ctrl-D) to retry that one
            break
        if not ask_yes_no("  Try this step again?"):
            break
    results.append((name, status, note))


try:
    for number, (name, intro, test, needs_server) in enumerate(STEPS, 1):
        run_step(number, name, intro, test, needs_server)
finally:
    motor_driver.stop()  # always -- even after Ctrl-C or a crash

print()
print("=== Device test summary ===")
for name, status, note in results:
    print(f"{status:5} {name:18} {note}")
failed = [name for name, status, _ in results if status == "FAIL"]
print("Failed:", ", ".join(failed) if failed else "none -- every tested part works!")
print("Fix any FAIL and re-run (Ctrl-D). When done: uv run deploy.py restore")
