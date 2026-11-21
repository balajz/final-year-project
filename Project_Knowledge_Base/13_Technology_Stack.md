# 13 — Technology Stack

Status legend: **Confirmed** (verified present and exercised), **Proposed** (selected, not yet
exercised), **Optional** (allowed but not required), **TBD** (not yet specified).

## 1. Programming Languages

| Technology | Version | Status | Role |
|---|---|---|---|
| Python | 3.15 | **Confirmed** | Primary implementation language |
| Mermaid | — | **Confirmed** | Architecture and flow diagrams |

## 2. Numerical and Scientific Libraries

| Library | Status | Role |
|---|---|---|
| NumPy | **Confirmed** (2.5.x) | Matrix algebra, FFT, eigendecomposition, linear models |
| SciPy | **Proposed** | Signal filtering, Hilbert transform, statistical tests |
| spectrum / specparam | **Proposed** or **Optional** | Spectral parameterisation; may be implemented natively as a linear fit |
| scikit-learn | **Proposed** | Cross-validation utilities, calibration, metrics |
| pandas | **Optional** | CSV handling only; native parsing is sufficient |

> **Design note.** The geometry, connectivity, and guard layers are implemented natively in NumPy. This
> is a deliberate constraint: it keeps the offline artefact dependency-light and makes the mathematical
> operations auditable rather than delegated to a framework.

## 3. EEG and Data-Access Libraries

| Library | Status | Role |
|---|---|---|
| mne | **Proposed** | `.set`/`.bdf`/`.edf`/`.fif` readers, montage handling |
| mne[hdf5] | **Proposed** | HDF5 backend required for modern EEGLAB `.set` files |
| h5py | **Proposed** | HDF5 access for large `.set` files |
| pymatreader | **Proposed** | MATLAB-structure reading for EEGLAB metadata |
| AWS CLI / S3 client | **Optional** | HBN BIDS download from public object storage |

## 4. Machine-Learning Frameworks

| Framework | Status | Role |
|---|---|---|
| PyTorch | **Proposed** | Graph attention, temporal encoders, calibration heads |
| PyTorch Geometric | **Optional** or native | GATv2 layers; a native implementation is feasible at 19 nodes |

## 5. Models and Components

| Component | Status | Notes |
|---|---|---|
| Joint Löwdin oAEC | **Confirmed** | NumPy implementation |
| SPD guard | **Confirmed** | NumPy implementation |
| Fréchet mean + tangent projection | **Confirmed** | NumPy implementation |
| Alignment arms | **Confirmed** | Ablation harness |
| SpecParam fit | **Confirmed** | Linear fit in log-log space with R² acceptance |
| Artifact-proxy model | **Confirmed** | Logistic regression on recording-quality features |
| GATv2 spatial encoder | **Proposed** | Not yet trained |
| Parallel Transformer + BiGRU temporal encoder | **Proposed** | Not yet trained |
| Calibration layer | **Proposed** | Method not finalised |
| Evidence gate | **Proposed** | Policy not finalised |

## 6. Presentation and Interfaces

| Technology | Status | Role |
|---|---|---|
| Static HTML report | **Proposed** | Phase 1 output |
| Local web workbench | **Proposed** | Three-panel interface |
| Bundled offline assets | **Proposed** | No cloud dependency for demonstration |

## 7. Hardware and Deployment Environment

| Item | Status | Notes |
|---|---|---|
| Consumer laptop (Apple Silicon or x86) | **Confirmed** | Reference development and demonstration target |
| Offline operation | **Confirmed** requirement | No network dependency during inference |
| Storage for HBN mini-sets | **Confirmed** requirement | Several GB per mini-set |
| GPU acceleration | **Optional** | Not required; models are small |
| Cloud infrastructure | **Not used** | Deliberate |

## 8. Development Environment

| Item | Status | Notes |
|---|---|---|
| Isolated virtual environment | **Confirmed** requirement | Required by PEP 668 on modern macOS |
| Git version control | **Proposed** | Not yet initialised |
| Configuration via file | **Proposed** | Holds band edges, thresholds, seeds, and paths |

## 9. Data Formats

| Format | Status |
|---|---|
| CSV (`.csv`) | **Confirmed** — primary benchmark format |
| EEGLAB (`.set`) | **Proposed reader**, format confirmed |
| Biosemi (`.bdf`) | **Proposed reader** |
| EDF (`.edf`) | **Proposed reader** |
| FIF (`.fif`) | **Optional** intermediate cache |
| JSON | **Confirmed** — result records and evaluation outputs |
| NPZ | **Confirmed** — cached feature archives |

## 10. Constraints on the Stack

1. **Offline-first.** No inference-time network dependency.
2. **Dependency-light.** Geometry and connectivity are native NumPy.
3. **Auditable.** No mathematical step may be hidden inside an opaque framework call.
4. **Reproducible.** All stochastic steps seeded; configuration hashed into the result record.
