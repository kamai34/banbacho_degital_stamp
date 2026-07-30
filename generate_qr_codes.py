"""各店舗に配置する印刷用 QR コード画像を qrcodes/ に生成するスクリプト。
stores.py の secret を変更した場合はこのスクリプトを再実行すること。
"""

from pathlib import Path

import qrcode

from qr_token import make_token
from stores import STORES

OUT_DIR = Path(__file__).parent / "qrcodes"
OUT_DIR.mkdir(exist_ok=True)

for store in STORES:
    token = make_token(store["id"], store["secret"])
    img = qrcode.make(token)
    out_path = OUT_DIR / f"{store['id']}.png"
    img.save(out_path)
    print(f"generated: {out_path}  (token: {token})")
