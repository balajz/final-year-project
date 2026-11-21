# 17 — Applications and Use Cases

## 1. Primary Application

A screening-stage triage adjunct for paediatric attention-related assessment. The instrument consumes a
resting EEG recording and emits a calibrated index plus an abstention decision, intended to stratify
referral urgency rather than to diagnose.

## 2. Deployment Scenarios

| Scenario | Role | Constraint |
|---|---|---|
| Community / school screening | Tier-1 triage to identify children warranting specialist assessment | Offline, laptop-operable, no clinician required for the arithmetic |
| Primary-care referral routing | Support a clinician deciding whether referral is indicated | Operates alongside, never replacing, clinical judgement |
| Research cohort quality control | Quantify the artifact burden of a dataset before analysis | The measurement instrument use case |
| Retrospective re-evaluation | Re-report published cohort performance under subject-disjoint, artifact-paired protocol | Methodological use |

## 3. Use Cases by Panel

**Panel 1 (Screening).** A clinician uploads a recording; the panel returns the index, the matched
operating point, PPV at 5% and 10% prevalence, and an abstention state with a plain-language reason.

**Panel 2 (Reliability).** A user inspects the risk–coverage curve to choose a coverage level, reviews
which segments were abstained and why, and verifies the reproducibility badge and connectivity-integrity
line before trusting the output.

**Panel 3 (Topology).** A researcher inspects the cortical graph, coloured by the aperiodic exponent and
pruned by the learned gate, with a split-half stability metric guarding against decorative
interpretation.

## 4. Realistic Use-Case Boundaries

- The tool is a triage index, not a diagnosis; it is not appropriate for treatment decisions.
- It is validated on a specific resting 19-channel 128 Hz protocol; other protocols require
  revalidation.
- It is not a general EEG analysis platform.
- Its value at a given site depends on the local prevalence, which the user must supply.

## 5. Unsupported Claims Avoided

No claim is made of:

- Clinical efficacy or regulatory approval.
- Generalisation beyond the validated protocol.
- A diagnosis of any condition.
- Superiority over clinical assessment.

## 6. Who Benefits

| Party | Benefit |
|---|---|
| Clinician | A quantitative, trustworthy second opinion with explicit uncertainty |
| Caregiver | Fewer false alarms, so fewer unnecessary referrals and less anxiety |
| Health system | Better allocation of scarce specialist capacity |
| Researcher | A rigorous, artifact-aware evaluation protocol and baseline |
