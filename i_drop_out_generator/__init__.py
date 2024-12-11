import os
from PIL import Image, ImageDraw, ImageFont

dirnow  = os.path.dirname(os.path.abspath(__file__))
imgdir  = os.path.join(dirnow, "img", "base.png")
fontdir = os.path.join(dirnow, "font", "SourceHanSansSC-VF.ttf")

# 检查资源文件
assert os.path.isfile(imgdir)
assert os.path.isfile(fontdir)

# 找到最大非白色像素
def find_max_x_non_white_pixel(image):
    width, height = image.size
    max_x = -1  # 初始化最大 x 坐标
    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x, y))
            if pixel != (255, 255, 255):  # RGB 白色
                max_x = max(max_x, x)
    return max_x if max_x != -1 else None  # 如果没有非白色像素，返回 None

# 生成一张图片
def generate_text_image(text: str):
    width, height = 1920, 50
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(fontdir, 36)
    position = (0, 0)
    draw.text(position, text, fill="black", font=font)
    xmax = find_max_x_non_white_pixel(image)
    return image.crop((0, 0, xmax, height))

# 底边中点对应位置重叠
def overlay_images(big_image, small_image):
    big_width, big_height = big_image.size
    small_width, small_height = small_image.size
    position_x = (big_width - small_width) // 2
    position_y = big_height - small_height
    ans = big_image.copy()
    ans.paste(small_image, (position_x, position_y), small_image)
    return ans

# 保存生成的图片
def generate_image_and_save(text: str, output_path: str):
    text_image = generate_text_image(text).convert("RGBA")
    base_image = Image.open(imgdir).convert("RGBA")
    outp_image = overlay_images(base_image, text_image)
    outp_image.save(output_path)

__all__ = [
    "generate_image_and_save"
]