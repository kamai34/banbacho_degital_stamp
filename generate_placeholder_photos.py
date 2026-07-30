"""実際の店舗・オーナー写真を用意するまでの仮画像を assets/ に生成するスクリプト。
写真が揃ったら同名のファイルを差し替えるだけで良い。
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from stores import STORES

ASSETS_DIR = Path(__file__).parent / "assets"
ASSETS_DIR.mkdir(exist_ok=True)

COLORS = ["#F2C14E", "#5B8C5A", "#4E7AC7", "#C75B5B", "#8C5AA8", "#5AA8A0"]

for i, store in enumerate(STORES):
    img = Image.new("RGB", (800, 500), COLORS[i % len(COLORS)])
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", 60)
    except OSError:
        font = ImageFont.load_default()
    text = store["name"]
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(
        ((800 - w) / 2, (500 - h) / 2 - bbox[1]),
        text,
        fill="white",
        font=font,
    )
    out_path = ASSETS_DIR / Path(store["photo"]).name
    img.save(out_path)
    print(f"generated: {out_path}")
