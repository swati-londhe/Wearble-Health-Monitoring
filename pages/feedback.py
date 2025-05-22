import streamlit as st
from streamlit_option_menu import option_menu
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re

# Clear Streamlit cache to ensure changes take effect
st.cache_data.clear()
st.cache_resource.clear()

st.set_page_config(page_title="Wearable Health Monitoring - Feedback", layout="wide")

# --- Email Credentials ---
EMAIL_SENDER = "swatilondhe2911@gmail.com"
EMAIL_PASSWORD = "tzgg enkf kitu zxkc"  # Use App Password if using Gmail
EMAIL_RECEIVER = "sunfiboaitesting@sunfibo.com"

# --- CSS Styling ---
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
        background: url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgogIDxkZWZzPgogICAgPGZpbHRlciBpZD0iZ2xvd0ZpbHRlciI+CiAgICAgIDxmZUdhdXNzaWFuQmx1ciBpbj0iU291cmNlR3JhcGhpYyIgc3RkRGV2aWF0aW9uPSIyIiAvPgogICAgPC9maWx0ZXIAogIDwvZGVmcz4KICA8ZyBmaWx0ZXI9InVybCgjZ2xvd0ZpbHRlcikiPgogICAgPHBhdGggZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMDBmN2ZmIiBzdHJva2Utd2lkdGg9IjEiIGQ9Ik0wLDBoMjAwMHYxMjAwSDB6IiAvPgogICAgPGNpcmNsZSBjeD0iMTAwIiBjeT0iMTAwIiByPSIzIiBmaWxsPSIjMDBmN2ZmIiBvcGFjaXR5PSIwLjciIGFuaW1hdGVNb3Rpb24gZHVyPSIzMHMiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBiZWdpbj0iMHMiIHBhdGhUPSJNMTAwLDEwMCBDMzAwLDMwMCw1MDAsMTAwLDcwMCwzMDBDMTAwMCwxMDAsMTIwMCwzMDAsMTUwMCwxMDBDMTgwMCwzMDAsMjAwMCwxMDAsMjAwMCwxMjAwQzE1MDAsOTAwLDEyMDAsMTIwMCwxMDAwLDkwMEM3MDAsMTIwMCw1MDAsOTAwLDMwMCwxMjAwQzEwMCw5MDAsMCwxMjAwLDAsMTAwWiIgLz4KICAgIDxjaXJjbGUgY3g9IjUwMCIgY3k9IjUwMCIgcj0iMiIgZmlsbD0iI2ZmMDBlNiIgb3BhY2l0eT0iMC41IiBhbmltYXRlTW90aW9uIGR1cj0iMjBzIiByZXBlYXRDb3VudD0iaW5kZWZpbml0ZSIgYmVnaW49IjVzIiBwYXRoPSJNNTAwLDUwMCBDNzAwLDMwMCw5MDAsNTAwLDExMDAsMzAwQzEzMDAsNTAwLDE1MDAsMzAwLDE3MDAsNTAwQzE5MDAsNzAwLDE3MDAsOTAwLDE1MDAsMTEwMEMxMzAwLDkwMCwxMTAwLDExMDAsOTAwLDkwMEM3MDAsMTEwMCw1MDAsOTAwLDMwMCwxMTAwQzEwMCw5MDAsMzAwLDcxMCw1MDAsNTAwWiIgLz4KICA8L2c+Cjwvc3ZnPg==');
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
        margin: 0 !important;
        border: none !important;
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

    /* Feedback title styling */
    .feedback-title {
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

    .content {
        margin: 80px auto 0 auto !important; /* Adjusted for fixed navbar */
        padding: 2rem !important;
        max-width: 450px !important;
        width: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        z-index: 1 !important;
    }

    .feedback-box {
        padding: 2rem !important;
        width: 100% !important;
    }

    .submit-button, .logout-button {
        background: linear-gradient(90deg, #5e72e4, #a35ee4) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.8rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        display: block !important;
        width: 100% !important;
        text-align: center !important;
        text-decoration: none !important;
    }

    .submit-button:hover, .logout-button:hover {
        background: linear-gradient(90deg, #a35ee4, #5e72e4) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2) !important;
    }

    .logout-button {
        background: linear-gradient(90deg, #5e72e4, #a35ee4) !important;
        margin-top: 1.5rem !important;
    }

    .logout-button:hover {
        background: linear-gradient(90deg, #a35ee4, #5e72e4) !important;
    }

    .modal {
        position: fixed !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        background: #ffffff !important;
        padding: 2rem !important;
        border-radius: 15px !important;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.2) !important;
        z-index: 1000 !important;
        animation: slideIn 0.5s ease !important;
        text-align: center !important;
    }

    @keyframes slideIn {
        from { transform: translate(-50%, -60%); opacity: 0; }
        to { transform: translate(-50%, -50%); opacity: 1; }
    }

    .modal-overlay {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        background: rgba(0, 0, 0, 0.6) !important;
        z-index: 999 !important;
    }

    /* Adjusted styles for input fields */
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea {
        width: 100% !important;
        padding: 0.5rem !important;
        font-size: 1rem !important;
        border: 1px solid #ccc !important;
        border-radius: 5px !important;
        background-color: #fff !important;
        color: #333 !important;
        transition: border-color 0.3s ease !important;
        margin-bottom: 1.5rem !important;
    }

    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stTextArea"] textarea:focus {
        border-color: #5e72e4 !important;
        outline: none !important;
    }

    div[data-testid="stTextArea"] textarea {
        height: 120px !important;
        resize: none !important;
    }

    div[data-testid="stTextInput"] label,
    div[data-testid="stTextArea"] label {
        color: #e0e0e0 !important;
        font-size: 0.9rem !important;
    }

    /* Override Streamlit's default wide mode stretching */
    div[data-testid="stForm"] {
        max-width: 450px !important;
        width: 100% !important;
        margin: 0 auto !important;
    }

    div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(90deg, #5e72e4, #a35ee4) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.8rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }

    div[data-testid="stFormSubmitButton"] button:hover {
        background: linear-gradient(90deg, #a35ee4, #5e72e4) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2) !important;
    }

    @media (max-width: 768px) {
        .nav-menu {
            flex-wrap: wrap !important;
            gap: 1rem !important;
        }
        .content {
            padding: 1rem !important;
        }
        .feedback-box {
            padding: 1.5rem !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- Hide Sidebar ---
hide_sidebar = """
    <style>
        [data-testid="stSidebar"] {display: none;}
        [data-testid="stToolbar"] {right: 2rem;}
        .css-18ni7ap {padding-top: 3rem;}
        body {
            background: linear-gradient(135deg, #1f5156, #2a9d8f);
        }
    </style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)

# --- Navigation Bar ---
st.markdown("<div class='nav-bar'><div class='nav-menu'>", unsafe_allow_html=True)
pages = {
    "Home": "pages/home.py",
    "Dashboard": "pages/dashboard.py",
    "Alert": "pages/alert.py",
    "About Us": "pages/about.py",
    "Feedback": "pages/feedback.py"
}
selected = option_menu(None, list(pages.keys()),
                       menu_icon="cast", default_index=4, orientation="horizontal",
                       styles={
                           "container": {"padding": "0", "background-color": "transparent"},
                           "nav-link": {"font-size": "18px", "text-align": "center", "margin": "0 10px", "color": "#e0e0e0"},
                           "nav-link-selected": {"background": "linear-gradient(45deg, #00f7ff, #ff00e6)", "color": "#ffffff"},
                       })
st.markdown("</div></div>", unsafe_allow_html=True)

# --- Feedback Title ---
st.markdown("<h1 class='feedback-title'>Feedback</h1>", unsafe_allow_html=True)

# --- Feedback Form ---
st.markdown("<div class='content'><div class='feedback-box'>", unsafe_allow_html=True)

with st.form("feedback_form"):
    name = st.text_input("Name", placeholder="Your name", key="name")
    user_email = st.text_input("Email", placeholder="Your email", key="email")
    subject = st.text_input("Subject", placeholder="Subject", key="subject")
    feedback_message = st.text_area("Message", height=120, placeholder="Your message", key="feedback")
    submit = st.form_submit_button("Submit", help="Submit your feedback", type="primary")

    def send_email(from_email, to_email, password, message_text):
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = "New Feedback from Wearable Health Monitoring User"
        msg.attach(MIMEText(message_text, "plain"))
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())

    # Email validation and submission
    if submit:
        if not name or not user_email or not subject or not feedback_message:
            st.error("❗ Please fill in all fields.")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", user_email):
            st.error("❗ Invalid email address.")
        else:
            try:
                send_email(EMAIL_SENDER, EMAIL_RECEIVER, EMAIL_PASSWORD,
                           f"From: {name} ({user_email})\n\nSubject: {subject}\n\nMessage:\n{feedback_message}")
                st.session_state.feedback_submitted = True
                st.rerun()
            except Exception as e:
                st.error(f"❌ Failed to send feedback. Error: {e}")

if st.session_state.get("feedback_submitted", False):
    st.success("✅ Thank you! Your feedback has been sent to Sunfibo Technology.")

# --- Logout Button ---
with st.form(key="logout_form"):
    if st.form_submit_button("Logout", help="Click to logout", use_container_width=True):
        st.session_state.clear()  # Clear session state
        try:
            st.switch_page("main.py")  # Navigate to main page for login
        except Exception as e:
            st.error(f"❌ Failed to navigate to login page. Error: {e}. Please ensure 'main.py' exists in the project directory.")

st.markdown("</div></div>", unsafe_allow_html=True)

# --- Navigation Logic ---
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
elif selected == "About Us":
    try:
        st.switch_page("pages/about.py")
    except Exception as e:
        st.error("About Us page not found. Please ensure 'pages/about.py' exists.")
elif selected == "Feedback":
    pass