---
tags:
  - project-idea
  - candidate
  - bci
  - eeg
  - cross-session
  - calibration
  - alignment
status: candidate-not-selected
---

# Candidate: Session-Shift BCI — Does Alignment Substitute for Re-Calibration?

> **Status: candidate, NOT selected.** Derived in this vault (not user-authored) from [[Liu-2026-EEG-FM-Compass-Benchmark]] §3 and §4.9, [[Unsupervised-Alignment-Leverage]], and [[BCI-Paradigms-and-Applications]] §4.1.
> **First candidate from the BCI quadrant** — unblocks commitment 19, which required at least one candidate from outside the ADHD-measurement cell. It must still be weighed against the other three on the same seven criteria.

---

## 1. Real-World Problem

Every non-invasive BCI needs a calibration block before it works: the user sits, performs imagined movements or attends to stimuli, and the decoder is fitted to that session. In the literature this is reported as "20–40 trials per class" — a number that sounds small and is, in practice, 5–20 minutes of a user's time, **repeated every session**, because EEG changes across days: cap placement shifts, impedance changes, electrode gel dries, the user's strategy drifts.

Two literatures have grown up around this and they do not meet:

- **Cross-session transfer** studies the shift (session-to-session adaptation is a classic BCI problem).
- **Cross-subject transfer** studies a *different* shift, and is what every modern benchmark reports.

The deployment condition — **same user, new day, new cap placement** — is neither, and it is the one the user actually experiences. Compass makes this concrete: its LOSO protocol is across-subject-same-session, and its few-shot protocol for MI/P300 is *within one session*. The missing cell is the deployment cell.

## 2. The Gap, Stated Precisely

Compass's two scenarios and what they cover:

| | Same session | Different session |
|---|---|---|
| **Same subject** | few-shot protocol ✅ | **nobody benchmarks this** ❌ |
| **Different subject** | LOSO protocol ✅ | — |

This is not a gap in one paper. It is a gap in the benchmark convention: subject-disjoint evaluation was the field's correction for leakage, and it displaced session-disjoint evaluation — which is a *different* and, for a BCI product, a *larger* shift. The evidence that it matters is in the paper's own tables: a change in the *amount* of same-session labelled data moves the classical-vs-foundation gap by 25 accuracy points on BCIC-IV-2a. A change of *session* is a bigger perturbation than a change in the number of trials, and its effect on that gap is unmeasured.

## 3. Core Contribution

A **calibration-budget audit** with an exchange rate as the headline quantity.

**Primary question.** How many labelled trials from a new session does unsupervised session-wise alignment replace?

- **Arm A — no adaptation.** Fit on session 1, test on session *s*. The floor.
- **Arm B — unsupervised alignment only.** Euclidean / Riemannian alignment on the target session's *unlabelled* windows, no labels used. Costs a short unlabelled recording, not a labelled task block.
- **Arm C — k labelled trials.** k ∈ {5, 10, 20, 40, 80}, fitted on the target session. The current practice.
- **Arm D — alignment + k.** Whether they compose or substitute.

**The exchange rate** `k*` = the number of labelled trials at which Arm C matches Arm B. Then the deployment sentence becomes one line: *"alignment on 3 minutes of unlabelled rest is worth N labelled trials"* — or, if `k*` is small, *"labelling five trials is cheaper than any of this, and the field's cleverness is buying nothing."* **Both outcomes are publishable and one of them is a genuinely useful negative result.**

Three supporting pieces, each of which is what makes it a contribution rather than a transfer:

1. **Session-identification probe as a precondition.** Before asking whether adaptation helps, ask whether there is a shift to adapt to: can a classifier tell session 1 from session 2 using the features the decoder uses? If session identity is at chance, the premise is dead and the cross-session literature needs re-reading. Nobody runs this check before reporting a transfer gain, and it costs nothing.
2. **The decomposition.** What alignment removes that labelled trials also remove (shared: covariance geometry, scale, reference) vs what it cannot (session-specific neural strategy, drift in the aperiodic background, new artifacts). This is the BCI analogue of the `{aperiodic} × {alignment}` 2×2 already designed for ADHD in [[Decoding-Multiverse-and-Aperiodic-Identity]] §4 — **the same mechanism question, on a target where the labels are true.**
3. **Who fails.** Per-subject slopes, not just means. If alignment rescues most users and cannot rescue a minority, that minority is a candidate *BCI-illiteracy* phenotype, and its features (aperiodic exponent drift, resting alpha, artifact load) are the interesting part. This is [[BCI-Paradigms-and-Applications]] §4.2, arrived at from the other direction.

## 4. Why It Beats "Model X on Dataset Y"

- **The headline is a deployment quantity** (minutes of user time, trials-to-criterion), not a benchmark score. Nobody can ask "so what?" of a number that is literally minutes saved per session.
- **The labels are true.** The instruction is the label; there is no clinician, no rating scale, no |d| ≈ 0.2. This is the well-posed-target advantage of the BCI quadrant, and it is the reason a positive result is achievable here when the ADHD branch only ever produced ceilings.
- **It is a measurement contribution, not a model contribution** — the shape the vault has already decided is defensible, applied to a quadrant with large effect sizes.
- **It uses the vault's existing mechanism.** EA, the alignment decomposition, the aperiodic fingerprint, and the subject-as-unit rule all transfer directly. Nothing new has to be invented; the work is in the protocol.
- **It is laptop-feasible.** Nine to fifty-four subjects, 2–5 sessions, 2–4 classes, CSP/LDA and EEGNet-scale models. No pre-training, no A100s, no 1.9 TB.

## 5. Data (documented public; access not verified by us)

| Dataset | Subjects | Sessions | Classes | Status |
|---|---|---|---|---|
| **BCI Competition IV 2a** | 9 | 2 (different days) | 4 MI | ✓ established, in [[BCI-Paradigms-and-Applications]] |
| **BCI Competition IV 2b** | 9 | **5** | 2 MI, 3 bipolar channels | ✓ established |
| **Lee2019 / OpenBMI MI** | 54 | 2 | 2 MI | ~ verify availability and licence |
| **Kaya 2018 (GigaDB) MI** | 9 | multiple days, 3 sessions | 2 MI | ~ verify |
| PhysioNet EEGMMIDB | 109 | **1** (14 runs) | real/imagined movement | ✗ *not* cross-session — do not use for the main claim |

**The binding constraint is n = 9** for the two canonical datasets. That is not a sample of a population; it is the population. Consequences, which must be stated in any design: report per-subject results with the subject as the unit; use paired within-subject tests; never report a confidence interval over subjects as if it estimated a population parameter; treat a 54-subject replication (Lee2019) as the thing that makes the claim general, and the 9-subject result as the thing that makes it visible.

## 6. Scorecard Against the Seven Criteria ([[00-Project-Overview]] §4)

| Criterion | Assessment |
|---|---|
| 1. Real-world problem | **Strong.** Calibration time is the main usability complaint about non-invasive BCI and is paid every session. |
| 2. Meaningful AI contribution | **Moderate–strong.** Unsupervised adaptation with a measured exchange rate against supervision; not a new architecture, and does not need to be. |
| 3. Defensible novelty | **Unverified — the main risk.** Cross-session transfer is well populated. The delta is the exchange-rate framing + the session-identification precondition + honest small-n statistics. A prior-art check is mandatory before selection. |
| 4. Practical implementation | **Strong.** CSP+LDA, Riemannian tangent-space classifiers, EEGNet. CPU/laptop. One student, one semester. |
| 5. Data feasibility | **Strong on access, weak on n.** Public, small, standard, no DUA. 9 subjects is the limit. |
| 6. Evaluation rigour | **Strong by construction** — the protocol *is* the contribution. Within-subject, cross-session, permutation null, held-out session, no window leakage (whole runs held out, not windows). |
| 7. Post-college extensibility | **Strong.** A calibration-budget curve is a reusable reporting standard and a natural open-source tool; it extends to any BCI paradigm and to consumer EEG. |

## 7. Risks and the Honest Novelty Problem

1. **Cross-session BCI is not a new topic.** Session-to-session transfer learning has a substantial literature. If a paper already reports accuracy-vs-calibration-trials curves for aligned vs unaligned decoders, this candidate collapses to a replication. **A prior-art check is the first thing to do, not the last** — the same failure mode as A3 for the multiverse candidate.
2. **The 9-subject ceiling.** A 9-subject, 2-session design cannot support a general claim. It can support a *demonstration* and a *protocol*. Frame it as such, or add Lee2019.
3. **Transductive alignment can be read as peeking.** It is unsupervised, but it uses the target session's data before the test block. The assumption — a short unlabelled recording is available — must be stated up front, and the zero-shot baseline must be reported next to it.
4. **The result may be boring.** If `k*` is small, the finding is "labels are cheap; alignment is not a substitute." That is a legitimate measurement result and it *deflates* a large literature, which is exactly the shape of contribution this vault has been producing. But it will read as a negative result to a supervisor expecting a system.
5. **Artifact drift across sessions is a confound, not just a nuisance.** Caps are re-placed; impedance and line noise change. If alignment helps mainly by re-normalising *recording geometry* rather than neural covariance, the neural interpretation fails while the deployment claim survives. Both readings must be measured: per-session line-noise power, EMG-band power, and the aperiodic exponent.

## 8. Kill Conditions

- **Premise dead:** session-identification accuracy ≈ chance on the features the decoder uses, on both 2a and 2b → there is no shift worth adapting to, and the candidate becomes a null result about the literature rather than a project.
- **Framing dead:** `k* ≤ 5` trials on every dataset → alignment is not a substitute for calibration; reframe as "the calibration burden is smaller than assumed," which is a smaller paper.
- **Novelty dead:** a published calibration-budget curve with alignment exists → either drop, or pivot to the *who-fails* analysis (piece 3) if that is unclaimed.
- **Scope dead:** only one dataset shows the effect and the other reverses → dataset artifact; do not report.

## 9. Open Questions Before Selection

1. **Prior art.** Has anyone reported accuracy as a function of labelled trials *and* unlabelled alignment windows, on a held-out session, with the subject as the unit? (Reading/reasoning answerable.)
2. **Does BCI-IV-2b's 5 sessions make it the better primary dataset** than 2a's 2? More sessions means more within-subject shift estimates; 3 bipolar channels means a much weaker decoder.
3. **Is Lee2019 MI accessible** with 2 sessions × 54 subjects, and does it have the same paradigm?
4. **What is the published cross-session ceiling** on 2a/2b for CSP+LDA and for EEGNet? If it is already near the within-session number, there is little shift to recover and the premise weakens before any design work.
5. **Does the aperiodic exponent drift across sessions** in a way that predicts who fails? This is the cheapest link to the vault's A4 hypothesis, and it is answerable from published re-analyses rather than from new data.

## 10. Competing Candidates (none selected)

- [[Candidate-Decoding-Multiverse-Aperiodic-Audit]] — strongest existing candidate; ill-posed target, measurement lever, HBN.
- [[Candidate-Event-Locked-NeuroBehavioral-HBN]] — event-locked paradigm contrast, HBN, ill-posed target.
- [[Candidate-Evidence-Aware-ADHD-Screening]] — calibration/abstention, weakest standalone, strongest add-on.
- **This one** — best-posed target, largest effect sizes, smallest n, novelty unverified.

The honest comparison: this candidate is the only one where a *positive* result is likely and the only one that fits the seven criteria without a caveat on feasibility. It is also the only one whose novelty could be destroyed by a single existing paper. Those two facts are the decision.

## 11. Connections
- **Papers:** [[Liu-2026-EEG-FM-Compass-Benchmark]] (protocol gap + the 25-point inversion) · [[Wang-2025-CBraMod-CrissCross-Brain-Foundation-Model]] (alignment evidence, measured on MI)
- **Areas:** [[BCI-Paradigms-and-Applications]] · [[Personalization-and-Domain-Adaptation]] · [[Problem-Space-Map]]
- **Concepts/opportunities:** [[Unsupervised-Alignment-Leverage]] · [[Subject-Level-Evaluation-Hygiene]] · [[Aperiodic-1f-Activity-and-Band-Ratios]] · [[Decoding-Multiverse-and-Aperiodic-Identity]]
- **Decisions:** [[Decision-Log]] 19 · [[Reading-Queue]] §2 (prior-art question)
