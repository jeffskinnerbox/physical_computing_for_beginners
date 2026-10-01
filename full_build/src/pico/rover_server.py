# rover_server.py -- edited again (same file since Class 3, no new filename).
# Class 5 changes: (1) the Mahony filter also fuses the magnetometer (9-DOF),
# so yaw is anchored to magnetic north; (2) a compass heading, published as a
# new "heading" field; (3) library mode -- no loop of its own. code.py calls
# update() to keep the filter running and server.poll() to answer the browser.
import os
import math
import time
import board
import busio
import wifi
import socketpool
import adafruit_lsm9ds1
from adafruit_httpserver import Server, Request, Response, JSONResponse
import wheel_odometry

# Configure your Access Point credentials
ap_ssid = os.getenv("CIRCUITPY_WIFI_AP_SSID")
ap_password = os.getenv("CIRCUITPY_WIFI_AP_PASSWORD")   # Minimum 8 characters (or leave as "" for an open network)

print("Starting Wi-Fi Access Point...")
wifi.radio.start_ap(ssid=ap_ssid, password=ap_password)

# The default IP address for a CircuitPython AP is typically 192.168.4.1
ap_ip = wifi.radio.ipv4_address_ap
print(f"AP Active! Connect to SSID: '{ap_ssid}'")
print(f"Server IP Address: {ap_ip}")

# Set up socket pool and HTTP server
pool = socketpool.SocketPool(wifi.radio)
server = Server(pool)

i2c = busio.I2C(board.GP1, board.GP0)  # SCL, SDA -- same wiring as Class 4
imu = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

MAHONY_KP = 2.0   # unchanged from Class 4
MAHONY_KI = 0.05  # unchanged from Class 4

# Gyro bias settings -- unchanged from Class 4.
CAL_SAMPLES = 200  # startup calibration: about 2 seconds of readings
STILL_GYRO = 0.02  # rad/s: below this on every axis counts as "still"
STILL_ACCEL = 0.3  # m/s^2: total acceleration this close to 1 g counts as "still"
BIAS_ALPHA = 0.01  # while still, move the bias 1% of the way toward each reading
GRAVITY = 9.81     # m/s^2

# Magnetometer calibration -- new in Class 5.
MAG_OFFSET = (0.0, 0.0, 0.0)  # gauss -- paste YOUR line from class-5-mag-calibration.py
MAG_AXIS_SIGN = (-1, 1, 1)    # [VERIFY] same signs that passed the Phase 1 axis check

q0, q1, q2, q3 = 1.0, 0.0, 0.0, 0.0
integral_fbx = integral_fby = integral_fbz = 0.0
last_time = time.monotonic()


def _mahony_update(ax, ay, az, gx, gy, gz, mx, my, mz, dt):
    """Class 4's filter plus a second reference: north from the magnetometer."""
    global q0, q1, q2, q3, integral_fbx, integral_fby, integral_fbz
    norm = (ax * ax + ay * ay + az * az) ** 0.5
    mag_norm = (mx * mx + my * my + mz * mz) ** 0.5
    if norm == 0 or mag_norm == 0:
        return
    ax, ay, az = ax / norm, ay / norm, az / norm
    mx, my, mz = mx / mag_norm, my / mag_norm, mz / mag_norm

    # Where the filter thinks gravity points (unchanged from Class 4).
    vx = 2 * (q1 * q3 - q0 * q2)
    vy = 2 * (q0 * q1 + q2 * q3)
    vz = q0 * q0 - q1 * q1 - q2 * q2 + q3 * q3

    # Turn the measured field into a world-frame "north" (bx) with its downward
    # dip (bz), then work out where that north should appear to the rover (w).
    hx = 2 * (mx * (0.5 - q2 * q2 - q3 * q3) + my * (q1 * q2 - q0 * q3) + mz * (q1 * q3 + q0 * q2))
    hy = 2 * (mx * (q1 * q2 + q0 * q3) + my * (0.5 - q1 * q1 - q3 * q3) + mz * (q2 * q3 - q0 * q1))
    bx = (hx * hx + hy * hy) ** 0.5
    bz = 2 * (mx * (q1 * q3 - q0 * q2) + my * (q2 * q3 + q0 * q1) + mz * (0.5 - q1 * q1 - q2 * q2))
    wx = 2 * (bx * (0.5 - q2 * q2 - q3 * q3) + bz * (q1 * q3 - q0 * q2))
    wy = 2 * (bx * (q1 * q2 - q0 * q3) + bz * (q0 * q1 + q2 * q3))
    wz = 2 * (bx * (q0 * q2 + q1 * q3) + bz * (0.5 - q1 * q1 - q2 * q2))

    # Error = gravity mismatch (Class 4) + north mismatch (new).
    ex = (ay * vz - az * vy) + (my * wz - mz * wy)
    ey = (az * vx - ax * vz) + (mz * wx - mx * wz)
    ez = (ax * vy - ay * vx) + (mx * wy - my * wx)

    # From here down: identical to Class 4.
    integral_fbx += MAHONY_KI * ex * dt
    integral_fby += MAHONY_KI * ey * dt
    integral_fbz += MAHONY_KI * ez * dt
    gx += MAHONY_KP * ex + integral_fbx
    gy += MAHONY_KP * ey + integral_fby
    gz += MAHONY_KP * ez + integral_fbz
    qa, qb, qc = q0, q1, q2
    q0 += (-qb * gx - qc * gy - q3 * gz) * 0.5 * dt
    q1 += (qa * gx + qc * gz - q3 * gy) * 0.5 * dt
    q2 += (qa * gy - qb * gz + q3 * gx) * 0.5 * dt
    q3 += (qa * gz + qb * gy - qc * gx) * 0.5 * dt
    norm = (q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3) ** 0.5
    q0, q1, q2, q3 = q0 / norm, q1 / norm, q2 / norm, q3 / norm


def _calibrate_gyro_bias():
    """Unchanged from Class 4: average the gyro while the rover sits still."""
    print("Calibrating gyro -- keep the rover perfectly still...")
    sum_x = sum_y = sum_z = 0.0
    for _ in range(CAL_SAMPLES):
        gx, gy, gz = imu.gyro  # already radians/sec
        sum_x += gx
        sum_y += gy
        sum_z += gz
        time.sleep(0.01)
    return sum_x / CAL_SAMPLES, sum_y / CAL_SAMPLES, sum_z / CAL_SAMPLES


def _is_still(ax, ay, az, gx, gy, gz):
    """Unchanged from Class 4: tiny rotation AND only gravity on the accelerometer."""
    accel_mag = (ax * ax + ay * ay + az * az) ** 0.5
    return (
        abs(gx) < STILL_GYRO
        and abs(gy) < STILL_GYRO
        and abs(gz) < STILL_GYRO
        and abs(accel_mag - GRAVITY) < STILL_ACCEL
    )


def _read_magnetometer():
    """Calibrated magnetometer reading, axes lined up with the accel/gyro."""
    return tuple(sign * (raw - off)
                 for raw, off, sign in zip(imu.magnetic, MAG_OFFSET, MAG_AXIS_SIGN))


def _start_at_compass_heading():
    """Start the filter already facing the way the compass says. From (1, 0, 0, 0)
    the filter would need 30+ seconds to swing around onto north by itself.
    Assumes the rover boots sitting flat."""
    global q0, q1, q2, q3
    mx, my, _ = _read_magnetometer()
    yaw = math.atan2(-my, mx)
    q0, q1, q2, q3 = math.cos(yaw / 2), 0.0, 0.0, math.sin(yaw / 2)


def _read_orientation():
    """Advance the Mahony filter one step and return (roll, pitch, yaw)."""
    global last_time, bias_x, bias_y, bias_z
    global integral_fbx, integral_fby, integral_fbz
    now = time.monotonic()
    dt = now - last_time
    last_time = now
    ax, ay, az = imu.acceleration
    gx, gy, gz = imu.gyro  # already radians/sec
    gx, gy, gz = gx - bias_x, gy - bias_y, gz - bias_z  # remove the gyro bias
    mx, my, mz = _read_magnetometer()                    # new in Class 5
    if _is_still(ax, ay, az, gx, gy, gz):  # still: leftover reading is bias -- refine it
        bias_x += BIAS_ALPHA * gx
        bias_y += BIAS_ALPHA * gy
        bias_z += BIAS_ALPHA * gz
        integral_fbx = integral_fby = integral_fbz = 0.0  # clear integral windup
    _mahony_update(ax, ay, az, gx, gy, gz, mx, my, mz, dt)
    roll = math.degrees(math.atan2(2 * (q0 * q1 + q2 * q3), 1 - 2 * (q1 * q1 + q2 * q2)))
    pitch = math.degrees(math.asin(max(-1.0, min(1.0, 2 * (q0 * q2 - q3 * q1)))))
    yaw = math.degrees(math.atan2(2 * (q0 * q3 + q1 * q2), 1 - 2 * (q2 * q2 + q3 * q3)))
    return roll, pitch, yaw


# At startup the rover must sit still (gyro bias) AND flat (compass heading).
bias_x, bias_y, bias_z = _calibrate_gyro_bias()
_start_at_compass_heading()
last_time = time.monotonic()

latest_orientation = (0.0, 0.0, 0.0)
latest_heading = 0.0  # compass degrees: 0 = magnetic north, increasing clockwise

# The collision-avoidance decision -- code.py fills these in each cycle.
scan_status = {
    "scan_heading": 90,        # last chosen SCAN angle (servo degrees, 90 = straight ahead)
    "drive_state": "driving",  # "driving" | "scanning" | "stopped"
    "stop_reason": "none",     # "none" | "ultrasonic" | "ir" | "limit_switch"
}


def _update_orientation():
    """Advance the filter one step and remember the results for /data.json."""
    global latest_orientation, latest_heading
    latest_orientation = _read_orientation()
    # yaw grows counter-clockwise; a compass grows clockwise -- flip and wrap to 0-360.
    latest_heading = (-latest_orientation[2]) % 360


def update():
    """One filter step. Class 4's own loop did this every 20 ms; that loop is
    gone, so code.py calls update() instead (through its wait() helper)."""
    _update_orientation()


STATUS_PAGE = """<!doctype html><html><body>
<h1>Rover Status</h1>
<pre id="data">loading...</pre>
<script>
setInterval(() => fetch('/data.json').then(r => r.json())
    .then(d => document.getElementById('data').textContent =
        JSON.stringify(d, null, 2)), 500);
</script>
</body></html>"""


@server.route("/data.json")
def data_json(request: Request):
    # read_speed() spends 0.25 s counting wheel ticks; passing the filter update
    # keeps orientation tracking running during that window instead of pausing it.
    speed_left, dir_left, speed_right, dir_right = wheel_odometry.read_speed(
        while_sampling=_update_orientation)
    roll, pitch, yaw = latest_orientation
    return JSONResponse(request, {
        "speed_left_cms": speed_left,
        "dir_left": dir_left,
        "speed_right_cms": speed_right,
        "dir_right": dir_right,
        "roll": roll,
        "pitch": pitch,
        "yaw": yaw,
        "heading": latest_heading,
        "scan_heading": scan_status["scan_heading"],
        "drive_state": scan_status["drive_state"],
        "stop_reason": scan_status["stop_reason"],
    })


@server.route("/")
def index(request: Request):
    return Response(request, STATUS_PAGE, content_type="text/html")


# Port 5000, not 80 -- CircuitPython's Web Workflow may already be using port 80.
server.start(str(ap_ip), port=5000)
print(f"HTTP Server running at http://{ap_ip}:5000")
# No "while True: server.poll()" loop here anymore -- code.py's own main loop
# calls server.poll() and update(), so it can keep driving at the same time.
