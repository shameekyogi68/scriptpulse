### Overview

ScriptPulse is divided into two strictly isolated layers:

1. Engine Layer (pure logic)
2. Presentation Layer (UI only)

No logic flows upward from UI into engine.

---

### Engine Pipeline (Fixed Order)

1. Validation
2. Preprocessing
3. Segmentation
4. Feature Extraction
5. Normalization (inline, once)
6. Effort Computation
7. Temporal Accumulation
8. Signal Alignment
9. Calibration (logistic)
10. Decision Logic
11. Output Formatting

Each stage:

* Has one responsibility
* Is deterministic
* Cannot be skipped or reordered

---

### File Responsibilities

| File              | Responsibility                  |
| ----------------- | ------------------------------- |
| validator.py      | Fail-fast structural validation |
| preprocess.py     | Surface-level normalization     |
| segment.py        | Scene & block segmentation      |
| features.py       | Raw per-scene features          |
| effort.py         | Linear effort computation       |
| temporal_graph.py | Decay & window accumulation     |
| accumulate.py     | Signal alignment                |
| calibration.py    | Frozen logistic mapping         |
| decision.py       | Alert gating                    |
| output.py         | Template-based output           |
