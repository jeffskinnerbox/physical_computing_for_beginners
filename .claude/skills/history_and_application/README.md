# History and Application Generator

A Claude Code skill that generates history and application documents for technologies,
software programs, machines, electronic circuits, or systems relevant to the autonomous
robot workshop.

## What It Produces

A single markdown document with two major sections:

1. **History** — Where did this technology come from?
   - Brief narrative (0.25-0.5 pages): storytelling format covering origins, key people, evolution
   - Detailed timeline: 10-25 bulleted chronological entries with names, dates, milestones

2. **Application** — Where has this technology been used?
   - Brief narrative (0.25-0.5 pages): storytelling format covering practical deployments
   - Detailed timeline: 10-25 bulleted chronological entries with industries, uses, impacts

## How to Invoke

Ask Claude to generate a history and application document for a topic:

- "Generate a history and application document for PID control"
- "What's the history and application of infrared sensors?"
- "Create a history-and-application for line-following robots"

## Output

Markdown file saved as `history-and-application-<topic>.md` in the project root.

## See Also

- `SKILL.md` — Full skill definition with instructions, examples, and rules



Skill structure — each generated document will contain:

  1. History Section
    - Brief narrative (0.25-0.5 pages) — storytelling format covering origins, key people, evolution over ~200 years to
  present
    - Detailed timeline — 10-25 bulleted chronological entries with names, dates, and significance
  2. Application Section
    - Brief narrative (0.25-0.5 pages) — same storytelling style covering practical deployments
    - Detailed timeline — 10-25 bulleted entries covering industries, uses, and impacts

  Key design choices modeled after the existing theory-of-operation skill:
- Same YAML frontmatter pattern and allowed-tools set
- Same reference-style link management rules
- Same [VERIFY] convention for uncertain details
- Same audience targeting (high school students, accessible language)
- Output files named history-and-application-<topic>.md
- Optional sections for Key Figures table, Evolution Diagram, and Connection to This Workshop

  You can invoke it with prompts like: "Generate a history and application document for PID control" or "What's the
  history and application of infrared sensors?"


Prompt to generate this skill:

Using the skill-generator skill, create for me the history-and-application skill for this project folder.
The history-and-application skill's topic will concern a technology, software program, machine, electronic circuit, or system.
There should be two major section to the document created with the skill: topic history and topic application.
Within history sections, give a  brief narrative (0.25 to 0.5 pages) on the topics history
(time frame, people involve with its creation, how it evolved over time)
starting about two hundred years ago (if needed) to the present.
Also include a more detailed, longer write-up, in a bulleted timeline format.
For the application section, use the same style but cover how/where the topic was put to use.
