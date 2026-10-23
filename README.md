# robotics-extraction

Deterministic, rule-based extraction of robotics engineering facts from drawings,
datasheets, safety schematics and I/O lists - no LLM. Mirrors Neurallel's EE-SME
extraction pattern (one SME app repo, one extraction repo per field), connected to
[`robotics-sme`](../robotics-sme) only through a small versioned JSON contract, never
shared code: `extract(path) -> {entries, unresolved, source, extractor_version}`.

See `robotics-sme`'s `docs/robotics-plan.md` §13 for the full design and policy this
repo implements (the zero-assumption policy, the data dictionary, the file-routing
table). This repo has no dependency on `robotics-sme` and is fully testable on its own.

## Status

Readers are **correct in shape, not tuned**: they were written against hand-built
synthetic fixtures (`tests/fixtures/`), not real vendor files. A real robot datasheet,
cell layout, safety schematic or I/O export may not match these stub readers' column
names or layer conventions at all - that rewrite (plan P8) is blocked until a real
sample of each file type is available, by design (plan §13.9).

## Setup

```powershell
uv venv --python 3.12 .venv
uv pip install --python .venv\Scripts\python.exe -e ".[dev]"
.venv\Scripts\python.exe -m pytest -q
```

## Usage

```python
import robotics_extraction as rx
record = rx.extract("robot_r2000a_datasheet.pdf")
# {"entries": [...], "unresolved": [...], "source": {...}, "extractor_version": "0.1.0"}
```
