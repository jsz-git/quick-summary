#!/usr/bin/env python3
"""
生成应用 Logo
"""
from PIL import Image, ImageDraw, ImageFont
import os

# 创建图标目录
os.makedirs("icons", exist_ok=True)

# 定义图标尺寸
sizes = [
    (32, 32),
    (128, 128),
    (256, 256),
    (512, 512),
    (1024, 1024)
]

for width, height in sizes:
    # 创建图像
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 绘制渐变背景
    for y in range(height):
        r = int(102 + (y / height) * 56)
        g = int(126 - (y / height) * 30)
        b = int(234 - (y / height) * 84)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # 绘制圆形背景
    margin = width // 10
    draw.ellipse(
        [margin, margin, width - margin, height - margin],
        fill=(255, 255, 255, 240)
    )

    # 绘制笔记图标
    center_x = width // 2
    center_y = height // 2
    note_size = width // 3

    # 绘制笔记纸张
    note_points = [
        (center_x - note_size, center_y - note_size),
        (center_x + note_size, center_y - note_size),
        (center_x + note_size, center_y + note_size),
        (center_x - note_size, center_y + note_size)
    ]
    draw.polygon(note_points, fill=(102, 126, 234))

    # 绘制笔
    pen_start = (center_x - note_size // 2, center_y + note_size // 2)
    pen_end = (center_x + note_size // 2, center_y - note_size // 2)
    draw.line([pen_start, pen_end], fill=(255, 193, 7), width=width // 20)

    # 绘制总结符号 (闪电)
    lightning_points = [
        (center_x, center_y - note_size // 3),
        (center_x + note_size // 4, center_y),
        (center_x - note_size // 6, center_y),
        (center_x + note_size // 6, center_y + note_size // 3)
    ]
    draw.polygon(lightning_points, fill=(255, 193, 7))

    # 保存图标
    if width == 1024:
        img.save("icons/icon.png")
        print(f"✅ 生成图标: {width}x{height}")
    elif width == 32:
        img.save("icons/32x32.png")
        print(f"✅ 生成图标: {width}x{height}")
    elif width == 128:
        img.save("icons/128x128.png")
        print(f"✅ 生成图标: {width}x{height}")
        img.save("icons/128x128@2x.png")
        print(f"✅ 生成图标: {width}x{height}@2x")

print("\n🎉 所有图标生成完成！")
