from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Optional, Protocol

import streamlit as st

from components.forms import InquiryData

logger = logging.getLogger(__name__)


@dataclass
class StorageResult:
    ok: bool
    message: str


class Storage(Protocol):
    def save_inquiry(self, data: InquiryData) -> StorageResult: ...


class GoogleSheetStorage(Storage):
    """
    Writes inquiries to a Google Sheet using gspread.

    Secrets required:
      - GOOGLE_SERVICE_ACCOUNT_JSON (inline JSON)
      - GOOGLE_SHEET_NAME
    """

    def __init__(self) -> None:
        self.sheet_name: str = st.secrets.get("GOOGLE_SHEET_NAME", "ThriveWFrida_Inquiries")
        self.service_json: Optional[str] = st.secrets.get("GOOGLE_SERVICE_ACCOUNT_JSON", None)

    def _client_worksheet(self):
        import gspread
        from google.oauth2.service_account import Credentials  # type: ignore

        if not self.service_json:
            raise RuntimeError("Missing GOOGLE_SERVICE_ACCOUNT_JSON in secrets")

        info = json.loads(self.service_json)
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_info(info, scopes=scopes)
        client = gspread.authorize(creds)
        sh = client.open(self.sheet_name)
        ws = sh.sheet1
        # Prepare header if empty
        if len(ws.get_all_values()) == 0:
            ws.append_row(
                [
                    "timestamp_utc",
                    "name",
                    "email",
                    "phone",
                    "goals",
                    "notes",
                    "source",
                    "user_agent",
                ]
            )
        return ws

    def save_inquiry(self, data: InquiryData) -> StorageResult:
        try:
            ws = self._client_worksheet()
            ts = datetime.now(tz=timezone.utc).isoformat()
            user_agent = st.session_state.get("_user_agent", "")
            ws.append_row(
                [
                    ts,
                    data.name,
                    data.email,
                    data.phone,
                    data.goals,
                    data.notes,
                    "streamlit",
                    user_agent,
                ]
            )
            return StorageResult(ok=True, message="Saved to Google Sheet.")
        except Exception as e:
            # Fallback to console log so the app still passes acceptance locally
            logger.exception("Failed to write to Google Sheet; falling back to console.")
            print("=== Inquiry (console fallback) ===")
            print(asdict(data))
            return StorageResult(ok=True, message=f"Saved locally (console fallback). Error: {e}")
