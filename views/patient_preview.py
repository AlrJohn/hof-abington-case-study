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

patient_shell_html = f"""
<style>
.patient-phone-wrapper {{
    display: flex;
    justify-content: center;
    padding: 10px 0 25px 0;
}}

.patient-phone {{
    width: 390px;
    min-height: 720px;
    border: 10px solid #18181b;
    border-radius: 42px;
    background: #f8fafc;
    box-shadow: 0 20px 45px rgba(0, 0, 0, 0.22);
    overflow: hidden;
    position: relative;
}}

.patient-status-bar {{
    height: 32px;
    background: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 18px;
    font-size: 12px;
    font-weight: 600;
    color: #18181b;
}}

.patient-header {{
    background: white;
    border-bottom: 1px solid #e4e4e7;
    padding: 16px 20px;
}}

.patient-header-title {{
    font-size: 23px;
    font-weight: 700;
    color: #18181b;
}}

.patient-header-subtitle {{
    font-size: 13px;
    color: #71717a;
    margin-top: 3px;
}}

.patient-message-card {{
    margin: 20px 16px;
    background: white;
    border: 1px solid #e4e4e7;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}}

.patient-unread {{
    display: inline-block;
    background: #2563eb;
    color: white;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 8px;
    border-radius: 999px;
    margin-bottom: 12px;
}}

.patient-sender {{
    font-size: 14px;
    font-weight: 700;
    color: #18181b;
}}

.patient-subject {{
    font-size: 19px;
    font-weight: 700;
    color: #18181b;
    margin-top: 7px;
}}

.patient-preview {{
    font-size: 14px;
    line-height: 1.55;
    color: #52525b;
    margin-top: 9px;
}}

.patient-date {{
    font-size: 11px;
    color: #a1a1aa;
    margin-top: 14px;
}}

.patient-content {{
    height: 570px;
    overflow-y: auto;
    padding: 18px;
}}

.patient-content .azra-patient-section {{
    margin-bottom: 18px;
}}

.patient-home {{
    height: 35px;
    width: 120px;
    background: #18181b;
    border-radius: 20px;
    margin: 12px auto;
}}
</style>

<div class="patient-phone-wrapper">
    <div class="patient-phone">

        <div class="patient-status-bar">
            <span>9:41</span>
            <span>● ● ● 🔋</span>
        </div>

        <div class="patient-header">
            <div class="patient-header-title">Messages</div>
            <div class="patient-header-subtitle">
                Maria Reyes
            </div>
        </div>

        <div class="patient-message-card">

            <div class="patient-unread">
                NEW MESSAGE
            </div>

            <div class="patient-sender">
                Example Health Research Team
            </div>

            <div class="patient-subject">
                Clinical Trial Opportunity
            </div>

            <div class="patient-preview">
                You may be receiving this message because
                you are due for cervical and colorectal
                cancer screening...
            </div>

            <div class="patient-date">
                Today · New message
            </div>

        </div>

        <div class="patient-content">
            {sections_html}
        </div>

        <div class="patient-home"></div>

    </div>
</div>
"""

st.markdown(patient_shell_html, unsafe_allow_html=True)
    
