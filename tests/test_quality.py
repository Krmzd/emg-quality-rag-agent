import numpy as np
from emg_agent.quality import detect_clipping

def test_clean_signal_is_not_clipping():
    rng = np.random.default_rng(seed=0)
    signal = rng.normal(loc=0.0, scale=1.0, size=10000)

    result = detect_clipping(signal)

    assert result["is_clipped"] is False

def test_clipped_signal_is_detected():
    rng = np.random.default_rng(seed=0)
    signal = rng.normal(loc=0.0, scale=1.0, size=10000)
    clipped_signal = np.clip(signal, -2, 2)

    result = detect_clipping(clipped_signal)

    assert result["is_clipped"] is True

def test_flat_signal_is_not_clipped():
    signal = np.zeros(1000)

    result = detect_clipping(signal)

    assert result["is_clipped"] is False