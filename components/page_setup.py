"""Shared page helpers — CSS injection and page config."""

import pathlib
import streamlit as st

_CSS_PATH = pathlib.Path(__file__).resolve().parent.parent / "assets" / "style.css"


def setup_page(title: str, icon: str = "🤖"):
    """Standard page setup: wide layout, title, inject custom CSS."""
    st.set_page_config(page_title=title, page_icon=icon, layout="wide")
    _inject_css()


def inject_css():
    """Inject custom CSS (call once per page render)."""
    _inject_css()


def _inject_css():
    if _CSS_PATH.exists():
        css = _CSS_PATH.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
