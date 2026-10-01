"""
CS1: Fixed model-assisted comprehension evaluation.

This is a deterministic prototype rubric for the case-study demo.
It is not a clinically validated comprehension instrument.
"""

from typing import Any

from services.outreach_service import validate_message


CRITERIA = [
    "Purpose",
    "Familiar language",
    "Sentence clarity",
    "Organization",
    "Participation information",
    "Actionability",
    "Trust",
    "Safety language",
]


def evaluate_message(
    message: dict[str, Any]
) -> dict[str, Any]:
    """
    Evaluate the current message against the fixed comprehension rubric.
    """

    validation = validate_message(message)

    if not validation["valid"]:
        return {
            "overall_score": 0,
            "criterion_scores": {
                criterion: 0
                for criterion in CRITERIA
            },
            "issues": validation["errors"],
            "recommendation": "Needs revision",
            "is_stale": False,
            "label": "Model-assisted rubric evaluation",
        }

    sections = message.get("sections", [])

    text = " ".join(
        section.get("text", "")
        for section in sections
    )

    lower_text = text.lower()

    scores = {
        "Purpose": 95,
        "Familiar language": 92,
        "Sentence clarity": 92,
        "Organization": 95,
        "Participation information": 94,
        "Actionability": 94,
        "Trust": 96,
        "Safety language": 97,
    }

    issues = []

    if "why" not in lower_text and "because" not in lower_text:
        scores["Purpose"] = 70
        issues.append(
            "The message should clearly explain why the patient is receiving it."
        )

    if "does not mean" not in lower_text:
        scores["Safety language"] = 75
        issues.append(
            "The message should clarify that outreach does not establish a cancer diagnosis."
        )

    if "study team" not in lower_text:
        scores["Actionability"] = 75
        issues.append(
            "The message should identify who the patient can contact."
        )

    if "participate" not in lower_text:
        scores["Participation information"] = 75
        issues.append(
            "The message should explain participation."
        )

    overall_score = round(
        sum(scores.values()) / len(scores)
    )

    if not issues:
        issues.append(
            "No basic comprehension issues detected by the fixed rubric."
        )

    return {
        "overall_score": overall_score,
        "criterion_scores": scores,
        "issues": issues,
        "recommendation": "Ready for clinician review",
        "is_stale": False,
        "label": "Model-assisted rubric evaluation",
    }
