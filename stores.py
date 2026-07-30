# 参加店舗データ（サンプル）
# 実運用時は各項目を実際の店舗情報・写真パスに差し替えてください。
# "secret" は QR コード生成・照合に使う秘密文字列です。値を変えたら
# generate_qr_codes.py を再実行して QR 画像も作り直してください。

STORES = [
    {
        "id": "hanaya",
        "name": "花屋",
        "owner_name": "（オーナー名を入力）",
        "photo": "assets/hanaya.png",
        "intro": "（お店の紹介文をここに入力してください。営業時間や取り扱い商品など）",
        "question": "（オーナーへの質問をここに入力してください。例：一番人気の商品は？）",
        "secret": "NzJ71Yp5HH0",
    },
    {
        "id": "uoya",
        "name": "魚屋",
        "owner_name": "（オーナー名を入力）",
        "photo": "assets/uoya.png",
        "intro": "（お店の紹介文をここに入力してください）",
        "question": "（オーナーへの質問をここに入力してください）",
        "secret": "HvcWxsSkB8I",
    },
    {
        "id": "soba",
        "name": "蕎麦屋",
        "owner_name": "（オーナー名を入力）",
        "photo": "assets/soba.png",
        "intro": "地元名物の茶そばが自慢のお蕎麦屋さん。（紹介文を入力してください）",
        "question": "（オーナーへの質問をここに入力してください）",
        "secret": "gFSVTEmI_RQ",
    },
    {
        "id": "kissa_nokurashi",
        "name": "喫茶 のくらし",
        "owner_name": "（オーナー名を入力）",
        "photo": "assets/kissa_nokurashi.png",
        "intro": "コーヒー好きのお母さんが営む喫茶店。（紹介文を入力してください）",
        "question": "（オーナーへの質問をここに入力してください）",
        "secret": "elYFXgMQQkI",
    },
]
