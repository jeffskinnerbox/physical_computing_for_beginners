# What Are Breadboards and Dupont Wires?

Every single class in this course, starting with Class 1's pushbutton and rotary encoder, you've
pushed component legs into a perforated white board and connected them with short colored wires.
This doc explains what that board actually is (and why it's called something you'd expect to
find in a kitchen), and what those wires are (and why they're named after a chemical company).
Neither name makes sense until you know the history, so this doc covers both.

## Part 1: Breadboards

### Where the name comes from

Before there was a purpose-built prototyping board, there was, literally, a breadboard — the
wooden board people used at home to cut bread. In the early-to-mid 1900s, hobbyist electronics
tinkerers didn't have anything better on hand, so they nailed or screwed their component leads
directly onto an actual wooden bread-cutting board to hold a circuit together while they built
and tested it. It worked — wood doesn't conduct electricity, so it was safe to build on — but it
meant every new circuit needed new holes drilled or new nails driven, and once you were done, the
board was full of hardware and hard to reuse.

By the 1970s, the electronics industry had built a purpose-made, reusable version of the same
idea: a plastic board full of spring-loaded holes you could push component legs into and pull
back out, no drilling, no soldering. The name never changed even though the wood did — this
course's boards are solid plastic, but they're still called breadboards, a piece of vocabulary
fossilized from a tool nobody actually cuts bread on anymore.

### What a breadboard is

[Wikipedia's article on the breadboard][01] describes it as a construction base for prototyping
electronics — a way to build and test a circuit without any permanent connection like solder. In
plain terms: it's a reusable board of holes, and pushing a component's leg or a wire's tip into a
hole makes an electrical connection, the same way a wire wrapped around a screw terminal would,
except you can pull it back out and try again in seconds.

### Why they're used

The whole appeal is **speed and reversibility**. Soldering a circuit together is permanent —
undoing a mistake means desoldering, which risks damaging the component or the board. A
breadboard makes every connection removable: got the wiring wrong? Pull the wire, move it, done.
That's exactly why this course leans on breadboards for every class — you're not building one
final circuit, you're building, testing, and rebuilding a new circuit each week on top of what
came before, and a breadboard lets you experiment without any of it being permanent. It's the
electronics equivalent of a whiteboard versus a printed page: fast to change, meant to be reused,
not meant to be the final product.

### Sizes

Breadboards come in a range of sizes, but two show up constantly and are worth knowing by name:

* **Full-size** — roughly 6.5 inches long, with about 830 total tie-points (holes). This is the
  "6 inch" board you'll hear people refer to, and it's large enough to hold several components
  and their wiring side by side.
* **Half-size** — roughly 3.25 inches long, with about 400 tie-points. This is the "3 inch"
  board — literally about half a full-size board, both in length and hole count.

You'll also see smaller "mini" breadboards (170 tie-points or fewer) for very simple circuits
where a half-size board would be overkill. The size you need depends entirely on how many
components and wires the circuit has to hold at once — this course's later classes (Class 4
onward, stacking a motor driver, an IMU, and a servo on top of everything from earlier classes)
lean toward the larger end for exactly that reason.

### The channel down the middle

Every standard breadboard has a gap running down its center, splitting it into a left half and a
right half. That gap exists for one specific, deliberate reason: it's sized to fit a **DIP chip**
(Dual In-line Package) — the classic black rectangular chip package with two rows of pins running
down its long sides. Straddle a DIP chip across the center channel, and each of its pins lands in
a *separate* row on either side, since (as the next section explains) rows on opposite sides of
the channel are never electrically connected to each other. Without that gap, a chip's two rows
of pins would short together the moment you plugged it in. Even in a project that never uses a
DIP chip, the channel keeps that separation available and is also just a handy visual and
physical divider for organizing a circuit's layout.

### The power rails along the top and bottom

Running along the top and bottom edges of most breadboards are two pairs of long rows, usually
marked with a red `+` line and a blue or black `−` line. These are the **power rails**, and
unlike the interior rows (below), a single rail runs the *entire length* of the board as one
electrically connected line. The idea is to give every part of your circuit easy access to power
and ground without running a separate wire all the way back to the microcontroller for every
single component — connect the Pico's `3V3 OUT` and `GND` to the rails once, and then any
component anywhere on the board can tap into power or ground with a short wire to the nearest
rail. Every lesson script's wiring table in this course leans on exactly this pattern: one wire
from the Pico to each rail, then every sensor and LED borrows power and ground locally from
whichever rail is closest. (For what `3V3 OUT` and `GND` actually are on the Pico 2 W, see
[Types of Pins on the Pico 2 W][04].)

### How the holes are actually connected

This is the part that trips people up the first time, because it isn't visually obvious from
looking at the board: **the interior holes are connected in short rows, not columns.**
Specifically, on each side of the center channel, every group of 5 holes running *across* the
board (perpendicular to the channel) is one single electrical node — push two wires into any two
holes in that same row of 5, and they're connected to each other exactly as if you'd twisted
their bare ends together. But a hole is *not* connected to the hole directly above or below it in
the same column — each row of 5 is its own island, electrically isolated from every other row.

The power rails work the opposite way: they run the *long* way, the full length of the board, as
one continuous line — the reverse of the short interior rows. That's the one exception worth
memorizing: interior rows are short and run sideways; power rails are long and run lengthwise.
Getting this backwards is the single most common breadboard wiring mistake — plugging two
unrelated components into the same row expecting them to be separate, or plugging one into a row
by itself expecting it to reach across the board on its own.

### When not to use a breadboard

A breadboard is fantastic for exactly what this course uses it for — building and rewiring a
circuit repeatedly while you're still learning and testing. It's the wrong tool once a project
moves past that stage, for a few concrete reasons:

* **High-frequency signals.** The spring contacts inside a breadboard, and the way wires sit
  loosely next to each other, add small amounts of unwanted capacitance and inductance to a
  circuit. At low speeds — everything this course does — that's invisible. At high frequencies
  (fast digital clocks, RF/radio circuits), that parasitic effect can actually distort the
  signal.
* **High current.** The thin internal spring contacts aren't rated for much current, and can
  overheat or arc under real power-electronics loads. This course's motors (Class 3's DRV8833
  driver) stay well within safe breadboard current, but a project pushing serious amperage
  through motors or high-power LEDs needs a more robust connection method.
* **Anything permanent or subject to vibration.** A breadboard's push-fit connections aren't
  fully secure — bump the board, or run something that vibrates (like a moving robot), and a
  loosely seated wire can work its way out. A final, permanent build — the kind you'd actually
  want to trust running unattended — belongs on a soldered perfboard or a custom PCB, not a
  breadboard.

## Part 2: Dupont Wires (a.k.a. Jumper Wires)

### Where the name comes from

"Dupont wire" is one of those names that sticks around long after most people have forgotten why.
It comes from **DuPont**, the American chemical and materials company, which decades ago
developed a small pin-and-socket connector system for reliably connecting wires to circuit
boards. That connector design became extremely popular and widely copied across the electronics
industry, to the point that the *generic* name for that style of small, snap-together connector —
regardless of who actually manufactures it today — became "Dupont connector," and a short length
of wire terminated with one is a "Dupont wire." You'll also hear the exact same wires called
**jumper wires** or **jump wires** — those names describe the *function* (a short wire that
"jumps" a connection from one point to another) rather than the connector brand, and in everyday
use, all three names refer to the same thing.

### What they are

[Wikipedia's article on jump wires][02] describes a jumper (or jump wire) as an electrical wire,
or group of them, with a connector at each end used to interconnect components on a breadboard or
other prototyping device without soldering. In plain terms: it's the short cable that carries a
signal, power, or ground from one hole on your breadboard (or one pin on your Pico) to another,
and its end connector is exactly what makes push-fit, solderless wiring possible in the first
place.

### What they're used for

Every wire in every wiring table in this course's lesson scripts — from the Class 1 pushbutton's
connection to `GP2`, to the Class 4 LSM9DS1's I2C connection over `SCL`/`SDA` — is a Dupont/jumper
wire. Anywhere you need to connect a breadboard hole to a Pico GPIO pin, or one breadboard hole to
another, a jumper wire is the tool. It's the physical link that turns a wiring table's rows into
an actual working circuit.

### Lengths

Jumper wires are sold pre-cut to a handful of standard lengths, most commonly **10 cm**,
**15 cm**, and **20 cm**, though shorter and longer lengths exist too. You pick the length based
on how far apart the two points you're connecting are — a short 10 cm wire for a component
sitting right next to the Pico on the same breadboard, a longer 20 cm wire for something mounted
farther away. There's no electrical difference between lengths at the voltages and speeds this
course works with; it's purely about physically reaching where you need to go without excess
slack getting in the way.

### Terminal types

The connector on each end of a jumper wire is either a solid pin (**male**) or a socket that a
pin plugs into (**female**), and wires come in every combination of the two:

* **Male-to-male** — a pin on both ends. This is the type you use to connect two holes on the
  same breadboard, or a breadboard hole to a Pico GPIO pin, since both a breadboard hole and a
  Pico pin expect to receive a pin. This is the most common type in this course's wiring.
* **Male-to-female** — a pin on one end, a socket on the other. Useful for connecting a
  breadboard (male end) directly to a component that already has its own protruding pins, like
  many sensor breakout boards (female end) — no breadboard hole involved on that side at all.
* **Female-to-female** — a socket on both ends. Used to connect two things that both already have
  protruding pins — for example, linking two breakout boards' pin headers together directly
  without a breadboard in between.

### Colors

Jumper wires are sold in assorted colors — red, black, yellow, green, blue, and more — purely for
your own organization. The color of a wire has **no electrical meaning**; a red wire doesn't
carry more current or voltage than a black one. That said, a common convention worth adopting
(and one you'll see followed in this course's own wiring diagrams) is using red for power, black
for ground, and any other color for signal wires — not because the wire itself cares, but because
color-coding makes a finished circuit far easier to read back later and catch mistakes in.

### Making your own

If a standard pre-made length doesn't fit your project, you're not stuck buying a new pack — a
Dupont wire is just a length of stranded wire with a small crimped-on pin or socket terminal at
each end, and both the terminals and the crimping tool to attach them are sold separately. Cut a
length of wire to whatever size you need, strip a few millimeters of insulation off the end, crimp
on a Dupont terminal, and slide it into a plastic connector housing — you've made a custom-length
jumper wire identical to a store-bought one. It's a more advanced skill this course doesn't
require, but it's good to know the pre-made wires aren't some sealed mystery part — they're a
simple, repeatable assembly you can build yourself.

### Going without: plain 22 AWG solid wire

You don't strictly need Dupont-terminated wire for breadboard work at all. Plain **solid-core 22
AWG hookup wire** — bare, stiff, uninsulated-except-for-a-jacket wire with no connector on either
end — pushes into a breadboard hole just as well as a jumper wire's male pin does, because a
breadboard's spring contacts just need something rigid and the right diameter to grip. The
trade-off runs both directions: solid wire has to be cut and stripped to an exact custom length
for every connection, which is more work than grabbing a pre-made jumper — but because it's
stiff, it holds a bent shape and sits flat and tidy on the board in a way a limp stranded jumper
wire sometimes doesn't, which some people find makes for a cleaner-looking, easier-to-trace
circuit. Either works fine for this course; it's a matter of convenience versus tidiness, not
correctness.

### When not to use Dupont wires

The same cautions that apply to breadboards mostly carry straight over to the jumper wires that
plug into them, plus one Dupont-specific weak point:

* **High current or permanent builds.** Like the breadboard itself, a jumper wire's thin
  push-fit pin isn't meant for heavy current or a connection that has to survive years of use —
  for that, solder the wire directly or use a proper screw terminal.
* **Female-to-female (and any loose push-fit) connections are the least secure.** A socket
  gripping a bare pin — whether that's a female jumper wire on a component's header, or a jumper
  plugged into a breadboard hole — relies purely on spring tension to stay seated, with nothing
  physically locking it in place. That's fine sitting still on a desk, but it's exactly the
  connection most likely to work loose on anything that gets bumped, carried around, or actually
  moves — which matters directly for this course's own Class 5/6 Random Rover, where the
  breadboard itself is riding on a moving chassis. Double-check jumper connections on a moving
  build before every test run, and consider it a candidate for a more permanent connection method
  once a circuit graduates past the prototyping stage.

For what those wires are actually plugging into on the Pico 2 W side, see [What Is a
Pinout?][03] and [Types of Pins on the Pico 2 W][04]; for the vocabulary around GPIO pins and
pull-up resistors that show up constantly in this course's own breadboard wiring, see the
[Glossary of Terms for Microcontrollers][05].

[01]:https://en.wikipedia.org/wiki/Breadboard
[02]:https://en.wikipedia.org/wiki/Jump_wire
[03]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/tree/main/explainers/raspberry-pi-pico-2w-pinout.md
[04]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/tree/main/explainers/types-of-pins-on-raspberry-pi-pico-2w.md
[05]:https://github.com/jeffskinnerbox/physical_computing_for_beginners/tree/main/explainers/glossary-of-terms-for-microcontrollers.md
