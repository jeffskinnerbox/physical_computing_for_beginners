# Physical Computing for Beginners — Bill of Materials

This is the complete Bill of Materials (BOM) for the "Physical Computing for Beginners" course: a
7-session series (1 Pre-Class + 6 Classes) that builds up to an autonomous obstacle-avoiding robot
car (the "Random Rover"), running on a Raspberry Pi Pico 2 W with CircuitPython.

This document is the **single source of truth** for everything the course needs to buy, borrow, or
install — what it costs, where it comes from, and who pays for it. The course syllabus and lesson
plans reference component names but never prices; all cost and sourcing information lives here.
Whoever is financing the class should be able to read this document alone and understand the full
budget picture, with no need to cross-reference the syllabus or lesson plans.

**Assumed class size: 9 people (8 students + 1 instructor).** The instructor keeps a full kit and
builds a rover alongside the students, so all per-person hardware quantities below include the
instructor. All math is shown so the numbers can be recalculated for a different class size.

**Grand Total: $783.97 for the course (~$87.11 per person, 9 people)** — see the Cost Summary below
for the full breakdown.

Adafruit prices in this document were confirmed against the live product pages. Amazon-sourced
prices could not be confirmed the same way (Amazon does not expose price in a non-interactive page
fetch) — reconfirm those before ordering, and treat the two shipping line items as estimates that
should be replaced with real numbers once an order is built in each vendor's cart.

----

## Hardware

### Per-Student Required

Each of the 9 people (8 students + instructor) keeps one of everything in this table — this is the
hardware that goes home with each person at the end of the course. Several items are sold in
multi-packs; the "Item Cost" column is the *effective per-unit cost* for readability, with the
actual pack purchase (and any spares that come with it) noted in the table and priced exactly in
the Cost Summary below.

| Item | Quantity | Item Cost | Source | Notes |
| :-----: | :-----: | :-----: | :-----: | :--------: |
| Raspberry Pi Pico 2W with Header | 1 | $8.00 | [Adafruit][01] | microcontroller, used every class starting Pre-Class |
| JST PH 2mm 4-Pin to Male Header Cable - I2C STEMMA Cable - 200mm | 2 | $1.50 | [Adafruit][14] | I2C wiring, Class 4 onward |
| JST PH 2mm 4-Pin to Female Socket Cable - I2C STEMMA Cable - 200mm | 2 | $1.50 | [Adafruit][15] | I2C wiring, Class 4 onward |
| DRV8833 DC/Stepper Motor Driver Breakout Board | 1 | $5.95 | [Adafruit][05] | Class 3 motor driver, reused Class 5-6 |
| IMU 9-DOF LSM9DS1 Breakout Board (STEMMA) | 1 | $19.95 | [Adafruit][06] | Class 4 IMU, reused Class 6 stretch #2 |
| STEMMA QT / Qwiic JST SH 4-pin Cable, 100mm | 3 | $0.95 | [Adafruit][07] | I2C connections for the LSM9DS1 (Class 4 onward) |
| 1.14" 240x135 Color Newxie TFT Display | 1 | $9.95 | [Adafruit][09] | Class 6 stretch #3 status display |
| Emo Smart Robot Car Chassis Kit | 1 | $13.99 | [Amazon][02] | 2 DC gearbox motors + wheels; assembled across Classes 1-2, driven starting Class 3 |
| HC-SR04 Ultrasonic Distance Sensor | 1 | $1.30 | [Amazon][03] | sold in 10-pack ($12.99); Class 2 sensor, reused Class 5-6 |
| SG90 9g Micro Servo Motor | 1 | $2.00 | [Amazon][04] | sold in 10-pack ($19.99); Class 2 servo, reused Class 5-6 |
| KY-040 360 Degree Rotary Encoder Module | 1 | $2.89 | [Amazon][08] | sold in 8-packs ($12.99/pack); 9 needed requires 2 packs (16 units, 7 spare) — 1 pack alone is short by 1 |
| Tactile Push Button Switch | 2 | $0.02 | [Amazon][10] | sold in 500-pack ($9.99); Class 1 button + spare |
| Breadboard 830 Point Solderless Prototype PCB Board | 1 | $3.00 | [Amazon][11] | sold in 3-packs ($8.99); one board per person, kept for the whole course |
| I TYPE 9 Volt Battery Clip | 1 | $0.65 | [Amazon][12] | sold in 10-pack ($6.49); Class 3 motor power |
| 9V Alkaline Battery | 1 | $1.59 | [Amazon][13] | sold in 8-packs ($12.69/pack); 9 needed requires 2 packs (16 units, 7 spare) — 1 pack alone is short by 1 |
| 5V Buck Converter Module | 1 | $1.50 | [Amazon][16] | sold in 10-pack ($14.99); onboard 5V power |
| USB A to Micro USB Charging Cable with Data Transfer | 1 | $1.00 | [Amazon][25] | backup for a student whose own cable fails; not the primary supply (see Tools below) |
| Micro Limit Switch | 1 | $0.35 | [Amazon][26] | sold in 20-pack ($6.50); Lever Arm Long 28MM SPDT 3 Pins 3 Terminals Momentary Switch |
| IR Obstacle Avoidance Sensor | 1 | $0.35 | [Amazon][27] | sold in 10-pack ($8.77); 2-30cm detection range, 3.3-5V, for smart car robot and line tracking projects |
| LED (assorted) | 2 | $0.00 | Makersmiths | Class 1 button LED + encoder brightness LED; stocked by the makerspace |
| Resistor (assorted, 220-330Ω for LEDs, ~1k/2k Ω for HC-SR04 voltage divider) | 4 | $0.00 | Makersmiths | Class 1 LED current-limiting + Class 2 HC-SR04 voltage divider; stocked by the makerspace |

Per-Student Required Cost = 8.00 + 13.99 + 1.30 + 2.00 + 5.95 + 19.95 + 3×0.95 + 2.89 + 9.95 + 2×0.02 + 3.00 + 0.65 + 1.59 + 2×1.50 + 2×1.50 + 1.50 + 0 + 0 + 1.00 ≈ **$83.55 per person** (see Cost Summary for the exact bulk-purchase total, which accounts for whole-pack rounding)

### Per-Student Optional

None. All three Class 6 stretch-goal items (rotary encoder speed control, WiFi IMU chart, TFT status
display) are treated as in-scope/required for this course rather than optional add-ons; their
hardware (KY-040, LSM9DS1, TFT) already appears in Per-Student Required above.

### Shared Supplies

Consumables and bulk items used by the whole class, not kept individually by each student.

| Item | Quantity | Item Cost | Source | Notes |
| :-----: | :-----: | :-----: | :-----: | :--------: |
| Dupont Wires - 120pcs 20cm Jumper Wire | 1 | $9.99 | [Amazon][18] | shared jumper wire stock for all classes |
| Invisible Hold Mounting Tape | 1 | $11.99 | [Amazon][19] | mounts the Class 2 HC-SR04 onto the SG90 servo horn and helps with chassis assembly |
| Painter's/Marking Tape + Tape Measure | 1 | $0.00 | Makersmiths | marks the 12" square/circle test tracks, Class 3 onward |

Shared Supplies Cost = 9.99 + 11.99 + 0 = $21.98 total ÷ 9 people ≈ $2.44 per student

### Shipping

| Item | Quantity | Item Cost | Source | Notes |
| :-----: | :-----: | :-----: | :-----: | :--------: |
| Adafruit Shipping | NA | $10.00 [estimated] | NA | flat estimate for the combined Adafruit order (Pico, DRV8833, LSM9DS1, STEMMA/JST cables, TFT) — confirm actual rate/free-shipping threshold before ordering |
| Amazon Shipping | NA | $0.00 [estimated] | NA | assumes Amazon Prime free shipping on all Amazon-sourced items |

Shipping Cost = 10.00 + 0.00 = $10.00 total (assumption — verify both vendors' actual shipping before purchasing)

### Cost Summary

Exact totals from whole-pack/whole-unit purchasing (9 people: 8 students + instructor):

```text
Per-Student Required (bulk-purchase total) = $72.00 (Pico) + $125.91 (chassis) + $12.99 (HC-SR04 10-pack)
    + $19.99 (SG90 10-pack) + $53.55 (DRV8833 ×9) + $179.55 (LSM9DS1 ×9) + $25.65 (STEMMA cable ×27)
    + $25.98 (KY-040, 2× 8-packs) + $89.55 (TFT ×9) + $9.99 (button 500-pack) + $26.97 (breadboard, 3× 3-packs)
    + $6.49 (battery clip 10-pack) + $25.38 (9V battery, 2× 8-packs) + $27.00 (JST male ×18)
    + $27.00 (JST female ×18) + $14.99 (buck converter 10-pack) + $0.00 (LED) + $0.00 (resistor)
    + $9.00 (USB backup cable ×9)
    = $751.99 total (~$83.55 per person)

Shared Supplies = $21.98 total (~$2.44 per person)
Shipping = $10.00 total (~$1.11 per person)

Grand Total = $751.99 + $21.98 + $10.00 = $783.97 for the course (~$87.11 per person, 9 people)
```

----

## Software

All free — no paid software is required anywhere in this course.

| Item | Source | Notes |
| :-----: | :-----: | :--------: |
| CircuitPython Firmware for Pico 2 W | [Firmware Download][20] | flashed onto the Pico in the Pre-Class |
| Mu Editor | [Install Guide][21] | recommended editor, installed in the Pre-Class |
| Thonny | [Setup Guide][22] | alternate editor, installed in the Pre-Class |
| Adafruit CircuitPython Library Bundle | [Download][23] | downloaded in the Pre-Class; supplies `adafruit_debouncer`, `adafruit_hcsr04`, `adafruit_motor`, `adafruit_lsm9ds1`, `adafruit_httpserver`, `adafruit_st7789`, `adafruit_display_text` |
| GitHub account (free) | [GitHub Docs][24] | required so students can access the course repository |
| Python 3 + `pyserial`, `matplotlib`, `numpy` | `pip install pyserial matplotlib numpy` | required on the student's laptop (not the Pico) starting Class 4, to run `class-4-code-2.py`'s live 3D orientation display |
| Modern web browser (Chrome, Firefox, or Edge) | already on any Windows 11 laptop | required starting Class 6 stretch #2, to view the live WiFi chart served by `class-6-code-2.py` |
| Makersmiths classroom/guest WiFi network | facility infrastructure | required starting Class 6 stretch #2, so the Pico W and the student's laptop can both reach the rover's web server |

----

## Code Blocks

Pseudocode/reference implementations provided by the instructor, embedded inline in each class's
lesson plan — no separate cost, but listed here for completeness.

| Item | Quantity | Source | Notes |
| :-----: | :-----: | :-----: | :--------: |
| `class-0-code.py` | 1 | Instructor | blink onboard LED + serial heartbeat, Pre-Class |
| `class-1-code-1.py` / `class-1-code-2.py` | 2 | Instructor | undebounced vs. debounced button + rotary encoder, Class 1 |
| `class-2-code-1.py` / `class-2-code-2.py` / `class-2-code-3.py` | 3 | Instructor | HC-SR04 alone, SG90 alone, combined servo-swept sensor, Class 2 |
| `class-3-code-1.py` / `class-3-code-2.py` | 2 | Instructor | motor driver library + calibrated square/circle test, Class 3 |
| `class-4-code-1.py` / `class-4-code-2.py` | 2 | Instructor | Mahony-filtered IMU orientation (Pico) + live 3D viewer (laptop), Class 4 |
| `class-5-code.py` | 1 | Instructor | Random Rover collision-avoidance logic, Class 5 |
| `class-6-code-1.py` / `class-6-code-2.py` / `class-6-code-3.py` | 3 | Instructor | encoder speed control, WiFi IMU chart, TFT status display — Class 6 stretch goals |

----

## Tools

Equipment needed during the course that is not part of the take-home hardware kit.

| Item | Quantity | Source | Notes |
| :-----: | :-----: | :-----: | :--------: |
| Windows 11 Laptop | 1 | Student | one per student, no sharing; all install guides and the Pre-Class assume Windows 11 specifically |
| USB Cable | 1 | Student | own cable, brought to every class starting with the Pre-Class; course keeps a small spare supply (see Shared Supplies) for a cable that fails, not as the primary source |

----

## Appendix: Considered but Not Selected

These items were evaluated during course planning and removed after iterating on the lesson plans.
Kept here for transparency into the purchasing decisions behind the final BOM — none of these are
part of the course budget above.

| Item Name | Source | Type of Unit | Items per Unit | Total Items Needed | Total Units Needed | Unit Cost | Total Cost |
| :---------- | :------: | :------------: | :--------------: | :------------------: | :------------------: | :---------: | :----------: |
| Pushbutton Switch, 3-Way Toggle | [Adafruit](https://www.adafruit.com/product/1684) | single | 1 | 9 | 9 | $1.95 | $17.55 |
| DRV8833 DC Motor Driver Module | [Amazon](https://www.amazon.com/DRV8833-Driver-Module-Bridge-Controller/dp/B0GSJSY6XK) | multiple | 5 | 9 | 2 | $6.99 | $13.98 |
| IMU MPU-6050 6-DoF Accel and Gyro Sensor (STEMMA) | [Adafruit](https://www.adafruit.com/product/3886) | single | 1 | 9 | 9 | $12.95 | $116.55 |
| IMU BNO055 9-DOF Absolute Orientation IMU Fusion (STEMMA) | [Adafruit](https://www.adafruit.com/product/4646) | single | 1 | 9 | 9 | $29.95 | $269.55 |
| IMU TDK InvenSense ICM-20948 9-DoF (STEMMA) | [Adafruit](https://www.adafruit.com/product/4554) | single | 1 | 9 | 9 | $19.95 | $179.55 |
| Slim Rubber Rotary Encoder Knob - 11.5mm x 14.5mm D-Shaft | [Adafruit](https://www.adafruit.com/product/5093) | single | 1 | 3 | 1 | $0.75 | $2.25 |
| I2C Stemma QT Rotary Encoder Breakout with Encoder | [Adafruit](https://www.adafruit.com/product/5880) | single | 1 | 3 | 1 | $7.95 | $23.85 |
| Monochrome 1.12" 128x128 OLED Graphic Display - STEMMA QT / Qwiic | [Adafriuit](https://www.adafruit.com/product/5297) | single | 1 | 1 | 1 | $17.50 | $17.50 |

----

[01]:https://www.adafruit.com/product/6315
[02]:https://www.amazon.com/dp/B01LXY7CM3
[03]:https://www.amazon.com/AEDIKO-HC-SR04-Ultrasonic-Distance-Arduino/dp/B09BYWHSMJ
[04]:https://www.amazon.com/Micro-Helicopter-Airplane-Remote-Control/dp/B072V529YD/?th=1
[05]:https://www.adafruit.com/product/3297
[06]:https://www.adafruit.com/product/4634
[07]:https://www.adafruit.com/product/4210
[08]:https://www.amazon.com/WGCD-KY-040-Degree-Encoder-Arduino/dp/B07B68H6R8/
[09]:https://www.adafruit.com/product/6113
[10]:https://www.amazon.com/VIBICCK-500pcs-Momentary-Electronics-Prototyping/dp/B0FPC5J3Z7/?th=1
[11]:https://www.amazon.com/EL-CP-003-Breadboard-Solderless-Distribution-Connecting/dp/B01EV6LJ7G/?th=1
[12]:https://www.amazon.com/LampVPath-Battery-Connector-Plastic-Housing/dp/B079HY8DD9?th=1
[13]:https://www.amazon.com/Amazon-Basics-Performance-All-Purpose-Batteries/dp/B00MH4QM1S/?th=1
[14]:https://www.adafruit.com/product/3955
[15]:https://www.adafruit.com/product/3950
[16]:https://www.amazon.com/dp/B0FTF8P9DQ
[18]:https://www.amazon.com/Connector-Solderless-Multicolor-Electronic-Breadboard/dp/B09FPGT7JT/?th=1
[19]:https://www.amazon.com/Invisible-Mounting-Double-Sided-Permanent-Classroom/dp/B07LFRN1K8/
[20]:https://circuitpython.org/board/raspberry_pi_pico2_w/
[21]:https://learn.adafruit.com/welcome-to-circuitpython/installing-mu-editor
[22]:https://learn.adafruit.com/circuitpython-libraries-on-micropython-using-the-raspberry-pi-pico/thonny-setup
[23]:https://circuitpython.org/downloads
[24]:https://docs.github.com/en
[25]:https://www.amazon.com/Charging-Transfer-Charger-Speakers-Controllers/dp/B0GVBKRW6G?th=1
[26]:https://www.amazon.com/dp/B07YKFX99S?th=1
[27]:https://www.amazon.com/dp/B0DTJZ3432

