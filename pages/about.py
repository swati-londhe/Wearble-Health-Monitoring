import streamlit as st
from streamlit_option_menu import option_menu

# Set page configuration
st.set_page_config(page_title="Wearable Health Monitoring - About Us", layout="wide")

# Custom CSS for CyberHealth aesthetic
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
 ваше направление: column;
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
        background: url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgogIDxkZWZzPgogICAgPGZpbHRlciBpZD0iZ2xvd0ZpbHRlciI+CiAgICAgIDxmZUdhdXNzaWFuQmx1ciBpbj0iU291cmNlR3JhcGhpYyIgc3RkRGV2aWF0aW9uPSIyIiAvPgogICAgPC9maWx0ZXIAogIDwvZGVmcz4KICA8ZyBmaWx0ZXI9InVybCgjZ2xvd0ZpbHRlcikiPgogICAgPHBhdGggZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMDBmN2ZmIiBzdHJva2Utd2lkdGg9IjEiIGQ9Ik0wLDBoMjAwMHYxMjAwSDB6IiAvPgogICAgPGNpcmNsZSBjeD0iMTAwIiBjeT0iMTAwIiByPSIzIiBmaWxsPSIjMDBmN2ZmIiBvcGFjaXR5PSIwLjciIGFuaW1hdGVNb3Rpb24gZHVyPSIzMHMiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBiZWdpbj0iMHMiIHBhdGhUPSJNMTAwLDEwMCBDMzAwLDMwMCw1MDAsMTAwLDcwMCwzMDBDMTAwMCwxMDAsMTIwMCwzMDAsMTUwMCwxMDBDMTgwMCwzMDAsMjAwMCwxMDAsMjAwMCwxMjAwQzE1MDAsOTAwLDEyMDAsMTIwMCwxMDAwLDkwMEM3MDAsMTIwMCw1MDAsOTAwLDMwMCwxMjAwQzEwMCw5MDAsMCwxMjAwLDAsMTAwWiIgLz4KICAgIDxjaXJjbGUgY3g9IjUwMCIgY3k9IjUwMCIgcj0iMiIgZmlsbD0iI2ZmMDBlNiIgb3BhY2l0eT0iMC41IiBhbmltYXRlTW90aW9uIGR1cj0iMjBzIiByZXBlYXRDb3VudD0iaW5kZWZpbml0ZSIgYmVnaW49IjVzIiBwYXRoPSJNNTAwLDUwMCBDNzAwLDMwMCw5MDAsNTAwLDExMDAsMzAwQzEzMDAsNTAwLDE1MDAsMzAwLDE3MDAsNTAwQzE5MDAsNzAwLDE3MDAsOTAwLDE1MDAsMTEwMEMxMzAwLDkwMCwxMTAwLDExMDAsOTAwLDkwMEM3MDAsMTEwMCw1MDAsOTAwLDMwMCwxMTAwQzEwMCw5MDAsMzAwLDcxMCw1MDAsNTAwWiIgLz4KICA8L2c+Cjwvc3ZnPg==');
        pointer-events: none;
        z-index: 0;
    }

    /* Hide sidebar */
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
        display: flex;
        justify-content: center;
        gap: 2rem;
    }

    /* Content styling */
    .content {
        margin-top: 80px;
        padding: 2rem;
        color: #e0e0e0;
        position: relative;
        z-index: 1;
        max-width: 1200px;
        width: 100%;
    }

    .about-header {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00f7ff, #ff00e6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        animation: glow 2s ease-in-out infinite alternate;
        text-shadow: 0 0 20px rgba(0, 247, 255, 0.7);
    }

    @keyframes glow {
        from { text-shadow: 0 0 10px #00f7ff, 0 0 20px #ff00e6; }
        to { text-shadow: 0 0 20px #ff00e6, 0 0 30px #00f7ff; }
    }

    .section-header {
        font-size: 1.6rem;
        font-weight: 600;
        color: #ffffff;
        background: linear-gradient(90deg, #39ff14, #ff00e6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 10px rgba(57, 255, 20, 0.7);
    }

    .content-text {
        font-size: 0.9rem;
        color: #e0e0e0;
        line-height: 1.5;
        margin-bottom: 0.3rem;
    }

    .highlight-box {
        background: linear-gradient(145deg, #1b263b, #2a3b5b);
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.5);
        border: 2px solid #00f7ff;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        min-height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }

    .highlight-box:hover {
        box-shadow: 0 10px 20px rgba(0, 247, 255, 0.7);
        border-color: #ff00e6;
        transform: translateY(-5px);
    }

    .contact-link {
        color: #00f7ff;
        text-decoration: none;
        font-weight: bold;
        transition: color 0.3s ease;
    }

    .contact-link:hover {
        color: #ff00e6;
        text-decoration: underline;
    }

    hr {
        border: 1px solid #00f7ff;
        margin: 2rem 0;
        box-shadow: 0 0 10px #00f7ff;
    }

    @media (max-width: 768px) {
        .content {
            padding: 1rem;
        }
        .about-header {
            font-size: 2rem;
        }
        .section-header {
            font-size: 1.4rem;
        }
        .content-text {
            font-size: 0.8rem;
        }
        .highlight-box {
            min-height: 180px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Hide sidebar
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
    "About Us": "pages/about.py",
    "Feedback": "pages/feedback.py"
}
selected = option_menu(None, list(pages.keys()),
                       menu_icon="cast", default_index=3, orientation="horizontal",
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
    try:
        st.switch_page("pages/alert.py")
    except Exception as e:
        st.error("Alert page not found. Please ensure 'pages/alert.py' exists.")
elif selected == "Feedback":
    try:
        st.switch_page("pages/feedback.py")
    except Exception as e:
        st.error("Feedback page not found. Please ensure 'pages/feedback.py' exists.")
elif selected == "About Us":
    pass

# About Us Content
st.markdown("<div class='content'>", unsafe_allow_html=True)

# Main Title
st.markdown("<h1 class='about-header'>About Us – Smart Health Monitoring System</h1>", unsafe_allow_html=True)
st.markdown("<p class='content-text' style='text-align: center; margin-bottom: 2rem;'>Welcome to our AI-Powered Wearable Health Monitoring Platform, where technology meets wellness.</p>", unsafe_allow_html=True)

# First Row: Who We Are, What We Do, Technologies We Use
col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("<h2 class='section-header'>🔍 Who We Are</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class='highlight-box'>
        <p class='content-text'>
            We are a passionate team of developers and researchers working at the intersection of healthcare and artificial intelligence. 
            Our goal is to revolutionize preventive healthcare using wearable technology, machine learning, and real-time data visualization.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("<h2 class='section-header'>💡 What We Do</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class='highlight-box'>
        <p class='content-text'>
            Our platform integrates with smartwatches (like boAt, Fitbit, Apple Watch, WearOS) via Google Fit and Apple HealthKit to fetch health data. We provide:
        </p>
        <ul class='content-text'>
            <li>Live Health Dashboard</li>
            <li>Health Recommendations</li>
            <li>Dehydration Alerts</li>
            <li>Emergency Notifications</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("<h2 class='section-header'>🧠 Technologies We Use</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class='highlight-box'>
        <p class='content-text'><strong>APIs:</strong> Google Fit, Apple HealthKit</p>
        <p class='content-text'><strong>Frontend:</strong> Streamlit, React Native</p>
        <p class='content-text'><strong>Backend:</strong> Python, Firebase, SQLite</p>
        <p class='content-text'><strong>ML Models:</strong> Decision Trees</p>
    </div>
    """, unsafe_allow_html=True)

# Second Row: Our Vision, Our Mission, Contact Us
col4, col5, col6 = st.columns(3, gap="medium")

with col4:
    st.markdown("<h2 class='section-header'>🌐 Our Vision</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class='highlight-box'>
        <p class='content-text'>
            To build a reliable, intelligent, and accessible health companion that assists users in maintaining their health 
            and notifies their loved ones in critical situations.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("<h2 class='section-header'>🎯 Our Mission</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class='highlight-box'>
        <p class='content-text'>
            Our mission is to empower individuals to take charge of their health through real-time monitoring, smart predictions, 
            and actionable recommendations via wearable technology.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("<h2 class='section-header'>📬 Contact Us</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class='highlight-box'>
        <p class='content-text'>
            For queries or feedback, reach out:
        </p>
        <p class='content-text'>
            📧 <strong>Smart Health:</strong> <a class='contact-link' href='mailto:support@smarthealth.ai'>support@smarthealth.ai</a><br> 
            📧 <strong>Sunfibo Tech:</strong> <a class='contact-link' href='mailto:sunfibotechnology@gmail.com'>sunfibotechnology@gmail.com</a><br>    
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p class='content-text' style='text-align: center;'>© 2025 Smart Health Monitoring System. All rights reserved.</p>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)