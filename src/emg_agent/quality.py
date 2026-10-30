import numpy as np


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
