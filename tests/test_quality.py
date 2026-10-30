import numpy as np
from emg_agent.quality import detect_clipping, detect_flat_channel, detect_line_noise

# detect_clipping function tests
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


# flat signal function tests
def test_flat_signal_is_not_clipped():
    signal = np.zeros(1000)

    result = detect_clipping(signal)

    assert result["is_clipped"] is False

def test_zero_signal_is_flat():
    signal = np.zeros(1000)

    result = detect_flat_channel(signal)

    assert result["is_flat"] is True

def test_constant_signal_is_flat():
    signal = np.full(1000, 0.5)

    result = detect_flat_channel(signal)

    assert result["is_flat"] is True

def test_normal_signal_is_not_flat():
    rng = np.random.default_rng(seed=0)
    signal = rng.normal(loc=0.0, scale=1.0, size=10000)
    
    result = detect_flat_channel(signal)
 
    assert result["is_flat"] is False

# test 60Hz noise function
def test_signal_with_60Hz_has_line_noise():
    fs=2000
    rng = np.random.default_rng(seed=0)
    signal = rng.normal(loc=0.0, scale=1.0, size=10000)
    t = np.arange(10000) / fs
    hum = 2.0 * np.sin(2 * np.pi * 60 * t)
    noisy_signal = signal + hum

    result = detect_line_noise(noisy_signal, fs=fs)

    assert result["has_line_noise"] is True
    

def test_clean_signal_has_no_line_noise():
    fs = 2000
    rng = np.random.default_rng(seed=0)
    signal = rng.normal(loc=0.0, scale=1.0, size=10000)

    result = detect_line_noise(signal, fs=fs)

    assert result["has_line_noise"] is False


def test_flat_signal_has_no_line_noise():
    fs = 2000
    signal = np.zeros(10000)

    result = detect_line_noise(signal, fs=fs)

    assert result["has_line_noise"] is False