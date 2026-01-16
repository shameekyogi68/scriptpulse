from typing import Dict, List, Union, Optional

def accumulate_signals(temporal: Dict[str, List[float]]) -> Dict[str, List[Optional[float]]]:
    """
    Aligns and returns accumulated effort signals.
    Prepends None to windowed signals to align indices with the decayed signal.
    """
    # Validate keys
    required_keys = ["decayed", "window_short", "window_medium", "window_long"]
    for k in required_keys:
        if k not in temporal:
            raise KeyError(f"Missing required key: {k}")

    decayed = temporal["decayed"]
    target_len = len(decayed)

    # Pass-through decayed
    # Copy to ensure no mutation if caller modifies return
    aligned_decayed: List[Optional[float]] = list(decayed) 

    # Align windows
    def align_window(window_raw: List[float]) -> List[Optional[float]]:
        # Calculate padding
        # logic: window list contains values for indices [pad_len ... target_len-1]
        # So pad_len = target_len - len(window_raw)
        pad_len = target_len - len(window_raw)
        
        if pad_len < 0:
            # Should not happen given temporal_graph logic, but if input is malformed:
            raise ValueError("Window signal longer than decayed signal")
        
        padding = [None] * pad_len
        return padding + list(window_raw)

    return {
        "decayed": aligned_decayed,
        "window_short": align_window(temporal["window_short"]),
        "window_medium": align_window(temporal["window_medium"]),
        "window_long": align_window(temporal["window_long"])
    }
