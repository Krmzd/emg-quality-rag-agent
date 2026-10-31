import numpy as np
# Settings for the EMG Physical Action dataset (UCI).
# Sampling rate: not stated in the dataset readme; 2000 Hz is an
# assumption to be verified. Line frequency: recorded in the UK (50 Hz).
FS = 1000
LINE_FREQ = 50 

def load_recording(path):
    """
    Load one recording from the EMG Physical Action dataset.

    Parameters:
        path: path to a .txt file from the dataset (for example
            ".../sub1/Normal/txt/Bowing.txt").

    Returns:
        A 2-D NumPy array with shape (n_samples, 8): one row per sample,
        one column per channel (ch1 to ch8).
    """
    return np.loadtxt(path)