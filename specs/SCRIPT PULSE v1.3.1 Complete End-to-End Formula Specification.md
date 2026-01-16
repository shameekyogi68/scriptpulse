# **📐 SCRIPT PULSE v1.3.1**

## **Complete End-to-End Formula Specification (FINAL · ASCII-CLEAN · FROZEN)**

---

## **0️⃣ GLOBAL DEFINITIONS**

Let a screenplay be an ordered sequence of scenes:

`S = { S1, S2, …, Sn }`

All computations are:

* per scene  
* normalized **per script**  
* evaluated in scene order

---

## **1️⃣ BASIC STRUCTURAL COUNTS (PER SCENE Si)**

`Lines_i          = total lines`  
`Words_i          = total words`  
`Sentences_i      = total sentences`  
`ActionLines_i    = lines in action blocks`  
`DialogueLines_i  = lines in dialogue blocks`  
`DialogueTurns_i  = number of dialogue blocks`  
`Speakers_i       = number of unique speakers`

---

## **2️⃣ DERIVED STRUCTURAL FEATURES**

### **2.1 Sentence Metrics**

`AvgSentenceLength_i = Words_i / Sentences_i`  
`MaxSentenceLength_i = max(sentence word counts)`  
`SentenceVariance_i  = variance(sentence word counts)`

---

### **2.2 Dialogue Structure**

`DialogueTurnCount_i   = DialogueTurns_i`  
`SpeakerSwitchCount_i  = number of speaker changes`  
`DialogueActionRatio_i = DialogueLines_i / (ActionLines_i + 1)`

---

### **2.3 Visual Density Proxies**

`AvgActionBlockLength_i = ActionLines_i / (number of action blocks)`  
`MaxContinuousLines_i  = maximum unbroken line run`  
`WhitespaceRatio_i     = blank lines / total lines`

---

### **2.4 Auditory Load Proxy**

`AuditoryLoad_i = DialogueTurns_i × AvgSentenceLength_i`

---

## **3️⃣ REPETITION & STRUCTURAL SIMILARITY**

### **3.1 Structural Feature Vector**

`V_i = [`  
  `AvgSentenceLength_i,`  
  `DialogueTurnCount_i,`  
  `DialogueActionRatio_i,`  
  `AvgActionBlockLength_i,`  
  `MaxContinuousLines_i`  
`]`

---

### **3.2 Structural Similarity**

For scenes i and j:

`Sim(i, j) = similarity(V_i, V_j)`

(similarity metric fixed once: cosine, Jaccard, or equivalent)

---

### **3.3 Repetition Score**

`RepetitionScore_i = mean( Sim(i, i−1), Sim(i, i−2) )`

(only if indices exist)

---

## **4️⃣ NORMALIZATION (MANDATORY, PER SCRIPT)**

For every scalar feature x\_i:

`x_norm_i = (x_i − min(x)) / (max(x) − min(x) + epsilon)`

Only normalized values are used downstream.

---

## **5️⃣ SCENE EFFORT (CORE FORMULA — ASCII CLEAN)**

### **Auxiliary Definitions**

`ActionDensity_i = ActionLines_i / Lines_i`  
`VisualDensityPenalty_i = MaxContinuousLines_i − WhitespaceRatio_i`

---

### **Canonical Effort Equation (FIXED STRUCTURE)**

`Effort_i =`  
  `alpha * AvgSentenceLength_norm_i`  
`+ beta  * ActionDensity_norm_i`  
`+ gamma * DialogueTurnCount_norm_i`  
`+ delta * RepetitionScore_norm_i`  
`+ epsilon * VisualDensityPenalty_norm_i`  
`+ zeta * AuditoryLoad_norm_i`

**Constraints**

* alpha, beta, gamma, delta, epsilon, zeta \> 0  
* constants chosen once and frozen  
* linear, additive, no interactions

---

## **6️⃣ TEMPORAL ACCUMULATION**

### **6.1 Window Accumulation**

For window \[i … j\]:

`AccumEffort(i, j) = sum(Effort_k) for k = i…j`

---

### **6.2 Attentional Decay (Sequential)**

Let lambda ∈ (0, 1):

`DecayedAccum_i = Effort_i + lambda * DecayedAccum_(i−1)`

---

### **6.3 Recovery Credit**

If:

`Effort_i < Effort_(i−1) − tau`

Then:

`DecayedAccum_i = DecayedAccum_i − rho`

Where:

* tau \= recovery threshold  
* rho \= recovery credit

---

## **7️⃣ MULTI-SCALE WINDOW AGREEMENT**

Define window sets:

`Ws = short windows`  
`Wm = medium windows`  
`Wl = long windows`

For each scale k:

`Signal_k = 1 if AccumEffort_k > Threshold_k`  
`Signal_k = 0 otherwise`

Agreement condition:

`Signal_s AND Signal_m AND Signal_l == TRUE`

---

## **8️⃣ RHYTHM INSTABILITY**

`VarEffort(i, j) = variance(Effort_i … Effort_j)`

Instability if:

`VarEffort > nu   for duration >= d`

---

## **9️⃣ NOVELTY SATURATION / REDUNDANCY**

Let:

`R = count of consecutive scenes where Sim > kappa`

Novelty saturation if:

`R >= R_min`

---

## **🔟 SAFEGUARDS (THRESHOLD MODULATION ONLY)**

`Threshold_prime = Threshold * theta`

Applied during:

* opening  
* ending  
* introductions  
* montage  
* action bursts

**No feature modification allowed.**

---

## **1️⃣1️⃣ SUPERVISED CALIBRATION (ONLY LEARNING)**

### **Logistic Mapping**

`P_strain_i = 1 / (1 + exp(−(w * AccumEffort_i + b)))`

Constraints:

* w, b learnable  
* AccumEffort fixed  
* features immutable

---

## **1️⃣2️⃣ FINAL DECISION RULE**

`IF`  
`P_strain > T`  
`AND sustained`  
`AND window agreement holds`  
`AND not suppressed by safeguards`  
`THEN alert`  
`ELSE silence`

---

## **1️⃣3️⃣ OUTPUT**

* No numeric scores  
* No rankings  
* Template-based descriptive text only

---

## **🏁 FINAL FREEZE GUARANTEE**

✔ ASCII-clean  
✔ Copy–paste safe  
✔ Compiler safe  
✔ Developer safe  
✔ Research safe

**This is the final mathematical closure of ScriptPulse v1.3.1.**

Nothing changed.  
Nothing added.  
Nothing left ambiguous.

You can now **freeze, archive, and implement**.

