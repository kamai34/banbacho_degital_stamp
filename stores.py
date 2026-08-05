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
        "accent": ("#D98CB3", "#F3C6DC"),
        "icon": "🌸",
    },
    {
        "id": "uoya",
        "name": "魚屋",
        "owner_name": "（オーナー名を入力）",
        "photo": "assets/uoya.png",
        "intro": "（お店の紹介文をここに入力してください）",
        "question": "（オーナーへの質問をここに入力してください）",
        "secret": "HvcWxsSkB8I",
        "accent": ("#6E9B5B", "#B7D69B"),
        "icon": "🐟",
    },
    {
        "id": "soba",
        "name": "蕎麦屋",
        "owner_name": "（オーナー名を入力）",
        "photo": "assets/soba.png",
        "intro": "地元名物の茶そばが自慢のお蕎麦屋さん。（紹介文を入力してください）",
        "question": "（オーナーへの質問をここに入力してください）",
        "secret": "gFSVTEmI_RQ",
        "accent": ("#8A7A6B", "#C6B9A9"),
        "icon": "🍵",
    },
    {
        "id": "kissa_nokurashi",
        "name": "喫茶 のくらし",
        "owner_name": "（吉野優美）",
        "photo": "assets/kissa_nokurashi.png",
        "intro": "普段は和風クレープ喫茶店を営まれていますが、月に1度○○○○専門店として営業されています。また、土日限定で○○○○も振る舞われています。仕立屋さんとして使われていた町家を、カフェやレンタルスペースとして再生することで、当時の記憶をつなぎます。",
        "question": "○の中には何が入るのですか？　なぜこの店を開いたのですか？　最近驚いたことはありますか？",
        "secret": "elYFXgMQQkI",
        "accent": ("#2B4570", "#7FA0C9"),
        "icon": "☕",
    },
]
