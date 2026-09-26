# class-4-phase-2-wireframe.py -- save as wireframe.py on laptop and execute there, not the pico mcu
# Phase 2: runs on your LAPTOP, not the Pico. Reads roll,pitch,yaw CSV over
# serial from class-4-phase-1-code.py or class-4-phase-3-code.py and draws a live-updating 3D box.
# Windows usage: python wireframe.py <port>     (e.g. python wireframe.py COM5)
# Linux usage:   python wireframe.py <device>   (e.g. python wireframe.py /dev/ttyACM0)

import sys
import serial
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 -- needed to enable 3D projection

# Pass your board's serial port as a command-line argument, e.g. COM5.
# Find it in Mu/Thonny's device list or Windows Device Manager.
PORT = sys.argv[1] if len(sys.argv) > 1 else "COM5"
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=1)

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

while True:
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
    ax.set_title("roll={:.0f} pitch={:.0f} yaw={:.0f}".format(roll, pitch, yaw))
    # Redraw the window and let it handle events (resize, close, etc.).
    fig.canvas.draw_idle()
    fig.canvas.flush_events()
