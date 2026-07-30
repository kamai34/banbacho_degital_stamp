from pathlib import Path

import streamlit.components.v1 as components

_FRONTEND_DIR = Path(__file__).parent / "qr_scanner_frontend"
_component = components.declare_component("qr_scanner", path=str(_FRONTEND_DIR))


def qr_scanner(key: str | None = None):
    """Renders a live camera QR scanner. Returns the decoded text once a QR
    code is scanned, otherwise None."""
    return _component(key=key, default=None)
