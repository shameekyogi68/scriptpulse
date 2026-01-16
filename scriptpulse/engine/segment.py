
import re
from dataclasses import dataclass
from typing import List, Optional, Literal

@dataclass
class Block:
    block_type: Literal["ACTION", "DIALOGUE"]
    lines: List[str]
    speaker: Optional[str]
    sentences: List[str]

@dataclass
class SceneSegment:
    scene_index: int
    header: str
    raw_lines: List[str]
    blocks: List[Block]

def segment_scenes(lines: List[str]) -> List[SceneSegment]:
    """
    Deterministically segments a screenplay into scenes and structural blocks.
    """
    scenes: List[SceneSegment] = []
    
    current_scene: Optional[SceneSegment] = None
    current_block: Optional[Block] = None
    
    # Track the type of the previous non-blank line for classification logic
    # Types: "BLANK", "SPEAKER", "PARENTHETICAL", "DIALOGUE", "ACTION"
    # Initialized to "BLANK" effectively, or None. 
    # But Header lines reset/intervene.
    last_non_blank_type = None 
    
    scene_index_counter = 0
    
    # "A new scene begins only on a line matching: ^INT\. or ^EXT\. ... Match must be: Uppercase ... At line start"
    scene_header_pattern = re.compile(r'^(INT\.|EXT\.)')
    
    # "Split sentences using regex on: . ! ?"
    sentence_split_pattern = re.compile(r'[.!?]')

    def finalize_block():
        nonlocal current_block
        if current_block:
            # Sentence Splitting
            # "Combine lines... Split... Strip... Discard empty"
            # Assuming space join for safety
            full_text = " ".join(current_block.lines)
            # Regex split consumes the delimiter. 
            # Prompt example: "He runs! He falls." -> ["He runs", "He falls"]
            # This implies delimiters are removed.
            raw_splits = sentence_split_pattern.split(full_text)
            clean_sentences = [s.strip() for s in raw_splits if s.strip()]
            current_block.sentences = clean_sentences
            
            if current_scene:
                current_scene.blocks.append(current_block)
            current_block = None

    for line in lines:
        # Check Scene Header
        # "Match must be: Uppercase ... At line start"
        if line.isupper() and scene_header_pattern.match(line):
            finalize_block()
            
            # Begin new scene
            current_scene = SceneSegment(
                scene_index=scene_index_counter,
                header=line,
                raw_lines=[line],
                blocks=[]
            )
            scenes.append(current_scene)
            scene_index_counter += 1
            
            # Reset block-level context
            last_non_blank_type = None 
            continue

        # Check for content before first scene header
        if current_scene is None:
            if line == "":
                continue
            else:
                # "Lines before the first scene header must not exist"
                raise ValueError("Content before first scene header")

        # In Scene
        current_scene.raw_lines.append(line)
        
        # Determine Line Type
        current_type = None
        
        # 1. If line == "" -> BLANK
        if line == "":
            current_type = "BLANK"
        
        # 2. Else if line is fully uppercase AND length <= 40 -> SPEAKER
        elif line.isupper() and len(line) <= 40:
            current_type = "SPEAKER"
            
        # 3. Else if line starts with '(' AND ends with ')' -> PARENTHETICAL
        elif line.startswith('(') and line.endswith(')'):
            current_type = "PARENTHETICAL"
            
        # 4. Else if previous non-blank line was SPEAKER or PARENTHETICAL -> DIALOGUE
        elif last_non_blank_type in ["SPEAKER", "PARENTHETICAL"]:
            current_type = "DIALOGUE"
            
        # 5. Else -> ACTION
        else:
            current_type = "ACTION"


        # Block Construction Logic
        if current_type == "BLANK":
            finalize_block()
            # BLANK does not update last_non_blank_type

        elif current_type == "SPEAKER":
            finalize_block() # "Ends when... a new SPEAKER"
            # Start Dialogue Block
            # "A dialogue block: Starts at a SPEAKER"
            # Speaker line is not added to 'lines' (content), but stored in 'speaker'.
            current_block = Block(
                block_type="DIALOGUE",
                lines=[],
                speaker=line,
                sentences=[]
            )
            last_non_blank_type = "SPEAKER"

        elif current_type == "PARENTHETICAL":
            # "Includes... optional PARENTHETICAL"
            # Strictly, should be inside a Dialogue block if prev was Speaker.
            if current_block and current_block.block_type == "DIALOGUE":
                current_block.lines.append(line)
            else:
                # Fallback if structure is weird (shouldn't be with validator)
                # But if it falls to Paren, we treat as Dialogue content?
                # Or start new block? No provided rule for Paren-only block.
                # Assuming valid script, we append.
                # In robust code, might need handling, but "Gravity-locked" implies ignoring edge case not in spec.
                pass
            last_non_blank_type = "PARENTHETICAL"

        elif current_type == "DIALOGUE":
            if current_block and current_block.block_type == "DIALOGUE":
                current_block.lines.append(line)
            last_non_blank_type = "DIALOGUE"

        elif current_type == "ACTION":
            # Action Block: "Consists of one or more consecutive ACTION lines"
            # If current is Dialogue, we must close it (Implicit end of dialogue block if Action appears)
            if current_block and current_block.block_type == "DIALOGUE":
                finalize_block()
            
            if current_block is None:
                current_block = Block(
                    block_type="ACTION",
                    lines=[line],
                    speaker=None,
                    sentences=[]
                )
            elif current_block.block_type == "ACTION":
                current_block.lines.append(line)
            else:
                # Should have been finalized above
                pass
            
            last_non_blank_type = "ACTION"

    finalize_block()

    if not scenes:
        raise ValueError("No scenes detected")
        
    return scenes
