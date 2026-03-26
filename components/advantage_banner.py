"""Styled advantage banner component."""

import streamlit as st


def render_advantage(title: str, points: list[str]):
    """Render a MAF advantage callout banner with bullet points."""
    bullets = "".join(f"<li>{p}</li>" for p in points)
    html = f"""
    <div class="advantage-banner">
        <h4>✅ MAF Advantage — {title}</h4>
        <ul>{bullets}</ul>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
