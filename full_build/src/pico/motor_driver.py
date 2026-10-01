# motor_driver.py -- DRV8833 motor driver library.
import board
import pwmio
from adafruit_motor import motor

MAX_THROTTLE = 0.6  # calibrate per robot

pwm_ain1 = pwmio.PWMOut(board.GP9, frequency=50)
pwm_ain2 = pwmio.PWMOut(board.GP10, frequency=50)
pwm_bin1 = pwmio.PWMOut(board.GP11, frequency=50)
pwm_bin2 = pwmio.PWMOut(board.GP12, frequency=50)

motor_a = motor.DCMotor(pwm_ain1, pwm_ain2)
motor_b = motor.DCMotor(pwm_bin1, pwm_bin2)

last_direction_a = 0
last_direction_b = 0


def _clamp(throttle):
    if throttle is None:
        return None
    return max(-MAX_THROTTLE, min(MAX_THROTTLE, throttle))


def _sign(throttle):
    if not throttle:
        return 0
    return 1 if throttle > 0 else -1


def drive(left, right):
    global last_direction_a, last_direction_b
    motor_a.throttle = _clamp(left)
    motor_b.throttle = _clamp(right)
    last_direction_a = _sign(left)
    last_direction_b = _sign(right)


def stop():
    global last_direction_a, last_direction_b
    motor_a.throttle = 0.0
    motor_b.throttle = 0.0
    last_direction_a = 0
    last_direction_b = 0
