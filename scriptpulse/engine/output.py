from typing import List

def format_output(alerts: List[bool]) -> List[str]:
    """
    Formats alert signals into template-based output messages.
    Returns a list of strings strictly following the template:
    "Structural strain detected in scene {i}."
    """
    messages = []
    for i, is_alert in enumerate(alerts):
        if is_alert:
            messages.append(f"Structural strain detected in scene {i}.")
    return messages
