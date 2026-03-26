"""Syntax-highlighted code block helper."""

import streamlit as st


def render_code(code: str, language: str = "python", title: str | None = None):
    """Render a code block with optional title above it."""
    if title:
        st.markdown(f"**{title}**")
    st.code(code, language=language)
