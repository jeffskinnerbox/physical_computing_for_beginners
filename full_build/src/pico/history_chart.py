# class-6-code-2.py -- save as history_chart.py; code.py does `import history_chart`
# Stretch 2: add a rolling-history chart to the rover website already running
# since Class 3. Reuses rover_server's `server` object -- no new WiFi join, no
# new adafruit_httpserver instance. This file only appends a small history
# section to the existing status page's HTML.

import rover_server  # Classes 3-5's website; server/scan_status already exist

CHART_PAGE_ADDITION = """
<h2>Recent History</h2>
<canvas id="hist" width="600" height="200" style="border:1px solid #333"></canvas>
<script>
let history = [];
async function pollHistory() {
    const r = await fetch('/data.json');   // same route Classes 3-5 already serve
    const d = await r.json();
    history.push(d);
    if (history.length > 150) history.shift();  // rolling ~150-sample window
    const canvas = document.getElementById('hist');
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawSeries(ctx, canvas, history, p => p.roll, 2, 'orange');    // IMU tilt
    drawSeries(ctx, canvas, history, p => p.pitch, 2, 'blue');     // IMU tilt
    drawSeries(ctx, canvas, history, p => p.heading - 180, 0.5, 'purple');  // compass, 0-360 centered
    drawSeries(ctx, canvas, history, p => p.speed_left_cms, 10, 'green');  // wheel speed
    setTimeout(pollHistory, 200);
}
function drawSeries(ctx, canvas, hist, getValue, scale, color) {
    ctx.strokeStyle = color;
    ctx.beginPath();
    hist.forEach((p, i) => {
        const x = i * (canvas.width / 150);
        const y = canvas.height / 2 - getValue(p) * scale;
        i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    });
    ctx.stroke();
}
pollHistory();
</script>
"""

# Append CHART_PAGE_ADDITION into rover_server.STATUS_PAGE's existing HTML
# (before the closing </body> tag) rather than replacing the whole page, so
# the wheel-speed/orientation/scan-state numbers Classes 3-5 already show
# keep displaying above the new chart.
rover_server.STATUS_PAGE = rover_server.STATUS_PAGE.replace(
    "</body>", CHART_PAGE_ADDITION + "</body>"
)

# No new route is needed: rover_server's existing "/" handler looks up
# STATUS_PAGE each time a browser asks, so it serves the edited page from now on.
# No new main loop, no new server.start(), no new server.poll() loop here --
# class-5-code.py's (or class-6-code-1.py's, if merged) existing main loop
# already calls rover_server.server.poll() every cycle.
