import numpy as np
from scipy.signal import welch

def detect_clipping(signal, threshold = 0.01, tolerance = 0.001):
    """
    This functions check the signal saturation. 
    Take the EMG channel as an input then based on the threshold and tolerance it retuns a dictionary
    Parameters:
    signal: the 1-D Numpy array, one EMG channel
    threshold: the limit for calling a channel "clipped". It's a fraction between 0 and 1. If the fraction of clipped 
    samples is above it, the channel is reported as clipped. Default 0.01, which means 1%.
    tolerance: how close a sample must be to the max or min to count as clipped.
    Its a fraction of the signal's range (max - min). Default 0.001, which means 0.1% of the range.
    Returns:
    A dictionary with:
        is_clipped: yes or no
        clipped_fraction: how much of a signal is clipped
        threshold: the threshold that used.
    """

    min_signal = np.min(signal)
    max_signal = np.max(signal)
    signal_range =  max_signal - min_signal
    if signal_range == 0:
        return {
            "is_clipped": False,
            "clipped_fraction": 0.0,
            "threshold": threshold,
        }
    tolerance_distance = tolerance * signal_range
    near_max = signal >= max_signal - tolerance_distance
    near_min = signal <= min_signal + tolerance_distance
    clipped = near_max | near_min
    clipped_fraction = np.mean(clipped)
    is_clipped = clipped_fraction > threshold 

    return {
        "is_clipped": bool(is_clipped),
        "clipped_fraction": float(clipped_fraction),
        "threshold": threshold,
    }


def detect_flat_channel(signal, std_threshold = 1e-6):
    """
        This functions check the signal flat. 
        Take the EMG channel as an input then based on the threshold and standard deviation it retuns a dictionary
        Parameters:
        signal: the 1-D Numpy array, one EMG channel
        threshold: the limit for calling a channel "flat". 
        standard deviation: 
        Returns:
        A dictionary with:
            is_flat: yes or no
            std:the channel's standard deviation
            threshold: the threshold that used.
        """
    signal_std = np.std(signal)
    is_flat = signal_std < std_threshold

    return {
        "is_flat": bool(is_flat),
        "std": float(signal_std),
        "std_threshold": std_threshold,

    }

def detect_line_noise(signal, fs, line_freq = 60, threshold = 0.1):
    """
    Detect power-line noise (for example 60 Hz) in one EMG channel.

    Parameters:
        signal: one EMG channel as a 1-D NumPy array.
        fs: sampling rate in Hz (samples per second), for example 2000.
        line_freq: power-line frequency in Hz. Default 60 (North America);
            use 50 for Europe and many other countries.
        threshold: the limit for reporting line noise. A fraction between
            0 and 1. If the fraction of the signal's power within 2 Hz of
            line_freq is above it, line noise is reported. Default 0.1 (10%).

    Returns:
        A dictionary with:
            has_line_noise: True if the line-noise ratio is above the threshold.
            line_noise_ratio: fraction of total power near line_freq (0 to 1).
            threshold: the threshold that was used.
    """
    # calculate the spectrum: turns the signal into a table of requency -> power. freqs holds frquencies, psd hold the power at each one.
    freqs, psd = welch(signal, fs=fs, nperseg = min(len(signal), int(fs)))

    total_power = np.sum(psd)
    if total_power == 0:
        return {
            "has_line_noise": False,
            "line_noise_ratio": 0.0,
            "threshold": threshold,
            }

    in_band = (freqs >= line_freq - 2) & (freqs <= line_freq + 2)

    band_power = np.sum(psd[in_band])

    line_noise_ratio = band_power / total_power

    has_line_noise = line_noise_ratio > threshold

    return {
        "has_line_noise": bool(has_line_noise),
        "line_noise_ratio": float(line_noise_ratio),
        "threshold": threshold,
    }

def detect_baseline_drift(signal, fs, cutoff=10, threshold=0.2):
    """
    Detect baseline drift (slow low-frequency movement) in one EMG channel.

    Parameters:
        signal: one EMG channel as a 1-D NumPy array.
        fs: sampling rate in Hz (samples per second), for example 2000.
        cutoff: frequencies at or below this value (in Hz) count as drift.
            Default 10 Hz.
        threshold: the limit for reporting drift. A fraction between 0 and 1.
            If the fraction of the signal's power at or below the cutoff is
            above it, drift is reported. Default 0.2 (20%).

    Returns:
        A dictionary with:
            has_drift: True if the drift ratio is above the threshold.
            drift_ratio: fraction of total power at or below the cutoff (0 to 1).
            threshold: the threshold that was used.
    """
    freqs, psd = welch(signal, fs=fs, nperseg=min(len(signal), int(fs)))

    total_power = np.sum(psd)
    if total_power == 0:
        return {
            "has_drift": False,
            "drift_ratio": 0.0,
            "threshold": threshold,
        }

    low_band = freqs <= cutoff

    low_power = np.sum(psd[low_band])

    drift_ratio = low_power / total_power

    has_drift = drift_ratio > threshold

    return {
        "has_drift": bool(has_drift),
        "drift_ratio": float(drift_ratio),
        "threshold": threshold,
    }

def estimate_snr(signal, fs, window_ms=100, threshold_db=10):
    """
    Estimate the signal-to-noise ratio (SNR) of one EMG channel.

    The signal is cut into short windows and the RMS of each window is
    calculated. The quietest windows (10th percentile) estimate the noise,
    and the most active windows (90th percentile) estimate the signal.

    Parameters:
        signal: one EMG channel as a 1-D NumPy array.
        fs: sampling rate in Hz (samples per second), for example 2000.
        window_ms: window length in milliseconds. Default 100 ms.
        threshold_db: SNR below this value (in dB) is reported as low.
            Default 10 dB.

    Returns:
        A dictionary with:
            has_low_snr: True if the SNR is below the threshold.
            snr_db: the estimated SNR in decibels.
            threshold_db: the threshold that was used.
    """
    centered = signal - np.mean(signal)
    window_len = int(window_ms / 1000 * fs)
    n_windows = len(centered) // window_len
    windows = centered[: n_windows * window_len].reshape(n_windows, window_len)
    window_rms = np.sqrt(np.mean(windows**2, axis = 1))
    noise_rms = np.percentile(window_rms, 10)
    signal_rms = np.percentile(window_rms, 90)

    if signal_rms == 0:
        return {
            "has_low_snr": True,
            "snr_db": 0.0,
            "threshold_db": threshold_db,
        }

    snr_db = 20 * np.log10(signal_rms / max(noise_rms, 1e-12))

    has_low_snr = snr_db < threshold_db

    return {
        "has_low_snr": bool(has_low_snr),
        "snr_db": float(snr_db),
        "threshold_db": threshold_db,
    }