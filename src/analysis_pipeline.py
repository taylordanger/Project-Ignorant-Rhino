"""Minimal analysis pipeline for replication study
Usage:
  python -m src.analysis_pipeline --input data/file.h5 --output results/

This script is a template and intentionally simple: load HDF5 time-series, detrend,
compute Welch PSD, detect peaks, and save summary CSV + plots.
"""
import argparse
import os
import json
import numpy as np
import h5py
import matplotlib.pyplot as plt
from scipy import signal
from pathlib import Path

from src.utils import load_h5_timeseries, detrend_series, detect_peaks_prominence


def run_analysis(input_path, output_dir, config):
    os.makedirs(output_dir, exist_ok=True)
    # load data
    ts, meta = load_h5_timeseries(input_path)
    sr = meta.get('sampling_rate', config.get('sampling_rate', 1000))

    # preprocessing
    ts_d = detrend_series(ts)

    # Welch PSD
    nperseg = config.get('welch_nperseg', 4096)
    noverlap = int(nperseg * config.get('welch_overlap', 0.5))
    f, Pxx = signal.welch(ts_d, fs=sr, nperseg=nperseg, noverlap=noverlap)

    # detect peaks
    peaks = detect_peaks_prominence(f, Pxx, prominence=config.get('peak_prominence', 1e-8))

    # save summary
    summary = {
        'input': str(input_path),
        'sampling_rate': sr,
        'nperseg': nperseg,
        'num_peaks': int(len(peaks['freqs']))
    }
    with open(Path(output_dir) / 'summary.json', 'w') as fh:
        json.dump(summary, fh, indent=2)

    # save plot
    plt.figure(figsize=(8,4))
    plt.semilogy(f, Pxx)
    plt.scatter(peaks['freqs'], peaks['powers'], marker='x', color='red')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('PSD')
    plt.title('Welch PSD and detected peaks')
    plt.tight_layout()
    plt.savefig(Path(output_dir) / 'psd.png')
    plt.close()

    # save peaks CSV
    import pandas as pd
    df = pd.DataFrame({'frequency': peaks['freqs'], 'power': peaks['powers']})
    df.to_csv(Path(output_dir) / 'peaks.csv', index=False)

    return summary


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--config', default='config/pre_registration_config.yaml')
    args = p.parse_args()

    import yaml
    cfg = {}
    if os.path.exists(args.config):
        with open(args.config) as fh:
            cfg = yaml.safe_load(fh)

    out = run_analysis(args.input, args.output, cfg)
    print('Done. Summary:', out)
