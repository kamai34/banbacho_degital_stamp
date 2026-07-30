import streamlit as st

from qr_scanner_component import qr_scanner
from qr_token import parse_token
from storage import load_stamps, save_stamps
from stores import STORES

st.set_page_config(
    page_title="万場町まちなかスタンプラリー",
    page_icon="🏮",
    layout="centered",
)

# --- 初期化 -----------------------------------------------------------
# local storage からの読み出しは初回レンダリングでは値が返らないことがあるため、
# 1度だけ強制的に再実行して値を確定させる。
if "stamps_ready" not in st.session_state:
    st.session_state.stamps = load_stamps()
    st.session_state.stamps_ready = True
    st.rerun()

st.session_state.setdefault("view", "list")
st.session_state.setdefault("selected_store", None)


def go_list():
    st.session_state.view = "list"
    st.session_state.selected_store = None


def go_detail(store_id: str):
    st.session_state.view = "detail"
    st.session_state.selected_store = store_id


# --- 画面 ---------------------------------------------------------------
st.title("万場町まちなかスタンプラリー")

if st.session_state.view == "list":
    got_count = len(st.session_state.stamps)
    st.caption(f"獲得スタンプ: {got_count} / {len(STORES)}")
    if got_count == len(STORES):
        st.success("すべてのスタンプを集めました！おめでとうございます 🎉")

    for store in STORES:
        got = store["id"] in st.session_state.stamps
        label = f"{'✅' if got else '⬜'}　{store['name']}"
        if st.button(label, key=f"list_{store['id']}", use_container_width=True):
            go_detail(store["id"])
            st.rerun()

else:
    store = next(s for s in STORES if s["id"] == st.session_state.selected_store)

    if st.button("← 一覧にもどる"):
        go_list()
        st.rerun()

    st.subheader(store["name"])
    st.image(store["photo"], use_container_width=True)
    st.markdown(f"**オーナー**：{store['owner_name']}")
    st.write(store["intro"])
    st.info(f"🗣️ オーナーへの質問：{store['question']}")

    st.divider()
    st.markdown("### スタンプ")

    got = store["id"] in st.session_state.stamps
    show_key = f"show_scanner_{store['id']}"

    if got:
        st.success("スタンプ獲得済み ✅")
    else:
        st.write("⬜ 未獲得")

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
                    save_stamps(st.session_state.stamps)
                    st.session_state[show_key] = False
                    st.success("スタンプを獲得しました！")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("このQRコードはこのお店のものではないようです。もう一度お試しください。")
            if st.button("キャンセル", key=f"cancel_{store['id']}"):
                st.session_state[show_key] = False
                st.rerun()
        else:
            if st.button("📷 カメラを起動", key=f"btn_{store['id']}", use_container_width=True):
                st.session_state[show_key] = True
                st.rerun()
