from PIL import Image
import os

input_dir = r"d:\11test"
output_dir = os.path.join(input_dir, "cropped")
os.makedirs(output_dir, exist_ok=True)

images = ["median_filter_result.png", "screenshot1.png", "screenshot2.png"]

for filename in images:
    img_path = os.path.join(input_dir, filename)
    img = Image.open(img_path)
    w, h = img.size
    left_half = img.crop((0, 0, w // 2, h))
    out_path = os.path.join(output_dir, filename)
    left_half.save(out_path)
    print(f"{filename}: {w}x{h} -> {w//2}x{h} -> {out_path}")

print("完成！")
