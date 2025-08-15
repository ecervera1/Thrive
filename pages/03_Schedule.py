from __future__ import annotations

from typing import Optional

import streamlit as st
from streamlit.components.v1 import html

from services.seo import inject_seo

BRAND_NAME: str = st.secrets.get("BRAND_NAME", "Thrive with Frida")
HEX_PRIMARY: str = st.secrets.get("HEX_PRIMARY", "#0F1115")
SCHEDULING_EMBED_URL: Optional[str] = st.secrets.get("SCHEDULING_EMBED_URL", "")


def page() -> None:
    st.set_page_config(page_title=f"Schedule — {BRAND_NAME}", page_icon="📅", layout="wide")
    inject_seo(
        title=f"Schedule — {BRAND_NAME}",
        description="Book your consultation or session via Cal.com.",
        image_url=None,
        theme_color=HEX_PRIMARY,
    )

    st.markdown("## Schedule")

    if not SCHEDULING_EMBED_URL:
        st.error("Scheduling link is not configured.")
        st.write(
            "Add `SCHEDULING_EMBED_URL` to `.streamlit/secrets.toml` "
            "(e.g., `https://cal.com/your-handle?embed=true`)."
        )
        return

    with st.container(border=True):
        st.caption("Loading scheduling…")
        iframe = f"""
        <iframe
            src="{SCHEDULING_EMBED_URL}"
            width="100%"
            height="900"
            frameborder="0"
            allowfullscreen
            title="Cal.com Scheduling"
            style="border-radius:12px;"
        ></iframe>
        """
        html(iframe, height=920, scrolling=True)


if __name__ == "__main__":
    page()
