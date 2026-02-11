Template analysis steps

1. Place raw HDF5 files in `data/` (do NOT commit data). Each file should contain a dataset `timeseries` and set attribute `sampling_rate` if available.

2. Run the pipeline on one file to confirm operation:

```bash
python -m src.analysis_pipeline --input data/example_raw.h5 --output results/run01
```

3. Inspect `results/run01/psd.png` and `results/run01/peaks.csv` for automated outputs.

4. To batch-process multiple files, write a small shell script that enumerates `data/*.h5` and calls the pipeline.

5. Use `notebooks/` for deeper exploratory analysis and figures for the replication report.
