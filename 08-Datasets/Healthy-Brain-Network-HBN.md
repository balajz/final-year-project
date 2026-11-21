---
tags:
  - dataset
  - adhd
  - eeg
  - public
  - verified
---

# Healthy Brain Network (HBN)

**Status: primary cohort. Access verified 2026-11-15.**

## 1. Identity
- **Source:** Child Mind Institute, New York. Community-recruited biobank of children, adolescents and young adults; EEG releases cover ages **5–21** (the parent HBN study extends to 22).
- **Data paper (cite this):** Shirazi et al., *HBN-EEG: The Healthy Brain Network EEG Datasets in BIDS with HED annotations*, bioRxiv 2024. [DOI: 10.1101/2024.10.03.615261](https://doi.org/10.1101/2024.10.03.615261). Project paper: Alexander et al., *Sci Data* 2017, [DOI: 10.1038/sdata.2017.181](https://doi.org/10.1038/sdata.2017.181). Protocols: Langer et al., *Sci Data* 2017, [DOI: 10.1038/sdata.2017.40](https://doi.org/10.1038/sdata.2017.40).
- **Two access routes, both real:** see §6. The BIDS route requires **no DUA**.

## 2. Labels
- **Clinical:** K-SADS semi-structured diagnostic interview (parent + child ≥11 y), clinical judgement. ADHD subtyped (combined / inattentive / hyperactive-impulsive). IQ via WISC-V / WASI / WAIS by age.
- **Dimensional (this is the important part):** the BIDS releases ship **four CBCL-derived bifactor scores** in the participant metadata — **p-factor, internalizing, externalizing, attention** — as anonymised factor scores rather than raw item responses.
- **Why that matters:** it makes a **transdiagnostic specificity contrast** possible on public data — decode `attention` and check whether the same model decodes `externalizing` or `internalizing` equally well. If it does, the model is reading generic psychopathology, not attention. This is the public substitute for the private ADHD-vs-Tic cohort ([[Dankook-ADHD-vs-Tic-Private]]).

## 3. Acquisition
- **EEG:** 128-channel EGI HydroCel net, recorded at 250 or 500 Hz (Troendle et al. downsample all to 250 Hz), **Cz reference**, impedance < 40 kΩ.
- **Resting state:** alternating eyes-closed / eyes-open while the head rests on a chin rest; during eyes-open the child fixates a central cross. Troendle's analysis uses 5 min total (EO 20 s / EC 40 s cycles), compliance monitored by video.
- **Six tasks per participant** (HED-annotated, with reaction times and accuracy in `_events.tsv`):
  - *Passive:* **Resting State**, **Surround Suppression** (four flashing peripheral disks, ~3.6 min × 2 runs), **Movie Watching** (four short films).
  - *Active:* **Contrast Change Detection** (two flickering grated disks, respond to a contrast increase, immediate feedback), **Sequence Learning** (reproduce a flashed circle sequence with a mouse; **10 targets for ≥8 y, 7 for younger**), **Symbol Search** (computerised WISC-IV).
- **Not yet available:** eye-tracking and per-subject electrode locations are listed as *future* additions. Do not plan artifact control around EOG/eye-tracking in these releases.
- **Caveat:** every release nominally covers all tasks, but individual participants may have missing tasks or runs for technical reasons. Per-task `n` must be counted, not assumed.

## 4. Composition
**As used by [[Troendle-2026-TBR-Multiverse-HBN]]:** 1,499 identified → **1,122 analysable** after exclusions; 228 healthy control · 429 ADHD-combined · 465 ADHD-inattentive; 280 ADHD participants medicated in daily life; ages ~9.5–11.0 by group, with the **inattentive group oldest, controls middle, combined youngest**.

**As distributed in BIDS (releases 1–11):**

| Release | NEMAR ID | Subjects | Size |
|---|---|---:|---:|
| R1 | `ds005505` | 136 | 103 GB |
| R2 | `ds005506` | 152 | 120 GB |
| R3 | `ds005507` | 183 | 140 GB |
| R4 | `ds005508` | 324 | 230 GB |
| R5 | `ds005509` | 330 | 224 GB |
| R6 | `ds005510` | 134 | 91 GB |
| R7 | `ds005511` | 381 | 245 GB |
| R8 | `ds005512` | 257 | 157 GB |
| R9 | `ds005514` | 295 | 185 GB |
| R10 | `ds005515` | 295 | 160 GB |
| R11 | `ds005516` | 295 | 220 GB |
| **Total** | — | **2,782** | **~1.9 TB** |
| *NC* | `nm000103` | 458 | 251 GB (research-only; **not for commercial use**) |

Note `ds005513` is not used. Releases are chronological batches as data were collected; the source does not state whether any participant appears in more than one release — **assume they are disjoint but verify before pooling**.

⚠ **Numbering trap:** "Release 11" in the BIDS series (`ds005516`) is not necessarily the same snapshot as the "Release 11 (2022-11-23)" cited by [[Troendle-2026-TBR-Multiverse-HBN]]. Do not assume the BIDS R11 batch reproduces their 1,122-subject sample.

## 5. Storage and Compute Reality
- Full download is **~1.9 TB**. Each release is 91–245 GB. This is a disk-array job, not a laptop job.
- **Mini sets:** 20 participants who completed *all* tasks, **downsampled to 100 Hz**, in BDF and SET formats, distributed as Google Drive folders. These are the correct vehicle for a first pass.
- Selective S3 download is possible without credentials:
  ```bash
  aws s3 cp s3://fcp-indi/data/Projects/HBN/BIDS_EEG/cmi_bids_R1 ./R1 \
    --recursive --no-sign-request
  ```
  Restrict by subject/session with `--include`/`--exclude` patterns instead of pulling a whole release.
- **Consequence for the design:** any decisive test would have to run on a mini set or a single-release subject subset. A 1,000-subject specification curve would need either a cluster or a streaming feature-extraction pass that never stores raw data — a real constraint on the design, and a reason to prefer a 200–300-subject version.

## 6. Access
1. **BIDS / NEMAR / S3 (verified, no DUA):** NEMAR (`ds005505`–`ds005512`, `ds005514`–`ds005516`) or the public S3 bucket above. Free, anonymous, immediate.
2. **NITRC / FCON 1000** (https://fcon_1000.projects.nitrc.org/indi/cmi_healthy_brain_network): Data Usage Agreement, no fee; gives the full project (imaging, phenotypes) rather than EEG-only.
3. **Licence caveat:** the `nm000103` release is explicitly **not for commercial use**. If the project ever moves toward a product, that distinction matters. Cite the data papers.

## 7. Known Confounds
| Confound | Magnitude | Handling |
|---|---|---|
| **Movement / amplitude** | 197 subjects (12.6%) dropped for >60% epochs above 90 µV in Troendle | Report attrition **by group** ([[Decision-Log]] 16) |
| **Medication** | 280 medicated, not randomised | Specification dimension; report medicated vs unmedicated separately |
| **Comorbidity** | ~75% of ADHD cases carry a comorbid diagnosis | Specification dimension; do not exclude — it is the *point* of the bifactor design |
| **Age composition** | Groups differ by ~1.5 y, in a direction that interacts with IAF | Stratify or match; do not rely on linear age adjustment alone |
| **Task availability by age** | Sequence Learning uses 7 vs 10 targets by age band | Count per-task `n`; never let "paradigm" vary with "age" |
| **Release drift** | 11 batches, different collection dates and QC flags | Pin the release; treat batch as a grouping variable |
| **Subtype exclusion** | Hyperactive-impulsive-only (n = 85) too small for crossed designs | Report it; do not present the sample as all ADHD |

## 8. Reference Pipeline (published, reusable)
Automagic 3.1 → PREP bad channels (z > 5, correlation < 0.4, predictability < 0.75, SNR z > 5) → 0.5 Hz high-pass → ZapLine line noise → ICA on a 2 Hz-highpassed copy → **ICLabel p > 0.8 artifact removal** → interpolate → objective quality tiers (good / ok / bad) → 2 s segments → 90 µV rejection → FFT 1–40 Hz → **SpecParam** (R² ≥ 0.85). Code and extracted features: **OSF `u5yxv`**.

Adopting this pipeline is the cheapest way to get a credible feature set on day one — and it is also the *baseline* that any new preprocessing claim must beat.

## 9. Status in Our Project
- **Primary cohort** for the decoding multiverse and the aperiodic identity test ([[Decoding-Multiverse-and-Aperiodic-Identity]], [[Candidate-Decoding-Multiverse-Aperiodic-Audit]]).
- **Enabling cohort** for the event-locked contrast ([[Candidate-Event-Locked-NeuroBehavioral-HBN]]): HED events plus per-trial accuracy make stimulus-locked windows and error-trial analyses possible; the CBCL bifactors make the specificity test possible.
- Confirms **A2** in [[Assumptions-Register]] and unblocks both HBN candidates.
- Open design questions: (a) which release subset is affordable at 91–245 GB each; (b) per-task `n` by age band; (c) whether a **clinical diagnosis** exists in the BIDS metadata or only the CBCL factors; (d) which SpecParam implementation the reference pipeline used.

> **Scope note:** these are recorded as design considerations, not as work this vault performs. Nothing here is downloaded, trained, or run — see [[Decision-Log]] commitment 21.

## 10. Connections
- Papers: [[Troendle-2026-TBR-Multiverse-HBN]]
- Concepts: [[Aperiodic-1f-Activity-and-Band-Ratios]], [[Multiverse-and-Specification-Curve-Analysis]], [[Subject-Level-Evaluation-Hygiene]]
- Opportunities: [[Decoding-Multiverse-and-Aperiodic-Identity]], [[ADHD-Event-Locked-Connectivity-and-Leakage]]
- Candidates: [[Candidate-Decoding-Multiverse-Aperiodic-Audit]], [[Candidate-Event-Locked-NeuroBehavioral-HBN]]
- Datasets: [[ADHD-200]] (multi-site complement), [[IEEE-DataPort-ADHD-Child-121]] (pilot/audit cohort)
