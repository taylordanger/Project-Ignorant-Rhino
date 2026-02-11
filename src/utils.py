import numpy as np
import h5py
from scipy import signal


def load_h5_timeseries(path):
    """Expect dataset 'timeseries' and optional attrs 'sampling_rate'. Return (data, meta)."""
    meta = {}
    with h5py.File(path, 'r') as f:
        if 'timeseries' in f:
            data = f['timeseries'][:]
        else:
            # try first dataset
            name = list(f.keys())[0]
            data = f[name][:]
        if 'sampling_rate' in f.attrs:
            meta['sampling_rate'] = float(f.attrs['sampling_rate'])
        elif 'sampling_rate' in f.get('timeseries', {}).attrs:
            meta['sampling_rate'] = float(f['timeseries'].attrs['sampling_rate'])
    return data.astype(float), meta


def detrend_series(x):
    return signal.detrend(x, type='linear')


def detect_peaks_prominence(freqs, psd, prominence=1e-8):
    # convert to linear power
    from scipy.signal import find_peaks
    # simple peak find on PSD (log transform is common)
    powers = psd
    peaks_idx, props = find_peaks(powers, prominence=prominence)
    freqs_peaks = freqs[peaks_idx]
    powers_peaks = powers[peaks_idx]
    return {'freqs': freqs_peaks.tolist(), 'powers': powers_peaks.tolist(), 'props': props}
