from __future__ import annotations

import streamlit as st

from services.seo import inject_seo

BRAND_NAME: str = st.secrets.get("BRAND_NAME", "Thrive with Frida")
HEX_PRIMARY: str = st.secrets.get("HEX_PRIMARY", "#0F1115")


def page() -> None:
    st.set_page_config(page_title=f"About — {BRAND_NAME}", page_icon="✨", layout="wide")
    inject_seo(
        title=f"About — {BRAND_NAME}",
        description="Modern, refined coaching. Credentials-forward, outcomes-focused.",
        image_url=None,
        theme_color=HEX_PRIMARY,
    )

    st.markdown("## About")
    st.write(
        """
**Frida** is a high-performance personal trainer crafting minimalist programs for maximum impact.
Certified (e.g., *NASM CPT*, *CPR/AED*), she combines strength training with intelligent mobility,
data-aware progression, and realistic nutrition guidance. Sessions emphasize form, tempo control,
and breathing—building durable strength without noise.

**Philosophy**: clear intent, clean execution, and consistent iteration. We track what matters,
adjust what’s necessary, and keep the rest elegant and simple.
"""
    )

    st.markdown("### Who this is for")
    st.write(
        """
- Busy professionals and founders who value time and outcomes  
- Executives who prefer discreet, concierge scheduling  
- High-achievers returning to training who want sustainable progress  
- Remote clients who need effective programming they’ll actually follow
"""
    )

    st.info(
        "This bio tone is derived from the public handle **@thrivewfrida**. "
        "Update copy anytime in this page’s source to better match the live Instagram profile."
    )


if __name__ == "__main__":
    page()
