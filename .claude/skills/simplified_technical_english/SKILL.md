---
name: simplified_technical_english
description: Write or rewrite technical documents in ASD-STE100 Simplified Technical English (STE) for a 12-18 year old reader. Two modes - (1) transform an existing document into STE, (2) compose a new document in STE from the start. Includes a step-by-step workflow, bad/good STE examples, a heuristic checker script, and a verification checklist that is applied repeatedly (maximum 3 passes) until it passes. Use this skill whenever the user types /simplified_technical_english or /ste, asks for "Simplified Technical English", "STE", "ASD-STE100", "controlled language", or asks to make a technical document, procedure, install guide, lesson script, or code comments simpler, clearer, or easier for students or non-native English readers to follow.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
license: MIT
metadata:
  author: Jeff Irland (Makersmiths)
  version: "0.0.1"
  alias: ste
---

# Simplified Technical English (ASD-STE100)
STE is a controlled language. It uses a small set of approved words, each with one meaning, and a set of writing rules (short sentences, active voice, one instruction per sentence).
The result is text that a young reader or a non-native English reader understands the first time they read it, with less chance of a wrong action.

This skill gives you:

* The workflow for **Mode A - Transform** (rewrite an existing document into STE).
* The workflow for **Mode B - Compose** (write a new document in STE).
* `references/ste-rules.md` - a summary of the STE writing rules and common word substitutions. Read it before you write.
* `references/ste-examples.md` - bad and good STE examples, including code comments and text diagrams. Read it before you write.
* `scripts/ste_check.py` - a heuristic checker. It finds long sentences, passive voice, `-ing` words, unapproved words, long paragraphs, and similar problems.
* The **Verification Checklist** (below) - apply it in a loop, maximum 3 passes.

The official specification and dictionary are free on request from the [ASD-STE100 website][01].
The rules file in this skill is a working summary, not the full specification. If a word choice is not clear, choose the shortest, most common word that has only one meaning.


## Target Reader
Write every STE document for this reader:

* Age 12 to 18.
* Elementary knowledge of Bash, PowerShell, Python, and CircuitPython.
* Elementary knowledge of Linux, Windows 11, and macOS.
* Possibly a non-native English reader.

This reader has consequences for the text:

* **Code blocks must have good comments.** Each important line or group of lines gets a comment that tells *what* the line does and *why*. Write the comments in STE too (short, active, one idea per comment).
* **Use text diagrams for complex topics.** A signal path, a wiring connection, a state machine, a folder tree, or a data flow is easier to see than to read. Put the diagram in a fenced code block (` ```text `) and tell the reader in one sentence what the diagram shows. Use plain ASCII box-and-arrow characters so the diagram looks correct in every terminal and editor.
* **Define each technical term the first time you use it.** Use one sentence. After that, always use the same term for the same thing.


## Choose the Mode
* The user gives a file or pasted text and asks to "convert", "rewrite", "make STE", "simplify" → **Mode A - Transform**.
* The user asks for a new document (guide, procedure, explanation, lesson section) and asks for STE, or another skill in this repo calls for STE → **Mode B - Compose**.
* If another generator skill (for example `teen-install-instructions`, `explainer`, `lesson_plan_generator`) makes the document, let that skill control the *structure*. Use this skill to control the *language*.


## Mode A - Transform an Existing Document
Mode A edits the source file in place. Do not make a separate `-ste.md` copy.

1. **Make a backup of the source before you change it.** Do this before all other steps:

    ```bash
    cp -f <file> <file>.bak   # overwrites an older .bak, if one exists
    ```

    The `.bak` file is the only copy of the original text. If the backup fails, stop and tell the user.
2. **Read the full source.** Identify the document type and the sections. Mark each section as one of these:
    * *Procedural* - steps the reader does (maximum 20 words per sentence).
    * *Descriptive* - information the reader learns (maximum 25 words per sentence).
    * *Safety* - warnings and cautions.
3. **Mark what you must not change.** Do not change code statements, commands, file paths, URLs, pin names, part numbers, values with units, or quoted error messages. Do not change link definitions. You can change code *comments*.
4. **Make a term list.** Find each thing that the source names in more than one way (for example "board", "Pico", "microcontroller", "the device"). Choose one term for each thing. Use only that term in the output. Technical names (for example `Raspberry Pi Pico 2 W`, `GPIO`, `CircuitPython`, `HC-SR04`) are permitted in STE.
5. **Run the checker on the source** to see the size of the job:

    ```bash
    python3 .claude/skills/simplified_technical_english/scripts/ste_check.py <source.md>
    ```

6. **Rewrite section by section.** Apply the rules in `references/ste-rules.md`:
    * Procedures: imperative verbs, one instruction per sentence, condition first ("If the LED does not come on, ..."), numbered steps.
    * Descriptions: the most important information first, one topic per sentence, maximum 6 sentences per paragraph.
    * Safety: start with a command ("Do not touch ..."), then give the risk.
    * Replace unapproved words. Break long sentences. Change passive voice to active voice. Remove `-ing` forms.
7. **Rewrite the code comments in STE.** Add comments where the code has none. Do not change the code itself.
8. **Add text diagrams** where a paragraph explains connections, flow, order, or structure.
9. **Do the Verification Loop** (below).
10. **Write the output.**
    * Write the STE text to the source file (in place). The backup from step 1 keeps the original.
    * If the user gives a different output path, write there. Make a backup first if that file exists.
    * Keep the repo Markdown conventions (reference-style links `[text][01]` with definitions at the bottom, 2-space indent for bullets under bullets, 2 blank lines above headings).
11. **Report** to the user: the output path, the backup path, the number of verification passes, and any item that still fails (with the reason).


## Mode B - Compose a New Document
1. **Get the purpose and the reader task.** Write one sentence: "After this document, the reader can ___." If the purpose is not clear, ask the user.
2. **Make the outline.** Mark each section as procedural, descriptive, or safety. Put prerequisites and safety before the first step.
3. **Make the term list** before you write, so that you use one term for each thing from the start.
4. **Write in STE from the first draft.** Use `references/ste-rules.md` and the patterns in `references/ste-examples.md`. Short sentences are easier to write correctly than to fix later.
5. **Write code with STE comments.** Apply the `python_code` skill style for Python and CircuitPython. Every important line gets a comment.
6. **Add text diagrams** for each complex topic.
7. **Do the Verification Loop** (below).
8. **Write the output** to the path the user gives, or ask for a path. Report as in Mode A step 11.


## Verification Loop
Apply the checklist to the full document. Maximum 3 passes.

```text
   +-------------------+
   |  Draft (pass = 1) |
   +---------+---------+
             |
             v
   +-------------------+      all items pass      +--------+
   | Run ste_check.py  +------------------------->|  Done  |
   | + manual checklist|                          +--------+
   +---------+---------+                               ^
             | one or more items fail                  |
             v                                         |
   +-------------------+         pass < 3              |
   | Fix each failure  +---> pass = pass + 1 --> (check again)
   +---------+---------+                               |
             | pass = 3 and items still fail           |
             v                                         |
   +-------------------------------+                   |
   | Stop. Report each item that   +-------------------+
   | still fails and why.          |
   +-------------------------------+
```

In each pass:

1. Run the checker. Exit code 0 means no errors (warnings can remain).

    ```bash
    python3 .claude/skills/simplified_technical_english/scripts/ste_check.py <output.md>
    ```

2. Read the document yourself against the manual items in the checklist. The script is a heuristic: it does not understand meaning. It can flag a correct sentence (for example a technical name that ends in `-ing`). If a flag is a false positive, write it down and continue.
3. Fix each failure. Then start the next pass.

After 3 passes, stop, even if items still fail. Tell the user which items fail and why (for example: "Sentence at line 42 has 23 words. A shorter version loses the meaning of the command.").


## Verification Checklist
**Script items** (from `ste_check.py`):

* [ ] Procedural sentences have 20 words or fewer.
* [ ] Descriptive sentences have 25 words or fewer.
* [ ] Paragraphs have 6 sentences or fewer.
* [ ] No passive voice in procedures. Minimum passive voice in descriptions.
* [ ] No `-ing` verb forms (technical names are permitted).
* [ ] No words from the unapproved-word list.
* [ ] No contractions (`don't`, `it's`) and no semicolons.

**Manual items** (you check these):

* [ ] Each sentence has one topic. Each procedural sentence has one instruction (or two actions done at the same time).
* [ ] Instructions use the imperative ("Connect the wire."), not "You should connect the wire."
* [ ] Conditions come before the instruction ("If the LED is off, push the button.").
* [ ] Each word has one meaning in the document. The same thing always has the same name (term list).
* [ ] No noun clusters of more than 3 words (write "the speed of the left motor", not "left motor speed sensor value").
* [ ] Articles (`the`, `a`, `an`) are not removed to make sentences shorter.
* [ ] Each warning or caution starts with a command and then gives the risk.
* [ ] Each technical term has a one-sentence definition at its first use.
* [ ] Each code block has comments in STE that tell what and why. The code itself did not change (Mode A, compare with the `.bak` file).
* [ ] Each complex topic (wiring, flow, states, structure) has a text diagram with a one-sentence introduction.
* [ ] Commands, paths, URLs, values, and part numbers are the same as in the source (Mode A). Compare with the `.bak` file.
* [ ] The `<file>.bak` backup exists and has the original text (Mode A).
* [ ] Repo Markdown conventions are kept (reference-style links, 2-space indent for bullets under bullets).



[01]:https://www.asd-ste100.org/
