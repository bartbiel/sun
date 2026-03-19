# sun
<h1>Dependencies</h1>
<br>Python 3.13.7
<br>python -m pip install [package]
<br>packahes: pillow numpy opencv-python matplotlib astropy sunpy
<h2>Scripts - manual only
<h3>saveLabelOnImage.py</h3>
<br>Save a label on an image (e.g: Author, Equipment, Timestamp)
<h3>pixelCalc.py</h3>
<br>Returns how many pixels corresponds with one heliographic grade
<br>params: aperture_mm, focal_length_mm, pixel_size_um, B_deg, L_deg
<br>S = south → negative
<br>E = east (sun's left side) → negative
<h3>drawRects.py</h3>
<br>Add rectangles to highlight spot and add a label. 
<h3>run.py</h3>
<br>run saveImage script with filename nad UTC data
<h2>Pipeline</h2>
<ol>
<li>Run pixelCalc.py if McIntosh classification is expected
<li>Run drawRects.py if spot rectangles are expected
<li>Run run.py if a label is expected
</ol>
<br>Additional dependences:
<br>Resources catalogs: ./in for incoming images; ./out for the results

