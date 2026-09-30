"""Stable data boundary used by the CS2 Streamlit views.

The functions in this module return deterministic, clearly synthetic demo data.
When CS1's services are ready, their responses can be normalized here without
changing any view code.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any


Candidate = dict[str, Any]
CaseData = dict[str, Any]
Message = dict[str, Any]
Evaluation = dict[str, Any]

DEMO_CANDIDATE_ID = "DEMO-001"

_CANDIDATE: Candidate = {
    "id": DEMO_CANDIDATE_ID,
    "display_name": "Jordan Lee (Synthetic)",
    "trial_title": "Example NSCLC Study",
    "status": "Ready for outreach",
    "priority": "Standard",
}

_CASE: CaseData = {
    "candidate": _CANDIDATE,
    "patient_summary": {
        "patient_id": DEMO_CANDIDATE_ID,
        "display_name": "Jordan Lee (Synthetic)",
        "age_group": "Adult",
        "condition": "Non-small cell lung cancer",
        "preferred_language": "English",
        "data_notice": "Synthetic demonstration record. No real patient data is used.",
    },
    "trial_summary": {
        "trial_id": "NCT-DEMO-001",
        "title": "Example NSCLC Study",
        "phase": "Phase II demonstration study",
        "status": "Recruiting (demo)",
        "organization": "Example Health Research Team",
        "location": "Example Health System",
    },
    "match_summary": {
        "summary": "Azra has already surfaced this patient as a possible match.",
        "review_note": (
            "The detailed criteria remain in the clinician view and are not copied "
            "into the patient-facing message."
        ),
        "source_ids": ["SRC-PAT-001", "SRC-MATCH-001"],
    },
    "sources": [
        {
            "id": "SRC-PAT-001",
            "label": "Synthetic patient record",
            "category": "Patient",
            "detail": (
                "Demonstration-only condition and care-team context created for this "
                "prototype."
            ),
        },
        {
            "id": "SRC-TRIAL-001",
            "label": "Demo trial information",
            "category": "Trial",
            "detail": (
                "Example study purpose, visit pattern, and participation details. "
                "These are not claims about a real trial."
            ),
        },
        {
            "id": "SRC-MATCH-001",
            "label": "Mock Azra match evidence",
            "category": "Match",
            "detail": (
                "Simulated evidence indicating that the patient's diagnosis was "
                "reviewed before outreach."
            ),
        },
        {
            "id": "SRC-ORG-001",
            "label": "Approved organization information",
            "category": "Organization",
            "detail": (
                "Demonstration contact and verification language for Example Health "
                "Research Team."
            ),
        },
    ],
}

_MESSAGE: Message = {
    "version": 1,
    "sections": [
        {
            "id": "why_receiving_this",
            "title": "Why you are receiving this",
            "text": (
                "Your care team is sharing information about an example research "
                "study that may be relevant based on information already reviewed "
                "in your record. This does not confirm eligibility, and participation "
                "is voluntary."
            ),
            "source_ids": ["SRC-PAT-001", "SRC-MATCH-001"],
            "edited_by_clinician": False,
        },
        {
            "id": "study_overview",
            "title": "What the study is about",
            "text": (
                "The example study is looking at a research treatment for adults "
                "with non-small cell lung cancer. Researchers want to learn how the "
                "treatment is tolerated and how it may affect the disease."
            ),
            "source_ids": ["SRC-TRIAL-001"],
            "edited_by_clinician": False,
        },
        {
            "id": "participation",
            "title": "What participation may involve",
            "text": (
                "If the study team confirms that you may qualify, participation could "
                "include an initial screening visit, study visits about every three "
                "weeks, routine blood tests, and imaging. The study team would explain "
                "the complete schedule before you decide."
            ),
            "source_ids": ["SRC-TRIAL-001"],
            "edited_by_clinician": False,
        },
        {
            "id": "questions",
            "title": "Questions to discuss",
            "text": (
                "You may want to ask: Why might this study be relevant to me? What "
                "would I need to do? What risks should I know about? Would the study "
                "affect my current care? Who can I speak with before deciding?"
            ),
            "source_ids": ["SRC-TRIAL-001"],
            "edited_by_clinician": False,
        },
        {
            "id": "next_step",
            "title": "Next step",
            "text": (
                "If you would like to learn more, contact the Example Health Research "
                "Team at 555-0100 or ask your physician about this study. You do not "
                "have to participate, and requesting information does not enroll you."
            ),
            "source_ids": ["SRC-ORG-001"],
            "edited_by_clinician": False,
        },
    ],
}

_REWRITTEN_TEXT = {
    "why_receiving_this": (
        "Your care team identified an example research study that may be relevant to "
        "you. This does not confirm eligibility, and taking part is your choice."
    ),
    "study_overview": (
        "This example study is testing a research treatment for adults with non-small "
        "cell lung cancer. The research team wants to understand its effects and how "
        "people tolerate it."
    ),
    "participation": (
        "Participation may include a screening visit, visits about every three weeks, "
        "blood tests, and imaging. The study team would review the full schedule with "
        "you before you decide."
    ),
    "questions": (
        "Consider asking why the study may be relevant, what visits are required, what "
        "risks to discuss, whether current care would change, and who can answer more "
        "questions."
    ),
    "next_step": (
        "To learn more, call the Example Health Research Team at 555-0100 or speak with "
        "your physician. Asking for information does not enroll you in the study."
    ),
}


def get_candidates(status: str = "Ready for outreach") -> list[Candidate]:
    """Return the synthetic candidate queue with the current workflow status."""
    candidate = deepcopy(_CANDIDATE)
    candidate["status"] = status
    return [candidate]


def get_case(candidate_id: str) -> CaseData:
    """Return the synthetic case selected by the clinician."""
    if candidate_id != DEMO_CANDIDATE_ID:
        raise ValueError(f"Unknown synthetic candidate: {candidate_id}")
    return deepcopy(_CASE)


def generate_outreach(case_data: CaseData) -> Message:
    """Return a deterministic outreach draft for the supplied synthetic case."""
    candidate_id = case_data.get("candidate", {}).get("id")
    if candidate_id != DEMO_CANDIDATE_ID:
        raise ValueError("The demo generator only accepts the synthetic demo case.")
    return deepcopy(_MESSAGE)


def evaluate_message(message: Message) -> Evaluation:
    """Return a deterministic model-assisted rubric result for the current draft."""
    edited = any(section.get("edited_by_clinician") for section in message["sections"])
    version = int(message.get("version", 1))
    score = 92 if edited or version > 1 else 89
    issues = (
        ["A clinician-edited section should receive a final source review."]
        if edited
        else ["The participation section could be slightly shorter."]
    )
    return {
        "overall_score": score,
        "criterion_scores": {
            "Purpose": 94,
            "Familiar language": 88 if score == 89 else 93,
            "Sentence clarity": 86 if score == 89 else 92,
            "Organization": 95,
            "Participation information": 84 if score == 89 else 91,
            "Actionability": 92,
            "Trust": 96,
            "Safety language": 97,
        },
        "issues": issues,
        "recommendation": "Ready for clinician review",
        "is_stale": False,
        "label": "Model-assisted rubric evaluation",
    }


def regenerate_section(
    section_id: str,
    instruction: str,
    message: Message,
) -> Message:
    """Replace only the selected section with a deterministic clearer version."""
    if section_id not in _REWRITTEN_TEXT:
        raise ValueError(f"Unknown message section: {section_id}")

    updated = deepcopy(message)
    for section in updated["sections"]:
        if section["id"] == section_id:
            section["text"] = _REWRITTEN_TEXT[section_id]
            section["edited_by_clinician"] = False
            section["revision_type"] = "AI-assisted demo revision"
            section["last_instruction"] = instruction.strip() or "Make this clearer"
            break
    updated["version"] = int(updated.get("version", 1)) + 1
    return updated


def get_sources(case_data: CaseData, source_ids: list[str]) -> list[dict[str, str]]:
    """Resolve source identifiers for clinician-only evidence display."""
    wanted = set(source_ids)
    return [
        deepcopy(source)
        for source in case_data["sources"]
        if source["id"] in wanted
    ]
