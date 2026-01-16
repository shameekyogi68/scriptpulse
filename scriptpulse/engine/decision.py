from typing import List, Dict, Optional

# MANDATORY DECISION CONSTANTS (FROZEN)
PROB_THRESHOLD = 0.7

THRESHOLD_SHORT  = 3.0
THRESHOLD_MEDIUM = 5.0
THRESHOLD_LONG   = 9.0

def decide_alerts(
    probs: List[float],
    signals: Dict[str, List[Optional[float]]]
) -> List[bool]:
    """
    Applies final decision rules and returns alert flags.
    Checks probability threshold and mandatory multi-scale window agreement.
    """
    
    # Input validation (basic integrity check)
    if len(probs) != len(signals["decayed"]):
        # Assuming all signals are aligned by accumulate module, but let's trust caller or fail
        # Strictly speaking accumulate guarantees alignment. 
        # But probs comes from calibration.
        # If lengths mismatch, it's a pipeline error.
        raise ValueError("Length mismatch between probabilities and signals")

    alerts = []
    
    # Extract aligned window signals
    w_short = signals["window_short"]
    w_medium = signals["window_medium"]
    w_long  = signals["window_long"]
    
    for i in range(len(probs)):
        p = probs[i]
        
        # 1. Probability Check
        prob_pass = (p > PROB_THRESHOLD)
        
        # 2. Multi-Scale Window Agreement
        # Agreement holds ONLY IF all 3 signals exist (not None) AND exceed their thresholds
        
        val_s = w_short[i]
        val_m = w_medium[i]
        val_l = w_long[i]
        
        signal_s = (val_s is not None) and (val_s > THRESHOLD_SHORT)
        signal_m = (val_m is not None) and (val_m > THRESHOLD_MEDIUM)
        signal_l = (val_l is not None) and (val_l > THRESHOLD_LONG)
        
        agreement = signal_s and signal_m and signal_l
        
        # Final Rule (AND)
        final_alert = prob_pass and agreement
        
        alerts.append(final_alert)
        
    return alerts
