# Azra-Inspired UI Research

This prototype uses visual patterns observed in Azra AI's publicly available materials. It is not a copy of Azra's private application, and the team did not have access to internal design files or authenticated product screens.

## Public Sources Reviewed

- [Azra AI Clinical Research Platform](https://www.azra-ai.com/solutions/clinical-trials)
- [Azra AI corporate website](https://www.azra-ai.com/)

The clinical-research page was the primary reference because it includes public images of feasibility, patient-review, and portfolio-reporting interfaces. The corporate website was used to confirm typography, color, button, and motion patterns.

## Observed Product Patterns

Azra's public clinical-research images use a light application canvas rather than the dark marketing treatment used on the corporate website. Repeated interface patterns include:

- A deep-purple application header
- White cards and work areas
- Very pale lavender page and input backgrounds
- Purple primary actions and lighter purple secondary controls
- Compact worklists and tables
- Small colored status pills with visible text labels
- Thin gray-lavender borders
- Modest corner rounding rather than heavily rounded cards
- Dense clinician information organized into clear panels

The public product images also show patterns that fit this prototype's workflow: clinical trial lists, patients to review, eligibility-match percentages, source-oriented criteria review, and portfolio status reporting.

## Measured Public-Site Tokens

The following values were observed from the public Azra site and its published product imagery, then simplified into a small prototype palette:

| Purpose | Prototype token | Reference basis |
|---|---:|---|
| Deep application purple | `#250040` | Dominant product header color |
| Primary action purple | `#4D287A` | Public-site primary button |
| Bright purple accent | `#9747FF` | Public-site brand accent and focus color |
| Hover purple | `#BA85FF` | Public-site primary-button hover color |
| Pale lavender canvas | `#FAF4FF` | Product form and dashboard surfaces |
| Secondary surface | `#F7F3FA` | Product panel contrast |
| Card surface | `#FFFFFF` | Product cards, tables, and forms |
| Primary text | `#1D1D20` | High-contrast application text |
| Muted text | `#52525B` | Supporting labels and descriptions |
| Border | `#E4E2E6` | Low-contrast panel separation |

Azra's public site uses Poppins, medium-to-bold headings, approximately 8–10 pixel button radii, and short 150–200 millisecond color and shadow transitions. The prototype uses those traits without reproducing the marketing site's large-scale motion or dark page treatment.

## Prototype Application Rules

- Use the light product style for clinician work and patient content.
- Reserve deep purple for navigation and high-level application chrome.
- Use purple for primary actions, focus, and active workflow states.
- Keep patient content quieter and less dense than the clinician workspace.
- Communicate status with both text and color.
- Use motion only for brief hover and focus feedback.
- Keep clinician evidence, model-assisted scores, and internal match context out of the patient view.
- Label the interface `Azra AI Outreach Prototype` using text rather than copying a logo asset.

## Known Limitations

The design is based only on public Azra materials available on September 30, 2026. Exact internal components, accessibility specifications, spacing tokens, and authenticated workflows could differ. The intended outcome is a respectful visual fit that shows integration awareness, not a claim of exact brand-system compliance.
