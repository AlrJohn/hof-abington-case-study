"""CS2-owned helpers for predictable Streamlit workflow state."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, MutableMapping

from services.data_adapter import DEMO_CANDIDATE_ID


_DEFAULT_STATE: dict[str, Any] = {
    "_active_view": None,
    "selected_candidate_id": DEMO_CANDIDATE_ID,
    "workflow_status": "Ready for outreach",
    "message": None,
    "evaluation": None,
    "approved": False,
    "selected_channel": "Patient Portal",
    "sent": False,
}


def initialize_state(state: MutableMapping[str, Any]) -> None:
    """Add missing workflow keys without overwriting an active demo session."""
    for key, value in _DEFAULT_STATE.items():
        if key not in state:
            state[key] = deepcopy(value)


def reset_demo(state: MutableMapping[str, Any]) -> None:
    """Restore the demo to its initial state while preserving Streamlit internals."""
    for key, value in _DEFAULT_STATE.items():
        state[key] = deepcopy(value)


def mark_message_changed(state: MutableMapping[str, Any]) -> None:
    """Invalidate approval and evaluation after a clinician changes the draft."""
    state["approved"] = False
    state["sent"] = False
    state["workflow_status"] = "Needs review"
    if state.get("evaluation"):
        state["evaluation"]["is_stale"] = True


def approve_message(state: MutableMapping[str, Any]) -> None:
    """Record approval of the exact current message version."""
    state["approved"] = True
    state["sent"] = False
    state["workflow_status"] = "Approved"


def mark_sent(state: MutableMapping[str, Any]) -> None:
    """Complete the simulated delivery step without contacting an external system."""
    state["sent"] = True
    state["workflow_status"] = "Sent"
