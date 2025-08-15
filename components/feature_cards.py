from __future__ import annotations

import streamlit as st


def render_feature_cards(accent_hex: str = "#C7A97B") -> None:
    st.markdown("### What we offer")
    cols = st.columns(4, gap="large")
    cards = [
        ("1:1 Coaching", "Precision programming and hands-on coaching tailored to you."),
        ("Small-Group", "Train with 2–4 peers. Accountability with a premium feel."),
        ("Virtual", "Remote sessions and expert program oversight—wherever you are."),
        ("Nutrition Add-On", "Pragmatic guidance to complement your training."),
    ]
    for col, (title, blurb) in zip(cols, cards):
        with col:
            st.markdown(
                f"""
                <div class="card">
                    <div class="card-title">{title}</div>
                    <div class="card-blurb">{blurb}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
