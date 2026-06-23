import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any

import streamlit as st


# ----- in-memory store (per browser session) -----
def _store() -> Dict[str, Any]:
    if "conversations_store" not in st.session_state:
        st.session_state.conversations_store = {}
    return st.session_state.conversations_store


# ----- helpers ------
def now_utc():
    return datetime.now(timezone.utc)

def create_new_conversation_id() -> str:
    return str(uuid.uuid4())


# ----- core services -----
def create_new_conversation(title: Optional[str] = None, role: Optional[str] = None, content: Optional[str] = None) -> str:
    conv_id = create_new_conversation_id()
    ts = now_utc()
    doc = {
        "_id": conv_id,
        "title": title or "Untitled Conversation",
        "messages": [],
        "last_interacted": ts,
    }
    if role and content:
        doc["messages"].append({"role": role, "content": content, "ts": ts})
    _store()[conv_id] = doc
    return conv_id


def add_message(conv_id: str, role: str, content: str) -> bool:
    doc = _store().get(conv_id)
    if not doc:
        return False
    doc["messages"].append({"role": role, "content": content, "ts": now_utc()})
    doc["last_interacted"] = now_utc()
    return True


def get_conversation(conv_id: str) -> Optional[Dict[str, Any]]:
    doc = _store().get(conv_id)
    if doc:
        doc["last_interacted"] = now_utc()
    return doc


def get_all_conversations() -> Dict[str, str]:
    items = sorted(
        _store().values(),
        key=lambda d: d["last_interacted"],
        reverse=True,
    )
    return {d["_id"]: d["title"] for d in items}