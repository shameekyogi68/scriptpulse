### Feature Normalization

Per script:

```
x_norm = (x − min(x)) / (max(x) − min(x) + ε)
```

ε = 1e-8

---

### Effort Equation (Fixed)

```
Effort =
  α·AvgSentenceLength
+ β·ActionDensity
+ γ·DialogueTurnCount
+ δ·RepetitionScore
+ ε·VisualDensityPenalty
+ ζ·AuditoryLoad
```

All weights:

```
α = β = γ = δ = ε = ζ = 1.0
```

---

### Temporal Accumulation

**Sequential decay:**

```
A_i = Effort_i + λ·A_(i−1)
```

λ = 0.9

**Recovery credit:**

```
If Effort_i < Effort_(i−1) − τ:
    A_i = A_i − ρ
```

τ = 0.15
ρ = 0.1

---

### Multi-Scale Windows

| Window | Size |
| ------ | ---- |
| Short  | 3    |
| Medium | 5    |
| Long   | 9    |

Agreement requires **all three** to exceed thresholds.
