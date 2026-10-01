# wheel_odometry.py -- wheel-speed odometry via slot IR optocouplers.
import time
import board
import digitalio
from adafruit_debouncer import Debouncer
import motor_driver

WHEEL_DIAMETER_MM = 67
SLOTS_PER_REV = 20  # count your own wheel's encoder disc slots by hand and set this
SAMPLE_SECONDS = 0.25
CALLBACK_SECONDS = 0.02
WHEEL_CIRCUMFERENCE_CM = (WHEEL_DIAMETER_MM / 10) * 3.14159
WHEEL_CIRCUMFERENCE_PER_SLOT = WHEEL_CIRCUMFERENCE_CM / SLOTS_PER_REV
CMS_PER_TICK = WHEEL_CIRCUMFERENCE_PER_SLOT / SAMPLE_SECONDS   # cm/s of speed per counted tick

sensor_a = digitalio.DigitalInOut(board.GP19)
sensor_a.direction = digitalio.Direction.INPUT
sensor_b = digitalio.DigitalInOut(board.GP17)
sensor_b.direction = digitalio.Direction.INPUT

debounced_a = Debouncer(sensor_a)
debounced_b = Debouncer(sensor_b)


def _ticks_to_cms(ticks):
    revolutions = ticks / SLOTS_PER_REV
    return (revolutions * WHEEL_CIRCUMFERENCE_CM) / SAMPLE_SECONDS


def read_speed(while_sampling=None):
    ticks_a = 0
    ticks_b = 0
    end_time = time.monotonic() + SAMPLE_SECONDS
    next_callback = time.monotonic()
    while time.monotonic() < end_time:
        debounced_a.update()
        debounced_b.update()
        if debounced_a.fell:
            ticks_a += 1
        if debounced_b.fell:
            ticks_b += 1
        if while_sampling is not None and time.monotonic() >= next_callback:
            while_sampling()  # optional -- used by Class 4's rover_server.py
            next_callback = time.monotonic() + CALLBACK_SECONDS
    speed_left = _ticks_to_cms(ticks_a)
    speed_right = _ticks_to_cms(ticks_b)
    return (speed_left, motor_driver.last_direction_a,
            speed_right, motor_driver.last_direction_b)
