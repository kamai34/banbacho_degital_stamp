from streamlit_local_storage import LocalStorage

_KEY = "manbacho_stamps"
_local_storage = LocalStorage()


def load_stamps() -> set[str]:
    raw = _local_storage.getItem(_KEY)
    if not raw:
        return set()
    return {x for x in raw.split(",") if x}


def save_stamps(stamps: set[str]) -> None:
    _local_storage.setItem(_KEY, ",".join(sorted(stamps)))
