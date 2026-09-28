# What Is an IMU, and What Does a Mahony Filter Do?
> **Part 1 of 3.** This doc → [What Is Gimbal Lock?][02] (part 2) →
> [What Are Quaternions, and Why Use Them?][03] (part 3).

In Class 4 you add a small sensor board to your rover: the
[Adafruit 9-DOF IMU LSM9DS1 Breakout Board (STEMMA)][01]. Its job is to answer a question every
moving robot eventually asks: *which way am I tilted, and which way am I facing?* A rover that
knows it's tipping over a curb, or that it just turned 90° instead of 45°, can make much better
decisions than one that only knows how fast its wheels spin.

The catch is that the board doesn't actually tell you "tilted 12°, facing north-east." It gives
you a stream of raw measurements, and your Pico has to turn those into an orientation. The math
that does that is called a **sensor fusion filter**, and the one you run in Class 4 is the
**Mahony filter**. This doc explains the sensor, why its raw output isn't enough, how the Mahony
filter fixes that, and how Mahony compares to the other famous filters: Madgwick, Kalman, and
the Extended Kalman filter.


## What an IMU is
**IMU** stands for **inertial measurement unit**: a package of motion sensors that measure how
the board itself is moving, without looking at anything outside it. The LSM9DS1 contains three
sensors, each measuring along three axes (x, y, z):

1. **Gyroscope**: measures *angular rate*, meaning how fast the board is spinning around each
   axis, in degrees (or radians) per second. Spin the board a quarter turn in one second and the
   gyro reads about 90°/s on that axis, then drops back to about 0 when you stop.
2. **Accelerometer**: measures *linear acceleration*, and that always includes gravity. Sitting
   still on a table, it reads about 1 g pointing straight down. Tilt the board and that 1 g
   shifts between the axes, which is how it senses which way is down.
3. **Magnetometer**: measures the Earth's magnetic field, so it works as a 3-axis compass
   pointing (roughly) north.

Three sensors times three axes is nine measurements, which is where **9-DOF** ("nine degrees of
freedom") comes from. An IMU with only a gyro and accelerometer is called **6-DOF**. The LSM9DS1
talks to the Pico over I2C, and its ranges are selectable: ±2 to ±16 g for the accelerometer,
±245 to ±2000 °/s for the gyro, and ±4 to ±16 gauss for the magnetometer.


### Some IMUs do the math for you — this one doesn't
A few IMU chips, like the Bosch **BNO055** and the CEVA **BNO085**, have a small processor built
in that runs sensor fusion on the chip and hands you a finished orientation. They're convenient,
but the fusion is a sealed box. The LSM9DS1 has no fusion processor: it only gives raw readings,
so **the Pico has to do the math.** That's a deliberate choice for this course: you get to see,
and tune, the filter yourself.


## What IMUs are good for
You almost certainly carry one. Your phone's IMU is what flips the screen when you turn it
sideways and what counts your steps. Game controllers like the Wii Remote and Nintendo Switch
Joy-Cons use one to turn a swing of your arm into a swing of a tennis racket. A drone reads its
IMU hundreds of times a second to stay level in the wind, and a VR headset uses one to move the
virtual world the instant you turn your head. The Apollo spacecraft that flew to the Moon had a
much bigger, heavier IMU, and one of its quirks is the star of [What Is Gimbal Lock?][02].

On the rover, the IMU lets it notice that it's climbing a ramp or tipping on a bump, and check
that a "turn 90°" command really produced 90° of turn instead of trusting the wheels, which slip.


## The problem: rates and vectors are not angles
Here's the key idea: **none of the three sensors directly measures an angle.** The gyro gives a
*rate* (degrees per second). The accelerometer gives a *direction* (where down is). The
magnetometer gives a different *direction* (where north is). To get "which way am I facing," you
have to combine them, and each one has a flaw:

- **The gyro drifts.** To turn a rate into an angle, you add it up over time (every 20 ms,
  angle += rate × 0.02 s). But every gyro has a small **bias**: it reads a tiny rotation even
  when perfectly still. Adding up a bias of just 0.5°/s gives a 30° error after one minute, even
  if the board never moved.
- **The accelerometer is noisy.** It knows which way is down only when the board isn't being
  shoved around. Every bump, motor start, or turn adds forces that look like tilt.
- **The magnetometer is easily fooled.** Motors, steel table legs, and battery wires all bend the
  magnetic field around the rover.

So the gyro is smooth and fast but wanders off over time, while the accelerometer and
magnetometer don't wander but jitter and get fooled in the short term. Their strengths and
weaknesses are exact opposites, which is what makes combining them work. (And once you do have an
orientation, how you *store* it matters too; that's the subject of [What Are Quaternions, and Why Use Them?][03].)


### Analogy 1: walking with your eyes closed
Close your eyes and walk across a room. You can feel each turn and count your steps, so for a few
seconds you know roughly where you are; that's the gyro. But every small misjudgment piles on the
last, and after thirty seconds you're confidently walking into a wall. That pile-up is **drift**.
Now open your eyes for a split second every few steps. A quick glance at the room is enough to
correct your mental position before the error grows. That glance is the accelerometer and
magnetometer.


### Analogy 2: speedometer and compass vs. a navigator
A raw IMU is like a car's **speedometer and compass**: it tells you how fast you're turning, which
way is down, and which way is north. It does *not* tell you where you're facing right now. Sensor
fusion is the **navigator** in the passenger seat doing the running arithmetic: "we've been
turning left at 10°/s for 3 seconds, so we're about 30° left of where we started, and the compass
agrees, so I trust it."


## What the Mahony filter does
The **Mahony filter**, from a 2008 paper by [Robert Mahony, Tarek Hamel, and Jean-Michel
Pflimlin][04], is that navigator. In plain English, every loop it does three things:

1. **Trust the gyro for the short term.** It adds up the gyro's rotation rate to update its
   orientation estimate. This is smooth and responds instantly.
2. **Check against the references.** It asks: "Given the orientation I think I have, where
   *should* down be (and, with a magnetometer, where should north be)?" Then it compares that to
   where the accelerometer (and magnetometer) says they actually are. The mismatch is the
   **error**.
3. **Nudge toward the references for the long term.** It feeds a small correction, sized by that
   error, back into the gyro rates before adding them up. Over many loops this pulls drift back
   out, without letting the accelerometer's jitter take over.

Two tuning knobs control the nudge, and they're the two constants at the top of your Class 4 code:

- **`MAHONY_KP` (proportional gain): how hard to nudge.** Too low and the gyro drift wins, so the
  estimate slowly wanders. Too high and the filter chases every bump the accelerometer feels, so
  the estimate jitters. Class 4 starts at `2.0` and has you tune it live to feel that
  drift-vs-jitter tradeoff.
- **`MAHONY_KI` (integral gain): learns the steady gyro bias.** If the error keeps pointing the
  same way loop after loop, that's probably bias, not motion. The integral term slowly adds it up
  and subtracts it out for good. Class 4 uses a small `0.05`.

(If you've met control systems before: this is a PI, or proportional-integral, controller
steering the gyro toward what gravity and north say is true.)

Inside, the filter doesn't store roll, pitch, and yaw. It stores orientation as a **quaternion**,
four numbers that describe any 3D rotation without the trouble spots where angle-based math
breaks, and only converts to roll/pitch/yaw at the very end, for printing and display. Why
quaternions are the better bookkeeping is explained in [What Are Quaternions, and Why Use Them?][03];
the specific failure they avoid, where two rotation axes line up and you lose a degree of freedom,
is covered in [What Is Gimbal Lock?][02].


### Why your yaw still drifts in Class 4
The general Mahony filter fuses all three sensors (a 9-DOF fusion). The Class 4 code currently
fuses only the **accelerometer and gyro**. Gravity pins down roll and pitch, but spinning the
board flat on a table doesn't change which way is down, so the accelerometer has no opinion about
**yaw**, and nothing anchors it to north. That's the slow yaw drift you see in Phase 1. Phase 3's
gyro bias calibration slows it way down; adding the magnetometer as a north reference is what
stops it for good, and that's exactly what Class 5 does. One catch: the rover's motors, battery,
and steel screws bend the magnetic field, so the magnetometer has to be calibrated on the finished
rover, not the bare breadboard.


## The family of filters: Mahony, Madgwick, Kalman, EKF
Mahony isn't the only way to fuse an IMU. Here are the main alternatives, from simplest to
heaviest.

**Complementary filter (the ancestor).** The simplest fusion there is:
`angle = 0.98 × (angle + gyro_rate × dt) + 0.02 × accel_angle`. Take mostly the gyro, blend in a
little accelerometer every loop. It works well for one or two tilt angles and is a few lines of
code. The Mahony filter is really a *nonlinear complementary filter*: the same "gyro short-term,
reference long-term" idea, extended to full 3D rotation with a quaternion and the bias-learning
`KI` term.

**Madgwick filter.** Published by [Sebastian Madgwick in 2010][05], it also stores a quaternion
and trusts the gyro short-term. The difference is how it corrects. Picture walking downhill in
thick fog: you can't see the bottom, but you can feel which way the ground slopes under your
feet, so you take one step in the steepest downhill direction, then feel again. Madgwick does
that every loop (the technique is called *gradient descent*): it takes one small step in whichever
direction makes the gap between predicted and measured gravity/north shrink fastest. It has a
single gain (`beta`) and is about as cheap as Mahony. The report does describe an optional
gyro-bias compensation term, but the widely copied basic version skips bias learning.

**Kalman filter.** Invented by [Rudolf Kálmán in 1960][06], it keeps track of not just its best
guess but *how sure it is* of that guess, and each loop it trusts whichever source, its own
prediction or the new sensor reading, is more trustworthy right now. A worked example:

- The gyro-based prediction says the tilt is **30°**, but it's not very sure: **±4°**.
- The accelerometer says **34°**, and it's more sure: **±2°**.
- The Kalman filter blends them, weighted by trust, to about **33°**, and its new uncertainty,
  about **±1.8°**, is smaller than either source alone.

The catch: the classic Kalman filter assumes the system is **linear**, meaning doubling the input
doubles the output. Rotation isn't like that: turning twice as far doesn't simply double the
x, y, and z readings.

**Extended Kalman filter (EKF).** The EKF handles this by pretending the system is linear just
for a tiny moment around its current guess, doing one Kalman step, and then re-doing that
approximation every loop. Engineers at NASA Ames, led by Stanley Schmidt, developed this approach
in the early 1960s, and a Kalman-style filter [flew in the Apollo guidance computer][07] to
navigate to the Moon. Today EKFs run in drones, phones, and aircraft. They can estimate bias,
sensor noise, and even position all at once, but they need matrix math (multiplying and
inverting grids of numbers) every loop, plus carefully tuned tables of how noisy each sensor is.

| Filter | Core idea | Tuning knobs | Cost on a tiny microcontroller | Good for |
| --- | --- | --- | --- | --- |
| Complementary | Weighted blend of gyro angle and accel angle | 1 blend factor | Tiny: a few multiplies | Single-axis tilt, balancing bots |
| Mahony | Gyro plus a proportional + integral nudge toward gravity/north; quaternion state | `KP`, `KI` | Low: a few dozen multiplies, no matrices | Hobby robots, drones, this course |
| Madgwick | Gyro plus one downhill step toward gravity/north; quaternion state | `beta` | Low: similar to Mahony | Wearables, hobby drones, motion capture |
| Kalman | Tracks how sure it is and trusts the more trustworthy source; linear systems only | Tables of how noisy each sensor is | Moderate: small matrix math | Linear problems: smoothing a noisy sensor, GPS position |
| Extended Kalman (EKF) | Kalman filter re-approximated as linear around the current guess each loop | Tables of how noisy each sensor is (many) | High: matrix multiply and inverse every loop | Spacecraft, aircraft, phones; fusing many sensors at once |


### Why Mahony for this course
Four reasons:

1. **It's readable.** The whole filter is one short `mahony_update()` function you can follow
   line by line, with no matrix library.
2. **It's cheap.** CircuitPython is interpreted and slower than C; Mahony still keeps up at about
   50 updates per second on the Pico.
3. **Its knobs mean something.** `MAHONY_KP` is "how hard to nudge" and `MAHONY_KI` is "learn the
   bias." You can predict what changing each one will do, then watch it happen.
4. **It learns bias out of the box.** The `KI` term tackles the gyro's biggest real-world flaw,
   which the widely copied basic Madgwick code skips.

A Kalman filter is the professional heavyweight and worth learning later, but for a rover that
needs to know roughly which way it's tilted and facing, Mahony gets you 90% of the result for 10%
of the complexity.


## Key takeaways
- An IMU measures *rates* (gyro) and *directions* (gravity from the accelerometer, north from the
  magnetometer), not angles; the LSM9DS1 leaves the math to the Pico.
- The gyro is smooth but drifts; the accelerometer and magnetometer don't drift but are noisy.
  Fusion keeps the best of both.
- The Mahony filter trusts the gyro short-term and nudges toward down and north long-term:
  `MAHONY_KP` sets how hard it nudges, `MAHONY_KI` learns the gyro's bias.
- Class 4 fuses only the accelerometer and gyro, so yaw has no north reference and slowly drifts.
- Complementary, Mahony, and Madgwick are cheap enough for the Pico; Kalman and EKF are more
  powerful but need heavier matrix math.


## Where to go next
- [What Is Gimbal Lock?][02]: roll, pitch, and yaw defined, and why they break at certain angles.
- [What Are Quaternions, and Why Use Them?][03]: the four-number rotation format the Mahony
  filter stores internally.

Sources:

- [Adafruit 9-DOF IMU LSM9DS1 product page][01]
- [Mahony, Hamel, and Pflimlin, "Nonlinear Complementary Filters on the Special Orthogonal Group" (2008)][04]
- [Madgwick, "An efficient orientation filter for inertial and inertial/magnetic sensor arrays" (2010)][05]
- [Kalman filter overview][06]
- [NASA: math invented for the Moon landing][07]
- [Extended Kalman filter overview][08]


[01]:https://www.adafruit.com/product/4634
[02]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/blob/main/explainers/what-is-gimbal-lock.md
[03]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/blob/main/explainers/what-are-quaternion-and-why-use-them.md
[04]:https://memsic.ccsd.cnrs.fr/UNICE/hal-00488376
[05]:https://www.semanticscholar.org/paper/An-efficient-orientation-filter-for-inertial-and-Madgwick/bfb456caf5e71d426bd3e2fd529ee833a6c3b7e7
[06]:https://en.wikipedia.org/wiki/Kalman_filter
[07]:https://www.nasa.gov/aeronautics/math-invented-for-moon-landing-helps-your-flight-arrive-on-time/
[08]:https://en.wikipedia.org/wiki/Extended_Kalman_filter
