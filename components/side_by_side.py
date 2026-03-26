"""Reusable side-by-side comparison renderer for MAF vs ADK.

Responsive: on mobile the CSS media query stacks columns vertically.
"""

import streamlit as st


def _render_framework_block(label_class: str, label_text: str, title: str, description: str, code: str, lang: str):
    """Render a single framework block (reused for both MAF and ADK)."""
    st.markdown(
        f'<span class="{label_class}">{label_text}</span>',
        unsafe_allow_html=True,
    )
    st.markdown(f"**{title}**")
    st.markdown(description)
    st.code(code, language=lang)


def render_comparison(
    section_title: str,
    maf_title: str,
    maf_description: str,
    maf_code: str,
    adk_title: str,
    adk_description: str,
    adk_code: str,
    maf_lang: str = "python",
    adk_lang: str = "python",
):
    """Render a side-by-side comparison block for MAF (left) and ADK (right).

    Columns stack vertically on mobile via CSS media queries.
    """
    st.markdown(f"### {section_title}")
    st.markdown("---")

    col_maf, col_adk = st.columns(2)

    with col_maf:
        _render_framework_block(
            "framework-label-maf", "Microsoft Agent Framework",
            maf_title, maf_description, maf_code, maf_lang,
        )

    with col_adk:
        _render_framework_block(
            "framework-label-adk", "Google ADK",
            adk_title, adk_description, adk_code, adk_lang,
        )


def render_comparison_multi(
    section_title: str,
    blocks: list[dict],
):
    """Render multiple side-by-side blocks under one section header.

    Each block dict has keys:
        maf_title, maf_description, maf_code,
        adk_title, adk_description, adk_code,
        maf_lang (optional), adk_lang (optional)
    """
    st.markdown(f"### {section_title}")
    st.markdown("---")

    for block in blocks:
        col_maf, col_adk = st.columns(2)

        with col_maf:
            st.markdown(
                '<span class="framework-label-maf">Microsoft Agent Framework</span>',
                unsafe_allow_html=True,
            )
            st.markdown(f"**{block['maf_title']}**")
            st.markdown(block["maf_description"])
            st.code(block["maf_code"], language=block.get("maf_lang", "python"))

        with col_adk:
            st.markdown(
                '<span class="framework-label-adk">Google ADK</span>',
                unsafe_allow_html=True,
            )
            st.markdown(f"**{block['adk_title']}**")
            st.markdown(block["adk_description"])
            st.code(block["adk_code"], language=block.get("adk_lang", "python"))

        st.markdown("")
