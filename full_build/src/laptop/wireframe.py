#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
# wireframe.py -- full build: Class 4's 3D viewer (class-4-phase-2-wireframe.py), reworked
# as a TEST TOOL for the finished rover. Runs on your LAPTOP, not the Pico.
# Instead of reading CSV over USB serial (the finished rover never prints CSV), it
# joins nothing itself -- YOU join the rover's WiFi network -- then polls the rover
# website's /data.json and draws a 3D box that follows roll/pitch/yaw, with the
# compass heading in the title. No change to the rover's code is needed.
#   uv run wireframe.py                      (uses http://192.168.4.1:5000)
#   uv run wireframe.py http://192.168.4.1:5000
# Put the rover on its stand: each request pauses the rover's drive loop ~0.25 s.

import json
import signal
import sys
import time
import urllib.request

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 -- needed to enable 3D projection

ROVER_URL = (sys.argv[1] if len(sys.argv) > 1 else "http://192.168.4.1:5000").rstrip("/")
POLL_SECONDS = 0.5  # same rate as the rover's own status page -- don't go faster
STARTUP_WAIT_S = 10  # a scan or turn silences the rover ~4 s -- wait past that


def read_rover():
    """Return the rover's /data.json as a dict, or None if it didn't answer."""
    try:
        with urllib.request.urlopen(ROVER_URL + "/data.json", timeout=2) as reply:
            return json.load(reply)
    except (OSError, ValueError):
        return None


def wait_for_rover():
    """Keep trying read_rover() for up to STARTUP_WAIT_S seconds; True once it answers."""
    deadline = time.monotonic() + STARTUP_WAIT_S
    while time.monotonic() < deadline:
        if read_rover() is not None:
            return True
        time.sleep(POLL_SECONDS)
    return False


print(f"Waiting up to {STARTUP_WAIT_S} s for the rover at {ROVER_URL}...")
if not wait_for_rover():
    sys.exit(
        f"Couldn't reach {ROVER_URL}/data.json for {STARTUP_WAIT_S} seconds.\n"
        "Is your laptop joined to the rover's WiFi network, and is the rover's code running?"
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

print("Full build -- 3D box test tool starting, reading from", ROVER_URL)
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
    # Let the window handle events (redraw, resize, close) every pass --
    # even when no data arrived -- so it never freezes as "Not Responding".
    fig.canvas.flush_events()

    d = read_rover()
    if d is None:
        ax.set_title("no answer from the rover -- still on its WiFi?")
        fig.canvas.draw_idle()
        plt.pause(POLL_SECONDS)
        continue
    roll, pitch, yaw = d["roll"], d["pitch"], d["yaw"]

    rotated = box_vertices @ rotation_matrix(roll, pitch, yaw).T

    for edge_line, (a, b) in zip(edge_lines, edges):
        pts = rotated[[a, b]]
        edge_line.set_data_3d(pts[:, 0], pts[:, 1], pts[:, 2])
    front_label.set_position_3d(rotated[FRONT_FACE].mean(axis=0))
    right_label.set_position_3d(rotated[RIGHT_FACE].mean(axis=0))
    ax.set_title(f"roll={roll:.0f} pitch={pitch:.0f} yaw={yaw:.0f} heading={d['heading']:.0f}")

    # Ask for a redraw; the flush_events() at the top of the loop does it.
    fig.canvas.draw_idle()
    plt.pause(POLL_SECONDS)  # wait between requests, keeping the window responsive

print("Stopped.")
