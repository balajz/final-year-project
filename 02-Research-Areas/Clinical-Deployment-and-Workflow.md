---
tags:
  - research-area
  - deployment
  - clinical
  - workflow
  - ethics
---

# Clinical Deployment & Workflow (Who Is Actually Helped, and How)

The brief explicitly asks for work that benefits clinicians, caregivers and researchers — not only patients, and not only classifiers. This note is the missing half of every model note in the vault.

## 1. The Beneficiary Table
| Beneficiary | What they need | What AI can realistically give | What it cannot |
|---|---|---|---|
| **Patient** | Fewer tests, faster answers, less uncertainty | Faster triage, better monitoring | A diagnosis on its own |
| **Caregiver** | Reassurance, escalation guidance, seizure/sleep diaries | Automated summaries, anomaly alerts | Medical authority |
| **Clinician** | Time, prioritisation, fewer false alarms | Pre-read, QC, abstention, second opinion | Replacement judgement |
| **EEG technician** | Faster, more consistent recording | Automated impedance/QC feedback | Full automation |
| **Researcher** | Reproducibility, comparable baselines | Audit harnesses, benchmark suites | Novelty |
| **Payer / health system** | Cost per true case found | Cheaper screening, reduced repeat tests | Cost-effectiveness without evidence |

## 2. The Metrics That Decide Adoption
Accuracy is not one of them.

| Metric | Why it decides adoption | Vault note |
|---|---|---|
| **PPV / NPV at realistic prevalence** | A 90%-accurate test at 5% prevalence can have PPV < 30% | [[Decision-Log]] commitment 8 |
| **False alarms per hour/day** | Alarm fatigue destroys clinical trust faster than poor accuracy | commitment 14 |
| **Calibration (Brier, ECE)** | A clinician cannot act on an uncalibrated probability | commitment 8 |
| **Time saved per case** | The actual selling point of pre-read tools | — |
| **Abstention rate at a target error rate** | "I don't know" is a feature, not a failure | commitment 8 |
| **Subgroup performance** | Age, sex, site, comorbidity, skin tone, hair type | new — see §4 |
| **Performance under dataset shift** | New amplifier, new montage, new population | [[Subject-Level-Evaluation-Hygiene]] |

## 3. The Deployment Realities
- **Regulatory.** US: FDA SaMD pathways (510(k), De Novo, PMA depending on risk). EU: MDR plus the **AI Act**, which classifies many clinical decision-support tools as high-risk and imposes documentation, human-oversight and post-market monitoring obligations. Any claim of clinical utility in a report should acknowledge this, without pretending to satisfy it.
- **Liability and oversight.** A tool that recommends and a clinician who decides is a different product from a tool that decides. Human-in-the-loop is not a courtesy; it is the regulatory category.
- **Dataset shift.** Models degrade silently. Post-market monitoring, drift detection and re-calibration are the difference between a demo and a device.
- **Equity.** EEG is notoriously sensitive to hair type, skin conductivity and electrode contact. Cohorts are rarely representative. Performance by subgroup is a required analysis, not an optional one.
- **Integration cost.** A model that requires a new amplifier, a new file format, or a manual export will not be used. Workflow fit beats accuracy.

## 4. The Under-Served Project Space
Things that are useful, publishable, and do not require a new biomarker:

1. **Quality-control and artifact auditing.** Score a recording before analysis; tell the technician what to fix. The vault already owns the intellectual machinery ([[Class-Correlated-Artifact-Control]]).
2. **Abstention and triage.** Route the ambiguous 20% to a human, auto-clear the easy 80%. Measurable, deployable, and directly matches how screening works.
3. **Second-read / pre-read.** Flag suspicious segments for a reader rather than replacing the read. Lower regulatory burden, clear time saving.
4. **Alarm reduction.** Suppress false alarms in ICU/EMU monitoring while preserving detection — a well-defined engineering problem with hard ground truth.
5. **Report generation and summarisation.** Turn hours of EEG plus behavioural logs into a structured summary. LLM-adjacent, but requires careful hallucination control.
6. **Caregiver-facing summarisation.** Sleep quality, seizure frequency, escalation triggers, in plain language.
7. **Benchmark and audit infrastructure.** The most cited contribution a small lab can make; also the most reusable.

## 5. What a Strong Final-Year Version Looks Like
Not "we built a classifier." Something like:

> A QC + abstention layer that sits in front of an existing ADHD or seizure pipeline, quantifies how much of the pipeline's output is driven by recording quality, and routes ambiguous cases to a human — evaluated on PPV at realistic prevalence and on false-alarm rate per hour.

That is cheap, uses public data, has a measurable evaluation, does not claim clinical authority, and is genuinely useful. It is also exactly what the vault's 18 commitments already describe.

## 6. Risks
- **Clinician input is hard to obtain.** Without it, "workflow" claims are speculative. State the assumption explicitly.
- **Regulatory language can be overclaimed.** Do not say "clinically validated" for a public-dataset result.
- **Utility without a user.** A tool nobody asked for is still a tool nobody uses; interview at least one clinician or technician if possible.

## 7. Connections
- [[Problem-Space-Map]] · [[Personalization-and-Domain-Adaptation]] · [[Multimodal-Physiological-Signals]]
- Concepts: [[Subject-Level-Evaluation-Hygiene]], [[Explanation-Stability-and-Faithfulness]]
- Opportunities: [[Class-Correlated-Artifact-Control]]
- Candidates: [[Candidate-Evidence-Aware-ADHD-Screening]]
- Decisions: [[Decision-Log]] commitments 8, 13, 14, 16
