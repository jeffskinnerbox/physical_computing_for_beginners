
# My Prompts

To create the course materials for.the course [Physical Computing for Beginners](https://www.makersmiths.org/event-6785489)
the series of Claude Code prompts were used.

* [10 Rules for Getting Better Results from AI Coding Agents](https://www.kdnuggets.com/10-rules-for-getting-better-results-from-ai-coding-agents)

----

# My 1st Prompt - Create `teen-install-instruction` Skill

I foresee a need to give my students detail instruction on how to install software, particularly on
Windows 11 and Ubuntu under WSL.
This prompt is all about creating documented instruction for teens to do the required install of software.
This became the 1st prompt mainly because it was the clears need that I have to address.
To me, it not the logic place to begin but more of a know problem that required a solution.
I'm like to iteratively improve this prompt and those updates will be added here.

## Context

Using your your `SKILL.md` creation skills,
I want to create a Claude `SKILL.md` file with the name `teen-install-instruction`.
The skill is for the generation of instruction used by a 12 to 18 year old person.
This person has elementary understanding of Bash, PowerShell, Python commands.
The instructions concern loading software onto Ubuntu 24.04 server, Windows 11 laptop,
or a CircuitPython capable micro-controller.
The instructions need to be well commented sequence of Bash, PowerShell,
Python commands written in a Markdown formatted file.

## Do First

When the skill you create starts, it should first do the following:

* Prompt the user for a simple description of this installation
  and the name that will be give to that skill.
* Ask the user for URLs to preferred sources or directory paths to preferred documents
  that are good sources of installation instructions, but these source do not need to be used exclusively.
* Ask as many questions required to clarify any ambiguity in the task it needs to perform.

## Instruction File Format

The instructions file the skill creates will have this overall format:

* 1st section should give purpose of this installation, that is, what the user gains from this installation.
* 2nd section in the file is a list (or table) of what will be installed with a description of what will be installed,
  it specific purpose, a reference URL to where these instruction are taken from,
  and URL links to formal documentation on how to use what is being installed.
* 3rd section describes the hardware & software of the target environment where the installation is to be performed.
* Subsequent section will contain the actual installation instructions.
  This should be a sequence of Bash, PowerShell, Python commands for the installation.
* Break the sequences into logically separate sections when you change targets or tools.
  Each of these separate section should have text describing the change of context.
* Separate large install sequences into major blocks within their own sub-section of the document.
* Each major block installation scripts should conclude with a test script to validate the installation.
  There should be at least one test like `<installed-tool> --version`,
  but the execution of the install software on test data should be done where it can be done.
  Also include instructions on any cleanup activity (e.g. Removal of test data, etc.) required after testing.
* Final section should be titled "Troubleshooting notes" and include here any guidance about troubleshoot common problems / errors.

## Markdown conventions and tooling

Generated documents are GitHub-flavored Markdown. Linting/formatting uses **markdownlint-cli2** with the
repo config `.markdownlint-cli2.jsonc` (not globally installed — run via `npx markdownlint-cli2 "**/*.md"`).
The config is a regular committed file in the repo root (it was previously a symlink into the instructor's
dotfiles `~/.dotfiles/checker-files/`, which is where the canonical copy still lives).
Key non-default rules to honor when editing Markdown by hand:

* Unordered-list indent is **4 spaces** (`ul-indent`), not 2.
* Long lines are allowed (`line-length` = 100).
* Headings: 2 blank lines above, 0 below (`blanks-around-headings`).

All links in generated course documents use **reference-style** form (`[text][01]`) with definitions
collected at the bottom of the file, numbered `[01]`, `[02]`, … with no space before the colon and no
duplicate URLs.
Do not use the URL string to create the `[text]`, but instead, provide a short informative string.

Export to other formats with **pandoc** (installed): `pandoc -f gfm input.md -o output.docx`
(or `-o output.pdf` with a PDF engine).

## Common commands & recurring steps

There is no build or test suite. The relevant commands are:

```bash
npx markdownlint-cli2 "**/*.md"                           # lint all Markdown against .markdownlint-cli2.jsonc
pandoc -f gfm lesson_plans/syllabus.md -o syllabus.docx   # export a doc
```

Note: the linter is **not** clean on the generated docs — it reports pre-existing, tolerated style
warnings (e.g. `MD013` lines over 300, `MD036` emphasis-used-as-heading, `MD060` table-pipe spacing).
Don't assume your edit caused these or chase a zero-warning result; just confirm you didn't add *new* ones.

## Validation Step

After the instructions have been created, perform the following validation steps:

* Start a separate agent that will validate that the main agent is using the most up to date installation procedures for your target environment.
  If modifications are recommended by this agent, the main agent should be informed and iterate until they agree.
  The main agent should then make any corrections required.
* Next, start another agent and ask it to create a Docker sandbox where it will validate the instructions just created.
  If prerequisite installs are identified, the main agent needs to be informed to include them.
  If errors are found, then the main agent should be informed, make corrections and iterate until they agree.

## Final Step

* At the concussion, the main agent will summarize any of the validation failures and the corrective action taken.
* Write the installation script into a file with the name provided by the user.

----

# My 2nd Prompt - Use `/teen-install-instructions`

This how I used the `SKILL.ms` created above.

## Context

Using `/teen-install-instructions` skill, create installation instructions for
installing and activating Windows Subsystem for Linux (WSL) on Windows 11.
If any installation steps requires you have administrator right,
provide a "Path B" set of instruction for that case.

* The description of this installation is: Installation of Windows Subsystem for Linux (WSL) on Windows 11
* Name of the installation file is: @install-wsl-on-windows-11.md


----

# My 3rd Prompt - Create candidate-projects.md Document

I want you to identify 2 candidate projects for each class in my "Physical Computing for Beginners" course.
Read the `@input/my-vision.md` file.

Work in three phases. Do not skip ahead, and stop for my approval between each phase.
Maintain a file called `@claude-log.md` throughout listing
your candidate sources you have identified,
evaluation score for the candidate,
short description of what the candidate does,
and why it was selected or rejected.

If this session ever restarts,
read the `@input/my-vision.md`  and  `@claude-log.md` files,
and resume from where they left off.

## Phase 1 - Candidate List

Search online for candidate project
Do not include sources older 5 years old.
You can include candidates that use MicroPython code.
Look for candidates that include some of these components:
N20 Motor,
Robot Car Chassis,
Ultrasonic Module,
Servo Motor,
DC Motor Driver,
IMU,
Rotary Encoder,
TFT Display OLD Display,
Button, Cables, Wires, Breadboard, Batteries.
You can include candidates that use different versions of components listed in `@input/my-version.md`

Only consider sources that have a full listing of code on the sources website or within an online repository like GitHub.
Look for candidates that are unique & different from candidates that you have already selected.
List your selected candidates in  `@claude-log.md`
Target number of candidate is 50, but do not run any longer than 15 minutes.  Once this reached move to the next Phase.

## Phase 2 - Evaluation

Start a separate agent that will evaluate the candidates from Phase 1.
Read the `@input/my-vision.md`  and  `@claude-log.md` files.
Evaluate each candidate for fit with the courses objectives, constrains, and format.
Create a candidate evaluation process and numerical scoring scheme.
When you identify candidate are effectively the same, evaluate them and select one.
Document your evaluation process in `@claude-log.md` and your evaluation for each candidate.

## Phase 3 - Select Candidates for Classes

Start a separate agent that will evaluate the candidates from Phase 2 and document the findings.
Read the `@input/my-vision.md`  and `@claude-log.md` files.
Examine critically the evaluation process documented in `@claude-log.md`,
and if see a need to modify the Phase 2 evaluation process, explain why,
and document it in `@claude-log.md`.
Using your evaluation process, select two candidates for each class.

Create a document `@candidate-projects.md` with a description of the project,
evaluation score for the candidate,
URLs to documentation and code sources,
description (500 words or less) of what the candidate does,
and why it was selected.
There should be 2 candidates for each class and their should be increasing function
or sophistication as you move from classes 1 to 6.

----

# My 4th Prompt - Create Development Environment for CircuitPython on Raspberry Pi Pico 2W Microcontroller

Using `/teen-install-instructions` skill, create installation instructions for a Microsoft Windows 11 laptop,
with a development environment for CircuitPython on Raspberry Pi Pico 2W microcontroller.
This develop environment is within Windows, not Windows Subsystem for Linux (WSL).

Also include install steps for:

* The editors that will be used are [Mu](https://learn.adafruit.com/welcome-to-circuitpython/installing-mu-editor) and [Thonny](https://learn.adafruit.com/circuitpython-libraries-on-micropython-using-the-raspberry-pi-pico/thonny-setup)
* Also include install of CircuitPython UF2 firmware itself.
* Adafruit CircuitPython Library Bundle:
  Almost every beginner tutorial needs a library (NeoPixel, sensors, displays) that isn't built in.
  Including as a "drag these folders onto your CIRCUITPY drive" step.

The description of this installation is: Windows 11 Development Environment for CircuitPython on Raspberry Pi Pico 2W Microcontroller
Name of the installation file is: @tech_setup_check/install-circuitpython-dev-env-on-windows-11.md

----

# My 5th Prompt - Improve Class Descriptions

I want you to make improvements to each class sub-sections in the "Chronological Sequence of Class Projects" section.
To create these improvement, create experimental code that is likely need for the class.
Examine this code and make updates to the class documentation.
Validate the code by checking for class write-up, modifying the code & write-up until they are consistent.
Write the code to a file like @class-1-code.py.
If there are multiple python code for a class just number then sequentially.

----

# My 5th Prompt - Create Syllabus

## Context

Using the `/syllabus_generator` and `/grill-me` skills,
read the @input/my-vision.md and @communications/course-description.md files
and create a syllabus and place it in @lesson_plans/syllabus-physical-computing-for-beginners.md.

----

# My 6th Prompt - Create Class Lesson Plans

Using the `/lesson_plan_generator skill`, create lesson plans for all classes.
Make sure lesson plan follows the outline in the `@lesson_plans/syllabus-physical-computing-for-beginners.md` document
and make use of the `/theory_of_operation`, `/history_and_application`, and `/explainer` skills.
Make sure the lesson plans flow easily through each class with minimal gaps or repetition in key work & concepts.
Put the lesson plan for class X in `@/lesson_plans/class-0X-lesson-plan.md` file for X, 1 thru last class numbers.
Create a lesson plan for the first class then stop and let me review it.

----

# My 7 Prompt - Create a BOM

1st Step:
Read the all the documents in `@lesson_plans` to identify any materials, including software (e.g. Mu) and things the student needs to supply (e.g. USB cable),
that might have been left out of the "Bill of Materials (BOM)" section of `@input/my-vision.md`.
Update the tables in  `@input/my-vision.md` with this missing information.
Pause at the conclusion of this step for user review.

2nd Step:
Use the `/bill_of_materials_generator` to improve the bill of material content in the file `@input/my-vision.md`.
Use the `/grill-me` to clarify any questions you may have.
Make sure to follow the reference links to get information about sources & cost.
Pause at the conclusion of this step for user review.

3rd Step:
Use the `/bill_of_materials_generator`, create a document `@lesson_plans/BOM.md` containing just the bill of materials tables in the file `@input/my-vision.md`.
Within `@lesson_plans/BOM.md` include any explanatory text so its the data is understood by people who will be financing the class.

----

# My 8th Prompt - Create Lesson Scripts

/plan
Review this entire directory concerning the course I will be teaching.
I have completed a detail vision of how the course will operate, goals/expectations, etc.
all documented in @input/my-vision.md.
From @input/my-vision.md, I have generated the contents of the @lesson_plans directory.

I now want you to help me generate lesson scrips for each each class.
I define a lesson scripts as follows:
1. A lesson script is a markdown file that gives very detail instruction to the instructor on how to build and code the class project.
1. The lesson script will be given to the students of the class to follow along.
   The lesson script will be accessible to the student and instructor via a GitHub site,
   and the student will use the lesson script to copy&paste commands and code for their creation of the project.
1. The lesson script will be a combination of explanatory text and CircuitPython code (or other types of code) needed for the project.
1. The lesson script needs to be sufficiently detailed so that a student, without the aid of the instructor, can do the project.
1. The example code (considered pseudo-code) in the lesson plans is lightly commented,
   but the expectation is the code in the lesson script will be commented in more detail and must complete in every why.
1. The explanatory text in the lesson script should describe each of the breakout boards, devices, key CircuitPython modules, PIN outs, etc.
1. The code in the lesson script will build the project in phases,
   as outline in its corresponding lesson plan document in @lesson_plan/ directory.
   You should include print statements so the student can see what is happening in the code.
1. The lesson script will not only provide code for the project but will also provide a detail plan to construct the project physically.
   This includes a wiring table of the breadboard, microcontroller, breakout boards, discrete components (switches, LED, resistors, etc.), etc.
1. At the very end of the lesson script, the projects entire CircuitPython code should be listed,
   with comments, but amount of print statements could be reduced to avoid clutter.
   Also a wiring table should be provided for the physical build.
   This last section should be useful for a student to jump to the end and build the whole project
   without going through all the earlier build steps in the lesson script.
1. The first section in the lesson script should say what this project is all about,
   and the last section should outline what the student should have learned.
1. All lesson script should look similar and have the same structure and flow.
1. The naming convention for the lesson script documents will follow the same pattern as that used for the lesson plans.
1. Use the following as your lesson script template document:

  ```markdown
  ## 1. What This Project Is
  Plain-language, student-voice intro: what gets built this class, why it matters, how it connects
  to the rover build overall. (Req: first section states what the project is about.)

  ## 2. What You'll Need
  Materials table (component name, quantity, purpose) — pulled from the companion lesson plan's
  "Materials & Components" section, filtered to per-student items only (no cost/sourcing — that's
  the BOM's job per CLAUDE.md's "don't hand-edit out of sync" rule).

  ## 3. Meet the Hardware
  For each new device/breakout board this class: what it is, the key CircuitPython module(s) it
  uses, and its pinout — written so a student who's never touched the part before understands what
  they're connecting and why. (Req: explanatory text on breakout boards, devices, modules, pinouts.)

  ## 4. Build It: Phase 1 — [phase title, e.g. "See the Bounce"]
  * **Wiring for this phase** — markdown table (component -> Pico 2 W pin), scoped to what's needed
    so far.
  * **What this code does** — short explanation before the block.
  * **The code** — complete, fully-commented CircuitPython (not pseudocode), with print statements
    so students see what's happening at each step. Comments explain *every* meaningful line, more
    densely than the lesson plan's pseudocode.
  * **Try it / what you should see** — expected serial console output.
  * **Checkpoint** — a concrete pass/fail the student can self-check before moving on.

  ## 5. Build It: Phase 2 — [...] (repeat Section 4's pattern once per code phase)
  Number of phases = number of `class-N-code-*.py` files the companion lesson plan defines for that
  class (e.g. Class 1 has 2 phases, Class 2 has 3, Class 5 has 1, Class 6 has 3).

  ## [N]. Troubleshooting Guide
  Consolidated problem/cause/fix table, adapted from the companion lesson plan's Troubleshooting
  Guide but reworded for a student reading independently (no instructor assumed present).

  ## [N+1]. Put It All Together
  The complete, final version of this class's project in one place — for a student who wants to
  skip the phased walkthrough and build straight through:

  * Full wiring table (every connection, this class's complete circuit)
  * Full CircuitPython code, comments kept, print statements trimmed to the essentials (not
    removed entirely — enough to confirm the program is alive and working)

  ## [N+2]. What You Learned
  Plain-language recap tied back to Section 1's stated goal — what the student can now do that they
  couldn't before this class. (Req: last section states what should have been learned.)

  ## References
  Reference-style links `[text][01]`, definitions block at bottom — reuse/adapt the companion lesson
  plan's Resources & References section, adding any student-friendly sources (e.g. device datasheets,
  Adafruit guides) not already listed there.
  ```

## Markdown Conventions and Tooling
Generated documents are GitHub-flavored Markdown. Linting/formatting uses **markdownlint-cli2** with the
repo config `.markdownlint-cli2.jsonc` (not globally installed — run via `npx markdownlint-cli2 "**/*.md"`).
The config is a regular committed file in the repo root (it was previously a symlink into the instructor's
dotfiles `~/.dotfiles/checker-files/`, which is where the canonical copy still lives).
Key non-default rules to honor when editing Markdown by hand:

* Unordered-list indent is **4 spaces** (`ul-indent`), not 2.
* Long lines are allowed (`line-length` = 100).
* Headings: 2 blank lines above, 0 below (`blanks-around-headings`).

All links in generated course documents use **reference-style** form (`[text][01]`) with definitions
collected at the bottom of the file, numbered `[01]`, `[02]`, … with no space before the colon and no
duplicate URLs.
Do not use the URL string to create the `[text]`, but instead, provide a short informative string.

Export to other formats with **pandoc** (installed): `pandoc -f gfm input.md -o output.docx`
(or `-o output.pdf` with a PDF engine).

----

# My 9th Prompt - Create Some Homework for Pre-Class

Do the following to @tech_setup_check/install-circuitpython-dev-env-on-windows-11.md, and in no other file:
1. At the bottom of @tech_setup_check/install-circuitpython-dev-env-on-windows-11.md,
   create a new section titled "## Homework Assignment".
   Explain that the contents of this section are homework problems that will
   expand there understanding of what the microcontroller can do.
1. Each homework exercise should have a description of the function of the code.
   Next provide the full code block, well commented, to be installed on the microcontroller.
   Close with examples on how this code could be used to solve a real world problems.
1. Here are suggested homework exercises:
    * Make the microcontroller a WiFi Captive Portal Access Point
      Using the code for blink the onboard LED, show the LED status on a webpage.
      In the Homework assignment description should include the SSID and password stored in a Yaml file called `env.yaml`
    * Make the microcontroller tell its secrets about the mapping of
      external PIN number, external PIN name, Python PIN name, PIN functions by printing them to console.
      Include a Website URL link to the official sources for this information.

Start a sub-agent to research other possible homework exercises.
All exercises must use only the microcontroller alone or with the TFT display.
Find five, recommend two & why, and let me select one or two to be added to the list of exercise I provided.

----

# My 10th Prompt - Merge install-circuitpython-dev-env-on-windows-11.md into class-00-lesson-script.md

Using the skill /file-combining, @tech_setup_check/install-circuitpython-dev-env-on-windows-11.md
into @lesson_scripts/class-00-lesson-script.md.

Here are some overriding desires when doing this merge:
1. The resulting merged document should have the structure of @lesson_scripts/class-00-lesson-script.md.
   Add new sections as required but the high level structure should undergo minimal change.
1. Make sure the merged document includes all the software installation steps from @tech_setup_check/install-circuitpython-dev-env-on-windows-11.md
1. The "## Homework Assignment" of @tech_setup_check/install-circuitpython-dev-env-on-windows-11.md
   should be move in its entirety into @lesson_scripts/class-00-lesson-script.md.

----

# My 11th Prompt - Create Create GitHUb Repository
I want to start using git within this project and create a Github repository for this project.
Create for me a Bash script that will prompts me for all the required information,
and at the end, prints out the information for me to validate and then performs the task.
Create the Bash script and put documentation on how to use the script as a comments block at the top of the Bash file.
The script should check first if git or github is already being used and only make modifications as requested by user.
Place this executable Bash script in @tech_setup_check/setup-gethub.sh
Don't execute, I wish to inspect it.

----

# My 12th Prompt - Create Uninstall Script for Pre-Class Tools
After the "What You Learned" section in @lesson_scripts/class-00-lesson-script.md,
create a new section that describes how all the code, tools, libraries, etc. that that we installed can be uninstall from the Windows 11 PC.
Point out that this not generally necessary but only if you want to return the PC to its ordinal condition.
Us the same writing style used in the installation sections.
Also give the user a way to assure the install was done completely & correctly (aka validation of the uninstall).

----

# My 13th Prompt - For a class-xx-lesson-script.md, Create HomeWork Project Candidates
For the @lesson_scripts/class-xx-lesson-script.md (called here the "current class"),
use a sub-agent to identify 6 projects for the "Homework Assignments" section.
These projects can only use devices & breakout boards used in this class or prior classes.
These projects should demonstrate / teach something not yet done for the current class
and should not repeat what was done in previous classes.
Review the candidate project with me, one at a time in detail, for my approval, rejection, or modification.

Once all the homework projects have been reviewed, add the projects to the "Homework Assignments" section
using the lesson_scripts/class-00-lesson-script.md document as a template for content and format.

Using a sub-agent, compare the current class to lesson_scripts/class-00-lesson-script.md.
Identify inconstancies and recommend  modifications to the current class.

----

# My 14th Prompt - Using the `/explainer` skill, create `micropython-vs-circuitpython.md`
using the /explainer skill, create a document located @explainer/micropython-vs-circuitpython.md
discussing the use, origins, and current state of MicroPython and CircuitPython.
Point out what MicroPython and CircuitPython share in common and what makes them different.
Point out when one is preferred over the other.
Point out who are the typical users and how MicroPython & CircuitPython differ from languages like C++.
My target audience are the students for my class.

----

# My 15th Prompt - Using the `/explainer` skill, create `microprocessor-vs-microcontroller.md`
Using the /explainer skill, create a document located @explainer/microprocessor-vs-microcontroller.md
discussing the origins of microprocessor & microcontrollers, the problem they are intended to solve,
and what makes them different.
Give specific examples of where they are used and how the user experience may be similar and different.
Point out when one is preferred over the other.
My target audience are the students for my class.

----

# My 16th Prompt - Using the `/explainer` skill, create `what-is-the-random-rover.md`

Using the /explainer skill, create a document located @explainer/what-is-the-random-rover.md
that describes the Random Rover, which is the end product of this series of classes.
Point out this type of robot is a popular first robot for a new student of robotics.
Point out that it has a simple "brain" much like a insect.
Point out that it meets the definition of a robot because it senses its environment, makes a plan for its movement, moves, and sense once again.
Point out that its an autonomous robot and explain what this means.
Point out that while it meets the definition of an autonomous robotic,
and is similar to a Roomba vacuum cleaner,
it is far from what industrial, self-driving cars, and humanoid robots require.

----

# My 17th Prompt - Create a README.md File Creation Skill
Using your your `SKILL.md` creation skills,
create a skill that will generate a README.md file for a specified directory.
Call this skill `readme_generator`.
The skill should read the @CLAUDE.md document for context and then focus only on the directories specified by the user.
Read the contents in the specified directory, and any existing README.md file in the directory.
If a README.md file exist, use the contents of the README.md file as a directive or guide for the contents to be created.

If no README.md file exist use the following format:

```markdown
# README
{Purpose of this specific folder/module}

## Usage
{How it fits into the larger project (often linking back to root README)}

## Build Process
{Local build/test instructions if they differ from root}

## Contents
{summaries the directory using a table like this}

| Topic | File/Diectory Name | Description/Summary |
|:------|:----------|:------------|
{The "Description/Summary" should be no more than 50 words.}
```

Before writing the README.md file, use the `\grill-me` skill to clarify any ambiguities.

Once the README.md file is created, lint the file and make corrections as needed.

----

# My 18th Prompt - Using the `/explainer` skill, create `raspberry-pi-pico-2w-pinout.md`
Using the /explainer skill, create a document located at @explainer/raspberry-pi-pico-2w-pinout.md
discussing what is a pinout (reference wikipedia as a source), what is it used for, how is its use communicated,
where can I find it for the raspberry pi 2W (reference <https://pico2w.pinout.xyz/#i=ph>) as one of your sources,
and how do I find the pinout for for other devices.
My target audience are the students for my course.

----

# My 19th Prompt - Using the `/explainer` skill, create `spi-i2c-uart-serial-communications.md`
Using the /explainer skill, create a document located at @explainer/spi-i2c-uart-serial-communications.md
discuss what serial communication and what its important within microcontrollers.
Discuss what SPI, I2C, and UART abbreviations stand for,
what these protocols are used for, how they operate,
and how they are accessed on the Raspberry Pi Pico 2W via CircuitPython.

Still using the /explainer skill, cross reference this document within @explainer/raspberry-pi-pico-2w-pinout.md.
Make sure you reference both ways, using URL links, and do it multiple place when useful.
Modify the text in both, as necessary, for optimal impact.

My target audience are the students for my course.

----

# My 20th Prompt - Using the `/explainer` skill, create `types-of-pins-on-raspberry-pi-pico-2w.md`
Using the /explainer skill, create a document located at @explainer/types-of-pins-on-raspberry-pi-pico-2w.md
and discuss all the pin functions and what the abbreviation stands for (reference <https://pico2w.pinout.xyz/#i=ph>):
SPI, I2C, UART, Ground, VBUS 5V, VSYS 5V, 3V3 En, 3V3 Out, ADC VRef, GP28 A2, ADC Gnd, GP27 A1, GP26 A0, RUN.
Discuss what these pins are used for, how they operate,
and how they are accessed on the Raspberry Pi Pico 2W via CircuitPython.

Still using the /explainer skill, cross reference this document within
@explainer/raspberry-pi-pico-2w-pinout.md and @explainer/spi-i2c-uart-serial-communications.md.
Make sure you reference both ways, using URL links, and do it multiple place when useful.
Modify the text in all, as necessary, for optimal impact.

My target audience are the students for my course.

----

# My 21st Prompt - Using the `/explainer` skill, create `glossary-of-terms-for-microcontrollers.md`
Using the /explainer skill, create a document located at @explainer/glossary-of-terms-for-microcontrollers.md
providing definitions / descriptions / uses of the following:
microcontroller (MCU),
ADC (Analog-to-Digital Converter),
CPU (Central Processing Unit),
EEPROM (Electrically Erasable Programmable Read-Only Memory),
Firmware,
Flash Memory,
GPIO (General Purpose Input/Output),
I2C (Inter-Integrated Circuit),
Interrupt,
RAM (Random Access Memory),
SPI (Serial Peripheral Interface),
UART (Universal Asynchronous Receiver/Transmitter),
PWM, DMA, Watchdog Timers,
NVM (Non-Volatile Memory),
DMA (Direct Memory Access),
DAC (Digital-to-Analog Converter),
ISR (Interrupt Service Routine),
NVM (Non-Volatile Memory),
PWM (Pulse Width Modulation),
Register,
RTOS (Real-Time Operating System),
SRAM (Static Random Access Memory),
Timers/Counters,
WDT (Watchdog Timer),
low-power mode definitions (like Sleep, Deep Sleep, or Brown-out Reset).
Organize these by topics areas with a few sentences about the topic area as a common introduction.

My target audience are the students for my course.

I added later the prompt ... Using the /explainer skill, add to @glossary-of-terms-for-microcontrollers.md the term pull up/down resistor

----

# My 22nd Prompt - Using the `/explainer` skill, create `what-are-breadboards-and-dupont-wires.md`

Using the /explainer skill, create a document located at @explainer/what-are-breadboards-and-dupont-wires.md
Explain the origins of the name "breadboard",
providing definitions / descriptions of a breadboard wire (give link to wikipedia),
why are the used,
they typically come in 3 inch & 6 inch boards (some smaller),
they have a channel down the middle & say way its there,
discuss the purpose of the rail down the left&right sides,
discuss how the holes are interconnected,
and when should you not use a breadboard.

Explain the origins of the name "Dupont wire" (also known as jumper, jump wire, jumper wire),
providing definitions / descriptions DuPont wire (give link to wikipedia),
what are they used for,
discus how you can purchase them in multiple lengths (typically 10cm, 15cm, 20cm),
come multiple terminal types (male-male / male-female / female-female),
come in multiple colors, you can even make your own if you wish to crimp them,
and you can do without an just use solid 22 AWG wire,
and when should you not use a Dupont wires.

My target audience are the students for my course.

----


# My XXX Prompt - Create `lesson_script_generator` Skill

----










# My XXX Prompt - Create `circuitpython_class_script` Skill

## Context
Using your your `SKILL.md` creation skills,
I want to create a Claude `SKILL.md` file with the name `circuitpython_class_script`.
The skill is for the generation of script used by a 12 to 18 year old person.
This person has elementary understanding of Bash, PowerShell, Python commands.

I'm instructing a class that involves the Raspberry Pi Pico 2W microcontroller and CircuitPython code.
Each class involves me giving brief lectures and then using my lecture content to create firmware on the microcontroller.
So I plan to incrementally design/build/test a project during the class.
The student will observe/follow my activities on their own microprocessor.

I want to have written script within a Markdown file for:
* my selection of electronic parts and assembling on a breadboard or on the project itself
* a table showing how the discrete components, breakout boards, power source, and microcontroller will be wired
* on a coding blocks that can copied & pasted into the to the development tools (e.g MU editor).
* in the script would be all the actions that needed to be performed by the instructor/students.

So I want to give the students detail script, at every step in the class session,
how copy & paste code into their Mu editor,
and perform the tasks expected in the class session.

This prompt is all about creating documented script for teens to do the required build & test of software.
This became the 1st prompt mainly because it was the clears need that I have to address.
To me, it not the logic place to begin but more of a know problem that required a solution.
I'm like to iteratively improve this prompt and those updates will be added here.

## Do First
When the skill you create starts, it should first do the following:

* Prompt the user for a simple description of this class project
  and the name that will be give to that skill.
* If sources are not provided, ask the user for URLs to preferred sources or directory paths to preferred documents
  that are good sources of installation instructions, but these source do not need to be used exclusively.
* Ask as many questions required to clarify any ambiguity in the task it needs to perform.

## Code Blocks / Snippets
The main purpose of the script is to provide code that the student will load into their editor and upload into the microcontroller.
Instruction should be give on how this is done at the very beginning of the document.
* Layout code blocks / code snippets that will be installed by the instructor / student in chronological order.
  Each block should build upon its predecessor.
* Above each of the code block should be a descriptive paragraph on what the code does.
* The code itself should be very well comment to help instruct the student
* If experiments or measurements are to be performed using what is coded,
  the student should be instructed on what needs to be done.

## Markdown conventions and tooling
Generated documents are GitHub-flavored Markdown. Linting/formatting uses **markdownlint-cli2** with the
repo config `.markdownlint-cli2.jsonc` (not globally installed — run via `npx markdownlint-cli2 "**/*.md"`).
The config is a regular committed file in the repo root (it was previously a symlink into the instructor's
dotfiles `~/.dotfiles/checker-files/`, which is where the canonical copy still lives).
Key non-default rules to honor when editing Markdown by hand:

* Unordered-list indent is **4 spaces** (`ul-indent`), not 2.
* Long lines are allowed (`line-length` = 100).
* Headings: 2 blank lines above, 0 below (`blanks-around-headings`).

All links in generated course documents use **reference-style** form (`[text][01]`) with definitions
collected at the bottom of the file, numbered `[01]`, `[02]`, … with no space before the colon and no
duplicate URLs.
Do not use the URL string to create the `[text]`, but instead, provide a short informative string.

Export to other formats with **pandoc** (installed): `pandoc -f gfm input.md -o output.docx`
(or `-o output.pdf` with a PDF engine).

## Common commands & recurring steps
There is no build or test suite. The relevant commands are:

```bash
npx markdownlint-cli2 "**/*.md"                           # lint all Markdown against .markdownlint-cli2.jsonc
pandoc -f gfm lesson_plans/syllabus.md -o syllabus.docx   # export a doc
```

Note: the linter is **not** clean on the generated docs — it reports pre-existing, tolerated style
warnings (e.g. `MD013` lines over 300, `MD036` emphasis-used-as-heading, `MD060` table-pipe spacing).
Don't assume your edit caused these or chase a zero-warning result; just confirm you didn't add *new* ones.

## Code Creation
Start a separate agent that will be responsible for the creation of all the code in the class project.
This is an expert in CircuitPython and will make sure all the blocks of code work together.

## Validation Step
Start a separate agent that will be responsible for testing of the code created.
This is an expert in CircuitPython and will make sure all the blocks of code re test to assure the meet the project objectives.

## Final Step
* At the concussion, the main agent will summarize any of the validation failures and the corrective action taken.
* Write the script into a file with the name provided by the user.

----

