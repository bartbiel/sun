import os
import cv2
import numpy as np

# ===== FILE SETTINGS =====
BASENAME = "in2"                          # Input filename without extension
EXTENSIONS = ["jpg", "jpeg", "png"]      # Allowed input extensions

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "resources", "in")
OUTPUT_DIR = os.path.join(BASE_DIR, "resources", "out")

# ===== GRID SETTINGS =====
GRID_STEP_DEG = 10                        # Grid spacing in degrees
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


def detect_solar_disk(gray):
    """
    Robust solar disk detection using threshold + contour.
    Works well for WL / H-alpha solar images.
    """

    # Smooth image to reduce noise
    blur = cv2.GaussianBlur(gray, (11, 11), 0)

    # Adaptive threshold (Sun is the brightest object)
    _, thresh = cv2.threshold(
        blur,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # Morphological cleanup
    kernel = np.ones((7, 7), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Find contours
    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        raise RuntimeError("No contours found – cannot detect solar disk")

    # Select the largest contour (solar disk)
    largest = max(contours, key=cv2.contourArea)

    (cx, cy), radius = cv2.minEnclosingCircle(largest)

    return int(cx), int(cy), int(radius)



def draw_heliographic_grid(img, cx, cy, r, step_deg):
    """Draw heliographic latitude and longitude grid."""
    h, w = img.shape[:2]

    # Longitudes (vertical ellipses)
    for lon in range(-90, 91, step_deg):
        theta = np.deg2rad(lon)
        pts = []
        for lat in np.linspace(-90, 90, 361):
            lat_r = np.deg2rad(lat)
            x = r * np.cos(lat_r) * np.sin(theta)
            y = r * np.sin(lat_r)
            pts.append((int(cx + x), int(cy - y)))

        cv2.polylines(img, [np.array(pts)], False, (0, 255, 0), 1)

    # Latitudes (horizontal ellipses)
    for lat in range(-80, 81, step_deg):
        lat_r = np.deg2rad(lat)
        pts = []
        for lon in np.linspace(-90, 90, 361):
            lon_r = np.deg2rad(lon)
            x = r * np.cos(lat_r) * np.sin(lon_r)
            y = r * np.sin(lat_r)
            pts.append((int(cx + x), int(cy - y)))

        cv2.polylines(img, [np.array(pts)], False, (0, 255, 0), 1)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    input_path = find_input_image(INPUT_DIR, BASENAME, EXTENSIONS)
    output_path = os.path.join(OUTPUT_DIR, f"{BASENAME}_grid.jpg")

    img = cv2.imread(input_path)
    if img is None:
        raise RuntimeError("Failed to load image")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cx, cy, r = detect_solar_disk(gray)
    draw_heliographic_grid(img, cx, cy, r, GRID_STEP_DEG)

    cv2.imwrite(output_path, img)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()