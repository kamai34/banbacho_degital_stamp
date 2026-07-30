PREFIX = "MANBACHO"


def make_token(store_id: str, secret: str) -> str:
    return f"{PREFIX}:{store_id}:{secret}"


def parse_token(token: str):
    parts = (token or "").strip().split(":")
    if len(parts) != 3 or parts[0] != PREFIX:
        return None
    return {"store_id": parts[1], "secret": parts[2]}
