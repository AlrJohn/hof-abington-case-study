# Demo Readiness Audit

Updated: October 1, 2026

## Current result

The synthetic Maria Reyes / NCT04471194 path is connected end to end in Streamlit:

1. The candidate queue is built from `data/patient.json` and `data/trial.json`.
2. Clinician review shows patient, trial, match, and source-map fixture content.
3. Message generation, evaluation, and targeted revision call the CS1 service modules through `services/data_adapter.py`.
4. Approval carries the same message and selected patient into the patient preview.
5. Patient-facing sender and patient labels are derived from the selected case rather than the retired Jordan Lee example.
6. Known-good message and evaluation fixtures are contract-tested against runtime service output.
7. Sending is intentionally simulated.

## Must finalize before the stakeholder demo

### 1. Confirm trial facts and recruitment status

The cached trial fixture includes the title, phase, study type, population, eligibility criteria, and interventions, but it does not include recruitment status, sponsor, enrollment, dates, study locations, or contacts. Confirm the current [ClinicalTrials.gov record](https://clinicaltrials.gov/study/NCT04471194) immediately before the demo and add an `as_of` timestamp. Do not imply that a patient can enroll based on a stale or incomplete cached record.

Owner: clinical/business content lead with CS1 support.

### 2. Approve sender identity and patient contact path

`Abington Hospital Research Team` and the verification guidance are currently demo configuration assembled in the adapter, not approved source data. Add structured organization data with the correct health-system name, research-team name, portal URL, phone number, hours, and escalation contact. The patient preview should not be presented as send-ready until those values are approved.

Owner: Abington/business stakeholder.

### 3. Clarify match-evidence semantics

The exclusion criteria currently combine a negatively worded description (for example, “No partial or complete hysterectomy”) with `patient_value: false` and `matched: true`. That is ambiguous even though the underlying synthetic medical-history field is clear. Replace this with explicit fields such as `criterion_met`, `observed_fact`, and `evidence_source_ids`, then validate that every criterion maps to an actual patient or source field.

Owner: CS1/Azra integration owner.

### 4. Complete clinician content and safety review

The generated copy is deterministic and source-linked, but a clinician should approve the exact language about overdue screening, preliminary eligibility, HPV self-sampling, FIT testing, voluntariness, privacy, costs, risks, benefits, and what happens after a patient responds. Confirm that only the minimum necessary patient-specific detail appears in outreach.

Owner: clinician/research operations lead.

### 5. Rehearse and freeze the demo fixture

Run the full test command, open all three views, exercise a manual edit and targeted revision, approve, preview each channel, simulate send, and reset. Freeze the reviewed JSON fixtures after this rehearsal so copy does not drift on demo day.

Owner: demo lead.

## Needed to replace demo fixtures with real integrations

| Area | Connected now | Still needed for real data |
|---|---|---|
| Patient context | One checked-in synthetic JSON record | Authorized EHR/FHIR or approved export, field mapping, consent/legal basis, minimum-necessary filtering, and test/sandbox records |
| Trial data | Cached subset with a ClinicalTrials.gov link | ClinicalTrials.gov API refresh, full normalized study schema, freshness timestamp, unavailable/stale handling, and site/contact validation |
| Match evidence | One mock potential-match object | Azra match API/export contract, stable identifiers, evidence provenance, confidence/status semantics, and reconciliation with patient/trial IDs |
| Outreach generation | Deterministic Python service | Approved prompt/content policy or template engine, structured output validation, model/version tracking, failure handling, and grounding checks |
| Comprehension evaluation | Deterministic keyword/rubric service | Validated scoring rules, threshold policy, explainable issue mapping, versioning, and human-review signoff |
| Workflow state | Streamlit session memory | Authentication, roles, durable storage, concurrency controls, message-version approval records, and audit history |
| Delivery | Channel preview and simulated send | Patient portal/SMS/email sandbox, approved templates, consent/preferences, opt-out handling, delivery receipts, retries, and failure escalation |
| Security/privacy | Synthetic data boundary and ignored private-data paths | Secrets management, encryption, access logging, retention/deletion policy, risk review, HIPAA/security assessment, and incident procedures |

## Known prototype limitations

- This app does not determine eligibility; it starts from a supplied potential match.
- The patient and match records are synthetic and must stay clearly labeled.
- Custom regeneration is not a language-model call; unsupported instructions are appended as a visible demo marker and require clinician review.
- The rubric is a deterministic prototype, not evidence that a patient understood the message.
- There is one candidate and one trial; multi-record queue behavior, filtering, pagination, and concurrent review are not implemented.
- Refreshing the browser or restarting the app loses workflow state.
- No external patient message is sent.

## Verification completed

- Seven automated tests pass, including the Streamlit queue-to-send workflow.
- Python compilation succeeds for the app, services, views, and tests.
- `git diff --check` reports no whitespace errors.
- Regression checks cover Maria/trial identifier propagation, source resolution, targeted revision isolation, fixture/service contract parity, preview identity, approval, and simulated send.
