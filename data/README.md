# Prototype Data

This directory will contain synthetic and publicly available fixture data for the Streamlit prototype. No real patient data or PHI belongs here.

The fixture contents are work to be done by CS1. Business 3 will help CS1 confirm the approved source material and patient-facing content rules.

Expected fixtures:

- `patient.json`: one synthetic patient
- `trial.json`: one cached public clinical-trial record
- `match_evidence.json`: one mock Azra match-evidence object
- `source_map.json`: approved sources and identifiers used for traceability
- `generated_message.json`: one known-good five-section outreach response
- `evaluation.json`: one known-good comprehension-evaluation response

CS2 may use these files through `services/data_adapter.py` once UI implementation begins.
