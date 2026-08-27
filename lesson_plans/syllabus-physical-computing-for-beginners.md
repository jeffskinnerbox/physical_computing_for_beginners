# Course Syllabus: Physical Computing for Beginners

* **Organization:** Makersmiths — Leesburg
* **Format:** In-person, hands-on, project-based
* **Location:** Makersmiths Leesburg, Electronics Room
* **Audience:** Middle schoolers (6th-8th grade, with a parent/guardian) and high schoolers
* **Class Size:** Up to 8 students + 1 instructor
* **Schedule:** 1 Pre-Class + 6 Classes, every Tuesday, 6:30-8:30pm, Sept 1 - Oct 13

## 1. Course Description

Physical computing is the practical art of making software and hardware work together so a system
can sense the real world and react to it. It shows up everywhere — robots, drones, self-driving
cars, home automation, wearables, and electronic art all run on the same three building blocks:
sensors that gather data, a microcontroller that decides what to do with it, and actuators that take
action. This course introduces young makers to those three building blocks and gives them the tools
to start building useful or creative things with them on their own.

Over one Pre-Class and six weekly Classes, students build up a stack of skills in order: reading a
debounced pushbutton switch and rotary encoder, measuring distance with an ultrasonic sensor,
sweeping a servo motor, driving DC motors with a dual H-bridge motor driver, reading motion data from
a 9-DOF inertial measurement unit (IMU), and finally combining everything into an autonomous,
obstacle-avoiding robot car nicknamed the "Random Rover." Each Class builds directly on the hardware
and skills from the Class before it, so the course is meant to be taken start to finish, in order.

Students program a Raspberry Pi Pico 2 W microcontroller using CircuitPython, a beginner-friendly
version of Python built specifically for microcontrollers. Class time is hands-on first: the
instructor gives a short (~5 minute) talk at the start of each Class, then builds the project
alongside the students on a projected screen while everyone works through the same steps at the
bench. Students are strongly encouraged to work in pairs and help each other, but every student
wires, codes, and tests their own working project, and every student keeps the hardware they build.

There are no grades, quizzes, or rubrics in this course. Progress is measured by completing each
Class's hands-on milestone and, in the final Class, demonstrating a working Random Rover to the
group. Students are taught — from day one — to research and adapt solutions from real-world maker
resources (Instructables, GitHub, Adafruit Learn, SparkFun) instead of waiting on the instructor,
because that is exactly how working makers solve problems outside of class. A course GitHub
repository backstops every Class with build guides and copy-paste-ready code, so no student is ever
stuck without a starting point ("leave no soldier behind").

The skills and hardware built here are also the on-ramp to a future Makersmiths course, where
students design, build, and competitively race a line-following robot on the same Pico 2 W platform
with N20 geared motors.

## 2. Learning Objectives

**Hardware & Electronics**

* Wire a breadboard circuit connecting a microcontroller to a sensor or actuator using a wiring diagram
* Identify and explain the role of STEMMA QT/I2C, PWM, and GPIO connections used across the course's projects
* Diagnose a non-working circuit by checking power, ground, and signal connections methodically

**Programming (CircuitPython)**

* Install CircuitPython firmware and required libraries onto a Raspberry Pi Pico 2 W
* Write and edit CircuitPython code using the Mu or Thonny editor and the CIRCUITPY drive
* Read sensor data in a loop and print it to the serial console for debugging
* Explain what switch bounce is and implement a software debounce routine for a switch and a rotary encoder
* Control a servo motor's angle and a DC motor's speed and direction using PWM

**Robotics Concepts**

* Explain the difference between reading distance with an ultrasonic sensor and orientation with an IMU
* Combine a distance sensor and a servo sweep to scan for the clearest open direction
* Describe, in plain language, how an obstacle-avoidance algorithm decides which way to steer
* Explain why open-loop "dead reckoning" movement (timed, uncorrected motor moves) drifts off target

**Design & Problem-Solving**

* Use Instructables, GitHub, Adafruit Learn, and SparkFun documentation to find and adapt working code
* Apply a "build a little, test a little" iterative approach instead of writing a whole program before testing
* Propose and discuss an algorithm as a group before writing code for it

## 3. Prerequisites

**Required**

* Age 11+ (roughly 6th grade and up)
* Middle schoolers (6th-8th grade) must attend with a parent or guardian who participates alongside them
* High schoolers may attend without a parent
* Bring your own Windows 11 laptop to every Class — no laptop sharing. This course's install guides
  and Pre-Class are written for Windows 11 specifically
* Attend the Pre-Class — it covers the software install every later Class depends on
* Regular attendance — each Class builds directly on hardware and code from the Class before it

**Recommended but Not Required**

* Basic familiarity with Python syntax (variables, loops, functions)
* Comfort typing commands and navigating files on a computer

**Provided by the Course**

* All CircuitPython and Python concepts needed for the projects, taught from scratch
* Step-by-step install guides for every tool used (see the Pre-Class)
* A course GitHub repository maintained by the instructor, containing handouts, install
  instructions, build guides, and copy-paste-ready code so no student is never stuck without a
  starting point
* All required electronic hardware, handed out each Class

## 4. Technology Requirements

**Hardware Per Student**
(component names only — see the course Bill of Materials for costs, quantities, and sourcing)

* Raspberry Pi Pico 2 W (with header)
* Emo Smart Robot Car Chassis Kit
* HC-SR04 Ultrasonic Distance Sensor
* SG90 Micro Servo Motor
* DRV8833 Dual H-Bridge DC/Stepper Motor Driver Breakout Board
* IMU: LSM9DS1 9-DOF Breakout Board (STEMMA)
* KY-040 Rotary Encoder Module
* 1.14" 240x135 Color TFT Display
* Tactile push buttons
* Breadboard, STEMMA QT/Qwiic cable, JST PH male header cable, JST PH female socket cable
* 9V battery clip, 9V batteries, 5V buck converter module

**Shared Tools** (provided by Makersmiths)

* Dupont jumper wires and mounting tape for shared/demo use
* Bench space, power, and general electronics tools in the Electronics Room

**Software** (all free)

* [CircuitPython firmware for the Raspberry Pi Pico 2 W][01]
* [Mu Editor][02] — recommended editor for CircuitPython
* [Thonny][03] — alternate editor, also used with the Pico
* [Adafruit CircuitPython Library Bundle][04]
* A free [GitHub][05] account, to access the course repository

**Student Computer Requirements**

* Windows 11 laptop, one per student (no sharing)
* At least one free USB port for the Pico 2 W
* Internet access for downloading software and researching projects

See the course **Bill of Materials** for full pricing, sourcing links, and purchase quantities.

## 5. Course Structure & Format

### Class Flow

Every Class (after the Pre-Class) follows the same roughly two-hour rhythm:

| Segment | Time | What Happens |
| :-------- | :----- | :-------------- |
| Warm-up / Hook | ~10 min | Review last Class's build, discuss what it unlocked |
| Introduction | ~10 min | Preview today's goal, new parts/protocols, and why they matter |
| Direct Teaching | ~10 min | Explain the concept with diagrams, no code yet |
| Guided Practice | ~40 min | Instructor builds along on the projector; students wire up and test code snippets together |
| Independent Work | ~40 min | Students build and debug their own project, in pairs where possible |
| Closing / Wrap-up | ~10 min | Demo results, preview next Class's prep/reading |

### Course Phases

| Phase | Classes | Focus | Milestone |
| :------ | :-------- | :------ | :---------- |
| Phase 0 — Setup | Pre-Class | Get every laptop and Pico ready to code | First CircuitPython program runs |
| Phase 1 — Inputs | Class 1-2 | Reliable sensing: debounced switches, encoders, distance, servo | Clean sensor readings on the serial console |
| Phase 2 — Outputs & Motion | Class 3-4 | Driving motors and reading orientation | Motor-driven movement in a controlled shape |
| Phase 3 — Integration | Class 5-6 | Combine sensing + motion into an autonomous robot | Working Random Rover demo |

### Pacing & Age Differentiation

Classes are hands-on and self-paced within the two-hour window — the instructor builds alongside the
class on the projector, and students work through the same steps at their own speed, with help
available throughout Independent Work. Middle schoolers attend with a parent/guardian who can help
with fine wiring and reading comprehension of build guides; high schoolers and faster-moving pairs
are pointed to the "Potential Source Materials" for that Class to extend their build (e.g., tuning a
filter constant, adding a second sensor angle) while others catch up. No student's pace blocks
another's — pairs work at whatever speed keeps both partners engaged.

## 6. Lessons Breakdown

### Phase 0 — Setup

**Pre-Class — Prepare Your Laptop and Pico**

* Discuss what physical computing is and the sensor -> processor -> actuator model
* Discuss the Raspberry Pi Pico 2 W, why CircuitPython instead of MicroPython or Arduino C++, and
  where to find help online (Instructables, GitHub, Adafruit Learn, SparkFun)
* Install the Mu and Thonny editors and the Adafruit CircuitPython Library Bundle
* Flash CircuitPython onto the Pico 2 W and find the CIRCUITPY drive
* Write, edit, and run a first small CircuitPython program that blinks the onboard LED and prints a
  heartbeat count to the serial console
* Connect to and use the serial console and the REPL
* **Milestone:** A running CircuitPython program on your own Pico 2 W, visible over the serial console

### Phase 1 — Inputs

**Class 1 — Push Button Switch and Rotary Encoder**

* What switch bounce is and why it confuses a microcontroller
* Discuss: should bounce be fixed in the switch/encoder hardware, or in code? Propose a debounce algorithm as a group
* Read a pushbutton switch and a rotary encoder with CircuitPython; light one LED from the switch and
  dim/brighten a second LED from the encoder
* Stream raw (bouncy) readings to the terminal, then apply debouncing and compare
* If time allows, start assembling the Car Chassis Kit
* **Milestone:** Side-by-side terminal output showing bouncy vs. debounced switch/encoder readings

**Class 2 — Ultrasonic Distance Sensor + Servo Motor**

* How the ultrasonic distance sensor and servo motor each communicate with the Pico
* Read live distance data to the terminal
* Sweep the servo back and forth and read distance at each angle
* Mount the distance sensor on the servo to scan for objects in front of the car
* Discuss: how could this scanning data help a car avoid bumping into things?
* Finish assembling the Car Chassis Kit
* **Milestone:** Live streamed distance-vs-angle data as the servo sweeps

### Phase 2 — Outputs & Motion

**Class 3 — Dual H-Bridge Motor Driver**

* How the DRV8833 dual H-bridge motor driver controls a DC gearbox motor's speed and direction
* Throttle PWM duty cycle to keep current in a safe range for the TT gearbox motors
* Drive the car in a square and a circle of any size, then try to hit exact 12-inch dimensions
* Discuss: why is precise geometry harder than "just moving"? Separate the causes — no
  wheel/heading feedback, battery voltage sag, wheel slip/friction — instead of one vague answer
* **Milestone:** Car reliably drives a 12-inch square and a 12-inch-diameter circle

**Class 4 — Inertial Measurement Unit (IMU)**

* Why knowing speed, heading, and acceleration matters for a moving vehicle
* Read acceleration and gyroscope data from the LSM9DS1 9-DOF IMU breakout board
* Fuse the readings into a single roll/pitch/yaw orientation and stream it to a live 3D display on the laptop
* Discuss: does the on-screen orientation match the IMU's real physical orientation? Does IMU
  orientation data help solve the Class 3 square/circle challenge, or is something still missing?
* **Milestone:** Live 3D orientation display driven by the IMU

### Phase 3 — Integration

**Class 5 — Build the Random Rover: Collision Avoidance**

* Combine the servo-mounted ultrasonic sensor, motor driver, and Pico 2 W into one autonomous car
* Sweep left-right on a timer (and immediately if something gets close) to find the clearest direction before steering
* Drive at constant speed around the room, avoiding obstacles
* Discuss: what does each component contribute to the collision-avoidance decision? How would you
  actually measure whether it's working, beyond eyeballing it?
* **Milestone:** Car drives autonomously and avoids at least one obstacle without instructor intervention

**Class 6 — Finish the Random Rover + Stretch Goals**

* Finish and tune the Random Rover from Class 5
* Optional stretch goals: reconnect the Class 1 rotary encoder for live speed control, stream IMU
  data over the Pico 2 W's WiFi to a graphical history display in a browser, add the TFT display for
  real-time distance/heading/speed status on the rover itself
* Discuss: looking back across the course's "what's missing?" questions, which single improvement
  would most help the rover's real-world reliability?
* End-of-course showcase: each student demonstrates their working Random Rover to the group
* **Milestone:** Final Random Rover Showcase (see Assignment Descriptions)

## 7. Recommended & Supplemental Studies

**Videos & Playlists**

* [Raspberry Pi Pico School][06]
* [Intro to Raspberry Pi Pico and RP2040][07]
* [MicroPython (YouTube playlist)][08]
* [CircuitPython School (YouTube playlist)][09]
* [CircuitPython Projects (YouTube playlist)][10]
* [Every Hardware Protocol Explained Simply in 10 Minutes!][11]
* [Real Python: Your First Steps][12]

**Websites**

* [Instructables][13]
* [GitHub Docs][05]
* [Adafruit Learn][14]
* [SparkFun Docs][15]

**Tools**

* [Snakie — CircuitPython-friendly practice tool][16]

**Class-by-Class References**

*Pre-Class*

* [What is CircuitPython?][17]
* [Recommended Editors][18]
* [Installing the Mu Editor][02]
* [Installing CircuitPython][01]
* [The CIRCUITPY Drive][19]
* [Creating and Editing Code][20]
* [Exploring Your First CircuitPython Program][21]
* [Connecting to the Serial Console][22]
* [Interacting with the Serial Console][23]
* [The REPL][24]
* [CircuitPython Libraries][25]
* [CircuitPython Hardware][26]
* [Welcome to the Community!][27]
* [CircuitPython Documentation][28]

*Class 1 — Push Button Switch and Rotary Encoder*

* [What Is Switch Bounce & How to Implement Debounce][29]
* [MicroPython Rotary Encoder Driver (GitHub)][30]
* [Hardware Debounced Rotary Encoder (Hackaday.io)][31]
* [How to Use a Rotary Encoder with the Raspberry Pi (The Pi Hut)][32]
* [Python Debouncer Library for Buttons and Sensors][33]
* [adafruit_debouncer Advanced Debouncing guide][34]

*Class 2 — Ultrasonic Distance Sensor + Servo Motor*

* [Python & CircuitPython | Ultrasonic Sonar Distance Sensors][35]
* [adafruit/Adafruit_CircuitPython_HCSR04][36]
* [CircuitPython Servo | CircuitPython Essentials][37]
* [DC, Servo, Stepper Motors and Solenoids with the Pico][38]

*Class 3 — Dual H-Bridge Motor Driver*

* [DC Motor Examples - Raspberry Pi Pico (CMU Creative Soft Robotics)][39]
* [Driving A DC Motor With CircuitPython][40]
* [Adafruit CircuitPython Motor Library — API Reference][41]
* [Adafruit DRV8833 DC/Stepper Motor Driver Breakout Board][42]

*Class 4 — Inertial Measurement Unit (IMU)*

* [Python & CircuitPython — Adafruit LSM9DS1 9-DOF Breakout][43]
* [API Reference — Adafruit LSM9DS1 Library][44]
* [Adafruit Learn — LSM6DSOX/ISM330DHC/LSM6DSO32 6-DoF IMUs (CircuitPython)][45]

*Class 5 — Random Rover: Collision Avoidance*

* [Raspberry Pi Pico W taught this car to avoid objects][46]
* [How to make an obstacle avoidance robot using Raspberry Pi Pico board][47]
* [Obstacle Avoidance Robot Using Raspberry Pi Pico][48]

*Class 6 — Finish the Random Rover + Stretch Goals*

* [Adafruit 1.14" 240x135 Color TFT Display][49]
* [Raspberry Pi Pico W Asynchronous Web Server – MicroPython Code][50]
* [Raspberry Pi Pico Web Server Control][51]
* [Raspberry Pi Pico W Soft Access Point Web Server Example][52]

## 8. Assignment Descriptions

**Ongoing Assignments**

* **Build Journal:** After every Class, jot a few notes (or photos) in your section of the course
  GitHub repo — what you built, what broke, what you fixed. No required format or length; this is
  for your own reference and for the instructor to spot common sticking points.
* **Course GitHub Repository:** The instructor maintains a repo with handouts, install instructions,
  build guides, and ready-to-use code for every Class. Pull code from it whenever you're stuck —
  no student is ever left without a working starting point.

**Milestone Assignments**

Each Class (see Lessons Breakdown above) ends with a hands-on milestone — a specific, observable
result (e.g., "clean debounced switch readings on the terminal," "car drives a 12-inch square").
There's no written report due; the milestone is demonstrated live during the Closing / Wrap-up
portion of the Class, or brought back working at the start of the following Class if it wasn't
finished in time.

**Final Showcase**

> **Random Rover Showcase — Class 6**
> Each student demonstrates their working Random Rover navigating the room and avoiding obstacles.
> This is a showcase, not a competition — every student who gets a working demo running is
> recognized. Students who completed stretch goals (speed control, WiFi telemetry, TFT status
> display) demonstrate those too. No age brackets, no elimination, no formal scoring.

---

[01]:https://circuitpython.org/board/raspberry_pi_pico2_w/
[02]:https://learn.adafruit.com/welcome-to-circuitpython/installing-mu-editor
[03]:https://learn.adafruit.com/circuitpython-libraries-on-micropython-using-the-raspberry-pi-pico/thonny-setup
[04]:https://circuitpython.org/downloads
[05]:https://docs.github.com/en
[06]:https://www.youtube.com/playlist?list=PLBJJ76R_ry5QY9BU5gqxrvtODWFkkTjYa
[07]:https://www.youtube.com/playlist?list=PLEBQazB0HUyQO6rJxKr2umPCgmfAU-cqR
[08]:https://www.youtube.com/playlist?list=PLLrTlbAfJTzL0aLrVIrdUHedNpsZxyaJd
[09]:https://www.youtube.com/playlist?list=PLBJJ76R_ry5T3X72OIDkMOXQIdmcvSkue
[10]:https://www.youtube.com/playlist?list=PLBJJ76R_ry5Rz5YgfjpI4eCHmS5o5umL8
[11]:https://www.youtube.com/watch?v=2LaiScfoYGQ
[12]:https://realpython.com/python-first-steps/
[13]:https://www.instructables.com/
[14]:https://learn.adafruit.com/
[15]:https://docs.sparkfun.com/
[16]:https://www.snakie.org/
[17]:https://learn.adafruit.com/welcome-to-circuitpython/what-is-circuitpython
[18]:https://learn.adafruit.com/welcome-to-circuitpython/recommended-editors
[19]:https://learn.adafruit.com/welcome-to-circuitpython/the-circuitpy-drive
[20]:https://learn.adafruit.com/welcome-to-circuitpython/creating-and-editing-code
[21]:https://learn.adafruit.com/welcome-to-circuitpython/exploring-your-first-circuitpython-program
[22]:https://learn.adafruit.com/welcome-to-circuitpython/kattni-connecting-to-the-serial-console
[23]:https://learn.adafruit.com/welcome-to-circuitpython/interacting-with-the-serial-console
[24]:https://learn.adafruit.com/welcome-to-circuitpython/the-repl
[25]:https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-libraries
[26]:https://learn.adafruit.com/welcome-to-circuitpython/beginner-boards
[27]:https://learn.adafruit.com/welcome-to-circuitpython/welcome-to-the-community
[28]:https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-documentation
[29]:https://www.picotech.com/library/articles/blog/what-is-switch-bounce-how-to-implement-debounce
[30]:https://github.com/miketeachman/micropython-rotary
[31]:https://hackaday.io/project/162207-hardware-debounced-rotary-encoder
[32]:https://thepihut.com/blogs/raspberry-pi-tutorials/how-to-use-a-rotary-encoder-with-the-raspberry-pi
[33]:https://learn.adafruit.com/debouncer-library-python-circuitpython-buttons-sensors/overview
[34]:https://learn.adafruit.com/debouncer-library-python-circuitpython-buttons-sensors/advanced-debouncing
[35]:https://learn.adafruit.com/ultrasonic-sonar-distance-sensors/python-circuitpython
[36]:https://github.com/adafruit/Adafruit_CircuitPython_HCSR04
[37]:https://learn.adafruit.com/circuitpython-essentials/circuitpython-servo
[38]:https://learn.adafruit.com/use-dc-stepper-servo-motor-solenoid-rp2040-pico
[39]:https://courses.ideate.cmu.edu/16-480/s2026/text/code/pico-motor.html
[40]:https://www.woolseyworkshop.com/2022/07/25/driving-a-dc-motor-with-circuitpython/
[41]:https://docs.circuitpython.org/projects/motor/en/latest/api.html
[42]:https://learn.adafruit.com/adafruit-drv8833-dc-stepper-motor-driver-breakout-board
[43]:https://learn.adafruit.com/adafruit-lsm9ds1-accelerometer-plus-gyro-plus-magnetometer-9-dof-breakout/python-circuitpython
[44]:https://docs.circuitpython.org/projects/lsm9ds1/en/latest/api.html
[45]:https://learn.adafruit.com/lsm6dsox-and-ism330dhc-6-dof-imu/python-circuitpython
[46]:https://www.raspberrypi.com/news/raspberry-pi-pico-w-taught-this-car-to-avoid-objects/
[47]:https://srituhobby.com/how-to-make-an-obstacle-avoidance-robot-using-raspberry-pi-pico-board/
[48]:https://circuitdiagrams.in/obstacle-avoidance-robot-using-raspberry-pi/
[49]:https://learn.adafruit.com/adafruit-1-14-240x135-color-newxie-tft-display/circuitpython
[50]:https://electrocredible.com/raspberry-pi-pico-w-web-server-asynchronous-micropython/
[51]:https://github.com/gurgleapps/pico-web-server-control
[52]:https://microcontrollerslab.com/raspberry-pi-pico-w-soft-access-point-web-server-example/
