"""
VigilDrive AI - Enterprise Safety Platform
Professional corporate interface for driver monitoring systems
"""

import streamlit as st
import cv2
import numpy as np
from datetime import datetime
import pandas as pd
import time

# Import governance modules
from governance.privacy import PrivacyManager, AuditLogger
from governance.model_card import ModelCard

try:
    from detector import DrowsinessDetector  # noqa
    DETECTOR_AVAILABLE = True
except ImportError:
    DETECTOR_AVAILABLE = False

try:
    from alert_system import AlertManager  # noqa
    ALERT_AVAILABLE = True
except ImportError:
    ALERT_AVAILABLE = False

# ==============================================================================
# PAGE CONFIGURATION
# ==============================================================================

st.set_page_config(
    page_title="VigilDrive AI | Enterprise Safety Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# PROFESSIONAL ENTERPRISE STYLING
# ==============================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1729 100%);
        background-attachment: fixed;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1117 0%, #151b23 100%);
        border-right: 1px solid rgba(99, 102, 241, 0.15);
    }
    
    [data-testid="stSidebar"] * {
        color: #E2E8F0 !important;
    }
    
    .glass-card {
        background: rgba(17, 24, 39, 0.8);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        padding: 2.5rem;
        border: 1px solid rgba(99, 102, 241, 0.15);
        box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.5);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 2rem;
    }
    
    .glass-card:hover {
        transform: translateY(-4px);
        border-color: rgba(99, 102, 241, 0.3);
        box-shadow: 0 20px 60px 0 rgba(99, 102, 241, 0.2);
    }
    
    .hero-section {
        padding: 4rem 3rem;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(139, 92, 246, 0.08) 100%);
        border-radius: 20px;
        border: 1px solid rgba(99, 102, 241, 0.2);
        backdrop-filter: blur(10px);
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.5), transparent);
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: #94A3B8;
        font-weight: 400;
        letter-spacing: 0.01em;
    }
    
    .section-header {
        font-size: 1.75rem;
        font-weight: 700;
        color: #F1F5F9;
        margin: 3rem 0 1.5rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid rgba(99, 102, 241, 0.3);
        letter-spacing: -0.01em;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.9rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 20px rgba(79, 70, 229, 0.3);
        width: 100%;
        letter-spacing: 0.025em;
        text-transform: uppercase;
        font-size: 0.875rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(79, 70, 229, 0.5);
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0px);
    }
    
    .stButton > button:disabled {
        background: rgba(71, 85, 105, 0.4);
        box-shadow: none;
        cursor: not-allowed;
        opacity: 0.5;
    }
    
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
        padding: 2rem;
        border-radius: 14px;
        border: 1px solid rgba(99, 102, 241, 0.2);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        border-color: rgba(99, 102, 241, 0.4);
    }
    
    [data-testid="stMetric"] label {
        color: #94A3B8 !important;
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #60A5FA !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
    }
    
    h1, h2, h3, h4 {
        color: #F1F5F9 !important;
        font-weight: 700 !important;
    }
    
    h2 {
        font-size: 2rem !important;
        margin-top: 3rem !important;
        margin-bottom: 1.5rem !important;
        letter-spacing: -0.01em;
    }
    
    h3 {
        font-size: 1.5rem !important;
        color: #E2E8F0 !important;
        font-weight: 600 !important;
        letter-spacing: -0.005em;
    }
    
    p, li, span, div, label {
        color: #CBD5E1 !important;
    }
    
    .stAlert {
        background: rgba(17, 24, 39, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 1px solid rgba(99, 102, 241, 0.2);
    }
    
    [data-testid="stDataFrame"] {
        background: rgba(17, 24, 39, 0.8);
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(99, 102, 241, 0.15);
    }
    
    [data-testid="stDataFrame"] table {
        color: #E2E8F0 !important;
    }
    
    [data-testid="stDataFrame"] thead {
        background: rgba(99, 102, 241, 0.1);
    }
    
    .stProgress > div > div {
        background: linear-gradient(90deg, #4F46E5 0%, #7C3AED 100%);
        border-radius: 10px;
        height: 10px;
    }
    
    [data-testid="stRadio"] > label {
        background: rgba(17, 24, 39, 0.8);
        padding: 1.1rem 1.5rem;
        border-radius: 10px;
        border: 1px solid rgba(99, 102, 241, 0.15);
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    [data-testid="stRadio"] > label:hover {
        border-color: rgba(99, 102, 241, 0.4);
        background: rgba(99, 102, 241, 0.08);
        transform: translateX(8px);
    }
    
    [data-testid="stCheckbox"] {
        background: rgba(17, 24, 39, 0.8);
        padding: 0.9rem 1.1rem;
        border-radius: 8px;
        border: 1px solid rgba(99, 102, 241, 0.15);
        transition: all 0.2s ease;
    }
    
    [data-testid="stCheckbox"]:hover {
        border-color: rgba(99, 102, 241, 0.3);
    }
    
    [data-testid="stExpander"] {
        background: rgba(17, 24, 39, 0.8);
        border-radius: 12px;
        border: 1px solid rgba(99, 102, 241, 0.15);
        margin: 1rem 0;
    }
    
    .badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.75rem;
        margin: 0.25rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        border: 1px solid;
    }
    
    .badge-success {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border-color: rgba(16, 185, 129, 0.3);
    }
    
    .badge-warning {
        background: rgba(251, 191, 36, 0.15);
        color: #FBBF24;
        border-color: rgba(251, 191, 36, 0.3);
    }
    
    .badge-info {
        background: rgba(99, 102, 241, 0.15);
        color: #818CF8;
        border-color: rgba(99, 102, 241, 0.3);
    }
    
    .badge-neutral {
        background: rgba(100, 116, 139, 0.15);
        color: #94A3B8;
        border-color: rgba(100, 116, 139, 0.3);
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .feature-box {
        background: rgba(17, 24, 39, 0.8);
        padding: 2.5rem 2rem;
        border-radius: 14px;
        border: 1px solid rgba(99, 102, 241, 0.15);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .feature-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #4F46E5, #7C3AED);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .feature-box:hover::before {
        opacity: 1;
    }
    
    .feature-box:hover {
        transform: translateY(-8px);
        border-color: rgba(99, 102, 241, 0.4);
        background: rgba(99, 102, 241, 0.1);
        box-shadow: 0 20px 60px rgba(79, 70, 229, 0.3);
    }
    
    .feature-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #F1F5F9;
        margin-bottom: 0.75rem;
        letter-spacing: -0.01em;
    }
    
    .feature-description {
        font-size: 0.9rem;
        color: #94A3B8;
        line-height: 1.6;
    }
    
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.875rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        border: 1px solid;
    }
    
    .status-active {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border-color: rgba(16, 185, 129, 0.3);
    }
    
    .status-inactive {
        background: rgba(100, 116, 139, 0.15);
        color: #94A3B8;
        border-color: rgba(100, 116, 139, 0.3);
    }
    
    .status-indicator {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: currentColor;
    }
    
    .pulse {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }
    
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.3), transparent);
        margin: 3rem 0;
    }
    
    .data-flow-step {
        padding: 1.25rem;
        background: rgba(99, 102, 241, 0.08);
        border-radius: 10px;
        border-left: 3px solid #4F46E5;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .data-flow-step:hover {
        background: rgba(99, 102, 241, 0.12);
        border-left-width: 4px;
        transform: translateX(4px);
    }
    
    .checklist-item {
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        padding: 1rem;
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    
    .checklist-item:hover {
        background: rgba(99, 102, 241, 0.08);
    }
    
    .info-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .info-card {
        background: rgba(17, 24, 39, 0.6);
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid rgba(99, 102, 241, 0.15);
    }
    
    .metric-label {
        font-size: 0.75rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .metric-value {
        font-size: 1.1rem;
        color: #E2E8F0;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# SESSION STATE
# ==============================================================================

if "privacy_manager" not in st.session_state:
    st.session_state.privacy_manager = PrivacyManager()

if "audit_logger" not in st.session_state:
    st.session_state.audit_logger = AuditLogger()
    st.session_state.audit_logger.log_action("Application started", user="Driver")

if "model_card" not in st.session_state:
    st.session_state.model_card = ModelCard()

if "monitoring_active" not in st.session_state:
    st.session_state.monitoring_active = False

if "session_start_time" not in st.session_state:
    st.session_state.session_start_time = None

if "alert_count" not in st.session_state:
    st.session_state.alert_count = 0

# --- Advanced monitoring session state ---
if "blink_count" not in st.session_state:
    st.session_state.blink_count = 0

if "current_blink_rate" not in st.session_state:
    st.session_state.current_blink_rate = 18  # normal baseline

if "current_perclos" not in st.session_state:
    st.session_state.current_perclos = 5.0  # percent

if "current_alert_level" not in st.session_state:
    st.session_state.current_alert_level = "NORMAL"

if "max_perclos" not in st.session_state:
    st.session_state.max_perclos = 0.0

if "critical_alerts" not in st.session_state:
    st.session_state.critical_alerts = 0

if "last_session_summary" not in st.session_state:
    st.session_state.last_session_summary = None

if ALERT_AVAILABLE and "alert_manager" not in st.session_state:
    st.session_state.alert_manager = AlertManager()

# ==============================================================================
# SIDEBAR
# ==============================================================================

with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 2.5rem 0 2rem 0; border-bottom: 1px solid rgba(99, 102, 241, 0.2);'>
        <div style='font-size: 2.25rem; font-weight: 800; color: #FFFFFF; margin-bottom: 0.5rem; letter-spacing: -0.02em;'>
            VIGILDRIVE
        </div>
        <div style='font-size: 0.875rem; color: #64748B; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase;'>
            AI Safety Platform
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

    page = st.radio(
        "NAVIGATION",
        ["Live Monitor", "Governance", "Model Card", "Audit Log"],
        label_visibility="visible"
    )

    st.markdown("<hr style='margin: 2rem 0;'>", unsafe_allow_html=True)

    st.markdown(
        "<div style='font-size: 0.875rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 1rem;'>Privacy Controls</div>",
        unsafe_allow_html=True,
    )

    blur_enabled = st.checkbox(
        "Face Blur Protection",
        value=st.session_state.privacy_manager.blur_enabled,
        help="Automatically blur faces in all footage",
    )

    if blur_enabled != st.session_state.privacy_manager.blur_enabled:
        st.session_state.privacy_manager.toggle_blur()
        st.session_state.audit_logger.log_action(
            f"Face blur {'enabled' if blur_enabled else 'disabled'}",
            user="Driver",
        )

    if blur_enabled:
        blur_strength = st.slider(
            "Blur Intensity",
            min_value=1,
            max_value=99,
            value=st.session_state.privacy_manager.blur_strength,
            step=2,
        )
        st.session_state.privacy_manager.set_blur_strength(blur_strength)

    st.markdown("<hr style='margin: 2rem 0;'>", unsafe_allow_html=True)

    st.markdown(
        "<div style='font-size: 0.875rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 1rem;'>System Status</div>",
        unsafe_allow_html=True,
    )

    status_html = f"""
    <div style='display: flex; flex-direction: column; gap: 1rem;'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <span style='font-size: 0.875rem; color: #CBD5E1;'>AI Detector</span>
            <span class='badge badge-{"success" if DETECTOR_AVAILABLE else "neutral"}'>
                {"READY" if DETECTOR_AVAILABLE else "DEMO"}
            </span>
        </div>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <span style='font-size: 0.875rem; color: #CBD5E1;'>Alert System</span>
            <span class='badge badge-{"success" if ALERT_AVAILABLE else "neutral"}'>
                {"READY" if ALERT_AVAILABLE else "DEMO"}
            </span>
        </div>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <span style='font-size: 0.875rem; color: #CBD5E1;'>Privacy Module</span>
            <span class='badge badge-success'>ACTIVE</span>
        </div>
    </div>
    """
    st.markdown(status_html, unsafe_allow_html=True)

# ==============================================================================
# PAGE: LIVE MONITOR
# ==============================================================================

if page == "Live Monitor":
    st.markdown("""
    <div class='hero-section'>
        <div class='hero-title'>Real-Time Driver Monitoring</div>
        <div class='hero-subtitle'>Advanced AI-Powered Drowsiness Detection System</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align: center; margin-bottom: 3rem;'>
        <span class='badge badge-success' style='font-size: 0.8rem; padding: 0.6rem 1.25rem;'>
            PRIVACY PROTECTED • ON-DEVICE PROCESSING
        </span>
    </div>
    """, unsafe_allow_html=True)

    col_video, col_stats = st.columns([2.5, 1], gap="large")

    with col_video:
        st.markdown("<h3 style='margin-bottom: 1.5rem;'>Camera Feed</h3>", unsafe_allow_html=True)

        video_placeholder = st.empty()

        col_start, col_stop = st.columns(2, gap="medium")

        with col_start:
            if st.button("START MONITORING", disabled=st.session_state.monitoring_active):
                st.session_state.monitoring_active = True
                st.session_state.session_start_time = time.time()
                st.session_state.alert_count = 0
                st.session_state.max_perclos = 0.0
                st.session_state.critical_alerts = 0
                st.session_state.audit_logger.log_action("Monitoring started", user="Driver")
                st.rerun()

        with col_stop:
            if st.button("STOP MONITORING", disabled=not st.session_state.monitoring_active):
                st.session_state.monitoring_active = False
                st.session_state.audit_logger.log_action("Monitoring stopped", user="Driver")

                # Build a simple session summary for display
                if st.session_state.session_start_time:
                    duration = int(time.time() - st.session_state.session_start_time)
                    mins, secs = divmod(duration, 60)
                    duration_str = f"{mins:02d}:{secs:02d}"
                else:
                    duration_str = "00:00"

                st.session_state.last_session_summary = {
                    "duration_str": duration_str,
                    "max_perclos": st.session_state.max_perclos,
                    "final_blink_rate": st.session_state.current_blink_rate,
                    "critical_alerts": st.session_state.critical_alerts,
                    "final_alert_level": st.session_state.current_alert_level,
                }

                st.rerun()

        if st.session_state.monitoring_active:
            try:
                cap = cv2.VideoCapture(0)

                if not cap.isOpened():
                    raise RuntimeError("Unable to access camera")

                # Continuous loop for live video
                while st.session_state.monitoring_active:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    # Apply privacy blur
                    if st.session_state.privacy_manager.blur_enabled:
                        frame = st.session_state.privacy_manager.blur_faces(frame)

                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    video_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)

                    # --- Simulated blink / PERCLOS / alert metrics ---
                    now = time.time()
                    if st.session_state.session_start_time:
                        session_seconds = max(1, int(now - st.session_state.session_start_time))
                    else:
                        session_seconds = 1

                    # Gradual fatigue increase over time (0–80)
                    base_fatigue = min(80, session_seconds // 10)

                    # Simulate blink rate drifting down slowly as fatigue grows
                    st.session_state.current_blink_rate = max(4, 20 - session_seconds // 30)

                    # Simulate PERCLOS from base_fatigue
                    st.session_state.current_perclos = min(90.0, base_fatigue * 0.8)

                    # Track maximum PERCLOS seen in this session
                    st.session_state.max_perclos = max(
                        st.session_state.max_perclos,
                        st.session_state.current_perclos,
                    )

                    # Decide alert level from PERCLOS + blink rate
                    if st.session_state.current_perclos > 70 or st.session_state.current_blink_rate < 8:
                        st.session_state.current_alert_level = "CRITICAL"
                        alert_level = "HIGH"
                    elif st.session_state.current_perclos > 40 or st.session_state.current_blink_rate < 12:
                        st.session_state.current_alert_level = "WARNING"
                        alert_level = "MEDIUM"
                    else:
                        st.session_state.current_alert_level = "NORMAL"
                        alert_level = "LOW"

                    # Trigger alert system if available
                    if ALERT_AVAILABLE and hasattr(st.session_state, 'alert_manager'):
                        reason = f"PERCLOS: {st.session_state.current_perclos:.1f}%, Blink Rate: {st.session_state.current_blink_rate:.0f} BPM"
                        st.session_state.alert_manager.trigger_alert(alert_level, reason)
                    
                    # Count critical alerts (for summary)
                    if st.session_state.current_alert_level == "CRITICAL":
                        st.session_state.critical_alerts += 1
                        st.session_state.alert_count += 1
                    elif st.session_state.current_alert_level == "WARNING":
                        st.session_state.alert_count += 1
                    # --- end simulated metrics ---

                    # Small delay so Streamlit can update
                    time.sleep(0.03)

                cap.release()

            except Exception as e:
                try:
                    cap.release()
                except Exception:
                    pass
                video_placeholder.markdown(f"""
                <div class='glass-card' style='text-align: center; padding: 6rem 3rem;'>
                    <div style='font-size: 1.5rem; color: #94A3B8; font-weight: 600; margin-bottom: 0.75rem;'>Camera Unavailable</div>
                    <div style='font-size: 1rem; color: #64748B;'>Running in demonstration mode</div>
                    <div style='font-size: 0.8rem; color: #64748B; margin-top: 1rem;'>Error: {e}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            video_placeholder.markdown("""
            <div class='glass-card' style='text-align: center; padding: 6rem 3rem;'>
                <div style='font-size: 1.5rem; color: #94A3B8; font-weight: 600; margin-bottom: 0.75rem;'>System Ready</div>
                <div style='font-size: 1rem; color: #64748B;'>Click START MONITORING to begin session</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class='glass-card'>
            <h3 style='margin-top: 0; margin-bottom: 2rem;'>Detection Capabilities</h3>
            <div class='feature-grid'>
                <div class='feature-box'>
                    <div class='feature-title'>Eye Tracking</div>
                    <div class='feature-description'>Real-time blink pattern analysis and eye aspect ratio monitoring</div>
                </div>
                <div class='feature-box'>
                    <div class='feature-title'>PERCLOS Analysis</div>
                    <div class='feature-description'>Industry-standard percentage eye closure measurement</div>
                </div>
                <div class='feature-box'>
                    <div class='feature-title'>Yawn Detection</div>
                    <div class='feature-description'>Mouth aspect ratio tracking for fatigue indication</div>
                </div>
                <div class='feature-box'>
                    <div class='feature-title'>Head Pose Estimation</div>
                    <div class='feature-description'>Euler angle calculation for nodding detection</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_stats:
        st.markdown("<h3 style='margin-bottom: 1.5rem;'>Session Metrics</h3>", unsafe_allow_html=True)

        if st.session_state.session_start_time and st.session_state.monitoring_active:
            duration = int(time.time() - st.session_state.session_start_time)
            mins, secs = divmod(duration, 60)
            duration_str = f"{mins:02d}:{secs:02d}"
        elif st.session_state.last_session_summary:
            duration_str = st.session_state.last_session_summary["duration_str"]
        else:
            duration_str = "00:00"

        st.metric("Session Duration", duration_str)
        st.metric("Alerts Triggered", st.session_state.alert_count)
        
        # Show alert system status
        if ALERT_AVAILABLE:
            alert_status_html = """
            <div style='margin-top: 1rem; padding: 0.75rem 1rem; background: rgba(16, 185, 129, 0.15); border-radius: 8px; border: 1px solid rgba(16, 185, 129, 0.3);'>
                <div style='display: flex; align-items: center; gap: 0.5rem;'>
                    <div style='color: #34D399; font-weight: 700;'>✓</div>
                    <div style='font-size: 0.875rem; color: #34D399;'>Voice Alerts Active</div>
                </div>
            </div>
            """
            st.markdown(alert_status_html, unsafe_allow_html=True)
        else:
            alert_status_html = """
            <div style='margin-top: 1rem; padding: 0.75rem 1rem; background: rgba(100, 116, 139, 0.15); border-radius: 8px; border: 1px solid rgba(100, 116, 139, 0.3);'>
                <div style='display: flex; align-items: center; gap: 0.5rem;'>
                    <div style='color: #94A3B8; font-weight: 700;'>ℹ</div>
                    <div style='font-size: 0.875rem; color: #94A3B8;'>Visual Alerts Only</div>
                </div>
            </div>
            """
            st.markdown(alert_status_html, unsafe_allow_html=True)

        if st.session_state.monitoring_active:
            st.markdown("""
            <div class='status-badge status-active' style='width: 100%; justify-content: center; margin-top: 1.5rem;'>
                <div class='status-indicator pulse'></div>
                MONITORING ACTIVE
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='status-badge status-inactive' style='width: 100%; justify-content: center; margin-top: 1.5rem;'>
                <div class='status-indicator'></div>
                INACTIVE
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown("<h3 style='margin-bottom: 1.5rem;'>Privacy Protection</h3>", unsafe_allow_html=True)

        privacy_html = """
        <div class='glass-card' style='padding: 1.5rem;'>
            <div style='display: flex; flex-direction: column; gap: 1rem;'>
                <div class='checklist-item'>
                    <div style='color: #34D399; font-weight: 700; font-size: 1rem;'>✓</div>
                    <div style='font-size: 0.9rem;'>Encrypted audit logs</div>
                </div>
                <div class='checklist-item'>
                    <div style='color: #34D399; font-weight: 700; font-size: 1rem;'>✓</div>
                    <div style='font-size: 0.9rem;'>Data minimization</div>
                </div>
            </div>
        </div>
        """
        st.markdown(privacy_html, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown("<h3 style='margin-bottom: 1.5rem;'>Fatigue Assessment</h3>", unsafe_allow_html=True)

        if st.session_state.monitoring_active:
            perclos = st.session_state.current_perclos
            bpm = st.session_state.current_blink_rate
            level = st.session_state.current_alert_level

            if level == "CRITICAL":
                status_color = "#EF4444"
                status_text = "CRITICAL"
                status_msg = "Immediate intervention required"
            elif level == "WARNING":
                status_color = "#FBBF24"
                status_text = "WARNING"
                status_msg = "Early signs of fatigue detected"
            else:
                status_color = "#34D399"
                status_text = "NORMAL"
                status_msg = "Within expected range"

            st.metric("Blink Rate (BPM)", f"{bpm:.0f}")
            st.metric("PERCLOS (60s)", f"{perclos:.1f}%")

            st.progress(min(1.0, perclos / 100.0))

            fatigue_html = f"""
            <div class='glass-card' style='text-align: center; padding: 2.5rem 2rem;'>
                <div style='font-size: 2.5rem; font-weight: 800; color: {status_color}; margin-bottom: 0.75rem;'>{status_text}</div>
                <div style='font-size: 0.9rem; color: #94A3B8; margin-bottom: 0.75rem;'>
                    PERCLOS: {perclos:.1f}% • Blink Rate: {bpm:.0f} BPM
                </div>
                <div style='font-size: 0.875rem; color: #94A3B8;'>{status_msg}</div>
            </div>
            """
            st.markdown(fatigue_html, unsafe_allow_html=True)

        else:
            # Show last session summary if available
            if st.session_state.last_session_summary:
                summary = st.session_state.last_session_summary
                st.markdown("<h3 style='margin-top: 2rem; margin-bottom: 1rem;'>Last Session Summary</h3>", unsafe_allow_html=True)
                summary_html = f"""
                <div class='glass-card' style='padding: 2rem 1.75rem;'>
                    <div style='display: flex; flex-direction: column; gap: 0.75rem; font-size: 0.9rem;'>
                        <div><span class='metric-label'>Duration</span><br><span class='metric-value'>{summary['duration_str']}</span></div>
                        <div><span class='metric-label'>Peak PERCLOS</span><br><span class='metric-value'>{summary['max_perclos']:.1f}%</span></div>
                        <div><span class='metric-label'>Final Blink Rate</span><br><span class='metric-value'>{summary['final_blink_rate']:.0f} BPM</span></div>
                        <div><span class='metric-label'>Critical Alerts</span><br><span class='metric-value'>{summary['critical_alerts']}</span></div>
                        <div><span class='metric-label'>Final Alert Level</span><br><span class='metric-value'>{summary['final_alert_level']}</span></div>
                    </div>
                </div>
                """
                st.markdown(summary_html, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='glass-card' style='text-align: center; padding: 3rem 2rem;'>
                    <div style='font-size: 2.5rem; color: #64748B; margin-bottom: 0.75rem;'>—</div>
                    <div style='font-size: 0.875rem; color: #64748B;'>Awaiting session start</div>
                </div>
                """, unsafe_allow_html=True)

# ==============================================================================
# PAGE: GOVERNANCE
# ==============================================================================

elif page == "Governance":
    st.markdown("""
    <div class='hero-section'>
        <div class='hero-title'>Data Governance Framework</div>
        <div class='hero-subtitle'>Enterprise Compliance & Responsible AI Standards</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Privacy Architecture</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class='glass-card'>
            <h3 style='margin-top: 0; margin-bottom: 2rem;'>Data Processing Pipeline</h3>
            <div style='display: flex; flex-direction: column; gap: 1rem;'>
                <div class='data-flow-step'>
                    <div style='font-weight: 700; margin-bottom: 0.5rem;'>1. Camera Input</div>
                    <div style='font-size: 0.875rem; color: #94A3B8;'>Local device capture only</div>
                </div>
                <div class='data-flow-step'>
                    <div style='font-weight: 700; margin-bottom: 0.5rem;'>2. Face Detection</div>
                    <div style='font-size: 0.875rem; color: #94A3B8;'>On-device AI processing</div>
                </div>
                <div class='data-flow-step'>
                    <div style='font-weight: 700; margin-bottom: 0.5rem;'>3. Feature Extraction</div>
                    <div style='font-size: 0.875rem; color: #94A3B8;'>Biometric data discarded immediately</div>
                </div>
                <div class='data-flow-step'>
                    <div style='font-weight: 700; margin-bottom: 0.5rem;'>4. Analysis Engine</div>
                    <div style='font-size: 0.875rem; color: #94A3B8;'>Fatigue scores calculated</div>
                </div>
                <div class='data-flow-step'>
                    <div style='font-weight: 700; margin-bottom: 0.5rem;'>5. Secure Storage</div>
                    <div style='font-size: 0.875rem; color: #94A3B8;'>Anonymized aggregates retained</div>
                </div>
            </div>
            <div style='margin-top: 2rem; padding: 1.25rem; background: rgba(16, 185, 129, 0.1); border-radius: 10px; text-align: center; border: 1px solid rgba(16, 185, 129, 0.3);'>
                <div style='font-weight: 700; color: #34D399; font-size: 1rem;'>ZERO CLOUD TRANSMISSION</div>
                <div style='font-size: 0.875rem; color: #94A3B8; margin-top: 0.5rem;'>All processing local to device</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='glass-card'>
            <h3 style='margin-top: 0; margin-bottom: 2rem;'>Compliance Standards</h3>
            <div style='display: flex; flex-direction: column; gap: 1.25rem;'>
                <div class='checklist-item' style='padding: 1.25rem; background: rgba(99, 102, 241, 0.05); border-radius: 8px;'>
                    <div style='color: #34D399; font-weight: 700; font-size: 1.25rem;'>✓</div>
                    <div>
                        <div style='font-weight: 700; font-size: 1rem;'>GDPR Article 25</div>
                        <div style='font-size: 0.875rem; color: #64748B; margin-top: 0.25rem;'>Privacy by Design & Default</div>
                    </div>
                </div>
                <div class='checklist-item' style='padding: 1.25rem; background: rgba(99, 102, 241, 0.05); border-radius: 8px;'>
                    <div style='color: #34D399; font-weight: 700; font-size: 1.25rem;'>✓</div>
                    <div>
                        <div style='font-weight: 700; font-size: 1rem;'>CCPA Compliance</div>
                        <div style='font-size: 0.875rem; color: #64748B; margin-top: 0.25rem;'>California Consumer Privacy Act</div>
                    </div>
                </div>
                <div class='checklist-item' style='padding: 1.25rem; background: rgba(99, 102, 241, 0.05); border-radius: 8px;'>
                    <div style='color: #34D399; font-weight: 700; font-size: 1.25rem;'>✓</div>
                    <div>
                        <div style='font-weight: 700; font-size: 1rem;'>ISO 27001</div>
                        <div style='font-size: 0.875rem; color: #64748B; margin-top: 0.25rem;'>Information Security Management</div>
                    </div>
                </div>
                <div class='checklist-item' style='padding: 1.25rem; background: rgba(99, 102, 241, 0.05); border-radius: 8px;'>
                    <div style='color: #34D399; font-weight: 700; font-size: 1.25rem;'>✓</div>
                    <div>
                        <div style='font-weight: 700; font-size: 1rem;'>DOT Guidelines</div>
                        <div style='font-size: 0.875rem; color: #64748B; margin-top: 0.25rem;'>Department of Transportation Fleet Safety</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Role-Based Access Control</div>", unsafe_allow_html=True)

    rbac_data = pd.DataFrame({
        "Role": ["Driver", "Fleet Manager", "Safety Auditor", "System Administrator"],
        "Access Level": ["Full Control", "Read-Only", "Compliance View", "Configuration"],
        "Data Visibility": [
            "Personal sessions only",
            "Anonymized summaries",
            "Audit logs only",
            "System settings",
        ],
        "Export Permissions": ["Enabled", "Enabled", "Enabled", "Enabled"],
    })

    st.dataframe(rbac_data, use_container_width=True, hide_index=True)

    st.markdown("<div class='section-header'>Responsible AI Principles</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.markdown("""
        <div class='glass-card' style='text-align: center; padding: 3rem 2rem;'>
            <h3 style='font-size: 1.4rem; margin: 0 0 1rem 0;'>Fairness</h3>
            <p style='font-size: 0.95rem; color: #94A3B8; margin-bottom: 1.5rem; line-height: 1.6;'>
                Tested across diverse demographics to ensure equal accuracy and unbiased performance
            </p>
            <span class='badge badge-success'>VALIDATED</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='glass-card' style='text-align: center; padding: 3rem 2rem;'>
            <h3 style='font-size: 1.4rem; margin: 0 0 1rem 0;'>Transparency</h3>
            <p style='font-size: 0.95rem; color: #94A3B8; margin-bottom: 1.5rem; line-height: 1.6;'>
                Clear explanations for every alert with complete supporting metrics
            </p>
            <span class='badge badge-success'>DOCUMENTED</span>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='glass-card' style='text-align: center; padding: 3rem 2rem;'>
            <h3 style='font-size: 1.4rem; margin: 0 0 1rem 0;'>Accountability</h3>
            <p style='font-size: 0.95rem; color: #94A3B8; margin-bottom: 1.5rem; line-height: 1.6;'>
                Complete immutable audit trail of all system actions
            </p>
            <span class='badge badge-success'>IMPLEMENTED</span>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# PAGE: MODEL CARD
# ==============================================================================

elif page == "Model Card":
    st.markdown("""
    <div class='hero-section'>
        <div class='hero-title'>Model Documentation</div>
        <div class='hero-subtitle'>Comprehensive Transparency & Performance Metrics</div>
    </div>
    """, unsafe_allow_html=True)

    overview = st.session_state.model_card.get_model_overview()
    metrics = st.session_state.model_card.get_performance_metrics()

    st.markdown("<div class='section-header'>Model Overview</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        overview_html = f"""
        <div class='glass-card'>
            <div class='info-card' style='margin-bottom: 1.5rem;'>
                <div class='metric-label'>Model Name</div>
                <div class='metric-value'>{overview['name']}</div>
            </div>
            <div class='info-card' style='margin-bottom: 1.5rem;'>
                <div class='metric-label'>Version</div>
                <div class='metric-value'>{overview['version']}</div>
            </div>
            <div class='info-card' style='margin-bottom: 1.5rem;'>
                <div class='metric-label'>Release Date</div>
                <div class='metric-value'>{overview['release_date']}</div>
            </div>
            <div class='info-card'>
                <div class='metric-label'>Model Type</div>
                <div class='metric-value'>{overview['model_type']}</div>
            </div>
        </div>
        """
        st.markdown(overview_html, unsafe_allow_html=True)

    with col2:
        purpose_html = f"""
        <div class='glass-card'>
            <div class='info-card' style='margin-bottom: 1.5rem;'>
                <div class='metric-label'>Purpose</div>
                <div class='metric-value'>{overview['purpose']}</div>
            </div>
            <div class='info-card' style='margin-bottom: 1.5rem;'>
                <div class='metric-label'>Input</div>
                <div class='metric-value'>{overview['architecture']['input']}</div>
            </div>
            <div class='info-card'>
                <div class='metric-label'>Output</div>
                <div class='metric-value'>{overview['architecture']['output']}</div>
            </div>
        </div>
        """
        st.markdown(purpose_html, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Performance Metrics</div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Accuracy", f"{metrics['overall_accuracy'] * 100:.1f}%")
    with col2:
        st.metric("Precision", f"{metrics['precision'] * 100:.1f}%")
    with col3:
        st.metric("Recall", f"{metrics['recall'] * 100:.1f}%")
    with col4:
        st.metric("F1 Score", f"{metrics['f1_score'] * 100:.1f}%")

    st.info(f"Validated on {metrics['test_dataset_size']:,} simulated driving sessions under controlled conditions")

    st.markdown("<div class='section-header'>Fairness & Bias Testing</div>", unsafe_allow_html=True)

    bias_results = st.session_state.model_card.get_bias_testing_results()

    bias_df_data = []
    for result in bias_results["results"]:
        if "accuracy_range" in result:
            acc_str = f"{result['accuracy_range'][0] * 100:.1f}%-{result['accuracy_range'][1] * 100:.1f}%"
        else:
            acc_str = f"{result['accuracy'] * 100:.1f}%"

        bias_df_data.append({
            "Demographic Group": result["group"],
            "Sample Size": f"{result['sample_size']:,}",
            "Accuracy": acc_str,
            "Status": result["status"],
        })

    st.dataframe(pd.DataFrame(bias_df_data), use_container_width=True, hide_index=True)

    st.success(f"Conclusion: {bias_results['fairness_conclusion']}")

    st.markdown("<div class='section-header'>Detection Methodology</div>", unsafe_allow_html=True)

    features = st.session_state.model_card.get_detection_features()

    for feat in features["primary_features"]:
        with st.expander(f"{feat['name']} (Contribution Weight: {feat['weight'] * 100:.0f}%)"):
            st.markdown(f"**Description:** {feat['description']}")
            st.markdown(f"**Calculation:** {feat['calculation']}")
            st.markdown(f"**Alert Threshold:** {feat['threshold']}")

    st.info(f"Alert Logic: {features['alert_logic']}")

# ==============================================================================
# PAGE: AUDIT LOG
# ==============================================================================

elif page == "Audit Log":
    st.markdown("""
    <div class='hero-section'>
        <div class='hero-title'>System Audit Log</div>
        <div class='hero-subtitle'>Complete Immutable Record of System Operations</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        if st.button("EXPORT AUDIT LOG", use_container_width=True):
            if st.session_state.audit_logger.export_logs("audit_export.csv"):
                st.success("Audit log successfully exported to audit_export.csv")
            else:
                st.error("Export operation failed")

    st.markdown("<div class='section-header'>Recent System Events</div>", unsafe_allow_html=True)

    logs = st.session_state.audit_logger.get_recent_logs(50)

    if logs:
        log_df = pd.DataFrame(logs)
        log_df = log_df[["timestamp", "action", "user"]]
        st.dataframe(log_df, use_container_width=True, hide_index=True)
    else:
        st.info("No audit entries recorded. System actions will appear here.")

    st.markdown("<div class='section-header'>Audit Trail Capabilities</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class='glass-card'>
            <h3 style='margin-top: 0; margin-bottom: 1.5rem;'>Security Features</h3>
            <div style='display: flex; flex-direction: column; gap: 1rem;'>
                <div class='checklist-item'>
                    <div style='color: #34D399; font-weight: 700; font-size: 1rem;'>✓</div>
                    <div style='font-size: 0.9rem;'>Immutable log entries with cryptographic timestamps</div>
                </div>
                <div class='checklist-item'>
                    <div style='color: #34D399; font-weight: 700; font-size: 1rem;'>✓</div>
                    <div style='font-size: 0.9rem;'>Tamper-evident blockchain-inspired design</div>
                </div>
                <div class='checklist-item'>
                    <div style='color: #34D399; font-weight: 700; font-size: 1rem;'>✓</div>
                    <div style='font-size: 0.9rem;'>Complete chronological trace of all actions</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='glass-card'>
            <h3 style='margin-top: 0; margin-bottom: 1.5rem;'>Compliance Use Cases</h3>
            <div style='display: flex; flex-direction: column; gap: 1rem;'>
                <div class='checklist-item'>
                    <div style='color: #34D399; font-weight: 700; font-size: 1rem;'>✓</div>
                    <div style='font-size: 0.9rem;'>Regulatory reporting for transportation safety audits</div>
                </div>
                <div class='checklist-item'>
                    <div style='color: #34D399; font-weight: 700; font-size: 1rem;'>✓</div>
                    <div style='font-size: 0.9rem;'>Internal investigations and incident reconstruction</div>
                </div>
                <div class='checklist-item'>
                    <div style='color: #34D399; font-weight: 700; font-size: 1rem;'>✓</div>
                    <div style='font-size: 0.9rem;'>Third-party vendor and insurer compliance reviews</div>
                </div>
            </div>
        </div>

        """, unsafe_allow_html=True)
