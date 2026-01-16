from typing import List
import re

def preprocess_lines(lines: List[str]) -> List[str]:
    """
    Returns a new list of normalized lines.
    Length and ordering preserved.
    Performs deterministic whitespace normalization.
    """
    normalized_lines = []
    
    # Pre-compile regex for space collapsing to avoid re-compiling every line
    # Matches 2 or more spaces, to be replaced by 1. 
    # Or matches 1 or more? Rule: "Collapse multiple spaces into one". 
    # If we have "A B", do we keep "A B"? Yes.
    # If we have "A  B", we want "A B".
    # Logic: replace(tab, space) then collapse spaces (space+ -> space).
    space_collapse_pattern = re.compile(r' +')

    for line in lines:
        # Rule 1.1: Strip leading and trailing whitespace
        # This removes spaces, tabs, newlines from ends
        s = line.strip()

        # Rule 1.2: Replace internal tabs with a single space
        s = s.replace('\t', ' ')

        # Rule 1.3: Collapse multiple spaces into one space
        # We use strict space character based on "Collapse multiple spaces"
        s = space_collapse_pattern.sub(' ', s)

        # Rule 5 check: Ensure no line contains \n or \r (should be handled by strip if at ends, assuming none internal)
        # We explicitly remove them just in case, ensuring deterministic "no \n or \r" state?
        # Instructions say "Ensure...". 
        # Since input contract says "Newlines already stripped", we trust input but strip() aids this.
        # We will not aggressively remove internal \n unless strictly forced, as contracts imply they aren't there.
        # However, to be "safe", let's just assert or rely on strip. 
        # Actually, let's just stick to the transformation.
        
        normalized_lines.append(s)

    return normalized_lines
