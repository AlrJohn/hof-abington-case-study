"""
CS1: Outreach generation and targeted section regeneration.

This module is designed to work with the existing CS2 data_adapter
interface. It accepts the normalized case_data dictionary used by
the current Streamlit UI.
"""

from copy import deepcopy
from typing import Any


REQUIRED_SECTION_IDS = [
    "why_me",
    "about_study",
    "what_involves",
    "eligibility",
    "next_steps",
]


def _patient(case_data: dict[str, Any]) -> dict[str, Any]:
    return case_data.get("patient", {})


def _trial(case_data: dict[str, Any]) -> dict[str, Any]:
    return case_data.get("trial", {})


def _match(case_data: dict[str, Any]) -> dict[str, Any]:
    return case_data.get("match_evidence", {})


def generate_outreach(case_data: dict[str, Any]) -> dict[str, Any]:
    """
    Generate the five-section patient-facing outreach message.

    This function intentionally accepts case_data because that is the
    interface currently used by the CS2 views through data_adapter.py.
    """

    patient = _patient(case_data)
    trial = _trial(case_data)
    match = _match(case_data)

    display_name = patient.get(
        "display_name",
        "Maria Reyes (Synthetic)"
    )
    patient_name = display_name.removesuffix(" (Synthetic)").split()[0]

    trial_id = trial.get(
        "trial_id",
        "NCT04471194"
    )

    trial_title = trial.get(
        "title",
        "Clinical trial"
    )

    match_status = match.get(
        "match_status",
        "POTENTIAL_MATCH"
    )

    return {
        "version": 1,
        "trial_id": trial_id,
        "patient_id": patient.get(
            "patient_id",
            "MARIA-001"
        ),
        "sections": [
            {
                "id": "why_me",
                "title": "Why Me",
                "text": (
                    f"Hello {patient_name}. You may be receiving this "
                    "message because you are due for cervical and "
                    "colorectal cancer screening. A research study is "
                    "looking at ways to make these screenings easier "
                    "for people in rural communities."
                ),
                "source_ids": [
                    "SRC-TRIAL",
                    "SRC-ELIGIBILITY",
                    "SRC-PATIENT"
                ],
                "edited_by_clinician": False,
            },
            {
                "id": "about_study",
                "title": "About the Study",
                "text": (
                    f"The study is called \"{trial_title}.\" "
                    "It is studying ways to help people complete "
                    "cervical and colorectal cancer screening, "
                    "including self-sampling and educational materials."
                ),
                "source_ids": [
                    "SRC-TRIAL",
                    "SRC-INTERVENTION"
                ],
                "edited_by_clinician": False,
            },
            {
                "id": "what_involves",
                "title": "What Participation Involves",
                "text": (
                    "If you take part, you may receive information "
                    "about cancer screening and mailed screening "
                    "materials. The study includes cervical cancer "
                    "screening using an HPV self-sampling approach "
                    "and colorectal cancer screening using a FIT test."
                ),
                "source_ids": [
                    "SRC-INTERVENTION"
                ],
                "edited_by_clinician": False,
            },
            {
                "id": "eligibility",
                "title": "Why You Are a Perfect Match",
                "text": (
                    f"The available information lists your preliminary "
                    f"study match as perfect
                    "\" Your information indicates that you live in a "
                    "rural Pennsylvania community and are overdue for "
                    "both cervical and colorectal cancer screening. "
                    "A study team member must confirm your eligibility "
                    "before you can participate."
                    
                ),
                "source_ids": [
                    "SRC-ELIGIBILITY",
                    "SRC-EXCLUSION",
                    "SRC-PATIENT"
                ],
                "edited_by_clinician": False,
            },
            {
                "id": "next_steps",
                "title": "Next Steps",
                "text": (
                    "If you are interested, a member of the study team "
                    "can explain the study, answer your questions, and "
                    "confirm whether you are eligible. Receiving this "
                    "message does not mean that you have cancer, and "
                    "you do not have to participate."
                ),
                "source_ids": [
                    "SRC-TRIAL",
                    "SRC-ELIGIBILITY",
                    "SRC-PATIENT"
                ],
                "edited_by_clinician": False,
            },
        ],
    }


def validate_message(message: dict[str, Any]) -> dict[str, Any]:
    """
    Basic CS1 response-structure validation.
    """

    errors = []

    if not isinstance(message, dict):
        return {
            "valid": False,
            "errors": ["Message must be a dictionary."],
        }

    sections = message.get("sections")

    if not isinstance(sections, list):
        return {
            "valid": False,
            "errors": ["Message must contain a sections list."],
        }

    section_ids = [section.get("id") for section in sections]

    for required_id in REQUIRED_SECTION_IDS:
        if required_id not in section_ids:
            errors.append(
                f"Missing required section: {required_id}"
            )

    for section in sections:
        section_id = section.get("id", "unknown")

        if not section.get("title"):
            errors.append(
                f"{section_id}: missing title."
            )

        if not section.get("text"):
            errors.append(
                f"{section_id}: missing text."
            )

        if not section.get("source_ids"):
            errors.append(
                f"{section_id}: missing source IDs."
            )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
    }


def regenerate_section(
    section_id: str,
    instruction: str,
    context: dict[str, Any],
) -> dict[str, Any]:
    """
    Regenerate only the requested section.

    The existing CS2 code passes the current message as context.
    """

    message = deepcopy(context)

    if not isinstance(message, dict):
        raise ValueError("Invalid message context.")

    sections = message.get("sections", [])

    target = None

    for section in sections:
        if section.get("id") == section_id:
            target = section
            break

    if target is None:
        raise ValueError(
            f"Unknown message section: {section_id}"
        )

    original_sources = deepcopy(
        target.get("source_ids", [])
    )

    normalized = instruction.strip().lower()

    original_text = target.get("text", "")

    if normalized == "make this easier to understand":
        if section_id == "why_me":
            new_text = (
                "You may be receiving this message because you are "
                "due for cervical and colorectal cancer screening. "
                "This study is looking at ways to make screening "
                "easier for people in rural communities."
            )

        elif section_id == "about_study":
            new_text = (
                "This study is looking at ways to help people get "
                "cancer screening. It includes information about "
                "cervical and colorectal cancer screening and may "
                "include mailed testing materials."
            )

        elif section_id == "what_involves":
            new_text = (
                "If you take part, you may receive screening "
                "information and testing materials by mail. "
                "One test looks for HPV, and another is a stool "
                "test called FIT."
            )

        elif section_id == "eligibility":
            new_text = (
                "The information available suggests that you may "
                "be a possible match for this study. A study team "
                "member still needs to check your information and "
                "confirm whether you can participate."
            )

        elif section_id == "next_steps":
            new_text = (
                "If you are interested, a study team member can "
                "answer your questions and check whether you can "
                "take part. You do not have to participate."
            )

        else:
            new_text = original_text

    elif normalized == "make this shorter":
        sentences = [
            sentence.strip()
            for sentence in original_text.split(".")
            if sentence.strip()
        ]

        if len(sentences) > 1:
            new_text = sentences[0] + "."
        else:
            words = original_text.split()
            new_text = " ".join(words[:24]).rstrip(".,;:") + "."

    elif normalized == "make this sound warmer":
        new_text = (
            original_text
            + " Please feel free to ask the study team any "
            "questions you may have."
        )

    else:
        new_text = (
            original_text
            + f"\n\n[Requested revision: {instruction}]"
        )

    target["text"] = new_text
    target["source_ids"] = original_sources
    target["edited_by_clinician"] = False
    target["revision_type"] = "AI-assisted demo revision"

    message["version"] = int(
        message.get("version", 1)
    ) + 1

    validation = validate_message(message)

    if not validation["valid"]:
        raise ValueError(
            "Regenerated message failed validation: "
            + "; ".join(validation["errors"])
        )

    return message
