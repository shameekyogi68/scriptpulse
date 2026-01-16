### Output Type

```python
List[str]
```

---

### Output Rules

* One message per alert
* Scene index is zero-based
* No numeric values
* No explanations
* No ranking

Example:

```
Structural strain detected in scene 4.
```

If no alerts:

```
[]
```

Silence is valid output.
