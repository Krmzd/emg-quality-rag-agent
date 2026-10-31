import numpy as np
from emg_agent.quality import detect_clipping, detect_flat_channel, detect_line_noise, detect_baseline_drift, estimate_snr, check_quality

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


# baseline drift tests
def test_signal_with_drift_is_detected():
    fs = 2000
    rng = np.random.default_rng(seed=0)
    signal = rng.normal(loc=0.0, scale=1.0, size=10000)
    t = np.arange(10000) / fs

    drift = 3.0 * np.sin(2 * np.pi * 1 * t)
    drifting_signal = signal + drift

    result = detect_baseline_drift(drifting_signal, fs=fs)

    assert result["has_drift"] is True


def test_clean_signal_has_no_drift():
    fs = 2000
    rng = np.random.default_rng(seed=0)
    signal = rng.normal(loc=0.0, scale=1.0, size=10000)

    result = detect_baseline_drift(signal, fs=fs)

    assert result["has_drift"] is False


def test_flat_signal_has_no_drift():
    fs = 2000
    signal = np.zeros(10000)

    result = detect_baseline_drift(signal, fs=fs)

    assert result["has_drift"] is False


 # estimate_snr tests
def test_signal_with_bursts_has_good_snr():
    fs = 2000
    rng = np.random.default_rng(seed=0)
    signal = rng.normal(loc = 0.0, scale = 0.05, size = 10000)
    signal[2000:4000] += rng.normal(loc=0.0, scale=1.0, size=2000)
    signal[6000:8000] += rng.normal(loc=0.0, scale=1.0, size=2000)

    result = estimate_snr(signal, fs=fs)

    assert result["has_low_snr"] is False


def test_noise_only_signal_has_low_snr():
    fs = 2000
    rng = np.random.default_rng(seed=0)
    signal = rng.normal(loc=0.0, scale=1.0, size=10000)

    result = estimate_snr(signal, fs=fs)

    assert result["has_low_snr"] is True


def test_flat_signal_has_low_snr():
    fs = 2000
    signal = np.zeros(10000)

    result = estimate_snr(signal, fs=fs)

    assert result["has_low_snr"] is True


def test_check_quality_finds_problem_channel():
    fs = 2000
    rng = np.random.default_rng(seed=0)

    good_channel = rng.normal(loc=0.0, scale=0.05, size=10000)
    good_channel[2000:4000] += rng.normal(loc=0.0, scale=1.0, size=2000)
    good_channel[6000:8000] += rng.normal(loc=0.0, scale=1.0, size=2000)

    flat_channel = np.zeros(10000)

    emg = np.column_stack([good_channel, flat_channel])

    report = check_quality(emg, fs=fs)

    assert report["n_samples"] == 10000
    assert report["duration_s"] == 5.0
    assert len(report["channels"]) == 2

    assert report["channels"][0]["problems"] == []
    assert "flat" in report["channels"][1]["problems"]