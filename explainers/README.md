# README

This folder is where the "why does it work that way?" questions live. A class script or lesson
plan can't stop to explain, say, the whole history of the microcontroller every time it mentions
one — that would bury the actual build instructions. So instead, whenever a concept in the course
is worth a real explanation rather than a one-line aside, it gets pulled out into its own document
here, written in plain English for a middle/high-school reader. Each one is generated with the
`explainer` skill, which favors a narrative structure — status quo, then the problem, then the
solution — over a dry glossary-style definition, so a student reads it more like a short story
about *why* something was invented than a spec sheet about *what* it is.


## Usage

There's no root `README.md` in this repo — the full course documentation map lives in
`CLAUDE.md`, and it's worth a look if you want to see how everything here connects. Explainers
sit off to the side of the main syllabus/lesson-plan/BOM generation pipeline: they're
supplementary reading, not something a student needs to get through before a class. Think of them
as the answer to a question a curious student might ask mid-build — "wait, why CircuitPython and
not MicroPython?" — without making every lesson script stop and explain it inline. A lesson plan
or lesson script is free to link out to one of these whenever it touches a concept an explainer
already covers in more depth.


## Build Process

Nothing to build here — it's all static markdown. If you want a new explainer, that's what the
`explainer` skill is for; just invoke it with the topic you want covered. If you'd rather hand
someone a Word doc or PDF instead of a markdown file, pandoc will convert any of these directly:
`pandoc -f gfm <file>.md -o <file>.docx`, following the same export convention used elsewhere in
`CLAUDE.md`.


## Contents

| Topic | File/Directory Name | Description/Summary |
| :------ | :---------- | :------------ |
| CircuitPython vs. MicroPython | `micropython-vs-circuitpython.md` | Compares the two Python variants used on microcontrollers — their shared origins, where they diverge (upload workflow, libraries, governance), and why this course picks CircuitPython. Also contrasts both with C/C++. |
| The Random Rover | `what-is-the-random-rover.md` | Explains what kind of robot the course's capstone project is, why obstacle-avoiding rovers are a common first robotics build, and how its sense-decide-act loop compares to a Roomba and to more advanced autonomous machines. |
| Microprocessors vs. microcontrollers | `microprocessor-vs-microcontroller.md` | Explains the historical split between microprocessors (Intel 4004) and microcontrollers (TI TMS 1000), what distinguishes them, and why the Pico 2 W's RP2350 microcontroller is the right chip for this course's projects. |

## Future Explainers Topics

These are the topics on the list but not yet written — good candidates next time a student asks
a question one of them would answer:

- raspberry-pi-pico-2w-pinout.md
- microcontroller-serial-communications.md
- definition-of-terms-for-microcontrollers.md
- all-about-microcontroller-memory.md
- what-is-git-and-github.md
