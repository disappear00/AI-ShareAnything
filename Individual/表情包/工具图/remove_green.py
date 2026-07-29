"""
移除图片中的所有绿色像素，使其变为透明
用法: python remove_green.py 输入图片路径 [输出图片路径]
"""

import sys
from PIL import Image


def remove_green(input_path, output_path=None, g_threshold=80, g_ratio_r=1.3, g_ratio_b=1.1):
    """
    移除图片中的绿色像素
    
    参数:
        input_path: 输入图片路径
        output_path: 输出图片路径（默认在原文件名后加 _transparent）
        g_threshold: 绿色通道最小值（默认80）
        g_ratio_r: G/R 比率阈值（默认1.3，G需大于R的1.3倍）
        g_ratio_b: G/B 比率阈值（默认1.1，G需大于B的1.1倍）
    
    返回:
        (透明像素数, 总像素数, 透明百分比)
    """
    if output_path is None:
        name, ext = input_path.rsplit('.', 1)
        output_path = f"{name}_transparent.{ext}"
    
    img = Image.open(input_path).convert('RGBA')
    pixels = img.load()
    width, height = img.size
    
    count = 0
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if g > g_threshold and g > r * g_ratio_r and g > b * g_ratio_b:
                pixels[x, y] = (r, g, b, 0)
                count += 1
    
    img.save(output_path)
    total = width * height
    percent = count * 100 / total
    return count, total, percent, output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python remove_green.py 输入图片路径 [输出图片路径]")
        print("示例: python remove_green.py photo.png photo_clean.png")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    count, total, percent, out = remove_green(input_path, output_path)
    print(f"完成！移除 {count} 个绿色像素 ({percent:.1f}%)")
    print(f"保存至: {out}")
