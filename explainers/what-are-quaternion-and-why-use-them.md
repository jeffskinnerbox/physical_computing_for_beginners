# What Are Quaternions, and Why Use Them?
> **Part 3 of 3.** [What Is an IMU, and What Does a Mahony Filter Do?][01] (part 1) →
> [What Is Gimbal Lock?][02] (part 2) → this doc.

In Class 4 you'll clip an IMU onto your breadboard, tilt it around in your hand, and watch a 3D
model on your laptop tilt right along with it. Buried in the middle of that code is a strange
line: `q0, q1, q2, q3 = 1.0, 0.0, 0.0, 0.0`. Those four numbers are a **quaternion**, the way
your Pico actually keeps track of which way the board is pointing. This document explains what a
quaternion is, where the idea came from (a stone bridge in Dublin, 1843), and why robots,
spacecraft, and video games all prefer it over the roll/pitch/yaw angles you already know.

You don't need to do any quaternion math to finish Class 4. The goal is that when you see
`q0..q3` in the code, you know what they mean and why they're there.


## Start here: the rover needs to know which way it's facing
Your IMU (inertial measurement unit) doesn't hand you an orientation. Its gyroscope reports
*how fast* the board is turning, and its accelerometer reports which way gravity is pulling. Those
are rates and directions, not "you are tilted 20° to the left." Your code has to add up those
readings over time to build an orientation estimate, and a filter (the Mahony filter, in Class 4)
keeps that estimate from drifting. [What Is an IMU, and What Does a Mahony Filter Do?][01] covers
all of that in detail.

That leaves one question this document answers: once you've *got* an orientation, how should you
store it in memory? It sounds like a boring bookkeeping choice. It turns out to be one of the most
important decisions in the whole program.


## The obvious answer: three angles
The natural way to describe a tilt is with three angles: **roll** (tipping side to side),
**pitch** (nose up or down), and **yaw** (turning left or right while staying flat). Together
they're called **Euler angles** (pronounced "OY-ler"), and [What Is Gimbal Lock?][02] defines
them properly. They're great for *people*: if the rover's website says "roll 5°, pitch −2°,
yaw 90°," you picture a rover sitting almost flat, turned a quarter-turn left from where it
started. That's why the Class 4 code still prints roll/pitch/yaw at the end of every loop.

But storing orientation *as* three angles, and updating those angles directly from the gyroscope,
causes trouble for the computer.


## The problem with three angles
The biggest problem has a name: **gimbal lock**. When pitch reaches straight up or straight down
(±90°), roll and yaw stop meaning different things. Two of your three angles end up describing
the same motion, and the math loses track of one direction of rotation. The numbers can jump
wildly even though the physical object moved smoothly. [What Is Gimbal Lock?][02] walks through
exactly why this happens, and why the order you apply the three angles in matters too.

Gimbal lock isn't the only headache, though:

1. **Lots of trigonometry.** Updating three angles from gyro readings needs trigonometry functions
   (sine, cosine, tangent) every single loop. On a small microcontroller running 50 times a
   second, that's slow, and some of those formulas divide by numbers that can get close to zero.
2. **Wrap-around.** Yaw jumps from 359° to 0°. Average "359°" and "1°" naively and you get
   180°, pointing exactly backward, when the right answer is 0°.

Engineers also use a 3×3 **rotation matrix**, a grid of nine numbers, which avoids gimbal lock.
But nine numbers is a lot to store and update, and after thousands of small updates, rounding
errors slowly bend the grid out of shape until it no longer describes a pure rotation.


## The solution: four numbers instead of three
A **quaternion** is a group of four numbers, usually written `(w, x, y, z)`, that together describe
one rotation. The key idea is surprisingly simple:

> **Any** orientation can be reached from "level and facing forward" by a single twist around
> one axis.

Hold your phone flat, then turn it to any crazy angle you like. There is always *one* imaginary
skewer you could push through the phone, and *one* amount of spin around that skewer, that would
take it from flat to where it is now. A quaternion just packs those two things together:

- `x, y, z`: which way the skewer points (the **axis** of rotation).
- `w`: how much to spin around it (the **angle**).

That's it. There are no "first roll, then pitch, then yaw" steps, so there's no order to get
wrong, and no special angle where two axes collapse into one. The four numbers always describe
one rotation cleanly.

There's one rule: for a quaternion to represent a rotation, its four numbers squared must add up
to exactly 1 (`w² + x² + y² + z² = 1`). A quaternion that follows this rule is called a **unit
quaternion**. The "level, facing forward, no rotation" quaternion is `(1, 0, 0, 0)`, which is
exactly the starting value in the Class 4 code: `q0, q1, q2, q3 = 1.0, 0.0, 0.0, 0.0`.


## Why quaternions win (and how the rover code uses each advantage)
Here's how each strength shows up in the code you'll run in the [Class 4 lesson script][03].

1. **No gimbal lock.** A quaternion describes one twist about one axis, so there's no orientation
   where it breaks, and the filter keeps working even with the IMU pointed at the ceiling. Only
   the roll/pitch/yaw *display* can get weird near ±90° pitch; see [What Is Gimbal Lock?][02].
2. **Cheap math, no trig in the update loop.** Look at `mahony_update()`: it folds the gyro
   rates into `q0..q3` using nothing but multiplication and addition. No `sin`, no `cos`, no
   `atan2`. That's faster on the Pico and avoids dividing by near-zero numbers. The trig only
   appears once, in `quaternion_to_euler()`, when it's time to show a human the answer.
3. **Easy to fix rounding drift.** Computers round every calculation a tiny bit. After thousands
   of updates, the four numbers stop adding up (squared) to exactly 1. The fix is one step:
   divide all four by their total length, called **renormalizing**. That's the `norm = ...` line
   at the bottom of `mahony_update()`. Fixing a drifted rotation matrix is much messier.
4. **Compact.** Four numbers versus nine for a rotation matrix. Less memory, fewer calculations,
   and fewer places for rounding error to creep in.
5. **Smooth blending.** You can slide smoothly between two quaternions with a trick called
   **slerp** (short for "spherical linear interpolation," which just means "fill in the
   in-between steps along a curved path"). The in-between steps always take the shortest, most
   natural route, with no 359°-to-1° wrap-around surprise. Class 4 doesn't use slerp, but it's
   the reason video games and animation tools switched to quaternions.

So the rover's plan is: **think in quaternions, talk in angles.** The Mahony filter keeps a
quaternion internally, because that's what's reliable for the computer. Only at the last step
does `quaternion_to_euler()` convert it to roll/pitch/yaw, because that's what's readable for you:
on the serial console, in the laptop's 3D wireframe viewer, and on the rover status website. As
the author of [Why Robots Use Quaternions][04] puts it, the representation that's easiest for
humans isn't always the one that's best for the robot.


## Where quaternions came from: a bridge in Dublin
Quaternions were invented by the Irish mathematician [William Rowan Hamilton][05]. Mathematicians
already had a trick for rotating things on a flat, 2D page: pair up two numbers in a special way
so that multiplying them *is* a rotation. (These pairs are called complex numbers, but you don't
need them here.) For years Hamilton tried to stretch the same trick to 3D using three numbers,
and every attempt failed.

On October 16, 1843, Hamilton was walking with his wife along the Royal Canal in Dublin when the
answer hit him: he needed *four* numbers, not three. He was so excited that he pulled out a knife
and carved the key rule into the stone of [Brougham Bridge][06] (now called Broom Bridge):

```text
i² = j² = k² = ijk = −1
```

The carving has long since worn away, but a plaque on the bridge marks the spot, and
mathematicians still walk the route every year on the anniversary.

Hamilton spent the rest of his life promoting quaternions, and for a while they were taught
widely. But in the 1880s, Josiah Willard Gibbs and Oliver Heaviside pulled out the parts
physicists found most useful and repackaged them as **vectors**, the arrows-with-length you may
have met in science class. Vectors were simpler for everyday physics, and quaternions faded into
a mathematical curiosity. Heaviside even called them "a positive evil of no inconsiderable
magnitude" ([History of quaternions][07]).

Then computers arrived and needed to rotate things in 3D, fast and reliably. Spacecraft attitude
(orientation) control systems adopted quaternions. In 1985 Ken Shoemake showed computer animators
how to use them for smooth rotation, and by the mid-1990s they were steering the camera and
characters in 3D games like *Tomb Raider*. Today they're standard in drones, phones, VR headsets,
robot software, and, in a small way, your Random Rover.


## For the curious: the actual numbers (optional)
You can skip this section and still ace Class 4. But if you want to see how the four numbers are
built, here's the recipe. For a rotation of angle θ (theta) around an axis pointing in direction
`(ax, ay, az)` (a direction arrow with length 1):

```text
w = cos(θ / 2)
x = ax · sin(θ / 2)
y = ay · sin(θ / 2)
z = az · sin(θ / 2)
```

Notice the **half angle** (θ/2). It's one of the odd quirks of quaternions, and it's why the
numbers don't look like degrees at all.

In the Class 4 code, the names map like this: `q0` is `w`, `q1` is `x` (the roll axis), `q2` is
`y` (the pitch axis), and `q3` is `z` (the vertical axis, so it controls yaw).

**Worked example: the rover turns 90° to the left, staying flat.** That's a spin of θ = 90° around
the vertical axis, so the axis is `(0, 0, 1)` and θ/2 = 45°:

```text
w = cos(45°)     = 0.707   -> q0
x = 0 · sin(45°) = 0       -> q1
y = 0 · sin(45°) = 0       -> q2
z = 1 · sin(45°) = 0.707   -> q3
```

So after the turn, the filter would hold `q0, q1, q2, q3 ≈ 0.707, 0, 0, 0.707`. Check the unit
rule: 0.707² + 0.707² = 0.5 + 0.5 = 1. And if you plug those numbers into the yaw line of
`quaternion_to_euler()`, you get `atan2(2 · (0.707 · 0.707), 1 − 2 · 0.707²) = atan2(1, 0) = 90°`,
exactly the turn we started with. Roll and pitch both come out to 0°, because the rover never
tipped.

Want to try one yourself? A 180° spin about the vertical axis gives θ/2 = 90°, so the quaternion
is `(0, 0, 0, 1)`. Tilt the IMU in Class 4, print `q0..q3` next to roll/pitch/yaw, and see if you
can predict the numbers before they appear.


## Key takeaways
- An IMU gives rates and directions; your code builds orientation from them.
- Roll/pitch/yaw are easy for people but fragile for computers, especially near ±90° pitch.
- A quaternion is four numbers describing one twist around one axis: no gimbal lock, no trig in
  the update loop, a one-step fix for rounding drift, and smooth blending.
- The rover thinks in quaternions (`q0..q3`) and only converts to roll/pitch/yaw to show you.
- Hamilton carved the idea into a Dublin bridge in 1843; it sat mostly unused for a century until
  computer graphics, spacecraft, and robots brought it back.


## Where to go next
- [What Is an IMU, and What Does a Mahony Filter Do?][01]: how the IMU measures motion and how
  the filter turns rates into a steady orientation.
- [What Is Gimbal Lock?][02]: the Euler-angle definitions, why three angles break at ±90°, and
  the Apollo story.
- [Class 4 Lesson Script][03]: the IMU and Mahony filter code this doc refers to.
- [Why Robots Use Quaternions (Akshet Patel)][04]
- [William Rowan Hamilton (Wikipedia)][05]
- [Broom Bridge (Wikipedia)][06]
- [History of quaternions (Wikipedia)][07]
- [Quaternions and spatial rotation (Wikipedia)][08]: the full math, if you want it.


[01]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/blob/main/explainers/what-is-an-imu-and-mahony-filter.md
[02]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/blob/main/explainers/what-is-gimbal-lock.md
[03]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/blob/main/lesson_scripts/class-04-lesson-script.md
[04]:https://akshetpatel.substack.com/p/why-robots-use-quaternions
[05]:https://en.wikipedia.org/wiki/William_Rowan_Hamilton
[06]:https://en.wikipedia.org/wiki/Broom_Bridge
[07]:https://en.wikipedia.org/wiki/History_of_quaternions
[08]:https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation
