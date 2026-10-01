# code.py -- full build: the finished Random Rover (Classes 1-6, all stretch goals).
# ruff: noqa: I001 -- import order matters here (see the comments on each import).
# Class 5's stop-look-go rover (class-5-code.py), plus Class 6's three stretch goals:
#   Stretch 1 -- speed_knob:    the encoder sets the drive speed live
#   Stretch 2 -- history_chart: rolling-history chart on the rover website
#   Stretch 3 -- tft_status:    on-board screen with real distance/heading/speed
# Drives forward, rescans on a timer or on proximity, turns toward the clearest
# direction by compass (closed-loop), and reports its decisions on the website.
import time
import board
import digitalio
import pwmio
import adafruit_hcsr04
from adafruit_motor import servo
import motor_driver   # Class 3
import tft_status     # Stretch 3 -- imported first so the screen is up during boot
import rover_server   # Class 5 library version -- importing it calibrates the gyro
                      # and reads the compass, so boot the rover still and flat
import history_chart  # noqa: F401 -- Stretch 2 -- must come after rover_server (edits its STATUS_PAGE)
import speed_knob     # Stretch 1

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP6, echo_pin=board.GP7)
pwm = pwmio.PWMOut(board.GP8, duty_cycle=0, frequency=50)
scan_servo = servo.Servo(pwm, min_pulse=500, max_pulse=2500)  # recalibrate per servo if needed

# The two fixed safety sensors -- both are digital, LOW when triggered.
bump_switch = digitalio.DigitalInOut(board.GP5)
bump_switch.direction = digitalio.Direction.INPUT
bump_switch.pull = digitalio.Pull.UP  # switch pulls the pin LOW when pressed

ir_sensor = digitalio.DigitalInOut(board.GP13)
ir_sensor.direction = digitalio.Direction.INPUT  # module drives its own LOW-on-detect output

# Tune these for your specific robot -- start conservative and adjust.
DRIVE_SPEED = 0.6                     # STARTING drive speed -- the knob changes it live
TURN_SPEED = 0.45                     # spin-in-place speed -- slow enough to stop near the target
SCAN_ANGLES = [30, 60, 90, 120, 150]  # servo degrees, left to right
CENTER_ANGLE = 90                     # servo angle that looks straight ahead
SETTLE_TIME = 0.15                    # seconds -- let the servo stop before trusting a reading
STOP_DISTANCE_CM = 25                 # distance that triggers an immediate rescan
SCAN_INTERVAL = 3.0                   # seconds -- rescan on this timer even if nothing is close
HEADING_TOLERANCE_DEG = 5             # "close enough" to the target heading
TURN_TIMEOUT_S = 3.0                  # give up on a turn whose heading never arrives
BACKOFF_S = 0.3                       # reverse time after a safety stop


def wait(seconds):
    """Drop-in for time.sleep() that keeps rover_server's IMU filter running
    about every 20 ms -- otherwise the heading would miss motion made while sleeping."""
    end_time = time.monotonic() + seconds
    while time.monotonic() < end_time:
        rover_server.update()
        time.sleep(0.02)


def read_distance():
    """Distance in cm, or None if the sensor missed its echo."""
    try:
        return sonar.distance
    except RuntimeError:
        return None


def scan():
    """Sweep SCAN_ANGLES and return the angle with the most open space."""
    readings = {}
    for angle in SCAN_ANGLES:
        scan_servo.angle = angle
        wait(SETTLE_TIME)
        readings[angle] = read_distance()
        print("scan: angle", angle, "distance_cm", readings[angle])
    scan_servo.angle = CENTER_ANGLE
    valid = {a: d for a, d in readings.items() if d is not None}
    best_angle = max(valid, key=valid.get) if valid else CENTER_ANGLE
    print("scan: chosen angle", best_angle)
    return best_angle


def heading_error(target):
    """Signed degrees from the current heading to target, -180..180 (+ = turn right).
    The +180 / % 360 / -180 trick makes 350 -> 10 a 20-degree turn, not 340."""
    return (target - rover_server.latest_heading + 180) % 360 - 180


def turn_toward(angle):
    """Spin in place until the compass heading points where the scan angle did."""
    degrees_off_center = angle - CENTER_ANGLE  # + = right of straight ahead
    if abs(degrees_off_center) < HEADING_TOLERANCE_DEG:
        print("drive: no turn needed")
        return
    target = (rover_server.latest_heading + degrees_off_center) % 360
    print("drive: turning", degrees_off_center, "deg to heading", round(target))
    start = time.monotonic()
    while True:
        error = heading_error(target)
        if abs(error) <= HEADING_TOLERANCE_DEG:
            break
        if time.monotonic() - start > TURN_TIMEOUT_S:
            print("drive: turn timed out, still off by", round(error), "deg")
            break
        if error > 0:
            motor_driver.drive(TURN_SPEED, -TURN_SPEED)   # spin right (clockwise)
        else:
            motor_driver.drive(-TURN_SPEED, TURN_SPEED)   # spin left -- also fixes overshoot
        wait(0.02)  # no server.poll() during a turn: its 0.25 s pause would overshoot
    motor_driver.stop()
    print("drive: heading now", round(rover_server.latest_heading))


def safety_override_triggered():
    """Check the bump switch and IR sensor; return which one fired, or "none"."""
    if not bump_switch.value:  # pulled LOW when pressed
        print("SAFETY: bump switch contact")
        return "limit_switch"
    if not ir_sensor.value:  # module drives LOW when it sees an obstacle
        print("SAFETY: IR sensor near-field obstacle")
        return "ir"
    return "none"


print("Full build -- Random Rover starting...")
speed_knob.reset(DRIVE_SPEED)
scan_servo.angle = CENTER_ANGLE
last_scan_time = time.monotonic()

while True:
    rover_server.server.poll()  # answer any pending website request
    rover_server.scan_status["drive_state"] = "driving"
    speed = speed_knob.update()
    print("drive: forward, heading", round(rover_server.latest_heading), "speed", round(speed, 2))
    motor_driver.drive(speed, speed)

    stop_reason = "none"
    while True:
        rover_server.server.poll()
        new_speed = speed_knob.update()  # Stretch 1: knob clicks take effect while driving
        if new_speed != speed:
            speed = new_speed
            motor_driver.drive(speed, speed)
        stop_reason = safety_override_triggered()
        if stop_reason != "none":
            rover_server.scan_status["drive_state"] = "stopped"
            motor_driver.stop()
            print("drive: emergency stop-and-reverse (safety override)")
            motor_driver.drive(-speed, -speed)
            wait(BACKOFF_S)  # back off enough to clear whatever triggered it
            motor_driver.stop()
            break
        distance = read_distance()
        tft_status.show(distance, rover_server.latest_heading, speed)  # Stretch 3
        if distance is not None and distance < STOP_DISTANCE_CM:
            print("drive: obstacle close, distance_cm", distance)
            stop_reason = "ultrasonic"
            break
        if time.monotonic() - last_scan_time >= SCAN_INTERVAL:
            break
        wait(0.05)

    rover_server.scan_status["stop_reason"] = stop_reason
    rover_server.scan_status["drive_state"] = "scanning"
    motor_driver.stop()
    print("drive: stopped for scan" if stop_reason == "none" else "drive: emergency stop for scan")
    best_angle = scan()
    rover_server.scan_status["scan_heading"] = best_angle
    turn_toward(best_angle)
    last_scan_time = time.monotonic()
