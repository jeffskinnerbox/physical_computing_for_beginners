
Created .claude/skills/theory-of-operation/SKILL.md. Here's what the skill does:

  Two required output sections:
  1. Brief Overview — 1-2 paragraphs (80-200 words) giving a self-contained mental model of how the system works. Covers
   purpose, core principle, inputs/outputs, and major stages.
  2. Detailed Step-by-Step Decomposition — 4-10 ordered steps, each with a short title (3-8 words) and a thorough
  description covering trigger, process, components involved, result, and transition to the next step.

  Key design decisions:
- Domain-agnostic — works for electronics, software, mechanical, chemical, or hybrid systems
- Steps follow the operational sequence (what happens when it runs), not the build or teaching order
- Grounded in external sources: Wikipedia's definition, JANA Corp's documentation guidance, MIL-STD-40051 structure,
  and EEVblog engineering discussion on the value of Funktionsbeschreibung
- Optional supporting sections: block diagrams, key parameters tables, common misconceptions
- Follows existing project conventions: YAML frontmatter, reference-style links, [VERIFY] flags, pandoc export

  Sources:
- Theory of operation - Wikipedia
- JANA Corp - Theory of Operations Document Services
- EEVblog Forum - Why "Theory of Operation"?
- MIL-STD-40051 - Technical Manuals including Theory of Operation
- Wikibooks - General Engineering Introduction/Theory of Operation

