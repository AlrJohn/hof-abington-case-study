# Streamlit Application Structure

This scaffold separates the CS2-owned interface from the CS1-owned generation and evaluation work. No application behavior has been implemented yet.

```text
Hof_Abington_Case_Study/
|-- app.py                         CS2: Streamlit entry point
|-- .streamlit/
|   `-- config.toml                CS2: theme and application settings
|-- assets/
|   `-- styles.css                 CS2: optional presentation styling
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
|   `-- data_adapter.py            CS2: stable UI-facing data shape
`-- views/
    |-- __init__.py
    |-- candidate_queue.py         CS2: queue and status
    |-- clinician_review.py        CS2: review and approval workflow
    `-- patient_preview.py         CS2: patient preview and simulated send
```

## Ownership Boundary

CS1 owns the fixture contents and the functions that generate, evaluate, and regenerate outreach. The placeholder files for that work are labeled `Work to be done by CS1`.

CS2 owns the Streamlit entry point, view modules, UI state, presentation styling, and the adapter that shields the views from changes in CS1's response format. Those files are labeled as intentionally on hold.

## Integration Boundary

When implementation begins, the views should call the service modules through a small set of operations:

```text
generate_outreach(patient, trial, match_evidence)
evaluate_message(message)
regenerate_section(section_id, instruction, context)
```

`services/data_adapter.py` will normalize the returned data before it reaches a view. This allows CS2 to build against fixture data while CS1 completes the live functions, and it limits later schema changes to one place.

## Current State

The scaffold is complete. All CS2 implementation remains paused, as requested.
