
---

# My Claude Code Methodology
I want to develop physical computing solutions, specifically focused on robotics.
I'm doing this for a currently imaginary entity I'll call the "Autonomous Robot Workshop", abbreviated as ARW.
ARW is a place where young and old will learn about the creation of wheeled base robotics.

I have two distinct development methodologies when using Claude Code:

| Methodology | When Used | Description |
|:-----------:|:---------:|-------------|
| Spec-Kit Methodology | Softwre Development | This [Spec-Driven Development or SDD][A1] process ([developed by GitHub][A2]) is an intent-driven software development process where precise, structured Markdown specifications are created, refined, and validated before writing code. Instead of ad-hoc prompt engineering or passive documentation, specifications act as executable contracts (my-vision, PRD, system specification, etc.) that guide AI coding agents step by step. |
| Script Methodology | Teaching | Like Spec-Kit, key documents (my-vision, BOM, course syllabus, class lesson plan, etc.) act as executable contracts, but the end goal is different.  Here the focus isn't on developing a software system, but instead developing course material, that could also include code or detail procesures, for teaching a subject matter. |

[A1]:https://heeki.medium.com/using-spec-driven-development-with-claude-code-4a1ebe5d9f29
[A2]:https://github.github.com/spec-kit/

## My Spec-Kit Based Workflow

* [Spec-Driven Development in Action with GitHub Speckit](https://pub.towardsai.net/spec-driven-development-in-action-with-github-speckit-44190f2a7c57)
* [Specification Engineering: The New Skill After Prompt Engineering](https://www.kdnuggets.com/specification-engineering-the-new-skill-after-prompt-engineering)
* [GitHub Spec Kit Tutorials](https://www.youtube.com/playlist?list=PL4cUxeGkcC9h9RbDpG8ZModUzwy45tLjb)
* [The ONLY guide you'll need for GitHub Spec Kit](https://www.youtube.com/playlist?list=PLncUKimFWV_Nq4HMVWwvlIRX1Dbkg-PZS)
* [GitHub: github/spec-kit](https://github.com/github/spec-kit)
* [GitHub Spec Kit](https://github.github.com/spec-kit/)

[Spec-Kit: Quick Start Guide](https://github.github.com/spec-kit/quickstart.html)

Quick Start Guide

```text
/speckit.constitution -> /speckit.specify -> /speckit.clarify -> /speckit.checklist -> /speckit.plan -> /speckit.tasks -> /speckit.analyze -> /speckit.implement

/prd-generator my-vision.md

/speckit-constitution  --->  /speckit-specify  --->  /speckit-plan --->  /speckit-tasks  --->  /speckit-implement
                                         \                ^                       \                  ^
                                          v              /                         v                /
                                          /speckit-clarify                         /speckit-analyze
```

This guide will help you get started with Spec-Driven Development using Spec Kit.


## My Claude Code Workflow
Following the official Spec Kit documentation, [Spec-Kit: Quick Start Guide](https://github.github.com/spec-kit/quickstart.html).

#### Installation of Your Tools & Project Folder

##### Step 1: Install Specify -- DONE
In your terminal, run the `specify` CLI command to initialize your project:

```bash
# Create a new project directory
uvx --from git+https://github.com/github/spec-kit.git specify init <PATH_TO_PROJECT_NAME>

# OR initialize in the current directory
uvx --from git+https://github.com/github/spec-kit.git specify init .
```

>**NOTE:** You can also install the CLI persistently on your computer with `pipx`.
>I prefer not to do this. See [Sparc Kit: Quick Start](https://github.github.com/spec-kit/quickstart.html#step-1-install-specify).

##### Step 2: Install SKILL.md Files -- DONE
I have several Claude Code `SKILL.md` files that I use regularly.
I include them in this project via this command:

```bash
# install skill files <-- still not working right
cd ~/.dotfiles/pkg-claude/local/skills
cp -a python_skills/* questioning_skills/* sdlc_skills/* <PATH_TO_PROJECT_NAME>/.claude/skills
cp -a README.md <PATH_TO_PROJECT_NAME>/.claude/skills
```

#### Start Your Custom Workflow Process
I have customized the Spec-Kit workflow to include some additional documents that I find necessary.

##### Step 3: Create the `my-vision.md` Document -- DONE
The first of these document is the `my-vision.md` document, which I personally author without Claude.
Its my description of the solution I'm looking to create.
The goal is to describe what I expect but leaving all design details for Claude to specify via the workflow.
This document is the "spark" that ignites the detail specification process.

Below is a real example of a `my-vision.md` file.
Create a `my-vision.md` file using this documents structure:

```markdown
# My Vision
This document capture my current thinking of the software/hardware system I wish to create,
which I'm calling "claudewatch".
This document should be used to create the key documents that initiates my development workflow,
that is, the product requirements document (`PRD.md`).

## Example Implementations
The websites below are examples of what I want to create.

* [ClaudeMeter](https://eddmann.com/ClaudeMeter/)
  * [GitHub: eddmann/ClaudeMeter](https://github.com/eddmann/ClaudeMeter)
* [Clawdmeter](https://osrtos.com/projects/clawdmeter/)
  * [GitHub: HermannBjorgvin/Clawdmeter](https://github.com/HermannBjorgvin/Clawdmeter)

Build me something similar to ClaudeMeter & Clawdmeter.

## Key Features to be Built
These are the key features I expect the solution to have:
  * Auto-refresh -
    Automatic usage updates every 1, 5, or 10 minutes. Set it and forget it - your usage data is always up to date.
  * Menu Bar Indicator -
    Color-coded gauge icon in your menu bar. Green for safe, yellow for warning, red for critical - see your status at a glance.
  * Smart Notifications -
    Configurable warning and critical thresholds. Get notified before you hit your limits, not after.
  * Real-time Monitoring -
    Track your 5-hour session limits, 7-day weekly usage, and model-specific limits in real-time.
    Never get caught off guard by hitting your limits.
  * Animated Claude Mascot -
    An ASCII art mascot, resembling `ClaudeMeter_Mascot.jpeg`, becomes more excited or “busy” on the display
    and changes colors as the number of tokens are consumed

## Core Principles
These items are very important and should be placed in the `constitution.md` file:
  * Solution should run in a small terminal window, using color ASCII characters, and Claude mascot must be animated
  * I strongly prefer the look & feel of [GitHub: HermannBjorgvin/Clawdmeter](https://github.com/HermannBjorgvin/Clawdmeter)
  * The solutions default look & feel (colors, sizes, fonts, etc.) & behavior (thresholds, animation speed, etc.)
    should be configurable via a YAML configuration file
  * The solution must proactively give its warnings so the user has time to take action
  * The solution must be information rich for the user but nicely formatted & visually appealing
  * If the solution fails or errors, the solution must write a clear description and likely root cause of the failure/error.

## Core Software Components
These items are very important and should be placed in the `constitution.md` file:
  * All coding should be in Python, and when needed, Bash

## Core Hardware Components
These items are very important and should be placed in the `constitution.md` file:
  * The is no special hardware components for this solution.  Everything should run in a Linux terminal session.

## How to Use `my-vision.md`
Using the file `my-vision.md` file,
create for me a product requirements document (PRD) call PRD.md using the skills `/prd-generator`.
Also use the skill `/grill-me` to ask me any clarifying questions concerning the PRD.
```

##### Step 4: Create the Production Requirements Document (PRD) -- DONE
Next, we need to create the `PRD.md` file.
It can be create using this prompt within Claude Code:

```text
Using the @my-vision.md file,
create for me a product requirements document (PRD), called @PRD.md, using the skill /prd-generator.
Also use the skill /grill-me to ask me any required clarifying questions concerning the PRD.
```

##### Step 5: Create the Project's Constitution Document and CLAUDE.md -- DONE
Now we will use the Spec-Kit process to create the projects `constitution.md` file.
You can use the `/speckit.constitution` slash command to establish the core rules and principles for your project.
You should provide your project's specific principles as arguments,
or as I do, reference other documents that you have created:

```text
Using the skill /speckit.constitution and the files @my-vision.md & @PRD.md, create the the projects constitution.md file.
```

Following this, you can update the `CLAUDE.md` file.
The `CLAUDE.md` file will be used for additional context about technologies to be used, project structure,
shell commands, and other important information:

```text
Now create the `CLAUDE.md` file
```

##### Step 6: Create the Project's Specification Document -- DONE
I use the `/speckit.specify` slash command to describe what you want to build.
The focus should be on the **what & why** (the feature spec for implementation), not the tech stack,
this is exactly what the `PRD.md` can help with

```test
Using the /speckit.specify skill, read the @PRD.md document
```

A good specification usually includes:
1. **Objective**: What should the model achieve?
1. **Context**: What does the model need to know?
1. **Inputs**: What data, files, tools, or assumptions are allowed?
1. **Output Format**: What should the final answer look like?
1. **Constraints**: What should the model avoid?
1. **Evaluation Criteria**: How will we judge correctness?
1. **Edge Cases**: What could go wrong?
1. **Verification Steps**: What tests or checks must pass?

##### Step 7: Refine and Validate Specification Document -- DONE
Use the `/speckit.clarify` slash command to identify and resolve ambiguities in your specification.
If you did an excellent job on the previous steps,
use of `/speckit.clarify` may not be necessary.

In any event, you can provide specific focus areas as arguments.
Identify underspecified areas in the current feature spec by asking up to 5 highly targeted clarification questions
and provide answers back into the spec.

Here are some standard areas worthy of additional analysis:

```text
/speckit.clarify Focus on security, performance, and extensibility requirements.
```

Then validate the requirements with `/speckit.checklist` before creating the technical plan:

```text
/speckit.checklist
```

Then have Claude walk-through the checklist it created and you provide clarifying answers to the issues identified.

##### Step 8: Create a Technical Implementation Plan -- DONE
use the `/speckit.plan` slash command to provide your technology stack and architecture choices.

```text
/speckit-plan
```

##### Step 9: Create the Project's Tasks Document and Analysis -- DONE
Generate an actionable, dependency-ordered `tasks.md` file listing feature based on identified design artifacts.

```text
/speckit-tasks
```

After the `task.md` file is generated,
perform a non-destructive cross-artifact consistency & quality analysis
across `spec.md`, `plan.md`, and `tasks.md`.

```text
/speckit-analyze
```

Then remediate all the issues identified by `/speckit-analyze`:

```text
Remediate all the issues identified by asking me clarifing questions and make recommendations.
```

##### Step 10: Create the Project's Implementation Document
Execute the implementation plan by processing and executing all tasks defined in `tasks.md`, across all the phases.

>**NOTE:** For complex projects, implement in phases to avoid overwhelming the agent's context.
>Start with core functionality, validate it works, then add features incrementally.

```text
/speckit-implement do implementation of Phase 1 tasks
```

 All phases complete. The tool is ready for live credential validation whenever you're ready for T036.



/speckit-git-commit               Auto-commit changes after a Spec Kit command completes (project)
/speckit-git-feature              Create a feature branch with sequential or timestamp numbering (project)
/speckit-git-initialize           Initialize a Git repository with an initial commit (project)
/speckit-agent-context-update     Refresh the managed Spec Kit section in the coding agent context file (project)
/speckit-checklist                Generate a custom checklist for the current feature based on user requirements. (project)
/speckit-git-remote               Detect Git remote URL for GitHub integration (project)
/speckit-git-validate             Validate current branch follows feature branch naming conventions (project)



---

