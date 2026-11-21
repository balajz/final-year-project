---
tags:
  - workflow
  - reading
  - triage
---

# Reading Queue & Intake Log

Purpose: stop re-reading papers we already screened, and keep a record of *why* a paper was queued, deferred, or rejected. Triage rules live in [[Paper-Triage-Checklist]].

## 1. Queue (not yet read)

| # | Paper | Added | Why it is queued | Priority |
|---|---|---|---|---|
| — | *(empty — awaiting the next paper)* | — | — | — |

## 2. Open Questions (answered by reading and reasoning, not by running code)
*These are things to resolve on paper. Nothing in this vault gets executed, downloaded, trained, or simulated.*

> **Product-layer obligations (added 2026-11-16).** [[Candidate-C5-Reliability-Screening-Workbench]] converted several open questions into *gates*: the Phase 2 `s_ASD` gauge stays unbuilt until the NITRC DUA is approved **and** the usable ASD `n` is confirmed; the input-format question (`.set`/`.bdf`/`.edf`) is now a hard product constraint; and the aperiodic-fingerprint question is explicitly *cohort-level only*. The risk rows that decide these are in [[09-Verification-Pending/V-01-Risk-Register-2026-11-16]].

| Question | Why it is open | What would close it |
|---|---|---|
| Re-derive Baibulova's theta dominance as a possible 1/f effect | [[Troendle-2026-TBR-Multiverse-HBN]] shows band effects can be aperiodic artefacts | A reasoned re-reading of their reported spectra; correction in [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]] |
| Verify the author list / venue of the TBR multiverse paper | Author list absent from the supplied excerpt | Correct metadata in [[Troendle-2026-TBR-Multiverse-HBN]] |
| Confirm ADHD-200 EEG subset size and per-site table | Currently flagged unverified in [[ADHD-200]] | Upgrade or drop ADHD-200 from Tier 2 |
| Does the HBN BIDS route carry a **clinical diagnosis**, or only the CBCL bifactors? | Documentation promises demographics + factors; clinical labels may live only in the NITRC phenotype | Determines whether an ADHD label is even available without the DUA — a design fact, not an experiment |
| Whether HBN releases overlap in subjects | Affects whether releases can be treated as one sample | Record in [[Healthy-Brain-Network-HBN]] §4 |
| Per-task `n` by age band in HBN | Sequence Learning uses 7 vs 10 targets by age; a paradigm effect could be an age effect | Feasibility note on [[Candidate-Event-Locked-NeuroBehavioral-HBN]] |
| Prior-art check for the decoding multiverse | [[Assumptions-Register]] A3 unverified | Keep, reframe, or kill the decoding candidate |
| **Produce one candidate from an empty quadrant** | [[Problem-Space-Map]] shows five documented-but-empty quadrants; commitment 19 blocks selection without one | A fourth candidate note, or an explicit rejection recorded in the log |
| **Decide A1** (measurement science vs working system) | [[Assumptions-Register]] A1 is load-bearing under everything | A recorded decision in [[Decision-Log]] |
| Does any published ADHD-200 or ABIDE study report **source-prediction accuracy** from its own features? | Would bound the ceiling on every pooled multi-site result | A number, or "nobody has done it" recorded as a gap |
| Is there a **leave-one-site-out** ADHD-200 result under a strict protocol? | The honest multi-site ceiling; unknown to us | Cite or mark as open |
| Are temporal-stability / FC-variability features correlated with **framewise displacement**? | If yes, the "dynamic FC" literature is partly a motion literature ([[Hidayah-2026-Multimodal-GNN-ADHD-ASD]]) | Re-read that literature net of motion |

**Resolved:** the methylphenidate provenance conflict (settled against the dataset's primary description; see [[Decision-Log]]).
**Not present:** the 8-universe pilot, pipeline smoke tests, and dataset downloads. Those belong to a later execution phase if the project is ever built; the vault only records that they would be the decisive tests, and what they would cost.

## 3. Screened Out (read, judged not worth a full note)
| Paper | Verdict | Date |
|---|---|---|
| Ward & Imran (2026), ABFR-KAN (MELBA) | **Held at triage** — rs-fMRI/ASD, outside our modality and direction; abstract + intro only | 2026-11-15 |

Log: [[2026-11-15-ABFR-KAN-Triage]]. Two ideas worth stealing if we ever revisit: atlas-free anchor-patch functional connectivity (parallels montage-agnostic spatial EEG representations), and KAN-vs-MLP fairness as a concrete instance of the "complexity must be earned" rule. Three red flags logged there: ABIDE subsetting (281 of >1,100 → differential attrition), parameter-matched MLP baselines, and ABIDE site/motion confounds.

## 4. Rejected at Triage (not read in full)
| Paper | Reason | Date |
|---|---|---|
| — | — | — |

## 5. Deferred (interesting, but not now)
| Paper | Reason for deferral | Revisit when |
|---|---|---|
| Ward & Imran (2026), ABFR-KAN | Held at triage — rs-fMRI/ASD, not EEG, not our direction. Full results not read. | Only if anchor-based atlas-free representations become relevant to our spatial encoder |
| ADHD-200 primary papers | Multi-site; only needed for cross-site replication | HBN result looks promising |
| Differential-diagnosis cohorts (ADHD vs ASD / tic) | Needed only if the ADHD-vs-Tic framing is revived | Public cohort located |

## 6. How to Add an Entry
When a paper arrives, add one row to §1 **before** reading it:

```
| N | FirstAuthor-Year-Topic | YYYY-MM-DD | one line: what it might change | high / med / low |
```

Then, after the 4-pass triage in [[Paper-Triage-Checklist]], move the row to §3 (screened out), §4 (rejected), or promote it to a full note in `01-Research-Papers` and delete the row.

**Rule:** every paper that becomes a note gets a session log in `06-Research-Log` and at least one forward link to a concept or opportunity. A note with no forward link is not finished.

## 7. Connections
- [[00-Project-Overview]] · [[Paper-Triage-Checklist]] · [[Decision-Log]]
