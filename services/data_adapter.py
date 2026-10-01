"""Fixture-backed boundary between the Streamlit views and outreach services.

The adapter owns the UI-facing shape. Source fixtures and the CS1 service modules
can evolve without requiring the Streamlit pages to understand their raw schemas.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from services.evaluation_service import evaluate_message as _evaluate_message
from services.outreach_service import (
    generate_outreach as _generate_outreach,
    regenerate_section as _regenerate_section,
    validate_message,
)


Candidate = dict[str, Any]
CaseData = dict[str, Any]
Message = dict[str, Any]
Evaluation = dict[str, Any]

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DEMO_CANDIDATE_ID = "MARIA-001"


def _load_fixture(filename: str) -> dict[str, Any]:
    """Load one checked-in JSON fixture and fail with a useful file-level error."""
    path = DATA_DIR / filename
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Unable to load demo fixture {path.name}: {exc}") from exc


def _location_label(patient: dict[str, Any]) -> str:
    location = patient.get("location", {})
    city = location.get("city")
    state = location.get("state")
    return ", ".join(value for value in (city, state) if value) or "Not provided"


def _build_case() -> CaseData:
    """Normalize all CS1-owned fixtures into the stable shape used by the UI."""
    patient = _load_fixture("patient.json")
    trial = _load_fixture("trial.json")
    match_evidence = _load_fixture("match_evidence.json")
    source_map = _load_fixture("source_map.json")

    patient_id = patient.get("patient_id")
    trial_id = trial.get("trial_id")
    if patient_id != DEMO_CANDIDATE_ID:
        raise ValueError(f"Expected patient {DEMO_CANDIDATE_ID}, found {patient_id!r}.")
    if match_evidence.get("patient_id") != patient_id:
        raise ValueError("Patient and match-evidence fixtures refer to different patients.")
    if match_evidence.get("trial_id") != trial_id:
        raise ValueError("Trial and match-evidence fixtures refer to different trials.")

    english = patient.get("communication", {}).get("english")
    candidate: Candidate = {
        "id": patient_id,
        "display_name": patient.get("display_name", patient_id),
        "trial_title": trial.get("title", trial_id),
        "status": "Ready for outreach",
        "priority": "Follow-up" if patient.get("engagement", {}).get("letter_received") else "Standard",
    }

    return {
        "candidate": candidate,
        "patient_summary": {
            "patient_id": patient_id,
            "display_name": patient.get("display_name", patient_id),
            "age_group": str(patient.get("age", "Not provided")),
            "condition": patient.get("condition", "Not provided"),
            "preferred_language": "English" if english else "Not provided",
            "location": _location_label(patient),
            "data_notice": patient.get(
                "data_notice",
                "Synthetic case-study patient. No real patient data.",
            ),
        },
        "trial_summary": {
            "trial_id": trial_id,
            "title": trial.get("title", trial_id),
            "phase": trial.get("phase", "Not provided"),
            "status": trial.get("status", "Not provided in cached fixture"),
            "organization": "Abington Hospital Research Team",
            "location": _location_label(patient),
            "source_url": trial.get("source", {}).get("url"),
        },
        "match_summary": {
            "summary": match_evidence.get("match_status", "Potential match")
            .replace("_", " ")
            .title(),
            "review_note": match_evidence.get("review_note", ""),
            "source_ids": sorted(
                {
                    source_id
                    for criterion in match_evidence.get("criteria", [])
                    for source_id in criterion.get("source_ids", [])
                }
            ),
        },
        "sources": source_map.get("sources", []),
        "patient": patient,
        "trial": trial,
        "match_evidence": match_evidence,
        "delivery": {
            "sender_name": "Abington Hospital Research Team",
            "health_system_name": "Abington Hospital",
            "verification_text": (
                "Use the Abington Hospital website or phone number you already trust "
                "to verify this message. Participation is voluntary."
            ),
        },
    }


def get_candidates(status: str = "Ready for outreach") -> list[Candidate]:
    """Return the fixture-backed candidate queue with current workflow status."""
    candidate = deepcopy(_build_case()["candidate"])
    candidate["status"] = status
    return [candidate]


def get_case(candidate_id: str) -> CaseData:
    """Return the normalized synthetic case selected by the clinician."""
    case_data = _build_case()
    if candidate_id != case_data["candidate"]["id"]:
        raise ValueError(f"Unknown synthetic candidate: {candidate_id}")
    return case_data


def generate_outreach(case_data: CaseData) -> Message:
    """Generate and validate an outreach draft through the CS1 service."""
    message = _generate_outreach(deepcopy(case_data))
    validation = validate_message(message)
    if not validation["valid"]:
        raise ValueError("Generated message is invalid: " + "; ".join(validation["errors"]))
    return message


def evaluate_message(message: Message) -> Evaluation:
    """Evaluate the current draft through the CS1 comprehension service."""
    return _evaluate_message(deepcopy(message))


def regenerate_section(
    section_id: str,
    instruction: str,
    message: Message,
) -> Message:
    """Regenerate one section through the CS1 service boundary."""
    return _regenerate_section(section_id, instruction, deepcopy(message))


def get_sources(case_data: CaseData, source_ids: list[str]) -> list[dict[str, str]]:
    """Resolve source identifiers for clinician-only evidence display."""
    wanted = set(source_ids)
    return [
        deepcopy(source)
        for source in case_data["sources"]
        if source.get("id") in wanted
    ]
