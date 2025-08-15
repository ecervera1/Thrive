#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Landing + Navigation for Thrive with Frida (Streamlit)
Python 3.11+, Streamlit latest
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional

import streamlit as st

from components.hero import render_hero
from components.feature_cards import render_feature_cards
from components.gallery import render_gallery
from services.seo import inject_seo

# ---------- Brand Defaults (override via .streamlit/secrets.toml) ----------
BRAND_NAME: str = st.secrets.get("BRAND_NAME", "Thrive with Frida")
TAGLINE: str = st.secrets.get("TAGLINE", "Simplicity in Motion")
INSTAGRAM_HANDLE: str = st.secrets.get("INSTAGRAM_HANDLE", "@thrivewfrida")
HEX_PRIMARY: str = st.secrets.get("HEX_PRIMARY", "#0F1115")
HEX_ACCENT: str = st.secrets.get("HEX_ACCENT", "#C7A97B")
CITY_REGION: str = st.secrets.get("CITY_REGION", "")
INSTAGRAM_POST_URLS: List[str] = list(st.secrets.get("INSTAGRAM_POST_URLS", []))

# Paths
DATA_DIR = Path("data")
ASSETS_DIR = Path("assets")
SERVICES_JSON = DATA_DIR / "services.json"


def _load_services() -> list[dict]:
    try:
        with SERVICES_JSON.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _instagram_url_from_handle(handle: str) -> Optional[str]:
    h = handle.strip()
    if not h:
        return None
    if h.startswith("@"):
        h = h[1:]
    return f"https://www.instagram.com/{h}/"


def _inject_styles():
    css_path = ASSETS_DIR / "styles.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def main() -> None:
    st.set_page_config(
        page_title=f"{BRAND_NAME} | {TAGLINE}",
        page_icon="🏋️",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    inject_seo(
        title=f"{BRAND_NAME} — {TAGLINE}",
        description="High-performance personal training with a clean, modern approach. Strength and refinement, tailored to your life.",
        image_url=None,
        theme_color=HEX_PRIMARY,
    )

    _inject_styles()

    # --- NAV BAR (very minimal, relies on Streamlit pages) ---
    with st.container():
        col1, col2 = st.columns([1, 6])
        with col1:
            st.image(str(ASSETS_DIR / "logo.png"), caption=None, use_container_width=True)
        with col2:
            st.markdown(
                f"""
                <div class="brand-title">
                    <span class="brand-name">{BRAND_NAME}</span>
                    <span class="brand-tag">{TAGLINE}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()

    # --- HERO ---
    render_hero(
        headline="Strength, Refined.",
        subheadline="Precision coaching for busy, ambitious humans. Minimal noise, maximal results.",
        primary_cta_text="Book a Consultation",
        primary_cta_href="03_Schedule",
        secondary_cta_text="Send an Inquiry",
        secondary_cta_href="04_Inquiry",
        accent_hex=HEX_ACCENT,
    )

    # --- SOCIAL BADGE / INSTAGRAM ---
    insta_url = _instagram_url_from_handle(INSTAGRAM_HANDLE)
    with st.container():
        st.markdown(
            f"""
            <div class="social-badge">
                <a href="{insta_url}" target="_blank" rel="noopener noreferrer" aria-label="Instagram: {INSTAGRAM_HANDLE}">
                    <span class="ig-handle">Instagram {INSTAGRAM_HANDLE}</span>
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if INSTAGRAM_POST_URLS:
            st.caption("Latest from Instagram")
            from streamlit.components.v1 import html  # local import to keep top clean

            # Simple embed of the first post (optional)
            post = INSTAGRAM_POST_URLS[0]
            html(
                f"""
                <blockquote class="instagram-media" data-instgrm-permalink="{post}" data-instgrm-version="14"></blockquote>
                <script async src="//www.instagram.com/embed.js"></script>
                """,
                height=600,
            )
        else:
            st.caption("Tip: add INSTAGRAM_POST_URLS in secrets to embed a post here.")

    st.divider()

    # --- METHODOLOGY ---
    with st.container():
        left, right = st.columns([1, 1], gap="large")
        with left:
            st.markdown("### Simplicity in Motion")
            st.write(
                "We remove the non-essential and focus on what moves the needle. "
                "A structured system that adapts to your schedule, with measurable progress and sustainable intensity."
            )
        with right:
            st.markdown("### Strength + Refinement")
            st.write(
                "We build athletic strength, clean lines, and confident posture. "
                "Training is purposeful, recovery is respected, nutrition is pragmatic."
            )

    st.divider()

    # --- FEATURE CARDS ---
    render_feature_cards(accent_hex=HEX_ACCENT)

    st.divider()

    # --- GALLERY ---
    render_gallery(
        images_dir=ASSETS_DIR / "images",
        instagram_post_urls=INSTAGRAM_POST_URLS,
        max_images=8,
    )

    st.divider()

    # --- FOOTER ---
    footer = f"{BRAND_NAME}"
    if CITY_REGION:
        footer += f" • {CITY_REGION}"
    st.markdown(
        f"""
        <footer class="footer">
            <span>{footer}</span>
            <a href="{insta_url}" target="_blank" rel="noopener">Instagram</a>
        </footer>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
