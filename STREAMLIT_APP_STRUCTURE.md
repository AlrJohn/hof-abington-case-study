# Streamlit Application Structure

This structure separates the implemented CS2 interface from the CS1-owned generation and evaluation work. The application now loads the CS1 fixtures and routes deterministic generation, evaluation, and targeted revision through the CS1 services via the adapter.

```text
Hof_Abington_Case_Study/
|-- app.py                         CS2: Streamlit entry point
|-- requirements.txt              Shared: pinned runtime dependency
|-- AZRA_UI_RESEARCH.md            CS2: public-reference design decisions
|-- .streamlit/
|   `-- config.toml                CS2: theme and application settings
|-- assets/
|   `-- styles.css                 CS2: Azra-inspired presentation styling
|-- data/
|   |-- README.md                  Fixture rules and ownership
|   |-- patient.json               CS1: synthetic patient fixture
|   |-- trial.json                 CS1: cached public trial fixture
|   |-- match_evidence.json        CS1: mock Azra match evidence
|   |-- source_map.json            CS1: approved source identifiers
|   |-- generated_message.json     CS1: known-good outreach response
|   `-- evaluation.json            CS1: known-good evaluation response
|-- services/
|   |-- __init__.py
|   |-- outreach_service.py        CS1: generation and regeneration
|   |-- evaluation_service.py      CS1: comprehension evaluation
|   |-- data_adapter.py            CS2: stable UI-facing data shape and demo behavior
|   `-- ui_state.py                CS2: workflow state transitions
|-- views/
|   |-- __init__.py
|   |-- components.py              CS2: reusable presentation helpers
|   |-- candidate_queue.py         CS2: queue and status
|   |-- clinician_review.py        CS2: review and approval workflow
|   `-- patient_preview.py         CS2: patient preview and simulated send
`-- tests/
    |-- test_app.py                CS2: Streamlit page and workflow checks
    `-- test_data_adapter.py       CS2: adapter and state-transition checks
```

## Ownership Boundary

CS1 owns the fixture contents and the deterministic functions that generate, evaluate, and regenerate outreach. CS2 consumes those capabilities only through the adapter.

CS2 owns the Streamlit entry point, view modules, UI state, presentation styling, and the adapter that shields the views from changes in CS1's response format.

## Integration Boundary

During CS1 integration, the views should continue to use this small set of adapter operations:

```text
generate_outreach(patient, trial, match_evidence)
evaluate_message(message)
regenerate_section(section_id, instruction, context)
```

`services/data_adapter.py` normalizes data before it reaches a view. This lets CS2 run against deterministic demo data while CS1 completes the live functions, and it limits later schema changes to one place.

## Current State

The complete synthetic Maria Reyes / NCT04471194 case is connected end to end. The adapter loads patient, trial, match, and source fixtures, while runtime message operations call the CS1 service modules. The services remain deterministic prototype implementations; no EHR, live ClinicalTrials.gov feed, language model, delivery system, authentication, or durable database is connected.
