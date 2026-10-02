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


def _first_name(patient: dict[str, Any]) -> str:
    display_name = str(patient.get("display_name", "Maria")).strip()
    cleaned_name = display_name.removesuffix(" (Synthetic)").strip()
    return cleaned_name.split()[0] if cleaned_name else "there"


def _screening_label(patient: dict[str, Any]) -> str:
    screening = patient.get("screening", {})
    cervical_due = screening.get("cervical_screening_out_of_date") is True
    colorectal_due = screening.get("colorectal_screening_out_of_date") is True
    if cervical_due and colorectal_due:
        return "cervical and colorectal cancer screening"
    if cervical_due:
        return "cervical cancer screening"
    if colorectal_due:
        return "colorectal cancer screening"
    return "recommended cancer screening"


def _community_label(patient: dict[str, Any]) -> str:
    location = patient.get("location", {})
    if location.get("rural") and location.get("state") == "PA":
        return "rural Pennsylvania communities"
    if location.get("rural"):
        return "rural communities"
    return "communities like yours"


def _match_label(match: dict[str, Any]) -> str:
    return str(match.get("match_status", "POTENTIAL_MATCH")).replace("_", " ").lower()


def generate_outreach(case_data: dict[str, Any]) -> dict[str, Any]:
    """
    Generate the five-section patient-facing outreach message.

    This function intentionally accepts case_data because that is the
    interface currently used by the CS2 views through data_adapter.py.
    """

    patient = _patient(case_data)
    trial = _trial(case_data)
    match = _match(case_data)

    patient_name = _first_name(patient)
    screening_label = _screening_label(patient)
    community_label = _community_label(patient)

    trial_id = trial.get(
        "trial_id",
        "NCT04471194"
    )

    trial_title = trial.get(
        "title",
        "Clinical trial"
    )

    match_status = _match_label(match)

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
                    f"message because you are due for {screening_label}. "
                    "A research study is "
                    "looking at ways to make these screenings easier "
                    f"for people in {community_label}."
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
                "title": "Why You May Be a Match",
                "text": (
                    f"The available information lists you as a {match_status} "
                    "for this study. "
                    "Your information indicates that you live in a "
                    f"rural Pennsylvania community and are due for {screening_label}. "
                    "A study team member must review your information and confirm "
                    "whether you are eligible before you can participate."
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
                    "If you are interested, a member of the study team can explain "
                    "the study, answer your questions, and confirm whether you are "
                    "eligible. Receiving this "
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


def _revision_variants(case_data: dict[str, Any]) -> dict[str, dict[str, str]]:
    """Build distinct, fact-grounded rewrites for each visible revision preset."""
    patient = _patient(case_data)
    patient_name = _first_name(patient)
    screening_label = _screening_label(patient)
    community_label = _community_label(patient)

    return {
        "why_me": {
            "easier": (
                f"{patient_name}, we are contacting you because you are due for {screening_label}. "
                f"This study is looking at ways to make screening easier in {community_label}."
            ),
            "shorter": (
                f"{patient_name}, this study may be relevant because you are due for "
                f"{screening_label}."
            ),
            "warmer": (
                f"Hello {patient_name}. We understand that cancer screening can bring up "
                f"questions. We are reaching out because you are due for {screening_label}, "
                "and this study is exploring ways to make "
                f"screening more convenient for people in {community_label}. You can take "
                "your time and ask the study team any questions you may have."
            ),
        },
        "about_study": {
            "easier": (
                "This study is looking at ways to help people complete cervical and "
                "colorectal cancer screening. It includes mailed tests and easy-to-read "
                "screening information."
            ),
            "shorter": (
                "This study is testing mailed materials that may make cervical and "
                "colorectal cancer screening easier."
            ),
            "warmer": (
                "The study team wants to make cancer screening easier and more comfortable "
                "for people in rural communities. The study offers information and mailed "
                "screening materials so participants can better understand their options."
            ),
        },
        "what_involves": {
            "easier": (
                "If you take part, you may receive screening information and testing "
                "materials by mail. One test checks for HPV, and the other is a stool "
                "test called FIT."
            ),
            "shorter": (
                "Participation may include mailed information, an HPV self-sampling kit, "
                "and a FIT stool test."
            ),
            "warmer": (
                "If you choose to take part, the study team will explain each step and "
                "answer your questions. You may receive screening information, an HPV "
                "self-sampling kit, and a FIT stool test by mail."
            ),
        },
        "eligibility": {
            "easier": (
                "The information available suggests that you may be a potential match for "
                "this study. A study team member still needs to review your information "
                "and confirm whether you can participate."
            ),
            "shorter": (
                "You may be a potential match, but the study team must confirm your eligibility."
            ),
            "warmer": (
                f"{patient_name}, your information suggests that this study may be worth "
                "learning about. This is only a potential match, and a study team member "
                "will carefully review the details with you before you make any decision."
            ),
        },
        "next_steps": {
            "easier": (
                "If you want to learn more, a study team member can answer your questions "
                "and check whether you are eligible. Asking for information does not mean "
                "you have to participate."
            ),
            "shorter": (
                "Contact the study team to ask questions; learning more does not require "
                "you to participate."
            ),
            "warmer": (
                f"{patient_name}, you are welcome to ask as many questions as you need. "
                "A study team member can explain the study and confirm whether you are "
                "eligible. Learning more is your choice and does not commit you to participate."
            ),
        },
    }


def regenerate_section(
    section_id: str,
    instruction: str,
    context: dict[str, Any],
    case_data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Regenerate only the requested section using deterministic demo variants."""
    message = deepcopy(context)
    if not isinstance(message, dict):
        raise ValueError("Invalid message context.")

    target = next(
        (section for section in message.get("sections", []) if section.get("id") == section_id),
        None,
    )
    if target is None:
        raise ValueError(f"Unknown message section: {section_id}")

    variants = _revision_variants(case_data or {})
    normalized = instruction.strip().lower()
    if normalized == "make this easier to understand":
        variant = "easier"
    elif normalized == "make this shorter":
        variant = "shorter"
    elif normalized == "make this sound warmer":
        variant = "warmer"
    elif "warm" in normalized:
        variant = "warmer"
    elif "short" in normalized:
        variant = "shorter"
    else:
        variant = "easier"

    original_sources = deepcopy(target.get("source_ids", []))
    target["text"] = variants[section_id][variant]
    target["source_ids"] = original_sources
    target["edited_by_clinician"] = False
    target["revision_type"] = "AI-assisted demo revision"
    target["last_instruction"] = instruction.strip()
    message["version"] = int(message.get("version", 1)) + 1

    validation = validate_message(message)
    if not validation["valid"]:
        raise ValueError(
            "Regenerated message failed validation: " + "; ".join(validation["errors"])
        )
    return message
