"""Reusable presentation helpers for the CS2-owned Streamlit views."""

from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any

import streamlit as st


STATUS_CLASS = {
    "Ready for outreach": "ready",
    "Draft": "draft",
    "Needs review": "review",
    "Approved": "approved",
    "Sent": "sent",
}


def load_css(path: Path) -> None:
    """Load the small, local stylesheet used for branded presentation details."""
    st.markdown(f"<style>{path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def render_sidebar_brand() -> None:
    """Render a text-only prototype wordmark without copying a company logo asset."""
    st.markdown(
        """
        <div class="azra-wordmark" aria-label="Azra AI Outreach Prototype">
            <span class="azra-wordmark-main">azra</span><span class="azra-wordmark-ai">AI</span>
            <span class="azra-wordmark-product">Outreach Prototype</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(eyebrow: str, title: str, description: str) -> None:
    """Render the consistent heading used at the top of each workflow page."""
    st.markdown(
        f"""
        <header class="azra-page-header">
            <div class="azra-eyebrow">{escape(eyebrow)}</div>
            <h1>{escape(title)}</h1>
            <p>{escape(description)}</p>
        </header>
        """,
        unsafe_allow_html=True,
    )


def render_status_badge(status: str) -> None:
    """Render a labeled badge so workflow state is never communicated by color alone."""
    css_class = STATUS_CLASS.get(status, "ready")
    st.markdown(
        f'<span class="azra-status azra-status-{css_class}">{escape(status)}</span>',
        unsafe_allow_html=True,
    )


def render_workflow_steps(current_status: str) -> None:
    """Show the compact clinician workflow and its current position."""
    steps = ["Ready for outreach", "Draft", "Needs review", "Approved", "Sent"]
    current_index = steps.index(current_status) if current_status in steps else 0
    items = []
    for index, label in enumerate(steps):
        state = "complete" if index < current_index else "active" if index == current_index else "future"
        items.append(
            f'<div class="azra-step azra-step-{state}"><span>{index + 1}</span>{escape(label)}</div>'
        )
    st.markdown(f'<div class="azra-workflow">{"".join(items)}</div>', unsafe_allow_html=True)


def render_summary_card(label: str, value: str, detail: str = "") -> None:
    """Render a small information card for patient and trial context."""
    detail_html = f"<p>{escape(detail)}</p>" if detail else ""
    st.markdown(
        f"""
        <div class="azra-summary-card">
            <span>{escape(label)}</span>
            <strong>{escape(value)}</strong>
            {detail_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_evaluation(evaluation: dict[str, Any]) -> None:
    """Render the simulated fixed-rubric evaluation with an explicit limitation label."""
    stale_class = " azra-score-stale" if evaluation.get("is_stale") else ""
    score = escape(str(evaluation.get("overall_score", "—")))
    label = escape(evaluation.get("label", "Model-assisted rubric evaluation"))
    recommendation = escape(evaluation.get("recommendation", "Not evaluated"))
    st.markdown(
        f"""
        <div class="azra-score-card{stale_class}">
            <div>
                <span class="azra-score-label">{label}</span>
                <strong class="azra-score-value">{score}<small>/100</small></strong>
            </div>
            <span class="azra-score-recommendation">{recommendation}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("This simulated score supports clinician review; it is not proof of patient comprehension.")

    criteria = evaluation.get("criterion_scores", {})
    for criterion, criterion_score in criteria.items():
        st.progress(
            int(criterion_score),
            text=f"{criterion}: {criterion_score}/100",
        )

    issues = evaluation.get("issues", [])
    if issues:
        st.markdown("**Review notes**")
        for issue in issues:
            st.markdown(f"- {issue}")


def patient_section_html(title: str, text: str) -> str:
    """Return escaped patient copy for one complete secure-message wrapper."""
    # Keep this markup compact. Indented multiline fragments can be interpreted as
    # code blocks when Streamlit passes the complete message through Markdown.
    return (
        '<section class="azra-patient-section" data-message-section="true">'
        f"<h2>{escape(title)}</h2>"
        f"<p>{escape(text)}</p>"
        "</section>"
    )


def render_channel_notice(channel: str) -> None:
    """Show the patient notification associated with the selected delivery concept."""
    notices = {
        "Patient Portal": (
            "Secure portal message",
            "Your full research opportunity message is available below.",
        ),
        "Email": (
            "Email notification",
            "You have a new research opportunity message from Example Health. Sign in to the secure patient portal to review it.",
        ),
        "SMS": (
            "SMS notification",
            "Example Health: You have a new research opportunity message. Sign in to your secure patient portal to review it.",
        ),
        "Other / Future Integration": (
            "Future integration",
            "The approved message is ready for an additional health-system communication channel.",
        ),
    }
    title, message = notices[channel]
    st.markdown(
        f"""
        <div class="azra-notice-card">
            <span>{escape(title)}</span>
            <p>{escape(message)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
