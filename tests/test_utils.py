import sys
import os
import numpy as np
import h5py
from scipy import signal

# ensure project root is on sys.path so `src` is importable during tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import load_h5_timeseries, detrend_series, detect_peaks_prominence


def test_load_and_detect(tmp_path):
    # create synthetic timeseries: 50 Hz sine + noise
    sr = 1000.0
    t = np.arange(0, 10.0, 1.0/sr)
    freq = 50.0
    x = 0.5 * np.sin(2 * np.pi * freq * t) + 0.01 * np.random.randn(t.size)

    p = tmp_path / "test1.h5"
    with h5py.File(p, 'w') as f:
        d = f.create_dataset('timeseries', data=x)
        f.attrs['sampling_rate'] = sr

    data, meta = load_h5_timeseries(str(p))
    assert data.shape[0] == x.shape[0]
    assert abs(meta['sampling_rate'] - sr) < 1e-6

    # detrend should preserve shape
    xd = detrend_series(data)
    assert xd.shape == data.shape

    # compute PSD and detect peak near 50 Hz
    f, Pxx = signal.welch(xd, fs=sr, nperseg=2048)
    peaks = detect_peaks_prominence(f, Pxx, prominence=1e-6)
    # there should be at least one detected peak near 50 Hz
    freqs = np.array(peaks['freqs'])
    assert np.any(np.isclose(freqs, freq, atol=1.0))
