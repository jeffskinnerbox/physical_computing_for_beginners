# STE Examples - Bad and Good
Each example shows text that does not follow STE (Bad), the STE version (Good), and the rules that changed it.
Use these examples as patterns. The topics come from the Physical Computing for Beginners course.


## 1. Procedure - Long Sentence, Passive Voice, Hedging
**Bad:**

> Before you go ahead and plug in the board, it's a good idea to make sure that the BOOTSEL button is being held down, since otherwise the RPI-RP2 drive won't be shown by your computer.

**Good:**

> 1. Push and hold the BOOTSEL button on the board.
> 2. Connect the USB cable to the board and to the computer.
> 3. Release the BOOTSEL button.
>
> The computer shows a new drive with the name `RP2350`.

**Rules:** one instruction per step, imperative verbs, no `-ing` verb, no contraction, no passive voice, result given after the step, filler phrases removed.


## 2. Description - Too Many Ideas in One Sentence
**Bad:**

> The HC-SR04, which is an ultrasonic distance sensor that works kind of like a bat, sends out a high-frequency sound pulse when its trigger pin goes high and then measures how long it takes for the echo to bounce back, which lets your code figure out the distance.

**Good:**

> The HC-SR04 is an ultrasonic distance sensor. It finds distance with sound, as a bat does.
> When the TRIG pin goes high, the sensor sends a short sound pulse. The sound hits an object and comes back to the sensor. The ECHO pin stays high for the time that the sound travels.
> Your code measures this time and calculates the distance.

**Rules:** one topic per sentence, maximum 25 words, most important information first, `-ing` forms removed, "figure out" (idiom) → "calculates".


## 3. Noun Cluster
**Bad:** `Adjust the left wheel encoder pulse count threshold value.`

**Good:** `Adjust the threshold for the pulse count of the left wheel encoder.`

**Rules:** maximum 3 nouns in a row.


## 4. Inconsistent Terms
**Bad:**

> Plug the Pico into your laptop. When the microcontroller shows up, copy the file to the device. Then reset the board.

**Good:**

> Connect the board to the computer. When the `CIRCUITPY` drive shows, copy `code.py` to the drive. Then push the RESET button on the board.

**Rules:** one term for one thing (`board`, `computer`, `drive`), "shows up" (phrasal verb with two meanings) → "shows".


## 5. Safety Instruction
**Bad:**

> Be careful with the battery pack because shorting it can get things really hot, so you'll probably want to unplug it when you're rewiring stuff.

**Good:**

> **WARNING:** Disconnect the battery pack before you change the wiring. A short circuit can make the wires hot enough to burn you.

**Rules:** warning word first, command first, then the risk, no contractions, no filler words.


## 6. Code Comments
**Bad:**

```python
# ok so now we're gonna loop forever and keep checking the button
while True:
    if not btn.value:   # pressed!!
        led.value = not led.value
        time.sleep(0.2)  # wait a bit
```

**Good:**

```python
# Main loop: check the button again and again, without end.
while True:
    # The button connects the pin to GND, so False means "pushed" (pull-up).
    if not btn.value:
        led.value = not led.value  # Change the LED: on to off, or off to on.
        time.sleep(0.2)            # Wait 0.2 s so that one push changes the LED only one time (debounce).
```

**Rules:** comments in STE, one idea per comment, units given, "why" given for the value `0.2`, slang removed. The code did not change.


## 7. Shell Command Block
**Bad:**

```bash
# install stuff
uv run wireframe.py /dev/ttyACM0
```

**Good:**

```bash
# Bash (Linux or macOS). Start the 3D orientation viewer.
# uv installs the needed Python packages the first time, then runs the script.
# /dev/ttyACM0 is the USB serial port of the board. Your port name can be different.
uv run wireframe.py /dev/ttyACM0
```

**Rules:** shell named, what and why given, variable part identified.


## 8. Text Diagram for a Complex Topic
**Bad (text only):**

> The Pico's GP14 goes to the AIN1 of the DRV8833 and GP15 to AIN2, and the motor connects to AOUT1 and AOUT2, with the battery on VM and grounds tied together.

**Good (sentence + diagram):**

> This diagram shows how the board controls one motor through the motor driver.

```text
  Board (Pico 2 W)          Motor driver (DRV8833)           Motor
 +----------------+        +----------------------+       +-------+
 |           GP14 +------->| AIN1           AOUT1 +------>|   +   |
 |           GP15 +------->| AIN2           AOUT2 +------>|   -   |
 |            GND +--+  +--+ GND               VM |<--+   +-------+
 +----------------+  |  |  +----------------------+   |
                     |  |                             |
                     |  |              Battery + -----+
                     |  |                      - ---+
                     |  |                           |
                     v  v                           v
                     GND                           GND
```

> The board sends two control signals (AIN1, AIN2). The motor driver uses battery power to turn the motor. The board and the motor driver must have a common GND.

**Rules:** complex connections shown as a diagram, one-sentence introduction, short sentences after the diagram.


## 9. Note vs. Instruction
**Bad:**

> Note: Make sure you save the file first or your changes will be lost.

**Good:**

> 1. Save the file.
>
> Note: The board restarts the code each time you save `code.py`.

**Rules:** an instruction goes in a step, not in a note. A note gives information only.

