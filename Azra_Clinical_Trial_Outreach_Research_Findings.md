# Azra Clinical Trial Outreach
## Research Findings and Prototype Direction

**Research completed:** September 28, 2026  
**Purpose:** Determine the best evidence-backed direction for Azra AI's proposed patient outreach feature after Azra has already identified a patient as a potential clinical-trial match.

---

## 1. Executive Summary

The most important clarification for this project is that **Azra is not asking us to prove that patient outreach is a worthwhile feature**. Azra has already identified this as a real product need. The research question is therefore narrower and more useful:

> **Once Azra has already identified a potential patient for a specific clinical trial, what is the safest, clearest, and most useful way to turn the existing match evidence into patient-facing outreach that a clinical research team can review and send?**

The research supports the direction we have been moving toward, but it also sharpens several parts of the prototype.

### Main conclusion

The strongest prototype is **not a generic AI trial summarizer** and it is **not a new trial-matching system**. It is a **post-match communication workflow** that turns Azra's existing match evidence into a personalized, plain-language outreach message.

The central patient-facing artifact should be a structured **"Why Me?" outreach packet** delivered as a secure portal message or an email-like communication. It should answer, very early:

1. **Why am I receiving this message?**
2. **Why might this study be relevant to me?**
3. **What is the study trying to learn?**
4. **What might participation involve?**
5. **What should I do if I want to learn more?**

This direction is supported by patient-portal recruitment research. In a Duke study, patients were especially supportive of research messages when the study was relevant to their health, and patients specifically asked for messages to explain personal relevance and provide more study information such as time commitment, procedures, eligibility criteria, location/virtual status, compensation, and contact information. [R4]

The clinician-facing side should be where most of the product differentiation lives. Azra already has traceable evidence supporting its inclusion/exclusion analysis. Instead of hiding that evidence behind the generated message, the proposed feature should carry it forward:

> **Azra identifies the match -> AI drafts the patient explanation -> clinician can inspect the evidence supporting each personalized statement -> clinician edits or regenerates a specific section -> clinician approves -> existing secure communication infrastructure sends it.**

That is a much stronger product than "put patient data and trial data into an LLM and send the answer."

### What the research changed

The research supports several decisions we were already considering:

- **Keep Azra's existing screening as the source of truth.** Do not build another eligibility model.
- **Make personal relevance explicit.** "Why am I receiving this?" should be one of the first things the patient sees.
- **Do not reduce the message to a tiny generic email.** Research suggests patients want enough detail to decide whether it is worth engaging.
- **Use an LLM as a controlled drafting/simplification layer, not an autonomous clinical decision-maker.**
- **Keep a clinician in the approval loop.** Research on LLM simplification shows strong potential but still supports human review.
- **Use source traceability.** Azra already exposes criterion-level evidence, so the outreach feature should preserve that advantage.
- **Separate notification from protected/sensitive content when appropriate.** A common real-world pattern is a generic email/text notification followed by detailed content inside a secure portal.
- **Treat delivery channel as configurable.** Portal messaging is common, but evidence does not support assuming it is always the best engagement channel.
- **Do not claim the prototype will increase enrollment.** Our prototype can more defensibly claim to improve the process of preparing individualized outreach and support understandable patient communication.
- **Do not build a quiz as the core patient experience.** The research and Azra consultation point toward clear information and preparation for a human conversation rather than "testing" the patient.

---

# 2. The Product Boundary

## 2.1 What Azra already does

Azra's current Clinical Research Intelligence Platform already handles the difficult upstream problem: finding and pre-screening potential patients.

Azra publicly describes:

- a unified patient intelligence layer that combines structured and unstructured clinical data;
- protocol/criteria parsing;
- automated pre-screening;
- patient matching;
- and traceable evidence for each eligibility determination, including document text citations supporting inclusion or exclusion criteria. [R1]

That changes the design problem completely.

### We should **not** build this:

```text
Patient record
    ↓
Our eligibility algorithm
    ↓
Our matching score
    ↓
Our recruitment system
```

That duplicates Azra.

### We should build this:

```text
Azra identifies a potential match
          ↓
Azra provides patient facts + trial criteria + match evidence
          ↓
Our outreach-generation layer
          ↓
Clinician review and targeted revision
          ↓
Approved patient-facing "Why Me?" outreach
          ↓
Existing secure patient communication channel
```

The system starts **after matching**.

## 2.2 Why this product boundary matters

There are three benefits.

### First: it uses Azra's strongest existing asset

Azra already says its eligibility determinations are traceable. [R1] The outreach feature can reuse that evidence instead of creating another black-box clinical inference layer.

### Second: it reduces safety risk

The LLM is not being asked:

> "Is this person eligible?"

It is being asked:

> "Using only these already-approved/source-grounded facts, explain why this person is being contacted and what this study is about."

That is a much narrower generation task.

### Third: it produces a cleaner product story

The product is a bridge:

> **Azra already knows who may be relevant. The new feature helps the clinical team explain that opportunity to the patient clearly, personally, and efficiently.**

---

# 3. The Most Important Patient Need: "Why Am I Receiving This?"

The strongest external validation for the "Why Me?" concept comes from research on patient-portal recruitment messaging.

A Duke Health mixed-methods study reviewed patient portal recruitment messaging and interviewed both research teams and patients. Across the ten study teams in the qualitative sample, 35,037 recruitment messages were sent; 33% were viewed, 17% received a response, and 7% produced an "Interested" response. More important for our design, patients said they were especially supportive of recruitment messages when the study was relevant to their health. [R4]

The patient interviews revealed two especially important complaints.

## 3.1 Complaint: "Why did I get this?"

Some patients were confused by a research message and worried that it might imply bad news or a serious health problem.

The researchers' recommendation was to **emphasize personal relevance** and make clear why the research invitation relates to the person's health. [R4]

### Design implication

The message should not begin with a generic statement like:

> "You may be eligible for a clinical research study."

It should begin with context:

> **Why you're receiving this**  
> Your care team identified a research study that may be relevant based on information already in your medical record and the study's screening criteria.

Then, when institutionally appropriate and backed by Azra's match evidence:

> **Why this study may be relevant to you**  
> This study is looking for people with [plain-language condition/characteristic]. Your record shows [relevant patient fact], which is one reason the research team believes the study may be worth discussing with you.

This is fundamentally different from a generic trial summary.

## 3.2 Complaint: "There isn't enough information"

Patients in the same Duke study said the initial recruitment message often did not contain enough information to decide whether to engage. Their suggested information included:

- study title;
- research aims;
- study website;
- eligibility criteria;
- time commitment;
- study procedures;
- compensation;
- whether participation is in-person or virtual;
- and contact information. [R4]

A separate Johns Hopkins patient-portal pilot also found that a longer recruitment message containing more context produced a higher response rate than a shorter version: 2.1% versus 1.2% in that study. The authors cautioned that message content optimization needs more research, so this should not be treated as a universal rule that "longer is always better." [R5]

### Design implication

We should optimize for **scannability and usefulness**, not minimum word count.

The message should be structured with headings and short sections instead of trying to compress everything into three sentences.

---

# 4. Recommended Patient-Facing "Why Me?" Packet

The outreach should remain a static message. It does not need chat, a conversational assistant, or rich interactivity to be useful.

A recommended structure is below.

## Section 1: Specific subject line

Avoid:

> Research Opportunity

Prefer something that clearly identifies the topic without exposing sensitive information in an insecure notification channel.

Inside a secure portal, for example:

> Research opportunity related to [study area]

Duke patients preferred subject lines specific to the research study rather than generic research notices. [R4]

## Section 2: Why you are receiving this

Purpose: eliminate confusion immediately.

Example:

> **Why you're receiving this**  
> A clinical research study is currently enrolling patients at [site]. Based on information already reviewed by the research team, this study may be relevant to you. Receiving this message does not mean you are required to participate or that final eligibility has been confirmed.

### Important wording rule

Do **not** say:

> "You are eligible."

Even if Azra's internal prescreening shows a complete criterion match, final study eligibility normally remains a clinical/research-team determination and recruitment language should not imply certainty.

Prefer:

- "may be a potential fit"
- "may meet some or all of the initial criteria"
- "the research team identified this study as potentially relevant"
- "may be worth discussing"

## Section 3: Why this may be relevant to you

This is the core differentiator.

The system should connect:

```text
Trial criterion
        +
Relevant patient fact
        ↓
Plain-language explanation
```

Example clinician-side evidence:

```text
TRIAL CRITERION:
Diagnosis of Stage III or IV non-small-cell lung cancer

PATIENT EVIDENCE:
FHIR Condition/123:
Non-small-cell lung cancer, Stage IV
```

Patient-facing wording:

> The study is looking for people being treated for advanced non-small-cell lung cancer. Your medical record includes this diagnosis, which is one reason the study was identified as potentially relevant to you.

The LLM is not deciding whether that match is true. Azra already provides the match. The model's job is to translate it.

## Section 4: What the study is trying to learn

Example:

> **What is this study about?**  
> Researchers are studying whether [plain-language explanation of intervention/question] may [study objective].

This should come from authoritative study material.

For the prototype, ClinicalTrials.gov can supply study purpose, intervention, design, locations, and eligibility information. ClinicalTrials.gov provides an API with JSON output, which makes it reasonable to use one real study in the demo. [R21]

## Section 5: What participation may involve

Patients specifically reported caring about practical study requirements. [R4]

When the source data supports it, include:

- approximate study duration;
- number/frequency of visits;
- in-person vs remote;
- major procedures;
- intervention/treatment assignment;
- blood draws/imaging/questionnaires;
- compensation or reimbursement, if applicable;
- study location.

This is more useful to a patient than a technical protocol summary.

## Section 6: Important things to know

This section should be tightly governed.

Possible content:

- participation is voluntary;
- receiving the message does not guarantee final eligibility;
- choosing not to participate does not affect normal care;
- this message is not the informed-consent process;
- additional risks/benefits will be discussed by the study team.

### Important source limitation

ClinicalTrials.gov alone should **not automatically be treated as the complete source for risk information**.

If the production feature will communicate detailed risks or potential benefits, Azra should determine which IRB-approved or protocol/consent materials are the approved source for those statements.

FDA and OHRP guidance treat recruitment materials that go beyond basic trial listings more carefully, particularly around descriptions of risks and benefits and statements that could imply expected benefit. [R9][R10]

## Section 7: Questions you may want to ask

Rather than quizzing the patient, give them useful prompts:

- Why was this study identified for me?
- What would I need to do if I joined?
- How often would I need to visit the study site?
- What treatments or procedures are involved?
- What are the known risks?
- What other treatment choices do I have?
- Who can I speak with before deciding?

This matches the project's real goal better: **prepare the patient for a meaningful human conversation**.

## Section 8: Clear next step

Example:

> If you would like to learn more, select **I'm interested in learning more** or contact the study team at [approved contact method].

Potential response states:

- Interested in learning more
- Not interested
- Ask me later / Learn more
- Opt out of future research outreach, when supported by the institution

Duke study teams specifically suggested more response choices such as interested / not interested / learn more. [R4]

---

# 5. Plain-Language Requirements

"Make it simple" is not a sufficient requirement. We need rules.

CDC plain-language guidance recommends putting the most important message first, using logical chunks and headings, using active voice, choosing familiar words, aiming for an average of about 20 words per sentence, limiting each sentence to one idea, and keeping paragraphs focused. [R15]

The MRCT Center's clinical research health-literacy guidance similarly recommends plain language, clear design, numeracy support, cultural consideration, and usability testing across participant-facing research communications. [R16][R17]

## Prototype language rules

The generation prompt should enforce:

1. Put "why you are receiving this" first.
2. Use short headings.
3. Use active voice.
4. Prefer common words over clinical terms.
5. If a clinical term is necessary, define it immediately.
6. One main idea per sentence.
7. Keep paragraphs short.
8. Speak directly to the patient using "you."
9. Never imply guaranteed benefit.
10. Never imply final eligibility.
11. Never invent a risk, procedure, time commitment, or benefit not present in the approved source.
12. Clearly distinguish research from standard clinical care.
13. End with a simple next step.

## Readability target

A readability metric can be shown as a **supporting quality check**, not as proof that a message is understandable.

A 2025 JMIR study found that general-purpose LLMs substantially lowered the reading grade level of patient education material, but model performance varied and some outputs contained inaccuracies. The authors concluded that human review remains necessary. [R18]

For the prototype, we can aim for approximately a **6th-8th grade reading level**, but we should not claim that a grade-level score alone proves patient comprehension.

---

# 6. Clinician View: Where the Product Becomes More Than an LLM Wrapper

If the patient only receives a static outreach message, then the clinician view needs to demonstrate the intelligence and control behind that message.

The key design is:

> **Every personalized statement should be inspectable.**

## 6.1 Recommended clinician workflow

```text
Candidate Queue
    ↓
Open candidate
    ↓
Review Azra match summary
    ↓
Generate outreach
    ↓
Review patient-facing draft
    ↓
Click a personalized sentence to inspect supporting evidence
    ↓
Edit directly OR request a targeted AI revision
    ↓
Approve
    ↓
Send / simulate secure send
    ↓
Record status
```

## 6.2 Evidence-on-demand

For a generated sentence such as:

> "This study may be relevant because your record shows that you have been treated for X."

the clinician should be able to click and see:

**Patient source**

```text
FHIR Condition / Medication / Observation / Azra patient evidence
```

**Trial source**

```text
Trial inclusion criterion or approved study text
```

**Azra match evidence**

```text
Criterion status: matched
Source excerpt/citation: [...]
```

This is especially compatible with Azra because Azra already advertises criterion-level traceability and document text citations for trial pre-screening. [R1]

### Product principle

> **The model writes the phrasing. The source data determines the facts.**

That is a concrete technical and product distinction.

## 6.3 Targeted clinician revision

The clinician should have two revision paths.

### A. Direct edit

The clinician changes the message manually.

### B. Targeted AI revision

Select one section and choose something like:

- Make this easier to understand
- Make this shorter
- Explain this term
- Make the tone warmer
- Add more detail using only the supplied study information
- Custom instruction

Only regenerate the selected section.

### Why this is better than "regenerate message"

It:

- protects sections already reviewed;
- reduces unnecessary model variation;
- gives the clinician control;
- makes the review workflow faster;
- and creates a clearer audit trail.

For the prototype, one revision cycle is enough.

---

# 7. Human Review Is Not Optional in the Proposed Production Design

General-purpose LLMs are reasonable for the prototype, but the evidence does not support treating the generated medical/research message as automatically safe to send.

The 2025 JMIR study found meaningful readability improvements across ChatGPT, Gemini, and Claude, but also found model-to-model variability and inaccuracies, supporting human review. [R18]

A 2026 proof-of-concept study in *npj Digital Medicine* tested an LLM constrained to trial-specific informed-consent documents. Human reviewers gave the generated responses high mean accuracy scores, with readable outputs and minimal hallucination. However, the authors explicitly framed it as foundational validation before participant-facing evaluation, not proof that autonomous participant communication is ready for deployment. [R19]

### Design decision

For the prototype:

```text
Generate → Review → Approve → Send
```

not:

```text
Generate → Automatically send
```

---

# 8. Grounding Architecture for the LLM

The LLM should receive structured facts, not an entire raw chart and a trial page with a vague prompt.

A useful prototype input structure is:

```json
{
  "patient": {
    "id": "SYN-001",
    "facts": [
      {
        "id": "p1",
        "label": "Diagnosis",
        "value": "Stage IV non-small-cell lung cancer",
        "source": "FHIR Condition/123"
      }
    ]
  },
  "trial": {
    "nct_id": "NCT00000000",
    "facts": [
      {
        "id": "t1",
        "label": "Inclusion criterion",
        "value": "Stage III or IV non-small-cell lung cancer",
        "source": "ClinicalTrials.gov eligibility criterion"
      }
    ]
  },
  "match": [
    {
      "criterion_id": "t1",
      "patient_fact_ids": ["p1"],
      "status": "matched",
      "azra_evidence": "Source evidence supplied by Azra"
    }
  ]
}
```

The LLM should return a structured response:

```json
{
  "sections": [
    {
      "id": "why_contacted",
      "heading": "Why you're receiving this",
      "text": "...",
      "source_refs": ["p1", "t1"]
    },
    {
      "id": "why_relevant",
      "heading": "Why this study may be relevant to you",
      "text": "...",
      "source_refs": ["p1", "t1"]
    }
  ]
}
```

The front end can then use `source_refs` to power clinician traceability.

## 8.1 Critical prompt behavior

The prompt should contain rules such as:

> Use only the supplied patient facts, trial facts, and approved match evidence.

> Do not perform a new eligibility assessment.

> Do not state that the patient is definitively eligible.

> Do not add medical advice.

> Do not infer a risk, benefit, diagnosis, treatment history, procedure, or study requirement that is not explicitly present in the supplied information.

> If required information is missing, omit it or state that the study team can provide more information.

> Every personalized factual statement must return one or more source references.

This is more defensible than relying on "please don't hallucinate."

---

# 9. Delivery: FHIR Is Not the Message-Sending Protocol

This was one of the technical questions we needed to settle.

FHIR can be part of the data and workflow representation, but **FHIR is not inherently the transport mechanism that sends a MyChart message or email**.

HL7 FHIR has:

- `CommunicationRequest`, which can represent a request for information or educational material to be sent to a patient;
- `Communication`, which can record that a communication occurred. [R13][R14]

The FHIR specification explicitly says these resources do **not** represent the actual flow of the communication. [R13][R14]

### Production architecture

```text
Azra / EHR clinical data
        ↓
FHIR / HL7 / Azra internal data layer
        ↓
Outreach generation and review
        ↓
Approved message
        ↓
Health-system/EHR secure messaging interface
        ↓
Patient portal / approved communication channel
```

The exact final delivery integration depends on the hospital and EHR environment.

---

# 10. Portal vs Email: Do Not Hardcode the Product to One Channel

There is strong evidence that patient portals are already used for research recruitment.

Penn Medicine states that MyChart/myPennMedicine can be used for research recruitment. Patients can receive an email or text notification that a research-study message is waiting, then log in to the portal to see the message. Penn also requires IRB approval for this use, tracks contacted patient statuses, and honors research-contact opt-outs. [R7]

Johns Hopkins similarly describes a MyChart recruitment workflow in which patients receive a portal invitation detailing the study and the reasons for reaching out. [R8]

This closely validates the workflow we are proposing.

However, the research does **not** support saying that a portal is always the best engagement channel.

A 2026 randomized clinical trial of 15,376 potential participants found higher engagement from email than patient-portal messaging in that study: 9.9% versus 5.9%. The result is context-specific and should not be generalized to every health system or patient population, but it demonstrates that communication modality matters. [R6]

Another randomized comparison published in 2025 found that portal communication produced more early self-screener engagement than email in its setting, but did not significantly improve final randomization. [R29]

### Product decision

Azra should treat **message generation** and **message delivery** as separate layers.

The system should create one approved outreach artifact that can be routed through the health system's allowed channel:

- secure patient portal;
- approved email workflow;
- SMS notification with portal handoff;
- or another institution-approved channel.

### Prototype decision

Build one patient portal/email-style view and label the delivery as simulated.

Do not spend this week implementing a real messaging integration.

---

# 11. Security and Privacy Direction

The prototype should use **synthetic patient data only**.

In production, protected health information changes the requirements substantially.

HHS states that healthcare organizations can use electronic communication under HIPAA when appropriate safeguards are used, but protections depend on the communication method and context. [R11]

For cloud services that create, receive, maintain, or transmit ePHI on behalf of a covered entity, appropriate HIPAA business-associate arrangements and safeguards are required. [R12]

### Important design implication for the LLM

A production implementation should not send PHI to an arbitrary consumer AI endpoint.

Azra would need an approved enterprise deployment architecture consistent with its customers' privacy/security requirements, potentially including:

- business associate agreements where applicable;
- access controls;
- encryption in transit and at rest;
- logging/audit controls;
- data retention rules;
- model/provider data-use restrictions;
- and health-system security review.

The competition prototype does not need to implement this infrastructure.

## 11.1 Strong default communication pattern

Penn Medicine's public research recruitment guidance is especially useful here. It advises that ordinary patient email should not include PHI and points teams toward the patient portal for electronic recruitment messaging. [R30]

A strong production default is therefore:

```text
EMAIL / SMS NOTIFICATION
"Your healthcare portal has a new research opportunity message."
(no sensitive personalized detail)
             ↓
SECURE PATIENT PORTAL
full personalized Why Me packet
```

This should be presented as a recommended architecture pattern, not a statement that every health system must use it.

---

# 12. Recruitment Governance and IRB Review

This is an area where the prototype story needs to be careful.

FDA guidance says IRBs should review recruitment methods and materials for covered research and treats direct recruitment advertising as part of the beginning of the informed-consent and subject-selection process. Recruitment material should not imply guaranteed benefit or certainty of a favorable outcome. [R9]

OHRP guidance for HHS-supported research similarly distinguishes basic trial directory information from richer patient-facing recruitment content. When material goes beyond basic listings, especially when it includes descriptions of risks or benefits, IRB review may be required. [R10]

Penn Medicine's current MyChart research recruitment process explicitly requires IRB approval of recruitment message language before the system is used. [R7]

### Design implication

A real implementation cannot assume:

> "The AI can generate any new patient-facing message on demand and send it."

A more realistic model is:

1. study/institution defines an approved message structure and approved source materials;
2. Azra fills bounded personalized sections using match evidence;
3. clinician/research staff reviews the generated draft;
4. approved version is sent;
5. message version and approval are logged.

This is a **product-design recommendation**, not legal advice. Exact governance will depend on the study, institution, applicable regulations, and IRB.

---

# 13. How Azra's Existing Workflow Supports This Direction

Azra already uses workflow patterns that fit this feature.

Its high-risk screening solution describes:

- navigation work;
- documented patient contact attempts;
- outreach activity;
- EHR write-back;
- and bi-directional synchronization. [R2]

Azra's Navigation as a Service offering also explicitly describes proactive patient engagement after the technology has surfaced a patient. [R3]

### Important implication

A candidate table with statuses such as:

- Match identified
- Draft not generated
- Draft generated
- Needs review
- Approved
- Sent
- Patient interested
- Patient declined

is not an unrelated CRM feature if it stays lightweight.

It follows an existing Azra pattern:

> **identify -> act -> document -> close the loop**

For the case competition, this table should support the workflow but should not become the main technical project.

---

# 14. Competitive Research: What Already Exists?

The goal of the competitor review is **not** to prove Azra needs outreach. Azra has already told us it does.

The purpose is to learn which patterns are already established, avoid reinventing weak approaches, and identify where Azra's existing match evidence creates a more useful implementation.

| Product / approach | Trial matching / targeting | Patient-friendly trial info | Outreach / communication | Tracking / workflow | Public evidence of patient-specific "Why Me?" with clinician-visible criterion provenance |
|---|---:|---:|---:|---:|---:|
| **Azra today** | Strong | Limited for this use case | Proposed new capability | Strong workflow patterns elsewhere | **Azra has the evidence layer, but this outreach use case is the proposed gap** |
| **Epic / MyChart research recruitment** | EHR-based targeting possible | Message templates / study info | Yes | Yes | Not clearly the core public product concept |
| **TrialX** | Yes / trial finder and referral workflows | Strong AI simplification of trial listings | Yes | Yes | Public materials reviewed do not clearly show Azra-style criterion-level provenance in the clinician drafting workflow |
| **Clinrol** | Yes | Patient-facing trial information | AI/SMS/communication tools | Yes | Not clearly shown publicly |
| **Trialflow** | Matching/scoring | Plain-language explanations | Email/SMS automation | CRM/funnel tracking | Not clearly shown publicly |
| **SubjectWell / OneView** | Recruitment ecosystem | Recruitment information | Centralized communications | Strong funnel tracking | Not clearly shown publicly |

### What competitors validate

The market already validates several pieces:

- patient recruitment messages;
- automated communication;
- patient-friendly study explanations;
- portal workflows;
- patient status tracking;
- AI-supported recruitment;
- and simplified trial information.

So we should **not** claim those concepts individually are novel.

### Where Azra has an advantage

Azra's current platform already produces traceable, patient-specific evidence for why a person matches trial criteria. [R1]

The strongest opportunity is therefore to make that evidence useful downstream:

> **Take a traceable prescreening decision and turn it into a patient-specific explanation while preserving the evidence for the clinician.**

Based on the publicly available product information reviewed for this report, I did **not** find strong public evidence of a competitor whose core workflow is exactly:

```text
criterion-level patient match evidence
       ↓
patient-specific "why this may fit you" explanation
       ↓
sentence/section-level source provenance for clinician review
       ↓
targeted clinician revision
       ↓
approved outreach
```

That should be described as a **potential differentiator**, not as a claim that no company in the market has ever built it.

---

# 15. TrialX: The Most Useful Competitive Pattern to Borrow

TrialX is relevant because it already uses AI to simplify clinical-trial information for patients. Its public materials describe patient recruitment tools and AI-supported simplification of ClinicalTrials.gov content. [R23][R24]

This validates the idea that an LLM can be used to turn trial language into patient-facing language.

The lesson for our team is not:

> "Copy TrialX."

It is:

> **Trial simplification alone is already an established direction, so Azra's feature should go one step further and personalize the explanation using Azra's existing patient-to-criterion evidence.**

That is the difference between:

> "Here is this trial in simpler words."

and:

> "Here is this trial in simpler words, here is why your research team identified it for you, and here is the source evidence the clinician can inspect before sending."

---

# 16. Prototype Recommendation

The prototype should prove one complete vertical slice.

## Must-have

### 1. Candidate queue

Use 3-5 synthetic rows for visual context.

Example columns:

| Patient | Trial | Match status | Outreach status |
|---|---|---|---|
| Synthetic Patient A | NCT... | Potential match | Needs draft |
| Synthetic Patient B | NCT... | Potential match | Awaiting review |
| Synthetic Patient C | NCT... | Potential match | Sent |

Only one patient needs a complete real demo flow.

### 2. One synthetic patient

Use synthetic FHIR-like data:

- Patient
- Condition
- MedicationRequest if relevant
- Observation/lab if relevant

Do not use real PHI.

### 3. One real trial

Use one ClinicalTrials.gov study through:

- an API call, if easy and stable; or
- a cached JSON copy of the API response for demo reliability.

A cached fallback is recommended for Demo Day.

### 4. Mock Azra match evidence

Because Azra's actual internal API/data schema is not provided to the competition, create a realistic `match` object representing what Azra would supply.

Do **not** pretend our software performed the match.

Clearly label:

> "In production, this match evidence is supplied by Azra's existing prescreening engine."

### 5. Generate outreach

Call a strong general-purpose LLM.

Require structured JSON output with:

- section ID;
- heading;
- patient-facing text;
- source references.

### 6. Evidence traceability

Clinician clicks a personalized section.

UI displays:

- patient fact(s);
- trial criterion(s);
- source reference;
- Azra match result.

This should be one of the main demo moments.

### 7. Clinician revision

Allow:

- direct edit; and/or
- targeted AI revision of one selected section.

Do not rebuild a full document editor.

### 8. Approve

Simple button:

> Approve outreach

Once approved, lock/mark the version used for the simulated send.

### 9. Patient view

Show exactly what the patient receives:

- clean;
- simple;
- no technical source metadata;
- structured Why Me packet;
- clear next action.

### 10. Simulated send

Button:

> Send through secure patient channel

Prototype result:

> Sent successfully — secure delivery simulated for prototype.

Then update queue status.

No live MyChart integration is necessary.

---

# 17. Nice-to-Have Features

Only build these after the entire core path works.

## A. Readability check

Show:

- estimated reading grade;
- long-sentence warning;
- unexplained medical terminology warning.

Do not present it as proof of comprehension.

## B. Patient notification preview

Show two screens:

**External notification**

> You have a new message in your patient portal.

**Secure portal**

Full personalized outreach.

This visually explains the privacy model without implementing a real messaging integration.

## C. Version history

Small history:

```text
v1 – AI generated
v2 – clinician revised "What participation involves"
v2 – approved
```

Useful for auditability but not required for Friday.

## D. Language preference

Potential future direction: generate an approved translated version.

Do not make this a core prototype feature unless there is enough time for validation.

---

# 18. Features We Should Explicitly Keep Out of Scope

The research makes the scope boundary clearer.

Do **not** build:

- a new patient-trial matching algorithm;
- a new eligibility score;
- automatic final eligibility determination;
- real EHR connection;
- real Epic/MyChart connection;
- real email sending with PHI;
- real patient data;
- production authentication;
- a database unless the prototype actually needs one;
- formal electronic consent;
- consent document replacement;
- IRB workflow software;
- automated risk/benefit generation from incomplete source data;
- autonomous send without clinician approval;
- a patient chatbot;
- a full CRM;
- advanced analytics dashboards;
- a patient comprehension quiz as the center of the experience;
- automated medical advice.

These features either duplicate Azra, create unnecessary safety/governance complexity, or do not improve the core proof of concept enough for the five-day deadline.

---

# 19. Technical Architecture for the Prototype

```text
                ┌─────────────────────────────┐
                │  Synthetic Patient Data     │
                │  FHIR-like JSON             │
                └──────────────┬──────────────┘
                               │
                ┌──────────────▼──────────────┐
                │ Mock Azra Match Evidence    │
                │ criteria + patient facts    │
                └──────────────┬──────────────┘
                               │
┌──────────────────────┐       │
│ ClinicalTrials.gov   │───────┤
│ real study / JSON    │       │
└──────────────────────┘       │
                               ▼
                ┌─────────────────────────────┐
                │ Grounded LLM Generation     │
                │ structured JSON response    │
                └──────────────┬──────────────┘
                               │
                               ▼
                ┌─────────────────────────────┐
                │ Clinician Review View       │
                │ - draft                     │
                │ - evidence                  │
                │ - targeted revision         │
                │ - approve                   │
                └──────────────┬──────────────┘
                               │
                               ▼
                ┌─────────────────────────────┐
                │ Patient Outreach View       │
                │ "Why Me?" packet            │
                └──────────────┬──────────────┘
                               │
                               ▼
                ┌─────────────────────────────┐
                │ Simulated secure delivery   │
                └─────────────────────────────┘
```

### Recommended stack for this week

Use the simplest stack the CS students can implement reliably.

A reasonable option:

- Python
- Flask, FastAPI, or Streamlit
- HTML/CSS or framework-native UI
- local JSON fixtures
- ClinicalTrials.gov API or cached response
- one LLM API
- no database required

The sophistication should be in the **workflow, evidence model, and generated artifact**, not infrastructure.

---

# 20. What We Can Measure in the Prototype

The team should separate **prototype quality metrics** from **future clinical/business outcomes**.

## 20.1 Metric 1: Factual support rate

Target:

> **100% of patient-specific factual statements in the generated message have a source reference.**

This is testable in the prototype.

It does not prove a statement is clinically correct, but it demonstrates the intended grounding mechanism.

## 20.2 Metric 2: Clinician edit burden

Future pilot measures:

- percentage of generated sections approved as written;
- average number of edits;
- average time from draft generation to approval;
- percentage requiring complete rewrite.

This directly measures whether the product actually saves staff effort.

## 20.3 Metric 3: Plain-language quality

Prototype evaluation:

- reading-grade estimate;
- plain-language checklist;
- unexplained jargon count;
- sentence-length warnings.

Better future evaluation:

- usability testing with representative patients;
- patient-reported understanding and clarity.

MRCT explicitly recommends usability testing of recruitment materials with members of the intended audience. [R17]

## 20.4 Metric 4: Patient-reported relevance

Future pilot question:

> "After reading this message, do you understand why this research study was sent to you?"

This directly tests the Why Me concept.

## What we should **not** claim from the prototype

We cannot demonstrate by Friday that the system:

- increases enrollment;
- improves retention;
- reduces trial dropout;
- reduces screen failure;
- improves informed consent;
- or saves a specific percentage of staff time.

Those are reasonable **future outcomes to study**, not prototype results.

---

# 21. Claims the Team Can Defend

## Claim 1

**Patient portals are already used by major health systems for research recruitment.**

Supported by Penn Medicine, Johns Hopkins, Duke, and published research. [R4][R7][R8]

## Claim 2

**Patients want recruitment messages to make personal relevance clear and to contain enough practical study information to decide whether to engage.**

Directly supported by Duke patient interviews. [R4]

## Claim 3

**Plain-language communication is an established best practice in clinical research recruitment.**

Supported by MRCT and CDC guidance. [R15][R16][R17]

## Claim 4

**LLMs can help reduce the reading complexity of patient education material, but human review remains important.**

Supported by the 2025 JMIR study and 2026 trial-document-grounded LLM proof of concept. [R18][R19]

## Claim 5

**FHIR can represent patient data and communication workflow objects, but sending a portal message requires an actual messaging/EHR integration beyond FHIR itself.**

Supported by the FHIR Communication and CommunicationRequest definitions. [R13][R14]

## Claim 6

**Azra already has traceable patient-to-criterion evidence that can be reused to ground outreach.**

Supported by Azra's own description of its clinical research platform. [R1]

---

# 22. Claims the Team Should Avoid

Do not say:

> "This eliminates hallucinations."

Say:

> "The design reduces unsupported generation by constraining the model to supplied sources and requiring clinician review."

Do not say:

> "The patient is 100% eligible."

Say:

> "Azra has identified the patient as a potential match based on its prescreening criteria; final eligibility remains with the study team."

Do not say:

> "This is HIPAA compliant."

A prototype using synthetic data cannot establish that a future production architecture is compliant.

Say:

> "The proposed production architecture is designed to integrate with approved secure communication infrastructure and would require Azra and the health system to apply the necessary HIPAA security, privacy, and vendor controls."

Do not say:

> "IRB review is not needed."

Recruitment governance is study- and institution-specific, and richer recruitment content may require review. [R9][R10]

Do not say:

> "Patient portals are better than email."

Evidence is mixed and context-dependent. [R6][R29]

Say:

> "The generation layer should be channel-agnostic so health systems can use the approved channel that fits their workflow and population."

Do not say:

> "Our innovation is using an LLM to simplify a trial."

That already exists.

Say:

> "The feature converts Azra's existing, traceable prescreening evidence into patient-specific outreach while preserving source visibility and clinician control."

---

# 23. Recommended Demo Story

The demo should be one continuous story.

## Step 1 — Set the context

> "Azra has already identified this synthetic patient as a potential candidate for this study. We are not performing the match."

Show the patient queue.

## Step 2 — Open the patient

Show:

- patient information;
- trial;
- Azra match evidence.

Keep this brief.

## Step 3 — Generate outreach

Click:

> Generate Patient Outreach

## Step 4 — Show the Why Me packet

Point out:

- why contacted;
- why relevant;
- study purpose;
- participation overview;
- next steps.

## Step 5 — Show traceability

Click a personalized sentence.

Reveal:

- patient fact;
- trial criterion;
- match evidence.

This is likely the strongest technical demo moment.

## Step 6 — Demonstrate clinician control

Select one section.

Example clinician instruction:

> "Make this easier to understand without removing the visit schedule."

Regenerate only that section.

## Step 7 — Approve

Clinician approves the final message.

## Step 8 — Show the patient view

Switch to the clean portal view.

The audience sees exactly what the patient receives.

## Step 9 — Simulate send

Click send.

Update status:

> Sent

Then explain:

> "In a real deployment, Azra would hand the approved communication to the health system's existing secure messaging infrastructure. We are intentionally not rebuilding that infrastructure in this proof of concept."

---

# 24. Open Questions We Should Ask Azra Before a Real Implementation

These questions are more useful now than additional generic competitive research.

## Data and matching

1. What exact object/API would expose the patient's prescreening result?
2. Does Azra already expose the patient facts supporting each matched inclusion/exclusion criterion in a machine-readable structure?
3. Which source should be treated as authoritative when patient data conflict?
4. Does Azra distinguish "matched," "unknown/not found," and "failed" criteria?

## Patient-facing source material

5. What approved study materials can the outreach generator use in addition to ClinicalTrials.gov?
6. Is the protocol available?
7. Is there an IRB-approved recruitment summary/template?
8. Is the informed consent form available as a source for approved patient-facing risk/procedure language?
9. Which pieces of those documents can be dynamically personalized?

## Workflow

10. Who is expected to initiate outreach: research coordinator, nurse navigator, PI, physician, or another role?
11. Who must approve the message before send?
12. Does Azra want one approval per message or approval of templates/rules at the study level?
13. What status tracking does the research team need after send?

## Delivery

14. Which channels are most important across Azra's current customers?
15. Does Azra already integrate with Epic/MyChart, Oracle Health/Cerner, or another patient-messaging interface in a way that could support this?
16. Should Azra send the communication directly, or create the approved message and hand it back to the EHR?
17. Should a nonsecure email/text contain only a generic portal notification?

## Patient preferences

18. How are research-contact opt-outs stored today?
19. Can Azra access those preferences?
20. Should patients be able to opt out of one study, one research program, or all future research outreach?

## AI governance

21. Which LLM providers/deployment environments are already approved by Azra?
22. What PHI can be sent to the model?
23. What audit logging is required?
24. What generated-content retention policy is required?
25. Does Azra want the clinician to see source provenance for every generated claim or only patient-specific claims?

These questions should shape the production design after the competition.

---

# 25. Final Recommended Product Definition

A concise definition for the team:

> **Azra Outreach transforms Azra's existing clinical-trial prescreening evidence into a personalized, plain-language patient invitation. It explains why the patient is being contacted, why the study may be relevant, what participation may involve, and how to learn more. Clinical research staff can inspect the source evidence behind personalized statements, revise individual sections, approve the message, and send it through an approved health-system communication channel.**

The product is **not**:

- a trial matcher;
- a replacement for the research coordinator;
- informed consent;
- a chatbot;
- or a new patient portal.

It is the missing communication layer between:

> **"Azra found a potential match"**

and

> **"The patient understands why the research team is reaching out and can decide whether they want a conversation."**

---

# 26. Recommended Prototype Requirements to Freeze

If the team needs one list to build against, use this.

## Required

- [ ] Candidate queue with mock patients/statuses
- [ ] One complete synthetic demo patient
- [ ] One real ClinicalTrials.gov study
- [ ] Mock Azra criterion-level match evidence
- [ ] Grounded LLM generation
- [ ] Structured Why Me packet
- [ ] Clinician evidence/source view
- [ ] Targeted revision of one section
- [ ] Direct clinician editing
- [ ] Approve action
- [ ] Patient-facing portal/message view
- [ ] Simulated send
- [ ] Status update after send
- [ ] Clear disclaimer that final eligibility is determined by the study team
- [ ] No real patient data

## Only if the core is finished

- [ ] Readability indicator
- [ ] Version history
- [ ] Generic email/SMS notification preview
- [ ] Additional response options
- [ ] Language preference / translation concept

## Do not build for Friday

- [ ] Real EHR integration
- [ ] Real FHIR server
- [ ] Real portal integration
- [ ] Real email/SMS delivery
- [ ] New trial-matching model
- [ ] Full database
- [ ] Formal consent
- [ ] Patient chatbot
- [ ] Production security infrastructure
- [ ] Complex analytics dashboard

---

# 27. Source List

**[R1] Azra AI — Clinical Research Intelligence Platform**  
https://www.azra-ai.com/solutions/clinical-trials

**[R2] Azra AI — Cancer Screening Follow-Up & Compliance / EHR write-back workflow**  
https://www.azra-ai.com/solutions/high-risk-screening

**[R3] Azra AI — Navigation as a Service**  
https://www.azra-ai.com/services/clinical-navigation

**[R4] Miller et al. — Describing current use, barriers, and facilitators of patient portal messaging for research recruitment**  
https://pmc.ncbi.nlm.nih.gov/articles/PMC10130833/

**[R5] Plante et al. — Recruitment of trial participants through electronic medical record patient portal messaging: A pilot study**  
https://pmc.ncbi.nlm.nih.gov/articles/PMC6992491/

**[R6] Gouda et al. (2026) — Messaging Modality and Content for Recruitment of Research Participants: A Randomized Clinical Trial**  
https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2849286

**[R7] Penn Medicine Clinical Research — MyPennMedicine Recruitment Messaging**  
https://www.med.upenn.edu/clinicalresearch/mypennmedicine.html

**[R8] Johns Hopkins ICTR — MyChart/Epic Recruitment**  
https://ictr.johnshopkins.edu/service/recruitment/mychart-epic/

**[R9] U.S. FDA — Recruiting Study Subjects: Guidance for IRBs and Clinical Investigators**  
https://www.fda.gov/regulatory-information/search-fda-guidance-documents/recruiting-study-subjects

**[R10] HHS OHRP — Clinical Trial Websites: When is IRB Review Required?**  
https://www.hhs.gov/ohrp/regulations-and-policy/guidance/clinical-trial-websites/index.html

**[R11] HHS — HIPAA and Email Communication With Patients**  
https://www.hhs.gov/hipaa/for-professionals/faq/does-hipaa-permit-health-care-providers-to-use-email-to-discuss-health-issues-with-patients/index.html

**[R12] HHS — HIPAA and Cloud Computing**  
https://www.hhs.gov/hipaa/for-professionals/special-topics/health-information-technology/cloud-computing/index.html

**[R13] HL7 FHIR — CommunicationRequest**  
https://hl7.org/fhir/R4/communicationrequest.html

**[R14] HL7 FHIR — Communication**  
https://hl7.org/fhir/R4/communication.html

**[R15] CDC — Plain Language Materials & Resources**  
https://www.cdc.gov/health-literacy/php/develop-materials/plain-language.html

**[R16] MRCT Center — Principles of Health Literacy in Clinical Research**  
https://mrctcenter.org/health-literacy/introduction/principles-of-health-literacy-in-clinical-research/

**[R17] MRCT Center — Recruitment and Health Literacy in Clinical Research**  
https://mrctcenter.org/health-literacy/trial-life-cycle/overview/recruitment/

**[R18] Will et al. (2025) — Enhancing the Readability of Online Patient Education Materials Using Large Language Models**  
https://www.jmir.org/2025/1/e69955/

**[R19] Moscatel et al. (2026) — Performance of a large language model in the informed consent process for participation in a clinical trial**  
https://www.nature.com/articles/s41746-026-02745-9

**[R20] ClinicalTrials.gov API modernization / API v2 — National Library of Medicine**  
https://www.nlm.nih.gov/pubs/techbull/ma24/ma24_clinicaltrials_api.html

**[R21] ClinicalTrials.gov API**  
https://clinicaltrials.gov/data-api/api

**[R22] Epic — Life Sciences / Research Capabilities**  
https://www.epic.com/software/life-sciences/

**[R23] TrialX — Patient Recruitment Management / TrialX Connect**  
https://www.trialx.com/patient-recruitment-management-system

**[R24] TrialX — AI Simplification of Clinical Trial Information**  
https://trialx.com/simplifying-clinical-trial-information-how-trialxs-ai-tool-makes-protocol-jargon-understandable-for-patients/

**[R25] Clinrol — AI Clinical Trial Recruitment & Engagement**  
https://www.clinrol.com/

**[R26] Trialflow — Clinical Trial Recruitment Platform**  
https://gettrialflow.com/

**[R27] SubjectWell — Patient Recruitment / OneView**  
https://subjectwell.com/

**[R28] Penn Medicine — Penn iConnect Patient Recruitment Management System**  
https://www.med.upenn.edu/clinicalresearch/iconnect2025.html

**[R29] Randomized study comparing patient portal and email communications for trial recruitment**  
https://pmc.ncbi.nlm.nih.gov/articles/PMC12373006/

**[R30] Penn Medicine — Recruitment Strategies, Resources, Privacy**  
https://www.med.upenn.edu/clinicalresearch/recruitment-strategies-resources-privacy.html

---

## Bottom Line

The research does **not** tell us to change the project into something larger.

It tells us to make the narrow project better.

The evidence-backed version of the idea is:

> **Use Azra's existing match and source evidence to generate a patient-centered "Why Me?" outreach message, keep the message grounded in approved data, give the clinician visibility and control over the source evidence and wording, and hand the approved message to the health system's existing secure communication channel.**

That is narrow enough to prototype by Thursday, consistent with real patient-recruitment workflows, supported by patient-preference research, technically realistic, and directly connected to capabilities Azra already has.
