from typing import List, Dict
from scriptpulse.engine.validator import validate_script
from scriptpulse.engine.preprocess import preprocess_lines
from scriptpulse.engine.segment import segment_scenes
from scriptpulse.engine.features import extract_scene_features
from scriptpulse.engine.effort import compute_effort
from scriptpulse.engine.temporal_graph import build_temporal_graph
from scriptpulse.engine.accumulate import accumulate_signals
from scriptpulse.engine.calibration import calibrate_strain
from scriptpulse.engine.decision import decide_alerts
from scriptpulse.engine.output import format_output

def run_scriptpulse(lines: List[str]) -> List[str]:
    """
    Runs the full ScriptPulse v1.3.1 engine pipeline.
    """
    # 1. Validation
    validate_script(lines)

    # 2. Preprocessing
    clean_lines = preprocess_lines(lines)

    # 3. Segmentation
    scenes = segment_scenes(clean_lines)

    # 4. Feature Extraction
    features = extract_scene_features(scenes)

    # 5. Normalization (INLINE, MANDATORY)
    # Per-feature, per-script min–max normalization
    # Keys: AvgSentenceLength, ActionDensity, DialogueTurnCount, RepetitionScore, VisualDensityPenalty, AuditoryLoad
    
    # First, calculate raw values for derived metrics per scene
    raw_for_norm: List[Dict[str, float]] = []
    
    for f in features:
        # ActionDensity = ActionLines / Lines (Avoid div by zero if Lines=0, though validator prevents empty script)
        # But a scene *could* technically have 0 lines if we just have header? 
        # Validator says "Non-Empty Script", but individual scene structure?
        # A scene has at least a header (raw_lines). So lines >= 1.
        lines_count = f["Lines"]
        action_density = float(f["ActionLines"]) / lines_count if lines_count > 0 else 0.0
        
        # VisualDensityPenalty = MaxContinuousLines - WhitespaceRatio
        # Warning: MaxContinuous is int/count. WhitespaceRatio is 0-1.
        # This seems physically odd (mixing units), but prompt says "Derive: MaxContinuousLines - WhitespaceRatio".
        # We strictly follow instruction.
        vis_penalty = float(f["MaxContinuousLines"]) - float(f["WhitespaceRatio"])
        
        raw_for_norm.append({
            "AvgSentenceLength": float(f["AvgSentenceLength"]),
            "ActionDensity": action_density,
            "DialogueTurnCount": float(f["DialogueTurnCount"]),
            "RepetitionScore": 0.0, # Placeholder
            "VisualDensityPenalty": vis_penalty,
            "AuditoryLoad": float(f["AuditoryLoad"])
        })

    # Now apply Min-Max Normalization per key
    keys_to_normalize = [
        "AvgSentenceLength", 
        "ActionDensity", 
        "DialogueTurnCount", 
        "RepetitionScore", 
        "VisualDensityPenalty", 
        "AuditoryLoad"
    ]
    
    features_norm: List[Dict[str, float]] = []
    
    # Pre-calculate min/max for each key to avoid re-iterating too much
    stats = {}
    for k in keys_to_normalize:
        vals = [item[k] for item in raw_for_norm]
        stats[k] = (min(vals), max(vals))

    for item in raw_for_norm:
        norm_item = {}
        for k in keys_to_normalize:
            val = item[k]
            min_v, max_v = stats[k]
            denom = max_v - min_v + 1e-8
            # x_norm_i = (x_i - min) / denom
            norm_val = (val - min_v) / denom
            norm_item[k] = norm_val
        features_norm.append(norm_item)

    # 6. Effort Computation
    effort = compute_effort(features_norm)

    # 7. Temporal Graph
    temporal = build_temporal_graph(effort)

    # 8. Accumulation / Alignment
    signals = accumulate_signals(temporal)

    # 9. Calibration
    probs = calibrate_strain(signals["decayed"])

    # 10. Decision
    alerts = decide_alerts(probs, signals)

    # 11. Output Formatting
    messages = format_output(alerts)
    
    return messages
