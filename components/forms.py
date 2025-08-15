from __future__ import annotations

import re
import time
from dataclasses import dataclass
from typing import Tuple

import streamlit as st

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass
class InquiryData:
    name: str
    email: str
    phone: str
    goals: str
    notes: str
    honey: str  # honeypot
    submitted_ts: float


def render_inquiry_form() -> InquiryData:
    with st.form(key="inquiry_form", clear_on_submit=False):
        name = st.text_input("Name*", max_chars=120, placeholder="Your full name")
        email = st.text_input("Email*", max_chars=120, placeholder="you@email.com")
        phone = st.text_input("Phone", max_chars=40, placeholder="+1…")
        goals = st.text_area("Goals", height=140, placeholder="Share your goals, timeline, any constraints.")
        notes = st.text_area("Additional Notes", height=120, placeholder="Anything else we should know?")
        honey = st.text_input("Leave this field empty", value="", key="hp", help="(anti-spam)", label_visibility="collapsed")
        submitted = st.form_submit_button("Preview")
        # The main Submit button is outside, but we use this to capture state
        ts = time.time()

    return InquiryData(
        name=name.strip(),
        email=email.strip(),
        phone=phone.strip(),
        goals=goals.strip(),
        notes=notes.strip(),
        honey=honey.strip(),
        submitted_ts=ts,
    )


def validate_inquiry(data: InquiryData) -> Tuple[bool, str]:
    if data.honey:
        return False, "Submission flagged as spam."
    if not data.name:
        return False, "Name is required."
    if not data.email or not EMAIL_RE.match(data.email):
        return False, "A valid email is required."
    # Optional sanity trims
    if len(data.goals) > 5000 or len(data.notes) > 5000:
        return False, "Text fields are too long."
    return True, "ok"
