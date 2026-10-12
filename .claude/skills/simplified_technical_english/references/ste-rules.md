# STE Writing Rules - Working Summary
This file is a working summary of the ASD-STE100 writing rules, adapted for course documents for a 12-18 year old reader.
It is not the official specification. The official specification and dictionary are free on request from the ASD-STE100 website.

Contents:

1. Words
2. Noun clusters
3. Verbs
4. Sentences
5. Procedures
6. Descriptive writing
7. Safety instructions
8. Punctuation
9. Code, commands, and diagrams (course additions)
10. Common word substitutions


## 1. Words
* Use approved words only with their approved meaning and part of speech. Example: `close` is a verb ("close the file"), not an adjective meaning "near" - use `near`.
* Technical names are permitted: part names, software names, file names, pin names, units (`Raspberry Pi Pico 2 W`, `CircuitPython`, `GP15`, `code.py`, `5 V`).
* Technical verbs are permitted when they name a specific technical action and no approved word has the same meaning (for example `solder`, `compile`, `download`, `install`, `flash`, `reboot`, `click`). Do not use a technical verb when a simple approved verb works.
* Use one word for one thing. If you call it "the board" in step 1, do not call it "the Pico" in step 2 and "the device" in step 3.
* Use American English spelling (the course uses it).
* Do not use slang, idioms, or jokes that need cultural knowledge ("piece of cake", "hit the ground running").


## 2. Noun Clusters
* Do not use more than 3 nouns in a row.
* Bad: `motor driver PWM frequency setting`. Good: `the PWM frequency of the motor driver`.
* If a long cluster is the official technical name, define it once, then use a shorter term or the abbreviation.


## 3. Verbs
* Use these verb forms: imperative, simple present, simple past, simple future, infinitive, and the past participle as an adjective ("the connected wire").
* Do not use `-ing` forms as verbs ("The motor is turning" → "The motor turns"). An `-ing` word that is a technical name is permitted (`string`, `wiring diagram`, `debouncing` when it is the defined name of the technique).
* Use active voice in procedures. Use active voice in descriptions as much as possible.
  * Passive: "The servo is moved by the code." Active: "The code moves the servo."
* Use an action verb, not a noun made from a verb. "Do an installation of" → "install". "Make an adjustment to" → "adjust".
* Do not use modal verbs that are not clear. "You should" → imperative ("Do X"). "You might want to" → "If ___, do X."


## 4. Sentences
* One topic per sentence.
* Procedural sentence: maximum 20 words. Descriptive sentence: maximum 25 words.
* Do not remove words (articles, "that", verbs) to make a sentence shorter. "Connect wire to pin" → "Connect the wire to the pin."
* Use vertical lists for complex text. Put a colon at the end of the text before the list.
* Use connecting words (`then`, `after`, `because`, `but`, `if`, `when`) to show how sentences are related.


## 5. Procedures
* Write each instruction as a command (imperative).
* One instruction per sentence. Two actions in one sentence only when the reader does them at the same time ("Push and hold the BOOTSEL button.").
* Put a condition first: "If the drive does not show, disconnect the cable."
* Number the steps. Each number is one step.
* Use a note for information that is not an instruction. Do not put an instruction in a note.
* Tell the reader the result to expect after an important step ("The LED flashes 3 times.").


## 6. Descriptive Writing
* Put the most important information first.
* One topic per paragraph. Maximum 6 sentences per paragraph.
* Give the reader the context first, then the detail.
* Use a text diagram or a table when the text compares items, shows a sequence, or shows a structure.


## 7. Safety Instructions
* Use `WARNING` for a risk of injury. Use `CAUTION` for a risk of damage to equipment.
* Start with a clear command. Then give the risk in a short sentence.
  * "WARNING: Disconnect the battery before you change the wiring. A short circuit can make the wires hot."
* Put the warning or caution before the step it applies to, not after.


## 8. Punctuation
* Do not use semicolons. Make two sentences.
* Do not use contractions (`don't` → `do not`, `it's` → `it is`).
* Use a colon before a vertical list.
* Use parentheses only for short references, units, or abbreviations, not for extra sentences.
* Use the same symbol for a range each time ("3.3 V to 5 V").


## 9. Code, Commands, and Diagrams (Course Additions)
These rules are not part of ASD-STE100. They apply the STE goals to the course reader.

* Do not change code, commands, paths, or output text. They are technical names.
* Write code comments in STE: short, active, imperative or simple present, one idea per comment.
  * Bad: `# Here we're basically checking to make sure the button isn't being pressed`
  * Good: `# Read the button. True means the button is released (pull-up).`
* Put a comment above each block of code that tells what the block does. Put an end-of-line comment where a value or a line is not obvious (pin numbers, magic numbers, units).
* Tell the reader which shell to use before each command block (Bash, PowerShell, or the CircuitPython REPL).
* Use a text diagram for wiring, signal flow, data flow, state machines, timing, and folder trees. Introduce each diagram with one sentence. Use only plain ASCII characters (`+ - | > v < ^`) so that the diagram aligns in every font.


## 10. Common Word Substitutions
Use the word on the right. The official dictionary has more entries. If a word is not on this list and is not a technical name, use the shortest common word that has one meaning.

| Do not use | Use |
| --- | --- |
| utilize, utilise, employ | use |
| perform, execute (an action) | do |
| ensure, verify, confirm | make sure, check |
| commence, initiate | start |
| terminate | stop, end |
| obtain, acquire | get |
| require | need |
| assist | help |
| attempt | try |
| prior to | before |
| subsequent to, following | after |
| in order to | to |
| due to | because of |
| approximately (non-numeric use), roughly | about |
| numerous, a lot of | many |
| sufficient | enough |
| additional | more |
| adjacent to | near, next to |
| locate | find |
| modify | change |
| indicate | show |
| demonstrate | show |
| determine | find, calculate |
| facilitate | help, make possible |
| basically, simply, just, actually, really | (delete) |
| easy, obvious, of course | (delete - it is not easy for every reader) |
| should | must (requirement) or imperative (instruction) |
| might, could possibly | can, may (possibility) |
| it's, don't, can't, won't | it is, do not, cannot, will not |
