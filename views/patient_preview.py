"""Approved patient message, channel preview, and simulated-send view."""

from html import escape

import streamlit as st

from services.ui_state import initialize_state, mark_sent
from views.components import (
    patient_section_html,
    render_channel_notice,
    render_page_header,
    render_workflow_steps,
)


CHANNELS = ["Patient Portal", "Email", "SMS", "Other / Future Integration"]


def render() -> None:
    """Render the clean patient experience only after clinician approval."""
    initialize_state(st.session_state)
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

    channel = st.radio(
        "Delivery concept",
        CHANNELS,
        key="selected_channel",
        horizontal=True,
        help="This prototype previews a channel but does not contact a patient.",
    )
    render_channel_notice(channel)

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
        '<section class="azra-patient-section azra-verification-section">'
        "<h2>Verify this message</h2>"
        "<p>Call Example Health at 555-0100 or sign in through the health system "
        "website you normally use. Participation is voluntary.</p>"
        "</section>"
        '<p style="color:#52525b;font-size:.75rem;margin:1rem 0 0;">'
        f"Demo message for {escape('Jordan Lee (Synthetic)')} · No real patient data"
        "</p>"
        "</div>"
    )
    st.markdown(patient_shell_html, unsafe_allow_html=True)

    st.info(
        "The patient view intentionally excludes match evidence, source IDs, internal scores, and clinician controls.",
    )

    back, send = st.columns([1, 1])
    with back:
        if st.button("Back to clinician review", use_container_width=True):
            st.switch_page("views/clinician_review.py")
    with send:
        if not st.session_state["sent"]:
            if st.button(
                "Simulate send",
                type="primary",
                use_container_width=True,
            ):
                mark_sent(st.session_state)
                st.rerun()
        else:
            st.success("Simulated delivery complete. No external message was sent.")


render()
