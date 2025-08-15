from __future__ import annotations

import html
from typing import Optional

import streamlit as st


def inject_seo(
    title: str,
    description: str,
    image_url: Optional[str] = None,
    theme_color: str = "#0F1115",
) -> None:
    """Inject basic meta tags into Streamlit via HTML."""
    desc = html.escape(description[:300])
    img_tag = f'<meta property="og:image" content="{image_url}"/>' if image_url else ""
    st.markdown(
        f"""
        <meta name="description" content="{desc}">
        <meta property="og:title" content="{html.escape(title)}">
        <meta property="og:description" content="{desc}">
        {img_tag}
        <meta name="theme-color" content="{theme_color}">
        """,
        unsafe_allow_html=True,
    )
