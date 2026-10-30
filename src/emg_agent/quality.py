import numpy as np


def detect_clipping(signal, threshold = 0.01, tolerance = 0.001):
    """
    This functions check the signal saturation. 
    Take the EMG channel as an input ten based on the threshold and tolerance it retuns a dictionary
    Parameters:
    signal: the 1-D Numpy array, one EMG channel
    threshold: the limit for calling a channel "clipped". It's a fraction between 0 and 1. If the fraction of clipped 
    samples is above it, the channel is reported as clipped. Default 0.01, which means 1%.
    tolerance: how close a sample must be to the max or min to count as clipped.
    Its a fraction of the signal's range (max - min). Default 0.001, which means 0.1% of the range.
    Returns:
    A dictionary with:
        is_clipped: yes or no
        clipped_fraction: hoe much of a signal is clipped
        threshold: th threshold that used.
    """

    pass

    