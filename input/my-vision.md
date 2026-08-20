
# My Vision for the Class: Physical Computing for Beginners

This file will provide the initial context, required by Claude Code, so it can assist in creating:

* a course syllabus for all to read and understand the details of the course,
* lesson plans for each class so the instructor a plan for each class,
* step-by-step install instructions to prepare development environment,
* theory of operation document to explain complex project processes,
* explainer documents to address explain ideas complex at a teen level,
* class build guides on how to construct the project step-by-step,
* wiring diagram to help construct breadboard circuity,
* a bill of materials (BOM) covering the entire course and its financial allocation to students,
* code snippets useful for students to copy & paste,
* tested project built code so when all else fails the instructor has what works.

That course is called "Physical Computing for Beginners" and is described in the following text.

----

## Course Description

This course is to teach students about Physical Computing.
Physical computing is building interactive systems that combine software and hardware to sense and respond to the real world.
It uses three main parts: inputs (sensors), processing (microcontrollers), and outputs (actuators).

* **Sensors** gather real-world data like temperature, light, motion, or sound.
* **Processor**, a microcontroller, runs code to read the sensor data and decide what to do.
* **Outputs** are actuators that take action in the physical world by turning on lights, making sounds, or moving motors.

### Course Goal

In this course, students will build physical computing projects.
The goal is for the student to:

1. Learn physical computing with Raspberry Pi Pico W and CircuitPython.
1. Learn CircuitPython, and its firmware build procedures on the Raspberry Pi Pico,
   so the student can create project without the help of an instructor.
1. The student should learn how to use the Internet
   (e.g [Instructables](https://www.instructables.com/), [GitHub](https://docs.github.com/en), [Adafruit](https://learn.adafruit.com/), [Sparkfun](https://docs.sparkfun.com/), etc.)
   as powerful resources/enablers to build their own physical computing projects.
1. Give each student the skills they can build, in a future course,
   a line following robot with Raspberry Pi Pico W microcontroller and N20 Geared Motors.
   In this future course, students will design, build, and competitively test a line following robotic car on a common track.

### Prerequisite Knowledge
While knowledge of Python, MicoPython, or CircuitPython is not a prerequisite,
it would be beneficial for the student to study these topic.
Below is a recommend list of study sites.
* [Raspberry Pi Pico School](https://www.youtube.com/playlist?list=PLBJJ76R_ry5QY9BU5gqxrvtODWFkkTjYa)
* [Intro to Raspberry Pi Pico and RP2040](https://www.youtube.com/playlist?list=PLEBQazB0HUyQO6rJxKr2umPCgmfAU-cqR)
* [MicroPython](https://www.youtube.com/playlist?list=PLLrTlbAfJTzL0aLrVIrdUHedNpsZxyaJd)
* [CircuitPython School](https://www.youtube.com/playlist?list=PLBJJ76R_ry5T3X72OIDkMOXQIdmcvSkue)
* [CircuitPython Projects](https://www.youtube.com/playlist?list=PLBJJ76R_ry5Rz5YgfjpI4eCHmS5o5umL8)

### Course Structure

* Total of 6 classes, each 2 hours long, and each class will have a project that the student is expected to complete.
  While it is desirable the project is completed in class, they will have the ability to take the project home and finish it.
* The classes will be at Makersmiths within the Electronics room where supporting tools will be available.
* The instructor will supply the project to be done.
  This includes project objective, instructive build guide, required electronic hardware for the project,
  and software snippets that will help the student create the project.

### Class Dynamics / Activities

Each class is project based (i.e. students learn primarily by build and experimenting with things)
and has the activities listed below.

#### Students

1. In each class, the student is assigned a physical computing project to design, build, and test.
   All students are assigned the same project.
1. Students are encouraged to work in teams (ideally 2 to a team) and help each other complete the project.
   Despite the encourage team work, each student is expected to design, build, and test their own working project.
1. Students will have access to the internet and are free to search for solutions (including working code)
   to any challenges they may face.

#### Instructor

* The instructor will define what projects will be done for each class.
  The classes, to the extent possible, will be sequenced so previous classes will be helpful for the classes that follow.
* The instructor will perform the assigned project along with the class.
  The project computer activity by the instructor will be displayed on a screen so the class can follow as necessary.
* Class activities will follow this pattern:
  1. Prior to attending a class, students are expected to read the build guide prior to the class, and do reading and viewing assignments.
     Reading and viewing assignment will be on the build guide.
  1. At the beginning of each class, the instructor will give a short (5 minute) lecture on what will be done in the class.
  1. The students will be asked to login to their computers, go to a GitHub page, and do any other preparatory steps.
  1. Project hardware components will be handed out and the instructor will reference any relevant GitHub content that will be needed,
     Build guides will on GitHub, available for students to read and copy&paste via the computer.
  1. The students then begin to work on their projects.
     Instructor will follow along with the build and help the students as needed.
  1. At the conclusion of the class, and if time permits,
     the students will be asked to demonstrate and discuss the operation of what they built.
     Students will be encourage to finish and even expand there projects at home.
     The instructor will reference the build guide where expansion plans are suggested including source with build plans and code.

### Chronological Sequence of Class Activities

A chronological sequence of class activities maps out the step-by-step order of a lesson from start to finish.
A standard lesson flows from an warm-up hook to direct instruction, guided practice, independent work, and a final wrap-up

1. **Warm-up / Hook**: Grab student attention and review past work.
   Discuss what they have accomplished so far and what they have learned.
   Point out how this empowers them to build things.
1. **Introduction**: Share the main goal and new key words.
   Discuss the main things that will be learned in the current class.
   Point out the new devices (e.g. Servo Motor) / tools (e.g. I2C protocol) / capabilities (e.g. create WiFi Access Point)
   that will be learned and how this will empower them (e.g. see what the microcontroller is doing).
1. **Direct Teaching**: Explain the core concept or skill.
   Without code, but using diagrams where possible, explain what your about to build.
   Point out how the code will bring life to these diagrams.
1. **Guided Practice**: Work through examples together as a group.
   Project your project activities on a overhead screen.
   Start the hands on work of building the project.
   Give them code snippets and have them test those snippets.
1. **Independent Work**: Let students try the task on their own.
   Let the students work the task by themselves or with other students.
   Let them struggle but offer help.
1. **Closing / Wrap-up**: Review what was learned and check for understanding.
   Let them continue working at home offering help via GitHub communication.
   Remind them to prepare for next weeks class by doing the reading & video studies.

### Chronological Sequence of Class Projects

Contained here is a chronological sequence of a class projects
and a brief description of what will be built in each of the classes.
This not only states what will be accomplished in the classes but
helps students move smoothly through core concepts, building upon them as the progress.
It is expected that the courses will follow this entire class sequence as stated below,
but if improvements can be made, changes should be suggested.

All the subsections (i.e. Objective, Talking Points, Features/Capabilities, Potential Source Materials)
are suggestions and should be expanded on.
They should be examined for class room ideas and project source code
but are not expected to be the only source to consider.

Tips for Students:

* Like any professional engineer, build a little and then test.  Build a little more and then test.
  Repeat until you accomplished your goal. CircuitPython are very supportive of this process.

#### Pre-Class: Preparation of Student Laptop

* **Description:** This "pre-class" will focus on getting the students, and their laptops,
  ready for development on the Raspberry Pi Pico 2W microcontroller, installing required software tools
  on a Windows 11 instance.
  In this class, students do their first CircuitPython build: a minor one that blinks the onboard LED and
  prints a heartbeat count to the serial console, proving the board, firmware, and editor are all talking
  to each other.
  The Adafruit CircuitPython Library Bundle and editors [Mu](https://learn.adafruit.com/welcome-to-circuitpython/installing-mu-editor) & [Thonny](https://learn.adafruit.com/circuitpython-libraries-on-micropython-using-the-raspberry-pi-pico/thonny-setup) will be installed for later use.
  The Pre-Class homework also includes a standalone test of the IR obstacle sensor used later for the
  Class 5 Random Rover, run without any rover hardware.
* **Objective**: Get the student familiar with the tools they will be using in the class.
  Also discuss how this project was created from Internet resource and how they can do this too.
* **Talking Points**:
  * Discuss [Raspberry Pi Pico 2W with Header](https://www.adafruit.com/product/6315), [MicroPython](https://micropython.org/), [CircuitPython](https://circuitpython.org/downloads),
  [Instructables](https://www.instructables.com/), [GitHub](https://docs.github.com/en), [Adafruit](https://learn.adafruit.com/), [Sparkfun](https://docs.sparkfun.com/), etc.
  * Why CircuitPython instead of MicroPython or Arduino C++? What did we trade away (performance) for what we gained (beginner-friendliness, readability)?
  * What is "firmware," and why does it have to be flashed onto the board before any of the student's own code can run?
  * Why does the CIRCUITPY drive show up on the laptop like an ordinary USB flash drive? What actually happens when you drag/save a `.py` file onto it?
* **Features/Capabilities**: Blink the onboard LED and print a heartbeat count to the serial console,
  proving the board, CircuitPython firmware, and editor (Mu/Thonny) are all talking to each other.
* **Course Pseudocode**: [`class-0-code.py`](./class-0-code.py) &mdash; save as `code.py` on the CIRCUITPY drive. No external parts required.
* **Potential Source Materials**:
  * [What is CircuitPython?](https://learn.adafruit.com/welcome-to-circuitpython/what-is-circuitpython),
  * [Recommended Editors](https://learn.adafruit.com/welcome-to-circuitpython/recommended-editors),
  * [Installing the Mu Editor](https://learn.adafruit.com/welcome-to-circuitpython/installing-mu-editor),
  * [Installing CircuitPython](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython),
  * [The CIRCUITPY Drive](https://learn.adafruit.com/welcome-to-circuitpython/the-circuitpy-drive),
  * [Creating and Editing Code](https://learn.adafruit.com/welcome-to-circuitpython/creating-and-editing-code),
  * [Exploring Your First CircuitPython Program](https://learn.adafruit.com/welcome-to-circuitpython/exploring-your-first-circuitpython-program),
  * [Connecting to the Serial Console](https://learn.adafruit.com/welcome-to-circuitpython/kattni-connecting-to-the-serial-console),
  * [Interacting with the Serial Console](https://learn.adafruit.com/welcome-to-circuitpython/interacting-with-the-serial-console),
  * [The REPL](https://learn.adafruit.com/welcome-to-circuitpython/the-repl),
  * [CircuitPython Libraries](https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-libraries),
  * [CircuitPython Hardware](https://learn.adafruit.com/welcome-to-circuitpython/beginner-boards),
  * [Welcome to the Community!](https://learn.adafruit.com/welcome-to-circuitpython/welcome-to-the-community),
  * [CircuitPython Documentation](https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-documentation).

#### 1st Class: Push Button Switch and Rotary Encoder

* **Description:** This class will be the first time the students do a "physical computing"
  build with the microcontroller and CircuitPython (other than a "Hello World").
  I want the project to be simple but informative.
  The push button switch and rotary encoder are simple to understand devices,
  but prove to be complex to our little microcontroller.
  What is physically going on in objects you connect to a microcontroller can be confound & confusing.

  The microcontroller will be set up to to operate two LEDs.
  One is turned on with the push button switch and the other has its brightness controlled via the rotary encoder.
  Also, print statements should provide the use status information about the switch and encoder.

  The circuit will be first build with no debouncing.
  The class will observer what happens when the button is push or the encoder moved.
  The that the output erratic and not deterministic.
  This is a problem you do not want.
  Debouncing is added to both the switch & encoder, problem solved.

  If you have time, start the assembly of the Car Chassis Kit.
* **Wiring Continuity**: First circuit of the course (button on `GP2`, encoder on `GP3`/`GP4`, LEDs on `GP14`/`GP15`).
  Leave it on the breadboard after this class &mdash; the rotary encoder is reused, unchanged, as a live
  speed control in the Class 6 stretch goal (`class-6-code-1.py`).
* **Objective**: Show how to use CircuitPython modules to [debounce a switch](https://www.picotech.com/library/articles/blog/what-is-switch-bounce-how-to-implement-debounce)
  and process the rotary encoder.
* **Talking Points**:
  * Should we fix this problem in the switch/encoder or in the microcontroller?
  Can the students propose an algorithm that solves the switch bounce problem?
  * The same settle-time debounce fixes both the switch and the encoder even though they're different kinds of devices &mdash; what property do they share that lets one technique cover both?
  * What if the debounced signal were controlling a motor instead of an LED? Does an erratic, undebounced signal go from a cosmetic annoyance to a safety problem?
  * Debouncing adds a small delay before a press/turn is recognized &mdash; can the class feel/measure whether this makes the button feel laggy, and where's the line between "reliable" and "unresponsive"?
* **Features/Capabilities**: Send data to terminal showing how
  the rotary encoder & switch bounces give erroneous results without debouncing.
  Repeat with debouncing applied.
* **Course Pseudocode**:
  * [`class-1-code-1.py`](./class-1-code-1.py) &mdash; no debouncing. Button on `GP2`, encoder CLK/DT on `GP3`/`GP4`,
    button LED on `GP15`, encoder brightness LED (PWM) on `GP14`. Prints raw press count / encoder position
    to the serial console so the class can see the erratic, non-deterministic counts.
  * [`class-1-code-2.py`](./class-1-code-2.py) &mdash; same wiring, now debounced with `adafruit_debouncer.Debouncer`
    on the button and a minimum-step-interval software debounce on the encoder. Requires
    `adafruit_debouncer` from the Adafruit CircuitPython Library Bundle in `/lib`.
* **Potential Source Materials**:
  * [MicroPython Rotary Encoder Driver (GitHub)](https://github.com/miketeachman/micropython-rotary)
  * [Hardware Debounced Rotary Encoder (Hackaday.io)](https://hackaday.io/project/162207-hardware-debounced-rotary-encoder)
  * [How to Use a Rotary Encoder with the Raspberry Pi (The Pi Hut)](https://thepihut.com/blogs/raspberry-pi-tutorials/how-to-use-a-rotary-encoder-with-the-raspberry-pi)
  * [Python Debouncer Library for Buttons and Sensors](https://learn.adafruit.com/debouncer-library-python-circuitpython-buttons-sensors/overview)
  * [adafruit_debouncer Advanced Debouncing guide](https://learn.adafruit.com/debouncer-library-python-circuitpython-buttons-sensors/advanced-debouncing)

#### 2nd Class: Ultrasonic Distance Sensor + Servo Motor

* **Description:** First test the [HC-SR04 ultrasonic distance sensor](https://www.amazon.com/AEDIKO-HC-SR04-Ultrasonic-Distance-Arduino/dp/B09BYWHSMJ) with the microcontroller send data to the terminal.
  Use Adafruit's official Learn guide for wiring and reading an HC-SR04 ultrasonic
  range sensor from CircuitPython. Covers the trigger/echo wiring pattern, the voltage-divider
  caveat needed to protect the Pico's 3.3V logic from the sensor's 5V echo pin, and the full
  CircuitPython driver usage (the `adafruit_hcsr04` library) with inline example code that
  prints live distance readings to the serial console.
  A simple, complete "read a sensor, print a value" loop.

  Now do a similar test with the [SG90 9g micro servo motor](https://www.amazon.com/Micro-Helicopter-Airplane-Remote-Control/dp/B072V529YD/?th=1)
  and using the [CircuitPython Servo Learn guide](https://learn.adafruit.com/circuitpython-essentials/circuitpython-servo).
  Walks through what a servo is and how PWM controls its shaft angle, then
  builds up working code in small steps: import `pwmio`, create a `PWMOut` on one GPIO pin, wrap it with
  `adafruit_motor.servo.Servo`, set `.angle` to sweep the servo across its range, and calibrate the
  `min_pulse`/`max_pulse` widths for a real motor (since cheap micro servos vary). The full source is
  `class-2-code-2.py`, included with the course material.
  Students end the class session with a servo that continuously sweeps 0-180 degrees and back, and
  an understanding of PWM as a concept they will reuse for motors later in the course.
  Again, a simple, complete "set a position, print a value" loop.

  Finely place the ultrasonic distance sensor on top of servo motor with two sided tape,
  and sense object in front of us. The servo motor sweeps back & forth to measure distance of objects.
  Data from the sensor and the servo need to be printed out so the student an read the values,
  discuss how they are created, and what do they mean, how could the be used.

  If you have time, continue working the assembly of the Car Chassis Kit.
* **Wiring Continuity**: All-new pins (`GP6`/`GP7` sensor, `GP8` servo) &mdash; nothing from Class 1 is touched
  or rewired, it just sits unused on the breadboard for now. This sensor+servo pairing is carried forward
  unchanged into Class 5's rover.
* **Objective**: The students are to use the servo-swept distance sensor to observe the table in front of them,
  then explore & discuss how those readings could be used to navigate a car without bumping into things.
* **Talking Points**:
  * Discuss and demonstrate the communication protocols used by each device.
  Can the students propose an algorithm that enables them to navigate the car and not bump into objects?
  * The HC-SR04 encodes distance as a timed sound echo; the servo encodes angle as a PWM pulse-width &mdash; compare how each device physically encodes information.
  * Why does the sensor have both a minimum *and* a maximum usable range? Tie the near-field blind spot and far-range limit back to the speed of sound and the sensor's beam angle.
  * When the sensor is sweeping with the servo, how do you know a given distance reading really corresponds to the angle you think the servo is pointed at? (This is why class-2-code-3.py sleeps briefly after each move before reading.)
  * Why did the servo protocol pick 500-2500us pulse widths instead of something simpler like a 0-100% analog voltage? Tie back to the protocol-design discussion from Class 1.
* **Features/Capabilities**: Stream live data to the terminal
  so the student can "see" what the sensor and servo is seeing/doing.
* **Course Pseudocode**:
  * [`class-2-code-1.py`](./class-2-code-1.py) &mdash; HC-SR04 alone. TRIG on `GP6`, ECHO on `GP7` through a
    resistor voltage divider (5V ECHO -> 3.3V logic). Prints distance in cm using `adafruit_hcsr04`.
  * [`class-2-code-2.py`](./class-2-code-2.py) &mdash; SG90 alone. Signal on `GP8`. Sweeps 0-180 degrees using
    `adafruit_motor.servo`, with calibration notes for `min_pulse`/`max_pulse` since cheap servos vary.
  * [`class-2-code-3.py`](./class-2-code-3.py) &mdash; combined: HC-SR04 mounted on the SG90 shaft, sweeps and
    prints angle + distance pairs at each stop, the direct precursor to the collision-avoidance logic in Class 5.
* **Potential Source Materials**:
  * [HC-SR04 Ultrasonic Module Distance Sensor - Product Page](https://www.amazon.com/AEDIKO-HC-SR04-Ultrasonic-Distance-Arduino/dp/B09BYWHSMJ)
  * [Python & CircuitPython | Ultrasonic Sonar Distance Sensors](https://learn.adafruit.com/ultrasonic-sonar-distance-sensors/python-circuitpython)
  * [adafruit/Adafruit_CircuitPython_HCSR04](https://github.com/adafruit/Adafruit_CircuitPython_HCSR04)
  * [SG90 9g Micro Servo Motor - Product Page](https://www.amazon.com/Micro-Helicopter-Airplane-Remote-Control/dp/B072V529YD/?th=1)
  * [CircuitPython Servo | CircuitPython Essentials](https://learn.adafruit.com/circuitpython-essentials/circuitpython-servo)
  * [DC, Servo, Stepper Motors and Solenoids with the Pico](https://learn.adafruit.com/use-dc-stepper-servo-motor-solenoid-rp2040-pico)

#### 3rd Class: Dual H-Bridge Motor Driver

* **Description:** The [DRV8833](https://learn.adafruit.com/adafruit-drv8833-dc-stepper-motor-driver-breakout-board) Dual [H-Bridge Motor Driver](https://www.electronics-tutorials.ws/io/h-bridge-circuit.html) device will allow you to easily control the
  speed & direction of the DC gearbox motors included with our [Emo Smart Robot Car Chassis Kit](https://www.amazon.com/dp/B01LXY7CM3).
  I say "easily" but you must talk the language of the DRV8833 to get it to move the way you want it too.
  DRV8833 dual H-bridge driver for controlling two DC/N20 motors: forward, reverse, stop, and PWM-based speed control per channel.
  Our DRV8833 motor driver for our motors works well down to 3V but you must throttling PWM duty cycle in your code to limit high currents.
  Full source is provided as course material, written to be dropped into a student project and called from simple test code
  (spin motor A forward at half speed, reverse motor B, etc.).
  I plan to use a 9 volt battery to drive the wheels.

  Again, print discrete status messages as each move happens (forward, reverse, stop, calibration attempt)
  so the class can see what the wheels are being told to do, even though there's no live wheel-speed telemetry yet.
  Once the driver is tested, attempt the 12 inch square and circle by timing calibrated straight/turn moves
  &mdash; open-loop "dead reckoning," since there's no feedback (yet) to correct for drift.
  Have the student discuss what useful things they can do with this information? What information is absent?
* **Wiring Continuity**: All-new pins (`GP9`-`GP12` motor driver, plus the 9V battery for `VM`) &mdash; Classes 1
  and 2's circuits stay in place, untouched. This motor driver is carried forward unchanged into Class 5's rover.
* **Objective**: The student is to understand the use of the dual H-bridge motor driver,
  and make the car drive in a 12 inch square and a 12 inch diameter circle.
* **Talking Points**:
  * First, make it move in a square & circle of any random size. Is this easy?
    Now make it move in a 12 inch square and a 12 inch diameter circle. This is harder? Why ... What is missing? How can the fix this?
  * Push the "what is missing?" question further: have students name the specific causes separately &mdash; no wheel/heading feedback, battery voltage sag, and wheel slip/friction &mdash; instead of one vague "it's not accurate."
  * The motor circuit runs off its own 9V battery, separate from the Pico's logic power &mdash;
    so why does it still need a common ground with the Pico?
  * Why doesn't a 50% PWM duty cycle mean the motor moves at exactly 50% of its full speed? Discuss stall torque, friction, and voltage sag.
  * This code drives each motor with 2 PWM pins ("locked antiphase") &mdash; briefly compare to the DRV8833's alternative phase/enable mode and why one was chosen for this course.
* **Features/Capabilities**: Print a discrete status message to the terminal each time a move happens
  (forward, reverse, stop, square/circle attempt) so the student can "see" what the motors were just told to do &mdash;
  not a continuous live stream, since there's no wheel-speed feedback yet.
* **Course Pseudocode**:
  * [`class-3-code-1.py`](./class-3-code-1.py) &mdash; motor driver test library (save as `motor_driver.py`).
    Motor A: `AIN1`/`AIN2` on `GP9`/`GP10`; Motor B: `BIN1`/`BIN2` on `GP11`/`GP12`. Uses
    `adafruit_motor.motor.DCMotor` with a `MAX_THROTTLE` cap to limit current. Exposes `drive(left, right)`
    and `stop()` for forward/reverse/stop/PWM speed per channel.
  * [`class-3-code-2.py`](./class-3-code-2.py) &mdash; imports `motor_driver`, attempts the 12 inch square and
    12 inch diameter circle by timing straight/turn moves (open-loop dead reckoning, no encoder/IMU feedback
    yet). `SPEED`, `SECONDS_PER_INCH`, and `SECONDS_PER_90_DEGREES` must be measured/calibrated per robot;
    the resulting drift is the built-in prompt for the "what is missing?" discussion.
* **Potential Source Materials**:
  * [DC Motor Examples - Raspberry Pi Pico (CMU Creative Soft Robotics)](https://courses.ideate.cmu.edu/16-480/s2026/text/code/pico-motor.html)
  * [Driving A DC Motor With CircuitPython](https://www.woolseyworkshop.com/2022/07/25/driving-a-dc-motor-with-circuitpython/)
  * [Adafruit CircuitPython Motor Library — API Reference](https://docs.circuitpython.org/projects/motor/en/latest/api.html)
  * [Adafruit DRV8833 DC/Stepper Motor Driver Breakout Board](https://learn.adafruit.com/adafruit-drv8833-dc-stepper-motor-driver-breakout-board)

#### 4th Class: Inertial Measurement Unit (IMU)

* **Description:** We will use a [9-DOF LSM9DS1 Breakout Board](https://www.adafruit.com/product/4634) [inertial measurement unit (IMU)](https://www.youtube.com/watch?v=qS9GwaekLW4)
  Know how fast you are move, what direction your going, are you speeding up or down
  are some of the important things to know when driving a vehicle.
  We will explore explore sensing motion as with a inertial measurement unit (IMU).
  Using Adafruit's official Learn guide for reading a 9-DOF IMU breakout over I2C in CircuitPython.
  Full example code initializes the sensor and reads acceleration (x/y/z) and gyroscope (x/y/z) each loop.
  The guide also covers basic interpretation — e.g., using accelerometer values to detect tilt/orientation
  — as a stepping stone toward more advanced uses.

  In an enhancement to the IMU, the raw accelerometer and gyroscope readings are fused with a Mahony filter
  into a single roll/pitch/yaw orientation, which is what actually gets printed to the serial console
  (not the raw six values). Kalman and Madgwick filters are mentioned here only for context/comparison —
  Mahony is the one implemented in `class-4-code-1.py`. Discuss why you need a filter like this at all.

  If you have time, continue working the assembly of the Car Chassis Kit.
* **Wiring Continuity**: All-new pins (`GP0`/`GP1` I2C) &mdash; Classes 1-3's circuits stay in place, untouched.
  This same I2C wiring is reused unchanged for the Class 6 WiFi stretch goal (`class-6-code-2.py`).
* **Objective**: The objective is to read data from an IMU and display the results by communicating to a Python 3D
  graphical display on the laptop. This display should show how the movement of the IMU changes the image on the display.
* **Talking Points**:
  * IMU shows great potential, but does it solve our problems?  Can it help us do the square and the circle as in the 3rd class?
  * Why fuse the accelerometer and gyroscope instead of just using whichever one is "better"? What does each one get wrong on its own (accelerometer noisy under vibration, gyro drifts over time)?
  * Have students actually raise/lower `MAHONY_KP` in class-4-code-1.py and watch the live tradeoff between drift and jitter, instead of just discussing it in the abstract.
  * Would mounting the IMU off to one side of the car vs. exactly at its pivot point change the readings while turning? Why or why not?
  * Orientation (roll/pitch/yaw) tells you which way you're pointed, but nothing about how far you've traveled &mdash; what's still missing to solve the Class 3 square/circle challenge?
* **Features/Capabilities**: Reads accelerometer and gyroscope data from the IMU, fuses it with a Mahony filter into
  roll/pitch/yaw, and streams that orientation over USB serial to a live 3D box rendered on the laptop.
  The purpose is to show how the physical orientation of the IMU is accurately (or not) reflected in the display.
* **Course Pseudocode**:
  * [`class-4-code-1.py`](./class-4-code-1.py) &mdash; runs on the Pico. LSM9DS1 over I2C, `SCL`->`GP1`, `SDA`->`GP0`.
    Reads accel + gyro, fuses them with a Mahony filter (tunable `MAHONY_KP`/`MAHONY_KI`) into roll/pitch/yaw,
    and prints `roll,pitch,yaw` CSV lines over USB serial. This is the "why do we need a filter" payoff:
    raw accelerometer alone is noisy, raw gyro alone drifts.
  * [`class-4-code-2.py`](./class-4-code-2.py) &mdash; runs on the STUDENT LAPTOP (`pip install pyserial matplotlib numpy`).
    Reads the serial CSV and redraws a 3D box in real time with matplotlib, so students see whether
    tilting the physical board is faithfully reflected on screen. Usage: `python class-4-code-2.py <port>`.
* **Potential Source Materials**:
  * [Python & CircuitPython — Adafruit LSM9DS1 9-DOF Breakout](https://learn.adafruit.com/adafruit-lsm9ds1-accelerometer-plus-gyro-plus-magnetometer-9-dof-breakout/python-circuitpython)
  * [API Reference — Adafruit LSM9DS1 Library](https://docs.circuitpython.org/projects/lsm9ds1/en/latest/api.html)
  * [Adafruit Learn — LSM6DSOX/ISM330DHC/LSM6DSO32 6-DoF IMUs (CircuitPython)](https://learn.adafruit.com/lsm6dsox-and-ism330dhc-6-dof-imu/python-circuitpython)

#### 5th Class: Create the Random Rover with Collision Avoidance

* **Description:** An obstacle-avoiding robot car that mounts the ultrasonic sensor on a micro
  servo so it can sweep left-right and "look" for the clearest direction before choosing which
  way to steer, driven by a Pico W and a motor driver.
  This design actively scans its surroundings before deciding how to move: it rescans on a periodic
  timer while otherwise driving straight, but if anything comes within a set stopping distance while
  driving, it interrupts that timer, stops immediately, and rescans right away instead of waiting.

  Two extra safety layers back up the ultrasonic sweep: a fixed IR obstacle sensor mounted low and
  forward gives a near-field check between scans (the ultrasonic sweep only re-checks periodically
  or when triggered &mdash; the IR sensor closes that gap), and a mechanical limit switch mounted as a
  physical bumper is the last-resort fallback &mdash; if the rover actually contacts something, the
  switch fires an immediate stop-and-reverse regardless of what either sensor reported.
* **Wiring Continuity**: Two new pins this class: `GP5` (limit switch, digital input with internal
  pull-up, wired as a physical bumper on the chassis front) and `GP13` (IR obstacle sensor, digital
  input, fixed forward-facing). Both are carried forward unchanged into Class 6. Otherwise, reconnects
  exactly the Class 2 sensor+servo circuit (`GP6`-`GP8`) and the Class 3 motor driver circuit
  (`GP9`-`GP12`) as they were left wired &mdash; nothing to move. The Class 1 and Class 4 circuits can
  stay on the breadboard unused or be set aside; neither is needed for this build.
* **Objective**: Create an autonomous car with wheel motors, operating at a constant speed,
  move around the room without hitting anything.
  Avoid collisions by using the servo-mounted ultrasonic distance sensor.
* **Talking Points**:
  * What will it take to build an autonomous car with collision avoidance?
    How do each of the components help solve the challenge?
  * class-5-code.py rescans both on a timer *and* immediately when something gets too close &mdash; what's the risk of relying on only one of those two triggers?
  * The rover steers toward whichever scan angle had the most clearance &mdash; can students design a room layout (e.g. a narrow gap with open space just beyond it) where "pick the largest reading" picks a bad direction?
  * The rover stops to scan instead of sensing continuously while driving &mdash; discuss the safety/simplicity vs. speed/smoothness tradeoff of that "stop-look-go" design.
  * Beyond eyeballing that it doesn't hit things, how would the class actually measure/test whether their rover's collision avoidance is working?
  * Three different signals now decide "stop": ultrasonic distance, IR near-field, and the bump switch. What does each one catch that the others miss, and what's the risk of trusting only one?
* **Features/Capabilities**: Performance of the car is streamed to the terminal. Reads the IR sensor
  and limit switch every loop; either one true forces an immediate stop independent of the ultrasonic
  scan/timer logic.
* **Course Pseudocode**:
  * [`class-5-code.py`](./class-5-code.py) &mdash; combines Class 2's servo-swept HC-SR04 (`GP6`/`GP7` trigger/echo,
    `GP8` servo signal) with Class 3's `motor_driver` (`GP9`-`GP12`). Drives forward at `DRIVE_SPEED`; sweeps
    the sensor across `SCAN_ANGLES` on a timer or immediately if anything comes within `STOP_DISTANCE_CM`,
    turns toward the clearest heading (reusing Class 3's turn-time calibration), then continues. Also polls
    the IR sensor (`GP13`) and limit switch (`GP5`) every loop; either going active forces an immediate
    stop-and-reverse, overriding the normal scan-and-turn logic. Streams every scan reading, chosen heading,
    drive state, and sensor-triggered stop event to the serial console.
* **Potential Source Materials**:
  * [Raspberry Pi Pico W taught this car to avoid objects](https://www.raspberrypi.com/news/raspberry-pi-pico-w-taught-this-car-to-avoid-objects/)
  * [How to make an obstacle avoidance robot using Raspberry Pi Pico board](https://srituhobby.com/how-to-make-an-obstacle-avoidance-robot-using-raspberry-pi-pico-board/)
  * [Obstacle Avoidance Robot Using Raspberry Pi Pico](https://circuitdiagrams.in/obstacle-avoidance-robot-using-raspberry-pi/)

#### 6th Class: Continue building the Random Rover

* **Description:** Continue building an obstacle-avoiding robot car and complete the project.
  Then add the stretch objectives outlined in "Objective": a rotary encoder that lets students speed
  the rover up or down live while it drives, an IMU that streams tilt data over the Pico W's WiFi to a
  chart in a browser instead of only the serial console, and a TFT screen that shows the rover's
  distance/heading/speed status on the robot itself so it's readable without a USB cable attached.
* **Wiring Continuity**: Stretch #1 and #2 need no new wiring &mdash; they reconnect the Class 1 encoder
  (`GP3`/`GP4`) and Class 4 IMU (`GP0`/`GP1`) exactly as already wired, right alongside the Class 5 rover
  circuit (`GP6`-`GP12`). The Class 5 limit switch (`GP5`) and IR sensor (`GP13`) also carry forward
  unchanged, needing no rewiring. Stretch #3 is the only new wiring this class: a TFT on `GP18`-`GP22`,
  pins not used by anything else in the course, so it drops in without disturbing the rover.
* **Objective**: Stretch Objectives are to
  1. Add a rotary encoder to control speed.
  1. Send IMU data via WiFi to a graphical historical display.
  1. Add a TFT display showing real-time status.
* **Talking Points**:
  * Adding encoder speed control changes the rover's behavior &mdash; does driving slower actually make it make smarter decisions, or does it just take longer to make the same decisions?
  * Looking back across all 6 classes' "what's missing?" discussions (wheel/heading feedback in Class 3, orientation-vs-distance in Class 4), which single improvement would most help the rover's real-world reliability, and what would it take to add it?
  * This is the last class before the future line-following robot course &mdash; which skills/parts built here (motor driver, calibration mindset, sensor fusion) will carry forward, and what's genuinely new there (line sensor, competitive track) that this course didn't cover?
* **Features/Capabilities**: Stretch #1 prints the new drive speed to the terminal each time the encoder
  changes it. Stretch #2 serves a live-updating chart in a web browser (no cable needed, just the Pico W's
  IP address) that scrolls a rolling history of IMU tilt as the Pico streams it over WiFi. Stretch #3 shows
  the rover's distance/heading/speed directly on its own on-board TFT screen, readable with no laptop or
  cable attached at all.
* **Course Pseudocode**:
  * [`class-6-code-1.py`](./class-6-code-1.py) &mdash; stretch #1. Reuses the Class 1 rotary encoder (`GP3`/`GP4`)
    to raise/lower `current_speed` live and feeds it to `motor_driver.drive()`.
  * [`class-6-code-2.py`](./class-6-code-2.py) &mdash; stretch #2. Pico W joins WiFi (credentials in `settings.toml`),
    runs an `adafruit_httpserver` web server, and serves a page with a hand-drawn HTML5 canvas chart that
    polls `/data.json` every 200ms and keeps a rolling ~150-sample history of roll/pitch from the LSM9DS1
    (accelerometer-only tilt estimate; port class-4-code-1.py's Mahony filter in for full yaw).
  * [`class-6-code-3.py`](./class-6-code-3.py) &mdash; stretch #3. ST7789 1.14" 240x135 TFT over SPI
    (`SCK`/`MOSI`/`CS`/`DC`/`RST` on `GP18`-`GP22`) shows distance/heading/speed as large on-board text via
    `displayio` + `adafruit_display_text`, so rover status is visible without a USB cable. Ships with demo
    values; swap in the real variables from class-5-code.py / class-6-code-1.py.
* **Potential Source Materials**:
  * [Adafruit 1.14" 240x135 Color Newxie TFT Display](https://learn.adafruit.com/adafruit-1-14-240x135-color-newxie-tft-display/circuitpython)
  * [Raspberry Pi Pico W Asynchronous Web Server – MicroPython Code](https://electrocredible.com/raspberry-pi-pico-w-web-server-asynchronous-micropython/)
  * [Raspberry Pi Pico Web Server Control](https://github.com/gurgleapps/pico-web-server-control)
  * [Raspberry Pi Pico W Soft Access Point Web Server Example](https://microcontrollerslab.com/raspberry-pi-pico-w-soft-access-point-web-server-example/)

----

## Course Assets

### Bill of Materials (BOM)

A Bill of Materials (BOM) is a complete list of the raw parts, items, components, quantities, software, code, and
tools needed to run this course. It is the **single source of truth** for all cost and sourcing information —
the syllabus and lesson plans reference component names but never prices; all cost information lives here.
These items must be purchased prior to the course's first class.

Assumed class size for all per-person math below: **9 people (8 students + 1 instructor)**, with the instructor
keeping a full kit and rover like every student. Adafruit prices below were confirmed live; Amazon-sourced prices
could not be confirmed by fetching the live product page (Amazon does not expose price in a non-interactive
fetch), so reconfirm those before ordering.

#### Hardware

##### Per-Student Required

Each of the 9 people (8 students + instructor) keeps one of everything in this table. Several items are sold in
multi-packs; the "Item Cost" column is the *effective per-unit cost* for readability, with the actual pack
purchase (and any spares that come with it) noted below the table and priced in the Cost Summary.

| Item | Quantity | Item Cost | Source | Notes |
| :-----: | :-----: | :-----: | :-----: | :--------: |
| Raspberry Pi Pico 2W with Header | 1 | $8.00 | [Adafruit][01] | microcontroller, used every class starting Pre-Class |
| Emo Smart Robot Car Chassis Kit | 1 | $13.99 | [Amazon][02] | 2 DC gearbox motors + wheels; assembled across Classes 1-2, driven starting Class 3 |
| HC-SR04 Ultrasonic Distance Sensor | 1 | $1.30 | [Amazon][03] | sold in 10-pack ($12.99); Class 2 sensor, reused Class 5-6 |
| SG90 9g Micro Servo Motor | 1 | $2.00 | [Amazon][04] | sold in 10-pack ($19.99); Class 2 servo, reused Class 5-6 |
| DRV8833 DC/Stepper Motor Driver Breakout Board | 1 | $5.95 | [Adafruit][05] | Class 3 motor driver, reused Class 5-6 |
| IMU 9-DOF LSM9DS1 Breakout Board (STEMMA) | 1 | $19.95 | [Adafruit][06] | Class 4 IMU, reused Class 6 stretch #2 |
| STEMMA QT / Qwiic JST SH 4-pin Cable, 100mm | 2 | $0.95 | [Adafruit][07] | I2C connection for the LSM9DS1 (Class 4 onward) + 1 spare; the LSM9DS1 is the only I2C device in the course |
| KY-040 360 Degree Rotary Encoder Module | 1 | $2.89 | [Amazon][08] | sold in 8-packs ($12.99/pack); 9 needed requires 2 packs (16 units, 7 spare) — 1 pack alone is short by 1 |
| 1.14" 240x135 Color Newxie TFT Display | 1 | $9.95 | [Adafruit][09] | Class 6 stretch #3 status display |
| Tactile Push Button Switch | 2 | $0.02 | [Amazon][10] | sold in 500-pack ($9.99); Class 1 button + spare |
| Breadboard 830 Point Solderless Prototype PCB Board | 1 | $3.00 | [Amazon][11] | sold in 3-packs ($8.99); one board per person, kept for the whole course |
| I TYPE 9 Volt Battery Clip | 1 | $0.65 | [Amazon][12] | sold in 10-pack ($6.49); Class 3 motor power |
| 9V Alkaline Battery | 1 | $1.59 | [Amazon][13] | sold in 8-packs ($12.69/pack); 9 needed requires 2 packs (16 units, 7 spare) — 1 pack alone is short by 1 |
| 5V Buck Converter Module | 1 | $1.50 | [Amazon][16] | sold in 10-pack ($14.99); onboard 5V power |
| LED (assorted) | 2 | $0.00 | Makersmiths | Class 1 button LED + encoder brightness LED; stocked by the makerspace |
| Resistor (assorted, 220-330Ω for LEDs, ~1k/2k Ω for HC-SR04 voltage divider) | 4 | $0.00 | Makersmiths | Class 1 LED current-limiting + Class 2 HC-SR04 voltage divider; stocked by the makerspace |
| USB A to Micro USB Charging Cable with Data Transfer | 9 | $1.00 | [Amazon][25] | backup for a student whose own cable fails; not the primary supply (see Tools below) |
| Micro Limit Switch | 1 | $0.35 | [Amazon][26] | sold in 20-pack ($6.50); Class 5 rover bump sensor, reused Class 6 |
| IR Obstacle Avoidance Sensor | 1 | $0.35 | [Amazon][27] | sold in 10-pack ($8.77); Class 5 rover near-field backup sensor, reused Class 6; also Pre-Class Homework 5 standalone test |

Per-Student Required Cost = 8.00 + 13.99 + 1.30 + 2.00 + 5.95 + 19.95 + 2×0.95 + 2.89 + 9.95 + 2×0.02 + 3.00 + 0.65 + 1.59 + 1.50 + 0 + 0 + 1.00 + 0.35 + 0.35 ≈ **$74.41 per person** (see Cost Summary for the exact bulk-purchase total, which accounts for whole-pack rounding)

##### Per-Student Optional

None. All three Class 6 stretch-goal items (rotary encoder speed control, WiFi IMU chart, TFT status display) are
treated as in-scope/required for this course rather than optional add-ons; their hardware (KY-040, LSM9DS1, TFT)
already appears in Per-Student Required above.

##### Shared Supplies

Consumables and bulk items used by the whole class, not kept individually by each student.

| Item | Quantity | Item Cost | Source | Notes |
| :-----: | :-----: | :-----: | :-----: | :--------: |
| Dupont Wires - 120pcs 20cm Jumper Wire | 1 | $9.99 | [Amazon][18] | shared jumper wire stock for all classes |
| Invisible Hold Mounting Tape | 1 | $11.99 | [Amazon][19] | mounts the Class 2 HC-SR04 onto the SG90 servo horn and helps with chassis assembly |
| Painter's/Marking Tape + Tape Measure | 1 | $0.00 | Makersmiths | marks the 12" square/circle test tracks, Class 3 onward |

Shared Supplies Cost = 9.99 + 11.99 + 0 = $21.98 total ÷ 9 people ≈ $2.44 per student

##### Shipping

| Item | Quantity | Item Cost | Source | Notes |
| :-----: | :-----: | :-----: | :-----: | :--------: |
| Adafruit Shipping | NA | $10.00 [estimated] | NA | flat estimate for the combined Adafruit order (Pico, DRV8833, LSM9DS1, STEMMA cables, TFT) — confirm actual rate/free-shipping threshold before ordering |
| Amazon Shipping | NA | $0.00 [estimated] | NA | assumes Amazon Prime free shipping on all Amazon-sourced items |

Shipping Cost = 10.00 + 0.00 = $10.00 total (assumption — verify both vendors' actual shipping before purchasing)

##### Cost Summary

Exact totals from whole-pack/whole-unit purchasing (9 people: 8 students + instructor):

```text
Per-Student Required (bulk-purchase total) = $72.00 (Pico) + $125.91 (chassis) + $12.99 (HC-SR04 10-pack)
    + $19.99 (SG90 10-pack) + $53.55 (DRV8833 ×9) + $179.55 (LSM9DS1 ×9) + $17.10 (STEMMA cable ×18)
    + $25.98 (KY-040, 2× 8-packs) + $89.55 (TFT ×9) + $9.99 (button 500-pack) + $26.97 (breadboard, 3× 3-packs)
    + $6.49 (battery clip 10-pack) + $25.38 (9V battery, 2× 8-packs)
    + $14.99 (buck converter 10-pack) + $0.00 (LED) + $0.00 (resistor)
    + $9.00 (USB backup cable ×9) + $6.50 (limit switch 20-pack) + $8.77 (IR sensor 10-pack)
    = $704.71 total (~$78.30 per person)

Shared Supplies = $21.98 total (~$2.44 per person)
Shipping = $10.00 total (~$1.11 per person)

Grand Total = $704.71 + $21.98 + $10.00 = $736.69 for the course (~$81.85 per person, 9 people)
```


#### Software

All free.

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

#### Code Blocks

Pseudocode/reference implementations provided by the instructor, embedded inline in each class's lesson plan.

| Item | Quantity | Source | Notes |
| :-----: | :-----: | :-----: | :--------: |
| `class-0-code.py` | 1 | Instructor | blink onboard LED + serial heartbeat, Pre-Class |
| `class-1-code-1.py` / `class-1-code-2.py` | 2 | Instructor | undebounced vs. debounced button + rotary encoder, Class 1 |
| `class-2-code-1.py` / `class-2-code-2.py` / `class-2-code-3.py` | 3 | Instructor | HC-SR04 alone, SG90 alone, combined servo-swept sensor, Class 2 |
| `class-3-code-1.py` / `class-3-code-2.py` | 2 | Instructor | motor driver library + calibrated square/circle test, Class 3 |
| `class-4-code-1.py` / `class-4-code-2.py` | 2 | Instructor | Mahony-filtered IMU orientation (Pico) + live 3D viewer (laptop), Class 4 |
| `class-5-code.py` | 1 | Instructor | Random Rover collision-avoidance logic, Class 5 |
| `class-6-code-1.py` / `class-6-code-2.py` / `class-6-code-3.py` | 3 | Instructor | encoder speed control, WiFi IMU chart, TFT status display — Class 6 stretch goals |

#### Tools

| Item | Quantity | Source | Notes |
| :-----: | :-----: | :-----: | :--------: |
| Windows 11 Laptop | 1 | Student | one per student, no sharing; all install guides and the Pre-Class assume Windows 11 specifically |
| USB Cable | 1 | Student | own cable, brought to every class starting with the Pre-Class; course keeps a small spare supply (see Shared Supplies) for a cable that fails, not as the primary source |

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

These items are removed from consideration after iterating on the lesson plans

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

## Course Documentation

Claude Code, using this file as key part of its context,
will assist in the development of this course further by creating the documentation listed below.
These documents

| Document | Primary Audience | Description |
| :--------- | :--------: | :------------ |
| syllabus | student | High-level course map that tells students what to expect: topics, schedule, materials, objectives, and how progress is measured. |
| lesson plan | instructor | A step-by-step teaching guide that tells the instructor exactly how to run a single class: what to prep, what to say, what to build, how to handle problems, and how to wrap up. It covers the *how* — the syllabus covers the *what* and *when*. |
| lesson script | student | TBD |
| install instructions | student | A step-by-step software install guide, written at a level a 12-18 year old with basic Bash/PowerShell/Python literacy can follow without hand-holding. |
| theory of operation | student | Explain how a technology, software program, machine, electronic circuit, or system works. Document contains brief overview and detailed step-by-step decomposition of the system's operation. |
| explainer | student | Makes complex ideas accessible to teens through plain English, use of examples & analogies, and narrative structure. It provides the What → Why → How. Explain simple concepts that are unfamiliar. |
| build guide | student | This is a step-by-step construction plan for the project.  It provides a wiring guide for the hardware (via "wiring diagrams" document). Software architecture, interface specifications, helpful code snippets, testing recommendations |
| wiring diagrams | student | A visual or tabular reference document showing how to physically connect components—pin-to-pin wiring, power/ground routing, and connector orientation—so students can wire the hardware correctly without misreading a schematic. |
| bill of materials (BOM) | instructor | A complete, itemized bill of materials (BOM). It says what do we need to buy, how much does it cost, and where do we get it. The single source of truth for all cost and sourcing information in the project. |
| code snippets | student | A grab-bag of ready-to-use, well-commented code blocks (sensor reads, motor control, common patterns) that students copy-paste into their own sketches — like a spice rack next to the stove, not a full recipe. |
| tested project code | instructor | The instructor's own working reference build (code + wiring), fully verified end-to-end — the "answer key" pulled out when a student's project won't cooperate and you need to prove it can work. |

----

## Training

* [CircuitPython School](https://www.youtube.com/playlist?list=PLBJJ76R_ry5T3X72OIDkMOXQIdmcvSkue)
* [How to Use Python: Your First Steps](https://realpython.com/python-first-steps/)
* [Every Hardware Protocol Explained Simply in 10 Minutes!](https://www.youtube.com/watch?v=2LaiScfoYGQ)

## Tools

* [Snakie](https://www.snakie.org/)
