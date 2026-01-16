from typing import List

# MANDATORY CONSTANTS (FROZEN)
LAMBDA = 0.9
TAU    = 0.15
RHO    = 0.1

WINDOW_SHORT  = 3
WINDOW_MEDIUM = 5
WINDOW_LONG   = 9

def build_temporal_graph(effort: List[float]) -> dict:
    """
    Computes decayed and windowed accumulated effort signals.
    """
    if not effort:
        return {
            "decayed": [],
            "window_short": [],
            "window_medium": [],
            "window_long": []
        }

    # 1. Sequential Decay Accumulation
    decayed_series = []
    
    # Init first element
    # DecayedAccum_0 = Effort_0
    decayed_series.append(effort[0])

    for i in range(1, len(effort)):
        eff_current = effort[i]
        eff_prev = effort[i-1]
        acc_prev = decayed_series[i-1]

        # Basic Decay Formula
        # DecayedAccum_i = Effort_i + LAMBDA * DecayedAccum_(i-1)
        acc_current = eff_current + (LAMBDA * acc_prev)

        # Recovery Logic
        # If Effort_i < Effort_(i-1) - TAU
        if eff_current < (eff_prev - TAU):
            # Then DecayedAccum_i = DecayedAccum_i - RHO
            acc_current = acc_current - RHO

        decayed_series.append(acc_current)

    # 2. Window Accumulation
    def compute_windowed_sums(data: List[float], w: int) -> List[float]:
        # Only valid logic: sum(Effort[i-w+1 : i+1])
        # Indices i start from w-1 to len-1
        if w > len(data):
            return []
        
        results = []
        # Precompute initial sum to optimize sliding window, or just sum slice for clarity/correctness
        # Given "Deterministic" and potentially small script, sum slice is safest and clearest.
        # i represents end index (inclusive)
        for i in range(w - 1, len(data)):
            # slice from i - w + 1 to i + 1 (exclusive) contains w elements
            window_slice = data[i - w + 1 : i + 1]
            results.append(sum(window_slice))
        return results

    return {
        "decayed": decayed_series,
        "window_short": compute_windowed_sums(effort, WINDOW_SHORT),
        "window_medium": compute_windowed_sums(effort, WINDOW_MEDIUM),
        "window_long": compute_windowed_sums(effort, WINDOW_LONG)
    }
