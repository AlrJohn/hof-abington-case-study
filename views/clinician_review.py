"""Clinician review, editing, evidence, evaluation, and approval view."""

from copy import deepcopy

import streamlit as st

from services.data_adapter import (
    evaluate_message,
    generate_outreach,
    get_case,
    get_sources,
    regenerate_section,
)
from services.ui_state import (
    approve_message,
    initialize_state,
    mark_message_changed,
)
from views.components import (
    render_evaluation,
    render_page_header,
    render_status_badge,
    render_summary_card,
    render_workflow_steps,
)


def _save_manual_edits(edited_values: dict[str, str]) -> None:
    """Save changed sections, record clinician authorship, and invalidate approval."""
    message = deepcopy(st.session_state["message"])
    changed = False
    for section in message["sections"]:
        new_text = edited_values[section["id"]].strip()
        if new_text and new_text != section["text"]:
            section["text"] = new_text
            section["edited_by_clinician"] = True
            section.pop("revision_type", None)
            changed = True

    if changed:
        message["version"] = int(message.get("version", 1)) + 1
        st.session_state["message"] = message
        mark_message_changed(st.session_state)
        st.session_state["edit_notice"] = "Clinician edits saved. Run the comprehension check before approval."
    else:
        st.session_state["edit_notice"] = "No message changes were detected."


def _render_message_editor(case_data: dict) -> None:
    """Render the five-section message editor and its source references."""
    message = st.session_state["message"]
    edited_values: dict[str, str] = {}

    st.subheader("Patient-facing message")
    st.caption(f"Draft version {message['version']} · Factual claims retain clinician-visible source IDs.")

    with st.form("message_editor"):
        for section in message["sections"]:
            label = section["title"]
            if section.get("edited_by_clinician"):
                label += " · Edited by Clinician"
            elif section.get("revision_type"):
                label += " · AI-assisted demo revision"

            edited_values[section["id"]] = st.text_area(
                label,
                value=section["text"],
                height=130,
                key=f"section_{section['id']}_v{message['version']}",
            )
            st.caption("Sources: " + ", ".join(section["source_ids"]))

        submitted = st.form_submit_button(
            "Save clinician edits",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        _save_manual_edits(edited_values)
        st.rerun()

    notice = st.session_state.pop("edit_notice", None)
    if notice:
        st.info(notice)

    with st.expander("View evidence for this message"):
        for section in message["sections"]:
            st.markdown(f"**{section['title']}**")
            for source in get_sources(case_data, section["source_ids"]):
                st.markdown(f"- `{source['id']}` · {source['label']}: {source['detail']}")


def _render_revision_controls() -> None:
    """Render deterministic targeted-regeneration controls for the UI prototype."""
    message = st.session_state["message"]
    title_by_id = {section["id"]: section["title"] for section in message["sections"]}

    st.subheader("Targeted revision")
    st.caption("This control simulates CS1's future section-regeneration service.")
    section_id = st.selectbox(
        "Section to revise",
        options=list(title_by_id),
        format_func=title_by_id.get,
        key="revision_section",
    )
    preset = st.selectbox(
        "Revision instruction",
        ["Make this easier to understand", "Make this shorter", "Make this sound warmer", "Custom instruction"],
        key="revision_preset",
    )
    custom = ""
    if preset == "Custom instruction":
        custom = st.text_input("Custom instruction", key="revision_custom")

    if st.button("Regenerate selected section", use_container_width=True):
        instruction = custom.strip() if preset == "Custom instruction" else preset
        if not instruction:
            st.warning("Enter a custom instruction before regenerating.")
        else:
            updated = regenerate_section(section_id, instruction, message)
            st.session_state["message"] = updated
            st.session_state["evaluation"] = evaluate_message(updated)
            st.session_state["approved"] = False
            st.session_state["sent"] = False
            st.session_state["workflow_status"] = "Needs review"
            st.session_state["revision_notice"] = f"Revised only: {title_by_id[section_id]}."
            st.rerun()

    notice = st.session_state.pop("revision_notice", None)
    if notice:
        st.success(notice)


def render() -> None:
    """Render the complete fixture-backed clinician workflow."""
    initialize_state(st.session_state)
    case_data = get_case(st.session_state["selected_candidate_id"])
    status = st.session_state["workflow_status"]

    render_page_header(
        "Clinician workspace",
        "Review Patient Outreach",
        "Generate a grounded message, inspect evidence, check clarity, and approve the exact patient-facing version.",
    )
    render_workflow_steps(status)

    patient, trial, match = st.columns(3)
    with patient:
        render_summary_card(
            "Synthetic patient",
            case_data["patient_summary"]["display_name"],
            f"{case_data['patient_summary']['condition']} · {case_data['patient_summary']['patient_id']}",
        )
    with trial:
        render_summary_card(
            "Trial",
            case_data["trial_summary"]["title"],
            f"{case_data['trial_summary']['phase']} · {case_data['trial_summary']['trial_id']}",
        )
    with match:
        render_summary_card(
            "Azra match context",
            "Potential match supplied",
            case_data["match_summary"]["review_note"],
        )

    st.caption(case_data["patient_summary"]["data_notice"])
    st.divider()

    if st.session_state["message"] is None:
        with st.container(border=True):
            st.subheader("Generate outreach")
            st.write(
                "Create the five-section demo message and run the fixed simulated comprehension rubric."
            )
            if st.button("Generate outreach", type="primary"):
                message = generate_outreach(case_data)
                st.session_state["message"] = message
                st.session_state["evaluation"] = evaluate_message(message)
                st.session_state["workflow_status"] = "Draft"
                st.rerun()
        return

    editor_column, review_column = st.columns([1.75, 1], gap="large")
    with editor_column:
        _render_message_editor(case_data)

    with review_column:
        st.subheader("Comprehension check")
        evaluation = st.session_state["evaluation"]
        render_evaluation(evaluation)

        if evaluation.get("is_stale"):
            st.warning(
                "The message changed after this evaluation. Run the check again before approval.",
            )
            if st.button("Run comprehension check", type="primary", use_container_width=True):
                st.session_state["evaluation"] = evaluate_message(st.session_state["message"])
                st.session_state["workflow_status"] = "Needs review"
                st.rerun()

        st.subheader("Current status")
        render_status_badge(st.session_state["workflow_status"])

        st.subheader("Evidence sources")
        for source in case_data["sources"]:
            with st.expander(f"{source['id']} · {source['label']}"):
                st.caption(source["category"])
                st.write(source["detail"])

    st.divider()
    controls, approval = st.columns([1.25, 1], gap="large")
    with controls:
        _render_revision_controls()

    with approval:
        st.subheader("Clinician decision")
        st.write("Approve the exact message version shown above before opening the patient preview.")
        evaluation_is_stale = st.session_state["evaluation"].get("is_stale", True)
        if not st.session_state["approved"]:
            if st.button(
                "Approve message",
                type="primary",
                disabled=evaluation_is_stale,
                use_container_width=True,
            ):
                approve_message(st.session_state)
                st.switch_page("views/patient_preview.py")
        else:
            st.success("This exact message version is approved.")
            if st.button("Open patient preview", type="primary", use_container_width=True):
                st.switch_page("views/patient_preview.py")


render()
