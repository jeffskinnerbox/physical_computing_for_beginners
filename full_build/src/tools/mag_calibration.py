# mag_calibration.py (class-5-mag-calibration.py) -- deploy with `uv run deploy.py tool mag_calibration`
# (runs as code.py), run ONCE on the fully assembled rover; `uv run deploy.py restore` afterward.
# Finds the rover's own magnetic offset (hard-iron calibration), then prints
# corrected readings so you can check the magnetometer's axis directions.
import time
import board
import busio
import adafruit_lsm9ds1

CAL_SECONDS = 30               # how long to turn and tumble the rover
MAG_AXIS_SIGN = (-1, 1, 1)     # [VERIFY] LSM9DS1 mag X axis points opposite the accel/gyro X axis

i2c = busio.I2C(board.GP1, board.GP0)  # SCL, SDA -- same wiring as Class 4
imu = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

lows = [float("inf")] * 3
highs = [float("-inf")] * 3

print("Magnetometer calibration starts in 3 s -- pick up the rover.")
time.sleep(3)
print("GO: slowly turn and tumble the rover through every orientation for", CAL_SECONDS, "s")
end_time = time.monotonic() + CAL_SECONDS
while time.monotonic() < end_time:
    for axis, value in enumerate(imu.magnetic):  # gauss
        lows[axis] = min(lows[axis], value)
        highs[axis] = max(highs[axis], value)
    time.sleep(0.02)

# The center of each axis's swing is the rover's own magnetic offset.
offset = tuple(round((low + high) / 2, 3) for low, high in zip(lows, highs))
spans = tuple(round(high - low, 3) for low, high in zip(lows, highs))
print("Done. Copy this line into rover_server.py:")
print("MAG_OFFSET =", offset)
print("Spans (gauss) -- should be roughly equal:", spans)

print("Axis check: corrected mx, my, mz every half second (Ctrl-C to stop)")
while True:
    corrected = [sign * (raw - off)
                 for raw, off, sign in zip(imu.magnetic, offset, MAG_AXIS_SIGN)]
    print("mx {:+.2f}  my {:+.2f}  mz {:+.2f}".format(*corrected))
    time.sleep(0.5)
