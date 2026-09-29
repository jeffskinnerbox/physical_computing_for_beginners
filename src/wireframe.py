#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib", "pyserial"]
# ///
# class-4-phase-2-wireframe.py -- save as wireframe.py on laptop and execute there, not the pico mcu
# Phase 2: runs on your LAPTOP, not the Pico. Reads roll,pitch,yaw CSV over
# serial from class-4-phase-1-code.py or class-4-phase-3-code.py and draws a live-updating 3D box.
# The block above tells `uv` which Python and packages to use, so no pip or venv needed:
#   uv run wireframe.py          (finds the Pico's serial port by itself)
#   uv run wireframe.py COM5     (or name the port: COM5 on Windows, /dev/ttyACM0 on Linux)

import signal
import sys

import matplotlib.pyplot as plt
import numpy as np
import serial
import serial.tools.list_ports
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 -- needed to enable 3D projection

BAUD = 115200

# USB vendor IDs a CircuitPython Pico shows up with: Adafruit (who
# maintains CircuitPython) and Raspberry Pi.
PICO_VENDOR_IDS = {0x239A, 0x2E8A}


def find_pico_port():
    """Return the serial port of the first plugged-in CircuitPython board, or None."""
    ports = sorted(
        (p for p in serial.tools.list_ports.comports() if p.vid in PICO_VENDOR_IDS),
        key=lambda p: p.device,
    )
    return ports[0].device if ports else None


# Use the port named on the command line, or go find the Pico ourselves.
PORT = sys.argv[1] if len(sys.argv) > 1 else find_pico_port()
if PORT is None:
    sys.exit(
        "Couldn't find a Pico. Check the USB cable, or name the port yourself:\n"
        "    uv run wireframe.py COM5"
    )

try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
except serial.SerialException as err:
    # Most common cause: Thonny is still connected to the board.
    sys.exit(
        f"Couldn't open {PORT}: {err}\n"
        "Is Thonny still connected? Click Stop, then Run > Disconnect, and try again."
    )

# The 8 corners of a simple rectangular box, and which corners connect
# to which to draw its 12 edges.
box_vertices = np.array(
    [
        [-1, -0.5, -0.2],
        [1, -0.5, -0.2],
        [1, 0.5, -0.2],
        [-1, 0.5, -0.2],
        [-1, -0.5, 0.2],
        [1, -0.5, 0.2],
        [1, 0.5, 0.2],
        [-1, 0.5, 0.2],
    ]
)
edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7),
]

# The 4 corners of the small +X end of the box -- the "front", pointing
# along the IMU's X (roll) axis.
FRONT_FACE = [1, 2, 6, 5]

# The 4 corners of the -Y long side. With X pointing forward and Z up,
# +Y points LEFT (right-hand rule), so -Y is the box's "right" side.
RIGHT_FACE = [0, 1, 5, 4]


def rotation_matrix(roll, pitch, yaw):
    """Build a combined 3D rotation matrix from roll/pitch/yaw degrees."""
    # Roll is negated so the on-screen box rolls the same way as the physical
    # board (display-only fix -- the Pico's roll value itself is unchanged).
    r, p, y = np.radians([-roll, pitch, yaw])
    rx = np.array([[1, 0, 0], [0, np.cos(r), -np.sin(r)], [0, np.sin(r), np.cos(r)]])
    ry = np.array([[np.cos(p), 0, np.sin(p)], [0, 1, 0], [-np.sin(p), 0, np.cos(p)]])
    rz = np.array([[np.cos(y), -np.sin(y), 0], [np.sin(y), np.cos(y), 0], [0, 0, 1]])
    return rz @ ry @ rx


plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(-2, 2)

# Label each plot axis with the IMU axis it stands for, and the rotation
# measured around it: roll spins around X, pitch around Y, yaw around Z.
ax.set_xlabel("X  (roll axis)")
ax.set_ylabel("Y  (pitch axis)")
ax.set_zlabel("Z  (yaw axis)")

# Create the 12 edge lines ONCE, then just move them every frame -- much
# faster than clearing the plot and drawing brand-new lines each time.
edge_lines = [ax.plot([], [], [], color="C0")[0] for _ in edges]

# Red "Front" and "Right" labels, created once and moved to the center of
# their faces every frame so you can always tell which way the box is facing.
front_label = ax.text(0, 0, 0, "Front", color="red", ha="center", va="center")
right_label = ax.text(0, 0, 0, "Right", color="red", ha="center", va="center")
plt.show(block=False)

print("Class 4, Phase 2 -- 3D box display starting, reading from", PORT)
print("Close the window or press Ctrl-C to stop.")

# Ctrl-C normally raises an error that matplotlib's window can swallow.
# Instead, just raise a flag the loop checks, so the program stops cleanly.
running = True


def stop(*_):
    global running
    running = False


signal.signal(signal.SIGINT, stop)

# Keep going until Ctrl-C or the window is closed.
while running and plt.fignum_exists(fig.number):
    # The Pico sends lines faster than we can draw them. Read everything
    # already waiting and keep only the NEWEST line, so the box shows where
    # the board is now -- not where it was several seconds ago.
    raw = ser.readline()
    while ser.in_waiting:
        raw = ser.readline()
    line = raw.decode("utf-8", errors="ignore").strip()
    if not line:
        continue
    try:
        roll, pitch, yaw = [float(v) for v in line.split(",")]
    except ValueError:
        # Skip any partial/garbled line rather than crashing the display.
        continue

    rotated = box_vertices @ rotation_matrix(roll, pitch, yaw).T

    for edge_line, (a, b) in zip(edge_lines, edges):
        pts = rotated[[a, b]]
        edge_line.set_data_3d(pts[:, 0], pts[:, 1], pts[:, 2])
    front_label.set_position_3d(rotated[FRONT_FACE].mean(axis=0))
    right_label.set_position_3d(rotated[RIGHT_FACE].mean(axis=0))
    ax.set_title(f"roll={roll:.0f} pitch={pitch:.0f} yaw={yaw:.0f}")

    # Redraw the window and let it handle events (resize, close, etc.).
    fig.canvas.draw_idle()
    fig.canvas.flush_events()

# Let go of the serial port so Thonny can reconnect to the Pico right away.
ser.close()
print("Stopped -- serial port closed.")
