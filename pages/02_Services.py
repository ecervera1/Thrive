from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit as st
from services.seo import inject_seo

BRAND_NAME: str = st.secrets.get("BRAND_NAME", "Thrive with Frida")
HEX_PRIMARY: str = st.secrets.get("HEX_PRIMARY", "#0F1115")

DATA_DIR = Path("data")
SERVICES_JSON = DATA_DIR / "services.json"


def _load_services() -> list[dict[str, Any]]:
    try:
        with SERVICES_JSON.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def page() -> None:
    st.set_page_config(page_title=f"Services — {BRAND_NAME}", page_icon="🗂", layout="wide")
    inject_seo(
        title=f"Services — {BRAND_NAME}",
        description="Private coaching, concierge training, small-group formats, and remote programming.",
        image_url=None,
        theme_color=HEX_PRIMARY,
    )

    st.markdown("## Services")
    st.caption("Select a service to begin. Pricing is available upon request.")
    services = _load_services()
    if not services:
        st.warning("No services found. Add entries to `data/services.json`.")
        return

    cols = st.columns(2, gap="large")
    for idx, svc in enumerate(services):
        with cols[idx % 2]:
            with st.container():
                st.markdown(f"### {svc.get('title', 'Service')}")
                st.write(svc.get("blurb", ""))
                meta = []
                if length := svc.get("session_length"):
                    meta.append(f"**Session**: {length}")
                if dtype := svc.get("delivery_type"):
                    meta.append(f"**Delivery**: {dtype}")
                if meta:
                    st.caption(" • ".join(meta))

                left, right = st.columns(2)
                with left:
                    if st.button("Schedule", key=f"sched_{idx}"):
                        st.switch_page("pages/03_Schedule.py")
                with right:
                    if st.button("Send Inquiry", key=f"inq_{idx}"):
                        st.switch_page("pages/04_Inquiry.py")

    st.divider()
    st.write("Looking for something bespoke? Use the **Inquiry** page to describe needs and availability.")


if __name__ == "__main__":
    page()
