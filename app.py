"""Entry point for the Azra-inspired clinical trial outreach prototype."""

from pathlib import Path

import streamlit as st

from services.ui_state import initialize_state, reset_demo
from views.components import load_css, render_sidebar_brand, render_status_badge


ROOT = Path(__file__).resolve().parent

st.set_page_config(
    page_title="Azra AI Outreach Prototype",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="auto",
)

load_css(ROOT / "assets" / "styles.css")
initialize_state(st.session_state)

pages = [
    st.Page(
        "views/candidate_queue.py",
        title="Candidate Queue",
        default=True,
    ),
    st.Page(
        "views/clinician_review.py",
        title="Clinician Review",
    ),
    st.Page(
        "views/patient_preview.py",
        title="Patient Preview",
    ),
]

navigation = st.navigation(pages, position="hidden")

with st.sidebar:
    render_sidebar_brand()
    st.page_link("views/candidate_queue.py", label="Candidate Queue")
    st.page_link("views/clinician_review.py", label="Clinician Review")
    st.page_link("views/patient_preview.py", label="Patient Preview")
    st.divider()
    st.caption("Clinician-controlled clinical trial outreach")
    render_status_badge(st.session_state["workflow_status"])
    st.write("")
    if st.button("Reset demo", use_container_width=True):
        reset_demo(st.session_state)
        st.rerun()

navigation.run()
