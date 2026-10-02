"""Unit tests for deterministic demo data and workflow state."""

import json
import unittest
from pathlib import Path

from services.data_adapter import (
    DEMO_CANDIDATE_ID,
    evaluate_message,
    generate_outreach,
    get_candidates,
    get_case,
    regenerate_section,
)
from services.ui_state import approve_message, initialize_state, mark_message_changed, mark_sent, reset_demo


class DataAdapterTests(unittest.TestCase):
    def test_normalized_demo_model(self) -> None:
        candidate = get_candidates()[0]
        case_data = get_case(DEMO_CANDIDATE_ID)
        message = generate_outreach(case_data)
        evaluation = evaluate_message(message)

        self.assertEqual(candidate["id"], DEMO_CANDIDATE_ID)
        self.assertEqual(candidate["display_name"], "Maria Reyes")
        self.assertEqual(case_data["patient"]["age"], 54)
        self.assertEqual(case_data["trial"]["trial_id"], "NCT04471194")
        self.assertEqual(case_data["match_evidence"]["patient_id"], DEMO_CANDIDATE_ID)
        self.assertEqual(len(message["sections"]), 5)
        self.assertEqual(message["patient_id"], DEMO_CANDIDATE_ID)
        self.assertEqual(message["trial_id"], "NCT04471194")
        self.assertTrue(all(section["source_ids"] for section in message["sections"]))
        self.assertIn("overall_score", evaluation)
        self.assertIn("criterion_scores", evaluation)
        self.assertFalse(evaluation["is_stale"])

    def test_targeted_regeneration_changes_only_selected_section(self) -> None:
        message = generate_outreach(get_case(DEMO_CANDIDATE_ID))
        original = {section["id"]: section["text"] for section in message["sections"]}
        updated = regenerate_section("what_involves", "Make this shorter", message)
        revised = {section["id"]: section["text"] for section in updated["sections"]}

        self.assertNotEqual(original["what_involves"], revised["what_involves"])
        for section_id in original:
            if section_id != "what_involves":
                self.assertEqual(original[section_id], revised[section_id])

    def test_each_revision_preset_changes_each_selected_section(self) -> None:
        message = generate_outreach(get_case(DEMO_CANDIDATE_ID))
        original_text = {
            section["id"]: section["text"]
            for section in message["sections"]
        }
        instructions = (
            "Make this easier to understand",
            "Make this shorter",
            "Make this sound warmer",
        )

        for section in message["sections"]:
            for instruction in instructions:
                with self.subTest(section=section["id"], instruction=instruction):
                    updated = regenerate_section(section["id"], instruction, message)
                    updated_by_id = {
                        item["id"]: item
                        for item in updated["sections"]
                    }
                    revised = updated_by_id[section["id"]]

                    self.assertNotEqual(revised["text"], original_text[section["id"]])
                    self.assertEqual(revised["source_ids"], section["source_ids"])
                    self.assertEqual(revised["last_instruction"], instruction)
                    for other_id, other_text in original_text.items():
                        if other_id != section["id"]:
                            self.assertEqual(updated_by_id[other_id]["text"], other_text)

    def test_warmer_why_me_is_personalized_and_safe(self) -> None:
        message = generate_outreach(get_case(DEMO_CANDIDATE_ID))
        updated = regenerate_section("why_me", "Make this sound warmer", message)
        why_me = next(
            section for section in updated["sections"] if section["id"] == "why_me"
        )

        self.assertIn("Hello Maria", why_me["text"])
        self.assertIn("bring up questions", why_me["text"])
        self.assertNotIn("perfect match", why_me["text"].lower())

    def test_sources_are_resolved_from_fixture(self) -> None:
        case_data = get_case(DEMO_CANDIDATE_ID)
        source_ids = {source["id"] for source in case_data["sources"]}
        message = generate_outreach(case_data)

        for section in message["sections"]:
            self.assertTrue(set(section["source_ids"]).issubset(source_ids))

    def test_known_good_contract_fixtures_match_runtime_services(self) -> None:
        data_dir = Path(__file__).resolve().parent.parent / "data"
        expected_message = json.loads(
            (data_dir / "generated_message.json").read_text(encoding="utf-8")
        )
        expected_evaluation = json.loads(
            (data_dir / "evaluation.json").read_text(encoding="utf-8")
        )

        message = generate_outreach(get_case(DEMO_CANDIDATE_ID))
        self.assertEqual(message, expected_message)
        self.assertEqual(evaluate_message(message), expected_evaluation)

    def test_state_transitions_and_reset(self) -> None:
        state: dict = {}
        initialize_state(state)
        self.assertEqual(state["workflow_status"], "Ready for outreach")

        state["evaluation"] = {"is_stale": False}
        approve_message(state)
        self.assertTrue(state["approved"])

        mark_message_changed(state)
        self.assertFalse(state["approved"])
        self.assertTrue(state["evaluation"]["is_stale"])
        self.assertEqual(state["workflow_status"], "Needs review")

        approve_message(state)
        mark_sent(state)
        self.assertEqual(state["workflow_status"], "Sent")

        reset_demo(state)
        self.assertIsNone(state["message"])
        self.assertFalse(state["approved"])
        self.assertEqual(state["workflow_status"], "Ready for outreach")


if __name__ == "__main__":
    unittest.main()
