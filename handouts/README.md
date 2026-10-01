# README

Printable per-class handouts and single-file HTML summaries/slide decks for Physical Computing for
Beginners — the short, hand-to-a-student material that sits alongside the full lesson plans and
lesson scripts, plus a running list of reference links (videos, datasheets) kept for building
future handouts.


## Contents

```text
.
├── class-00-handout.md                # Pre-Class link sheet: course docs, Pico 2 W pinout/datasheets, peripheral pinouts
├── class-03-handout.md                # "The Robotics Challenge": physical computing vs. robotics, sense/think/act, the four problems
├── class-3-the-robotics-challenge.html  # 12-slide HTML deck version of class-03-handout.md
├── class-03-summary.html              # 13-slide Class 3 deck "From Exploring to Engineering": H-bridge, open-loop drift, odometry, rover website
├── class-3-closing-the-loop.html      # 16-slide Class 3 deck: open vs. closed loop, debounced wheel ticks, KI integral control, tuning homework
├── class-04-summary.html              # 17-slide Class 4 deck "A Sense of Balance": Class 3 recap, LSM9DS1, roll/pitch/yaw, Mahony filter
├── build-challenge.md                 # what a build challenge is, plus project-idea links (I2S audio, packet radio, ball-balancing robot)
└── references-and-resources.md        # curated link list: Pico 2 W docs, learning Python, CircuitPython, Mu/Thonny, project + parts sources
```


## Purpose / Role in Repository

Handouts are supplementary to the main generation pipeline described in the root [README][01]:
the instructor teaches from [`lesson_plans/`][02] and students build from
[`lesson_scripts/`][03], while these files are the quick take-home or on-screen summary of a
class. The markdown handouts are written by hand; the `.html` decks are self-contained single-file
slide presentations (the two `*-summary.html` decks were built from the Class 3/4 lesson scripts
with the `/html_slide_deck` skill — see `input/my-prompts.md`). Open one in any browser; no server
needed, and without internet it just falls back from its web fonts. Deeper "why does it work that
way" topics live in [`explainers/`][04] instead.

`class-00-handout.md` links to `references-and-resources.md` (and `build-challenge.md` to this
folder) by GitHub URL, so keep those names stable.


## Usage

```bash
# open an HTML deck (arrow keys / on-screen controls to navigate)
xdg-open class-04-summary.html        # Linux; on Windows: start class-04-summary.html

# export a markdown handout for printing
pandoc -f gfm class-03-handout.md -o class-03-handout.docx
```


## Notes

- Handouts exist only for the classes listed above; there is no per-class handout for every
    class yet.
- The Resources section below is scratch notes — links collected for future handouts, not yet
    folded into `references-and-resources.md`.
- See the root [README][01] for the course map and [`CLAUDE.md`][05] for repo conventions.


## Resources

Embedded systems

- [Embedded Firmware Explained in Simple Terms][06]
- [All About Microcontroller Memory - Flash, RAM, EEPROM | Embedded Systems Explained][07]
- [Embedded Systems Explained][08]
- [Hackaday Europe 2026: Nicola Cimmino - The 1-Bit CPU That Ran Factories][09]

Datasheets

- [GPIO pinout and pin function guide for the Raspberry Pi Pico 2 W][10] - Make sure it says
    "Raspberry Pi Pico 2 W Pinout" at the top left corner of the page
- [Raspberry Pi Pico 2 W Datasheet][11]
- [RP2350 Microcontroller Product Brief][12]
- [Hardware Design With RP2350][13]

Serial communications

- [Serial Communications Explained: UART, I2C, and SPI][14]
- [I2C, SPI and UART Explained - Communication Protocols in Embedded Systems for Beginners][15]
- [UART vs SPI vs I2C: A Quick Comparison][16]


[01]:../README.md
[02]:../lesson_plans/README.md
[03]:../lesson_scripts/README.md
[04]:../explainers/README.md
[05]:../CLAUDE.md
[06]:https://www.youtube.com/watch?v=MqFqF-kGQGA&t=51s
[07]:https://www.youtube.com/watch?v=lPFZsCDTIfw&t=103s
[08]:https://www.youtube.com/watch?v=xaCAIZKu_zQ&list=PLeAb9_hv082weQ10WcvFfLBlNcCYXlQ4q
[09]:https://www.youtube.com/watch?v=ioL9cbNx0O8
[10]:https://pico2w.pinout.xyz/
[11]:https://pip-assets.raspberrypi.com/categories/1088-raspberry-pi-pico-2-w/documents/RP-008304-DS-3-pico-2-w-datasheet.pdf
[12]:https://pip-assets.raspberrypi.com/categories/1214-rp2350/documents/RP-008374-DS-1-rp2350-product-brief.pdf
[13]:https://pip-assets.raspberrypi.com/categories/1214-rp2350/documents/RP-008280-DS-1-hardware-design-with-rp2350.pdf
[14]:https://www.youtube.com/watch?v=IyGwvGzrqp8
[15]:https://www.youtube.com/watch?v=q0V3tuf7Az4
[16]:https://www.youtube.com/shorts/itFzfhZ2C-4
