"""
data_loader.py -- Unified multi-format EEG ingestion module.

Supports:
- IEEE-121 CSV format (native zero-dependency NumPy/pure-Python parser)
- EEGLAB .set / .fdt (via MNE + pymatreader / h5py)
- BioSemi .bdf (via MNE)
- European Data Format .edf (via MNE)
- MNE .fif

Features:
- Automated channel normalization: modern 10-20 (T7/T8/P7/P8), legacy 10-20 (T3/T4/T5/T6), and EGI-128.
- Canonical 19-channel reordering.
- Missing optional dependency diagnostics with PEP 668 venv remediation.
"""

from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import csv
import os
import sys
import numpy as np

# Canonical 19-channel modern 10-20 layout
STANDARD_1020_19 = [
    "Fp1", "Fp2", "F3", "F4", "C3", "C4", "P3", "P4",
    "O1", "O2", "F7", "F8", "T7", "T8", "P7", "P8",
    "Fz", "Cz", "Pz"
]

# Legacy 10-20 to modern 10-20 / 10-10 equivalences
LEGACY_ALIASES = {
    "T3": "T7",
    "T4": "T8",
    "T5": "P7",
    "T6": "P8",
    "FP1": "Fp1",
    "FP2": "Fp2",
    "FZ": "Fz",
    "CZ": "Cz",
    "PZ": "Pz",
    "OZ": "Oz",
}

# Standard EGI HydroCel GSN 128 to 10-20 electrode mapping
EGI128_TO_1020 = {
    "E22": "Fp1", "E25": "Fp1",
    "E9": "Fp2",  "E8": "Fp2",
    "E33": "F7",  "E24": "F3",
    "E11": "Fz",  "E124": "F4",
    "E122": "F8", "E45": "T7",
    "E36": "C3",  "E129": "Cz", "CZ": "Cz", "VREF": "Cz",
    "E104": "C4", "E108": "T8",
    "E58": "P7",  "E52": "P3",
    "E62": "Pz",  "E92": "P4",
    "E96": "P8",  "E70": "O1",
    "E83": "O2",
}

def normalize_channel_name(ch: str) -> str:
    """Canonicalizes an electrode name to standard modern 10-20 casing."""
    c = ch.strip().strip("'\"")
    cu = c.upper()
    if cu in EGI128_TO_1020:
        return EGI128_TO_1020[cu]
    if cu in LEGACY_ALIASES:
        return LEGACY_ALIASES[cu]
    for std in STANDARD_1020_19:
        if cu == std.upper():
            return std
    return c

class EEGRecording:
    """Standardized in-memory container for 19-channel EEG."""
    def __init__(
        self,
        data: np.ndarray,              # shape (19, n_samples)
        sfreq: float,
        ch_names: List[str],           # Exactly 19 canonical names
        subject_id: str,
        label: Optional[str] = None,
        source_format: str = "unknown"
    ):
        assert data.shape[0] == 19, f"Expected 19 channels, got {data.shape[0]}"
        assert ch_names == STANDARD_1020_19, f"Channel ordering does not match STANDARD_1020_19"
        self.data = data.astype(np.float32)
        self.sfreq = float(sfreq)
        self.ch_names = list(ch_names)
        self.subject_id = str(subject_id)
        self.label = label
        self.source_format = source_format

    @property
    def duration_sec(self) -> float:
        return self.data.shape[1] / self.sfreq

    @property
    def n_samples(self) -> int:
        return self.data.shape[1]

    def epoch(self, window_sec: float = 2.0, step_sec: float = 2.0) -> np.ndarray:
        """Slices recording into 3D window array: (n_windows, 19, window_samples)."""
        w_samp = int(round(window_sec * self.sfreq))
        s_samp = int(round(step_sec * self.sfreq))
        n_samp = self.data.shape[1]
        if n_samp < w_samp:
            return np.empty((0, 19, w_samp), dtype=np.float32)
        
        windows = []
        for start in range(0, n_samp - w_samp + 1, s_samp):
            windows.append(self.data[:, start:start + w_samp])
        return np.stack(windows, axis=0) if windows else np.empty((0, 19, w_samp), dtype=np.float32)


def load_ieee121_csv(
    csv_path: str | Path,
    sfreq: float = 128.0,
    max_subjects: Optional[int] = None
) -> List[EEGRecording]:
    """Native zero-dependency parser for IEEE-121 CSV."""
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        raw_cols = [c.strip() for c in header]

        # Map header columns to canonical 19
        ch_indices = {}
        class_idx = None
        id_idx = None

        for idx, col in enumerate(raw_cols):
            if col.lower() == "class":
                class_idx = idx
            elif col.lower() == "id":
                id_idx = idx
            else:
                norm = normalize_channel_name(col)
                if norm in STANDARD_1020_19:
                    ch_indices[norm] = idx

        missing = [c for c in STANDARD_1020_19 if c not in ch_indices]
        if missing:
            raise ValueError(f"CSV is missing canonical 10-20 channels: {missing}")
        if id_idx is None:
            raise ValueError("CSV missing 'ID' column")

        # Map from canonical index (0..18) to CSV column index
        col_order = [ch_indices[c] for c in STANDARD_1020_19]

        subjects: Dict[str, Dict[str, Any]] = {}
        for row in reader:
            if len(row) <= id_idx:
                continue
            sid = row[id_idx].strip()
            if max_subjects is not None and sid not in subjects and len(subjects) >= max_subjects:
                continue
            
            cls = row[class_idx].strip() if class_idx is not None else None
            rec = subjects.setdefault(sid, {"label": cls, "data": []})
            
            vals = []
            for col_i in col_order:
                v_str = row[col_i].strip()
                try:
                    vals.append(float(v_str) if v_str else np.nan)
                except ValueError:
                    vals.append(np.nan)
            rec["data"].append(vals)

    recordings = []
    for sid, rec in subjects.items():
        arr = np.array(rec["data"], dtype=np.float32).T  # (19, n_samples)
        # Impute NaNs with median
        for c in range(arr.shape[0]):
            bad = ~np.isfinite(arr[c])
            if bad.all():
                arr[c] = 0.0
            elif bad.any():
                arr[c, bad] = np.nanmedian(arr[c])
        recordings.append(EEGRecording(
            data=arr,
            sfreq=sfreq,
            ch_names=STANDARD_1020_19,
            subject_id=sid,
            label=rec["label"],
            source_format="csv"
        ))

    return recordings


def load_mne_container(
    file_path: str | Path,
    subject_id: Optional[str] = None,
    label: Optional[str] = None
) -> EEGRecording:
    """
    Ingests .set, .bdf, or .edf via MNE.
    Validates presence of required dependencies and raises clean actionable errors.
    """
    file_path = Path(file_path)
    ext = file_path.suffix.lower()

    try:
        import mne
    except ImportError:
        raise ImportError(
            f"MNE is required to load '{ext}' files.\n"
            "To install in a virtual environment (PEP 668 compliant):\n"
            "    python3 -m venv .venv\n"
            "    source .venv/bin/activate\n"
            "    pip install mne pymatreader h5py scipy\n"
        )

    if ext == ".set":
        try:
            raw = mne.io.read_raw_eeglab(str(file_path), preload=True)
        except Exception as e:
            if "matlab" in str(e).lower() or "hdf" in str(e).lower():
                raise ImportError(
                    f"Loading large EEGLAB .set file requires 'pymatreader' and 'h5py'.\n"
                    f"Error was: {e}\n"
                    "Install via: pip install pymatreader h5py"
                )
            raise e
    elif ext == ".bdf":
        raw = mne.io.read_raw_bdf(str(file_path), preload=True)
    elif ext == ".edf":
        raw = mne.io.read_raw_edf(str(file_path), preload=True)
    elif ext == ".fif":
        raw = mne.io.read_raw_fif(str(file_path), preload=True)
    else:
        raise ValueError(f"Unsupported file format: {ext}. Expected .csv, .set, .bdf, .edf, or .fif")

    # Map raw channels to canonical 19
    raw_names = raw.ch_names
    norm_names = [normalize_channel_name(c) for c in raw_names]
    name_to_idx = {name: i for i, name in enumerate(norm_names)}

    missing = [c for c in STANDARD_1020_19 if c not in name_to_idx]
    if missing:
        raise ValueError(f"Recording '{file_path.name}' is missing 10-20 channels: {missing}")

    ordered_idx = [name_to_idx[c] for c in STANDARD_1020_19]
    data_19 = raw.get_data()[ordered_idx, :]

    sid = subject_id or file_path.stem
    return EEGRecording(
        data=data_19,
        sfreq=raw.info["sfreq"],
        ch_names=STANDARD_1020_19,
        subject_id=sid,
        label=label,
        source_format=ext[1:]
    )


def load_eeg(file_path: str | Path, **kwargs) -> List[EEGRecording]:
    """Unified entry point for EEG loading."""
    path = Path(file_path)
    ext = path.suffix.lower()
    if ext == ".csv":
        return load_ieee121_csv(path, **kwargs)
    else:
        rec = load_mne_container(path, **kwargs)
        return [rec]


if __name__ == "__main__":
    print("Testing data_loader.py...")
    test_csv = "data/adhdata.csv"
    if os.path.exists(test_csv):
        recs = load_ieee121_csv(test_csv, max_subjects=3)
        print(f"Loaded {len(recs)} test subjects from CSV:")
        for r in recs:
            print(f"  ID: {r.subject_id:6s} | Label: {r.label:7s} | Duration: {r.duration_sec:5.1f}s | Channels: {len(r.ch_names)} | Windows (2s): {len(r.epoch())}")
        print("✅ data_loader.py IEEE-121 ingestion PASSED.")
    else:
        print("CSV file not found, skipping IEEE-121 load test.")
