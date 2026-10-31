import sys

from emg_agent.data import FS, LINE_FREQ, load_recording
from emg_agent.quality import check_quality

path = sys.argv[1]
emg = load_recording(path)

report = check_quality(emg, fs=FS, line_freq=LINE_FREQ)

print(f"File: {path}")
print(f"Samples: {report['n_samples']}, duration: {report['duration_s']:.2f} s")
print()

for ch in report["channels"]:
    print(
        f"ch{ch['channel']}: problems={ch['problems']}, "
        f"clipped={ch['clipping']['clipped_fraction']:.3f}, "
        f"line_noise={ch['line_noise']['line_noise_ratio']:.3f}, "
        f"drift={ch['drift']['drift_ratio']:.3f}, "
        f"snr={ch['snr']['snr_db']:.1f} dB"
    )
