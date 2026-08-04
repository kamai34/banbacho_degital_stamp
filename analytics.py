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

SHEET_ACCESS = "access_log"
SHEET_STAMPS = "stamp_log"

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


def log_access(age_group: str) -> None:
    now = datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S")
    _append_row(SHEET_ACCESS, ["日時", "年代"], [now, age_group])


def log_stamp(store_id: str, store_name: str) -> None:
    now = datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S")
    _append_row(SHEET_STAMPS, ["日時", "店舗ID", "店舗名"], [now, store_id, store_name])
