# Glossary of Terms for Microcontrollers

This class throws around a lot of three- and four-letter abbreviations — MCU, ADC, GPIO, RTOS —
often in the same breath as the parts you're actually wiring. Most of the other docs in
`explainers/` teach one concept at a time through a story; this one is different on purpose. It's
a quick-lookup reference: short, plain-English definitions for every term you're likely to hit in
this course's lesson scripts, datasheets, or CircuitPython library docs, grouped by topic so
related terms sit next to each other instead of in alphabetical order. If a term gets a fuller
treatment elsewhere in this folder — the way [SPI, I2C, and UART][01] each get a whole doc of
their own — this glossary gives the short version and links out to the long one.

## The chip itself

Every board in this course is built around one chip that does the actual thinking — the Pico 2
W's chip is an RP2350. This section covers the words for that chip and what's inside it.

**Microcontroller (MCU).** A single chip that packs a processor, memory, and input/output pins
all onto one piece of silicon — a complete tiny computer, sized and priced to be built directly
into a single-purpose device rather than run a general operating system. The Pico 2 W's RP2350 is
the MCU this whole course is built around. Because everything it needs is already on the chip,
its firmware (below) runs directly on the bare-metal hardware — no operating system sits between
your `code.py` and the silicon. See [Microprocessors vs.
microcontrollers][03] for the fuller history of why MCUs exist as a separate category from
desktop-computer CPUs.

**Microprocessor.** Just the CPU core on its own chip, with no memory or input/output built in —
the kind of chip inside a laptop or a Raspberry Pi 4/5. Unusable by itself, a microprocessor has
to be wired up to separate RAM chips, separate flash or hard-drive storage, and separate I/O
chips to do anything, and it's normally paired with a full operating system that juggles many
programs at once. See [Microprocessors vs. microcontrollers][03] for the full history.

**Microcontroller vs. Microprocessor.** The short version: a microcontroller is self-contained
(CPU, memory, and I/O on one chip, running one program forever) while a microprocessor is just
the CPU, needing a whole board of supporting chips and a full operating system around it. That's
why the Pico 2 W's RP2350 — cheap, low-power, and running your `code.py` the instant it's
plugged in — is a microcontroller, while the chip in your laptop is a microprocessor. See
[Microprocessors vs. microcontrollers][03] for the complete comparison, including cost, power,
and real-time response tradeoffs.

**Operating System (OS).** The background software on a general-purpose computer — Windows,
macOS, Linux — that manages hardware and juggles multiple programs running at once, deciding
which one gets the CPU's attention at any instant. The Pico 2 W has no operating system:
CircuitPython *is* essentially the whole environment, and there's exactly one program (your
`code.py`) running in an endless loop, so there's nothing to schedule or switch between.

**CPU (Central Processing Unit).** The part of the MCU that actually executes your code — it
reads each instruction in your CircuitPython program (translated down to machine instructions),
does the math or logic it asks for, and moves on to the next one, over and over, extremely fast.
Everything else on the chip — memory, GPIO pins, the ADC — exists to feed the CPU data or carry
out what the CPU decides.

**Register.** A tiny, extremely fast storage slot built directly into the chip's hardware — not
regular memory, but a handful of bytes the CPU and its peripherals (like the GPIO controller or
the ADC) read and write directly to configure themselves or report status. When CircuitPython
runs a line like `led.value = True`, somewhere underneath that friendly Python call, a specific
bit in a specific hardware register just got flipped. You'll never touch a register directly in
this course — the whole point of a CircuitPython library like `digitalio` is to hide that
low-level detail behind a readable name — but it's worth knowing the friendly Python call is a
thin wrapper over exactly this.

## Memory

A microcontroller needs somewhere to hold two very different things: the program itself, and the
data that program is working with while it runs. Those two jobs use different kinds of memory
with very different trade-offs, mainly around one question — does the data survive when the power
goes off?

**RAM (Random Access Memory).** The chip's working scratchpad — fast, but it forgets everything
the instant power is lost. Every variable your CircuitPython code creates while running (a sensor
reading, a loop counter, a rolling average) lives in RAM. "Random access" just means the chip can
jump straight to any address instantly, rather than reading through memory in order.

**SRAM (Static Random Access Memory).** The specific *type* of RAM microcontrollers like the
RP2350 use — fast and simple, but it takes more physical space per bit than the RAM in a laptop,
which is why an MCU has kilobytes of RAM rather than the gigabytes a laptop has. For this
course's purposes, "RAM" and "SRAM" mean the same thing; you'll see "SRAM" specifically in
datasheets and chip specs.

**Flash Memory.** Where your actual `code.py` file lives, along with CircuitPython itself and any
libraries you copied onto the board. Unlike RAM, flash memory *keeps* its contents with the power
off — that's exactly why it's the right place for a program: you want your code still there the
next time you plug the board in, not erased. Saving a file to your `CIRCUITPY` drive is writing
to flash.

**Mask ROM / OTP ROM.** Two even more permanent forms of program memory than flash. **Mask ROM**
has its contents baked into the silicon at the factory — it can never be changed afterward, which
only makes economic sense for chips made by the millions running code that will never update.
**OTP (One-Time Programmable) ROM** is blank until it leaves the factory, but can be written to
exactly once by the manufacturer or an early boot step, after which it's permanently locked. The
RP2350 uses a small amount of OTP ROM to hold its boot-time security and configuration settings,
but everything you interact with in this course — CircuitPython and your `code.py` — lives in the
rewritable flash memory above, not mask or OTP ROM.

**EEPROM (Electrically Erasable Programmable Read-Only Memory).** An older, smaller, and slower
non-volatile memory technology than flash, historically used for small amounts of settings or
configuration data that a program needs to remember between power cycles — a saved calibration
value, for instance. Flash memory has mostly replaced EEPROM in modern chips like the RP2350
because it can be erased and rewritten faster and in larger chunks, but you'll still see "EEPROM"
in older datasheets and tutorials as the generic term for "a small non-volatile settings store."

**FRAM (Ferroelectric RAM).** A less common memory technology that behaves like non-volatile
EEPROM/flash — it keeps its contents with the power off — but reads and writes at speeds close to
regular RAM, with none of flash's "erase before rewrite" delay. It shows up in a handful of
specialty microcontrollers and add-on boards where a program needs to save data constantly
without wearing out flash (which only tolerates a limited number of rewrites). The RP2350 doesn't
use FRAM — worth knowing the name exists mainly so it doesn't look like a typo for "RAM" or
"EEPROM" when you spot it in a datasheet.

> [!WARNING]
> It's easy to assume "memory" always means the same thing, but a microcontroller's memory is
> split by one hard question — does it survive when the power goes off? Volatile memory (RAM/
> SRAM) doesn't; non-volatile memory (flash, EEPROM, mask/OTP ROM, FRAM) does. Writing to the
> wrong one for the job is a real bug: store a sensor calibration value in RAM instead of flash,
> and it's gone the moment the board loses power.

**NVM (Non-Volatile Memory).** The umbrella term covering any memory that keeps its contents with
the power off — flash and EEPROM are both *kinds* of NVM. When a datasheet says "NVM," it's
speaking generally about the erase-power-and-it-survives category rather than naming one specific
technology. The opposite of NVM is *volatile* memory — RAM — which is why the code/data split on
a microcontroller is really a volatile/non-volatile split: NVM for what has to survive a reboot,
RAM for what doesn't need to.

## Talking to the outside world

An MCU is useless in isolation — the entire point of this course is wiring sensors, motors, and
displays to one, so it needs standardized ways to send and receive both digital (on/off) and
analog (continuously varying) signals through its physical pins.

**Peripherals.** The umbrella term for all the built-in hardware on an MCU that isn't the CPU
itself — GPIO pins, the ADC, timers, interrupt controllers, and the UART/I2C/SPI serial
interfaces below are all peripherals. The CPU runs your code; peripherals are what let that code
actually talk to the outside world (or measure it, or keep time) without the CPU having to
bit-bang every signal by hand.

**GPIO (General Purpose Input/Output).** Any pin on the board that your code can configure to
either read a signal (input) or send one (output), for general use rather than one fixed job.
Every `GPnn` pin on the Pico 2 W's silkscreen — `GP2` for the Class 1 pushbutton, `GP15` for an
LED — is a GPIO pin. "General purpose" is the key phrase: the same physical pin can be a digital
input one moment and a digital output the next, entirely depending on how your code configures
it. See [Types of Pins on the Pico 2 W][02] for the pins on the Pico 2 W that *aren't*
general-purpose — the power, ground, and reset pins with one fixed job. For the breadboard and
jumper wires that actually carry a GPIO signal from the pin to a component, see [What Are
Breadboards and Dupont Wires?][04].

**Pull-Up / Pull-Down Resistor.** A resistor that gives a digital input pin a known, default
state so it never "floats" — without one, a GPIO pin configured as an input with nothing driving
it picks up stray electrical noise and can read randomly as high or low even when nothing is
happening. A **pull-up** resistor ties the pin to power by default (reading high/`True`) until
something pulls it to `GND` (reading low/`False`); a **pull-down** does the opposite, resting low
until something pulls it high. This course's Class 1 pushbutton and rotary encoder are both wired
this way — "active-low," resting `True` until pressed, at which point the pin connects to `GND`
and reads `False`. Rather than a physical resistor on the breadboard, this course uses the
RP2350's *internal* pull-up, turned on entirely in software:

```python
button.pull = digitalio.Pull.UP
```

One course-specific wrinkle worth knowing: the Pico 2 W's original RP2350 chip revision has a
known silicon bug (erratum RP2350-E9) affecting internal pull-*downs* specifically — a pin
configured with an internal pull-down can sometimes falsely read high. This course sidesteps the
bug entirely by wiring everything active-low with pull-*ups* instead. See the Class 1 lesson
script's "Understanding Pull-Up & Pull-Down Resistors" section for the full wiring rationale.

**ADC (Analog-to-Digital Converter).** The piece of hardware that reads a continuously varying
voltage on a pin and converts it into a number your code can use. Digital logic only understands
"high" or "low," but plenty of real-world signals — a potentiometer's wiper position, a light
sensor's output — vary smoothly instead of snapping between two states, and an ADC is the bridge
between that analog world and the CPU's digital one. The Pico 2 W's `GP26 A0`, `GP27 A1`, and
`GP28 A2` pins are its ADC-capable pins; see [Types of Pins on the Pico 2 W][02] for the full
walkthrough, including the CircuitPython `analogio` code that reads one.

**DAC (Digital-to-Analog Converter).** The mirror image of an ADC — hardware that takes a number
from your code and turns it into an actual analog voltage on a pin, instead of just "high" or
"low." A DAC is what you'd reach for to generate a smoothly varying signal, like an audio
waveform. This course doesn't use the Pico 2 W's DAC for anything — every analog-feeling output
in this class (the SG90 servo, the DRV8833-driven motors) is actually controlled with PWM
(below), not a true DAC — but it's worth knowing the two are different tools: PWM *simulates* an
analog effect by rapidly switching a digital pin, while a DAC produces a genuinely analog voltage.

**PWM (Pulse Width Modulation).** A trick for getting analog-feeling behavior out of a pin that
can only truly be "on" or "off": switch the pin on and off very rapidly, and vary the *fraction of
time* it spends on (called the duty cycle) instead of varying the voltage itself. A motor or LED
responds to that rapid switching as if it were receiving a steady in-between voltage, because the
switching happens faster than the motor or LED can react. This course uses PWM constantly — it's
how the Class 2 SG90 servo is told what angle to move to, and how the Class 3 DRV8833 driver
controls motor speed.

## Serial communication protocols

Once you're moving beyond a single wire carrying one on/off signal, you need an agreed-upon set
of rules for how two chips take turns sending bits back and forth. This course covers three such
rule sets in depth in a dedicated doc — [SPI, I2C, and UART][01] — so the entries here are
intentionally short; follow the link for the full breakdown, including wiring and CircuitPython
code for each.

**UART (Universal Asynchronous Receiver/Transmitter).** A simple, one-to-one serial link over two
wires (`TX`/`RX`), with no shared clock — each side just keeps its own timing at an agreed speed
(the baud rate). This is what carries your `print()` output to the Serial console in Mu every
class.

**I2C (Inter-Integrated Circuit).** A two-wire (`SDA`/`SCL`) serial bus that lets multiple devices
share the same pair of pins, each identified by its own address. This course uses I2C to read the
Class 4 LSM9DS1 motion sensor.

**SPI (Serial Peripheral Interface).** A faster, four-or-more-wire serial link (`SCK`, `MOSI`,
`MISO`, and a `CS` pin per device) built for moving data quickly — the go-to choice for anything
with a lot of data to move, like a display. This course uses SPI to drive the Class 6 stretch-goal
TFT screen.

## Reacting to events

**Main Loop.** The `while True:` block at the bottom of every `code.py` in this course — the code
that runs top to bottom, over and over, for as long as the board has power. Everything you've
written so far lives in the main loop: read a sensor, decide something, act, repeat. It's the
simplest possible way to structure a program, and it's why this course leans on polling (checking
a pin's state yourself, every pass through the loop) rather than interrupts for something like
the Class 1 pushbutton — one loop, checked on its own schedule, is easier to reason about than
code that can be interrupted mid-step.

So far, every piece of code you've written in this course runs top to bottom in a loop, checking
things on its own schedule. But some events — a button press, a timer running out, a sensor
finishing a reading — need the chip's attention *immediately*, not just whenever the main loop
next happens to check. This section covers the tools an MCU has for reacting to events instead of
just polling for them.

**Interrupt.** A signal that pauses whatever the CPU is currently doing so it can immediately
handle something more urgent, then resumes exactly where it left off. Think of it like your phone
buzzing mid-conversation — you don't ignore it until a natural pause; it interrupts you right
then, you handle it, and you go back to what you were doing. Hardware interrupts are how a chip
reacts instantly to something like a button press without your main loop having to constantly
check the pin's state (that constant checking is called *polling*, and it's what this course's
own `class-1-code-*.py` scripts actually do instead — polling with debouncing, not interrupts, to
keep the code simple for a first project).

**ISR (Interrupt Service Routine).** The specific block of code that runs when an interrupt fires
— the "handler" for that event. When a hardware interrupt pauses the CPU's normal flow, it's the
ISR that gets control, does whatever needs to happen right away (like recording that a button was
pressed), and then hands control back to wherever the CPU was before. ISRs are deliberately kept
short, since nothing else on the chip runs while one is executing.

**Timers/Counters.** Hardware built into the MCU that counts clock ticks (or external pulses)
independently of the CPU running your code, and can trigger an interrupt once it reaches a target
count. A timer is what makes precise, code-independent timing possible — generating a PWM signal's
rapid on/off switching, or measuring the return-echo delay the Class 2 HC-SR04 ultrasonic sensor
depends on, are both jobs handled by the chip's timer hardware rather than your Python code
manually counting.

**DMA (Direct Memory Access).** A way to move a block of data (say, from a sensor into RAM)
without the CPU babysitting every single byte of the transfer. Normally the CPU has to actively
read each piece of incoming data one at a time; DMA hardware handles a whole transfer on its own
and only interrupts the CPU once, at the end, freeing the CPU to keep running your code in the
meantime. This course's own sensor libraries don't require you to think about DMA directly — it's
a background optimization CircuitPython's underlying drivers may use — but it's a common word in
chip datasheets, so it's worth recognizing.

**RTOS (Real-Time Operating System).** A specialized operating system built for microcontrollers
that need to guarantee several tasks all get handled within strict, predictable time limits — for
example, a robot that has to service its motor control loop, its sensor readings, and its
communication link all without ever missing a firm deadline. CircuitPython itself is not an
RTOS — it runs your `code.py` as one single program in a loop, with no separate scheduled tasks —
which is exactly why this course keeps things simple with polling loops and `time.sleep()` rather
than juggling multiple real-time tasks. An RTOS is the tool you'd reach for on a more complex
project where several time-critical jobs genuinely have to run independently.

## Startup, safety, and power

The last group covers what happens at the edges of a program's life — how code gets onto the chip
in the first place, what keeps a chip from silently freezing forever, and how it saves power when
it doesn't need to be fully awake.

**Firmware / Embedded Firmware.** The software permanently loaded onto a device to make its
hardware work — on the Pico 2 W, CircuitPython itself is firmware, and it's what turns a bare
RP2350 chip into something that can run your `code.py` at all. "Embedded firmware" is the same
idea with the word that emphasizes *where* it runs: permanently built into a single-purpose
device (an "embedded system"), as opposed to an app you install and remove on a general-purpose
computer. "Flashing firmware" (a term you saw in the Pre-Class) means writing that low-level
software into the board's flash memory (above), typically by dragging a `.uf2` file onto the
board while it's in bootloader mode.

**BOOTSEL.** The physical button on the Pico 2 W that puts it into bootloader mode — hold it down
while plugging in the USB cable, and instead of running `code.py`, the board shows up on your
computer as a plain USB drive (`RPI-RP2`) ready to accept a new `.uf2` firmware file. It's the
mechanism behind "flashing firmware": BOOTSEL tells the chip "don't run your normal program yet,
just wait for me to drop a new one in."

**WDT / Watchdog Timer.** A safety timer that automatically resets the whole chip if your program
ever gets stuck — hangs, freezes, or otherwise fails to "check in" within an expected window.
Code running normally periodically resets the watchdog's countdown (informally called "petting"
or "feeding" it); if that countdown ever reaches zero because the code stopped responding, the
watchdog forces a hardware reset (the same effect as the `RUN` pin — see [Types of Pins on the
Pico 2 W][02]) rather than leaving the device frozen and unresponsive forever. This matters most
for unattended devices — imagine the Random Rover locking up mid-run with no one there to unplug
and replug it.

**Brown-out Reset.** A safety reset that triggers automatically if the chip's supply voltage dips
too low to guarantee reliable operation — "brown-out" describes power sagging rather than cutting
out completely (a full loss of power would be a "blackout" by comparison). Running low-quality
USB cables or drawing too much current at once (several servos moving simultaneously, say) can
sag the voltage enough to trigger one. Rather than let the chip behave unpredictably on
insufficient power, a brown-out reset forces a clean restart once voltage returns to a safe level.

**Sleep / Deep Sleep.** Low-power modes that shut down parts of the chip that aren't needed at the
moment, to save battery. In a light **sleep**, the CPU pauses but most of the chip's memory and
peripherals stay powered, so it wakes up quickly and picks up close to where it left off. In
**deep sleep**, far more of the chip is powered down — sometimes even most of RAM — trading a much
lower power draw for a slower, more limited wake-up (often closer to a fresh restart than a
resume). This course runs every board plugged into USB power, so battery-saving sleep modes never
come up in a lesson script, but they're the reason a battery-powered project (like an
untethered Random Rover) can run for hours or days instead of minutes: the chip spends most of its
time asleep, waking only briefly to check a sensor or run one control loop.

[01]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/tree/main/explainers/spi-i2c-uart-serial-communications.md
[02]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/tree/main/explainers/types-of-pins-on-raspberry-pi-pico-2w.md
[03]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/tree/main/explainers/microprocessor-vs-microcontroller.md
[04]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/tree/main/explainers/what-are-breadboards-and-dupont-wires.md
