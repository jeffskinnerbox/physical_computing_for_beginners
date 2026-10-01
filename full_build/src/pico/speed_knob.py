# speed_knob.py -- full build: Class 6 Stretch 1 (class-6-code-1.py) as a library.
# The Class 1 KY-040 encoder on GP3/GP4 sets the rover's drive speed live.
# rotaryio counts the encoder's clicks in hardware, in the background, so no
# click is lost while code.py is busy scanning, turning, or answering the
# website -- the hardware version of Class 1's debouncing idea.
import board
import rotaryio
import motor_driver

MIN_SPEED = 0.3   # keep above your straight-drive stall point (tuning Step 10)
MAX_SPEED = 0.9   # Class 6 placeholder -- clamped to motor_driver.MAX_THROTTLE below
SPEED_STEP = 0.05

# Speeds above MAX_THROTTLE do nothing (motor_driver clamps them), so the knob
# stops at whichever limit is lower -- no dead clicks at the top of the range.
TOP_SPEED = min(MAX_SPEED, motor_driver.MAX_THROTTLE)

# Clockwise = faster. If yours runs backwards, swap board.GP3 and board.GP4 here.
# If it takes two clicks per speed step, add divisor=2 (some KY-040s give fewer
# pulses per click). The device test tells you which you need.
_encoder = rotaryio.IncrementalEncoder(board.GP3, board.GP4)  # CLK, DT -- Class 1 wiring
_last_position = _encoder.position
current_speed = TOP_SPEED


def reset(speed):
    """Start from code.py's DRIVE_SPEED. Not clamped to MIN_SPEED, so
    DRIVE_SPEED = 0 (tuning Step 7) still means 'don't drive' until the knob turns."""
    global current_speed
    current_speed = min(speed, TOP_SPEED)


def update():
    """Apply any knob clicks since the last call and return current_speed."""
    global current_speed, _last_position
    position = _encoder.position
    clicks = position - _last_position
    if clicks:
        _last_position = position
        current_speed = max(MIN_SPEED, min(TOP_SPEED, current_speed + clicks * SPEED_STEP))
        print("knob: current_speed", round(current_speed, 2))
    return current_speed
