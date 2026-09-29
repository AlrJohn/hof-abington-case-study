# Azra Clinical Trial Outreach Case Study

This project explores a clinician-reviewed outreach layer for patients whom Azra has already identified as possible clinical-trial candidates. The prototype turns supplied patient, trial, and match information into a personalized plain-language **Why Me** message while keeping clinical staff in control of what is sent.

## The problem

Clinical-trial information is often medically complex, and research teams may need to translate the same material repeatedly for different patients. A patient receiving outreach needs a clear explanation of:

- Why the care or research team is contacting them
- Why the study may be relevant to them
- What the study examines
- What participation could involve
- What questions they may want to ask

This project begins **after** Azra has surfaced a possible patient-to-trial match. It does not reproduce Azra's matching process or determine whether a patient is eligible.

## Proposed solution

The prototype generates a structured patient message grounded only in supplied facts. A clinician can review the draft, inspect the source behind patient-specific statements, revise individual sections, approve the message, and simulate sending it. The patient then sees a clean version without clinician-only evidence controls.

The core differentiators are:

- Patient-specific explanations instead of a generic trial summary
- Source references for patient-specific statements
- Clinician editing and approval before simulated delivery
- Separate clinician and patient views of the same outreach
- Structured LLM output that can be validated before display

## Planned demonstration flow

1. Open a queue of synthetic trial candidates.
2. Select one patient who has already been matched to a trial.
3. Review the supplied patient facts, trial details, and match context.
4. Generate the structured Why Me outreach.
5. Inspect the evidence supporting a patient-specific statement.
6. Edit the message or request a targeted rewrite of one section.
7. Approve and simulate sending the message.
8. Switch to the patient-facing view.

## Technical approach

The proof of concept is intentionally small: one fully working synthetic patient and one trial.

- **Patient data:** Synthetic, FHIR-shaped JSON
- **Trial data:** A real public or realistic trial represented as JSON
- **Match context:** Structured criteria or characteristics supplied as an existing match
- **Backend:** A lightweight Python service using Flask or FastAPI
- **Generation:** An LLM API constrained to supplied facts and structured output
- **Traceability:** Source IDs attached to patient-specific statements
- **Interface:** Simple HTML, CSS, and JavaScript, or Streamlit
- **State:** In-memory or local JSON status tracking for the demo
- **Delivery:** Mocked approval, sending, and patient-portal experience

The exact framework and setup commands will be documented once implementation begins.

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

The prototype is intended to demonstrate clearer patient outreach and reduced manual rewriting. A future pilot could measure patient-reported clarity, reading level, clinician preparation time, approval rates, and common clinician edits. Enrollment and retention outcomes would require separate real-world evaluation.

## Project status

The project is currently in the planning and initial setup stage. The research-backed working plan is available in [Azra Team Working Plan V3](./Azra_Team_Working_Plan_V3.docx). The reasoning behind the revisions is documented in [Why I Changed the Azra Working Plan for V3](./Azra_Working_Plan_V3_Change_Rationale.md).

## Contributors

Penn State and Hof University case competition team.
