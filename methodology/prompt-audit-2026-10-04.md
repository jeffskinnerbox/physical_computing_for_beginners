# Prompt Audit — Claude Code Configuration (2026-10-04)

Audit of the Claude Code instruction files that load into sessions in this repo, checked for dated
prompting patterns, stale facts, and files that contradict each other. Run with
`/claude-api prompt-audit`. Edits are **proposed only** — nothing was applied.


## Assumptions

- **Target model:** Claude Opus 5.5 (the model that ran the audit). No skill pins its own model.
- **Scope (audited, edits proposed):** project `CLAUDE.md`; the 14 skills in `.claude/skills/`
    (with their `agents/` and `references/` files); `~/.claude/CLAUDE.md`.
- **Scope (report only, no edits):** the 4 installed plugins (superpowers, code-simplifier,
    context7, skill-creator) and the Anthropic-synced skills under `~/.claude/skills/synced/`.
- **Not present:** `CLAUDE.local.md`, `AGENTS.md`, `.claude/CLAUDE.md`, a managed-policy
    `CLAUDE.md`, and any rules/commands/agents/output-styles folders under either `.claude/`.
- **Not read (can hold secrets):** settings files, `.mcp.json`, `~/.claude.json`.


## Summary

The biggest problems are broken facts, not dated wording:

- Six skills tell Claude to read `.claude/skills/shared/definitions.md`, which doesn't exist and
    never did in git history.
- The `python_code` skill's description is cut off, so it only partly loads. Claude Code shows it
    as "…use this skill when users".
- `html_slide_deck` saves its defaults to a different path than the one it reads them from, so a
    saved default is never used.
- Seven generator skills end in an all-caps "Critical Rules" list. The rules themselves are real,
    but the shouting makes current models apply them too rigidly.

Counts:

| Group | Result |
| --- | --- |
| 1 — Dated prompt text | 2 findings |
| 2 — Brittle config and stale facts | 7 findings, 8 flags |
| 3 — Tool descriptions | not applicable |
| 4 — Request config | not applicable; subagent roster check found nothing |
| `~/.claude/CLAUDE.md` | clean |


## Findings

Ordered by confidence, highest first.

| # | Location | Evidence | Pattern | Why it's a problem | Conf. | Action |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `lesson_plan_generator`, `syllabus_generator`, `theory_of_operation` SKILL.md:18-19; `bill_of_materials_generator`, `history_and_application` :19-20; `explainer` :14-15 | "read `.claude/skills/shared/definitions.md`" | G2 volatile specifics | The file doesn't exist and never did in git history, so every run starts with a failed read. | High | remove (or create the file, if you meant to) |
| 2 | `python_code/SKILL.md:3-4` | the continuation line `request Python code…` starts at column 0 | G2 stale fact | The YAML breaks, so the description loads truncated and loses its trigger. `CLAUDE.md` relies on this skill for every CircuitPython snippet. | High | rewrite as a single line |
| 3 | `html_slide_deck/SKILL.md:123` vs `:23` | saves to `.claude/html-slide-deck.defaults.json`, but reads `.claude/skills/html_slide_deck/assets/…` | G2 internal conflict | A saved default is never found. Both lines come from the same commit; the assets path is the one that exists. | High | rewrite the save path |
| 4 | `syllabus_generator/SKILL.md:73` | "Check for a bill of materials — Use accurate costs and sourcing info." | G2 conflict | Contradicts lines 37, 166 and 292 of the same file: no prices in the syllabus. | High | rewrite |
| 5 | `teen-install-instructions/SKILL.md:12,105,113,119,134,56-57` | "Task tool", `web_fetch`, `web_search` | G2 volatile specifics | Claude Code's subagent tool is now `Agent`, as the repo's own `readme_generator` frontmatter already says. The web tools are `WebFetch` and `WebSearch`. | Medium | rewrite |
| 6 | `CLAUDE.md:135-165` ("Other directories") | `full_build/` isn't mentioned | Re-baselining (add) | Commits 75d8d71 and b667458 added `full_build/` with a lesson-script copy-sync rule. Nothing in `CLAUDE.md` tells Claude about it. | Medium | add a paragraph |
| 7 | "Critical Rules" in lesson_plan :365, syllabus :286, BOM :329, theory :397, history :428, explainer :138, readme_generator :229; also inline "**Critical rule:**", "must NOT", "MUST align" | runs of **NEVER** / **ALWAYS** | G1a pressure language | Current models over-apply all-caps rules. The constraints are real and already stated with reasons in each skill's body. | Medium | rewrite at normal volume; keep every rule |
| 8 | `explainer/SKILL.md:17,25,128` | "Think Hard"; "Take time to think through these options" | G1b prose steering thinking | On Opus 5.5 thinking is always on and effort controls depth. The real instruction is to pick a structure, so that part stays. | Medium | rewrite |
| 9 | `wiring_diagram/SKILL.md:72` | "Pitfalls (hit and fixed while building the first one of these)" | G2 history narrative | The heading carries backstory; the pitfalls under it are what matters. | Medium | rewrite the heading |


## Flags (no edit proposed)

| # | Location | Issue |
| --- | --- | --- |
| F1 | `CLAUDE.md:145-162` (`src/` section) | The working tree has uncommitted deletions of all of `src/`, but `CLAUDE.md`, `full_build/README.md`, `lesson_scripts/README.md` and `tech_setup_check/install-wireframe-on-windows-11.md` still point to `src/wireframe/`. **To decide:** is the deletion intended? If yes, rewrite this section and those docs. If not, restore `src/`. |
| F2 | `workbench_voice/SKILL.md:40` vs `:44-46, :78-87` | The skill says both "prose is the default; save lists" and "use bullet points". It also says "vary sentence length" and "keep sentences short", and bans em dashes while using 10 itself. All from one commit (9ce8fe2), so history can't say which is current. **To decide:** which style wins. |
| F3 | project `teen-install-instructions` vs synced `anthropic-skills:teen-install-instructions` | Same descriptions, so routing between them is ambiguous. Project `readme_generator` and synced `readme-generator` also overlap. The fix would be outside the project: disable the synced copies. |
| F4 | `wiring_diagram/SKILL.md:18,96-98` | It relies on a `/design` skill and `seed-canvas.mjs` that aren't in this repo or the session's skill list. Lines 96-98 are garbled: a list bullet splits a parenthetical. Low confidence. |
| F5 | syllabus :29, :70, :222-231, :258-283; lesson_plan :29, :235-245, :320-362; explainer :166-175 | Examples come from a line-follower course (MiOYOOW, TCRT5000, QTR, "Design Session"). This risks over-indexing on the wrong project. Low confidence. |
| F6 | `explainer/SKILL.md:95-114` | The audience tiers are C-suite, BI analysts and data scientists. This course's audience is teens. The fallback ("assume lowest level") covers it. Low confidence. |
| F7 | `python_code/SKILL.md:780-833` | Empty stub headings, raw inline URLs, and a reference to a `LICENSE.txt` that doesn't exist. Some advice (`itertools`, `bisect`, `__slots__`) doesn't fit CircuitPython, which `CLAUDE.md` applies this skill to. Low confidence. |
| F8 | plugin `superpowers/using-superpowers` (report only) | `<EXTREMELY-IMPORTANT>… 1% chance… ABSOLUTELY MUST invoke` is G1a booster text. Its skills aren't in the session's roster, so it's probably disabled. `code-simplifier` pins `model: opus`, which is fine. |


## How to Apply

Findings 1–6 fix wrong facts, so confirm the direction before applying them. In particular,
finding 1 assumes `definitions.md` was never planned; if it was, create the file instead.

The diff below has 28 hunks, one per finding per file, so you can take them selectively. It was
checked with `git apply --check` against the working tree on 2026-10-04. To apply it all, save
the diff block to a file and run `git apply -p1 <file>` from the repo root, after making `.bak`
copies of the touched files.


## Proposed Diff

````diff
diff -ru a/.claude/skills/bill_of_materials_generator/SKILL.md b/.claude/skills/bill_of_materials_generator/SKILL.md
--- a/.claude/skills/bill_of_materials_generator/SKILL.md
+++ b/.claude/skills/bill_of_materials_generator/SKILL.md
@@ -16,9 +16,6 @@
 
 The BOM answers: what do we need to buy, how much does it cost, and where do we get it?
 
-## Definitions
-For shared terminology and type definitions across all the skills in `.claude/skills/`, read `.claude/skills/shared/definitions.md`.
-
 ## Relationship to Syllabus and Lesson Plans
 
 The three core course documents have distinct responsibilities:
@@ -29,7 +26,7 @@
 | **Lesson Plan** | Session-level teaching instructions, per-session materials list (names only) | Costs, sourcing, pricing |
 | **Bill of Materials** | All costs, quantities, sourcing, pricing, shipping, per-student totals | Teaching content, schedule |
 
-**Critical rule:** The BOM must be consistent with the syllabus and lesson plans.
+**Rule:** The BOM must be consistent with the syllabus and lesson plans.
 Every component referenced in the syllabus or lesson plans must appear in the BOM.
 Every component in the BOM should be used in at least one session described in the syllabus.
 
@@ -326,16 +323,16 @@
 Shipping Cost = 3*8 / 4 = $6.00 per student (assuming 4 students)
 ```
 
-## Critical Rules
+## Rules
 
-- **NEVER** include cost or pricing information in the syllabus or lesson plans — costs belong exclusively in the BOM
-- **NEVER** omit a component that appears in the syllabus or lesson plans — every referenced item must be in the BOM
-- **ALWAYS** read the syllabus and lesson plans before generating — ensure complete coverage
-- **ALWAYS** include source links for every purchasable hardware item
-- **ALWAYS** show the cost arithmetic so users can verify and adjust for their class size
-- **ALWAYS** separate required from optional items with independent cost subtotals
-- **ALWAYS** include shipping costs — they are real expenses that affect the per-student budget
-- **ALWAYS** use reference-style links (`[text][01]`) with definitions at the bottom of the file — never inline URLs
-- **ALWAYS** preserve URLs from source documents — do not drop links found in syllabus, course docs, or lesson plans
-- **NEVER** duplicate a URL in the reference list — reuse the same `[NN]` number for repeated references
-- **ALWAYS** flag it as "[VERIFY PRICE]", rather than guessing, if a price might be outdated.
+- Never include cost or pricing information in the syllabus or lesson plans — costs belong exclusively in the BOM
+- Never omit a component that appears in the syllabus or lesson plans — every referenced item must be in the BOM
+- Always read the syllabus and lesson plans before generating — ensure complete coverage
+- Always include source links for every purchasable hardware item
+- Always show the cost arithmetic so users can verify and adjust for their class size
+- Always separate required from optional items with independent cost subtotals
+- Always include shipping costs — they are real expenses that affect the per-student budget
+- Always use reference-style links (`[text][01]`) with definitions at the bottom of the file — never inline URLs
+- Always preserve URLs from source documents — do not drop links found in syllabus, course docs, or lesson plans
+- Never duplicate a URL in the reference list — reuse the same `[NN]` number for repeated references
+- Always flag it as "[VERIFY PRICE]", rather than guessing, if a price might be outdated.
diff -ru a/.claude/skills/explainer/SKILL.md b/.claude/skills/explainer/SKILL.md
--- a/.claude/skills/explainer/SKILL.md
+++ b/.claude/skills/explainer/SKILL.md
@@ -11,10 +11,7 @@
 # Explainer
 Transform complex technical concepts into clear, accessible explanations using narrative storytelling frameworks.
 
-## Definitions
-For shared terminology and type definitions across all the skills in `.claude/skills/`, read `.claude/skills/shared/definitions.md`.
-
-## Before Responding: Think Hard
+## Before Responding: Choose a Structure
 Before crafting your explanation:
 
 1. **Explore multiple narrative approaches** - Consider at least 2-3 different ways to structure the explanation
@@ -22,7 +19,7 @@
 3. **Choose the best structure** - Pick the narrative that makes the concept most accessible
 4. **Plan your examples** - Identify concrete, specific examples before writing
 
-Take time to think through these options. A well-chosen structure is more valuable than a quick response.
+A well-chosen structure is more valuable than a quick response.
 
 **If concept is unfamiliar or requires research:** Load `research_methodology.md` for detailed guidance.
 **If user provides YouTube video:** Call `uv run scripts/get_youtube_transcript.py <video_url_or_id>` for video's transcript.
@@ -125,7 +122,7 @@
 
 ## Workflow Summary
 
-1. **Think hard**: Explore 2-3 narrative structures, choose the clearest for the audience
+1. **Choose a structure**: Compare 2-3 narrative structures, pick the clearest for the audience
 2. **Identify audience**: Assess knowledge level (if unclear, assume beginner level)
 3. **Check if research needed**:
    - Can you explain this with your existing knowledge? → Proceed to step 4
@@ -135,10 +132,10 @@
 6. **Optional analogy**: Only if it adds value beyond direct explanation
 7. **Offer to dive deeper**: Invite questions on specific aspects
 
-## Critical Rules
-- **ALWAYS** preserve URLs from source documents — do not drop links found in course docs, BOM, or lesson plans
-- **ALWAYS** use reference-style links (`[text][01]`) with definitions at the bottom — never inline URLs
-- **NEVER** duplicate a URL in the reference list — reuse the same `[NN]` number for repeated references
+## Rules
+- Always preserve URLs from source documents — do not drop links found in course docs, BOM, or lesson plans
+- Always use reference-style links (`[text][01]`) with definitions at the bottom — never inline URLs
+- Never duplicate a URL in the reference list — reuse the same `[NN]` number for repeated references
 
 ## Output Structure
 
diff -ru a/.claude/skills/history_and_application/SKILL.md b/.claude/skills/history_and_application/SKILL.md
--- a/.claude/skills/history_and_application/SKILL.md
+++ b/.claude/skills/history_and_application/SKILL.md
@@ -16,9 +16,6 @@
 each section contains two required subsections: a **brief narrative** (0.25-0.5 pages) and
 a **detailed bulleted timeline**.
 
-## Definitions
-For shared terminology and type definitions across all the skills in `.claude/skills/`, read `.claude/skills/shared/definitions.md`.
-
 ## What Is a History and Application Document?
 
 A history and application document answers two questions about a technology or system:
@@ -425,19 +422,19 @@
 | Control Theory | Early governors and regulators | Process control, aerospace, automotive, robotics |
 | Sensors | Early detection methods | Industrial, medical, environmental, consumer |
 
-## Critical Rules
+## Rules
 
-- **NEVER** generate without researching the subject first — check sources, historical records, biographies
-- **NEVER** write the narratives as dry textbook summaries — tell a story
-- **NEVER** use jargon without immediately defining it in plain language
-- **ALWAYS** include both major sections (History and Application), each with both subsections (narrative and timeline)
-- **ALWAYS** make each narrative self-contained — it must stand alone as a correct summary
-- **ALWAYS** keep narratives to 0.25-0.5 pages (roughly 150-300 words each)
-- **ALWAYS** include 10-25 timeline entries per section
-- **ALWAYS** name specific people, dates, and places — no vague references
-- **ALWAYS** connect cause and effect in the narrative — explain why, not just what
-- **ALWAYS** preserve URLs from source documents — do not drop links found in course docs, BOM, or lesson plans
-- **ALWAYS** use reference-style links (`[text][01]`) with definitions at the bottom — never inline URLs
-- **NEVER** duplicate a URL in the reference list — reuse the same `[NN]` number
-- **ALWAYS** flag uncertain historical details as `[VERIFY]`
-- **ALWAYS** target high school students as the default audience — accessible language, minimal jargon
+- Never generate without researching the subject first — check sources, historical records, biographies
+- Never write the narratives as dry textbook summaries — tell a story
+- Never use jargon without immediately defining it in plain language
+- Always include both major sections (History and Application), each with both subsections (narrative and timeline)
+- Always make each narrative self-contained — it must stand alone as a correct summary
+- Always keep narratives to 0.25-0.5 pages (roughly 150-300 words each)
+- Always include 10-25 timeline entries per section
+- Always name specific people, dates, and places — no vague references
+- Always connect cause and effect in the narrative — explain why, not just what
+- Always preserve URLs from source documents — do not drop links found in course docs, BOM, or lesson plans
+- Always use reference-style links (`[text][01]`) with definitions at the bottom — never inline URLs
+- Never duplicate a URL in the reference list — reuse the same `[NN]` number
+- Always flag uncertain historical details as `[VERIFY]`
+- Always target high school students as the default audience — accessible language, minimal jargon
diff -ru a/.claude/skills/html_slide_deck/SKILL.md b/.claude/skills/html_slide_deck/SKILL.md
--- a/.claude/skills/html_slide_deck/SKILL.md
+++ b/.claude/skills/html_slide_deck/SKILL.md
@@ -120,8 +120,8 @@
 
 ### Saving or resetting the default
 
-- **Save as new default** → write the resolved spec as JSON to `.claude/html-slide-deck.defaults.json`
-  (create the `.claude/` directory if needed). This becomes "the default" for every future run
+- **Save as new default** → write the resolved spec as JSON to `.claude/skills/html_slide_deck/assets/html-slide-deck.defaults.json`
+  (the project-local path Step 1 reads). This becomes "the default" for every future run
   of this skill in this project, until reset.
 - **Just this deck** → use the resolved spec for the current build only; don't write the file.
 - **Reset the default** → delete the defaults file; the built-in spec from Step 2 applies again.
diff -ru a/.claude/skills/lesson_plan_generator/SKILL.md b/.claude/skills/lesson_plan_generator/SKILL.md
--- a/.claude/skills/lesson_plan_generator/SKILL.md
+++ b/.claude/skills/lesson_plan_generator/SKILL.md
@@ -15,9 +15,6 @@
 a single class: what to prep, what to say, what to build, how to handle problems, and how to wrap up.
 It covers the *how* — the syllabus covers the *what* and *when*.
 
-## Definitions
-For shared terminology and type definitions across all the skills in `.claude/skills/`, read `.claude/skills/shared/definitions.md`.
-
 ## Curriculum vs Syllabus vs Lesson Plan
 
 These three documents serve different purposes and operate at different levels of detail:
@@ -31,10 +28,10 @@
 The lesson plan takes the syllabus's Class outline and expands it into a minute-by-minute guide
 with instructor notes, prep checklists, troubleshooting tips, and engagement strategies.
 
-**Critical rule:** Lesson plans, syllabus, and bill of materials (BOM) for the same course must be consistent.
+**Rule:** Lesson plans, syllabus, and bill of materials (BOM) for the same course must be consistent.
 The lesson plan's Class number, title, topics, materials, and assessment must match the syllabus exactly.
 The BOM is the single source of truth for all cost and sourcing information —
-lesson plans must NOT include prices, per-student costs, or purchase links for components.
+lesson plans must not include prices, per-student costs, or purchase links for components.
 Reference the BOM for cost details instead.
 
 ## Makerspace Context
@@ -362,18 +359,18 @@
 document which values give the smoothest line following.
 ```
 
-## Critical Rules
+## Rules
 
-- **NEVER** generate a lesson plan without first reading the syllabus. The syllabus is the source of truth.
-- **NEVER** include prices, per-student costs, or purchase links in the lesson plan — those belong in the BOM
-- **NEVER** include grades, rubrics, formal quizzes, multiple-choice tests, or Bloom's taxonomy references
-- **NEVER** use education jargon (SMART objectives, scaffolding, differentiated instruction, formative assessment)
+- Never generate a lesson plan without first reading the syllabus. The syllabus is the source of truth.
+- Never include prices, per-student costs, or purchase links in the lesson plan — those belong in the BOM
+- Never include grades, rubrics, formal quizzes, multiple-choice tests, or Bloom's taxonomy references
+- Never use education jargon (SMART objectives, scaffolding, differentiated instruction, formative assessment)
   unless the user specifically requests it
-- **ALWAYS** include a troubleshooting guide — this is the most valuable section for volunteer instructors
-- **ALWAYS** include age differentiation for every major activity
-- **ALWAYS** include actual time estimates for every segment and activity
-- **ALWAYS** verify that Class number, title, topics, and materials match the syllabus
-- **ALWAYS** use reference-style links (`[text][01]`) with definitions at the bottom of the file — never inline URLs
-- **ALWAYS** preserve URLs from source documents — do not drop links found in syllabus, course docs, or BOM
-- **NEVER** duplicate a URL in the reference list — reuse the same `[NN]` number for repeated references
-- **ALWAYS** flag as "[VERIFY]", if technical details are uncertain (pin numbers, library versions, exact code).
+- Always include a troubleshooting guide — this is the most valuable section for volunteer instructors
+- Always include age differentiation for every major activity
+- Always include actual time estimates for every segment and activity
+- Always verify that Class number, title, topics, and materials match the syllabus
+- Always use reference-style links (`[text][01]`) with definitions at the bottom of the file — never inline URLs
+- Always preserve URLs from source documents — do not drop links found in syllabus, course docs, or BOM
+- Never duplicate a URL in the reference list — reuse the same `[NN]` number for repeated references
+- Always flag as "[VERIFY]", if technical details are uncertain (pin numbers, library versions, exact code).
diff -ru a/.claude/skills/python_code/SKILL.md b/.claude/skills/python_code/SKILL.md
--- a/.claude/skills/python_code/SKILL.md
+++ b/.claude/skills/python_code/SKILL.md
@@ -1,7 +1,6 @@
 ---
 name: python_code
-description: Guide for creating high-quality, efficient, and readable Python functions that communicate their intent clearly, handle their responsibilities cleanly, and make the job of the next person who modifies the code easier. You should use this skill when users
-request Python code to be generated by you.
+description: Guide for creating high-quality, efficient, and readable Python functions that communicate their intent clearly, handle their responsibilities cleanly, and make the job of the next person who modifies the code easier. Use this skill whenever you generate Python or CircuitPython code.
 license: Complete terms in LICENSE.txt
 ---
 
diff -ru a/.claude/skills/readme_generator/SKILL.md b/.claude/skills/readme_generator/SKILL.md
--- a/.claude/skills/readme_generator/SKILL.md
+++ b/.claude/skills/readme_generator/SKILL.md
@@ -226,22 +226,22 @@
 lint failures.
 
 
-## Critical Rules
+## Rules
 
-- **NEVER** generate READMEs for directories out of scope for this skill (Step 0) — tell the user
+- Never generate READMEs for directories out of scope for this skill (Step 0) — tell the user
     why and stop.
-- **NEVER** create a README for a directory with two or fewer files, unless the user explicitly
+- Never create a README for a directory with two or fewer files, unless the user explicitly
     asks for one anyway.
-- **NEVER**, in single-directory mode, touch any directory the user didn't name.
-- **ALWAYS** read `CLAUDE.md` before drafting — every README must be consistent with the
+- Never, in single-directory mode, touch any directory the user didn't name.
+- Always read `CLAUDE.md` before drafting — every README must be consistent with the
     project's documented structure and conventions.
-- **ALWAYS** treat an existing `README.md` as a directive for content, not something to overwrite
+- Always treat an existing `README.md` as a directive for content, not something to overwrite
     blindly.
-- **ALWAYS** get the user's approval of the template plan (whole-project Step 1) or resolve
+- Always get the user's approval of the template plan (whole-project Step 1) or resolve
     ambiguity via `grill-me` (single-directory Step 4) before writing.
-- **ALWAYS** back up an overwritten `README.md` to `README.md.bak` first.
-- **ALWAYS** get the user's review/approval of the finished README(s) before considering the task
+- Always back up an overwritten `README.md` to `README.md.bak` first.
+- Always get the user's review/approval of the finished README(s) before considering the task
     done.
-- **ALWAYS** lint the finished file(s) and fix newly introduced warnings.
-- In whole-project mode, **NEVER** loop the Step 2→4 regeneration cycle more than 5 times — stop
+- Always lint the finished file(s) and fix newly introduced warnings.
+- In whole-project mode, never loop the Step 2→4 regeneration cycle more than 5 times — stop
     and ask the user if the checklist still isn't passing after 5 loops.
diff -ru a/.claude/skills/syllabus_generator/SKILL.md b/.claude/skills/syllabus_generator/SKILL.md
--- a/.claude/skills/syllabus_generator/SKILL.md
+++ b/.claude/skills/syllabus_generator/SKILL.md
@@ -15,9 +15,6 @@
 topics, schedule, materials, objectives, and how progress is measured.
 It covers the *what* and *when* — the lesson plans cover the *how*.
 
-## Definitions
-For shared terminology and type definitions across all the skills in `.claude/skills/`, read `.claude/skills/shared/definitions.md`.
-
 ## Curriculum vs Syllabus vs Lesson Plan
 
 These three documents serve different purposes and operate at different levels of detail:
@@ -31,10 +28,10 @@
 The syllabus is the bridge: it takes curriculum-level goals and breaks them into a Class-by-Class schedule
 that lesson plans then flesh out with detailed teaching instructions.
 
-**Critical rule:** Syllabus, lesson plans, and bill of materials (BOM) for the same course must be consistent.
+**Rule:** Syllabus, lesson plans, and bill of materials (BOM) for the same course must be consistent.
 If a syllabus exists, lesson plans must follow its structure. If lesson plans exist, the syllabus must reflect them.
 The BOM is the single source of truth for all cost and sourcing information —
-the syllabus must NOT include prices, per-student costs, or purchase links for components.
+the syllabus must not include prices, per-student costs, or purchase links for components.
 Reference the BOM for cost details instead.
 
 ## Makerspace Context
@@ -69,9 +66,9 @@
 1. **Check for existing course documents** — Glob for `*.md` files in the project directory.
    Read the main course document (e.g., `building-a-line-following-robot.md`) for technical content,
    design iterations, and learning progression.
-2. **Check for existing lesson plans** — If lesson plans exist, the syllabus MUST align with their
+2. **Check for existing lesson plans** — If lesson plans exist, the syllabus must align with their
    Class structure, topics, materials, and assessment methods.
-3. **Check for a bill of materials** — Use accurate costs and sourcing info.
+3. **Check for a bill of materials** — Use its exact component names; costs and sourcing stay in the BOM.
 4. **Check CLAUDE.md** — for project-specific conventions and context.
 5. **Collect all URL links** — As you read source documents, collect every URL reference
    (product links, tutorial links, video links, datasheets, etc.). These must be preserved
@@ -283,15 +280,15 @@
 > Age brackets: 12-14, 15-18, Adults. Multiple attempts allowed.
 ```
 
-## Critical Rules
+## Rules
 
-- **NEVER** include grades, rubrics, GPA calculations, or formal quizzes
-- **NEVER** use academic jargon (Bloom's taxonomy, SMART objectives, scaffolding, differentiated instruction)
+- Never include grades, rubrics, GPA calculations, or formal quizzes
+- Never use academic jargon (Bloom's taxonomy, SMART objectives, scaffolding, differentiated instruction)
   unless the user specifically requests it
-- **ALWAYS** read existing project files before generating — don't start from scratch if context exists
-- **NEVER** include prices, per-student costs, or purchase links in the syllabus — those belong in the BOM
-- **ALWAYS** verify consistency with lesson plans and BOM if they exist
-- **ALWAYS** use reference-style links (`[text][01]`) with definitions at the bottom of the file — never inline URLs
-- **ALWAYS** preserve URLs from source documents — do not drop links found in course docs, BOM, or lesson plans
-- **NEVER** duplicate a URL in the reference list — reuse the same `[NN]` number for repeated references
+- Always read existing project files before generating — don't start from scratch if context exists
+- Never include prices, per-student costs, or purchase links in the syllabus — those belong in the BOM
+- Always verify consistency with lesson plans and BOM if they exist
+- Always use reference-style links (`[text][01]`) with definitions at the bottom of the file — never inline URLs
+- Always preserve URLs from source documents — do not drop links found in course docs, BOM, or lesson plans
+- Never duplicate a URL in the reference list — reuse the same `[NN]` number for repeated references
 - If unsure about technical details, flag them as "[VERIFY]" rather than guessing
diff -ru a/.claude/skills/teen-install-instructions/SKILL.md b/.claude/skills/teen-install-instructions/SKILL.md
--- a/.claude/skills/teen-install-instructions/SKILL.md
+++ b/.claude/skills/teen-install-instructions/SKILL.md
@@ -9,7 +9,7 @@
 Markdown install guide, written at a level a 12-18 year old with basic Bash/PowerShell/Python
 literacy can follow without hand-holding.
 
-Requires the **Task tool** (subagents) — this skill is designed for Claude Code. If the Task
+Requires the **Agent tool** (subagents) — this skill is designed for Claude Code. If the Agent
 tool isn't available, fall back per the note at the end of Step 4 and Step 5.
 
 ## Workflow overview
@@ -53,8 +53,8 @@
 
 ## Step 2: Research
 
-- `web_fetch` every URL the user gave you; read every local path they gave you.
-- Run `web_search` to confirm each tool's *current* official install instructions and latest
+- `WebFetch` every URL the user gave you; read every local path they gave you.
+- Run `WebSearch` to confirm each tool's *current* official install instructions and latest
   stable version — the user's sources are a starting point, not gospel, and may be stale.
 - Note the version numbers and dates you find; you'll need these for the manifest table and for
   Subagent A to check against.
@@ -102,7 +102,7 @@
 
 ## Step 4: Currency check (Subagent A)
 
-Launch a subagent with the Task tool using the prompt in `agents/currency-checker.md`, passing
+Launch a subagent with the Agent tool using the prompt in `agents/currency-checker.md`, passing
 it the full draft plus the sources you used.
 
 - If it returns required changes, make them, then re-run the subagent on the updated draft.
@@ -110,13 +110,13 @@
   version, and record the unresolved point for the Step 6 summary rather than looping forever.
 - Log every finding and fix (or non-fix, with reason) to your iteration log.
 
-*No Task tool available:* do this pass yourself instead. Explicitly switch hats — re-read the
+*No Agent tool available:* do this pass yourself instead. Explicitly switch hats — re-read the
 draft as a skeptical reviewer checking each command against current docs, not as its author —
 and log findings the same way.
 
 ## Step 5: Sandbox validation (Subagent B)
 
-Launch a subagent with the Task tool using the prompt in `agents/sandbox-validator.md`, passing
+Launch a subagent with the Agent tool using the prompt in `agents/sandbox-validator.md`, passing
 it the full (post-Step-4) draft.
 
 - **Ubuntu-target sections**: the subagent actually builds a Docker sandbox (`ubuntu:24.04`
@@ -131,7 +131,7 @@
   Dockerfile/test harness only if they're sandbox-only artifacts.
 - Fix errors it finds, re-run, cap at 3 rounds same as Step 4, log everything.
 
-*No Task tool / no Docker available:* do a careful manual dry-run of the Ubuntu commands
+*No Agent tool / no Docker available:* do a careful manual dry-run of the Ubuntu commands
 yourself where safe to do so (e.g. in this session's own Linux container), and fall back to the
 static-review approach for all three targets. Say clearly in the final summary that sandbox
 execution didn't happen and why.
diff -ru a/.claude/skills/theory_of_operation/SKILL.md b/.claude/skills/theory_of_operation/SKILL.md
--- a/.claude/skills/theory_of_operation/SKILL.md
+++ b/.claude/skills/theory_of_operation/SKILL.md
@@ -15,9 +15,6 @@
 required sections: a **brief overview** (1-2 paragraphs) and a **detailed step-by-step
 decomposition** of the system's operation.
 
-## Definitions
-For shared terminology and type definitions across all the skills in `.claude/skills/`, read `.claude/skills/shared/definitions.md`.
-
 ## What Is a Theory of Operation?
 
 A theory of operation is a description of how a device or system is intended to work.
@@ -394,19 +391,19 @@
 | Hybrid systems | Primary operational loop | Mix of above | System-level interaction |
 
 
-## Critical Rules
+## Rules
 
-- **NEVER** generate without researching the subject first — check sources, datasheets, documentation
-- **NEVER** explain how to build, assemble, or use the system — this is not a build guide or user manual
-- **NEVER** use jargon without immediately defining it in plain language
-- **ALWAYS** include both the brief overview AND the detailed steps — both are required
-- **ALWAYS** make the brief overview self-contained — it must stand alone as a correct summary
-- **ALWAYS** limit the overview to 1-2 paragraphs (80-200 words)
-- **ALWAYS** follow the operational sequence in steps, not the build or teaching sequence
-- **ALWAYS** give every step both a title and a detailed description
-- **ALWAYS** include concrete values and units where they build intuition
-- **ALWAYS** connect steps explicitly — no gaps in the operational chain
-- **ALWAYS** preserve URLs from source documents — do not drop links found in course docs, BOM, or lesson plans
-- **ALWAYS** use reference-style links (`[text][01]`) with definitions at the bottom — never inline URLs
-- **NEVER** duplicate a URL in the reference list — reuse the same `[NN]` number
-- **ALWAYS** flag uncertain technical details as `[VERIFY]`
+- Never generate without researching the subject first — check sources, datasheets, documentation
+- Never explain how to build, assemble, or use the system — this is not a build guide or user manual
+- Never use jargon without immediately defining it in plain language
+- Always include both the brief overview AND the detailed steps — both are required
+- Always make the brief overview self-contained — it must stand alone as a correct summary
+- Always limit the overview to 1-2 paragraphs (80-200 words)
+- Always follow the operational sequence in steps, not the build or teaching sequence
+- Always give every step both a title and a detailed description
+- Always include concrete values and units where they build intuition
+- Always connect steps explicitly — no gaps in the operational chain
+- Always preserve URLs from source documents — do not drop links found in course docs, BOM, or lesson plans
+- Always use reference-style links (`[text][01]`) with definitions at the bottom — never inline URLs
+- Never duplicate a URL in the reference list — reuse the same `[NN]` number
+- Always flag uncertain technical details as `[VERIFY]`
diff -ru a/.claude/skills/wiring_diagram/SKILL.md b/.claude/skills/wiring_diagram/SKILL.md
--- a/.claude/skills/wiring_diagram/SKILL.md
+++ b/.claude/skills/wiring_diagram/SKILL.md
@@ -69,7 +69,7 @@
     confirm the dots actually land on the real holes before calling it done — this is
     the check that catches a wrong fraction, not just a visual skim of the full diagram.
 
-## Pitfalls (hit and fixed while building the first one of these)
+## Pitfalls
 
 - **Label collision**: terminal pins must be spaced far enough apart that their text
   labels don't overlap into unreadable runs (e.g. "VCC"+"GND"+"OUT" merging into
diff -ru a/CLAUDE.md b/CLAUDE.md
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ -141,6 +141,12 @@
 purchase receipts (photos, a `receipts/` subdir) — no established doc conventions there yet, not
 course content.
 
+`full_build/` is the one-session build of the finished Random Rover (Classes 1-6 plus all three
+Class 6 stretch goals): `full-build-script.md` is the main doc; `src/pico/` holds ready-to-deploy
+rover code, several files copied verbatim from the Class 3/5/6 lesson scripts — when that lesson
+code changes, copy the change there too (its `README.md` lists which files); `src/tools/` and
+`test/` hold calibration tools and tests; `deploy.py` copies code onto `CIRCUITPY`.
+
 `src/` holds **laptop-side** code and rover tuning material — code that runs on the student's
 computer, not on the Pico. It has no project of its own; each subdirectory stands alone:
 
````
