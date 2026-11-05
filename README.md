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

## Answers with citations (RAG)

Ask a question in plain language. The system finds the most relevant
pieces of the project's documents and asks an LLM to answer **only from
those pieces**, citing each one by number.

```
question → search (Chroma) → 5 closest chunks → gpt-5-mini → answer with [1], [2] + source list
```

## Evaluation (baseline)

A 30-question test set (`eval/questions.json`): 25 questions answerable
from the documents, each with the expected source and a short evidence
phrase, and 5 questions the documents cannot answer.

| Metric | Result |
|---|---|
| Retrieval hit rate@5 (a top-5 chunk contains the evidence phrase) | 84% (21/25) |
| Answers judged correct (expert review) | 84% (21/25); 92% correct or partial |
| Refusals on unanswerable questions | 100% (5/5) |
| Invalid citation numbers | 0 in the final run |

Both wrong answers were refusals caused by retrieval misses: the model
said the sources did not answer the question instead of guessing.

Run it:

```bash
python scripts/eval_retrieval.py
python scripts/eval_answer.py
```

- **Documents:** the dataset readme, the CEDE-Check reporting checklist,
  and `docs/quality_tools.md` (listed in `docs/sources.json`).
- **Chunking:** PDF by page, Markdown by section, then whole sentences
  grouped into chunks of up to 1,000 characters with one sentence of overlap.
- **Embeddings and answers:** Azure OpenAI (`text-embedding-3-small`, `gpt-5-mini`).
- **Rules for the model:** answer only from the sources, cite every
  statement, say so when the sources don't answer, never invent numbers,
  never give medical advice.

Example:

```bash
python scripts/ask.py "What should be reported about electrode placement?"
```

## Dataset

**EMG Physical Action Data Set** (UCI Machine Learning Repository),
by Theo Theodoridis, University of Essex, UK. License: CC BY 4.0.

**Citation:** Theodoridis, T. (2011). EMG Physical Action Data Set
[Dataset]. UCI Machine Learning Repository.
https://doi.org/10.24432/C53W49

- 4 subjects, 10 normal and 10 aggressive actions each
- 8 surface EMG channels (Delsys), about 10,000 samples per file
- Channels: right biceps, right triceps, left biceps, left triceps,
  right thigh, right hamstring, left thigh, left hamstring
- Values are integers (raw device units); units are not documented
- Subject 2's data was **not filtered** (according to the dataset
  readme), so it is noisier than subjects 1, 3 and 4

  ## Document sources

- Besomi et al. (2024). Consensus for experimental design in
  electromyography (CEDE) project: Checklist for reporting and critically
  appraising studies using EMG (CEDE-Check). *Journal of Electromyography
  and Kinesiology*. https://doi.org/10.1016/j.jelekin.2024.102874
  (License: CC BY 4.0). Text is split into chunks for search.


## Project structure
```
emg-quality-rag-agent/
├── src/emg_agent/
│   ├── quality.py        # the five quality checks + check_quality
│   ├── data.py           # EMG dataset loader and settings (FS, LINE_FREQ)
│   ├── documents.py      # load documents and cut them into chunks
│   ├── llm.py            # connection to Azure OpenAI, embeddings
│   ├── vector_store.py   # store chunks in Chroma, search them
│   └── answer.py         # answer a question with citations
├── scripts/
│   ├── check_file.py     # run all quality checks on one recording
│   ├── build_index.py    # build the search index
│   ├── search.py         # show the 5 closest chunks for a question
│   └── ask.py            # answer a question with citations
├── tests/                # pytest tests (no Azure calls needed)
├── docs/
│   ├── quality_tools.md  # how the quality checks work
│   └── sources.json      # catalog of documents used for search
├── data/                 # dataset, documents, Chroma index (ignored by Git)
├── pyproject.toml
└── uv.lock
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
