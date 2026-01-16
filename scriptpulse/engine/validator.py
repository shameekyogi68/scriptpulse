import re
from typing import List

def validate_script(lines: List[str]) -> None:
    """
    Raises ValueError if validation fails.
    Returns None if script is valid.
    """
    # Rule 1: Non-Empty Script
    if not any(line.strip() for line in lines):
        raise ValueError("Empty script")

    scene_header_regex = re.compile(r'^(INT\.|EXT\.)')
    has_scene_header = False
    headers_found = 0
    last_line_was_speaker = False

    for line in lines:
        # Check scene header
        if scene_header_regex.match(line):
            has_scene_header = True
            headers_found += 1
            last_line_was_speaker = False
            continue

        # Check speaker line (Dialogue candidate)
        # Defined as fully uppercase line
        if line.isupper():
            # Rule 3: Scene Header Ordering
            if not has_scene_header:
                raise ValueError("Dialogue before first scene header")
            
            # Rule 4: Speaker Line Sanity
            if len(line) == 0: # Should be covered by isupper() which usually requires content, but let's be safe
                raise ValueError("Invalid speaker line")
            if len(line) > 40:
                raise ValueError("Invalid speaker line")
            if line[-1] in '.,!?:;':
                raise ValueError("Invalid speaker line")
            
            last_line_was_speaker = True
            continue

        # Check parenthetical
        if line.startswith('('):
            # Rule 5: Parenthetical Sanity
            if not line.endswith(')'):
                raise ValueError("Invalid parenthetical placement")
            if not last_line_was_speaker:
                raise ValueError("Invalid parenthetical placement")
            
            last_line_was_speaker = False
            continue

        # Any other line (Mixed case dialogue, empty lines, formatting)
        # Resets the "last was speaker" state because a parenthetical must strictly follow a speaker.
        last_line_was_speaker = False

    # Rule 2: Scene Header Presence
    if headers_found == 0:
        raise ValueError("No scene headers found")
