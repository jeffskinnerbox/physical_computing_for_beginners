# README

Standalone explainer documents generated via the `explainer` skill. Each one takes a technical
concept that comes up while teaching Physical Computing for Beginners and breaks it down in
plain English for a middle/high-school audience, using a narrative structure (status quo →
problem → solution, or similar) rather than a dry reference definition.


## Usage

This repo has no root `README.md` — see the project's `CLAUDE.md` for the full course
documentation map. Explainers are supplementary background reading, not part of the generated
syllabus/lesson-plan/BOM pipeline: they exist so a student (or instructor) can look up "why do we
use CircuitPython instead of MicroPython?" or "what is a microcontroller anyway?" without that
detail cluttering the lesson scripts. Lesson plans and lesson scripts may link out to an explainer
when a class touches a concept one already covers.


## Build Process

No build process — this directory holds static markdown reference files. To generate a new
explainer, invoke the `explainer` skill; to export an existing one to `.docx`/`.pdf`, use
`pandoc -f gfm <file>.md -o <file>.docx` per the conventions in `CLAUDE.md`.


## Contents

| Topic | File/Diectory Name | Description/Summary |
| :------ | :---------- | :------------ |
| CircuitPython vs. MicroPython | `micropython-vs-circuitpython.md` | Compares the two Python variants used on microcontrollers — their shared origins, where they diverge (upload workflow, libraries, governance), and why this course picks CircuitPython. Also contrasts both with C/C++. |
| The Random Rover | `what-is-the-random-rover.md` | Explains what kind of robot the course's capstone project is, why obstacle-avoiding rovers are a common first robotics build, and how its sense-decide-act loop compares to a Roomba and to more advanced autonomous machines. |
| Microprocessors vs. microcontrollers | `microprocessor-vs-microcontroller.md` | Explains the historical split between microprocessors (Intel 4004) and microcontrollers (TI TMS 1000), what distinguishes them, and why the Pico 2 W's RP2350 microcontroller is the right chip for this course's projects. |


## Future Explainers Topics

Listed below are explainer topics that haven't been generated yet.

- raspberry-pi-pico-2w-pinout.md
- microcontroller-serial-communications.md
- definition-of-terms-for-microcontrollers.md
- all-about-microcontroller-memory.md
- what-is-git-and-github.md
