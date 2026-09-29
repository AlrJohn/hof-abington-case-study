# Why I Changed the Azra Working Plan for V3

I compared the V2 working plan with the findings in [Azra Clinical Trial Outreach Research Findings](./Azra_Clinical_Trial_Outreach_Research_Findings.md). My main conclusion was that the team did not need a new product direction. V2 had already identified the correct part of the workflow: Azra finds a potential match, and our feature helps the clinical team explain that opportunity to the patient.

The research did show that several parts of the plan were still too general. The patient message needed more specific content requirements, the source rules needed to be stricter, and the plan needed a clearer distinction between what our prototype can demonstrate and what would require a real clinical pilot or production review. I created [Working Plan V3](./Azra_Team_Working_Plan_V3.docx) to address those gaps without making the five-day prototype larger.

## What stayed the same

I kept the post-match product boundary because the research strongly supports it. Azra already describes patient matching, prescreening, and criterion-level traceability as existing capabilities. Building another matching model would duplicate Azra's work and introduce an unnecessary clinical decision layer. V3 still begins with an existing potential match and ends with a reviewed patient-facing message.

I also kept the main demonstration sequence from V2. The clinician opens a patient, generates the Why Me message, checks the evidence behind a personalized statement, revises the draft, approves it, and switches to the patient view. That sequence remains the clearest way to show why the project is more useful than a generic trial summary.

The prototype remains intentionally small. It still uses one complete patient-to-trial example, synthetic patient data, a simple interface, simulated delivery, and no live hospital integration. The research gave us reasons to improve this vertical slice, not expand it into a full recruitment platform.

## Changes to the patient message

The Duke patient-portal study was the strongest reason to revise the patient-facing packet. Patients wanted recruitment messages to explain why the study related to them, but they also wanted enough practical information to decide whether a follow-up conversation was worth their time. V2 already included the Why Me explanation, study purpose, participation overview, questions, and next step. V3 keeps those sections and makes the requirements more specific.

I added a clear subject-line requirement and expanded the participation section to include visits, procedures, duration, location, whether participation is in person or remote, compensation or reimbursement when available, and approved contact information. I also changed the risks section into Important Things to Know. This section now focuses on facts that can be stated safely in an initial recruitment message: participation is voluntary, declining does not affect normal care, final eligibility is not confirmed, and the message does not replace informed consent.

This change also corrected an important source problem in V2. The earlier plan could be read as allowing the system to translate any risk information found in the trial record. The research findings explain that ClinicalTrials.gov should not automatically be treated as the complete source for detailed risk or benefit language. V3 therefore requires the system to use an approved protocol, recruitment template, consent material, or another institution-approved source for those statements. If that source is unavailable, the prototype must omit the detail and direct the patient to the study team.

## Added plain-language rules

V2 said that the message should be clear and written in plain language, but that was not specific enough to guide the prompt or test the output. V3 adds concrete rules based on CDC and MRCT health-literacy guidance. The message must put the reason for the outreach first, use short headings and paragraphs, prefer active voice and common words, define necessary clinical terms, and keep one main idea in each sentence.

The rules also prohibit language that implies guaranteed benefit, final eligibility, or a medical recommendation. The model cannot invent a procedure, risk, time commitment, diagnosis, treatment history, or study benefit that is not in the approved source material.

I kept a possible sixth- to eighth-grade reading estimate as a supporting quality check. I did not turn it into a pass-or-fail measure of comprehension because a grade-level score cannot prove that a patient understands the message. Representative-patient testing would be more meaningful in a future pilot.

## Stronger source grounding and clinician control

The largest technical change is a measurable source-coverage requirement. V3 sets a prototype target of 100 percent of patient-specific factual statements having at least one source reference. This does not prove that every statement is clinically correct, but it gives the team a concrete way to demonstrate the intended grounding mechanism.

I also added an approved source pack as a formal input. Instead of passing a large chart and a trial page to the model, the backend should send structured patient facts, trial facts, Azra match evidence, and the approved patient-facing source for each section. The model returns structured sections with source IDs, which allows the interface to show the supporting evidence to the clinician.

V3 retains direct editing and targeted section regeneration because they protect content the clinician has already reviewed. I added an approval lock or approved-version state so the demo can show exactly which version was used for the simulated send. This is a small prototype feature, but it makes the workflow more realistic and easier to explain.

## One real trial and a cached fallback

V2 allowed a real or realistic trial. I changed that requirement to one real ClinicalTrials.gov study because the public API makes this practical and gives the demo a stronger source basis. The patient remains synthetic, and the Azra match object remains a clearly labeled mock representation of Azra's existing prescreening output.

I also made a cached JSON copy of the trial response part of the required plan. The live API can still be used during development, but Demo Day should not depend on an external service. The same principle applies to the LLM call: the team should keep a known-good generated example and screenshots or a short recording for the backup path.

## Delivery is now channel agnostic

V2 described a portal or email-style patient view, but the research shows that no single delivery channel is always best. Portal recruitment is common, while randomized studies have produced different results when comparing portal and email engagement. V3 therefore separates message generation from message delivery.

The product creates one approved outreach artifact. A health system could route that artifact through a portal, an approved email workflow, a text notification that directs the patient to a portal, or another approved channel. The prototype still shows one portal or email-style experience, but the plan no longer presents that interface as the only production design.

I also added the generic-notification pattern as an optional demonstration. An ordinary email or text can say that a new research message is available, while the personalized content remains in the secure portal. This is a useful way to explain privacy without building a real messaging integration.

## Added governance and production assumptions

The research on recruitment guidance made it necessary to explain where the prototype stops. A real deployment may require IRB review of recruitment language, institution-approved templates, patient contact preferences, privacy and security controls, audit logs, data-retention rules, and an approved enterprise model environment. V3 includes these as production assumptions instead of pretending that the case-competition prototype solves them.

I did not add IRB workflow software, authentication, production security infrastructure, or a live EHR connection to the build. Those additions would consume the week without improving the core demonstration. The prototype uses synthetic data, shows a clinician approval step, and makes no claim that it is HIPAA compliant.

## Revised success measures

V2 already avoided claiming that the prototype would increase enrollment or retention. V3 keeps that boundary and makes the immediate measures more concrete.

The prototype can test whether every personalized factual statement has a source, whether required message sections are present, whether prohibited eligibility or benefit language is absent, whether a clinician can inspect and revise the message, and whether the complete demo works from cached inputs. These are results the team can actually show by Friday.

A future pilot could measure clinician preparation time, the number and type of edits, the percentage of sections approved as written, patient-reported clarity, and whether patients understand why the study was sent to them. Enrollment, retention, screen-failure rates, informed consent, and time savings still require real-world evidence.

## Changes to team responsibilities and the weekly schedule

The team structure did not change, but several assignments became more specific. Business 3 now owns the patient-facing source map and plain-language checklist in addition to the example message. Business 2 owns the prototype acceptance measures and governance assumptions. CS 1 owns source-coverage validation, cached trial data, and the structured source pack. CS 2 owns the approved-version state and simulated channel handoff.

Tuesday now includes selecting the real trial, saving the cached response, freezing the source hierarchy, and agreeing on the defendable claims. Wednesday focuses on evidence links, validation, clinician controls, and alignment between the prototype and presentation. Thursday remains the feature freeze and rehearsal day, but the backup path now includes cached data and a known-good generated message.

## Features I removed or kept out of scope

V3 explicitly keeps the following work out of the Friday build:

- A new matching or eligibility model
- Automatic final eligibility decisions
- Autonomous sending without clinician approval
- Real patient data or PHI
- Live EHR, FHIR server, portal, email, or text integration
- Production HIPAA and security infrastructure
- Formal consent or electronic signatures
- IRB workflow software
- Detailed risk or benefit generation from incomplete sources
- A patient chatbot or automated medical advice
- A full recruitment CRM or analytics dashboard
- A comprehension quiz as the center of the patient experience

I did not remove these because they are unimportant. I kept them out because they either duplicate Azra, create governance and safety problems, or require more time than the competition allows. The strongest use of the week is proving the grounded communication workflow.

## Questions that remain for Azra

The research also revealed questions that cannot be answered from public information. V3 records the most important ones so the team can separate a prototype assumption from a production requirement. We still need to know the exact structure of Azra's match evidence, which patient-facing study materials are approved, who initiates and approves outreach, which delivery channels matter across customers, how research-contact opt-outs are stored, and which model environments and audit rules Azra already supports.

These questions should guide a real implementation after the competition. They should not delay the current prototype because V3 uses explicit mock inputs and states those assumptions in the demo.

## Bottom line

V3 is not a larger version of V2. It is a more disciplined version.

The plan still proves one idea: Azra can take the evidence behind a potential trial match and help a clinical team turn it into a patient-facing explanation. The changes make that idea easier to defend because the message has clearer content rules, every personalized fact has a source, the clinician remains responsible for the final version, and the delivery and governance claims stay within what the research supports.

