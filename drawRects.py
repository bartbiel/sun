import os
from PIL import Image, ImageDraw, ImageFont


# ===== PATHS =====
EXTENSIONS = ["jpg", "jpeg", "png", "bmp"]      # Allowed input extensions

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "resources", "in")
OUTPUT_DIR = os.path.join(BASE_DIR, "resources", "out")


# ===== HELPERS =====
def load_font(font_size, font_path=None):
    try:
        if font_path:
            return ImageFont.truetype(font_path, font_size)
        return ImageFont.truetype("arial.ttf", font_size)
    except OSError:
        return ImageFont.load_default()


def find_input_image(directory, filename, extensions):
    """
    Accepts:
    - "in3"       → finds matching extension
    - "in3.jpg"   → validates directly
    """

    name, ext = os.path.splitext(filename)

    # --- CASE 1: extension provided ---
    if ext:
        for f in os.listdir(directory):
            if f.lower() == filename.lower():
                return os.path.join(directory, f)

        raise FileNotFoundError(f"File not found: {filename}")

    # --- CASE 2: no extension → search ---
    for ext in extensions:
        for variant in (ext, ext.upper()):
            path = os.path.join(directory, f"{filename}.{variant}")
            if os.path.exists(path):
                return path

    raise FileNotFoundError(
        f"No input file found in:\n{directory}\n"
        f"Expected: {filename}.[{', '.join(extensions)}]"
    )


# ===== MAIN DRAW FUNCTION =====
def draw_boxes_with_labels(
    image,
    boxes,
    line_thickness=3,
    line_color=(255, 0, 0),
    text_color=(255, 255, 255),
    font_size=16,
    font_path=None,
    text_margin=4
):
    draw = ImageDraw.Draw(image)
    font = load_font(font_size, font_path)

    for item in boxes:
        x1, y1, x2, y2 = item["bbox"]
        text = item.get("text", "")

        # --- RECTANGLE ---
        for i in range(line_thickness):
            draw.rectangle(
                [x1 - i, y1 - i, x2 + i, y2 + i],
                outline=line_color
            )

        # --- TEXT ---
        if text:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_height = bbox[3] - bbox[1]

            text_x = x1
            text_y = y1 - text_height - text_margin - 10

            if text_y < 0:
                text_y = y1 + text_margin

            shadow_offset = max(1, font_size // 15)

            draw.text(
                (text_x + shadow_offset, text_y + shadow_offset),
                text,
                font=font,
                fill=(0, 0, 0)
            )

            draw.text(
                (text_x, text_y),
                text,
                font=font,
                fill=text_color
            )

    return image


# ===== PROCESS FUNCTION =====
def process_image(
    filename,
    boxes,
    line_thickness=3,
    line_color=(255, 0, 0),
    text_color=(255, 255, 255),
    font_size=20,
    font_path=None,
    saveFlag=False
):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    input_path = find_input_image(INPUT_DIR, filename, EXTENSIONS)

    img = Image.open(input_path).convert("RGB")

    result = draw_boxes_with_labels(
        img,
        boxes,
        line_thickness=line_thickness,
        line_color=line_color,
        text_color=text_color,
        font_size=font_size,
        font_path=font_path
    )

    name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(INPUT_DIR, f"{name}_boxed.jpg")

    if ( saveFlag == True):
        result.save(output_path, "JPEG", quality=90)

        print("Input :", input_path)
        print("Output:", output_path)
    else:
        result.show()
# ===== EXAMPLE =====
if __name__ == "__main__": boxes = [ 
    {"bbox": (172, 487, 343, 631), "text": "4392"} 
   
    ]

process_image( 
    filename="1903X", 
    boxes=boxes, 
    line_thickness=4, 
    line_color=(255, 0, 0), 
    text_color=(255, 0, 0), 
    font_size=24, 
    saveFlag=True 
    )
