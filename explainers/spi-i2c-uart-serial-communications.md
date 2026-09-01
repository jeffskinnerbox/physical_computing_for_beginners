# Serial Communication: How Chips Talk to Each Other (SPI, I2C, and UART)

Every sensor and screen you've wired up in this course had to somehow tell the Pico 2 W what
it's sensing, and the Pico had to tell it what to do. That conversation happens over a handful
of standard "languages" called serial protocols. This doc explains what serial communication is,
why microcontrollers depend on it, and breaks down the three you'll actually touch in this
course — UART, I2C, and SPI — including exactly how to reach each one from CircuitPython on the
Pico 2 W. For the physical pins these protocols run over, see the companion doc,
[Raspberry Pi Pico 2 W pinout][01] or reference the [Raspberry Pi Pico 2 W Pinout website][02].
For every other pin label on the board that *isn't* SPI, I2C, or UART — power pins like `GND`,
`VBUS`, and `3V3 OUT`, plus the analog and reset pins — see [Types of Pins on the Pico 2 W][03].
For a shorter, one-paragraph-per-term version of SPI, I2C, and UART alongside every other
microcontroller abbreviation this course uses, see the [Glossary of Terms for
Microcontrollers][04].

## The problem: a chip only has so many legs

Your Pico 2 W's RP2350 chip needs to talk to a lot of other chips — the LSM9DS1 motion sensor,
a TFT display, maybe an SD card. Each of those chips can send and receive many different
pieces of information: X/Y/Z acceleration, rotation, magnetic heading, pixel colors, and so on.

The obvious way to move all that data would be **parallel** — give every single piece of
information its own dedicated wire, and send it all at once, side by side. That's actually how
the earliest computers and printers worked. But it doesn't scale. A sensor that reports 8
different values would need 8+ wires just for data, plus more for power and control. Wire up a
few sensors that way and you've used up every pin the Pico has, and probably built a rat's nest
of jumper wires while you're at it.

**Serial** communication solves this by sending information one bit at a time, in order, down a
single wire (or a small, fixed number of wires), the way you'd read a sentence one letter at a
time instead of seeing every letter flash on a sign simultaneously. It's slower per bit than
parallel, but modern serial links run fast enough that the difference doesn't matter for
sensors, screens, and motor drivers — and it only costs 1-4 wires no matter how much data
you're sending. That trade — a few wires, a strict but fast one-bit-at-a-time order — is why
essentially every sensor, display, and peripheral you'll ever wire to a microcontroller
communicates serially.

## Why serial matters specifically on a microcontroller

A microcontroller like the RP2350 has a limited number of GPIO pins — the Pico 2 W exposes 26
usable ones. Every wire you don't have to run to a sensor is a pin you get to use for something
else. Serial protocols are the reason you can wire an LSM9DS1 (which reports 9 different
measurements) using just 2 pins, or a TFT display (which draws thousands of individually
colored pixels) using around 4-6 pins.

But "serial" isn't one single standard — it's a category. Over the decades, engineers settled
on a handful of specific serial protocols, each tuned for a different job: some prioritize
simplicity, some prioritize speed, some let you chain many devices onto the same two wires.
This course uses three of them: **UART**, **I2C**, and **SPI**. You've technically already used
one without thinking of it as a protocol — every `print()` statement that shows up in Mu's
serial console has been traveling over UART.

## UART — Universal Asynchronous Receiver/Transmitter

**What it stands for:** Universal Asynchronous Receiver/Transmitter. "Asynchronous" is the key
word — more on that below.

**What it's used for:** UART is the simplest of the three, and the one you've been using since
the Pre-Class without realizing it. Every time your `class-0-code.py` heartbeat printed a count
to the serial console, or a lesson script had you read sensor output in Mu's Serial pane, that
text was traveling from the Pico to your laptop over UART, carried across the same USB cable
that powers the board. UART is a point-to-point link: exactly one device talking to exactly one
other device, nothing more.

**How it operates:** UART uses two wires for data — one labeled `TX` (transmit) that carries
outgoing bits, and one labeled `RX` (receive) that carries incoming bits. Each device's `TX`
connects to the other device's `RX`, crossed over, so both sides can talk and listen at the
same time.

The "asynchronous" part means there's no separate clock wire ticking out the timing, the way
I2C and SPI use. Instead, both devices agree in advance on a speed — called the **baud rate**,
typically 115200 bits per second for this class's boards — and each device counts out its own
bits at that agreed pace, trusting the other side is counting at the same speed. It's like two
people agreeing beforehand to speak at exactly one word per second, then each just trusting the
other is keeping pace, instead of one person tapping a metronome the whole conversation. That
simplicity is UART's advantage: only 2 wires, no shared clock signal, and it works over longer
cables than I2C or SPI tolerate — which is exactly why it's the protocol chosen for the
USB-to-laptop link every board in this class already uses.

**How to access it on the Pico 2 W in CircuitPython:** When you plug the Pico into your laptop
and open the Serial console in Mu, you're already using UART — CircuitPython automatically
sends anything passed to `print()` out over the USB serial connection, no extra code required.
If you ever need a *second* UART connection — say, to talk to a GPS module or another
microcontroller instead of your laptop — CircuitPython's `busio` module gives you direct
control:

```python
import busio
import board

uart = busio.UART(board.GP0, board.GP1, baudrate=9600)
uart.write(b"hello\n")
```

## I2C — Inter-Integrated Circuit

**What it stands for:** Inter-Integrated Circuit, usually pronounced "eye-squared-C" or
"eye-two-C."

**What it's used for:** I2C is built for wiring up multiple sensors and small peripherals onto
the same two wires without needing a dedicated pair of pins for each one. This course uses I2C
for exactly one device — the [9-DOF LSM9DS1 IMU breakout board][05] you wire up in Class 4 — but
I2C's real strength is that it doesn't stop at one. Because every device on an I2C bus gets its
own address, you can wire up several I2C sensors to the *same two pins* and the Pico can tell
them apart and talk to each one individually. That's why the LSM9DS1 breakout connects over a
[STEMMA QT cable][06] — Adafruit's snap-together I2C connector standard — instead of individual
jumper wires: it's designed to be one link in a chain of I2C devices you could plug together.

**How it operates:** I2C uses exactly two wires, no matter how many devices are on the bus:
`SDA` (Serial DAta — the actual bits) and `SCL` (Serial CLock — a shared timing signal every
device on the bus watches to know when to read the next bit). That shared clock is what makes
I2C **synchronous**, unlike UART: instead of each device separately counting out bits at an
agreed rate, one device (almost always the microcontroller, called the **controller**) actively
ticks the clock line, and every other device (the **peripherals**, like the LSM9DS1) reads
`SDA` in step with those ticks.

Because multiple peripherals share the same two wires, each one is manufactured with a fixed
**address** — a small numeric ID, like a mailbox number. When the controller wants to talk to a
specific sensor, it starts the conversation by broadcasting that sensor's address on the bus;
every other device ignores the exchange, and only the addressed one responds. That's the trick
that lets I2C scale from 1 device to a dozen without adding a single extra wire.

**How to access it on the Pico 2 W in CircuitPython:** CircuitPython's `board` module exposes
default I2C pins directly — on the Pico 2 W in this course's wiring, `SCL` is `GP1` and `SDA` is
`GP0` (see [Wiring Continuity in the Class 4 lesson plan][07]):

```python
import board
import busio
import adafruit_lsm9ds1

i2c = busio.I2C(board.GP1, board.GP0)  # SCL, SDA
sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
```

Notice the sensor's library (`adafruit_lsm9ds1`) already knows the LSM9DS1's fixed I2C address
internally — you don't have to look it up or type it yourself for a standard Adafruit breakout.
`SDA` and `SCL` only carry data, though — the LSM9DS1 still needs power and ground wired to
`3V3 OUT` and `GND` to actually turn on; see [Types of Pins on the Pico 2 W][03] for what those
pins are and how they work.

## SPI — Serial Peripheral Interface

**What it stands for:** Serial Peripheral Interface.

**What it's used for:** SPI trades I2C's "few wires, many devices" approach for "more wires,
much more speed." It's the protocol of choice whenever a device needs to move a lot of data
quickly — the textbook example being a display, which has to redraw potentially thousands of
pixels many times a second. This course's Class 6 stretch goal — the [1.14" 240×135 ST7789 TFT
status screen][08] — talks to the Pico over SPI for exactly that reason: I2C is too slow to
redraw a screen smoothly, but SPI easily keeps up.

**How it operates:** Where I2C uses 2 wires total, SPI typically uses 4: a shared clock (`SCK`,
same idea as I2C's `SCL`), one line carrying data *out* of the controller (`MOSI` — Controller
Out, Peripheral In), one line carrying data *back into* the controller (`MISO` — Controller In,
Peripheral Out), and a **chip select** line (`CS`, sometimes labeled `SS`) per peripheral. SPI
skips I2C's address system entirely — instead of broadcasting an address on a shared data line,
the controller picks which peripheral it's talking to by pulling that specific device's `CS`
wire low, the way flipping a single light switch (rather than announcing a room number) tells
exactly one room "you're on." Because `CS` is a separate, dedicated wire per device, SPI needs
one extra pin for every additional peripheral you add — the trade for its extra speed.

**How to access it on the Pico 2 W in CircuitPython:** Same `busio` module as I2C and UART, just
with more pins involved:

```python
import board
import busio
import digitalio

spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP16)
cs = digitalio.DigitalInOut(board.GP17)
cs.switch_to_output(value=True)
```

Display libraries like `adafruit_st7789` typically wrap this setup for you, taking the SPI bus
and chip-select pin as arguments rather than requiring you to manage individual bytes.

## Choosing between them

You won't have to pick a protocol from scratch in this course — each lesson script already
wires you to the right one for that sensor or screen — but it helps to know the trade-off each
one is making:

| Protocol | Wires | Speed | Best for |
| :--- | :--- | :--- | :--- |
| UART | 2 (`TX`/`RX`) | Moderate | One-to-one links — this class's USB serial console |
| I2C | 2 (`SDA`/`SCL`), shared by many devices | Slower | Multiple simple sensors on a budget of pins — this class's LSM9DS1 |
| SPI | 4+ (extra `CS` per device) | Fast | High-bandwidth peripherals like displays — this class's Class 6 TFT |

Every one of them is still "serial" in the sense that started this doc: information moving one
bit at a time, in order, over a small fixed number of wires — just tuned differently for how
many devices need to share the bus and how fast the data needs to move.



[01]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/tree/main/explainers/raspberry-pi-pico-2w-pinout.md
[02]:https://pico2w.pinout.xyz/#i=siuph
[03]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/tree/main/explainers/types-of-pins-on-raspberry-pi-pico-2w.md
[04]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/tree/main/explainers/glossary-of-terms-for-microcontrollers.md
[05]:https://www.adafruit.com/product/4634
[06]:https://learn.adafruit.com/introducing-adafruit-stemma-qt
[07]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/tree/main/lesson_plans/class-04-lesson-plan.md
[08]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/tree/main/lesson_plans/class-06-lesson-plan.md
