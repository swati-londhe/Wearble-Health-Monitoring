import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import sqlite3
from pathlib import Path
import json

# Move set_page_config to the top as the first Streamlit command
st.set_page_config(page_title="Wearable Health Monitoring", layout="wide")

# ---------- DATABASE SETUP ----------
DB_FILE = "users.db"

# Initialize or migrate database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    c.execute("PRAGMA table_info(users)")
    columns = [info[1] for info in c.fetchall()]
    
    if 'username' in columns and 'email' not in columns:
        c.execute('''CREATE TABLE users_new (
                        email TEXT PRIMARY KEY,
                        password TEXT NOT NULL
                     )''')
        c.execute('''INSERT INTO users_new (email, password)
                     SELECT username, password FROM users''')
        c.execute('DROP TABLE users')
        c.execute('ALTER TABLE users_new RENAME TO users')
    elif 'email' not in columns:
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        email TEXT PRIMARY KEY,
                        password TEXT NOT NULL
                     )''')
    
    conn.commit()
    conn.close()

# Insert new user
def create_user(email, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
    conn.commit()
    conn.close()

# Check credentials
def check_credentials(email, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    result = c.fetchone()
    conn.close()
    return result

# Check if email exists
def user_exists(email):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    result = c.fetchone()
    conn.close()
    return result is not None

# Initialize DB
init_db()

# Load local Lottie animation
def load_lottie_file(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Failed to load local animation: {e}")
        return None

# Load the local heartbeat.json file
lottie_health = load_lottie_file("heartbeat.json")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- CSS Styling with Enhancements ---
st.markdown("""
    <style>
    /* Centered layout for the entire app */
#     .stApp {
#      height: 100vh;
#      display: flex;
#      justify-content: center;
#      align-items: center;
#      overflow: hidden;
#      position: relative;
#      background-color: blue; /* Fallback or base color */
#      background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
#      width: 100%;
# }


    /* Animated background particles */
    .stApp::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: url('https://www.transparenttextures.com/patterns/dark-mosaic.png');
        opacity: 0.1;
        z-index: 0;
        animation: moveParticles 20s infinite linear;
    }

    @keyframes moveParticles {
        0% { background-position: 0 0; }
        100% { background-position: 100% 100%; }
    }

    /* Hide Streamlit banner */
    .css-1aumxhk {
        display: none !important;
    }

    /* Hide sidebar */
    [data-testid="stSidebar"] {
        display: none !important;
    }

    /* Centered login container wrapper */
    .login-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: 100%;
        position: relative;
        z-index: 1;
    }

    @keyframes fadeInUp {
        0% { opacity: 0; transform: translateY(30px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    /* Title styling with gradient text */
    .title {
        font-size: 32px;
        font-weight: bold;
        background: linear-gradient(90deg, #00d4ff, #ff6f61);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
        text-align: center;
    }

    /* Input field styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.8);
        border: none;
        border-radius: 25px;
        padding: 12px 20px;
        font-size: 16px;
        transition: all 0.3s ease;
        width: 100%;
        max-width: 350px;
        box-sizing: border-box;
        color: #333;
        margin: 0 auto 10px;
        display: block;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    .stTextInput > div > div > input:focus {
        background: #ffffff;
        box-shadow: 0 0 8px rgba(0, 123, 255, 0.5);
        outline: none;
        transform: scale(1.02);
    }
    .stTextInput > div > div > input::placeholder {
        color: #999;
        opacity: 1;
    }

    /* Button styling with glowing effect */
    .stButton > button {
        background: linear-gradient(90deg, #00c4ff, #ff6f61);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-size: 16px;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
        max-width: 350px;
        margin: 10px auto 0;
        display: block;
        box-shadow: 0 5px 15px rgba(0, 123, 255, 0.3);
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #0096d6, #e65a50);
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0, 123, 255, 0.5), 0 0 20px rgba(255, 111, 97, 0.5);
    }

    /* Tabs styling with subtle animation */
    .stTabs {
        width: 100%;
        max-width: 350px;
        margin: 0 auto 20px;
    }
    .stTabs [role="tablist"] {
        justify-content: center;
        margin-bottom: 0;
    }
    .stTabs [role="tab"] {
        background-color: rgba(255, 255, 255, 0.2);
        border: none;
        padding: 10px 20px;
        border-radius: 25px;
        margin: 0 5px;
        transition: all 0.3s ease;
        flex: 1;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        color: white;
    }
    .stTabs [role="tab"][aria-selected="true"] {
        background: linear-gradient(90deg, #00c4ff, #ff6f61);
        color: white;
        box-shadow: 0 5px 15px rgba(0, 123, 255, 0.3);
    }
    .stTabs [role="tab"]:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: translateY(-2px);
    }

    /* Footer styling */
    .footer {
        position: absolute;
        bottom: 20px;
        width: 100%;
        text-align: center;
        color: #00d4ff;
        font-size: 14px;
        opacity: 0.8;
        z-index: 1;
    }
    .footer a {
        color: #00d4ff;
        text-decoration: none;
        font-weight: bold;
    }
    .footer a:hover {
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)

# --- Hide Sidebar ---
hide_sidebar = """
    <style>
        [data-testid="stSidebar"] {display: none;}
        [data-testid="stToolbar"] {right: 2rem;}
        .css-18ni7ap {padding-top: 3rem;}
    </style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)

# --- Login Page ---
if not st.session_state["logged_in"]:
    with st.container():
        st.markdown("<div class='login-wrapper'>", unsafe_allow_html=True)
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)

        # Display Lottie animation only if it was loaded successfully
        if lottie_health:
            st_lottie(lottie_health, height=150, key="health_animation")
        else:
            st.warning("Unable to load animation. Check if 'heartbeat.json' is in the correct directory.")

        # Add a title
        st.markdown("<div class='title'>Wearable Health Monitoring</div>", unsafe_allow_html=True)

        # Tabs
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Signup"])

        # Login Tab
        with tab1:
            with st.form("login_form", clear_on_submit=False):
                email = st.text_input("Email", placeholder="Enter your email", key="login_email")
                password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
                login_button = st.form_submit_button("Login")

                if login_button:
                    if check_credentials(email, password):
                        st.session_state["logged_in"] = True
                        st.session_state["user_email"] = email
                        with open("last_user.json", "w") as f:
                            json.dump({"email": email}, f)

                        st.success("Login successful! Redirecting to Home...")
                        st.switch_page("pages/home.py")
                    else:
                        st.error("Invalid email or password")

        # Signup Tab
        with tab2:
            with st.form("signup_form", clear_on_submit=False):
                st.markdown("<div style='text-align: center; color: #00c4ff; font-weight: bold; margin-bottom: 10px;'>Create an account</div>", unsafe_allow_html=True)
                new_email = st.text_input("Email", placeholder="Enter your email", key="signup_email")
                new_password = st.text_input("New Password", type="password", placeholder="Enter password", key="signup_password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm password", key="signup_confirm_password")
                signup_button = st.form_submit_button("Signup")

                if signup_button:
                    if new_password == confirm_password:
                        if user_exists(new_email):
                            st.error("Email already exists. Please use a different email.")
                        else:
                            create_user(new_email, new_password)
                            st.success("Signup successful! Please login.")
                    else:
                        st.error("Passwords do not match.")

        st.markdown("</div>", unsafe_allow_html=True)  # Close login-container
        st.markdown("</div>", unsafe_allow_html=True)  # Close login-wrapper

    # Footer with authoritative message
    st.markdown(
        """
        <div class='footer'>
            Powered by <a href="https://sunfibo.com" target="_blank">Sunfibo Internship</a> | Secure Health Monitoring Solution
        </div>
        """,
        unsafe_allow_html=True
    )
else:   
    # Redirect to home page if already logged in
    st.switch_page("pages/home.py")