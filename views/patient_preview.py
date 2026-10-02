"""Approved patient message, channel preview, and simulated-send view."""

from html import escape

import streamlit as st

from services.data_adapter import get_case
from services.ui_state import initialize_state, mark_sent
from views.components import (
    patient_section_html,
    render_channel_notice,
    render_page_header,
    render_workflow_steps,
    reset_scroll_on_page_change,
)


CHANNELS = ["Patient Portal", "Email", "SMS", "Other / Future Integration"]


def render() -> None:
    """Render the clean patient experience only after clinician approval."""
    initialize_state(st.session_state)
    reset_scroll_on_page_change("patient_preview")
    render_page_header(
        "Approved patient experience",
        "Patient Preview",
        "Preview the secure message and the notification shown for the selected delivery concept.",
    )
    render_workflow_steps(st.session_state["workflow_status"])

    if not st.session_state["approved"] or st.session_state["message"] is None:
        st.warning(
            "Patient Preview is locked until a clinician generates, checks, and approves the message.",
        )
        if st.button("Return to clinician review", type="primary"):
            st.switch_page("views/clinician_review.py")
        return

    case_data = get_case(st.session_state["selected_candidate_id"])
    delivery = case_data["delivery"]
    patient_name = case_data["patient_summary"]["display_name"]

    channel = st.radio(
        "Delivery concept",
        CHANNELS,
        key="selected_channel",
        horizontal=True,
        help="This prototype previews a channel but does not contact a patient.",
    )
    render_channel_notice(channel, delivery["health_system_name"])

  # Build the five message sections from the current CS1-generated message.
sections_html = "".join(
    patient_section_html(section["title"], section["text"])
    for section in st.session_state["message"]["sections"]
)

patient_shell_html = (
    '<div class="azra-patient-shell">'
    '<div class="azra-patient-banner">'
    "<span>Example Health Research Team</span>"
    "<h1>A research study you may want to learn about</h1>"
    "</div>"
    f"{sections_html}"
    ...
)

st.markdown(patient_shell_html, unsafe_allow_html=True)
render()



    
