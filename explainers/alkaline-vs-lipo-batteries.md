# Alkaline vs. LiPo Batteries

The Random Rover runs from one 9V alkaline battery. On some rovers that works. On others the Pico
reboots again and again, the wheels stall, and the screen comes on and goes dark in a loop. Swap in
a LiPo battery and every one of those problems disappears. Nothing in the code changed, so what
did?

The short answer: the two batteries can hold a similar *voltage*, but they are very different at
delivering *current*. A 9V alkaline is built to give a little current for a long time. A LiPo is
built to give a lot of current right now. Motors need a lot of current right now.

This doc explains what happens inside each battery, what you gain and lose if you change the rover
to a LiPo, and how to choose the right battery at the start of your next project.


## The status quo: one 9V alkaline
The course uses a 9V alkaline battery for good reasons. It costs $1.59 (see the [BOM][01]). You can
buy one in any store. It needs no charger, it sits on a shelf for years, and it snaps onto a
battery clip in one second. It is also very hard to hurt yourself with one.

On the rover, the battery feeds two things. The [DRV8833 motor driver][02] takes the 9V directly
and sends it to the motors. A buck converter turns the 9V into 5V for the Pico, the servo, and the
ultrasonic sensor.

```text
 9V battery --+--> DRV8833 VM --> two motors
              |
              +--> buck converter --> 5V --> Pico, servo, HC-SR04
```

Everything shares one battery. Keep that in mind, because it is the reason a motor problem becomes
a Pico problem.


## The problem: the voltage is there until you use it
Measure a 9V battery with a multimeter and you see about 9V. That number is the *open-circuit*
voltage: the voltage when almost no current flows. It tells you very little about what happens when
the motors start.

Every battery acts like a perfect battery with a small resistor hidden inside it. That hidden
resistor is called the **internal resistance**.

```text
        inside the battery case
   +-----------------------------------+
   |                                   |
   |   perfect      internal           |
   |   battery      resistance         |
   |    (+) -------/\/\/\/\----------------(+)  to the rover
   |                                   |
   |    (-) -------------------------------(-)
   +-----------------------------------+
```

When current flows, some voltage is lost across that resistor before it leaves the case. The loss
is called **voltage sag**, and Ohm's law gives its size:

```text
 sag (volts) = current (amps) x internal resistance (ohms)
```

A fresh 9V alkaline has an internal resistance of roughly 1.5 to 2 ohms, and the value goes up as
the battery is used. A small LiPo pack is roughly 0.05 ohms. That is about 30 times lower.

Here is what each battery delivers to the rover at different loads. These are estimates, but the
pattern is the point.

| What the rover is doing | Current | Fresh 9V alkaline (1.7 ohms) | Half-used 9V alkaline (3 ohms) | 2S LiPo (0.05 ohms) |
| :-- | :-- | :-- | :-- | :-- |
| Pico and sensors only | 0.1 A | 9.2 V | 8.1 V | 8.0 V |
| Driving on a smooth floor | 0.5 A | 8.6 V | 6.9 V | 8.0 V |
| Both motors starting | 1.5 A | 6.9 V | 3.9 V | 7.9 V |
| Both motors stalled, servo moving | 2.5 A | 5.2 V | collapses | 7.9 V |

Look at the "both motors starting" row. The buck converter needs its input to stay well above 5V to
make a steady 5V. When the alkaline sags, the 5V rail drops, and the Pico resets. With the motors
off, the load is gone, the battery voltage comes back, and the Pico boots again. Then the motors
start again. That is the reboot loop.

The stalls come from the same place. A motor that gets 4V when it expected 9V cannot push the rover
over the edge of a carpet. A stalled motor then asks for even more current, which makes the sag
worse.

A battery that reads "8 volts but gives minimal current" is the half-used column. The multimeter
says it is fine. The motors say it is not.


## What is going on inside each battery

### Alkaline: a lot of energy, released slowly
An alkaline cell has zinc powder on one side, manganese dioxide on the other, and a paste of
potassium hydroxide between them. The chemical reaction is slow, and the charged particles (ions)
must move through thick, pasty material. That slow movement is the internal resistance.

Three more things make the 9V battery the worst case for motors:

1. **It is six tiny cells in a row.** Open a 9V battery and you find six small 1.5V cells in
   series. Their resistances add together, so the pack has six times the resistance of one cell.
2. **The cells are very small.** Less material means less surface for the reaction, so less
   current at one time.
3. **It gets worse as it empties.** Used-up material collects inside the cell and blocks the path.
   The resistance climbs and the voltage slides down, from about 9.5V when new to 6V or less.

The 9V alkaline was designed for smoke alarms, multimeters, and guitar pedals. Those devices use a
few thousandths of an amp for months. The [Energizer 522 datasheet][03] shows the result: the
capacity you get shrinks quickly as the current goes up.

### LiPo: built to move current
LiPo is short for *lithium polymer*. Inside, lithium ions move back and forth between a graphite
layer and a metal-oxide layer. The layers are paper-thin sheets, stacked or folded many times
inside a soft foil pouch. That gives an enormous surface area in a small space, and the ions have
only a very short distance to travel. The result is a very low internal resistance.

A LiPo also holds its voltage almost flat while it empties, then drops quickly at the end. So the
rover behaves the same at minute 40 as at minute 2.

The same chemistry makes a LiPo much less forgiving than an alkaline:

- **It can deliver a dangerous current.** A short circuit can push tens of amps through a jumper
  wire and melt it.
- **Overcharging damages it.** A cell must never go above 4.2V. That is why a LiPo needs a special
  *balance charger*.
- **Running it flat damages it.** A cell that drops below about 3.0V is permanently harmed.
- **Physical damage can start a fire.** A punctured, crushed, or swollen pouch must not be used.

A simple picture: the alkaline is a big water tank with a drinking straw for an outlet. The LiPo is
a smaller tank with a fire hose. The motors need the hose.


## First, get the LiPo voltages right
LiPo packs are named by how many cells are in series: 2S is two cells, 3S is three. Each cell is
3.7V nominal, 4.2V fully charged, and about 3.3V when it is time to stop.

| Pack | Fully charged | Nominal | Stop using at |
| :-- | :-- | :-- | :-- |
| 2S | 8.4 V | 7.4 V | about 6.6 V |
| 3S | 12.6 V | 11.1 V | about 9.9 V |

So a 2S pack is 8.4V at most, not 11.8V. The 11.8V number is something else: it is the *absolute
maximum* supply voltage in the [DRV8833 datasheet][04]. The recommended range for the driver is
2.7V to 10.8V.

That makes the choice clear:

- **3S is over the limit.** At 12.6V a fresh 3S pack is above the driver's absolute maximum. It can
  work for a while in a test and still shorten the life of the chip or destroy it. It also puts
  about 7.6V on motors meant for about 6V, at the course's `MAX_THROTTLE` of 0.6.
- **2S is the right size.** It runs from 8.4V down to about 6.6V, which is close to what a 9V
  alkaline gives. It is inside the driver's range, and at a throttle of 0.6 the motors see about 5V
  when the pack is full.

A quick 3S battery test can prove one useful thing. If the problem goes away, a poor performing random rover
problem is about current delivery and not the code or the wiring.


## Pros and cons of changing the rover to a 2S LiPo
This table compares the two batteries on the points that matter for the rover.

| | 9V alkaline | 2S LiPo (about 1000 mAh) |
| :-- | :-- | :-- |
| **Solves the reboots and stalls** | No. Even a fresh one sags at motor start-up | Yes. Sag is less than 0.2V at any load the rover can make |
| **Voltage during a run** | Slides from about 9.5V to 6V, so tuning drifts | Nearly flat from 8.4V to about 7V |
| **Run time** | Roughly 20 to 30 minutes of driving | Roughly 1.5 to 2 hours |
| **Cost for one rover** | $1.59 per battery, bought again and again | About $10 to $15 per pack, used for hundreds of charges |
| **Extra equipment** | None | Balance charger, fire-safe charging bag, low-voltage alarm, connector adapter, fuse |
| **Size and weight** | About 48 x 26 x 17 mm, 45 g | About 70 x 35 x 15 mm, 55 to 65 g. Longer and flatter |
| **Ready to use** | Open the package and snap it on | Must be charged before class, about one hour |
| **Storage** | Years on a shelf | Store at about 3.8V per cell, and check it every few months |
| **Safety** | Very safe for beginners | Needs rules, supervision, and a place to charge |
| **Where to get it** | Any store | Hobby shop or online, with shipping limits |

The prices and sizes for the LiPo are typical values, not a quote for a specific part. Check them
before you buy.

**Cost.** For one rover, the LiPo costs more on the first day and less over time. For a class it is
different. Nine alkaline batteries cost about $25 for each run of the course. Nine LiPo packs, two
or three chargers, charging bags, alarms, and adapters cost roughly $200 to $250 the first time,
and almost nothing after that. The LiPo pays for itself after many courses, not after one.

**Size.** A 2S pack is about the same weight as the 9V but a different shape. It will not fit a 9V
clip or a 9V holder, so it needs its own place on the chassis and Blu Tack or a strap to hold it.

**Readiness.** This is the largest cost, and it is not money. Someone must charge every pack before
class, check every pack after class, and put them at storage voltage if the next class is weeks
away. A 9V alkaline needs none of that.

**Will it solve the problem?** Yes. The sag table shows why, and the 3S test confirmed it.


## What must change on the rover
A LiPo is not a drop-in replacement. Plan for these changes:

1. **Connector.** A LiPo has no snap terminals. You need an adapter from the pack's power connector
   to the wires that the 9V clip used.
2. **Fuse.** Put a 3A fuse in the positive wire, close to the pack. The alkaline limited a short
   circuit by itself. A LiPo does not.
3. **Low-voltage alarm.** The rover will keep draining the pack until it is damaged. A small buzzer
   alarm plugs into the pack's balance connector and beeps at about 3.5V per cell.
4. **Buck converter check.** Make sure the 5V rail still reads about 5V when the input is 6.6V, the
   lowest voltage of a 2S pack.
5. **Compass calibration.** A different battery in a different place changes the magnetic field
   around the IMU. Run the magnetometer calibration again.
6. **Retune the motors.** The stall points and the speed in cm/s will change. Repeat the power and
   motor steps in the [tuning and calibration guide][05].
7. **Leave the capacitor in.** The 1000 µF capacitor across `VM` and `GND` still helps with motor
   noise.

Do not raise `MAX_THROTTLE` just because the rover now has power to spare. That limit protects the
motors, and the motors did not change.


## A third option to know about
The choice is not only alkaline or LiPo. Six AA NiMH rechargeable cells in a holder give 7.2V, have
a low internal resistance (roughly 0.2 to 0.3 ohms for the pack), and deliver several amps without
trouble. They are much safer than a LiPo, they use a simple charger, and they are easy to explain
to a beginner. The cost is size and weight: six AA cells are about three times as heavy as a 2S
LiPo.

For a class of beginners, NiMH is often the best middle path. For one experienced builder who wants
the smallest and lightest rover, the 2S LiPo is the better choice.


## What to think about earlier next time
The 9V battery looked right because only one question was asked: "Is the voltage right?" A battery
choice needs four questions. Ask them before you buy any parts.

1. **What is the peak current?** Add up the worst moment, not the average. For the rover that is
   two motors starting, plus the servo, plus the Pico with WiFi on: about 1.5 to 2.5A.
2. **Can the battery deliver that peak?** Multiply the peak current by the battery's internal
   resistance. If the sag is more than about 10% of the battery voltage, choose a different
   battery.
3. **What voltage can each part accept?** Write down the limits and find the narrowest one. On the
   rover: motors about 6V, DRV8833 2.7V to 10.8V, Pico `VSYS` 5.5V maximum, and the buck
   converter's own input range.
4. **How long must it run?** Divide the battery capacity in mAh by the average current in mA to get
   hours. Then take off about 25% as a safety margin.

This list of loads and limits is called a **power budget**. Ten minutes with a power budget on
paper would have shown that a 9V alkaline has a sag of 2.5V or more at motor start-up.

There was also an early warning in the project itself. The [BOM][01] lists an optional capacitor
"to buffer motor spikes and battery sag." When a design needs a part to hide a weak power supply,
the power supply deserves a second look.


## Rules of thumb
1. **Choose for peak current first, voltage second, capacity third.** Most battery problems on
   robots are current problems.
2. **Never use a 9V alkaline for motors.** It is good up to about 50 to 100 mA. Use it for logic,
   sensors, and alarms.
3. **Motors or servos mean a high-current chemistry.** That is AA alkaline at the least, and NiMH,
   LiPo, or Li-ion for anything that must work every time.
4. **Measure a battery under load.** The voltage with nothing connected tells you almost nothing.
   Measure it while the motors run.
5. **The full-charge voltage must be under every absolute maximum.** Use the *charged* number, not
   the nominal one. A 3S pack is a 12.6V pack.
6. **The empty voltage must be above what the regulator needs.** Check the low end too.
7. **For a LiPo, C rating times capacity is the maximum current.** A 1000 mAh pack rated 20C can
   give 20A. Plan to use half of that or less.
8. **Count the whole system, not only the battery.** Charger, safe storage, connectors, fuse,
   alarm, and the time to look after the packs are all part of the cost.
9. **Match the battery to the people.** The best battery for an expert can be the wrong battery for
   a room of beginners.
10. **Give motors and logic separate power if you can.** Then a motor surge cannot reset the
    computer.


## When to pick which
**Pick alkaline** when the device uses little current, must wait on a shelf for a long time, or will
be used by beginners with no charger nearby. Remote controls, sensors, clocks, and a Pico that only
reads a button are all good matches.

**Pick LiPo** when the device has motors, needs high current in a small and light package, and has
someone responsible for charging and storage. Drones, racing robots, and a rover that must run
hard for an hour are all good matches.

For the Random Rover, the 9V alkaline is the convenient choice and the wrong electrical choice. A
2S LiPo fixes the power problem completely. It brings new work with it: charging, a fuse, a
low-voltage alarm, and safety rules. If that work is acceptable, change to 2S. If it is not, six AA
NiMH cells fix the same problem with much less risk.


[01]:../lesson_plans/BOM.md
[02]:https://www.adafruit.com/product/3297
[03]:https://data.energizer.com/pdfs/522.pdf
[04]:https://www.ti.com/lit/ds/symlink/drv8833.pdf
[05]:strategy-for-tuning-calibration-random-rover.md
