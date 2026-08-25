# MicroPython vs. CircuitPython

In this class, your Raspberry Pi Pico 2 W runs CircuitPython. But you'll see the name
"MicroPython" all over the internet, in forum posts, and on other boards. What's the
difference, and why did we pick the one we picked? This doc explains both languages — where
they came from, what they share, where they split apart, and when you'd reach for one over
the other.

## The problem they both solve

Before either of these existed, if you wanted to program a microcontroller — the tiny chip
inside a robot, a smart thermostat, or a blinking LED badge — you almost always wrote in C or
C++. That's powerful, but it's also slow to work with. You have to compile your code into a
binary file, upload that whole file to the chip, and if you got one thing wrong, you edit,
recompile, and re-upload the whole thing again. For a beginner, that loop can take a minute
per tiny change. It's not a great way to learn, and it's not even a great way for professionals
to experiment quickly.

Python, on the other hand, is interpreted — you write a line, it runs, you see what happened,
you adjust. No compiling, no waiting. The catch is that classic Python needs an operating
system and megabytes of memory to run, and a microcontroller like the one on your Pico has
neither. It has kilobytes of RAM, not gigabytes, and no OS at all.

MicroPython was built to close that gap: a real Python interpreter, small enough to fit and
run directly on a bare microcontroller chip.

## Where MicroPython came from

MicroPython was created by Damien George, an Australian physicist, who launched it as a
[Kickstarter campaign][01] in 2013. The pitch was straightforward: shrink Python down until it
fits inside a chip with less memory than a single photo on your phone. The campaign was funded,
Damien built it, and MicroPython has been developed as an open-source project ever since —
meaning anyone can read its code, suggest changes, or build their own version of it. It's not
owned by one company; it's maintained by a community of contributors around the world, with
Damien still as the lead maintainer.

MicroPython isn't tied to one company's hardware. Chip makers and board designers add support
for it to their own products, so you'll find it running on boards from Espressif (ESP32),
STMicroelectronics, and many others — including, underneath everything, the Raspberry Pi Pico
itself.

## Where CircuitPython came from

A few years later, the company [Adafruit Industries][02] — which makes electronics kits and
parts for makers and hobbyists — took MicroPython's source code and forked it. "Forking" means
they copied the project and started developing their own version in parallel, rather than
changing the original. Adafruit's goal was specific: make a version of MicroPython that's as
easy as possible for a *beginner*, especially a young one, to get something working in the
first five minutes.

CircuitPython is still open source, and it still shares a lot of underlying code with
MicroPython, but Adafruit controls its direction and tunes every decision toward the same
question: what will make an 11-year-old succeed on their first try?

## What they have in common

Strip away the branding and both languages are close cousins:

- Both are real Python — mostly compatible with the Python 3 syntax you'd learn on a laptop.
  If you know `for` loops, `if` statements, and functions from regular Python, you already know
  most of MicroPython and CircuitPython.
- Both run *directly on the chip*, with no separate computer needed once the code is loaded.
- Both let you edit code and see it run in seconds, without compiling.
- Both are free and open source.
- Both were built to solve the exact same problem: making microcontrollers approachable to
  people who aren't professional embedded-systems engineers.

## Where they diverge

The differences are mostly about *who Adafruit designed CircuitPython for.*

**Getting code onto the board.** This is the biggest practical difference, and it's the one
you'll feel first. With CircuitPython, you plug the board into your computer over USB and it
shows up like a USB flash drive — a folder you can see in your file browser. You save a file
named `code.py` into that folder, and the instant you hit save, the board reloads and runs it.
No special software required beyond a text editor. MicroPython doesn't do this out of the box —
you typically use a separate tool (like Thonny or `mpremote`) that talks to the board over a
serial connection to upload and run files. It's not hard, but it's an extra piece of software
and an extra step that CircuitPython skips.

**Built-in libraries.** CircuitPython ships with a huge collection of ready-made libraries for
specific sensors, displays, and other parts — much of it from Adafruit's own product line — so
plugging in a sensor and reading it often takes three or four lines of code. MicroPython has
libraries too, but the ecosystem is more spread out across the community, and you'll more often
be pulling in a library written by some other MicroPython user rather than one that's officially
supported.

**Who's steering it.** MicroPython is community-governed open source — its features and
direction come from whoever's contributing at the time. CircuitPython is a community project
too, but Adafruit product decisions and beginner-friendliness are the compass it steers by.

**Board support.** MicroPython supports a broader range of chips and boards, including many
used in industry and by advanced hobbyists. CircuitPython supports fewer boards, but the ones
it supports (including your Pico 2 W) tend to be very well documented and beginner-tested.

**Performance.** MicroPython is generally a bit faster and leaner, since it doesn't carry
CircuitPython's beginner conveniences. For the projects in this class, that difference won't
matter — but it's why a professional building a battery-powered sensor that needs to sip power
for a year might reach for MicroPython instead.

## When to reach for which

- **Pick CircuitPython** when you're new to hardware, want the fastest possible path from
  "plug it in" to "it's blinking," and want official, well-tested libraries for common sensors
  and parts. This is why we use it in this class.
- **Pick MicroPython** when you need to run on a board CircuitPython doesn't support, you want
  maximum performance or the smallest possible memory footprint, or you're working somewhere
  the community's MicroPython libraries fit your project better than Adafruit's.

In practice, the two are close enough that skills transfer almost completely. Learning
CircuitPython here means you'll be able to pick up MicroPython on some other board later with
almost no relearning.

## Who actually uses these

MicroPython and CircuitPython both show up in three overlapping groups:

1. **Students and hobbyists** — this is CircuitPython's home turf. Makerspaces, classrooms, and
   weekend tinkerers building robots, wearables, and blinking-light art.
2. **Makers and artists** building one-off interactive projects — museum installations,
   costumes, art pieces — where getting something working matters more than squeezing out
   every last bit of performance.
3. **Engineers and companies prototyping quickly.** Before committing to a "real" C/C++
   firmware for a product, engineers will often rough out the logic in MicroPython because
   it's so much faster to iterate. A few companies even ship MicroPython in production for
   low-volume or non-performance-critical devices.

Full-time embedded/firmware engineers building high-volume commercial products (game
controllers, cars, medical devices) still mostly write in C or C++ for production, even if they
prototype in Python first.

## How this compares to C++

This is the part that matters most for understanding *why* your Pico feels so different from
an old-school microcontroller project:

- **Compiled vs. Interpreted.** C++ code must be translated ("compiled") into machine code
  *before* the chip can run it — a separate step, done on your computer, that can take anywhere
  from seconds to minutes depending on the project. MicroPython and CircuitPython run your code
  *directly*, line by line, as soon as you save it. That's the whole reason your edit-run loop
  in this class is so fast.
- **Manual vs. Automatic memory management.** In C++, you are personally responsible for
  requesting and releasing every chunk of memory your program uses. Forget to release it, and
  you get a "memory leak" that can crash the device after running for a while — a real and
  common bug even for experienced programmers. Python (both flavors) handles this for you
  automatically with something called a garbage collector, which quietly frees memory you're no
  longer using.
- **Forgiving vs. Strict.** C++ demands you declare the exact type of every variable
  (`int`, `float`, `bool`, ...) and will refuse to compile if you get it wrong. Python lets you
  skip that — you just assign a value and Python figures out the type. This makes Python far
  more forgiving for a beginner, though it also means some mistakes that C++ would catch before
  you ever run the code won't show up in Python until the program actually hits that line.
- **Speed + Control vs. Speed of learning.** C++ compiles down to code that runs about as
  fast as the hardware physically allows, and gives you fine-grained control over exactly how
  memory and timing work. That's why it's still the default for products that need to run for
  years on a coin battery, respond in microseconds, or ship by the millions. MicroPython and
  CircuitPython trade some of that raw speed and control for a dramatically shorter path from
  idea to working project — which is exactly the trade you want while you're learning.

Put simply: C++ is built for squeezing the most performance out of a chip, at the cost of a
slower, stricter workflow. MicroPython and CircuitPython are built for squeezing the most
learning and iteration speed out of *you*, the programmer, at a modest cost in raw performance —
a cost your Pico 2 W has plenty of headroom to absorb for everything you'll build in this
class.

- To learn more, subscribe to [The Python on Microcontrollers Newsletter][03]
- [MicroPython and CircuitPython: Pythons Quiet Takeover of IoT and Robotics][04]



[01]:https://www.kickstarter.com/projects/214379695/micro-python-python-for-microcontrollers
[02]:https://www.adafruit.com/
[03]:https://www.adafruitdaily.com/
[04]:https://arxiv.org/pdf/2608.18160

