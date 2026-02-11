Project Ignorant Rhino — replication analysis

Purpose
This repository contains an opinionated, minimal analysis pipeline and supporting materials to run the pre-registered independent replication of:

"Polyatomic time crystals of the brain neuron extracted microtubule are projected like a hologram meters away" (J. Appl. Phys. 2022; DOI:10.1063/5.0130618)

Status
- Pre-registration: included at `../replication_pre_registration_OSF.md`  
- Analysis template: `src/` (Welch PSD + automated peak detection)  
- Data: not included (raw HDF5 expected in `data/`)

Quick start
1. Create and activate a Python virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Put your raw HDF5 file(s) in `data/` (see `notebooks/TEMPLATE_ANALYSIS.md` for expected layout). Run the pipeline on a single file:

```bash
python -m src.analysis_pipeline --input data/example_raw.h5 --output results/run01
```

3. Inspect `results/run01/psd.png`, `results/run01/peaks.csv`, and `results/run01/summary.json` for automated outputs.

Configuration
- Analysis settings are in `config/pre_registration_config.yaml`. These parameters are fixed for the pre-registered analysis and should not be changed after data collection.

Data policy & reproducibility
- Store raw, unprocessed instrument outputs in HDF5 files with dataset `timeseries` and attributes such as `sampling_rate` and `sample_id`.  
- All analysis must be automated using the pipeline; manual peak-picking is prohibited by the pre-registration.  
- Upon completion, raw data and analysis scripts will be published (Zenodo/OSF) and this repo will include the commit used for analysis.

Contributing
- Open a pull request for improvements. Add unit tests for changes to `src/`.  
- Use descriptive commits and avoid changing pre-registration parameters after data collection.

Contact
- Taylor Sheppard — Sheppard Semiconductor Systems — lauren.taylor.sheppard@gmail.com

License
- MIT (see LICENSE file)

Citation
- If you use these materials in a replication attempt, please cite this repository and the original paper.
