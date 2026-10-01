# Prototype Data

This directory contains synthetic and publicly available fixture data for the Streamlit prototype. No real patient data or PHI belongs here.

The fixtures are loaded by `services/data_adapter.py`, which validates the patient/trial identifiers and exposes a stable shape to the Streamlit views.

Expected fixtures:

- `patient.json`: one synthetic patient
- `trial.json`: one cached public clinical-trial record
- `match_evidence.json`: one mock Azra match-evidence object
- `source_map.json`: approved sources and identifiers used for traceability
- `generated_message.json`: one known-good five-section outreach response
- `evaluation.json`: one known-good comprehension-evaluation response

`generated_message.json` and `evaluation.json` are known-good contract examples. Runtime generation, targeted revision, and evaluation route through the service modules so their integration is exercised in the demo.
