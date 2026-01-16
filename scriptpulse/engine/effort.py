from typing import List, Dict

# MANDATORY CONSTANTS (FROZEN)
ALPHA   = 1.0
BETA    = 1.0
GAMMA   = 1.0
DELTA   = 1.0
EPSILON = 1.0
ZETA    = 1.0

def compute_effort(features_norm: List[Dict[str, float]]) -> List[float]:
    """
    Computes per-scene Effort values using the fixed linear formula.
    Requires normalized input features.
    """
    effort_values = []
    
    for scene_features in features_norm:
        # Strict key access. Missing keys raise KeyError.
        avg_sentence_len = scene_features["AvgSentenceLength"]
        action_density = scene_features["ActionDensity"]
        dialogue_turns = scene_features["DialogueTurnCount"]
        repetition_score = scene_features["RepetitionScore"]
        visual_density = scene_features["VisualDensityPenalty"]
        auditory_load = scene_features["AuditoryLoad"]
        
        # Fixed Canonical Formula
        effort = (
            ALPHA   * avg_sentence_len +
            BETA    * action_density +
            GAMMA   * dialogue_turns +
            DELTA   * repetition_score +
            EPSILON * visual_density +
            ZETA    * auditory_load
        )
        
        effort_values.append(effort)
        
    return effort_values
