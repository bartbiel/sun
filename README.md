<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Solar Image Tools</title>
<style>
    body {
        font-family: Arial, sans-serif;
        max-width: 900px;
        margin: auto;
        line-height: 1.6;
        padding: 20px;
    }
    code, pre {
        background: #f4f4f4;
        padding: 5px;
        display: block;
        overflow-x: auto;
    }
    h1, h2, h3 {
        border-bottom: 1px solid #ddd;
        padding-bottom: 5px;
    }
</style>
</head>

<body>

<h1>🌞 Solar Image Tools</h1>

<p>A small collection of Python utilities for <strong>solar astrophotography workflows</strong>, including:</p>

<ul>
<li>📸 Adding detailed labels to images</li>
<li>📦 Drawing annotated bounding boxes</li>
<li>📏 Calculating pixel scale in heliographic coordinates</li>
</ul>

<hr>

<h2>📁 Project Structure</h2>

<pre>
project/

├── saveLabelOnImage.py   # Add metadata label to images
├── drawRects.py          # Draw rectangles with labels
├── pixelCalc.py          # Solar pixel scale calculator

├── resources/
│   ├── in/               # Input images
│   └── out/              # Output images
</pre>

<hr>

<h2>⚙️ Requirements</h2>

<ul>
<li>Python 3.10+</li>
<li>Pillow</li>
<li>NumPy</li>
</ul>

<pre>pip install pillow numpy</pre>

<hr>

<h2>📸 saveLabelOnImage.py</h2>

<h3>Purpose</h3>
<p>Adds a <strong>multi-line label</strong> (including UTC timestamp and equipment info) to an image.</p>

<h3>Features</h3>
<ul>
<li>Automatic font scaling</li>
<li>Multi-line text support</li>
<li>Shadow for readability</li>
<li>Fixed UTC input</li>
<li>High-quality JPEG output</li>
</ul>

<h3>Usage</h3>

<pre>
generateImage("in3", "2026-01-17 12:34")
</pre>

<h3>Input</h3>
<pre>resources/in/</pre>

<h3>Output</h3>
<pre>resources/out/YYYY-MM-DD_HH-MM-SS_UTC.jpeg</pre>

<h3>Label Example</h3>

<pre>
Bartlomiej Bielecki | Sun | WL
2026-01-17 12:34:00 UTC
Sky-Watcher 90/900 | ZWO ASI 462MM | IR-cut
FireCapture | AutoStakkert! | ImPPG
</pre>

<hr>

<h2>🟥 drawRects.py</h2>

<h3>Purpose</h3>
<p>Draws <strong>rectangles with labels</strong> on images.</p>

<h3>Features</h3>
<ul>
<li>Multiple bounding boxes</li>
<li>Custom colors and thickness</li>
<li>Text above rectangle</li>
<li>Shadow for readability</li>
<li>Preview or save mode</li>
</ul>

<h3>Input Format</h3>

<pre>
boxes = [
    {"bbox": (x1, y1, x2, y2), "text": "Label"}
]
</pre>

<h3>Usage</h3>

<pre>
process_image(
    filename="1903X",
    boxes=boxes,
    line_thickness=4,
    line_color=(255, 0, 0),
    text_color=(255, 0, 0),
    font_size=24,
    saveFlag=True
)
</pre>

<h3>Output Behavior</h3>

<ul>
<li><strong>saveFlag=True</strong> → saves to resources/in/</li>
<li><strong>saveFlag=False</strong> → displays image only</li>
</ul>

<hr>

<h2>📏 pixelCalc.py</h2>

<h3>Purpose</h3>
<p>Calculates <strong>pixel scale in heliographic coordinates</strong>.</p>

<h3>Calculations</h3>

<ul>
<li>arcsec per pixel</li>
<li>pixels per heliographic degree (center)</li>
<li>projection-corrected pixels</li>
</ul>

<h3>Usage</h3>

<pre>
result = px_per_helio_degree(
    90, 900, 2.9,
    B_deg=-5,
    L_deg=-21
)

print(result["px_per_deg_corrected"])
</pre>

<h3>Notes</h3>

<ul>
<li>B (latitude): South = negative</li>
<li>L (longitude): East (left side) = negative</li>
</ul>

<hr>

<h2>🧠 Design Philosophy</h2>

<ul>
<li>Minimal dependencies</li>
<li>Clear structure</li>
<li>Windows-friendly</li>
<li>Focused on real workflow</li>
</ul>

<hr>

<h2>🚀 Possible Extensions</h2>

<ul>
<li>Batch processing</li>
<li>JSON/CSV box import</li>
<li>Auto font scaling</li>
<li>YOLO/OpenCV integration</li>
</ul>

<hr>

<h2>👨‍🔬 Author</h2>

<p>Bartlomiej Bielecki<br>
Solar astrophotography tools</p>

</body>
</html>