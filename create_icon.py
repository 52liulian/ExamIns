from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    icon_size = (256, 256)
    image = Image.new('RGBA', icon_size, (70, 130, 180, 255))
    draw = ImageDraw.Draw(image)
    
    center_x, center_y = icon_size[0] // 2, icon_size[1] // 2
    
    draw.ellipse([center_x - 90, center_y - 90, center_x + 90, center_y + 90], 
                 fill=(255, 255, 255, 255), outline=(255, 255, 255, 255), width=3)
    
    speaker_points = [
        (center_x - 40, center_y - 30),
        (center_x - 40, center_y + 30),
        (center_x - 10, center_y + 50),
        (center_x - 10, center_y - 50)
    ]
    draw.polygon(speaker_points, fill=(70, 130, 180, 255))
    
    for i in range(3):
        radius = 20 + i * 15
        arc_rect = [center_x - 10 + i * 10, center_y - radius, 
                    center_x + 30 + i * 10, center_y + radius]
        draw.arc(arc_rect, start=300, end=60, fill=(255, 255, 255, 255), width=4)
    
    try:
        font = ImageFont.truetype("msyh.ttc", 40)
    except:
        font = ImageFont.load_default()
    
    text = "考试指令"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_x = center_x - text_width // 2
    draw.text((text_x, center_y + 70), text, fill=(255, 255, 255, 255), font=font)
    
    ico_path = os.path.join(os.path.dirname(__file__), "icon.ico")
    image.save(ico_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    
    png_path = os.path.join(os.path.dirname(__file__), "icon.png")
    image.save(png_path, format='PNG')
    
    print(f"图标已创建: {ico_path}")
    print(f"图标已创建: {png_path}")
    
    return ico_path

if __name__ == "__main__":
    create_icon()
