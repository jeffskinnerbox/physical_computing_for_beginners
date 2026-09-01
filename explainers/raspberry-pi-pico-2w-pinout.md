# What Is a Pinout? (And Where to Find the Pico 2 W's)

Every time you've wired something in this class — a button to `GP2`, an encoder to `GP3` and
`GP4`, an LED to `GP15` — you've been reading a *pinout* without necessarily calling it that.
This doc explains what that word means, why the map exists at all, how boards and datasheets
communicate it, and how to go find one yourself the next time you pick up a board this class
never covers.

## The problem a pinout solves

Look at your Pico 2 W. It has 40 tiny metal legs sticking out of both sides, and every single
one of them is unlabeled on the board itself — or at best labeled with a cryptic number like
`GP2` silkscreened in tiny print. Nothing about the physical pin tells you what it *does*.
Pin 4 could be a general-purpose input, a power rail like `VBUS` or `3V3 OUT`, a ground
connection, or a pin with a special job like driving analog voltage or carrying a [serial
protocol like SPI, I2C, or UART][03] — and from the pin alone, you can't tell which. (See
[Types of Pins on the Pico 2 W][04] for a full breakdown of every one of those non-`GPnn` labels.)

That's a real problem the moment you try to wire anything. If you guess wrong and connect your
button to a power pin instead of a signal pin, at best nothing happens; at worst you damage the
chip or the button. Multiply that by 40 pins and a handful of different jobs each pin can do,
and "just wire it up and see" stops being a viable strategy.

A **pinout** solves this by giving every physical pin a name and a job, laid out in the same
order the pins actually appear on the hardware. It's the translation layer between "the third
metal leg from the top-left corner" and "this is GPIO 2, and by the way it can also do PWM."

## What a pinout actually is

[Wikipedia defines a pinout][01] as a reference to the correlation between the connector or
device's pins, or "contacts," and their functions. In plain terms: it's a map. One side of the
map is the physical, unlabeled hardware — the actual pins you can touch with a wire. The other
side is the list of jobs those pins can perform — power, ground, digital input/output, analog
input, PWM, and communication protocols like [I2C, SPI, and UART][03], and so on. A pinout draws
the line between the two, pin by pin. Those protocol names will keep showing up in the notes
column of a pinout — this class's own LSM9DS1 sensor and TFT screen are wired to specific pins
*because* those pins are the ones wired internally to the chip's I2C and SPI hardware. If a
pinout label doesn't look like a `GPnn` pin at all — things like `VSYS`, `3V3 EN`, or `ADC
VREF` — those are covered pin-by-pin in [Types of Pins on the Pico 2 W][04].

This isn't unique to microcontrollers. Any connector with more than one contact needs a pinout
to be usable — USB cables, HDMI ports, car stereo wiring harnesses, even the pins on a wall
outlet. Anywhere a device exposes multiple electrical contacts and expects you to hook things
up correctly, someone had to publish a pinout so people could do that without guessing.

## What a pinout is used for

You reach for a pinout at two moments, and you've already done both this class without
thinking about it as "using a pinout":

**Wiring.** Before you connect a wire to a pin, you need to know what that pin does. When you
wired the pushbutton to `GP2` in Class 1, you weren't picking that pin at random — the lesson
script's wiring table told you `GP2` is a general-purpose digital pin safe to use as an input.
A pinout is what makes that table possible: it's the source that says "this specific pin can
do this specific job," so a wiring diagram or instruction sheet can point you to the right
spot instead of you probing the board with a multimeter to find out.

**Writing code.** Once something is physically wired, your code has to refer to the same pin
by name. In CircuitPython, that's a line like:

```python
button = digitalio.DigitalInOut(board.GP2)
```

`board.GP2` only means something because the pinout says GPIO 2 exists and is exposed at a
specific physical location on the board. The code and the wiring have to agree on the same
name for the same physical pin, and the pinout is the shared reference both of them point back
to.

## How a pinout's information gets communicated

There isn't one single format — a pinout shows up in several places, often at the same time,
because different situations call for different levels of detail:

- **Silkscreen labels on the board itself.** That's the small white printing you see next to
  each pin on your Pico 2 W — `GP2`, `GP3`, `3V3`, `GND`, and so on. It's the most convenient
  reference because it's physically attached to the hardware, but it's cramped: there's only
  room to print a short pin name, not what else that pin can do.
- **A labeled diagram.** A picture of the board with every pin's full name and function
  written out next to it, often color-coded by pin type (power pins one color, ground another,
  GPIO another). This is usually the easiest format for a beginner, because you can visually
  match a pin's position on the diagram to its position on the real board in front of you.
- **A pinout table.** The same information as the diagram, but as rows and columns — pin
  number, pin name, function, notes. Tables are easier to search and easier to embed in a
  wiring instruction sheet, which is exactly the format this course's own lesson scripts use
  (see the wiring tables in any `lesson_scripts/class-0N-lesson-script.md` file).
- **A datasheet.** The most complete and most technical source, published by the chip or board
  manufacturer. A datasheet describes every pin's electrical specifications too — not just
  "this is GPIO 2" but voltage limits, current limits, and every alternate function that pin
  can be switched into. Datasheets are the ground truth, but they're written for engineers, not
  beginners, so most people start with a diagram or table instead and only dig into the
  datasheet when they need a detail those don't cover.

## Where to find the Pico 2 W's pinout

For this class's board, the fastest and clearest reference is [pinout.xyz's Pico 2 W page][02].
It's an interactive diagram: hover over or click any pin, and it tells you that pin's name and
every function it supports — general-purpose I/O (GPIO), PWM, [I2C, SPI, UART][03], ADC, power, or
ground. Because it's interactive, you don't have to already know what you're looking for; you
can just point at a pin and ask it "what is this?" If you see one of those three protocol names
next to a pin and want to know what it actually means and why this class uses it, see
[Serial Communication: SPI, I2C, and UART][03] — it explains each protocol and shows the exact
CircuitPython code that talks to a pin over it. And if the label you're hovering over is a power
or control pin instead — `GND`, `VBUS`, `VSYS`, `3V3 EN`, `3V3 OUT`, `ADC VREF`, `ADC GND`, or
`RUN` — see [Types of Pins on the Pico 2 W][04] for what each one is for and how it operates.

If you want the manufacturer's own version, Raspberry Pi publishes an official datasheet for
the Pico 2 W that includes a full pinout diagram and table — the source pinout.xyz's own data
is built from. Reach for that when you need an electrical spec (like a pin's maximum current)
that a simplified diagram doesn't show.

## How to find the pinout for other devices

The Pico 2 W is just one board. Every microcontroller, sensor module, and breakout board you'll
ever pick up has its own pinout, and the good news is the search process is basically the same
every time:

1. **Start with the manufacturer's product page or datasheet.** Search `<exact board name> +
   datasheet` or `<exact board name> + pinout`. Manufacturers know people need this, so it's
   almost always published somewhere official — Raspberry Pi, Adafruit, SparkFun, and
   Espressif all publish pinouts for their boards.
2. **Check for a dedicated pinout site.** Sites like pinout.xyz maintain interactive diagrams
   for popular boards, similar to what you used for the Pico 2 W above. Not every board has
   one, but it's worth a search before you dig into a raw datasheet.
3. **Look at the silkscreen first.** Even without any external reference, the printing on the
   board itself is a rough pinout — enough to identify power, ground, and a handful of
   labeled GPIO pins. It won't tell you every function a pin supports, but it's often enough
   to get a simple project wired.
4. **Fall back to the datasheet for anything a diagram doesn't answer.** If you need to know a
   pin's exact voltage tolerance, maximum current, or a less common alternate function, that
   level of detail usually only lives in the full datasheet.

Once you have the pinout in hand, the process is the same one you've already been doing all
class: match a physical pin to a name, wire it to the right spot, and reference that same name
in your code. If any of the jargon in a pinout — MCU, GPIO, ADC, register, and so on — is
unfamiliar, the [Glossary of Terms for Microcontrollers][05] has a short definition for each one.
And once you know which pin you're after, [What Are Breadboards and Dupont Wires?][06] covers
the actual board and wires you'll use to connect it.

[01]:https://en.wikipedia.org/wiki/Pinout
[02]:https://pico2w.pinout.xyz/#i=ph
[03]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/tree/main/explainers/spi-i2c-uart-serial-communications.md
[04]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/tree/main/explainers/types-of-pins-on-raspberry-pi-pico-2w.md
[05]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/tree/main/explainers/glossary-of-terms-for-microcontrollers.md
[06]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/tree/main/explainers/what-are-breadboards-and-dupont-wires.md

