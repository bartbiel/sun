#drawHelioCoords
import cv2
import numpy as np
import math

# ================= SETTINGS =================
IMAGE_PATH = "sun.jpeg"     # Input image
OUTPUT_PATH = "sun_grid.jpeg"
GRID_STEP_DEG = 10          # Grid spacing in degrees
# ============================================


def detect_solar_disk(gray):
    """
    Detect solar disk using Hough Circle Transform.
    Returns (cx, cy, r)
    """
    # Blur to suppress granulation / noise
    blur = cv2.GaussianBlur(gray, (9, 9), 1.5)

    # Hough Circle detection
    circles = cv2.HoughCircles(
        blur,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=gray.shape[0] // 2,
        param1=100,
        param2=30,
        minRadius=int(gray.shape[0] * 0.3),
        maxRadius=int(gray.shape[0] * 0.55)
    )

    if circles is None:
        raise RuntimeError("Solar disk not detected")

    circles = np.uint16(np.around(circles))
    cx, cy, r = circles[0][0]
    return cx, cy, r


def heliographic_to_image(lat_deg, lon_deg, cx, cy, r):
    """
    Convert heliographic coordinates (deg) to image coordinates.
    Assumes:
    - B0 = 0°
    - P-angle = 0°
    - orthographic projection
    """
    lat = math.radians(lat_deg)
    lon = math.radians(lon_deg)

    x = r * math.cos(lat) * math.sin(lon)
    y = -r * math.sin(lat)

    return int(cx + x), int(cy + y)


def draw_heliographic_grid(img, cx, cy, r, step):
    """
    Draw heliographic latitude and longitude grid.
    """
    h, w = img.shape[:2]

    # Latitudes
    for lat in range(-90, 91, step):
        points = []
        for lon in range(-90, 91, 1):
            x, y = heliographic_to_image(lat, lon, cx, cy, r)
            if 0 <= x < w and 0 <= y < h:
                points.append((x, y))
        for i in range(len(points) - 1):
            cv2.line(img, points[i], points[i + 1], (0, 255, 0), 1)

    # Longitudes
    for lon in range(-90, 91, step):
        points = []
        for lat in range(-90, 91, 1):
            x, y = heliographic_to_image(lat, lon, cx, cy, r)
            if 0 <= x < w and 0 <= y < h:
                points.append((x, y))
        for i in range(len(points) - 1):
            cv2.line(img, points[i], points[i + 1], (0, 255, 0), 1)


def main():
    img = cv2.imread(IMAGE_PATH)
    if img is None:
        raise FileNotFoundError("Cannot load image")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect solar disk
    cx, cy, r = detect_solar_disk(gray)
    print(f"Solar disk: center=({cx},{cy}), radius={r}px")

    # Draw disk outline
    cv2.circle(img, (cx, cy), r, (255, 0, 0), 2)
    cv2.circle(img, (cx, cy), 3, (0, 0, 255), -1)

    # Draw heliographic grid
    draw_heliographic_grid(img, cx, cy, r, GRID_STEP_DEG)

    cv2.imwrite(OUTPUT_PATH, img)
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
