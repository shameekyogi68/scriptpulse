import streamlit as st
import matplotlib.pyplot as plt
from typing import List, Dict

# Explicitly add current directory to sys.path to allow imports from runnable script context
import sys
import os
sys.path.append(os.getcwd())

from run_scriptpulse import run_scriptpulse
from scriptpulse.engine.validator import validate_script
from scriptpulse.engine.preprocess import preprocess_lines
from scriptpulse.engine.segment import segment_scenes
from scriptpulse.engine.features import extract_scene_features
from scriptpulse.engine.effort import compute_effort
from scriptpulse.engine.temporal_graph import build_temporal_graph
from scriptpulse.engine.accumulate import accumulate_signals

# 1. App Header
st.title("ScriptPulse v1.3.1")
st.caption("Deterministic structural strain analysis. No semantic interpretation.")

# 2. Input Section
input_lines: List[str] = []

st.subheader("Input Screenplay")
paste_input = st.text_area("Paste screenplay text here:", height=300)
file_input = st.file_uploader("Or upload .txt file", type=["txt"])

if paste_input:
    input_lines = paste_input.splitlines()
elif file_input:
    # Read file content
    string_data = file_input.getvalue().decode("utf-8")
    input_lines = string_data.splitlines()

# 3. Run Button
if st.button("Run ScriptPulse"):
    if not input_lines:
        st.error("Please provide valid screenplay text.")
    else:
        try:
            # 2. Call Execution Pipeline
            messages = run_scriptpulse(input_lines)
            
            # --- VISUALIZATION DATA EXTRACTION (DUPLICATION FOR PLOTTING) ---
            # This logic strictly mirrors run_scriptpulse.py for data access
            
            # Validate & Preprocess
            validate_script(input_lines) # Will raise if invalid, caught by try/except
            clean_lines = preprocess_lines(input_lines)
            
            # Segment
            scenes = segment_scenes(clean_lines)
            
            # Features
            features = extract_scene_features(scenes)
            
            # Normalization (Inline copy from run_scriptpulse)
            raw_for_norm = []
            for f in features:
                lines_count = f["Lines"]
                action_density = float(f["ActionLines"]) / lines_count if lines_count > 0 else 0.0
                vis_penalty = float(f["MaxContinuousLines"]) - float(f["WhitespaceRatio"])
                
                raw_for_norm.append({
                    "AvgSentenceLength": float(f["AvgSentenceLength"]),
                    "ActionDensity": action_density,
                    "DialogueTurnCount": float(f["DialogueTurnCount"]),
                    "RepetitionScore": 0.0,
                    "VisualDensityPenalty": vis_penalty,
                    "AuditoryLoad": float(f["AuditoryLoad"])
                })

            keys_to_normalize = [
                "AvgSentenceLength", "ActionDensity", "DialogueTurnCount", 
                "RepetitionScore", "VisualDensityPenalty", "AuditoryLoad"
            ]
            
            stats = {}
            for k in keys_to_normalize:
                vals = [item[k] for item in raw_for_norm]
                stats[k] = (min(vals), max(vals))

            features_norm = []
            for item in raw_for_norm:
                norm_item = {}
                for k in keys_to_normalize:
                    val = item[k]
                    min_v, max_v = stats[k]
                    denom = max_v - min_v + 1e-8
                    norm_val = (val - min_v) / denom
                    norm_item[k] = norm_val
                features_norm.append(norm_item)
            
            # Effort
            effort = compute_effort(features_norm)
            
            # Temporal
            temporal = build_temporal_graph(effort)
            decayed_signal = temporal["decayed"]
            
            # --- END DATA EXTRACTION ---

            # 4. Alerts Display
            st.subheader("Analysis Results")
            if not messages:
                st.success("No structural strain detected.")
            else:
                for msg in messages:
                    st.warning(msg)

            # 5. Visualization (Matplotlib Only)
            st.subheader("Effort Signals")
            
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
            
            # Plot 1: Per-Scene Effort
            ax1.plot(effort, marker='o', linestyle='-', color='blue')
            ax1.set_title("Per-Scene Effort (Raw)")
            ax1.set_xlabel("Scene Index")
            ax1.set_ylabel("Effort Score")
            ax1.grid(True, linestyle='--', alpha=0.6)
            
            # Plot 2: Decayed Accumulated Effort
            ax2.plot(decayed_signal, marker='x', linestyle='-', color='red')
            ax2.set_title("Decayed Accumulated Effort")
            ax2.set_xlabel("Scene Index")
            ax2.set_ylabel("Accumulated Effort")
            ax2.grid(True, linestyle='--', alpha=0.6)
            
            plt.tight_layout()
            st.pyplot(fig)

        except ValueError as e:
            st.error(f"Validation Error: {str(e)}")
        except Exception as e:
            st.error(f"Execution Error: {str(e)}")

# 6. Limitations Section
st.markdown("---")
st.markdown("**Limitations:**")
st.markdown("• Structural analysis only")
st.markdown("• No semantic understanding")
st.markdown("• No quality judgments")
st.markdown("• Deterministic, non-adaptive system")
