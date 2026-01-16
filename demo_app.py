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

# Custom CSS for "Cinematic Professional" UI
st.markdown("""
    <style>
    /* Main Background adjustments are simplified as Streamlit controls theme mostly, 
       but we can style our containers to be 'Card-like' or 'Panel-like' */
    
    .professional-card {
        background-color: #f8f9fa; /* Light gray for cleanliness, or dark if dark mode enabled? Keeping light/neutral for safety */
        border-left: 4px solid #6c757d; /* Neutral accent */
        padding: 20px;
        margin-bottom: 20px;
        border-radius: 4px;
    }
    
    .focus-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        padding: 24px;
        margin-bottom: 16px;
    }
    
    .focus-header {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 600;
        color: #333;
        font-size: 1.05em;
        margin-bottom: 8px;
        border-bottom: 1px solid #eee;
        padding-bottom: 8px;
    }

    .overview-box {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 20px;
        border-radius: 4px;
        margin-bottom: 24px;
        color: #333333;
    }

    .sidebar-panel {
        background-color: #f1f3f5;
        padding: 15px;
        border-radius: 4px;
        font-size: 0.9em;
        color: #495057;
        margin-bottom: 20px;
    }
    
    .metric-label {
        font-size: 0.8em;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #6c757d;
    }
    
    .status-text-normal { color: #495057; font-weight: 500; }
    .status-text-alert { color: #b71c1c; font-weight: 600; }
    
    hr { margin-top: 10px; margin-bottom: 10px; border-top: 1px solid #eee; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR (Permanent Context) ---
with st.sidebar:
    st.header("ScriptPulse v1.3.1")
    st.markdown("---")
    
    # Neutral Sidebar Panel
    st.markdown("""
    <div class="sidebar-panel">
        <strong>What ScriptPulse Does</strong>
        <p style="margin-top:5px; margin-bottom:10px;">
        • Observes how structural pressure builds over time<br>
        • Highlights sections with sustained demand
        </p>
        <strong>What ScriptPulse Does Not Do</strong>
        <p style="margin-top:5px; margin-bottom:0;">
        • Judge quality<br>
        • Evaluate creativity<br>
        • Suggest changes
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    view_mode = st.radio("View Mode", ["Writer View", "Technical View"], index=0)

# --- HELPER FUNCTIONS ---
def get_arrow_text(curr, prev):
    if prev is None: return "Initial Scene"
    if curr > prev * 1.05: return "Pressure Increasing"
    if curr < prev * 0.95: return "Pressure Releasing"
    return "Pressure Holding"

def get_structural_summary_text(alert_count, total_scenes):
    if total_scenes == 0: return "No scenes detected.", "status-text-normal"
    
    if alert_count == 0:
        return "The structure provides the audience with natural breathing room.", "status-text-normal"
    else:
        return "The script pushes the audience continuously in specific sections without a clear structural break.", "status-text-alert"

# --- MAIN APP LAYOUT ---

# 1. Overview (Renamed from "Start Here")
st.title("ScriptPulse")
st.markdown("""
<div class="overview-box">
    <h4 style="margin-top:0;">Overview</h4>
    <p>ScriptPulse observes how long the audience is asked to remain engaged without relief. 
    Use this view to notice where pressure accumulates or releases.</p>
</div>
""", unsafe_allow_html=True)

# 2. Input
input_col, space_col = st.columns([2, 1])
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
            # --- ENGINE EXECUTION ---
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
            
            # --- WRITER COGNITION UI (REFINED) ---
            st.divider()

            # 3. Structural Summary
            summary, status_class = get_structural_summary_text(len(alert_indices), len(scenes))
            st.markdown(f'<div class="{status_class}" style="font-size:1.1em; margin-bottom:20px;">{summary}</div>', unsafe_allow_html=True)
            
            if view_mode == "Writer View":
                # 4. Audience Energy Timeline
                st.caption("AUDIENCE ENERGY LOAD")
                
                fig, ax = plt.subplots(figsize=(12, 3))
                # Cinematic styling: minimalist
                ax.plot(decayed, color='#333333', linewidth=1.2)
                ax.fill_between(range(len(decayed)), decayed, color='#e0e0e0', alpha=0.3)
                
                # Markers for alerts (Subtle red dots)
                if alert_indices:
                    vals = [decayed[i] for i in alert_indices]
                    ax.scatter(alert_indices, vals, color='#b71c1c', s=30, zorder=5, label='Alert')
                
                ax.set_yticks([])
                ax.set_xticks(range(len(scenes)))
                ax.set_xticklabels([str(i) for i in range(len(scenes))], fontsize=8, color='#666')
                
                # Remove borders
                for spine in ax.spines.values():
                    spine.set_visible(False)
                ax.spines['bottom'].set_visible(True)
                ax.spines['bottom'].set_color('#ddd')
                
                ax.set_ylabel("Pressure", fontsize=9, color='#666')
                ax.set_xlabel("Scene Index", fontsize=9, color='#666')
                st.pyplot(fig)

                # 5. Focus Points (Typography-based)
                st.write("")
                st.caption("FOCUS POINTS")
                
                if not alert_indices:
                    st.markdown("<p style='color:#666;'>No specific scenes require structural focus.</p>", unsafe_allow_html=True)
                else:
                    for i in alert_indices:
                        prev_eff = decayed[i-1] if i > 0 else 0
                        curr_eff = decayed[i]
                        arrow_txt = get_arrow_text(curr_eff, prev_eff)
                        
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
                                <div class="focus-header">Scene {i}: {header}</div>
                                <div style="display:flex; justify-content:space-between; margin-bottom:15px; font-size:0.9em; color:#555;">
                                    <span><strong>Context:</strong> {arrow_txt}</span>
                                </div>
                                <div style="margin-bottom:15px;">
                                    <span class="metric-label">Observation</span><br>
                                    <ul>
                                        <li>{"</li><li>".join(obs)}</li>
                                        <li>Contributes to sustained structural pressure</li>
                                    </ul>
                                </div>
                                <div>
                                    <span class="metric-label">Inquiry</span><br>
                                    <span style="font-size:0.95em; color:#444;">
                                    Do I want the audience to stay under pressure this long? Is this repetition intentional?
                                    </span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

            else:
                # Technical View
                st.subheader("Technical Analysis")
                st.write(f"**Total Scenes:** {len(scenes)}")
                
                if messages:
                    for m in messages:
                        st.text(f"• {m}")
                else:
                    st.text("• No strain detected.")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.caption("RAW EFFORT")
                    st.line_chart(effort)
                with col2:
                    st.caption("ACCUMULATED STRAIN")
                    st.line_chart(decayed)

        except ValueError as ve:
             st.error(f"Validation Error: {ve}")
        except Exception as e:
             st.error(f"Error: {e}")
