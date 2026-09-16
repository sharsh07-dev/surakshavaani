import streamlit as st
import requests
import json
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="SurakshaVaani Pro Console",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS FOR PREMIUM UI ---
st.markdown("""
<style>
    /* Import Modern Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background with Gradient */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #ffffff;
    }
    
    /* Header Styling */
    h1 {
        background: linear-gradient(120deg, #00f2fe 0%, #4facfe 50%, #00c6ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3.5rem !important;
        letter-spacing: -1px;
        margin-bottom: 0.5rem !important;
        text-align: center;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 10px rgba(0, 242, 254, 0.3)); }
        to { filter: drop-shadow(0 0 20px rgba(0, 242, 254, 0.6)); }
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #a8b2d1;
        margin-bottom: 2rem;
        font-weight: 300;
        letter-spacing: 0.5px;
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(0, 242, 254, 0.2);
        border: 1px solid rgba(0, 242, 254, 0.3);
    }
    
    /* Status Indicators */
    .status-safe {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.8rem;
        font-weight: 700;
        box-shadow: 0 10px 30px rgba(56, 239, 125, 0.3);
        animation: pulse-safe 2s infinite;
    }
    
    .status-danger {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.8rem;
        font-weight: 700;
        box-shadow: 0 10px 30px rgba(235, 51, 73, 0.5);
        animation: pulse-danger 1s infinite;
    }
    
    @keyframes pulse-safe {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    @keyframes pulse-danger {
        0%, 100% { transform: scale(1); box-shadow: 0 10px 30px rgba(235, 51, 73, 0.5); }
        50% { transform: scale(1.05); box-shadow: 0 15px 40px rgba(235, 51, 73, 0.8); }
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.1) 0%, rgba(0, 242, 254, 0.1) 100%);
        border: 1px solid rgba(79, 172, 254, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.2) 0%, rgba(0, 242, 254, 0.2) 100%);
        transform: translateY(-3px);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(120deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #a8b2d1;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 0.8rem 2rem;
        border-radius: 12px;
        border: none;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* File Uploader */
    .uploadedFile {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Live Feed Table */
    .feed-table {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Transcript Box */
    .transcript-box {
        background: linear-gradient(135deg, rgba(255, 193, 7, 0.1) 0%, rgba(255, 152, 0, 0.1) 100%);
        border-left: 4px solid #ffc107;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-size: 1.1rem;
        font-style: italic;
    }
    
    /* Critical Factor Tags */
    .critical-tag {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        display: inline-block;
        margin: 0.3rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(255, 65, 108, 0.4);
    }
    
    /* System Status Badge */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 20px;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        font-weight: 600;
        font-size: 0.9rem;
        animation: blink 2s infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(79, 172, 254, 0.5), transparent);
        margin: 2rem 0;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Audio Player Styling */
    audio {
        width: 100%;
        border-radius: 10px;
        filter: hue-rotate(200deg);
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1>🛡️ SurakshaVaani Pro</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Dual-Engine Threat Detection: Audio Intelligence • Tone Analysis • Keyword Recognition</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# --- MAIN LAYOUT ---
col1, col2 = st.columns([1.2, 1], gap="large")

with col1:
    st.markdown("### 🎤 Live Audio Feed Analysis")
    st.markdown("<p style='color: #a8b2d1; margin-bottom: 1.5rem;'>Upload audio clips to scan for emotional distress, screams, or critical keywords</p>", unsafe_allow_html=True)
    
    # File Uploader
    audio_file = st.file_uploader("Upload Audio Clip", type=['wav', 'mp3'], label_visibility="collapsed")
    
    if audio_file is not None:
        st.audio(audio_file)
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚨 SCAN FOR THREATS", type="primary", use_container_width=True):
            with st.spinner("🔄 Running Dual-Engine Analysis (Tone + Speech)..."):
                try:
                    # 1. CALL THE NEW API ENDPOINT
                    audio_bytes = audio_file.getvalue()
                    files = {"file": (audio_file.name, audio_bytes, "audio/wav")}
                    res = requests.post("http://127.0.0.1:8000/analyze-threat", files=files)
                    
                    if res.status_code == 200:
                        data = res.json()
                        
                        # 2. EXTRACT DATA
                        is_sos = data['sos_activated']
                        reasons = data['reasons']
                        transcript = data['transcription']
                        tone = data['tone_analysis']
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # 3. DISPLAY RESULTS - STATUS BANNER
                        if is_sos:
                            st.markdown("<div class='status-danger'>🆘 SOS TRIGGERED - IMMEDIATE RESPONSE REQUIRED</div>", unsafe_allow_html=True)
                            st.markdown("<br>", unsafe_allow_html=True)
                            for r in reasons:
                                st.markdown(f"<div class='critical-tag'>🔴 {r}</div>", unsafe_allow_html=True)
                        else:
                            st.markdown("<div class='status-safe'>✅ STATUS SAFE - NO THREATS DETECTED</div>", unsafe_allow_html=True)
                            st.markdown("<p style='text-align: center; color: #a8b2d1; margin-top: 1rem;'>No threat biomarkers detected in audio sample</p>", unsafe_allow_html=True)

                        st.markdown("<br><br>", unsafe_allow_html=True)
                        
                        # DETAILED METRICS
                        st.markdown("### 📊 Analysis Metrics")
                        m1, m2, m3 = st.columns(3)
                        
                        with m1:
                            st.markdown(f"""
                            <div class='metric-card'>
                                <div class='metric-value'>{tone['emotion']}</div>
                                <div class='metric-label'>🗣️ Tone Detected</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with m2:
                            threat_count = len(reasons) if is_sos else 0
                            st.markdown(f"""
                            <div class='metric-card'>
                                <div class='metric-value'>{threat_count}</div>
                                <div class='metric-label'>⚠️ Threat Factors</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with m3:
                            confidence_pct = tone['confidence'] * 100
                            st.markdown(f"""
                            <div class='metric-card'>
                                <div class='metric-value'>{confidence_pct:.1f}%</div>
                                <div class='metric-label'>🤖 AI Confidence</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # TRANSCRIPT BOX
                        st.markdown(f"""
                        <div class='transcript-box'>
                            <strong>📝 Transcription:</strong> "{transcript}"
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # RAW DATA EXPANDER
                        with st.expander("🔧 View System Telemetry"):
                            st.json(data)

                    else:
                        st.error(f"⚠️ Server Error {res.status_code}: {res.text}")
                        
                except Exception as e:
                    st.error(f"❌ Connection Failed. Is the server running?\n\nError: {e}")
    else:
        st.info("👆 Upload an audio file to begin threat analysis")

with col2:
    st.markdown("### 📡 Live Operator Feed")
    st.markdown("<p style='color: #a8b2d1; margin-bottom: 1.5rem;'>Real-time monitoring dashboard</p>", unsafe_allow_html=True)
    
    # System Status Badge
    current_time = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"<div class='status-badge'>🟢 SYSTEM ACTIVE • {current_time}</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Enhanced Feed Table
    st.markdown("""
    <div class='feed-table'>
    
    | ID | Time | Threat | Transcription | Status |
    |:---:|:---:|:---:|:---|:---:|
    | **#901** | 10:45:01 | 🔴 **SCREAM** | *[Unintelligible]* | 🚓 Dispatched |
    | **#902** | 10:45:15 | 🟡 KEYWORD | "Please help me" | 📞 Connecting |
    | **#903** | 10:46:00 | 🟢 NEUTRAL | "Just testing" | ✅ Ignored |
    | **#904** | 10:46:32 | 🔴 **ANGER** | "Get away from me!" | 🚨 Alert Sent |
    | **#905** | 10:47:10 | 🟢 NEUTRAL | "Hello there" | ✅ Ignored |
    
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # System Info
    st.markdown("""
    <div class='glass-card'>
        <h4 style='color: #4facfe; margin-bottom: 1rem;'>⚙️ System Configuration</h4>
        <p style='color: #a8b2d1; line-height: 1.8;'>
        <strong>Sampling Rate:</strong> 16 kHz<br>
        <strong>Detection Engines:</strong> 2 (Tone + Speech)<br>
        <strong>Model Version:</strong> v2.1.0<br>
        <strong>Uptime:</strong> 99.8%<br>
        <strong>Threats Detected:</strong> 127 (Last 24h)
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a8b2d1; font-size: 0.9rem;'>SurakshaVaani Pro Console • Powered by Advanced AI • Real-time Threat Detection</p>", unsafe_allow_html=True)