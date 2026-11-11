"""アクセス状況・スタンプ獲得ログを Google スプレッドシートに記録する。

Streamlit の Secrets に以下を設定しておく必要がある（未設定時は記録をスキップし、
本体のスタンプラリー機能には影響しない）。

    analytics_spreadsheet_id = "..."

    [gcp_service_account]
    type = "service_account"
    ...（サービスアカウントの JSON キーの中身をそのまま TOML 化したもの）
"""

from datetime import datetime, timedelta, timezone

import streamlit as st

JST = timezone(timedelta(hours=9))

SHEET_STAMPS = "stamp_log"
SHEET_SURVEY = "survey_responses"

_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


@st.cache_resource
def _client():
    import gspread
    from google.oauth2.service_account import Credentials

    creds = Credentials.from_service_account_info(
        dict(st.secrets["gcp_service_account"]), scopes=_SCOPES
    )
    return gspread.authorize(creds)


@st.cache_resource
def _spreadsheet():
    return _client().open_by_key(st.secrets["analytics_spreadsheet_id"])


def _append_row(sheet_name: str, header: list[str], row: list) -> None:
    try:
        sh = _spreadsheet()
        try:
            ws = sh.worksheet(sheet_name)
        except Exception:
            ws = sh.add_worksheet(title=sheet_name, rows=1000, cols=len(header))
            ws.append_row(header, value_input_option="USER_ENTERED")
        ws.append_row(row, value_input_option="USER_ENTERED")
    except Exception as e:
        # 分析ログの失敗でスタンプラリー本体を止めない（Secrets 未設定のローカル
        # 開発時なども含む）。サーバーログにだけ残す。
        print(f"[analytics] failed to log to '{sheet_name}': {e}")


def log_stamp(store_id: str, store_name: str) -> None:
    now = datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S")
    _append_row(SHEET_STAMPS, ["日時", "店舗ID", "店舗名"], [now, store_id, store_name])


def log_survey(
    gender: str,
    age: str,
    origin: str,
    found_new: str,
    unknown_stores: list[str],
    why_visited: str,
    why_not_visited: str,
    how_known: list[str],
    how_known_other: str,
    comment: str,
    stamped_stores: list[str],
) -> None:
    now = datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S")
    _append_row(
        SHEET_SURVEY,
        [
            "日時",
            "性別",
            "年代",
            "居住地",
            "今まで知らなかったお店に入ったか",
            "知らなかったお店",
            "行った理由",
            "行かなかった理由",
            "認知経路",
            "認知経路その他",
            "感想",
            "本日スタンプを押したお店(自動取得)",
        ],
        [
            now,
            gender,
            age,
            origin,
            found_new,
            "、".join(unknown_stores),
            why_visited,
            why_not_visited,
            "、".join(how_known),
            how_known_other,
            comment,
            "、".join(stamped_stores),
        ],
    )
