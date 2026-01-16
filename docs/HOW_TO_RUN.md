# How to Run ScriptPulse v1.3.1

This document explains how to run ScriptPulse step by step.

No programming knowledge is required beyond basic Python usage.

---

## 1. Requirements

You must have:

- Python **3.11 or newer**
- Git (optional, but recommended)

Python libraries required:

- numpy
- scikit-learn
- streamlit
- matplotlib

---

## 2. Install Dependencies

From the project root directory, run:

```bash
pip install numpy scikit-learn streamlit matplotlib
```

---

## 3. Project Structure Check

Your project should look like this:

```text
scriptpulse/
├── scriptpulse/
│   └── engine/
├── run_scriptpulse.py
├── demo_app.py
├── docs/
└── README.md
```

If files are missing, the system will not run correctly.

---

## 4. Running ScriptPulse (Command Line)

ScriptPulse can be run programmatically using Python.

Example:

```python
from run_scriptpulse import run_scriptpulse

lines = open("example_script.txt").read().splitlines()
messages = run_scriptpulse(lines)

for msg in messages:
    print(msg)
```

Output will be:

* A list of alert messages
* Or an empty list if no structural strain is detected

Silence is a valid result.

---

## 5. Running ScriptPulse (Web Demo)

To run the Streamlit demo:

```bash
streamlit run demo_app.py
```

Then open the URL shown in the terminal (usually `http://localhost:8501`).

---

## 6. Using the Demo App

Inside the demo:

1. Paste your screenplay text **or** upload a `.txt` file
2. Click **“Run ScriptPulse”**
3. View:

   * Alerts (if any)
   * Per-scene effort plot
   * Accumulated effort plot

---

## 7. Common Errors

* **“No scene headers found”**
  → Your script must include `INT.` or `EXT.`

* **“Dialogue before first scene header”**
  → Dialogue must come after a scene header

* **No output**
  → This means no structural strain was detected

---

## 8. Important Notes

* ScriptPulse does **not** judge writing quality
* ScriptPulse does **not** understand story meaning
* ScriptPulse only analyzes structure

---

## 9. Version

This document applies to:

```
ScriptPulse v1.3.1 (final, frozen)
```

No behavior will change unless the version changes.
