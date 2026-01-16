# How ScriptPulse Works (Simple Explanation)

This document explains how ScriptPulse works in plain, simple language.

No technical background is required.

---

## 1. What ScriptPulse Is

ScriptPulse is a tool that looks at the **structure** of a screenplay.

It does NOT:
- Understand the story
- Judge quality
- Know emotions or meaning

It ONLY looks at:
- How text is arranged
- How scenes and dialogue are structured
- How intensity builds over time

---

## 2. Big Picture

ScriptPulse works like a pipeline.

Each step does **one small job**, then passes the result to the next step.

If something is wrong early, the system stops immediately.

---

## 3. Step-by-Step Flow

### Step 1: Validation

ScriptPulse first checks:

- Is the script empty?
- Does it contain `INT.` or `EXT.`?
- Are speakers written in uppercase?
- Is dialogue placed correctly?

If any rule is broken → ScriptPulse stops.

This prevents bad input from producing bad results.

---

### Step 2: Preprocessing

Next, ScriptPulse:

- Cleans extra spaces
- Removes tabs
- Keeps line order exactly the same

Nothing is rewritten or corrected.

---

### Step 3: Segmentation

The script is split into **scenes**.

Each scene is split into blocks:
- Action
- Dialogue

ScriptPulse also detects:
- Speakers
- Parentheticals
- Sentences (using punctuation only)

No meaning is analyzed.

---

### Step 4: Feature Extraction

For each scene, ScriptPulse counts things like:

- Number of lines
- Number of dialogue turns
- Sentence length
- Amount of action vs dialogue
- How dense the text looks

These are just numbers.

---

### Step 5: Normalization

All numbers are scaled **within the same script**.

This means:
- ScriptPulse compares scenes only to other scenes in the same script
- There is no comparison to other scripts

---

### Step 6: Effort Calculation

ScriptPulse combines the numbers into a single value called **Effort**.

Effort represents:
> How demanding a scene is structurally

It is a simple weighted sum.
No complex math.
No learning here.

---

### Step 7: Temporal Accumulation

ScriptPulse looks at **how effort builds over time**:

- Effort adds up from scene to scene
- Older effort slowly fades
- Sudden drops can give recovery credit

This models attention and fatigue over time.

---

### Step 8: Multi-Window Checks

ScriptPulse checks effort over:
- Short range
- Medium range
- Long range

All three must agree before anything is flagged.

This prevents false alarms.

---

### Step 9: Calibration

A frozen logistic formula converts accumulated effort into a probability.

Important:
- The model is **not trained during use**
- It never changes
- It only maps numbers to a curve

---

### Step 10: Decision

An alert happens ONLY if:

- Probability is high enough
- Short, medium, and long windows all agree

Otherwise, ScriptPulse stays silent.

---

### Step 11: Output

If an alert happens, ScriptPulse says:

```
Structural strain detected in scene X.
```

That is all.

No explanation.
No score.
No judgment.

---

## 4. What “Structural Strain” Means

Structural strain means:

- The **format and pacing** may be demanding
- The **structure** may accumulate pressure

It does NOT mean:
- The scene is bad
- The writing is wrong
- The story fails

---

## 5. Why ScriptPulse Is Strict

ScriptPulse is strict because:

- Determinism matters
- Research needs reproducibility
- Guessing creates noise

If ScriptPulse is silent, that is valid output.

---

## 6. What ScriptPulse Is NOT

ScriptPulse is NOT:

- An AI writer
- A screenplay judge
- A creativity tool
- A semantic analyzer

It is a **structural measurement instrument**.

---

## 7. Version Guarantee

This explanation applies to:

```
ScriptPulse v1.3.1-final
```

The behavior will never change for this version.
