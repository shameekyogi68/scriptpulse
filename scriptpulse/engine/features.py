
from typing import List, Dict, Union
import math
# Type checking import only to avoid runtime circular dependency or just for clarity
# In python runtime, if we just type hint with strings it is fine.
# But for users of this function, they will pass SceneSegment objects.
# We assume the module is importable if needed, but we don't need to import the class definition 
# to run the logic if we just access attributes. 
# However, for type hints to be useful to static analysis, we usually suggest importing.
# But "Allowed Imports" did not list the module. 
# "SceneSegment and Block are imported only from engine.segment" -> OK to import.
from scriptpulse.engine.segment import SceneSegment, Block

def extract_scene_features(scenes: List[SceneSegment]) -> List[Dict[str, Union[float, int]]]:
    """
    Computes raw per-scene structural features.
    Deterministic, raw calculation only.
    """
    features_list = []

    for scene in scenes:
        # Pre-calc collections
        all_blocks = scene.blocks
        action_blocks = [b for b in all_blocks if b.block_type == "ACTION"]
        dialogue_blocks = [b for b in all_blocks if b.block_type == "DIALOGUE"]
        
        # 1. Basic Counts
        # Lines_i: Total raw lines
        lines_count = len(scene.raw_lines)
        
        # Words_i: Total word count across all non-blank lines
        words_count = 0
        for line in scene.raw_lines:
            stripped = line.strip()
            if stripped:
                # "Split on whitespace"
                words_count += len(stripped.split())
        
        # Sentences_i: Total detected sentences
        # Sentences are in block.sentences
        all_sentences = []
        for b in all_blocks:
            all_sentences.extend(b.sentences)
        sentences_count = len(all_sentences)
        
        # ActionLines_i: Total lines in ACTION blocks
        action_lines_count = sum(len(b.lines) for b in action_blocks)
        
        # DialogueLines_i: Total lines in DIALOGUE blocks (exclude speaker name line)
        # Block structure: speaker is a field, not in lines. lines are just the speech/paren.
        # So len(b.lines) is correct.
        dialogue_lines_count = sum(len(b.lines) for b in dialogue_blocks)
        
        # DialogueTurns_i: number of dialogue blocks
        dialogue_turns_count = len(dialogue_blocks)
        
        # Speakers_i: unique speakers
        unique_speakers = set()
        for b in dialogue_blocks:
            if b.speaker:
                unique_speakers.add(b.speaker)
        speakers_count = len(unique_speakers)
        
        # 2. Sentence Metrics
        sentence_lengths = [len(s.split()) for s in all_sentences]
        
        # AvgSentenceLength_i
        if sentences_count > 0:
            avg_sentence_len = words_count / sentences_count # Wait says "Using sentence word counts"
            # Text: "AvgSentenceLength_i = Words_i / Sentences_i"
            # But Words_i includes words from lines that might not be in "sentences"? 
            # (e.g. headers, or if splitting logic discarded something?)
            # Prompt says "Using sentence word counts" then formulas.
            # "Words_i" was defined as "total word count across all non-blank lines".
            # "Sentences_i" is total detected.
            # Formula: Words_i / Sentences_i. We follow formula strictly.
            # (Note: Words_i includes Header line words usually? Header is in raw_lines.)
            avg_sentence_len = float(words_count) / sentences_count
        else:
            avg_sentence_len = 0.0
            
        # MaxSentenceLength_i
        # "max words in any sentence" -> From detected sentences.
        if sentence_lengths:
            max_sentence_len = max(sentence_lengths)
        else:
            max_sentence_len = 0
            
        # SentenceVariance_i
        # "population variance of sentence word counts"
        if sentences_count < 2:
            sentence_variance = 0.0
        else:
            # Pop Variance: sum((x - mean)^2) / N
            # Mean of sentences specifically, or use logic? "variance of sentence word counts"
            # Implies we use the specific sentence lengths, NOT Words_i/Sentences_i (which uses global words)
            mean_s = sum(sentence_lengths) / sentences_count
            variance_sum = math.fsum((x - mean_s) ** 2 for x in sentence_lengths)
            sentence_variance = variance_sum / sentences_count # Population variance uses N
        
        # 3. Dialogue Structure
        
        # DialogueTurnCount_i (Same as above)
        
        # SpeakerSwitchCount_i
        # "changes between consecutive dialogue blocks"
        # Iterate through *dialogue blocks only* or all blocks? 
        # "consecutive dialogue blocks". 
        # Usually implies if D1(Bob), A1, D2(Bob) -> No switch? Or switch?
        # "between consecutive dialogue blocks" -> could mean ignoring Action.
        # Let's assume list of dialogue blocks in order.
        switch_count = 0
        current_speak = None
        for i, db in enumerate(dialogue_blocks):
            if i == 0:
                current_speak = db.speaker
            else:
                if db.speaker != current_speak:
                    switch_count += 1
                    current_speak = db.speaker
        
        # DialogueActionRatio_i
        dialogue_action_ratio = float(dialogue_lines_count) / (action_lines_count + 1)
        
        # 4. Visual Density Proxies
        
        # AvgActionBlockLength_i
        if action_blocks:
            avg_action_block_len = float(action_lines_count) / len(action_blocks)
        else:
            avg_action_block_len = 0.0
            
        # MaxContinuousLines_i
        # "longest uninterrupted run of non-blank lines in the scene"
        # Iterate raw lines.
        max_cont = 0
        current_cont = 0
        for line in scene.raw_lines:
            if line.strip():
                current_cont += 1
            else:
                if current_cont > max_cont:
                    max_cont = current_cont
                current_cont = 0
        if current_cont > max_cont:
            max_cont = current_cont
            
        # WhitespaceRatio_i
        # blank lines / total lines
        if lines_count > 0:
            blank_lines = sum(1 for line in scene.raw_lines if not line.strip())
            whitespace_ratio = float(blank_lines) / lines_count
        else:
            whitespace_ratio = 0.0
            
        # 5. Auditory Load Proxy
        # AuditoryLoad_i = DialogueTurns_i * AvgSentenceLength_i
        auditory_load = float(dialogue_turns_count) * avg_sentence_len
        
        scene_dict = {
            "Lines": lines_count,
            "Words": words_count,
            "Sentences": sentences_count,
            "ActionLines": action_lines_count,
            "DialogueLines": dialogue_lines_count,
            "DialogueTurns": dialogue_turns_count,
            "Speakers": speakers_count,
            
            "AvgSentenceLength": avg_sentence_len,
            "MaxSentenceLength": max_sentence_len,
            "SentenceVariance": sentence_variance,
            
            "DialogueTurnCount": dialogue_turns_count,
            "SpeakerSwitchCount": switch_count,
            "DialogueActionRatio": dialogue_action_ratio,
            
            "AvgActionBlockLength": avg_action_block_len,
            "MaxContinuousLines": max_cont,
            "WhitespaceRatio": whitespace_ratio,
            
            "AuditoryLoad": auditory_load
        }
        
        features_list.append(scene_dict)

    return features_list
