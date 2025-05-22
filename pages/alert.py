import streamlit as st
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import time
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os
from dotenv import load_dotenv
import json
load_dotenv()

# Set page config
st.set_page_config(page_title="Wearable Health Monitoring - Alert", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    /* Reset default margins and padding for the entire app */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"] {
        margin: 0 !important;
        padding: 0 !important;
        overflow: auto !important;
    }

    .stApp {
        background: linear-gradient(135deg, #0d1321, #1b263b);
        color: #e0e0e0;
        font-family: 'Orbitron', sans-serif;
        min-height: 100vh;
        overflow: auto;
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    /* Particle background effect */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgogIDxkZWZzPgogICAgPGZpbHRlciBpZD0iZ2xvd0ZpbHRlciI+CiAgICAgIDxmZUdhdXNzaWFuQmx1ciBpbj0iU291cmNlR3JhcGhpYyIgc3RkRGV2aWF0aW9uPSIyIiAvPgogICAgPC9maWx0ZXIAogIDwvZGVmcz4KICA8ZyBmaWx0ZXI9InVybCgjZ2xvd0ZpbHRlcikiPgogICAgPHBhdGggZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMDBmN2ZmIiBzdHJva2Utd2lkdGg9IjEiIGQ9Ik0wLDBoMjAwMHYxMjAwSDB6IiAvPgogICAgPGNpcmNsZSBjeD0iMTAwIiBjeT0iMTAwIiByPSIzIiBmaWxsPSIjMDBmN2ZmIiBvcGFjaXR5PSIwLjciIGFuaW1hdGVNb3Rpb24gZHVyPSIzMHMiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBiZWdpbj0iMHMiIHBhdGhTPSJNMTAwLDEwMCBDMzAwLDMwMCw1MDAsMTAwLDcwMCwzMDBDMTAwMCwxMDAsMTIwMCwzMDAsMTUwMCwxMDBDMTgwMCwzMDAsMjAwMCwxMDAsMjAwMCwxMjAwQzE1MDAsOTAwLDEyMDAsMTIwMCwxMDAwLDkwMEM3MDAsMTIwMCw1MDAsOTAwLDMwMCwxMjAwQzEwMCw5MDAsMCwxMjAwLDAsMTAwWiIgLz4KICAgIDxjaXJjbGUgY3g9IjUwMCIgY3k9IjUwMCIgcj0iMiIgZmlsbD0iI2ZmMDBlNiIgb3BhY2l0eT0iMC41IiBhbmltYXRlTW90aW9uIGR1cj0iMjBzIiByZXBlYXRDb3VudD0iaW5kZWZpbml0ZSIgYmVnaW49IjVzIiBwYXRoPSJNNTAwLDUwMCBDNzAwLDMwMCw5MDAsNTAwLDExMDAsMzAwQzEzMDAsNTAwLDE1MDAsMzAwLDE3MDAsNTAwQzE5MDAsNzAwLDE3MDAsOTAwLDE1MDAsMTEwMEMxMzAwLDkwMCwxMTAwLDExMDAsOTAwLDkwMEM3MDAsMTEwMCw1MDAsOTAwLDMwMCwxMTAwQzEwMCw5MDAsMzAwLDcxMCw1MDAsNTAwWiIgLz4KICA8L2c+Cjwvc3ZnPg==');
        pointer-events: none;
        z-index: 0;
    }

    [data-testid="stSidebar"] {
        display: none !important;
    }

    /* Navbar styling */
    .nav-bar {
        background: rgba(13, 19, 33, 0.95);
        backdrop-filter: blur(10px);
        padding: 1rem;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 1000;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    }

    .nav-menu {
        display: flex !important;
        justify-content: center !important;
        gap: 2rem !important;
    }

    .nav-menu a {
        color: #ffffff !important;
        text-decoration: none !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.2rem !important;
        border-radius: 25px !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }

    .nav-menu a:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 5px 15px rgba(0, 100, 255, 0.4) !important;
    }

    .nav-menu a::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 2px;
        background: #00d4ff;
        transform: scaleX(0);
        transform-origin: right;
        transition: transform 0.3s ease;
    }

    .nav-menu a:hover::after {
        transform: scaleX(1);
        transform-origin: left;
    }

    .animated-title {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #00f7ff, #ff00e6, #39ff14);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 60px;
        font-weight: bold;
        animation: pulse 3s ease-in-out infinite alternate, glow 2s ease-in-out infinite alternate;
        text-shadow: 0 0 20px rgba(0, 247, 255, 0.7);
    }

    .alert-box {
        background: #ff4b4b;
        padding: 10px;
        border-radius: 5px;
        color: #ffffff;
        margin-bottom: 10px;
        border: 2px solid #ff0000;
        box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
    }

    .safe-box {
        background: #4caf50;
        padding: 10px;
        border-radius: 5px;
        color: #ffffff;
        margin-bottom: 10px;
        border: 2px solid #39ff14;
        box-shadow: 0 0 10px rgba(57, 255, 20, 0.5);
    }

    .recommendation-box {
        background: linear-gradient(145deg, #1b263b, #2a3b5b);
        padding: 15px;
        border-radius: 10px;
        color: #e0e0e0;
        margin-bottom: 10px;
        border: 2px solid #00f7ff;
        box-shadow: 0 0 15px rgba(0, 247, 255, 0.7);
    }

    .recommendation-box:hover {
        border-color: #ff00e6;
        transform: translateY(-3px);
    }

    .content {
        margin-top: 80px; /* Adjusted for fixed navbar */
        width: 100%;
        padding: 2rem;
        z-index: 1;
    }

    @media (max-width: 768px) {
        .nav-menu {
            flex-wrap: wrap !important;
            gap: 1rem !important;
        }
        .content {
            padding: 1rem !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Hide Sidebar
hide_sidebar = """
    <style>
        [data-testid="stSidebar"] {display: none;}
        [data-testid="stToolbar"] {right: 2rem;}
        .css-18ni7ap {padding-top: 3rem;}
    </style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)

# Navigation Bar
st.markdown("<div class='nav-bar'><div class='nav-menu'>", unsafe_allow_html=True)
pages = {
    "Home": "pages/home.py",
    "Dashboard": "pages/dashboard.py",
    "Alert": "pages/alert.py",
    "About Us": "pages/about.py",  # Changed "About" to "About Us" for consistency
    "Feedback": "pages/feedback.py"
}
selected = option_menu(None, list(pages.keys()), 
                       menu_icon="cast", default_index=2, orientation="horizontal",
                       styles={
                           "container": {"padding": "0", "background-color": "transparent"},
                           "nav-link": {"font-size": "18px", "text-align": "center", "margin": "0 10px", "color": "#e0e0e0"},
                           "nav-link-selected": {"background": "linear-gradient(45deg, #00f7ff, #ff00e6)", "color": "#ffffff"},
                       })
st.markdown("</div></div>", unsafe_allow_html=True)

# Navigation Logic
if selected == "Home":
    try:
        st.switch_page("pages/home.py")
    except Exception as e:
        st.error("Home page not found. Please ensure 'pages/home.py' exists.")
elif selected == "Dashboard":
    try:
        st.switch_page("pages/dashboard.py")
    except Exception as e:
        st.error("Dashboard page not found. Please ensure 'pages/dashboard.py' exists.")
elif selected == "Alert":
    pass
elif selected == "About Us":
    try:
        st.switch_page("pages/about.py")
    except Exception as e:
        st.error("About Us page not found. Please ensure 'pages/about.py' exists.")
elif selected == "Feedback":
    try:
        st.switch_page("pages/feedback.py")
    except Exception as e:
        st.error("Feedback page not found. Please ensure 'pages/feedback.py' exists.")

# Function to get heart rate from session state
def get_heart_rate():
    if 'latest_heart_rate' in st.session_state:
        heart_rate = st.session_state.latest_heart_rate
        if heart_rate is not None and pd.notna(heart_rate):
            return heart_rate
    st.warning("No heart rate data available from Dashboard. Using default value.")
    return 105  # Fallback value

# Function to get health recommendations
def get_health_recommendations(heart_rate):
    if heart_rate < 60:
        status = "Low Heart Rate"
        recommendations = [
            "Your heart rate is lower than normal (bradycardia).",
            "Rest and avoid strenuous activity.",
            "Consult a healthcare professional if you feel dizzy or fatigued.",
            "Monitor your symptoms and seek immediate help if they worsen."
        ]
    elif 60 <= heart_rate <= 100:
        status = "Normal Heart Rate"
        recommendations = [
            "Your heart rate is within the normal range.",
            "Maintain a balanced diet and regular exercise.",
            "Stay hydrated and get adequate sleep.",
            "Continue monitoring your health metrics."
        ]
    else:
        status = "High Heart Rate"
        recommendations = [
            "Your heart rate is higher than normal (tachycardia).",
            "Rest in a calm environment and avoid caffeine or stimulants.",
            "Stay hydrated and practice deep breathing exercises.",
            "Seek medical attention if you experience chest pain or shortness of breath."
        ]
    return status, recommendations

# Function to send email alert
def send_email_alert(heart_rate, user_email):
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        
        # st.write(f"Attempting to send email to {user_email}...")
        # st.write(f"Sender Email: {sender_email}")
        # st.write(f"Sender Password: {'*' * len(sender_password or '')}")
        
        if not sender_email or not sender_password:
            return "Email configuration missing. Please set SENDER_EMAIL and SENDER_PASSWORD in .env file."
        
        subject = "Health Alert: Abnormal Heart Rate Detected"
        body = f"""
        Dear User,

        Your wearable health monitoring device has detected an abnormal heart rate of {heart_rate} BPM at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.
        Please consult a healthcare professional if you experience any symptoms.

        Regards,
        Wearable Health Monitoring Team
        """
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = user_email
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # st.write("Connecting to SMTP server...")
            server.starttls()
            # st.write("TLS started...")
            server.login(sender_email, sender_password)
            # st.write("Logged in to SMTP server...")
            server.send_message(msg)
            st.write("Email sent successfully!")
        
        return f"Email sent to {user_email}: Heart rate alert ({heart_rate} BPM)"
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return f"Failed to send email to {user_email}: Heart rate alert ({heart_rate} BPM)"# Initialize session state
if 'heart_rate_history' not in st.session_state:
    st.session_state.heart_rate_history = []
if 'timestamps' not in st.session_state:
    st.session_state.timestamps = []
if 'alerts' not in st.session_state:
    st.session_state.alerts = []
if 'last_email_sent' not in st.session_state:
    st.session_state.last_email_sent = None

# Main app
st.markdown("<div class='content'>", unsafe_allow_html=True)

# Animated centered title
st.markdown("<h1 class='animated-title'>🩺 Wearable Health Monitoring Alert</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #FFFFFF;'>Real-time heart rate monitoring with alerts and notifications</p>", unsafe_allow_html=True)

# Layout with columns
col1, col2 = st.columns([2, 1])

# Heart rate gauge
with col1:
    heart_rate = get_heart_rate()
    st.session_state.heart_rate_history.append(heart_rate)
    st.session_state.timestamps.append(datetime.now().strftime("%H:%M:%S"))
    
    # Limit history to last 20 readings
    if len(st.session_state.heart_rate_history) > 20:
        st.session_state.heart_rate_history = st.session_state.heart_rate_history[-20:]
        st.session_state.timestamps = st.session_state.timestamps[-20:]
    
    # Create gauge
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=heart_rate,
        title={'text': "Heart Rate (BPM)", 'font': {'color': '#FFFFFF'}},
        gauge={
            'axis': {'range': [0, 150], 'tickcolor': '#FFFFFF', 'tickfont': {'color': '#FFFFFF'}},
            'bar': {'color': "#00D4FF"},
            'steps': [
                {'range': [0, 50], 'color': "#FF4B4B"},
                {'range': [50, 100], 'color': "#4CAF50"},
                {'range': [100, 150], 'color': "#FF4B4B"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 100
            },
            'bgcolor': 'rgba(0,0,0,0)'
        }
    ))
    fig_gauge.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#FFFFFF'}
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

# Alerts, recommendations, and notifications
with col2:
    st.subheader("Alerts")
    user_email = st.session_state.get("user_email", None)
    if not user_email:
        try:
            with open("last_user.json", "r") as f:
             user_email = json.load(f).get("email", None)
             st.session_state["user_email"] = user_email
        except Exception:
            st.warning("⚠ User email not found in session or file. Please log in first.")
            st.stop()
    
    # Rule-based check for abnormal heart rate (outside 50-100 BPM)
    is_abnormal = heart_rate < 60 or heart_rate > 100
    email_cooldown = 300  # 5 minutes in seconds
    
    if is_abnormal:
        st.markdown(f"<div class='alert-box'>ALERT: Abnormal heart rate detected ({heart_rate} bpm)</div>", unsafe_allow_html=True)
        # Send email only if last email was sent more than 5 minutes ago
        current_time = time.time()
        if user_email and (st.session_state.last_email_sent is None or 
                          (current_time - st.session_state.last_email_sent) > email_cooldown):
            alert_msg = send_email_alert(heart_rate, user_email)
            st.session_state.alerts.append(alert_msg)
            st.session_state.last_email_sent = current_time
    else:
        st.markdown(f"<div class='safe-box'>Heart rate normal ({heart_rate} bpm)</div>", unsafe_allow_html=True)

    # Display recent alerts
    for alert in st.session_state.alerts[-3:]:
        st.markdown(f"<div style='color: #FFFFFF;'>{alert}</div>", unsafe_allow_html=True)

    # Health recommendations
    st.subheader("Health Recommendations")
    status, recommendations = get_health_recommendations(heart_rate)
    st.markdown(f"<div class='recommendation-box'><strong>{status}</strong><ul>", unsafe_allow_html=True)
    for rec in recommendations:
        st.markdown(f"<li style='color: #e0e0e0;'>{rec}</li>", unsafe_allow_html=True)
    st.markdown("</ul></div>", unsafe_allow_html=True)

# Heart rate trend chart
st.subheader("Heart Rate Trend")
st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
df = pd.DataFrame({
    'Time': st.session_state.timestamps,
    'Heart Rate (BPM)': st.session_state.heart_rate_history
})
fig_trend = px.line(df, x='Time', y='Heart Rate (BPM)', title="Heart Rate Over Time")
fig_trend.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="#FFFFFF",
    xaxis_gridcolor="rgba(255,255,255,0.1)",
    yaxis_gridcolor="rgba(255,255,255,0.1)",
    title_font=dict(size=24, color="#39ff14"),
    xaxis=dict(tickcolor="#00f7ff"),
    yaxis=dict(tickcolor="#00f7ff")
)
fig_trend.update_traces(line=dict(width=4, color="#00f7ff"), fill='tozeroy', fillcolor='rgba(0, 247, 255, 0.2)')
st.plotly_chart(fig_trend, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Auto-refresh every 5 minutes (300 seconds)
time.sleep(300)
st.rerun()