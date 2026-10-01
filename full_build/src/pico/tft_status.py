# tft_status.py -- full build: Class 6 Stretch 3 (class-6-code-3.py) as a library.
# ST7789 1.14" TFT over SPI showing the rover's REAL distance, heading, and speed.
# code.py calls show() as often as it likes; the screen only redraws every
# REFRESH_S seconds, because redrawing is much slower than a filter step.
import time
import board
import busio
import displayio
import terminalio
from fourwire import FourWire
from adafruit_st7789 import ST7789
from adafruit_display_text import label

REFRESH_S = 0.2  # redraw the screen 5 times a second

# Always release any previously-active display before creating a new one --
# skipping this is the most common cause of a blank/garbled screen.
displayio.release_displays()

spi = busio.SPI(clock=board.GP26, MOSI=board.GP27)  # second SPI bus -- GP19 is the odometry sensor
display_bus = FourWire(spi, command=board.GP21, chip_select=board.GP20, reset=board.GP22)
# rowstart/colstart shift drawing onto the visible glass -- see the Pre-Class TFT homework note
display = ST7789(display_bus, width=240, height=135, rotation=270, rowstart=40, colstart=53)

group = displayio.Group()
distance_label = label.Label(terminalio.FONT, text="dist: -- cm", x=10, y=20, scale=2)
heading_label = label.Label(terminalio.FONT, text="head: -- deg", x=10, y=55, scale=2)
speed_label = label.Label(terminalio.FONT, text="speed: --", x=10, y=90, scale=2)
group.append(distance_label)
group.append(heading_label)
group.append(speed_label)
display.root_group = group

_last_refresh = 0.0


def show(distance_cm, heading, speed):
    """Update the three lines, at most once every REFRESH_S seconds.
    distance_cm may be None (the sensor missed its echo)."""
    global _last_refresh
    now = time.monotonic()
    if now - _last_refresh < REFRESH_S:
        return
    _last_refresh = now
    distance_label.text = "dist: -- cm" if distance_cm is None else "dist: {:.0f} cm".format(distance_cm)
    heading_label.text = "head: {:.0f} deg".format(heading)
    speed_label.text = "speed: {:.2f}".format(speed)
