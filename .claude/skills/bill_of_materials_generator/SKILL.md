---
name: bill-of-materials-generator
description: Generate a complete bill of materials (BOM) for a makerspace workshop. Use when an instructor needs a BOM, parts list, materials list, shopping list, or cost breakdown for a hands-on workshop. The BOM is the single source of truth for all cost and sourcing information. Designed for volunteer makerspace instructors, not professional teachers. The generated BOM must be consistent with the course syllabus and lesson plans.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
license: MIT
metadata:
  author: Jeff Irland (Makersmiths)
  version: "0.0.1"
---

# Bill of Materials Generator

Generate a complete, itemized bill of materials (BOM) for a makerspace workshop.
The BOM is the **single source of truth** for all cost and sourcing information in the project.
Neither the syllabus nor the lesson plans should contain cost details — they reference the BOM instead.

The BOM answers: what do we need to buy, how much does it cost, and where do we get it?

## Definitions
For shared terminology and type definitions across all the skills in `.claude/skills/`, read `.claude/skills/shared/definitions.md`.

## Relationship to Syllabus and Lesson Plans

The three core course documents have distinct responsibilities:

| Document | Owns | Does NOT Own |
| :--------- | :----- | :------------- |
| **Syllabus** | Topics, schedule, objectives, structure, assessment | Costs, sourcing, pricing |
| **Lesson Plan** | Session-level teaching instructions, per-session materials list (names only) | Costs, sourcing, pricing |
| **Bill of Materials** | All costs, quantities, sourcing, pricing, shipping, per-student totals | Teaching content, schedule |

**Critical rule:** The BOM must be consistent with the syllabus and lesson plans.
Every component referenced in the syllabus or lesson plans must appear in the BOM.
Every component in the BOM should be used in at least one session described in the syllabus.

## Makerspace Context

This skill is designed for **makerspace workshops**. Key implications for the BOM:

- **Students keep what they build.** The per-student hardware cost is a real expense for students or parents.
  Budget transparency is essential — list every cost, including shipping.
- **The makerspace provides shared tools.** Soldering stations, multimeters, safety gear, etc.
  are provided by the facility and don't go into the per-student cost.
- **Instructors are volunteers** who need a clear shopping list they can hand to a purchaser or order themselves.
- **Mixed-age groups.** Some items may be optional "nice to have" upgrades that older/advanced students
  might use. Separate required from optional clearly.
- **Budget matters.** Many makerspaces operate on tight budgets. The BOM must help planners
  understand the minimum cost vs the full-featured cost.

## When to Use This Skill

Activate when:
- An instructor asks for a "bill of materials," "BOM," "parts list," "materials list," or "shopping list"
- Someone needs cost estimates or a budget breakdown for a workshop
- A course is being planned and materials need to be sourced and priced
- An existing BOM needs to be updated with new components or current pricing

## How to Generate a Bill of Materials

### Step 1: Gather Context

Before generating anything, read existing project files:

1. **Check for existing course documents** — Glob for `*.md` files in the project directory.
   Read the main course document for component names, technical specifications, and design iterations.
2. **Check the syllabus** — Extract all components, hardware, software, and tools mentioned
   in the Technology Requirements and Lessons Breakdown sections.
3. **Check existing lesson plans** — Extract per-session materials lists to ensure nothing is missed.
4. **Check for an existing BOM** — If one exists, use it as a starting point for updates.
5. **Check CLAUDE.md** — for project-specific conventions and context.
6. **Collect all URL links** — As you read source documents, collect every product URL,
   vendor link, and download link. These must be preserved in the generated BOM.
   See "Link Management" below for formatting rules.

If no existing documents are found, collect from the user:
- **What are students building?** — The project determines the components
- **Class size** — Needed for shared-item cost splitting
- **Budget target** — Maximum per-student cost
- **Makerspace inventory** — What tools/supplies does the facility already have?

If information is missing, make reasonable assumptions, state them explicitly, and proceed.

### Step 2: Categorize All Items

Separate every item into one of these categories:

1. **Per-Student Required Hardware** — Components each student needs and keeps.
   These form the base per-student cost.
2. **Per-Student Optional Hardware** — "Nice to have" components that enhance the project
   but aren't required for core functionality. Separate cost line.
3. **Shared Supplies** — Minor parts, consumables, and bulk items shared among all students.
   Cost is divided by class size.
4. **Shipping** — Shipping costs per vendor, divided by class size.
5. **Software** — All software used in the course. Should be free/open source for makerspace workshops.
   No cost, but list with download/install links.
6. **Code Blocks** — Pre-written code provided to students to stay on schedule.
   No cost, but list what's provided and by whom.
7. **Tools** — Equipment needed during the course. Indicate whether provided by the makerspace
   or by the student (e.g., laptop, safety glasses).

### Step 3: Build the Tables

For each category, create a table using the standard format (see Output Structure below).
For every hardware item, include:
- **Item** — Descriptive name matching what's used in the syllabus and lesson plans
- **Quantity** — Per student (for per-student tables) or total (for shared tables)
- **Item Cost** — Unit price, formatted as `$X.XX`
- **Source** — Vendor name as a reference-style link to the product page
- **Notes** — Brief description of what it's for, which sessions use it, or other relevant info

### Step 4: Calculate Cost Summaries

After each table, include a cost calculation line showing the math:

```text
Per-Student Required Cost = item1 + item2 + ... = $XX.XX per student
```

At the bottom, provide total cost summaries:

```text
Total Cost = required + shared + shipping = ~$XX per student
Total Cost = required + optional + shared + shipping = ~$XX per student (with options)
```

Use a reasonable default class size (e.g., 4 students) for dividing shared and shipping costs.
State the assumed class size explicitly so users can recalculate.

### Step 5: Review for Consistency

Before finalizing, verify:
- [ ] Every component mentioned in the syllabus appears in the BOM
- [ ] Every component mentioned in any lesson plan appears in the BOM
- [ ] Component names match exactly across BOM, syllabus, and lesson plans
- [ ] Every hardware item has a source link
- [ ] Costs are current and accurate (flag stale prices as "[VERIFY PRICE]")
- [ ] Cost math is correct (spot-check the arithmetic)
- [ ] Shipping costs account for all vendors used
- [ ] All URLs from source documents are preserved
- [ ] All links use reference-style format with `[01]`, `[02]`, etc. at bottom of file
- [ ] No duplicate URLs in the reference list

### Step 6: Export

Export to the requested format:
- **.md** — GitHub-flavored markdown (default). Clean headers, tables, bullet lists.
- **.docx** — Use pandoc: `pandoc -f gfm input.md -o output.docx`
- **.pdf** — Use pandoc with a PDF engine: `pandoc -f gfm input.md -o output.pdf`

## Output Structure

The final BOM must contain these sections in this order:

```text
# Bill of Materials

Introductory paragraph describing what the BOM covers.

* **Hardware -** brief description
* **Software -** brief description
* **Code Blocks -** brief description
* **Tools -** brief description

## Hardware

### Per-Student Required
[table + cost calculation]

### Per-Student Optional
[table + cost calculation]

### Shared Supplies
[table + cost calculation]

### Shipping
[table + cost calculation]

### Cost Summary
[total cost calculations]

## Software
[table with install links]

## Code Blocks
[table of provided code]

## Tools
[table indicating provider: Student or Makerspace]
```

### Table Formats

**Hardware tables** (per-student required, optional, shared, shipping) must use this format:

```markdown
| Item | Quantity | Item Cost | Source | Notes |
|:-----:|:-----:|:-----:|:-----:|:--------:|
| Component Name | 1 | $10.00 | [Vendor][01] | what it's for |
```

**Software table:**

```markdown
| Item | Source | Notes |
|:-----:|:-----:|:--------:|
| Software Name | [Webpage][01] | description |
```

**Code Blocks table:**

```markdown
| Item | Quantity | Source | Notes |
|:-----:|:-----:|:-----:|:--------:|
| Code Block Name | 1 | Provider | what it does |
```

**Tools table:**

```markdown
| Item | Quantity | Source | Notes |
|:-----:|:-----:|:-----:|:--------:|
| Tool Name | 1 | Makerspace | |
| Laptop Computer | 1 | Student | |
```

### Link Management

All URLs referenced in the generated BOM must use **reference-style markdown links**.
This keeps the document body clean and readable while collecting all URLs in one place at the bottom.

**Rules:**
1. In the document body, use numbered reference tags: `[link text][01]`, `[link text][02]`, etc.
2. Collect all reference definitions at the **very bottom** of the file, after all content sections.
3. Number references sequentially with zero-padded two-digit numbers: `[01]`, `[02]`, `[03]`, ... `[10]`, `[11]`, etc.
4. **No duplicate URLs.** If the same URL is referenced multiple times in the document, reuse the same reference number.
5. Preserve all URLs found in source documents (syllabus, course documents, lesson plans). Do not drop links.
6. Every reference definition must follow this format with no space before the colon:

   ```text
   [01]:https://example.com/page
   [02]:https://example.com/other-page
   ```

**Example in document body:**

```markdown
| Robot Car Kit | 1 | $10.00 | [Amazon][01] | car body for building robot |
| Raspberry Pi Pico W | 1 | $12.00 | [Amazon][03] | MCU for advanced features |
```

**Example at bottom of file:**

```markdown
[01]:https://www.amazon.com/MiOYOOW-Soldering-Electronics-Following-Competition/dp/B07ZH4XLQ3?th=1
[02]:https://www.amazon.com/Infrared-Avoidance-Transmitting-Receiving-Photoelectric/dp/B07PFCC76N?th=1
[03]:https://www.amazon.com/Raspberry-Pi-Pico-Wireless-Bluetooth/dp/B0B5H17CMK
```

## Best Practices

1. **BOM is the single source of truth for costs** — the syllabus and lesson plans reference
   component names but never include prices, per-student totals, or sourcing details.
   All cost information lives exclusively in the BOM.
2. **Consistency with syllabus and lesson plans** — component names must match exactly.
   If the syllabus says "Pololu QTR-8A Reflectance Sensor Array," the BOM must use that same name.
3. **Separate required from optional** — make it easy to calculate the minimum viable cost
   vs the full-featured cost. Parents and budget planners need this distinction.
4. **Show your math** — include the arithmetic for every cost subtotal and the final per-student total.
   This lets users verify and adjust for different class sizes.
5. **Include shipping** — shipping costs are real and often forgotten. List them per vendor
   and divide by class size. State the assumed class size.
6. **Link to actual product pages** — every hardware item needs a clickable link to where it can be purchased.
   This saves the purchaser from having to search for each item.
7. **Flag stale prices** — if a price might be outdated, mark it as "[VERIFY PRICE]".
   Hardware prices change; the BOM should be treated as a living document.
8. **Software must be free** — makerspace workshops should not require paid software.
   If a paid option exists, list it as optional with a free alternative.
9. **Indicate who provides tools** — clearly mark whether each tool is provided by the makerspace
   or the student. Students need to know to bring a laptop and safety glasses.

## Examples

### Example: Good Per-Student Required Table

```markdown
### Per-Student Required

These items are required by each student:

| Item | Quantity | Item Cost | Source | Notes |
|:-----:|:-----:|:-----:|:-----:|:--------:|
| Robot Car Kit | 1 | $10.00 | [Amazon][01] | car body for building robot |
| IR Emitter/Phototransistor Pair | 2 | $10.00 | [Amazon][02] | sensors to detect line |
| Raspberry Pi Pico W | 1 | $12.00 | [Amazon][03] | MCU for advanced features |
| Robotics Motor Driver Board | 1 | $19.00 | [PiShop.us][04] | board to interface with MCU |
| QTRX-MD-08RC Reflectance Sensor Array | 1 | $16.00 | [Pololu][05] | sensors to detect line |

Per-Student Required Cost = 10 + 2*10 + 12 + 19 + 16 = $77.00 per student
```

### Example: Good Cost Summary

```markdown
### Cost Summary

Assuming a class size of 4 students:

Total Cost = 77 + 1.50 + 6.00 = ~$85 per student
Total Cost = 77 + 23 + 1.50 + 6.00 = ~$108 per student (with options)
```

### Example: Good Shipping Table

```markdown
### Shipping

These shipping charges will be shared among all students:

| Item | Quantity | Item Cost | Source | Notes |
|:-----:|:-----:|:-----:|:-----:|:--------:|
| Amazon Shipping | NA | $0 | NA | free with Prime |
| PiShop.us Shipping | NA | $8 | NA | |
| Pololu Shipping | NA | $8 | NA | |
| Adafruit Shipping | NA | $8 | NA | |

Shipping Cost = 3*8 / 4 = $6.00 per student (assuming 4 students)
```

## Critical Rules

- **NEVER** include cost or pricing information in the syllabus or lesson plans — costs belong exclusively in the BOM
- **NEVER** omit a component that appears in the syllabus or lesson plans — every referenced item must be in the BOM
- **ALWAYS** read the syllabus and lesson plans before generating — ensure complete coverage
- **ALWAYS** include source links for every purchasable hardware item
- **ALWAYS** show the cost arithmetic so users can verify and adjust for their class size
- **ALWAYS** separate required from optional items with independent cost subtotals
- **ALWAYS** include shipping costs — they are real expenses that affect the per-student budget
- **ALWAYS** use reference-style links (`[text][01]`) with definitions at the bottom of the file — never inline URLs
- **ALWAYS** preserve URLs from source documents — do not drop links found in syllabus, course docs, or lesson plans
- **NEVER** duplicate a URL in the reference list — reuse the same `[NN]` number for repeated references
- **ALWAYS** flag it as "[VERIFY PRICE]", rather than guessing, if a price might be outdated.
