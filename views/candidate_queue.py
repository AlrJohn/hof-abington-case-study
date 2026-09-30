"""Candidate queue and outreach-status view owned by CS2."""

from html import escape

import streamlit as st

from services.data_adapter import get_candidates
from services.ui_state import initialize_state
from views.components import (
    STATUS_CLASS,
    render_page_header,
    render_workflow_steps,
    reset_scroll_on_page_change,
)


def render() -> None:
    """Render the synthetic queue and route the selected record to review."""
    initialize_state(st.session_state)
    reset_scroll_on_page_change("candidate_queue")
    status = st.session_state["workflow_status"]
    candidates = get_candidates(status)

    render_page_header(
        "Clinical research outreach",
        "Candidate Queue",
        "Review patients whom Azra has already surfaced as possible trial matches.",
    )
    render_workflow_steps(status)

    with st.container(key="queue_metrics"):
        metric_columns = st.columns(3)
        metric_columns[0].metric("Candidates", len(candidates))
        metric_columns[1].metric("Awaiting review", 0 if status in {"Approved", "Sent"} else 1)
        metric_columns[2].metric("Approved or sent", 1 if status in {"Approved", "Sent"} else 0)

    st.subheader("Outreach worklist")
    st.caption("This queue contains synthetic demonstration data only.")

    for candidate in candidates:
        with st.container(border=True):
            status_class = STATUS_CLASS.get(candidate["status"], "ready")
            st.markdown(
                f"""
                <div class="azra-candidate-grid">
                    <div class="azra-candidate-field">
                        <span>Patient</span>
                        <strong>{escape(candidate['display_name'])}</strong>
                        <small>{escape(candidate['id'])}</small>
                    </div>
                    <div class="azra-candidate-field">
                        <span>Trial</span>
                        <strong>{escape(candidate['trial_title'])}</strong>
                        <small>Pre-screened match supplied by Azra</small>
                    </div>
                    <div class="azra-candidate-field">
                        <span>Priority</span>
                        <strong>{escape(candidate['priority'])}</strong>
                    </div>
                    <div class="azra-candidate-field">
                        <span>Status</span>
                        <div><span class="azra-status azra-status-{status_class}">{escape(candidate['status'])}</span></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(
                "Open candidate",
                key=f"open_{candidate['id']}",
                type="primary",
                use_container_width=True,
            ):
                st.session_state["selected_candidate_id"] = candidate["id"]
                st.switch_page("views/clinician_review.py")

    st.info(
        "Azra supplies the potential match. This prototype begins with clinician-reviewed outreach and does not determine eligibility.",
    )


render()
