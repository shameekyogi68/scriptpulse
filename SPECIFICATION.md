# ScriptPulse v1.3.1 - Technical Documentation
**State:** Final Frozen Implementation  
**Version:** v1.3.1-final  
**Scope:** Deterministic Structural Strain Analysis  

---

## 1. Abstract

ScriptPulse v1.3.1 is a deterministic system for analyzing **structural strain** in screenplays using **non-semantic textual features** and **rule-governed temporal accumulation**. The system operates exclusively on **surface-level structure**—such as scene boundaries, dialogue turns, sentence length, and repetition—without performing semantic interpretation, sentiment analysis, or quality judgment.

ScriptPulse is designed as a **research-grade, reproducible pipeline** with strict engine/UI separation and a frozen supervised calibration layer. Its outputs indicate **when structural strain conditions are met**, not why they occur nor whether they are desirable.

---

## 2. Design Principles

ScriptPulse is governed by the following non-negotiable principles:

1. **Determinism**: Identical input always produces identical output.
2. **Non-semantic Processing**: No meaning inference, narrative understanding, or language modeling.
3. **Structural Exclusivity**: All signals are derived from observable text structure.
4. **Fail-Fast Validation**: Malformed input halts execution immediately.
5. **Single-Pass Pipeline**: Each stage performs one function only.
6. **Frozen Learning**: Supervised learning is limited to a fixed logistic mapping.

---

## 3. System Architecture

ScriptPulse is divided into two strictly separated layers:

### 3.1 Engine Layer (Pure Logic)

Located in `scriptpulse/engine/`, this layer contains 10 deterministic modules:

1. **`validator.py`**: Structural input validation (Scene headers, Speaker format).
2. **`preprocess.py`**: Surface normalization (Whitespace, Preservation).
3. **`segment.py`**: Scene and Block segmentation (Action vs. Dialogue).
4. **`features.py`**: Raw structural feature extraction (Counts, Density, Variance).
5. **`effort.py`**: Per-scene effort computation (Linear combination).
6. **`temporal_graph.py`**: Temporal accumulation and decay (Sequential processing).
7. **`accumulate.py`**: Signal accumulation and alignment (Windowing).
8. **`calibration.py`**: Frozen logistic mapping (Probabilistic strain).
9. **`decision.py`**: Alert gating (Multi-scale agreement).
10. **`output.py`**: Template-based messaging (Descriptive alerts).

**Engine files never import UI code.**

### 3.2 Presentation Layer (UI Only)

* **`demo_app.py`** (Streamlit): Responsible only for input collection, visualization, and display.
* No logic duplication is permitted beyond visualization-only recomputation.

---

## 4. Input Model

### 4.1 Accepted Formats
* Plain text screenplay (pasted or `.txt`).

### 4.2 Structural Requirements
A valid screenplay must contain:
* At least one `INT.` or `EXT.` scene header.
* Uppercase speaker lines ≤ 40 characters.
* Parentheticals enclosed in parentheses.
* Dialogue only following speakers.

Violation of any rule halts execution via `validator.py`.

---

## 5. Structural Segmentation

ScriptPulse segments scripts into:
* **Scenes**: Determined by `INT.` / `EXT.` headers.
* **Blocks**: Typed as `ACTION` or `DIALOGUE`.

Dialogue blocks are constructed deterministically from:
* Speaker Line
* Optional Parenthetical
* Dialogue Lines

Sentence boundaries are detected by surface punctuation only (`. ! ?`).

---

## 6. Feature Extraction

All features are computed **per scene**, without cross-scene inference.

### 6.1 Basic Counts
* Lines, Words, Sentences, Action lines, Dialogue lines, Dialogue turns, Unique speakers.

### 6.2 Sentence Metrics
* Average sentence length, Maximum sentence length, Sentence length variance.

### 6.3 Dialogue Structure
* Speaker switch count, Dialogue/action ratio.

### 6.4 Visual Density Proxies
* Average action block length, Maximum continuous line run, Whitespace ratio.

### 6.5 Auditory Load Proxy
* Dialogue turns × average sentence length.

---

## 7. Normalization

Features are normalized **per script** using min–max scaling. Normalization is applied **once**, in the execution orchestrator (`run_scriptpulse.py`).

---

## 8. Effort Model

Per-scene effort is computed using a fixed linear equation with positive, frozen weights:

```
Effort = α·AvgSentenceLength + β·ActionDensity + γ·DialogueTurnCount + δ·RepetitionScore + ε·VisualDensityPenalty + ζ·AuditoryLoad
```

---

## 9. Temporal Accumulation

ScriptPulse models strain as a **temporal phenomenon**.

### 9.1 Sequential Decay
Effort accumulates with exponential decay: `A_i = Effort_i + λ·A_(i−1)`.

### 9.2 Recovery Credit
If effort drops sufficiently between scenes, a fixed recovery credit is subtracted.

### 9.3 Multi-Scale Windows
Accumulated effort is also computed over Short (3), Medium (5), and Long (9) window lengths.

---

## 10. Calibration (Supervised Layer)

A frozen logistic regression maps accumulated effort to probability: `P(strain) = σ(w·AccumEffort + b)`. This layer performs deterministic inference only.

---

## 11. Decision Logic

An alert is triggered **only if all conditions hold**:
1. Calibrated probability exceeds threshold (`0.7`).
2. Short, Medium, AND Long window thresholds are all exceeded.
3. No suppression conditions apply.

---

## 12. Output Semantics

Outputs are **descriptive, not evaluative**.
Messages strictly follow the template: *"Structural strain detected in scene {i}."*
If no alerts occur, output is silence.

---

## 13. Limitations

ScriptPulse v1.3.1:
* Does not understand story meaning.
* Does not judge quality or effectiveness.
* Does not adapt to user preference.
* Does not generalize beyond structural patterns.
* Does not explain causality.

All conclusions are **structural only**.

---

## 14. Reproducibility

* All constants are frozen.
* All rules are explicit.
* `v1.3.1-final` is immutable.

---

## 15. Conclusion

ScriptPulse v1.3.1 demonstrates that **structural strain** can be modeled deterministically using surface-level textual features and temporal accumulation, without semantic analysis or interpretive modeling. It acts as a diagnostic aid, not a creative evaluator.
