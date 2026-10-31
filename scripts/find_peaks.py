import sys

import numpy as np
from scipy.signal import welch

from emg_agent.data import FS, load_recording

path = sys.argv[1]
channel = int(sys.argv[2])

emg = load_recording(path)
signal = emg[:, channel]

freqs, psd = welch(signal, fs=FS, nperseg=int(FS))
print(f"Channel {channel}, assuming fs = {FS} Hz")
print("Power at each candidate frequency compared with its neighbours:")

for f in [25, 50, 100, 150]:
    at_f = psd[freqs == f][0]
    neighbours = (np.abs(freqs - f) >= 3) & (np.abs(freqs - f) <= 8)
    neighbour_power = np.median(psd[neighbours])
    ratio = at_f / neighbour_power
    print(f"  {f:4d} Hz: {ratio:5.1f} times its neighbours")
