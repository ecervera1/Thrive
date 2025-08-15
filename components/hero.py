from __future__ import annotations

import streamlit as st


def render_hero(
    headline: str,
    subheadline: str,
    primary_cta_text: str,
    primary_cta_href: str,
    secondary_cta_text: str,
    secondary_cta_href: str,
    accent_hex: str = "#C7A97B",
) -> None:
    """Large hero section with CTAs."""
    st.markdown(
        f"""
        <section class="hero">
            <h1 class="hero-title">{headline}</h1>
            <p class="hero-sub">{subheadline}</p>
            <div class="cta-row">
                <a class="btn btn-primary" href="{primary_cta_href}">{primary_cta_text}</a>
                <a class="btn btn-secondary" href="{secondary_cta_href}">{secondary_cta_text}</a>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
