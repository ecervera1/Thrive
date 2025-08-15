from __future__ import annotations

import time

import streamlit as st

from components.forms import InquiryData, render_inquiry_form, validate_inquiry
from services.seo import inject_seo
from services.storage import GoogleSheetStorage, StorageResult

BRAND_NAME: str = st.secrets.get("BRAND_NAME", "Thrive with Frida")
HEX_PRIMARY: str = st.secrets.get("HEX_PRIMARY", "#0F1115")


def _throttle_ok() -> bool:
    """Very light, session-based throttle."""
    now = time.time()
    key = "last_submit_ts"
    last = st.session_state.get(key, 0.0)
    if now - last < 6.0:  # 6 seconds between submits
        return False
    st.session_state[key] = now
    return True


def page() -> None:
    st.set_page_config(page_title=f"Inquiry — {BRAND_NAME}", page_icon="✉️", layout="wide")
    inject_seo(
        title=f"Inquiry — {BRAND_NAME}",
        description="Send an inquiry. We'll reply within one business day.",
        image_url=None,
        theme_color=HEX_PRIMARY,
    )

    st.markdown("## Send an Inquiry")
    st.caption("Tell us how you'd like to work together. Required fields marked with *.")

    form_data = render_inquiry_form()

    if st.button("Submit Inquiry", type="primary", use_container_width=True):
        if not _throttle_ok():
            st.warning("Please wait a few seconds before submitting again.")
            return

        ok, msg = validate_inquiry(form_data)
        if not ok:
            st.error(msg)
            return

        storage = GoogleSheetStorage()
        result: StorageResult = storage.save_inquiry(form_data)
        if result.ok:
            st.success("Inquiry received. Thank you! We'll be in touch shortly.")
        else:
            st.error(f"Could not record your inquiry: {result.message}")

    st.info(
        "We never share your information. For faster coordination, you can also book directly on the **Schedule** page."
    )


if __name__ == "__main__":
    page()
