# emg-quality-rag-agent
An AI agent that uses an LLM and RAG to help rehabilitation clinics and wearable tech teams with EMG data. Checks signal quality with Python and answers questions about data collection and signal quality issues with cited sources.

## Signal-quality tools

All tools live in `src/emg_agent/quality.py`. Each one checks **one
channel** (a 1-D NumPy array) and returns a dictionary with a yes/no
result, the measured value, and the threshold used, so the agent can
explain *why* a channel passed or failed.

### Tests

16 pytest tests in `tests/test_quality.py` use **synthetic signals**
where the correct answer is known (random noise, clipped noise, zeros,
constants, added 60 Hz hum, added 1 Hz drift, signals with rest and
bursts). They include edge cases, for example a flat channel, which
originally made `detect_clipping` report 100% clipping; the test found
the bug and the fix is covered by it.

## Dataset

**EMG Physical Action Data Set** (UCI Machine Learning Repository),
by Theo Theodoridis, University of Essex, UK. License: CC BY 4.0.

- 4 subjects, 10 normal and 10 aggressive actions each
- 8 surface EMG channels (Delsys), about 10,000 samples per file
- Channels: right biceps, right triceps, left biceps, left triceps,
  right thigh, right hamstring, left thigh, left hamstring
- Values are integers (raw device units); units are not documented
- Subject 2's data was **not filtered** (according to the dataset
  readme), so it is noisier than subjects 1, 3 and 4


## Project structure

```
emg-quality-rag-agent/
├── src/emg_agent/
│   ├── quality.py      # the five quality checks + check_quality
│   └── data.py         # dataset loader and dataset settings (FS, LINE_FREQ)
├── tests/
│   └── test_quality.py # pytest tests with synthetic signals
├── scripts/
│   ├── check_file.py   # run all checks on one recording
│   ├── find_peaks.py   # look for power-line peaks (used to verify fs)
│   └── README.md       # how to use the scripts
├── data/               # downloaded dataset (ignored by Git)
├── pyproject.toml      # project settings and dependencies
└── uv.lock             # exact versions of all dependencies
````
````
## Setup

Requires [uv](https://docs.astral.sh/uv/). The project uses Python 3.12.

```bash
uv sync
source .venv/bin/activate
```

## Usage

Run the tests:

```bash
pytest -v
```

Check one recording:

```bash
python scripts/check_file.py "data/raw/EMG Physical Action Data Set/sub2/Normal/txt/Standing.txt"
```
