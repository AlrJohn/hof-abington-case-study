# Azra Clinical Trial Outreach Case Study

This project explores a clinician-reviewed outreach layer for patients whom Azra has already identified as possible clinical-trial candidates. The prototype turns supplied patient, trial, and match information into a short plain-language message, checks it against a fixed comprehension rubric, and keeps clinical staff in control of what is sent.

## The problem

Clinical-trial information is often medically complex, and research teams may need to translate the same material repeatedly for different patients. A patient receiving outreach needs a clear explanation of:

- Why the care or research team is contacting them
- Why the study may be relevant to them
- What the study examines
- What participation could involve
- What questions they may want to ask

This project begins **after** Azra has surfaced a possible patient-to-trial match. It does not reproduce Azra's matching process or determine whether a patient is eligible.

## Proposed solution

The prototype generates a structured patient message grounded only in supplied facts. It limits patient-specific detail to what is needed to explain the outreach, then applies a fixed PEMAT-informed evaluation for purpose, language, organization, actionability, trust, and safety wording. A clinician can inspect the sources, revise individual sections, approve the message, select a delivery concept, and simulate sending it. The patient sees a clean version without internal match evidence or clinician-only controls.

The core differentiators are:

- Limited patient-specific context instead of a generic trial summary or a list of sensitive match criteria
- Source references for patient-specific statements
- A fixed model-assisted comprehension evaluation with structured results
- Clinician editing and approval before simulated delivery
- Separate clinician and patient views of the same outreach
- Trust cues and channel-aware delivery previews
- Structured LLM output that can be validated before display

## Planned demonstration flow

1. Open a queue of synthetic trial candidates.
2. Select one patient who has already been matched to a trial.
3. Review the supplied patient facts, trial details, and match context.
4. Generate the structured five-section outreach.
5. Review the model-assisted comprehension score and issue list.
6. Inspect the evidence supporting a patient-specific statement.
7. Edit the message or request a targeted rewrite of one section.
8. Approve the message and select a delivery concept.
9. Switch to the patient-facing view and simulate sending it.

## Technical approach

The proof of concept is intentionally small: one fully working synthetic patient and one trial.

- **Patient data:** Synthetic, FHIR-shaped JSON
- **Trial data:** A real public or realistic trial represented as JSON
- **Match context:** Structured criteria or characteristics supplied as an existing match
- **Application:** Streamlit is the default for the compressed build unless the team has already agreed on another framework
- **Generation:** An LLM API constrained to supplied facts and structured output
- **Evaluation:** A second fixed PEMAT-informed prompt returning scores, issues, and a recommendation
- **Traceability:** Source IDs attached to patient-specific statements
- **Interface:** One clinician workflow and one patient-facing preview built in the same application
- **State:** In-memory or local JSON status tracking for the demo
- **Delivery:** Mocked channel selection, approval, sending, and patient-facing experience

The CS2 interface is implemented as a Streamlit prototype. Generation, evaluation, regeneration, and sending currently use deterministic simulated behavior until CS1 connects the corresponding services.

## Run the prototype

Use Python 3.11 or newer from the project directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

Run the automated tests with:

```powershell
python -m unittest discover -s tests -v
```

The interface design decisions and public Azra references are documented in [Azra-Inspired UI Research](./AZRA_UI_RESEARCH.md).

## Scope and safety boundaries

This repository is for a case-study prototype and is **not intended for clinical use**.

The prototype will not:

- Match patients to trials
- Determine final eligibility
- Replace a clinician, research team, or informed-consent process
- Use real patient data
- Connect to a live EHR, hospital FHIR server, or patient portal
- Implement production HIPAA, privacy, or security controls
- Claim improved enrollment, retention, or clinical outcomes

All patient information used for development and demonstration must be synthetic. Secrets, API credentials, private data, local databases, and runtime artifacts are excluded through the repository's `.gitignore`.

## Success measures

The prototype is intended to demonstrate a repeatable method for preparing and reviewing clearer patient outreach. Its comprehension result is a model-assisted rubric score, not proof that a patient understood the message. A future pilot could measure patient-reported clarity, clinician preparation time, approval rates, and common clinician edits. Enrollment, retention, and real patient comprehension would require separate evaluation.

## Project status

No code had been started as of Wednesday, September 30. The team is now following a compressed, fixture-first build plan focused on one complete demo path. The current working plan is [Azra Team Working Plan V4](./Azra_Team_Working_Plan_V4.docx), and the immediate assignments are in the [Wednesday Recovery Task Plan](./Azra_Wednesday_Recovery_Task_Plan.md). The prior [V3 change rationale](./Azra_Working_Plan_V3_Change_Rationale.md) remains available for the research decisions that preceded the September 29 update.

The Streamlit project structure and CS1/CS2 ownership boundary are documented in [Streamlit Application Structure](./STREAMLIT_APP_STRUCTURE.md). CS1-owned fixture and service placeholders remain unchanged. CS2-owned views run against deterministic demo behavior in `services/data_adapter.py` so the complete interface can be tested before service integration.

### CS1 integration boundary

The views call only the CS2 adapter. When CS1's implementation is ready, connect these operations inside `services/data_adapter.py` without rewriting the Streamlit pages:

- `generate_outreach(patient, trial, match_evidence)`
- `evaluate_message(message)`
- `regenerate_section(section_id, instruction, context)`

## Contributors

Penn State and Hof University case competition team.
