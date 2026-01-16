import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict

# Explicitly add current directory to sys.path
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

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="ScriptPulse", page_icon="📝", layout="centered")

# Custom CSS for "Writer translation" look
st.markdown("""
    <style>
    .stAlert {
        border-radius: 8px;
    }
    .traffic-light-green {
        color: #0f5132;
        background-color: #d1e7dd;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #198754;
    }
    .traffic-light-red {
        color: #842029;
        background-color: #f8d7da;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #dc3545;
    }
    .explanation-box {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 5px;
        padding: 15px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 1. App Header
st.title("ScriptPulse 1.3.1")
st.caption("Writer-Focused Structural Intuition Tool")

# 2. Input Section
input_lines: List[str] = []

with st.expander("📖 How to use this tool", expanded=False):
    st.markdown("""
    **ScriptPulse measures structural pressure.**
    It looks for sections where the audience is asked to focus intensely for a long time without a break.
    
    * Paste your script or upload a file.
    * Look for the **Energy Timeline**.
    * Check the **Scene Cards** for breakdown.
    """)

st.subheader("Input Screenplay")
tab1, tab2 = st.tabs(["Paste Text", "Upload File"])

with tab1:
    paste_input = st.text_area("Paste screenplay text here:", height=300, key="paste_in")

with tab2:
    file_input = st.file_uploader("Upload .txt file", type=["txt"], key="file_in")

if paste_input:
    input_lines = paste_input.splitlines()
elif file_input:
    string_data = file_input.getvalue().decode("utf-8")
    input_lines = string_data.splitlines()

# 3. Run Button
if st.button("Analyze Structure", type="primary"):
    if not input_lines:
        st.error("Please provide valid screenplay text.")
    else:
        try:
            # --- ENGINE PIPELINE (Data Extraction for Vis) ---
            # Replicating logic for visualization data access
            validate_script(input_lines)
            clean_lines = preprocess_lines(input_lines)
            scenes = segment_scenes(clean_lines)
            features = extract_scene_features(scenes)
            
            # Normalization (Inline)
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
            
            effort = compute_effort(features_norm)
            temporal = build_temporal_graph(effort)
            decayed_signal = temporal["decayed"]
            
            # Run Standard Core to get alerts (for compliance)
            messages = run_scriptpulse(input_lines)
            has_alerts = len(messages) > 0

            # --- WRITER TRANSLATION LAYER ---

            # 4. Traffic Light Status
            st.divider()
            st.subheader("Overall Structural Status")
            
            if not has_alerts:
                st.markdown("""
                <div class="traffic-light-green">
                    <h3>🟢 Breathing Room Detected</h3>
                    <p>The structure gives the audience enough chances to recover naturally. No sections appear structurally overwhelming.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="traffic-light-red">
                    <h3>🔴 Structural Pressure Detected</h3>
                    <p>The script pushes the audience continuously in specific sections without a clear structural break.</p>
                    <p><strong>{len(messages)} scenes</strong> show signs of high sustained demand.</p>
                </div>
                """, unsafe_allow_html=True)

            # 5. Audience Energy Timeline
            st.subheader("Audience Energy Load")
            st.caption("How demanding the structure is over time (cumulative pressure).")
            
            fig, ax = plt.subplots(figsize=(10, 4))
            
            # Gradient fill or simple fill
            scenes_idx = range(len(decayed_signal))
            ax.plot(scenes_idx, decayed_signal, color='#333333', linewidth=2, label='Accumulated Pressure')
            ax.fill_between(scenes_idx, decayed_signal, color='#e0e0e0', alpha=0.5)
            
            # Highlight Alert Zones
            # We need to map alerts to scene indices
            # messages are like "Structural strain detected in scene X."
            alert_indices = []
            for msg in messages:
                # Parse index strictly from template: "Structural strain detected in scene {i}."
                try:
                    parts = msg.strip('.').split(' ')
                    idx = int(parts[-1])
                    alert_indices.append(idx)
                except:
                    pass
            
            if alert_indices:
                # Highlight points
                alert_vals = [decayed_signal[i] for i in alert_indices]
                ax.scatter(alert_indices, alert_vals, color='red', s=50, zorder=5, label='Strain Alert')
            
            ax.set_xlabel("Scene Number")
            ax.set_ylabel("Structural Load (Low → High)")
            ax.set_yticks([]) # Hide raw numbers
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.legend()
            
            st.pyplot(fig)

            # 6. Scene Cards (Only for Alerts)
            if alert_indices:
                st.subheader("Scene Breakdown (High Pressure)")
                for idx in alert_indices:
                    with st.container():
                        st.markdown(f"#### 🎬 Scene {idx}")
                        # Provide some context from features if possible
                        f_curr = features[idx]
                        sc_header = scenes[idx].header.strip()
                        
                        cols = st.columns(3)
                        cols[0].metric("Action Lines", f_curr["ActionLines"])
                        cols[1].metric("Dialogue Turns", f_curr["DialogueTurns"])
                        cols[2].metric("Est. Auditory Load", f"{f_curr['AuditoryLoad']:.1f}")
                        
                        st.markdown("""
                        > *This scene continues structural pressure without offering a release.*
                        """)
                        st.divider()

            # 7. Explainer Boxes
            st.markdown("""
            <div class="explanation-box">
                <h4>🧠 What ScriptPulse is telling you</h4>
                <p>ScriptPulse does not judge story quality or creativity. 
                It only looks at <strong>how long and how intensely you ask the audience to stay focused without rest</strong>.</p>
                <p>Alerts simply mean: <em>“You might want to consider a pause, variation, or release here.”</em></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="explanation-box">
                <h4>🚫 What ScriptPulse is NOT saying</h4>
                <ul>
                    <li>It is NOT saying the scene is bad.</li>
                    <li>It is NOT saying the writing is wrong.</li>
                    <li>It is NOT saying the story fails.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        except ValueError as e:
            st.error(f"Validation Error: {str(e)}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
