---
name: html-slide-deck
description: Create a self-contained, single-file HTML slide presentation from a Markdown document (or outline/notes). Prompts the user to use the saved default look or customize it (canvas shape, fonts, colors, slide templates, navigation, extras) before building, and can save a new default or reset to the built-in one. Use when asked to turn a markdown file, notes, or an outline into a presentation, slide deck, or portable/offline HTML slideshow.
---

# HTML Slide Deck

Converts a Markdown document into a single, self-contained `.html` presentation: one file,
no build step, no external runtime — opens in any browser years from now. Fixed-size canvas
(default 1920×1080) scaled to fit the window, slides toggled with a tiny bit of vanilla JS,
with prev/next, a progress bar, dot navigation, fullscreen, and keyboard/touch controls.

Read this whole file before generating anything. Do not skip the customization prompt or the
verification step — both are required, not optional polish.

## Step 0 — Gather the source

Confirm the Markdown file (or pasted content) to convert, and the presentation title if the
user didn't give one (derive a short one from the doc's top-level heading if they didn't).

## Step 1 — Default or customize?

Check for a saved defaults file at `.claude/skills/html_slide_deck/assets/html-slide-deck.defaults.json` (project-local) or
`~/.claude/html-slide-deck.defaults.json` (personal, checked if no project one exists). If one
exists, that is "the default" for this step — not the built-in spec below. If neither exists,
the built-in spec in Step 2 is the default.

Ask the user directly, plainly:

> Use the default look for this deck, or customize it? (You can also say "reset the default"
> to go back to the built-in look, or "save these as my new default" after customizing.)

- If they say **use the default** → skip to Step 4 with the active default spec, unchanged.
- If they say **customize** → go to Step 3.
- If they say **reset the default** → delete the saved defaults file, confirm the built-in
  spec (Step 2) is restored, then ask again whether to use it or customize for this deck.

Don't re-ask this on every slide or every run in the same conversation — ask once per deck.

## Step 2 — The built-in default spec

This is the fallback whenever no saved defaults file exists and the user doesn't customize.

| Aspect | Default |
| --- | --- |
| Canvas | 1920×1080 (16:9), scaled with `transform: scale()` to fit the viewport |
| Headings/body font | IBM Plex Sans (400/500/600/700) |
| Code/mono font | JetBrains Mono (400/500/600) |
| Cover & closing slides | Dark navy `#12181F` background, `#F1F0EA` text, `#5DCAA5` accent |
| Content slides | Light `#F7F6F2` background, `#1C232B` text |
| Semantic accent colors | Teal (`#0F6E56`/`#085041`/`#E1F5EE`/`#5DCAA5`) = positive/solution/today · Coral (`#993C1D`/`#712B13`/`#FAECE7`/`#F0997B`) = problem/warning/disturbance · Purple (`#3C3489`/`#534AB7`/`#EEEDFE`/`#AFA9EC`) = alternate view/preview/"think" · Amber (`#854F0B`/`#BA7517`/`#FBF0DE`/`#E0A94C`) = process/tuning/homework · Neutral gray (`#5F5E5A`/`#8A9199`/`#F1EFE8`/`#B4B2A9`) = inert/not-yet-built |
| Slide templates | Title, agenda (numbered list), two-panel comparison, 3–4 card grid, big centered statement, data table, two-column detail, flow diagram (boxes + arrows), dark "punchline" slide |
| Navigation | Prev/next buttons, `N / total` counter, click-to-seek progress bar, per-slide dot nav, fullscreen toggle |
| Transition | Fade, 0.35s |
| Keyboard | → / Space / PageDown = next · ← / PageUp = prev · Home/End = jump · F = fullscreen · Esc = exit fullscreen |
| Touch | Swipe left/right (50px threshold) |
| Extras | None on by default (no page numbers, no speaker notes, no print stylesheet) |

## Step 3 — Customization menu

Walk the user through these categories **one question at a time**, in order, each with a short
default-first list of options. Accept "default" as an answer to skip any one category instantly.
After all categories, ask: **"Save these as your new default, use them just for this deck, or
both?"** — write to the defaults file only if they say save.

Before asking, offer to generate a visual preview (see below) so choices aren't made blind.

### A. Canvas & aspect ratio
1. **16:9, 1920×1080 (default)** — standard widescreen, works on any projector/monitor
2. **4:3, 1600×1200** — older projectors, or a denser/more text-heavy deck
3. **Ultra-wide, 2400×1080** — cinematic, good for wide diagrams
4. **Portrait, 1080×1350** — reading on a phone/tablet, not presenting on a screen

### B. Typography
1. **IBM Plex Sans + JetBrains Mono (default)** — clean, technical, distinct code font
2. **Inter + Fira Code** — very neutral, common in product/SaaS decks
3. **Source Serif 4 + Source Code Pro** — warmer, editorial/academic feel
4. **A font pair you specify** — name any two Google Fonts (heading/body + mono)

### C. Color system
1. **Default palette** — dark cover/closing, light content, teal/coral/purple/amber semantic
   accents (see Step 2 table)
2. **Single brand color** — you give one hex color; I derive a light/dark tint ramp from it
   and use that everywhere instead of the four semantic families
3. **All-dark theme** — every slide dark, one bright accent color
4. **All-light theme** — every slide light, no dark cover/closing contrast
5. **Your exact palette** — you give me the hex codes and what each is for

### D. Slide templates to use
1. **All of them (default)** — title, agenda, comparison, card grid, statement, table,
   two-column, diagram, punchline — picked per-section based on the content
2. **Text-forward only** — title, agenda, statement, and bulleted content slides; skip cards/
   diagrams/tables even if the content could support them (simpler, faster to read)
3. **Visual-forward** — prefer card grids, comparisons, and diagrams over plain bullet lists
   wherever the content allows it
4. **You specify** — tell me which templates you want available and I'll only use those

### E. Navigation & controls
1. **Full controls (default)** — prev/next, counter, progress bar, dots, fullscreen
2. **Minimal** — just prev/next and a counter, no dots or progress bar
3. **None** — arrow-key/swipe navigation only, no visible control bar (for a clean recording
   or a kiosk display)

### F. Extras (pick any, none on by default)
- **Page numbers** on every slide (bottom corner)
- **Speaker notes** — a hidden per-slide notes panel, toggled with `N`, not visible on the
  main canvas (useful if presenting with a second screen)
- **Print/PDF stylesheet** — an `@media print` block so the deck exports cleanly to PDF from
  the browser's print dialog
- **Logo/watermark** — small image or text in a corner of every slide

### Generating a visual preview

Before or during the menu, offer this: write a small standalone `preview-options.html` (same
single-file approach) that shows real rendered swatches — color chips with hex codes and their
semantic labels, "Aa" samples in each font pairing at heading/body/mono sizes, and small mocked-
up thumbnails of each slide template at reduced scale. Tell the user the file path and ask them
to open it in a browser, then answer the menu questions by number. Delete this preview file
after the choices are made (it's scratch, not a deliverable) unless they ask to keep it.

### Saving or resetting the default

- **Save as new default** → write the resolved spec as JSON to `.claude/html-slide-deck.defaults.json`
  (create the `.claude/` directory if needed). This becomes "the default" for every future run
  of this skill in this project, until reset.
- **Just this deck** → use the resolved spec for the current build only; don't write the file.
- **Reset the default** → delete the defaults file; the built-in spec from Step 2 applies again.

## Step 4 — Convert the Markdown into a slide outline

Read the whole source document first — don't start writing slide HTML before you've read it
end to end, the same way you'd read a lesson script fully before building a deck from it.
Then map it to slides using these heuristics (adjust per the active template settings from
Step 3D):

| Markdown pattern | Slide template |
| --- | --- |
| Document title / first `#` heading | Title/cover slide |
| A short list of `##` section headings | Agenda slide (numbered list) |
| Two things being weighed against each other | Two-panel comparison |
| A short list of 2–4 parallel concepts (a framework, pillars, steps) | Card grid (one card per item) |
| A single strong claim, quote, or thesis sentence | Big centered statement slide |
| A Markdown table | Data table slide |
| A process, pipeline, or before/after with a mechanism | Two-column detail or flow diagram (boxes + arrows) |
| A closing/summary/"key takeaways" section | Closing slide (dark, bulleted recap) |
| Everything else (a paragraph or short bullet list with no stronger structure) | Plain content slide — eyebrow, heading, bullets |

Keep each slide to one idea. If a section is dense, split it into two slides rather than
shrinking the type to fit — presentation slides read from across a room, not up close. Assign
each slide a semantic accent color by what kind of content it is (see the palette table),
not arbitrarily — this is what makes the deck read as one system instead of a random skin.

Don't invent facts, numbers, or claims the source doesn't support. Paraphrasing for brevity and
adding a one-line synthesis/transition between sections is fine; inventing specifics is not.

## Step 5 — Build the HTML file

### Constraints that always apply, regardless of customization

- Single `.html` file. The only external load allowed is the Google Fonts `<link>` (or
  whatever font source Step 3B resolved to) — everything else (CSS, JS, images-as-inline-SVG)
  lives inside the one file.
- `*, *::before, *::after { box-sizing: border-box; }` globally — this matters for the padding
  math below to work out.
- Each slide is a `<section class="slide" style="width:<canvas-w>px; height:<canvas-h>px; padding:128px; ...">`
  absolutely positioned at `top:0; left:0` inside a `#stage` sized to the chosen canvas, which
  is itself `transform: scale()`-fit to the viewport on load and on resize.
- With 128px padding on all sides, the usable content box is `(canvas-w − 256) × (canvas-h − 256)`.
  For the 1920×1080 default that's 1664×824 — check that every slide's content fits inside that
  box before moving on (Step 6 automates this check; don't skip it).
- No live custom elements (no `<x-connector>`-style tags) — this file has to render correctly
  with zero JS framework and zero runtime beyond the nav script below, so any arrows/connectors
  between boxes are plain `position:absolute` divs (a thin bar + a CSS border-triangle arrowhead)
  with pixel coordinates computed by hand, or a `<svg>` for anything curved.
- Body text ≥ 22–24px, headings ≥ 48px — this is presented on a screen from across a room.

### Base template (copy verbatim, then fill in slides)

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{DECK_TITLE}}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{{GOOGLE_FONTS_CSS2_URL}}" rel="stylesheet">
<style>
  *, *::before, *::after { box-sizing: border-box; }
  html, body {
    margin: 0; padding: 0; width: 100%; height: 100%;
    background: #000; overflow: hidden;
    font-family: '{{HEADING_FONT}}', Arial, sans-serif;
  }
  h1, h2, p, ul, li, table, tr, td, th { margin: 0; padding: 0; font-weight: 400; }
  ul { padding-left: 1.1em; }
  table { border-collapse: collapse; }
  td, th { border: 1px solid #DCD9CF; padding: 10px 12px; }

  #viewport {
    position: fixed; inset: 0;
    display: flex; align-items: center; justify-content: center;
    background: #000; overflow: hidden;
  }
  #stage {
    position: relative; width: {{CANVAS_W}}px; height: {{CANVAS_H}}px;
    flex: none; transform: scale(1); transform-origin: center center;
  }
  .slide {
    position: absolute; top: 0; left: 0; width: {{CANVAS_W}}px; height: {{CANVAS_H}}px;
    opacity: 0; visibility: hidden; transition: opacity .35s ease;
  }
  .slide.active { opacity: 1; visibility: visible; }

  #controls {
    position: fixed; left: 0; right: 0; bottom: 0; z-index: 1000;
    display: flex; align-items: center; gap: 18px;
    padding: 10px 24px; background: rgba(18,24,31,0.85); backdrop-filter: blur(6px);
    font-family: '{{HEADING_FONT}}', Arial, sans-serif; color: #F1F0EA;
  }
  #controls button {
    background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.2); color: #F1F0EA;
    width: 36px; height: 36px; border-radius: 8px; font-size: 18px; line-height: 1;
    display: flex; align-items: center; justify-content: center; cursor: pointer; flex: none;
  }
  #controls button:hover:not(:disabled) { background: rgba(255,255,255,0.2); }
  #controls button:disabled { opacity: .3; cursor: default; }
  #counter { font-size: 14px; font-variant-numeric: tabular-nums; min-width: 60px; text-align: center; flex: none; }
  #progress-track { flex: 1; height: 4px; background: rgba(255,255,255,0.18); border-radius: 2px; position: relative; cursor: pointer; }
  #progress-fill { position: absolute; left: 0; top: 0; bottom: 0; width: 0%; background: {{ACCENT_COLOR}}; border-radius: 2px; }
  #dots { display: flex; gap: 6px; flex: none; }
  .dot { width: 8px; height: 8px; border-radius: 50%; background: rgba(255,255,255,0.3); border: none; padding: 0; cursor: pointer; }
  .dot.active { background: {{ACCENT_COLOR}}; }
  #hint {
    position: fixed; top: 18px; right: 18px; z-index: 1000;
    font-size: 12px; color: rgba(255,255,255,0.55);
    font-family: '{{HEADING_FONT}}', Arial, sans-serif;
    background: rgba(18,24,31,0.6); padding: 6px 10px; border-radius: 6px;
    transition: opacity .4s ease;
  }
</style>
</head>
<body>

<div id="viewport">
  <div id="stage">
    <!-- {{SLIDES_GO_HERE}} -->
  </div>
</div>

<div id="hint">Space / ← → to navigate · F fullscreen</div>

<div id="controls">
  <button id="prevBtn" title="Previous (←)" aria-label="Previous slide">‹</button>
  <span id="counter">1 / {{SLIDE_COUNT}}</span>
  <button id="nextBtn" title="Next (→ / Space)" aria-label="Next slide">›</button>
  <div id="progress-track" title="Click to jump to a point in the deck">
    <div id="progress-fill"></div>
  </div>
  <div id="dots"></div>
  <button id="fsBtn" title="Fullscreen (F)" aria-label="Toggle fullscreen">⛶</button>
</div>

<script>
(function () {
  var slideIds = [{{SLIDE_ID_LIST}}];
  var slides = slideIds.map(function (id) { return document.getElementById(id); });
  var idx = 0;

  var counter = document.getElementById('counter');
  var fill = document.getElementById('progress-fill');
  var track = document.getElementById('progress-track');
  var prevBtn = document.getElementById('prevBtn');
  var nextBtn = document.getElementById('nextBtn');
  var fsBtn = document.getElementById('fsBtn');
  var dotsWrap = document.getElementById('dots');
  var stage = document.getElementById('stage');
  var hint = document.getElementById('hint');

  slideIds.forEach(function (id, i) {
    var d = document.createElement('button');
    d.className = 'dot';
    d.setAttribute('aria-label', 'Go to slide ' + (i + 1));
    d.addEventListener('click', function () { goTo(i); });
    dotsWrap.appendChild(d);
  });
  var dots = Array.prototype.slice.call(dotsWrap.children);

  function render() {
    slides.forEach(function (s, i) { s.classList.toggle('active', i === idx); });
    counter.textContent = (idx + 1) + ' / ' + slides.length;
    fill.style.width = (slides.length > 1 ? (idx / (slides.length - 1) * 100) : 100) + '%';
    dots.forEach(function (d, i) { d.classList.toggle('active', i === idx); });
    prevBtn.disabled = idx === 0;
    nextBtn.disabled = idx === slides.length - 1;
  }
  function goTo(i) { idx = Math.max(0, Math.min(slides.length - 1, i)); render(); }
  function next() { if (idx < slides.length - 1) { idx++; render(); } }
  function prev() { if (idx > 0) { idx--; render(); } }

  prevBtn.addEventListener('click', prev);
  nextBtn.addEventListener('click', next);

  document.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') { e.preventDefault(); next(); }
    else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); prev(); }
    else if (e.key === 'Home') { goTo(0); }
    else if (e.key === 'End') { goTo(slides.length - 1); }
    else if (e.key === 'f' || e.key === 'F') { toggleFullscreen(); }
    else if (e.key === 'Escape' && document.fullscreenElement) { document.exitFullscreen(); }
  });

  var touchStartX = null;
  document.addEventListener('touchstart', function (e) { touchStartX = e.changedTouches[0].clientX; }, { passive: true });
  document.addEventListener('touchend', function (e) {
    if (touchStartX === null) return;
    var dx = e.changedTouches[0].clientX - touchStartX;
    if (Math.abs(dx) > 50) { dx < 0 ? next() : prev(); }
    touchStartX = null;
  }, { passive: true });

  track.addEventListener('click', function (e) {
    var rect = track.getBoundingClientRect();
    var ratio = (e.clientX - rect.left) / rect.width;
    goTo(Math.round(ratio * (slides.length - 1)));
  });

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      (document.documentElement.requestFullscreen || function () {}).call(document.documentElement);
    } else {
      document.exitFullscreen();
    }
  }
  fsBtn.addEventListener('click', toggleFullscreen);

  function scaleStage() {
    var scale = Math.min(window.innerWidth / {{CANVAS_W}}, window.innerHeight / {{CANVAS_H}});
    stage.style.transform = 'scale(' + scale + ')';
  }
  window.addEventListener('resize', scaleStage);
  scaleStage();

  var hintTimer = setTimeout(function () { hint.style.opacity = '0'; }, 4000);
  document.addEventListener('mousemove', function () {
    hint.style.opacity = '1';
    clearTimeout(hintTimer);
    hintTimer = setTimeout(function () { hint.style.opacity = '0'; }, 4000);
  });

  render();
})();
</script>

</body>
</html>
```

Fill in `{{...}}` placeholders once (title, fonts URL, canvas size, accent color, slide count,
slide id list), then write one `<section id="..." class="slide" style="...">` per slide inside
`#stage`, in the same order as `slideIds`. Each slide's inline `style` sets its own background/
text color per the palette; the shared CSS above only handles positioning and the shell chrome.

If Extras (Step 3F) were requested, add them now: page numbers as an absolutely-positioned `<p>`
inside each slide; speaker notes as a `<div class="notes" hidden>` per slide plus a couple of
lines of JS toggling on `N`; a print stylesheet as an `@media print` block; a logo as a fixed
`<img>` or inline `<svg>` positioned the same on every slide.

## Step 6 — Verify before delivering

Never skip this. Render the file headlessly (Playwright/Puppeteer — check what's available in
this environment) and for every slide:

1. Toggle it `.active` (with transitions disabled) and confirm no child element's bounding box
   extends past the canvas edges — this catches overflow before the user ever sees it.
2. Take a screenshot and look at it — check line wrapping, color contrast, and that nothing
   looks cramped or oddly empty.

A rough Node/Playwright snippet:

```js
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: {{CANVAS_W}}, height: {{CANVAS_H}} } });
  await page.goto('file://' + process.cwd() + '/deck.html');
  const ids = [/* same slideIds array */];
  for (const id of ids) {
    const overflow = await page.evaluate((id) => {
      const el = document.getElementById(id);
      let maxRight = 0, maxBottom = 0;
      el.querySelectorAll('*').forEach(c => {
        const r = c.getBoundingClientRect();
        maxRight = Math.max(maxRight, r.right);
        maxBottom = Math.max(maxBottom, r.bottom);
      });
      return { maxRight, maxBottom };
    }, id);
    console.log(id, overflow); // flag anything past {{CANVAS_W}} / {{CANVAS_H}}
  }
  await browser.close();
})();
```

Fix any slide that overflows (shrink type, tighten spacing, or split into two slides) and
re-check before moving on.

## Step 7 — Deliver

Save as `<slug-of-title>.html` in the working directory (or wherever the user asked). Tell them
the file path, a one-line summary of what's in it, and — only if they customized — a one-line
reminder of what's different from the built-in default. Don't repeat the whole outline back;
they can open the file.
