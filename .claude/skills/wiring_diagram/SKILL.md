---
name: wiring_diagram
description: Generate a labeled schematic wiring diagram (PNG) from a markdown pinout table and embed it in the doc. Use when a markdown file has a "Wiring — <Board> to <Module>" table (columns like Board Pin | Module Pin | Signal/Function) and the user wants a visual/diagram/picture of that wiring added to the doc.
---

# Wiring diagram from a pinout table

## Quick start

Given a table like:

| Pico 2W Pin | Sensor Pin | Signal / Function |
| --- | --- | --- |
| `3V3(OUT)` or `VBUS` | `VCC` | Power |
| `GND` | `GND` | Common ground |
| `GP13` | `OUT` | Digital output |

Using the `/design` skill, produce one static, single-artboard `.dc.html`
(see `reference/example.dc.html` for a full worked example built from this exact table) with:

- **Left**: a simple silhouette of the board (rectangle + a couple of identifying
  details), with the used pins marked on its right edge and labeled with their exact
  name from column 1.
- **Right**: a simple silhouette of the module, with a row of terminal pins along one
  edge, one per row of the table, labeled with their exact name from column 2.
- **Wires**: one curved path per row, color-coded by function (power = red, ground =
  black/dark, signal = blue — reuse this convention across diagrams), each ending
  exactly on its terminal pin with a matching colored dot at both ends. If a table has
  a wiring relationship that doesn't fit power/ground/signal (e.g. a motor driver's
  output leads to a motor), add a 4th color and its own legend row rather than
  stretching "signal" to cover it.
- A small color-key legend below the diagram, and one caption line: "Schematic, not
  to scale."

Then render it (`scripts/render-png.sh <file>.dc.html <name>.png`) and add
`![<short description>](<name>.png)` to the markdown, directly after the pinout table.
Keep both the `.dc.html` source and the `.png` next to the markdown file — re-run the
script after any edit to the source rather than hand-editing the PNG.

## Using real product photos instead of drawn silhouettes

If a clean product photo of the board and/or module is available, use it in place of a
hand-drawn silhouette for that component rather than redrawing what already exists as a
photo. It's fine to mix — a real photo for one side and a hand-drawn silhouette for the
other (or for extra components with no photo, e.g. a motor or battery in the same
diagram) — as long as the wire/color conventions stay consistent across both.

- **Trim first, embed as a data URI**: crop excess background off a working copy of the
  source photo (`convert <photo>.png -fuzz 3% -trim +repage <trimmed>.png` — never
  overwrite the original), then base64-embed the trimmed copy directly in the `.dc.html`
  as `<image href="data:image/png;base64,...">` (SVG) or `<img src="data:...">` (HTML).
  Don't reference it by relative path — `render-png.sh` extracts the artboard markup into
  a different temp directory, which breaks relative image paths; a data URI has no such
  dependency and keeps the `.dc.html` self-contained.
- **Estimating pin positions on a photo**: a photo has no built-in coordinate system the
  way a hand-drawn silhouette does, so terminal positions have to be figured out per
  photo:
  - If the board's silkscreen prints the pin names legibly (many breakout boards do),
    upscale/crop the photo (`convert <photo>.png -resize 800x` or similar) and read the
    label positions directly off the zoomed image, then express each as a *fraction* of
    the photo's width/height so the math still works whatever size the photo is placed
    at in the final layout.
  - If the silkscreen doesn't print the pin names at all (e.g. a bare microcontroller's
    GPIO header), fall back to the board's known/official pinout order to compute
    position fractions, and add a caption line noting that positions are approximate —
    don't let the diagram imply a precision the photo doesn't actually show.
  - After rendering, crop the output PNG down to just the pin-cluster region
    (`convert <name>.png -crop <w>x<h>+<x>+<y> +repage <crop>.png`) and view that crop to
    confirm the dots actually land on the real holes before calling it done — this is
    the check that catches a wrong fraction, not just a visual skim of the full diagram.

## Pitfalls (hit and fixed while building the first one of these)

- **Label collision**: terminal pins must be spaced far enough apart that their text
  labels don't overlap into unreadable runs (e.g. "VCC"+"GND"+"OUT" merging into
  "VCCGNDOUT"). For 13px monospace 3-4 char labels, space pins ≥70px apart center to
  center. Always render and visually check before calling it done.
- **Z-order**: draw the wire `<path>`s (and their terminal dots) *after* both
  component `<g>` groups in the SVG, not before — otherwise an opaque component body
  drawn later covers the wire ends and they look disconnected from the actual pins.
- **Don't screenshot the full design-canvas editor payload** for this — it's a heavy
  app that can sit on "Loading artboard..." for a long time in a sandboxed headless
  browser. Instead extract just the artboard's own markup (everything between
  `</helmet>` and `</x-dc>`, plus its `<style>`/font `<link>`) into a plain static
  HTML file and screenshot that directly — `scripts/render-png.sh` does this.
- **Markdown embedding**: use a plain relative-path image reference
  (`![alt](name.png)`), never inline `<img>`/raw HTML in the `.md` file, and never an
  absolute `file://` link to a non-image file — some markdown preview tools (e.g.
  `markdown-preview.nvim`) serve from a base path that doesn't match the `.md`
  file's own directory, so bare relative *links* to sibling files can 404 even though
  a same-directory *image* embed renders fine.

## Optional: also publish an editable canvas

If the user wants to be able to tweak the diagram visually afterward, seed and
publish the same `.dc.html` as a design canvas via the `design` skill (`Main.dc.html`

- `seed-canvas.mjs` + `Artifact` tool) in addition to the embedded PNG — keep the PNG
as the doc's copy and the canvas as a separate link, and re-render the PNG from the
canvas source (not the other way around) after any edit.
