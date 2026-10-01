# servo_check.py -- deploy with `uv run deploy.py tool servo_check` (runs as code.py);
# put the rover back with `uv run deploy.py restore` when done. Tuning Step 3.
# Points the scan servo at the rover's own scan range so you can check its aim.
import time
import board
import pwmio
from adafruit_motor import servo

MIN_PULSE = 500    # copy the values from your code.py servo.Servo(...) line
MAX_PULSE = 2500
CHECK_ANGLES = [90, 30, 90, 150]  # only the rover's range -- no need to push to 0 or 180

pwm = pwmio.PWMOut(board.GP8, duty_cycle=0, frequency=50)
scan_servo = servo.Servo(pwm, min_pulse=MIN_PULSE, max_pulse=MAX_PULSE)

while True:
    for angle in CHECK_ANGLES:
        scan_servo.angle = angle
        print("servo at", angle)
        time.sleep(3)
