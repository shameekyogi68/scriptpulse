import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Optional

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
st.set_page_config(page_title="ScriptPulse", page_icon="📝", layout="wide")

# Custom CSS for "Writer Cognition" UX
st.markdown("""
    <style>
    .focus-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .focus-header {
        font-weight: 600;
        color: #d9534f;
        font-size: 1.1em;
        margin-bottom: 10px;
    }
    .metric-arrow-up { color: #d9534f; font-weight: bold; }
    .metric-arrow-down { color: #5cb85c; font-weight: bold; }
    .metric-arrow-flat { color: #777; font-weight: bold; }
    
    .start-here-box {
        background-color: #f0f8ff;
        border-left: 5px solid #007bff;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 25px;
    }
    .sticky-note {
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        color: #856404;
        padding: 15px;
        border-radius: 5px;
        font-size: 0.9em;
    }
    .summary-green { color: #155724; background-color: #d4edda; padding: 10px; border-radius: 5px; }
    .summary-yellow { color: #856404; background-color: #fff3cd; padding: 10px; border-radius: 5px; }
    .summary-red { color: #721c24; background-color: #f8d7da; padding: 10px; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR (Permanent Context) ---
with st.sidebar:
    st.header("ScriptPulse v1.3.1")
    st.markdown("---")
    st.markdown("""
    <div class="sticky-note">
        <strong>🚫 ScriptPulse is NOT</strong>
        <ul>
            <li>grading your script</li>
            <li>judging quality</li>
            <li>telling you what to change</li>
        </ul>
        <strong>✅ It IS</strong>
        <ul>
            <li>showing how structure behaves over time</li>
            <li>mirroring pressure vs. relief</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    view_mode = st.radio("View Mode", ["Writer View", "Technical View"], index=0)

# --- HELPER FUNCTIONS ---
def get_arrow(curr, prev):
    if prev is None: return "⏺"
    if curr > prev * 1.05: return "↑ Pressure Increases"
    if curr < prev * 0.95: return "↓ Pressure Releases"
    return "→ Pressure Holds"

def get_structural_summary(alert_count, total_scenes):
    if total_scenes == 0: return ("⚪", "No scenes detected.")
    ratio = alert_count / total_scenes
    if alert_count == 0:
        return ("green", "The structure provides the audience with natural breathing room throughout.")
    elif ratio < 0.2:
        return ("yellow", "Pressure builds steadily, with some specific moments demanding attention.")
    else:
        return ("red", "Extended pressure appears frequently without structural relief.")

# --- MAIN APP LAYOUT ---

# 1. Start Here Entry Point
st.title("ScriptPulse")
st.markdown("""
<div class="start-here-box">
    <h4>👋 Start Here</h4>
    <p>ScriptPulse looks at how long and how intensely the audience is asked to stay engaged without relief.
    You don’t need to fix anything. Just notice <strong>where pressure builds or releases.</strong></p>
</div>
""", unsafe_allow_html=True)

# 2. Input
input_col, help_col = st.columns([2, 1])
with input_col:
    paste_input = st.text_area("Screenplay Text", height=200, placeholder="Paste your scene here...")
    file_input = st.file_uploader("Or upload .txt", type=["txt"])

input_lines = []
if paste_input: input_lines = paste_input.splitlines()
elif file_input: input_lines = file_input.getvalue().decode("utf-8").splitlines()

if st.button("Analyze Structure", type="primary"):
    if not input_lines:
        st.warning("Please provide a script to analyze.")
    else:
        try:
            # --- ENGINE EXECUTION (VISUALIZATION DATA) ---
            # Replicating run_scriptpulse logic locally for data access
            validate_script(input_lines)
            clean_lines = preprocess_lines(input_lines)
            scenes = segment_scenes(clean_lines)
            features = extract_scene_features(scenes)
            
            # Normalization
            raw_for_norm = []
            for f in features:
                lines_count = f["Lines"]
                act_dens = float(f["ActionLines"])/lines_count if lines_count>0 else 0.0
                vis_pen = float(f["MaxContinuousLines"]) - float(f["WhitespaceRatio"])
                raw_for_norm.append({
                    "AvgSentenceLength": float(f["AvgSentenceLength"]),
                    "ActionDensity": act_dens,
                    "DialogueTurnCount": f["DialogueTurnCount"],
                    "RepetitionScore": 0.0,
                    "VisualDensityPenalty": vis_pen,
                    "AuditoryLoad": f["AuditoryLoad"]
                })
            
            keys = ["AvgSentenceLength", "ActionDensity", "DialogueTurnCount", "RepetitionScore", "VisualDensityPenalty", "AuditoryLoad"]
            stats = {k: (min(d[k] for d in raw_for_norm), max(d[k] for d in raw_for_norm)) for k in keys}
            
            features_norm = []
            for item in raw_for_norm:
                n_item = {}
                for k in keys:
                    mn, mx = stats[k]
                    n_item[k] = (item[k] - mn) / (mx - mn + 1e-8)
                features_norm.append(n_item)
                
            effort = compute_effort(features_norm)
            temporal = build_temporal_graph(effort)
            decayed = temporal["decayed"]
            
            # Get Alerts
            messages = run_scriptpulse(input_lines)
            alert_indices = []
            for msg in messages:
                try: alert_indices.append(int(msg.strip('.').split(' ')[-1]))
                except: pass
            
            # --- WRITER COGNITION UI ---

            # 3. Structural Summary
            color, summary_text = get_structural_summary(len(alert_indices), len(scenes))
            st.markdown(f'<div class="summary-{color}"><strong>Structural Summary:</strong> {summary_text}</div>', unsafe_allow_html=True)
            st.write("")

            if view_mode == "Writer View":
                # 4. Audience Energy Timeline (Writer Friendly)
                st.subheader("Audience Energy Load")
                st.caption("How demanding the structure is over time.")
                
                fig, ax = plt.subplots(figsize=(12, 3))
                ax.plot(decayed, color='#555', linewidth=1.5)
                ax.fill_between(range(len(decayed)), decayed, color='#e0e0e0', alpha=0.4)
                
                # Markers
                if alert_indices:
                    vals = [decayed[i] for i in alert_indices]
                    ax.scatter(alert_indices, vals, color='#d9534f', s=60, zorder=5, label='Focus Point')
                
                ax.set_yticks([])
                ax.set_xticks(range(len(scenes)))
                ax.set_xticklabels([str(i) for i in range(len(scenes))], fontsize=8)
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_visible(False)
                ax.set_ylabel("Pressure")
                ax.set_xlabel("Scene Index")
                st.pyplot(fig)

                # 5. Focus Points (Scene Cards)
                st.subheader("Focus Points")
                if not alert_indices:
                    st.info("🟢 No specific scenes require structural focus. The pacing feels naturally varied.")
                else:
                    for i in alert_indices:
                        prev_eff = decayed[i-1] if i > 0 else 0
                        curr_eff = decayed[i]
                        arrow = get_arrow(curr_eff, prev_eff)
                        
                        header = scenes[i].header.strip()
                        
                        # Comparison logic (Observational)
                        obs = []
                        if features[i]["ActionLines"] > features[i]["DialogueLines"]:
                            obs.append("Action-heavy structure")
                        else:
                            obs.append("Dialogue-heavy structure")
                        
                        if i > 0 and abs(features[i]["AvgSentenceLength"] - features[i-1]["AvgSentenceLength"]) < 2:
                             obs.append("Similar rhythm to previous scene")
                        
                        with st.container():
                            st.markdown(f"""
                            <div class="focus-card">
                                <div class="focus-header">📍 Focus Point: Scene {i} <span style="color:#333; font-weight:normal; font-size:0.8em">({header})</span></div>
                                <p><strong>Context:</strong> {arrow}</p>
                                <p><strong>Why this stands out (Descriptive):</strong></p>
                                <ul>
                                    <li>{"</li><li>".join(obs)}</li>
                                    <li>Contributes to sustained structural pressure</li>
                                </ul>
                                <hr style="margin: 10px 0;">
                                <p style="font-size:0.9em; color:#555;"><em>Questions to ask yourself:</em></p>
                                <ul style="font-size:0.9em; color:#555;">
                                    <li>Do I want the audience to stay under pressure this long?</li>
                                    <li>Is this repetition intentional?</li>
                                    <li>Would a structural shift (shorter sentences, break in pattern) help here?</li>
                                </ul>
                            </div>
                            """, unsafe_allow_html=True)

            else:
                # Technical View (Original functionality + extras)
                st.subheader("Technical Analysis")
                st.write(f"**Total Scenes:** {len(scenes)}")
                
                # Raw Alerts
                if messages:
                    for m in messages:
                        st.warning(m)
                else:
                    st.success("No alerts triggers.")
                
                # Plots
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Raw Effort**")
                    st.line_chart(effort)
                with col2:
                    st.write("**Accumulated Strain**")
                    st.line_chart(decayed)
                
                with st.expander("Raw Feature Data"):
                    st.json(features[:3]) # Show first 3 for debugging

        except ValueError as ve:
             st.error(f"Validation Error: {ve}")
        except Exception as e:
             st.error(f"Error: {e}")
