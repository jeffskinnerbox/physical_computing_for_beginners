# motor_check.py -- deploy with `uv run deploy.py tool motor_check` (runs as code.py);
# put the rover back with `uv run deploy.py restore` when done. Tuning Step 5.
# Steps the throttle up to find the stall points, then does timed runs to measure speed.
import time
import motor_driver

THROTTLES = [0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60]  # never above MAX_THROTTLE
STEP_SECONDS = 0.7         # short bursts, so a stalled motor isn't pushed for long
SPEED_RUN_THROTTLES = [0.5, 0.6]
SPEED_RUN_SECONDS = 2.0

def burst(left, right, seconds):
    motor_driver.drive(left, right)
    time.sleep(seconds)
    motor_driver.stop()
    time.sleep(1.5)        # pause so you can see (and write down) what happened

print("Set the rover on the floor -- starting in 5 s")
time.sleep(5)
print("--- straight: when do the wheels start rolling? ---")
for throttle in THROTTLES:
    print("straight throttle", throttle)
    burst(throttle, throttle, STEP_SECONDS)
print("--- spin in place: when does it start turning? ---")
for throttle in THROTTLES:
    print("spin throttle", throttle)
    burst(throttle, -throttle, STEP_SECONDS)
for throttle in SPEED_RUN_THROTTLES:
    print("--- speed run at", throttle, "-- put the rover on the start line; 8 s ---")
    time.sleep(8)
    burst(throttle, throttle, SPEED_RUN_SECONDS)
    print("measure the distance from the start line now")
print("done")
