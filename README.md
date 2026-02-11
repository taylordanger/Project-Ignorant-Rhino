Replication analysis repo

Purpose
This repository contains a minimal analysis pipeline template for the pre-registered replication study of "Polyatomic time crystals...". It provides scripts to load raw HDF5 time-series, run automated preprocessing and Welch PSD computation, detect spectral peaks, and produce a simple report.

Quick start
1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the pipeline on a raw HDF5 file:

```bash
python -m src.analysis_pipeline --input data/example_raw.h5 --output results/
```

Repository structure
- src/: analysis scripts
- config/: pre-registration parameters and analysis settings
- data/: (not committed) raw HDF5 files
- results/: generated outputs
- notebooks/: template analysis notes

Contributing
- Add unit tests for new analysis functions and keep the pipeline deterministic.

License: MIT
