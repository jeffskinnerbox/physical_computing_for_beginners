# What Is Gimbal Lock?
> **Part 2 of 3.** [What Is an IMU, and What Does a Mahony Filter Do?][01] (part 1) → this doc →
> [What Are Quaternions, and Why Use Them?][02] (part 3).

In Class 4 your Pico reads an [IMU (inertial measurement unit)][01] and prints three numbers about
50 times a second: `roll`, `pitch`, and `yaw`. Those three numbers feel like the most natural way
to describe how something is tilted — and most of the time they are. But hidden inside them is a
strange trap called **gimbal lock**: at certain angles, one of your three numbers stops meaning
anything useful. The same trap nearly caused real trouble for astronauts on their way to the
Moon. This document explains what roll/pitch/yaw actually are, where the trap comes from, why
NASA had to fly around it during Apollo, where it still shows up today, and why your rover mostly
doesn't have to care.


## Describing a tilt with three numbers
Any object floating in space — an airplane, a phone, your rover — can rotate three different
ways. The classic names come from aviation:

1. **Roll** — tipping side to side, like an airplane dipping one wing. The rotation is around
   the line running from the nose to the tail.
2. **Pitch** — tipping nose up or nose down, like a plane climbing or diving. The rotation is
   around the line running from wingtip to wingtip.
3. **Yaw** — turning left or right while staying flat, like a car steering around a corner.
   The rotation is around the line running straight up and down.

These three angles together are called **Euler angles** (pronounced "OY-ler," after the
18th-century mathematician Leonhard Euler). The idea is simple: start with the object sitting
level and facing forward, then apply a yaw turn, then a pitch tilt, then a roll tilt, one after
another. Three numbers, three steps, and you can reach any orientation there is.

There's one catch hiding in "one after another": **the order matters**. Hold a book flat, yaw it
90° then pitch it 90°, and note where it ends up. Reset, then pitch first and yaw second. The
book lands in a different position. Euler angles only make sense when everyone agrees on the
order — and that step-by-step recipe is exactly what sets up the trap.


## Gimbals: Euler angles you can hold in your hand
A **gimbal** is a ring that pivots on a single axis. Nest three of them — a ring inside a ring
inside a ring, each pivoting at right angles to the one around it — and you get a mount that
lets whatever sits in the middle point any direction while the outside frame moves freely.
Ship compasses, camera stabilizers, and old-school spacecraft navigation platforms all use
this trick.

A three-gimbal mount is basically Euler angles built out of metal. The outer ring handles one
rotation, the middle ring handles the second, and the inner ring handles the third. Reading the
angle of each ring gives you three numbers that describe the orientation — the same kind of
three numbers your rover prints.


## The trap: when two axes line up
Here's the problem. Turn the middle ring 90°, and the inner ring's pivot axis swings around
until it lines up perfectly with the outer ring's pivot axis. Now two rings spin around the
*same* line. Three rings, but only two different directions of rotation left. The mount has
lost one of its three **degrees of freedom** (independent ways to move). If the outside frame
now tries to twist in that missing direction, no ring can swing to absorb it — the middle object
gets dragged along. That's **gimbal lock**.

The math version works exactly the same way. With Euler angles, when pitch hits exactly +90°
or −90° (nose pointing straight up or straight down), the yaw axis and the roll axis line up.
Roll and yaw become the *same motion*. There are suddenly infinitely many combinations of roll
and yaw that describe the exact same orientation, and a small real-world wiggle can make the
computed roll and yaw numbers jump wildly.

It helps to separate the two versions:

- **Mechanical gimbal lock** happens to real, physical rings. The hardware genuinely can't
  follow the motion, and whatever the rings were holding steady gets knocked out of position.
- **Mathematical gimbal lock** happens to Euler-angle numbers in software. Nothing physical
  breaks, but the three numbers stop being a trustworthy, unique description of the orientation
  near pitch ±90°, and formulas that divide by the cosine of pitch (which is zero at 90°) blow up.


## Try it yourself
**With your hand.** Hold your hand flat, palm down, fingers pointing forward — your fingers are
the "nose." Now pitch your hand up until your fingers point straight at the ceiling. From here,
try a "yaw" (turning left/right around the vertical line) and then a "roll" (twisting around
the line your fingers point along). Both twist your hand around the same up-down line. At pitch
90°, roll and yaw have become one motion.

**With a phone.** Many phones have a level or compass app that shows roll/pitch/yaw-style
readouts. Stand the phone straight up on its bottom edge, then slowly tip it past vertical. Watch
for a reading that suddenly jumps 180° or flickers around even though the phone barely moved.

**With the Class 4 3D viewer.** Run the Pico code with the Phase 2 `wireframe.py` 3D viewer open
on your laptop (it reads the Pico's roll/pitch/yaw CSV over USB). Tilt the board until its front
points straight up (pitch near 90°) and watch the `roll, pitch, yaw` numbers: roll and yaw may
swing or trade values even though you're barely moving the board. That's mathematical gimbal
lock showing up in the Euler-angle *output* — the filter itself keeps tracking fine underneath,
for reasons covered below.


## Apollo: gimbal lock was a real problem
For the Apollo Moon missions, gimbal lock wasn't a numbers glitch — it was hardware. Both the
Command Module and the Lunar Module navigated using an **Inertial Measurement Unit (IMU)**. It
measured the same kinds of things as your rover's chip — rotation with gyroscopes, pushes and
pulls with accelerometers ([see the IMU explainer][01]) — but instead of a fingernail-sized chip,
it was a metal ball about a foot across ([Smithsonian: Apollo 17 IMU][03]). Inside, the sensors
sat on a platform held perfectly still relative to the stars by three nested gimbals while the
spacecraft rotated around it. The spacecraft read the ring angles to know which way it was
pointing. The whole guidance system — the Apollo Guidance Computer, its **DSKY** keypad-and-display,
the engines' steering — trusted that platform.

If the middle gimbal swung too close to 90°, the inner and outer gimbal axes lined up, and the
platform could get knocked out of its careful alignment. Losing it meant the spacecraft no
longer knew its orientation. Getting it back required re-aligning the platform by sighting
stars through the spacecraft's optics (a sextant in the Command Module, an alignment telescope
in the Lunar Module) — slow, fiddly work you definitely don't want to be doing in the middle of
an engine burn or a docking.

**How they avoided it.** Instead of eliminating the problem, the engineers built a warning
system and trained the crews to fly around it. The [Apollo Lunar Surface Journal's gimbal
page][04] describes it: the computer lit a gimbal-lock warning when the middle gimbal reached
70°, and at 85° it froze the platform and lit a "NO ATT" (no attitude) light, forcing a
realignment. The DSKY even had a dedicated **GIMBAL LOCK** warning lamp. Astronauts learned to
plan maneuvers that stayed away from that forbidden zone, sometimes taking the long way around
to get to a new attitude.

**"A fourth gimbal for Christmas."** On Apollo 11, about two hours after Eagle landed, Mission
Control warned Michael Collins — alone in the Command Module Columbia, orbiting the Moon — that
his maneuver was taking him close to gimbal lock. Collins, clearly tired of dodging it, radioed
back: "How about sending me a fourth gimbal for Christmas?" ([Gimbal lock, Wikipedia][05]).

**Apollo 13.** After the oxygen tank explosion, the crew moved into the Lunar Module Aquarius and
powered down nearly everything to save battery. Commander Jim Lovell had to maneuver the awkward,
lopsided stack of two docked spacecraft without letting it drift into gimbal lock — at one point
telling Mission Control, "We're having trouble maneuvering, Joe, without getting it in gimbal
lock." Losing the platform there would have been serious, because debris floating around the
crippled ship made it hard to sight stars for a realignment
([Universe Today: Avoiding Gimbal Lock][06]).


## Why not just add a fourth gimbal?
A fourth gimbal fixes mechanical gimbal lock: an extra ring can be driven to keep the other
three from ever lining up. NASA had already flown one — the Gemini spacecraft's Honeywell
inertial platform used [four gimbals][07]. But for Apollo, MIT's designers argued hard for the
simpler three-gimbal unit. The official reasoning was that the advantages of a redundant gimbal
were "outweighed by the equipment simplicity, size advantages, and corresponding implied
reliability" of the three-gimbal design. Fewer rings meant less weight, fewer motors and
bearings that could fail, and — critically — a unit they could finish in time to meet President
Kennedy's end-of-the-decade deadline ([ALSJ][04]).


## Why not just use better math?
Today's standard fix for gimbal lock is a different way of storing orientation called a
**quaternion** — four numbers instead of three, with no angle where it breaks (that's the story
of [What Are Quaternions, and Why Use Them?][02]). So why didn't Apollo just use one?

1. **Apollo's lock was physical.** Math only fixes the math version. When real metal rings line
   up, the platform itself loses a degree of freedom — no software can make a ring rotate around
   an axis it doesn't have. Only more gimbals, or no gimbals at all, fixes that.
2. **The computer was tiny.** The Apollo Guidance Computer had about 2,048 words of working
   memory and ran many thousands of times slower than your phone. Every calculation had to earn
   its place.
3. **1960s engineering habits.** Quaternions existed (they date back to 1843), but Euler angles
   and ring angles were what aerospace engineers, instruments, and astronauts already knew and
   trained with. Quaternions became standard in spacecraft and games later.


## Is gimbal lock still a problem today?
Yes — just in different places, and usually as a known hazard that designers work around.

- **Real gimbals.** Motorized camera stabilizers and drone camera mounts are still three nested
  rings, so the same geometry applies. Designers choose the ring order and add range limits so
  normal shots stay far away from the lined-up position.
- **3D animation.** Tools like Blender and Maya let animators choose Euler or quaternion rotation
  modes. Animate a character's arm or a spaceship in Euler mode past a 90° tilt and it can
  suddenly flip or wobble between keyframes — the [Blender manual][08] warns about exactly this
  and offers quaternion mode as the fix.
- **Video game cameras.** First-person games usually store where you're looking as yaw and
  pitch, then quietly stop you at about ±89° pitch so the camera never reaches straight up or
  down, where it would flip. The popular [LearnOpenGL camera tutorial][09] clamps pitch to
  ±89° for this reason.
- **Drones.** A drone doing flips points straight up and straight down all the time, so
  flight-control software such as ArduPilot [tracks orientation as a quaternion][10] and only
  uses roll/pitch/yaw for the numbers shown to the pilot.


## Why your rover (mostly) doesn't care
Your rover's LSM9DS1 is a **strapdown MEMS IMU**. "MEMS" (micro-electro-mechanical systems)
means its sensors are microscopic machines etched into a silicon chip. "Strapdown" means those
sensors are bolted straight to the rover and rotate right along with it — there are no rings;
the math does the job the rings used to do. With no gimbals to line up, mechanical gimbal lock
is impossible — only the math version is left. And the Class 4 Mahony filter already dodges that
by tracking orientation internally as a quaternion, only converting to roll/pitch/yaw at the very
end for display. The filter's real orientation estimate never glitches; only the three printed
numbers can look odd near pitch ±90°. For how the chip and filter work, see
[What Is an IMU, and What Does a Mahony Filter Do?][01]; for why quaternions dodge the trap, see
[What Are Quaternions, and Why Use Them?][02].


## Key takeaways
- Euler angles (roll, pitch, yaw) describe a tilt as three rotations in a row; when the middle
  one hits 90°, the other two collapse into the same motion — that's gimbal lock.
- Mechanical gimbal lock happens to real rings; mathematical gimbal lock happens to Euler-angle
  numbers in software.
- Apollo's three-ring IMU could really lock, so crews flew around a forbidden zone (warning at
  70°, freeze at 85°) instead of NASA adding a fourth gimbal.
- Gimbal lock still shows up in camera gimbals, animation tools, and game cameras; quaternions
  are the standard fix.
- Your rover's strapdown chip has no rings, and its filter thinks in quaternions, so only the
  printed roll/pitch/yaw numbers can act strange near pitch ±90°.


## Where to go next
- [What Is an IMU, and What Does a Mahony Filter Do?][01] — part 1: the rover's sensor chip,
  rates vs. angles, and how the filter blends gyro and accelerometer readings.
- [What Are Quaternions, and Why Use Them?][02] — part 3: the four-number way to store
  orientation that never hits gimbal lock.
- Sources: [Smithsonian: Apollo 17 IMU][03] · [Apollo Lunar Surface Journal: gimbals][04] ·
  [Gimbal lock, Wikipedia][05] · [Universe Today: Avoiding Gimbal Lock][06] ·
  [Smithsonian: Gemini inertial platform][07] · [Blender manual: rotation modes][08] ·
  [LearnOpenGL: Camera][09] · [ArduPilot quaternion attitude control][10]


[01]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/blob/main/explainers/what-is-an-imu-and-mahony-filter.md
[02]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/blob/main/explainers/what-are-quaternion-and-why-use-them.md
[03]:https://airandspace.si.edu/collection-objects/inertial-measurement-unit-apollo-17/nasm_A19770228000
[04]:https://www.apollojournals.org/alsj/gimbals.html
[05]:https://en.wikipedia.org/wiki/Gimbal_lock
[06]:https://www.universetoday.com/articles/13-more-things-that-saved-apollo-13-part-9-avoiding-gimbal-lock
[07]:https://www.si.edu/object/nasm_A19770604000
[08]:https://docs.blender.org/manual/en/latest/advanced/appendices/rotations.html
[09]:https://learnopengl.com/Getting-started/Camera
[10]:https://discuss.ardupilot.org/t/arducopter-quaternion-based-attitude-control/23554
