### Core Rules

* No semantic NLP
* No embeddings
* No language models
* No learning except frozen logistic regression
* No randomness
* No interpretation

### Determinism Guarantee

Given identical input text, ScriptPulse produces:

* Identical features
* Identical effort values
* Identical alerts
* Identical output text

---

### Validation Rules (Hard Fail)

* Script must not be empty
* Must contain at least one `INT.` or `EXT.` scene header
* Speaker lines must be uppercase and ≤ 40 characters
* Dialogue must follow a speaker
* Parentheticals must be enclosed and positioned correctly

Failure raises an exception immediately.
