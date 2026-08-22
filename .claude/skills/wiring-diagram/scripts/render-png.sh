#!/usr/bin/env bash
# Render a static .dc.html diagram artboard to a trimmed PNG.
# Usage: render-png.sh <input.dc.html> <output.png> [content-width-px]
#
# The input must be a static artboard: <helmet><link/><style/></helmet> then
# markup, with no {{holes}}, <sc-for>, <sc-if>, or <dc-import> (this script
# does not run the design-canvas runtime — it renders the markup directly).
set -euo pipefail

IN="$1"
OUT="$2"
WIDTH="${3:-1040}"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

python3 - "$IN" "$TMP/static.html" <<'PYEOF'
import re, sys
src = open(sys.argv[1]).read()
style = re.search(r'<style>(.*?)</style>', src, re.S)
style = style.group(1) if style else ''
font_link = re.search(r'<link rel="stylesheet"[^>]*>', src)
font_link = font_link.group(0) if font_link else ''
body = re.search(r'</helmet>(.*?)</x-dc>', src, re.S).group(1)
out = f"""<!doctype html>
<html><head><meta charset="utf-8">
{font_link}
<style>{style}</style>
</head><body>
{body}
</body></html>"""
open(sys.argv[2], 'w').write(out)
PYEOF

google-chrome --headless --disable-gpu --no-sandbox --hide-scrollbars \
  --force-device-scale-factor=2 --window-size="${WIDTH},1400" \
  --screenshot="$TMP/raw.png" "file://$TMP/static.html" >/dev/null 2>&1

convert "$TMP/raw.png" -fuzz 3% -trim +repage "$OUT"
echo "wrote $OUT"
identify "$OUT"
