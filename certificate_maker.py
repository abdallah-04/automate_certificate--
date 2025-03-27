from PIL import Image, ImageFont, ImageDraw
from bidi.algorithm import get_display
import os
def make_certificates(Names,output_dir):
    filename = os.getenv("certificate_path")

    img = Image.open(filename)
    draw = ImageDraw.Draw(img)

    center_x = 600
    center_y = 600
    font_path = os.getenv("FONT_PATH")
    font = ImageFont.truetype(font_path, 100)  

    os.makedirs(output_dir, exist_ok=True)

    for name in Names:
        img = Image.open(filename)
        draw = ImageDraw.Draw(img)
        img_width, img_height = img.size
        bbox = draw.textbbox((0, 0), name, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (img_width - text_width) // 2
        y = 600  

        draw.text((x, y), name, font=font, fill="black")
        output_path = os.path.join(output_dir, f"{name}_certificate.pdf")
        img.convert("RGB").save(output_path)
        print(f"Saved: {output_path}")

