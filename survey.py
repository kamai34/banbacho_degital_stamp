"""スタンプラリー参加者向けアンケートページ（?page=survey で表示）。"""

import streamlit as st
from streamlit_local_storage import LocalStorage

import analytics
from stores import STORES

AGE_GROUPS = ["10代以下", "20代", "30代", "40代", "50代", "60代", "70代", "80代以上"]
STORE_NAMES = [s["name"] for s in STORES]

_STAMPS_KEY = "manbacho_stamps"


def _stamped_store_names() -> list[str]:
    raw = LocalStorage().getItem(_STAMPS_KEY)
    if not raw:
        return []
    stamped_ids = {x for x in raw.split(",") if x}
    return [s["name"] for s in STORES if s["id"] in stamped_ids]


def render() -> None:
    st.caption("SHINJO・MANBACHO")
    st.title("万場町まちなかスタンプラリー アンケート")

    if st.session_state.get("survey_submitted"):
        st.success("ご回答ありがとうございました！")
        if st.button("スタンプラリーにもどる"):
            st.query_params.clear()
            st.rerun()
        return

    st.write(
        "ご参加いただきありがとうございました。今後の活動のため、"
        "アンケートにご協力いただけると幸いです。"
    )

    stamped_names = _stamped_store_names()

    with st.form("survey_form"):
        st.markdown("**01　性別はなんですか？**")
        gender = st.radio(
            "性別", ["男性", "女性", "回答しない"], index=None, label_visibility="collapsed"
        )

        st.markdown("**02　年齢はなんですか？**")
        age = st.radio(
            "年齢", AGE_GROUPS + ["回答しない"], index=None, label_visibility="collapsed"
        )

        st.markdown("**03　どこからいらっしゃいましたか？**")
        origin = st.radio(
            "居住地",
            ["新庄市内", "山形県内", "その他"],
            index=None,
            label_visibility="collapsed",
        )
        origin_yamagata_detail = st.text_input(
            "具体的に（山形県内を選んだ方）", key="origin_yamagata_detail"
        )
        origin_other = st.text_input("具体的に（その他を選んだ方）", key="origin_other")

        st.markdown("**04　本日スタンプを押したお店にチェックしてください（複数回答可）**")
        stamped_today = st.multiselect(
            "本日スタンプを押したお店",
            ["全店制覇!!"] + STORE_NAMES,
            label_visibility="collapsed",
        )

        st.markdown("**05　今まで知らなかったお店に入りましたか？**")
        found_new = st.radio(
            "新規発見", ["はい", "いいえ"], index=None, label_visibility="collapsed"
        )

        st.markdown("**06　今まで知らなかったお店はどれですか？（複数回答可）**")
        unknown_stores = st.multiselect(
            "知らなかったお店", STORE_NAMES, label_visibility="collapsed"
        )

        st.markdown("**07　行ったお店にはなぜ行ったのですか？**")
        why_visited = st.radio(
            "来店理由",
            ["元々知っていたから", "買いたいものがあったから", "たまたま目についたから", "その他"],
            index=None,
            label_visibility="collapsed",
        )
        why_visited_other = st.text_input("具体的に（その他を選んだ方）", key="why_visited_other")

        st.markdown("**08　行かなかったお店にはなぜ行かなかったのですか？**")
        why_not_visited = st.radio(
            "非来店理由",
            [
                "よく知らなかったから",
                "買いたいものが特になかったから",
                "あまり目につかなかったから",
                "その他",
            ],
            index=None,
            label_visibility="collapsed",
        )
        why_not_visited_other = st.text_input(
            "具体的に（その他を選んだ方）", key="why_not_visited_other"
        )

        st.markdown("**09　どこでこのスタンプラリーを知りましたか？（複数回答可）**")
        how_known = st.multiselect(
            "認知経路",
            ["SNS", "リリースペーパー", "前回のよろず市で", "知人・友人", "教育の日の発表", "その他"],
            label_visibility="collapsed",
        )
        sns_platforms = st.multiselect(
            "SNSの種類（SNSを選んだ方）",
            ["Instagram", "X", "LINE", "TikTok", "Facebook", "setlog", "その他"],
        )
        sns_other = st.text_input("具体的に（SNSのその他を選んだ方）", key="sns_other")
        how_known_other = st.text_input("具体的に（その他を選んだ方）", key="how_known_other")

        st.markdown("**10　スタンプラリーに関する感想、よろず市に関する感想など率直にお願いします！！**")
        comment = st.text_area("感想", label_visibility="collapsed")

        submitted = st.form_submit_button(
            "送信する", type="primary", use_container_width=True
        )

    if submitted:
        if origin == "山形県内" and origin_yamagata_detail:
            origin_resolved = f"山形県内（{origin_yamagata_detail}）"
        elif origin == "その他" and origin_other:
            origin_resolved = f"その他（{origin_other}）"
        else:
            origin_resolved = origin or ""

        try:
            analytics.log_survey(
                gender=gender or "",
                age=age or "",
                origin=origin_resolved,
                stamped_today=stamped_today,
                found_new=found_new or "",
                unknown_stores=unknown_stores,
                why_visited=(
                    why_visited_other
                    if why_visited == "その他" and why_visited_other
                    else why_visited
                )
                or "",
                why_not_visited=(
                    why_not_visited_other
                    if why_not_visited == "その他" and why_not_visited_other
                    else why_not_visited
                )
                or "",
                how_known=how_known,
                sns_platforms=sns_platforms if "SNS" in how_known else [],
                sns_other=sns_other if "SNS" in how_known and "その他" in sns_platforms else "",
                how_known_other=how_known_other if "その他" in how_known else "",
                comment=comment or "",
                stamped_stores_auto=stamped_names,
            )
        except Exception as e:
            # 記録に失敗しても回答自体は受け取ったことにする（送信した人が
            # エラー画面を見て不安にならないようにするため）。原因はサーバー
            # ログに残す。
            print(f"[survey] failed to record response: {e}")
        st.session_state.survey_submitted = True
        st.rerun()
