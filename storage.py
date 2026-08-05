from streamlit_local_storage import LocalStorage

_KEY = "manbacho_stamps"
_AGE_SURVEY_KEY = "manbacho_age_survey_done"


def _storage() -> LocalStorage:
    # LocalStorage() は自身の内部で st.session_state を見て、セッションごとに
    # ブラウザとの getAll 往復を1回だけ行うようキャッシュしている。そのため
    # モジュールレベルでインスタンス化して使い回す（＝全セッションで共有される）
    # のではなく、呼び出しのたびに生成してこの仕組みに任せる必要がある。
    return LocalStorage()


def load_stamps() -> set[str]:
    raw = _storage().getItem(_KEY)
    if not raw:
        return set()
    return {x for x in raw.split(",") if x}


def save_stamps(stamps: set[str]) -> None:
    _storage().setItem(_KEY, ",".join(sorted(stamps)))


def load_age_survey_done() -> bool:
    return _storage().getItem(_AGE_SURVEY_KEY) == "1"


def save_age_survey_done() -> None:
    _storage().setItem(_AGE_SURVEY_KEY, "1")
