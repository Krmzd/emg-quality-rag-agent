# EMG signal-quality checks: how they work and what they found

This document describes how the project's signal-quality checks work
(as implemented in `src/emg_agent/quality.py`) and what they found in the
EMG Physical Action dataset (using `scripts/check_file.py` and
`scripts/find_peaks.py`). It does not give general EMG recording advice;
for that, see the published sources listed in `docs/sources.json`.

Each check runs on one EMG channel and returns a yes/no result, the
measured value, and the threshold used. The thresholds are parameters
and can be changed.

## Clipping (amplifier saturation)

**What it detects.** Samples stuck at the channel's maximum or minimum
value, as happens when the signal exceeds the recording range.

**How it is measured.** The fraction of samples within a small tolerance
(0.1% of the signal range) of the channel's maximum or minimum. A
channel is reported as clipped if this fraction is above 1%.

**Notes.** A completely flat channel is not reported as clipped. A
clipped fraction below the threshold is not reported, but can still
indicate occasional saturation.

## Flat channel

**What it detects.** A channel with almost no variation over time.

**How it is measured.** The standard deviation of the channel. A channel
is reported as flat if its standard deviation is below 1e-6. This
threshold depends on the units of the data.

**Notes.** For a flat channel, the results of the other checks (SNR,
line noise, drift) are not meaningful.

## Power-line noise (50 or 60 Hz)

**What it detects.** Power concentrated at the power-line frequency
(50 Hz or 60 Hz, set by the `line_freq` parameter).

**How it is measured.** The power spectrum is estimated with Welch's
method (1-second segments, 1 Hz resolution). The line-noise ratio is the
fraction of total power within 2 Hz of the line frequency. A channel is
reported as having line noise if the ratio is above 10%.

**Notes.** In this dataset, channels without a power-line peak still had
line-noise ratios of a few percent, so the ratio has a baseline from the
signal itself. `scripts/find_peaks.py` compares the power at the line
frequency with neighbouring frequencies, which shows sharp peaks more
directly.

## Baseline drift

**What it detects.** Power concentrated at low frequencies, as produced
by a slowly moving baseline.

**How it is measured.** The fraction of total power at or below 10 Hz,
from the Welch power spectrum. A channel is reported as having drift if
this ratio is above 20%.

## Signal-to-noise ratio (SNR)

**What it detects.** Whether the most active parts of the recording are
much stronger than the quietest parts.

**How it is measured.** The signal is mean-removed and cut into 100 ms
windows, and the RMS of each window is calculated. The 10th percentile of
window RMS values is used as the noise estimate, and the 90th percentile
as the activity estimate. SNR in dB = 20 x log10(activity RMS / noise
RMS). A channel is reported as low SNR if the SNR is below 10 dB.

**Notes.** The method assumes the recording contains both quiet and
active periods. A low value can therefore mean either a noisy recording
or a muscle that was not very active during the task. In this dataset,
arm channels had low SNR during Standing and Bowing.

## EMG Physical Action dataset: findings

- **Sampling rate: 1000 Hz.** The dataset documentation does not state
  it. With an assumed 2000 Hz, subject 2 (Standing) showed a sharp
  spectral peak at 100 Hz in all 8 channels and none at 50 Hz. With
  1000 Hz, the peak appears at exactly 50 Hz (9x to over 1,300x stronger
  than neighbouring frequencies), matching the UK power-line frequency.
  A published paper using this dataset also reports 1 kHz.
- **Line frequency: 50 Hz** (recorded at the University of Essex, UK).
- **Subject 2, Standing:** all 8 channels were reported with line noise
  (11-43% of power within 2 Hz of 50 Hz). The dataset documentation
  states that subject 2's data was not filtered.
- **Subject 1, Bowing:** line-noise ratios were 1-6% on all channels.
  The leg channels had drift ratios of 15-27% (above the 20% threshold
  on the right thigh, right hamstring and left thigh), and the right
  thigh channel had 2.5% clipped samples.
