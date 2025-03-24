from PIL import Image, ImageFont, ImageDraw
#from sheet_API import fixed_name
from bidi.algorithm import get_display
import os
#Names = fixed_name

workshop_name = "Backend_Development_Workshop"
Names = ["Abdallah Almuflah", "Sara Ali", "Mohammed Alrashid", "Lina F", "Ali K."]
filename = os.getenv("certificate_path")

img = Image.open(filename)
draw = ImageDraw.Draw(img)

center_x = 600
center_y = 600
font_path = "C:\\Windows\\Fonts\\times.ttf"  
font = ImageFont.truetype(font_path, 100)  

base_dir = "C:\\Users\\Abdallah\\Desktop\\teeeest"
output_dir = os.path.join(base_dir, f"{workshop_name}")
os.makedirs(output_dir, exist_ok=True)

for i in Names:
    img = Image.open(filename)
    draw = ImageDraw.Draw(img)
    img_width, img_height = img.size

    bbox = draw.textbbox((0, 0), i, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (img_width - text_width) // 2
    y = 600  

    draw.text((x, y), i, font=font, fill="black")
    output_path = os.path.join(output_dir, f"{i}_certificate.pdf")
    img.convert("RGB").save(output_path)
    print(f"Saved: {output_path}")

