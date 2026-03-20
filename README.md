<div style="font-family: Arial, sans-serif; max-width: 900px; margin: auto; line-height: 1.6; padding: 20px;">

<h1>🌞 Solar Image Tools</h1>

<p>A lightweight collection of Python utilities for <b>solar astrophotography workflows</b>.</p>

<ul>
<li>📸 Add detailed labels to images</li>
<li>🟥 Draw annotated bounding boxes</li>
<li>📏 Calculate pixel scale in heliographic coordinates</li>
</ul>

<hr>

<h2>📁 Project Structure</h2>

<pre style="background:#f4f4f4; padding:10px;">
project/

├── saveLabelOnImage.py
├── drawRects.py
├── pixelCalc.py

├── resources/
│   ├── in/
│   └── out/
</pre>

<hr>

<h2>⚙️ Requirements</h2>

<ul>
<li>Python 3.10+</li>
<li>Pillow</li>
<li>NumPy</li>
</ul>

<pre style="background:#f4f4f4; padding:10px;">pip install pillow numpy</pre>

<hr>

<h2>📸 saveLabelOnImage.py</h2>

<p>Adds a <b>multi-line label</b> (UTC timestamp + equipment info) to an image.</p>

<h3>Usage</h3>

<pre style="background:#f4f4f4; padding:10px;">
generateImage("in3", "2026-01-17 12:34")
</pre>

<h3>Output</h3>

<pre style="background:#f4f4f4; padding:10px;">
resources/out/YYYY-MM-DD_HH-MM-SS_UTC.jpeg
</pre>

<h3>Example Label</h3>

<pre style="background:#f4f4f4; padding:10px;">
Bartlomiej Bielecki | Sun | WL
2026-01-17 12:34:00 UTC
Sky-Watcher 90/900 | ZWO ASI 462MM | IR-cut
FireCapture | AutoStakkert! | ImPPG
</pre>

<hr>

<h2>🟥 drawRects.py</h2>

<p>Draws <b>rectangles with labels</b> on images.</p>

<h3>Usage</h3>

<pre style="background:#f4f4f4; padding:10px;">
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
<li><b>saveFlag=True</b> → saves image</li>
<li><b>saveFlag=False</b> → preview only</li>
</ul>

<hr>

<h2>📏 pixelCalc.py</h2>

<p>Calculates <b>pixel scale in heliographic coordinates</b>.</p>

<h3>Usage</h3>

<pre style="background:#f4f4f4; padding:10px;">
result = px_per_helio_degree(
    90, 900, 2.9,
    B_deg=-5,
    L_deg=-21
)

print(result["px_per_deg_corrected"])
</pre>

<hr>

<h2>🧠 Design Philosophy</h2>

<ul>
<li>Minimal dependencies</li>
<li>Clear structure</li>
<li>Windows-friendly</li>
<li>Real workflow focus</li>
</ul>

<hr>

<h2>👨‍🔬 Author</h2>

<p><b>Bartlomiej Bielecki</b><br>
Solar astrophotography tools</p>

</div>