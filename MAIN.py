from PIL import Image, ImageFont, ImageDraw

Names = ["Abdallah Almuflah", "عبدالله المفلح"]
filename = "D:\\my_2projects\\automate_certificate-\\Copy of CERTIFICATE.png"

img = Image.open(filename)
draw = ImageDraw.Draw(img)

font_path = "C:\\Windows\\Fonts\\times.ttf"  
font = ImageFont.truetype(font_path, 100)  
for i in Names:
    img = Image.open(filename)
    draw = ImageDraw.Draw(img)
    draw.text((600, 600), i, font=font, fill="black")
    pdf_filename = f"C:\\Users\\Abdallah\\Desktop\\teeeest\\{i}_certificate.pdf"
    img.convert("RGB").save(pdf_filename)

