
# Class-03 Handout

## Definitions for Physical Computing
* **General Technical Definition:**
  The combination of software and hardware to create interactive systems capable of communicating
  with the physical environment using sensors, microcontrollers, and actuators.
* **Educational Definition:**
  The process of taking code off a flat computer screen and bringing it into the real world,
   making abstract programming concepts tangible through lights, sounds, and motion.
* **Relationship Between Physical Computing and Robotics:**
  The relationship between physical computing and robotics is best understood as
  a shared technological foundation with different application goals,
  where physical computing serves as the broader conceptual umbrella.

## What is a Robot?
A robot is an autonomous or semi-autonomous machine designed to sense its environment, process that information,
and execute a series of complex physical actions.
Unlike standard machinery or computers, a true robot must possess three core capabilities:
sensing, thinking (processing), and acting.

The three pillars of a robot:
* **Sense:** A robot uses sensors (such as cameras, microphones, sonar, or touch sensors)
  to gather information about the physical world around it.
* **Think:** An onboard computer or microcontroller processes the sensor data,
  applies programmed instructions or AI algorithms, and decides on the best course of action.
* **Act:** The robot uses actuators (such as motors, hydraulic arms, wheels, or speakers)
  to move, manipulate objects, or interact with its environment without direct, real-time human control.

## How Physical Computing Differs From Robotics?
While **physical computing** and **robotics** overlap significantly—both use sensors, microcontrollers, and actuators,
**they differ fundamentally in their primary intent, autonomy, and interaction design**.

Key differences broken down:
* **The Element of Autonomy:**
  Robotics heavily prioritizes autonomy and self-governance.
  A robot is designed to sense its environment, make a decision, and execute a physical task
  (like vacuuming a room or welding a car part) on its own.
  Physical computing systems are often reactive, waiting for a human to touch, walk by,
  or otherwise trigger an expressive response.
* **Mobility vs. Integration:**
  Robots usually have wheels, legs, or mechanical arms to alter the physical world around them.
  Physical computing systems are typically embedded into everyday objects or architectural spaces—like
  a smart mirror that displays the weather when you look at it,
  or an interactive art installation that changes colors based on the room's ambient noise.
* **Artistic Expression vs. Engineering Utility:**
  Physical computing emerged largely from art, design,
  and human-computer interaction (HCI) programs to make technology feel more organic.
  Robotics is rooted deeply in mechanical engineering, electrical engineering,
  and computer science to maximize functional efficiency.

## Our Not So Secret Goal
Build a Robot!

When we first imagine how our robot will behave, we idealistically think
motors behave the same,
nothing slips or bumps,
we can accurately sense any target or obstacle,
electrical/physical/mission noise is not present.

This is so wrong!

## Our Challenge
**The Sensing Problem:**
* Can we measure directly (or even indirectly) all the things we need to make good decisions?

**The Motor Problem:**
* Identical brand & model electric motors do not preform the same way
* Electric motors are also physical objects that have uneven friction
* When used, battery voltages/currents will sag

**The Wheel Problem:**
* Under real world conditions, wheels will slip, jam, even slide sideways
* If the wheel deforms, this introduces errors hard to measure or predict

**The Navigation Problem:**
* The robot has a mission (e.g. leave the room) that requires it to navigate its world
  (e.g. identify the door, travel to the door, mover through the door)
  * Identify a door (how?) and maneuver to the door (what path?)
  * Identify obstacles (what is an obstacle?) and avoid the obstacle (what path?)
* How does the robot know its orientation in the world?
  A sudden slip, motor sag, wheel jam can cause the forward direct to suddenly point in a new direction

