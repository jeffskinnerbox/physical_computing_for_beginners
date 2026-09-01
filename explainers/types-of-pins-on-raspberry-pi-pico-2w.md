# Types of Pins on the Raspberry Pi Pico 2 W

The [Pico 2 W pinout site][03] lists a lot of pin labels that aren't `GPnn` at all — `VBUS`,
`3V3 EN`, `ADC VREF`, `RUN`, and more. This doc walks through every one of those non-obvious pin
types: what the abbreviation means, what the pin is for, how it behaves electrically, and — for
the ones you can actually use from code — how to reach it in CircuitPython. For what a pinout is
in general and where to find the Pico 2 W's, see the companion doc,
[What Is a Pinout?][01]. For the communication-protocol pins (`SPI`, `I2C`, `UART`), see the
other companion doc, [Serial Communication: SPI, I2C, and UART][02] — this doc only summarizes
those three before pointing you there. And if you just need a quick one-paragraph reminder of
what an abbreviation like `ADC` or `GPIO` stands for, see the [Glossary of Terms for
Microcontrollers][04]. This doc covers the pins themselves; for what you actually plug *into*
them — the breadboard and the jumper wires every lesson script's wiring table depends on — see
[What Are Breadboards and Dupont Wires?][05].

## Two kinds of pins: power and signal

Every pin on the Pico 2 W falls into one of two broad jobs. **Power pins** move electricity in
or out of the board — they don't carry information, just voltage and current, the same way the
prongs on a wall plug don't "say" anything, they just deliver power. **Signal pins** carry
information — a digital `1` or `0`, an analog voltage that varies smoothly, or a stream of bits
following one of the serial protocols. Mixing the two up — for example, wiring a sensor's data
line to a power pin — is exactly the mistake a pinout exists to prevent (see [What Is a
Pinout?][01] for why that matters). Keep that split in mind as you go through the pins below;
each one is labeled as Power or Signal.

## SPI, I2C, UART (Signal — communication protocols)

These three labels show up scattered across several `GPnn` pins on the pinout diagram, marking
which pins are wired internally to the chip's dedicated communication hardware. **SPI** (Serial
Peripheral Interface), **I2C** (Inter-Integrated Circuit), and **UART** (Universal Asynchronous
Receiver/Transmitter) are protocols — agreed-upon rules two chips follow so they can exchange
data over just a few wires instead of one wire per piece of information. This course uses I2C to
read the Class 4 LSM9DS1 motion sensor and SPI to drive the Class 6 TFT status screen; UART is
what carries `print()` output from the Pico to your laptop's Serial console every class. The full
breakdown — what each abbreviation stands for, how each protocol moves bits down the wire, and
the exact CircuitPython code to talk over each one — lives in [Serial Communication: SPI, I2C,
and UART][02].

## Ground (Power)

**What it's for:** `GND` (Ground) pins are the return path for electric current. Power doesn't
do anything useful just by arriving somewhere — it has to flow in a complete loop, out of a
source, through a component, and back again. `GND` is that "back again" — every circuit you wire
in this class needs at least one connection back to a `GND` pin, or current has nowhere to
return to and nothing will work. The Pico 2 W has several `GND` pins spread around the board
specifically so you don't have to run a long wire back to a single spot every time.

**How it operates:** Electrically, `GND` is defined as 0 volts — the reference point every other
voltage on the board is measured against. All the `GND` pins on the Pico 2 W are connected
together internally, so it doesn't matter which one you use; they're electrically identical.

**Accessing it:** There's no CircuitPython code for `GND` — it's a wiring-only pin. Every
breadboard circuit in this course's lesson scripts includes a `GND` connection in its wiring
table for exactly this reason.

## VBUS 5V (Power)

**What it's for:** `VBUS` carries the raw 5-volt power coming in from whatever is plugged into
the Pico's USB-C port — your laptop, or a USB power bank/wall adapter. It's the Pico's main power
*input* when running over USB, which is how this class has powered every board so far.

**How it operates:** `VBUS` is only "live" when a USB cable is actually connected and supplying
power. It's not regulated down to a lower voltage — it passes the USB port's 5V through more or
less directly, which is why some power-hungry accessories (like a strip of several servo motors)
are better fed from `VBUS` than from the board's other power pins.

**Accessing it:** No CircuitPython code — `VBUS` is a wiring pin, useful when a breadboard
component needs 5V instead of the 3.3V most sensors in this course run on.

## VSYS 5V (Power)

**What it's for:** `VSYS` (System Voltage) is the Pico's single unified power *input* pin —
where the board actually expects to receive power from, whether that power originates from
`VBUS` (USB) or from an external battery or power supply wired directly to `VSYS`. Internally,
`VBUS` is one of a few sources that feeds into `VSYS`, and `VSYS` feeds the board's onboard
voltage regulator (see 3V3 Out, below).

**How it operates:** `VSYS` accepts a range of input voltages (roughly 1.8V–5.5V), which is what
makes it the pin to use for battery power instead of `VBUS` — a battery pack won't always supply
a clean 5V the way USB does, and `VSYS` is designed to tolerate that. This course powers every
board over USB, so `VSYS` doesn't come up in a lesson script's wiring table, but it's the pin
you'd reach for the day you want to build a Random Rover that isn't tethered to a laptop.

**Accessing it:** No CircuitPython code — `VSYS` is a wiring pin.

## 3V3 En (Power)

**What it's for:** `3V3 EN` (3.3V Enable) is a control pin, not a power-delivery pin — it's a
switch that turns the entire board on or off. Pulling this pin low (connecting it to `GND`)
shuts down the Pico's onboard voltage regulator, which cuts power to everything else on the
board, `GPnn` pins included.

**How it operates:** By default, `3V3 EN` is pulled high internally, meaning the board runs
normally — you'd have to deliberately wire something to pull it low to shut the board down.
It's mostly there for advanced, battery-powered projects that need a hardware power switch
(flip one switch, kill the whole board) rather than software-controlled shutdown.

**Accessing it:** No CircuitPython code — this is a hardware-only control pin. This course
doesn't use it; every project stays powered on for the whole class.

## 3V3 Out (Power)

**What it's for:** `3V3 OUT` is the Pico's regulated 3.3-volt power *output* — the pin nearly
every sensor in this course actually draws its power from. Most breakout boards (the pushbutton
pull-ups, the HC-SR04, the LSM9DS1) are designed to run on 3.3V, not the raw 5V from `VBUS`, so
`3V3 OUT` is the "house power outlet" your breadboard plugs into for most of this class's
circuits.

**How it operates:** Internally, the Pico's voltage regulator takes whatever comes in on `VSYS`
(which could be anywhere from 1.8V to 5.5V) and steps it down to a clean, steady 3.3V on `3V3
OUT` — that regulation is exactly why sensors prefer it over `VBUS`: `VBUS` can vary depending on
what's supplying USB power, but `3V3 OUT` is always 3.3V regardless.

**Accessing it:** No CircuitPython code — `3V3 OUT` is a wiring pin. Check any lesson script's
wiring table in this course and you'll almost always see a sensor's power lead going to `3V3
OUT`, or sometimes labeled simply `3V3` on the silkscreen. In practice that one wire usually goes
straight to your breadboard's `+` power rail, so every other component on the board can tap into
3.3V nearby instead of running its own wire all the way back to this pin — see [What Are
Breadboards and Dupont Wires?][05] for how those rails work.

## ADC VRef (Signal, but power-adjacent)

**What it's for:** `ADC VREF` (Analog-to-Digital Converter Voltage Reference) sets the upper
bound the chip's analog-to-digital converter measures against. An ADC (see the `A0`/`A1`/`A2`
pins below) doesn't just report "how many volts" — internally it reports "what fraction of the
reference voltage," so `ADC VREF` is what calibrates that fraction back into a real voltage
reading.

**How it operates:** By default, `ADC VREF` is tied to the same 3.3V as `3V3 OUT`, which is why
most projects never touch it directly — the Pico ships already configured to measure analog
pins against 3.3V. It only becomes relevant if you need a more precise or different reference
voltage than 3.3V for a specific analog sensor, which is beyond what this course's projects
require.

**Accessing it:** No CircuitPython code needed for typical use — CircuitPython's `analogio`
module already assumes the default 3.3V reference when you read an analog pin.

## ADC Gnd (Power)

**What it's for:** `ADC GND` is a dedicated ground pin specifically for analog readings, kept
electrically separate on the board's layout from the general-purpose `GND` pins. Precise analog
measurements are sensitive to electrical noise, and digital signals switching rapidly elsewhere
on the board can introduce exactly that noise if the analog and digital grounds share the same
noisy path.

**How it operates:** Electrically it's still 0V, same as any other `GND` — the separation is
about physical layout and noise isolation on the circuit board, not a different voltage.

**Accessing it:** No CircuitPython code — `ADC GND` is a wiring pin. Use it (instead of a
general `GND` pin) when wiring an analog sensor that needs a clean reading.

## GP26 A0, GP27 A1, GP28 A2 (Signal — analog input)

**What they're for:** These three pins are dual-purpose: each is a normal digital `GPnn` pin
(`GP26`, `GP27`, `GP28`) that *also* connects to one of the Pico 2 W's analog-to-digital
converters, labeled `A0`, `A1`, and `A2`. An ADC is what lets the Pico read a *continuously
varying* voltage — like the wiper on a potentiometer, or the output of an analog light sensor —
instead of just a plain on/off digital signal. Most `GPnn` pins on the Pico 2 W can only tell you
"high" or "low"; these three are the ones that can also tell you "exactly how high, on a scale."

**How it operates:** The RP2350's ADC measures the voltage on the pin and reports it as a number
between 0 and 65535 in CircuitPython (a 16-bit range), where 0 means 0V and 65535 means the
reference voltage (3.3V by default — see `ADC VREF` above). A value in between, say 32768, means
roughly half the reference voltage, about 1.65V. This course's own sensors don't need this — the
HC-SR04 reports distance digitally via timing, not a varying voltage, and the LSM9DS1 reports its
readings over I2C — so none of this course's lesson scripts wire anything to `A0`/`A1`/`A2`. Any
future analog sensor (a photo resistor, a soft potentiometer, an analog joystick) would land on
one of these three pins.

**Accessing it in CircuitPython:**

```python
import board
import analogio

pot = analogio.AnalogIn(board.A0)  # same as board.GP26
voltage = pot.value / 65535 * 3.3
```

Note that CircuitPython lets you refer to the pin as either `board.A0` or `board.GP26` — both
names point at the same physical pin, since it's genuinely both at once.

## RUN (Signal — hardware reset)

**What it's for:** `RUN` is the Pico 2 W's hardware reset pin. Momentarily connecting `RUN` to
`GND` restarts the chip, the same effect as pressing a reset button — whatever code was running
stops, and the board boots back up from the beginning, exactly like unplugging and replugging
the USB cable, but without the power cycle.

**How it operates:** `RUN` is pulled high internally by default (meaning the board runs
normally). Briefly grounding it triggers the reset; releasing it lets the board boot normally
again. Some boards built around the RP2040/RP2350 chip wire a physical reset button directly to
`RUN` for exactly this purpose — the Pico 2 W itself doesn't have an onboard reset button, so
`RUN` is exposed as a pin specifically so you can wire your own if a project needs one.

**Accessing it:** No CircuitPython code — this is a hardware-only control pin, and this course's
projects don't wire anything to it. You've already been triggering the equivalent of a `RUN`
reset all class by clicking the reset/restart control in Mu or pressing `Ctrl+D` in the serial
console, both of which restart the running program in software rather than the hardware `RUN`
pin.

## Quick reference

| Pin label | Kind | One-line job |
| :--- | :--- | :--- |
| SPI / I2C / UART | Signal | Serial communication protocols — see [Serial Communication: SPI, I2C, and UART][02] |
| GND | Power | Return path for current (0V reference) |
| VBUS 5V | Power | Raw 5V input from USB |
| VSYS 5V | Power | Unified power input feeding the board's regulator |
| 3V3 EN | Power | Hardware on/off switch for the whole board |
| 3V3 OUT | Power | Regulated 3.3V output most sensors draw power from |
| ADC VREF | Signal | Reference voltage analog readings are measured against |
| ADC GND | Power | Noise-isolated ground for analog readings |
| GP26 A0 / GP27 A1 / GP28 A2 | Signal | Analog-input-capable GPIO pins |
| RUN | Signal | Hardware reset — grounding it restarts the chip |

For the full pin-by-pin map (which physical leg is which of the above), see [pinout.xyz's Pico 2
W page][03], and for what a pinout is and how to read one in general, see [What Is a Pinout?][01].
For definitions of the underlying concepts these pins connect to — ADC, GPIO, NVM, and the rest —
see the [Glossary of Terms for Microcontrollers][04].



[01]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/tree/main/explainers/raspberry-pi-pico-2w-pinout.md
[02]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/tree/main/explainers/spi-i2c-uart-serial-communications.md
[03]:https://pico2w.pinout.xyz/#i=ph
[04]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/tree/main/explainers/glossary-of-terms-for-microcontrollers.md
[05]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/tree/main/explainers/what-are-breadboards-and-dupont-wires.md
