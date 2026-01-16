Below is the **FINAL, ACCURATE, NO-CONFUSION, DEVELOPER-READY HANDOFF**.

This is written so a developer can **implement end-to-end without asking questions**.  
It is **locked**, **unambiguous**, and **fully aligned** with ScriptPulse v1.3.1, NLP domain, and supervised learning requirements.

You can **send this as-is** to developers.

---

# **🎬 SCRIPTPULSE v1.3.1 — FINAL IMPLEMENTATION STACK**

### **DEVELOPER HANDOFF (LOCKED)**

**Purpose:** Research-grade, deterministic system  
**Domain:** Structural NLP \+ Supervised Learning  
**Status:** Implementation-ready  
**Interpretation:** ❌ NOT ALLOWED

---

## **1️⃣ CORE LANGUAGE (MANDATORY)**

Python 3.11+

All logic **must** be written in Python.

No other language is permitted for the engine.

---

## **2️⃣ CORE ENGINE — STRUCTURAL NLP \+ NUMERICAL PROCESSING**

### **Allowed Standard Libraries**

re  
string  
dataclasses  
typing  
math  
logging

### **Allowed External Libraries**

numpy

### **Engine Responsibilities (MANDATORY)**

The engine **must implement exactly**:

* Structural text preprocessing  
* Screenplay validation (halt on malformed input)  
* Rule-based scene segmentation (`INT.` / `EXT.`)  
* Dialogue vs action block detection  
* Uppercase speaker detection  
* Parenthetical detection  
* Sentence boundary detection (surface only)  
* Structural n-grams (block-type / surface-form)  
* Jaccard similarity (surface-form only)  
* Feature extraction (as per spec)  
* Feature normalization (within-script only)  
* Deterministic effort computation  
* Temporal accumulation & decay  
* Recovery, redundancy, transition costs  
* Reset & suppression logic  
* Multi-scale window agreement  
* Deterministic diagnostics

🚫 **FORBIDDEN in engine**

* Semantic NLP  
* Meaning inference  
* Embeddings  
* Sentiment analysis  
* Grammar parsing  
* Auto-correction  
* Guessing / fallback logic

---

## **3️⃣ SUPERVISED LEARNING MODULE (STRICTLY LIMITED)**

### **Library (ONLY)**

scikit-learn

### **Model (ONLY)**

sklearn.linear\_model.LogisticRegression

### **Purpose**

* Decide **WHEN to alert**  
* NOT what to analyze

### **Rules (MANDATORY)**

* Input: accumulated numerical effort signals only  
* Training: offline only  
* Weights: frozen per version  
* No feature learning  
* No personalization  
* No success prediction  
* Deterministic inference only

Formula implemented **exactly**:

P(strain) \= σ(w · AccumEffort \+ b)

---

## **4️⃣ INPUT HANDLING**

### **Plain Text**

* Accepted directly

### **PDF**

pdfminer.six

### **Rules**

* PDF → text only  
* Then structural validation  
* HALT if required elements missing  
* No auto-fix  
* No guessing  
* No fallback parsing

---

## **5️⃣ DEMO / WEBSITE LAYER (PRESENTATION ONLY)**

Streamlit

### **Responsibilities**

* Input upload / paste  
* Display scene breakdown  
* Display extracted features  
* Display effort & accumulation plots  
* Display alerts  
* Display explicit limitations

🚫 **FORBIDDEN**

* Business logic  
* NLP logic  
* ML logic  
* Numerical computation

---

## **6️⃣ VISUALIZATION (MANDATORY)**

Matplotlib

Used for:

* Per-scene effort visualization  
* Accumulated strain curve  
* Multi-window agreement  
* Alert spans

---

## **7️⃣ STORAGE (MINIMAL)**

Local files (JSON / CSV / TXT)

Used for:

* Sample scripts  
* Calibration datasets  
* Frozen model weights  
* Experiment outputs

Optional (later):

SQLite

---

## **8️⃣ REQUIRED PROJECT STRUCTURE**

scriptpulse/  
├── engine/                     \# PURE LOGIC ONLY  
│   ├── validator.py  
│   ├── preprocess.py  
│   ├── segment.py  
│   ├── features.py  
│   ├── effort.py  
│   ├── temporal\_graph.py  
│   ├── accumulate.py  
│   ├── calibration.py          \# logistic regression only  
│   ├── decision.py  
│   └── output.py  
│  
├── demo\_app.py                 \# Streamlit UI ONLY  
├── sample\_scripts/  
├── data/  
└── README.md

### **🔑 HARD RULE**

Files inside `engine/` **MUST NEVER** import Streamlit, UI, or web code.

---

## **9️⃣ EXPLICITLY FORBIDDEN TECHNOLOGIES**

🚫 LLMs / Transformers  
🚫 spaCy or semantic NLP libraries  
🚫 LangChain  
🚫 Deep learning frameworks  
🚫 MERN / MEAN for core logic  
🚫 Serverless execution  
🚫 Auto-correction systems  
🚫 Scoring, ranking, or grading scenes

Use of any above makes the system **INCORRECT**.

---

## **1️⃣0️⃣ NON-NEGOTIABLE SYSTEM RULES**

* Determinism is mandatory  
* Silence is a valid output  
* Alerts ≠ criticism  
* Effort is relative within a script  
* Structural strain ≠ story quality  
* No interpretation beyond spec

---

## **🏁 FINAL STATUS**

**This stack is complete, exact, and ready for implementation.**  
**No additions. No substitutions. No interpretation.**

This is the **final developer handoff**.

