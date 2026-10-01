"""Streamlit AppTest coverage for the fixture-backed workflow."""

import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parent.parent


def find_button(app: AppTest, label: str):
    """Return a button by its visible label with a useful failure message."""
    for button in app.button:
        if button.label == label:
            return button
    raise AssertionError(f"Button not found: {label}")


class StreamlitWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = AppTest.from_file(ROOT / "app.py", default_timeout=10).run()
        self.assertFalse(self.app.exception)

    def test_initial_queue_and_locked_patient_preview(self) -> None:
        rendered_markdown = "\n".join(element.value for element in self.app.markdown)
        self.assertIn("Candidate Queue", rendered_markdown)
        self.assertIn("Maria Reyes (Synthetic)", rendered_markdown)
        self.assertEqual(self.app.session_state["workflow_status"], "Ready for outreach")

        self.app.switch_page("views/patient_preview.py").run()
        self.assertFalse(self.app.exception)
        warnings = [warning.value for warning in self.app.warning]
        self.assertTrue(any("locked" in warning for warning in warnings))

    def test_generate_review_approve_and_send(self) -> None:
        self.app.switch_page("views/clinician_review.py").run()
        find_button(self.app, "Generate outreach").click().run()
        self.assertFalse(self.app.exception)
        self.assertEqual(len(self.app.text_area), 5)
        self.assertEqual(self.app.session_state["workflow_status"], "Draft")
        self.assertEqual(self.app.session_state["message"]["patient_id"], "MARIA-001")

        find_button(self.app, "Approve message").click().run()
        self.assertFalse(self.app.exception)
        self.assertTrue(self.app.session_state["approved"])

        # Approval routes directly to the patient page in the real application.
        self.app.switch_page("views/patient_preview.py").run()
        rendered_markdown = "\n".join(element.value for element in self.app.markdown)
        self.assertIn("Maria Reyes (Synthetic)", rendered_markdown)
        self.assertNotIn("Jordan Lee", rendered_markdown)
        find_button(self.app, "Simulate send").click().run()
        self.assertFalse(self.app.exception)
        self.assertTrue(self.app.session_state["sent"])
        self.assertEqual(self.app.session_state["workflow_status"], "Sent")


if __name__ == "__main__":
    unittest.main()
