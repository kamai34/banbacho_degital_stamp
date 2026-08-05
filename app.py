import time

import streamlit as st
from streamlit_local_storage import LocalStorage

import analytics
from qr_scanner_component import qr_scanner
from qr_token import parse_token
from stores import STORES

AGE_GROUPS = ["10代以下", "20代", "30代", "40代", "50代", "60代以上"]

_STAMPS_KEY = "manbacho_stamps"
_AGE_SURVEY_KEY = "manbacho_age_survey_done"


def _storage() -> LocalStorage:
    # LocalStorage() は自身の内部で st.session_state を見て、セッションごとに
    # ブラウザとの getAll 往復を1回だけ行うようキャッシュしている。そのため
    # モジュールレベルでインスタンス化して使い回す（＝全セッションで共有される）
    # のではなく、呼び出しのたびに生成してこの仕組みに任せる必要がある。
    return LocalStorage()


def load_stamps() -> set[str]:
    raw = _storage().getItem(_STAMPS_KEY)
    if not raw:
        return set()
    return {x for x in raw.split(",") if x}


def save_stamps(stamps: set[str]) -> None:
    _storage().setItem(_STAMPS_KEY, ",".join(sorted(stamps)))


def load_age_survey_done() -> bool:
    return _storage().getItem(_AGE_SURVEY_KEY) == "1"


def save_age_survey_done() -> None:
    _storage().setItem(_AGE_SURVEY_KEY, "1")

st.set_page_config(
    page_title="万場町まちなかスタンプラリー",
    page_icon="🏮",
    layout="centered",
)

# --- 初期化 -----------------------------------------------------------
# local storage からの読み出しはブラウザとの往復が必要なため、セッション開始直後の
# 数回は空の値しか返らないことがある（ライブラリ既知の挙動）。読み込めた分は
# 都度合算しつつ、数回リトライしてから値を確定させる。
if "stamps" not in st.session_state:
    st.session_state.stamps = set()
    st.session_state.age_survey_done = False
    st.session_state.stamps_load_attempts = 0

if st.session_state.stamps_load_attempts < 3:
    st.session_state.stamps |= load_stamps()
    if load_age_survey_done():
        st.session_state.age_survey_done = True
    st.session_state.stamps_load_attempts += 1
    st.rerun()

# save_stamps() の書き込みはブラウザ側の実行を待たない fire-and-forget のため、
# 1回呼んだ直後に画面を作り直すと、コンポーネントが実際に localStorage へ
# 書き込む前に消えてしまうことがある。読み込み側と同様に、複数回の再実行に
# わたって呼び直すことで書き込みが反映される猶予を作る。
st.session_state.setdefault("pending_saves", 0)
if st.session_state.pending_saves > 0:
    save_stamps(st.session_state.stamps)
    if st.session_state.age_survey_done:
        save_age_survey_done()
    st.session_state.pending_saves -= 1
    if st.session_state.pending_saves > 0:
        time.sleep(0.3)
        st.rerun()

# --- 年代アンケート（端末ごとに初回アクセス時1回だけ） -----------------------
if not st.session_state.age_survey_done:
    st.caption("SHINJO・MANBACHO")
    st.title("万場町まちなかスタンプラリー")
    st.write("ようこそ！差し支えなければ、年代を教えてください（任意・今後の企画の参考にします）")

    chosen = None
    cols = st.columns(3)
    for i, age_group in enumerate(AGE_GROUPS):
        with cols[i % 3]:
            if st.button(age_group, key=f"age_{age_group}", use_container_width=True):
                chosen = age_group

    skip = st.button("答えない", use_container_width=True)

    if chosen or skip:
        analytics.log_access(chosen or "未回答")
        st.session_state.age_survey_done = True
        st.session_state.pending_saves = 3
        st.rerun()

    st.stop()

st.session_state.setdefault("view", "list")
st.session_state.setdefault("selected_store", None)


def go_list():
    st.session_state.view = "list"
    st.session_state.selected_store = None


def go_detail(store_id: str):
    st.session_state.view = "detail"
    st.session_state.selected_store = store_id


def tile_css(store: dict, got: bool) -> str:
    a, b = store["accent"]
    ring = "0 0 0 3px #C9A24B, 0 6px 16px rgba(38,52,74,.18)" if got else "0 4px 10px rgba(38,52,74,.12)"
    opacity = "1" if got else ".8"
    return f"""
    <style>
    .st-key-tile_{store['id']} button {{
        background: linear-gradient(135deg, {a}, {b}) !important;
        color: #fff !important;
        aspect-ratio: 1 / 1;
        font-size: 15px !important;
        font-weight: 700 !important;
        box-shadow: {ring};
        opacity: {opacity};
    }}
    </style>
    """


def stamp_frame_html(store: dict, got: bool) -> str:
    if got:
        label = store["name"][:2]
        return f"""
        <div style="width:150px;height:150px;margin:14px auto;border-radius:50%;
        border:5px solid #BD4A34;display:flex;align-items:center;justify-content:center;
        flex-direction:column;font-family:'Shippori Mincho',serif;font-weight:700;
        color:#BD4A34;background:#FFFDF8;">
          <span style="font-size:28px;">{store['icon']}</span>
          <span style="font-size:14px;margin-top:2px;">{label}</span>
          <span style="font-size:10px;letter-spacing:.05em;margin-top:2px;">獲得済み</span>
        </div>
        """
    return """
    <div style="width:150px;height:150px;margin:14px auto;border-radius:50%;
    border:3px dashed #D8CFBC;display:flex;align-items:center;justify-content:center;
    font-size:12px;color:#9C9587;text-align:center;padding:0 24px;line-height:1.6;">
      ここにスタンプが<br>押されます
    </div>
    """


# --- 画面 ---------------------------------------------------------------
st.caption("SHINJO・MANBACHO")
st.title("万場町まちなかスタンプラリー")

if st.session_state.view == "list":
    got_count = len(st.session_state.stamps)
    st.progress(got_count / len(STORES))
    st.caption(f"獲得スタンプ　{got_count} / {len(STORES)}")

    if got_count == len(STORES):
        st.success("すべてのスタンプを集めました！おめでとうございます 🎉")

    cols_per_row = 4
    for row_start in range(0, len(STORES), cols_per_row):
        row_stores = STORES[row_start : row_start + cols_per_row]
        cols = st.columns(cols_per_row)
        for col, store in zip(cols, row_stores):
            got = store["id"] in st.session_state.stamps
            with col:
                st.html(tile_css(store, got))
                label = f"{store['icon']}\n\n{store['name']}"
                if st.button(label, key=f"tile_{store['id']}", use_container_width=True):
                    go_detail(store["id"])
                    st.rerun()

else:
    store = next(s for s in STORES if s["id"] == st.session_state.selected_store)
    got = store["id"] in st.session_state.stamps

    if st.button("一覧にもどる", icon=":material/arrow_back:"):
        go_list()
        st.rerun()

    st.subheader(f"{store['icon']} {store['name']}")

    with st.container(border=True):
        st.image(store["photo"], use_container_width=True)
        st.markdown(f"**オーナー**：{store['owner_name']}")
        st.write(store["intro"])

    with st.container(border=True):
        st.markdown("**🗣️ オーナーへの質問**")
        st.write(store["question"])

    st.html(stamp_frame_html(store, got))

    show_key = f"show_scanner_{store['id']}"

    if got:
        st.success("スタンプ獲得済みです ✅")
    else:
        if st.session_state.get(show_key):
            token = qr_scanner(key=f"scan_{store['id']}")
            if token:
                parsed = parse_token(token)
                if (
                    parsed
                    and parsed["store_id"] == store["id"]
                    and parsed["secret"] == store["secret"]
                ):
                    st.session_state.stamps.add(store["id"])
                    st.session_state.pending_saves = 3
                    st.session_state[show_key] = False
                    analytics.log_stamp(store["id"], store["name"])
                    st.success("スタンプを獲得しました！")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("このQRコードはこのお店のものではないようです。もう一度お試しください。")
            if st.button("キャンセル", key=f"cancel_{store['id']}"):
                st.session_state[show_key] = False
                st.rerun()
        else:
            if st.button(
                "カメラを起動してQRを読み取る",
                key=f"btn_{store['id']}",
                type="primary",
                use_container_width=True,
                icon=":material/photo_camera:",
            ):
                st.session_state[show_key] = True
                st.rerun()
            st.caption("お店に設置されたQRコードを画面に映してください")
