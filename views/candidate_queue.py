"""Candidate queue and outreach-status view owned by CS2."""

import streamlit as st

from services.data_adapter import get_candidates
from services.ui_state import initialize_state
from views.components import (
    render_page_header,
    render_status_badge,
    render_workflow_steps,
)


def render() -> None:
    """Render the synthetic queue and route the selected record to review."""
    initialize_state(st.session_state)
    status = st.session_state["workflow_status"]
    candidates = get_candidates(status)

    render_page_header(
        "Clinical research outreach",
        "Candidate Queue",
        "Review patients whom Azra has already surfaced as possible trial matches.",
    )
    render_workflow_steps(status)

    metric_columns = st.columns(3)
    metric_columns[0].metric("Candidates", len(candidates))
    metric_columns[1].metric("Awaiting review", 0 if status in {"Approved", "Sent"} else 1)
    metric_columns[2].metric("Approved or sent", 1 if status in {"Approved", "Sent"} else 0)

    st.subheader("Outreach worklist")
    st.caption("This queue contains synthetic demonstration data only.")

    for candidate in candidates:
        with st.container(border=True):
            details, trial, priority, state, action = st.columns([2.2, 2.5, 1, 1.3, 1.2])
            with details:
                st.caption("PATIENT")
                st.markdown(f"**{candidate['display_name']}**")
                st.caption(candidate["id"])
            with trial:
                st.caption("TRIAL")
                st.markdown(f"**{candidate['trial_title']}**")
                st.caption("Pre-screened match supplied by Azra")
            with priority:
                st.caption("PRIORITY")
                st.markdown(candidate["priority"])
            with state:
                st.caption("STATUS")
                render_status_badge(candidate["status"])
            with action:
                st.caption("ACTION")
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
