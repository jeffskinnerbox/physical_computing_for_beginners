# Random Rover Tuning Log Template
This is the tuning log from [Strategy for Tuning and Calibrating the Random Rover][01].
The **Step**, **Parameter**, and **Old value** columns are already filled in, in the
order you'll work through them, with the starting values from the lesson scripts.
You fill in the rest as you go.

How to use it:

* Add one row **every time you change a number**. If you try `TURN_SPEED` three times, that's
  three rows. Copy the row, then set its **Old value** to the last **New Value** you tried.
* **Test** is what you ran (for example, `[150]` turn test or stopping test, browser closed).
* **Result (3 runs)** is what you measured, three times (for example, `+3, +4, +2`).
* **Keep?** is `yes` or `no`. If it's `no`, put the old value back before your next test.
* For rows that record a measurement rather than a setting (battery volts, stall points, speed),
  put the measured number in **New Value**.
* If your own **Old value** differs from what's printed (because you already changed it in class),
  cross it out and write yours.


## Session A — Steps 0 to 5

| Step | Parameter | Old value | New Value | Test | Result (3 runs) | Keep? |
| :--- | :-------- | :-------- | :-------- | :--- | :-------------- | :---- |
| 1 | 9V battery voltage, at rest (measured) | — | | | | |
| 1 | `VSYS` voltage, at rest (measured) | 5 V | | | | |
| 1 | `VSYS` voltage, motors spinning (measured) | 5 V | | | | |
| 1 | Buck converter trimpot (only if adjustable) | 5 V | | | | |
| 3 | `CENTER_ANGLE` | `90` | | | | |
| 3 | `min_pulse` | `500` | | | | |
| 3 | `max_pulse` | `2500` | | | | |
| 4 | `MAG_OFFSET` | `(0.0, 0.0, 0.0)` | | | | |
| 4 | `MAG_AXIS_SIGN` | `(-1, 1, 1)` | | | | |
| 4 | Heading jump at motor start (measured) | — | | | | |
| 5 | `MAX_THROTTLE` | `0.6` | | | | |
| 5 | Straight stall point (measured) | — | | | | |
| 5 | Spin stall point (measured) | — | | | | |
| 5 | Speed at throttle 0.5, cm/s (measured) | — | | | | |
| 5 | Speed at throttle 0.6, cm/s (measured) | — | | | | |


## Session B — Steps 6 to 11

| Step | Parameter | Old value | New Value | Test | Result (3 runs) | Keep? |
| :--- | :-------- | :-------- | :-------- | :--- | :-------------- | :---- |
| 6 | `DRIVE_SPEED` (provisional) | `0.6` | | | | |
| 6 | `TURN_SPEED` | `0.45` | | | | |
| 6 | `HEADING_TOLERANCE_DEG` | `5` | | | | |
| 6 | `TURN_TIMEOUT_S` | `3.0` | | | | |
| 7 | `SETTLE_TIME` | `0.15` | | | | |
| 7 | `SCAN_ANGLES` | `[30, 60, 90, 120, 150]` | | | | |
| 8 | `DRIVE_SPEED` | `0.6` | | | | |
| 8 | Stretch 2 chart refresh, `setTimeout(pollHistory, ...)` (only if Stretch 2 is installed) | `200` | | | | |
| 8 | Status page refresh, `setInterval(..., ...)` | `500` | | | | |
| 8 | `STOP_DISTANCE_CM` | `25` | | | | |
| 8 | `SCAN_INTERVAL` | `3.0` | | | | |
| 9 | IR sensor trimmer, trigger distance in cm (measured) | — | | | | |
| 9 | `BACKOFF_S` | `0.3` | | | | |
| 10 | Stretch 1 `MIN_SPEED` | `0.3` | | | | |
| 10 | Stretch 1 `MAX_SPEED` | `0.9` | | | | |
| 10 | Stretch 1 `SPEED_STEP` | `0.05` | | | | |
| 10 | Stretch 3 `REFRESH_S` | `0.2` | | | | |
| 11 | 5-minute arena run (bumps / rescues / missed turns / stuck) | — | | | | |


## Extra rows

Use these for retries, or when you revisit a step after a battery swap or a new floor.

| Step | Parameter | Old value | New Value | Test | Result (3 runs) | Keep? |
| :--- | :-------- | :-------- | :-------- | :--- | :-------------- | :---- |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |


[01]:../../explainers/strategy-for-tuning-calibration-random-rover.md
