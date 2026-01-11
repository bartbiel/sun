# Save label on image (Windows-safe, JPEG/PNG input -> JPEG output)
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# ===== FILE SETTINGS =====
BASENAME = "in2"                          # Input filename without extension
EXTENSIONS = ["jpg", "jpeg", "png"]      # Allowed input extensions

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "resources", "in")
OUTPUT_DIR = os.path.join(BASE_DIR, "resources", "out")

# ===== TEXT SETTINGS =====
TEXT_COLOR = (255, 255, 255)             # Text color (RGB)
FONT_PATH = None                         # Optional path to .ttf font
TEXT_HEIGHT_RATIO = 0.022                # Text size relative to image height
MARGIN_RATIO = 0.015                     # Margin relative to image height
# =========================


def find_input_image(directory, basename, extensions):
    """
    Find input image by base name and allowed extensions.
    Example: in.jpg, in.jpeg, in.png
    """
    for ext in extensions:
        for variant in (ext, ext.upper()):
            filename = f"{basename}.{variant}"
            path = os.path.join(directory, filename)
            if os.path.exists(path):
                return path

    raise FileNotFoundError(
        f"No input file found in:\n{directory}\n"
        f"Expected: {basename}.[{', '.join(extensions)}]"
    )


def load_font(font_path, font_size):
    """
    Robust font loading for Windows.
    """
    try:
        if font_path:
            return ImageFont.truetype(font_path, font_size)
        return ImageFont.truetype("arial.ttf", font_size)
    except OSError:
        return ImageFont.load_default()


def generateImage():
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Locate input image
    image_path = find_input_image(INPUT_DIR, BASENAME, EXTENSIONS)
    img = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    # === UTC TIME ===
    now_utc = datetime.utcnow()
    timestamp_text = now_utc.strftime("%Y-%m-%d %H:%M:%S UTC")
    timestamp_file = now_utc.strftime("%Y-%m-%d_%H-%M-%S_UTC")

    # Label text (full UTC timestamp)
    label_text = f"Sun | WL | {timestamp_text}"

    # Scale font and margin to image height
    font_size = int(img.height * TEXT_HEIGHT_RATIO)
    margin = int(img.height * MARGIN_RATIO)

    font = load_font(FONT_PATH, font_size)

    # Measure text size
    bbox = draw.textbbox((0, 0), label_text, font=font)
    text_height = bbox[3] - bbox[1]

    # Bottom-left position
    x = margin
    y = img.height - text_height - margin

    # Shadow for Facebook compression
    shadow_offset = max(1, font_size // 15)
    draw.text(
        (x + shadow_offset, y + shadow_offset),
        label_text,
        font=font,
        fill=(0, 0, 0)
    )

    # Main text
    draw.text(
        (x, y),
        label_text,
        font=font,
        fill=TEXT_COLOR
    )

    # Save output image
    output_path = os.path.join(OUTPUT_DIR, f"{timestamp_file}.jpeg")
    img.save(output_path, "JPEG", quality=90, subsampling=0)

    print("Input image :", image_path)
    print("Output image:", output_path)
    print("UTC label   :", timestamp_text)


