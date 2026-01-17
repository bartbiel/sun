#drawSunPyCoords.py
import datetime
import os
import matplotlib.pyplot as plt
import numpy as np

import astropy.units as u
from astropy.coordinates import SkyCoord

import sunpy.map
from sunpy.coordinates import frames
from datetime import datetime, timezone
from astropy.time import Time


# ===== FILE SETTINGS =====
BASENAME = "in2"                          # Input filename without extension
EXTENSIONS = ["jpg", "jpeg", "png"]      # Allowed input extensions

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "resources", "in")
OUTPUT_DIR = os.path.join(BASE_DIR, "resources", "out")
# =========================
def find_input_image(input_dir, basename, extensions):
    """Find input image with allowed extensions."""
    for ext in extensions:
        path = os.path.join(input_dir, f"{basename}.{ext}")
        if os.path.exists(path):
            return path
    raise FileNotFoundError(
        f"No input file found for '{basename}' with extensions {extensions}"
    )

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    input_path = find_input_image(INPUT_DIR, BASENAME, EXTENSIONS)
    sun_map = sunpy.map.Map(input_path)
    lon_value = 35 * u.deg
    lat_value = 12 * u.deg
    now_utc = datetime.now(timezone.utc)
    t = Time(now_utc)

    stonyhurst_frame = frames.HeliographicStonyhurst(obstime=t)
    point_in_stonyhurst = SkyCoord(lon=lon_value, lat=lat_value, frame=stonyhurst_frame)
    point_in_hpc = point_in_stonyhurst.transform_to(sun_map.coordinate_frame)
    print(point_in_hpc)
    num_points = 100
    constant_lon = SkyCoord(lon_value, np.linspace(-90, 90, num_points) * u.deg,
                            frame=stonyhurst_frame)
    constant_lat = SkyCoord(np.linspace(-90, 90, num_points) * u.deg, lat_value,
                            frame=stonyhurst_frame)
    
    fig = plt.figure()
    ax = fig.add_subplot(projection=sun_map)
    sun_map.plot(axes=ax, clip_interval=(1, 99.99)*u.percent)
    ax.plot_coord(constant_lon, color="lightblue")
    ax.plot_coord(constant_lat, color="tomato")
    ax.plot_coord(point_in_stonyhurst, marker="o")
    sun_map.draw_grid(axes=ax)

    plt.show()

if __name__ == "__main__":
    main()