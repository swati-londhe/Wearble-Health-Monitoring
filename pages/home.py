import streamlit as st

# --- Page Config ---
st.set_page_config(page_title=" Smartwatch Health Monitoring", layout="wide")


# --- Hide Sidebar ---
hide_sidebar = """
    <style>
        [data-testid="stSidebar"] {display: none;}
        [data-testid="stToolbar"] {right: 2rem;}
        .css-18ni7ap {padding-top: 3rem;}
        body {
            background: linear-gradient(135deg, #1f5156, #2a9d8f); /* Deep teal to soft blue gradient */
        }
    </style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)

# --- Initialize Session State ---
if 'show_workflow' not in st.session_state:
    st.session_state.show_workflow = False

st.markdown("""
<div class="hero-section">
    <div class="particles"></div>
    <h1 class="hero-title">⌚  Smartwatch Health Monitoring</h1>
    <p class="hero-subtitle">Track your ❤️ heart rate, 🩸 SpO2, 🦶 steps, and 💤 sleep in real-time.</p>
</div>

<style>
            
.hero-section {
    position: relative;
    text-align: center;
    padding: 70px 20px;
    background: linear-gradient(to bottom, #0f0f0f, #1a1a1a);
    color: white;
    overflow: hidden;
    z-index: 1;
    border-radius: 12px;
    margin-bottom: 30px;
}

/* Particle Background Simulation */
.particles {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: transparent;
    z-index: 0;
}
.particles::before, .particles::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 300%;
    height: 300%;
    background-image: radial-gradient(white 1px, transparent 1px);
    background-size: 20px 20px;
    opacity: 0.08;
    animation: twinkle 8s linear infinite;
}

.particles::after {
    background-size: 25px 25px;
    animation-direction: reverse;
}

@keyframes twinkle {
    0% { transform: translate(0, 0); }
    50% { transform: translate(-10px, -10px); }
    100% { transform: translate(0, 0); }
}

.hero-title {
    font-size: 3em;
    font-weight: bold;
    background: linear-gradient(to right, #ff416c, #ff4b2b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: fadeInDown 1.2s ease-out;
    z-index: 2;
    position: relative;
}

.hero-subtitle {
    font-size: 1.4em;
    color: #f0f0f0;
    margin-top: 15px;
    animation: fadeInUp 2s ease-out;
    z-index: 2;
    position: relative;
}

/* Animations */
@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-30px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# --- Image and Project Overview Side by Side ---
left_col, right_col = st.columns([2, 3])

with left_col:
    # Using st.image with a placeholder URL
    st.image(
        "D:/Sunfibo internship/wearble health monitoring/wearable_health_monitoring_ai/images/home.jpg",
        use_container_width=True
    )

with right_col:
    # st.markdown("## 📝 Project Overview")
    st.markdown("""
        <div class="flip-card-container">
            <div class="flip-card">
                <div class="flip-card-inner">
                    <div class="flip-card-front">
                        <h3>Wearable Health Monitoring</h3>
                    </div>
                    <div class="flip-card-back">
                        <p>The Wearable Health Monitoring System is an AI-powered solution designed to continuously track and analyze users' health metrics through smartwatches.</p>
                    </div>
                </div>
            </div>
            <div class="flip-card">
                <div class="flip-card-inner">
                    <div class="flip-card-front">
                        <h3>Real-time Alerts</h3>
                    </div>
                    <div class="flip-card-back">
                        <p>Provides real-time alerts, recommendations, and visualizations using cloud-based machine learning models.</p>
                    </div>
                </div>
            </div>
            <div class="flip-card">
                <div class="flip-card-inner">
                    <div class="flip-card-front">
                        <h3>Device Integration</h3>
                    </div>
                    <div class="flip-card-back">
                        <p>Integrates with devices like boAt, Apple Watch, and WearOS smartwatches using Google Fit API and Apple HealthKit.</p>
                    </div>
                </div>
            </div>
            <div class="flip-card">
                <div class="flip-card-inner">
                    <div class="flip-card-front">
                        <h3>Health Insights</h3>
                    </div>
                    <div class="flip-card-back">
                        <p>Supports real-time data processing, personalized health suggestions, and emergency alerting mechanisms.</p>
                    </div>
                </div>
            </div>
        </div>
        <style>
            .flip-card-container {
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                margin: 20px 0;
            }
            .flip-card {
                flex: 1;
                min-width: 200px;
                height: 250px;
                perspective: 1000px;
            }
            .flip-card-inner {
                position: relative;
                width: 100%;
                height: 100%;
                text-align: center;
                transition: transform 0.6s;
                transform-style: preserve-3d;
            }
            .flip-card:hover .flip-card-inner {
                transform: rotateY(180deg);
            }
            .flip-card-front, .flip-card-back {
                position: absolute;
                width: 100%;
                height: 100%;
                backface-visibility: hidden;
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 10px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            }
            .flip-card-front {
                background: linear-gradient(135deg, #483D8B, #6A5ACD); /* Blue-purple gradient */
                color: white;
            }
            .flip-card-back {
                background: linear-gradient(135deg, #32CD32, #98FB98); /* Green-lime gradient */
                color: white;
                transform: rotateY(180deg);
            }
            .flip-card-front h3 {
                margin: 0;
                font-size: 1.2em;
            }
            .flip-card-back p {
                margin: 0;
                font-size: 0.9em;
            }
        </style>
    """, unsafe_allow_html=True)
# --- CTA Buttons ---
st.markdown("""
    <style>
        .button-style {
            background: linear-gradient(45deg, #ff4b2b, #ff6f61);
            color: white;
            padding: 4px 8px; /* Reduce padding */
            border-radius: 6px;
            border: none;
            font-size: 10px; /* Reduce font size */
            margin: 10px;
            cursor: pointer;
            transition: transform 0.5s, box-shadow 0.5s;
            display: inline-block;
            width: 120px; /* Fixed width */
            text-align: center;
        }
        .button-style:hover {
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(255, 75, 43, 0.7);
        }
        .stButton > button {
            font-size: 10px; /* Consistent button font size */
            border-radius: 6px;
            padding: 0.4em 1em; /* Adjust padding */
        }
    </style>
""", unsafe_allow_html=True)

# Layout for buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Learn How It Works"):
        st.session_state.show_workflow = True

with col2:
     if st.button("Go to Dashboard", key="go_to_dashboard", help="Navigate to the dashboard"):
        st.switch_page("pages/dashboard.py")



# --- System Workflow Section with 3D Tilt Effect ---
if st.session_state.show_workflow:
    st.markdown("---")
    st.markdown('<h2 id="how-it-works" style="text-align: center; padding-top: 40px;">⚙️ How the System Works</h2>', unsafe_allow_html=True)

    st.markdown("""
        <div class="workflow-container">
            <div class="workflow-box" data-tilt>1️⃣ Wear your boAt Smartwatch</div>
            <div class="workflow-box" data-tilt>2️⃣ Sync with Google Fit</div>
            <div class="workflow-box" data-tilt>3️⃣ Log in to Dashboard</div>
            <div class="workflow-box" data-tilt>4️⃣ View Real-time Stats</div>
            <div class="workflow-box" data-tilt>5️⃣ Get Health Alerts & Insights</div>
        </div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/vanilla-tilt/1.7.0/vanilla-tilt.min.js"></script>
        <script>
            VanillaTilt.init(document.querySelectorAll(".workflow-box"), {
                max: 25,
                speed: 400,
                glare: true,
                "max-glare": 0.5,
            });
        </script>
        <style>
            .workflow-container {
                display: flex;
                flex-direction: row;
                justify-content: space-around;
                gap: 30px;
                margin-top: 20px;
                flex-wrap: wrap;
            }
            .workflow-box {
                flex: 1;
                background: linear-gradient(135deg, #26a69a, #80deea);
                color: #ffffff;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.2);
                text-align: center;
                min-width: 200px;
                max-width: 220px;
                animation: slideIn 1s ease-in-out;
            }
            .workflow-box:nth-child(1) { animation-delay: 0s; }
            .workflow-box:nth-child(2) { animation-delay: 0.2s; }
            .workflow-box:nth-child(3) { animation-delay: 0.4s; }
            .workflow-box:nth-child(4) { animation-delay: 0.6s; }
            .workflow-box:nth-child(5) { animation-delay: 0.8s; }
            .workflow-box:hover {
                box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            }
            @keyframes slideIn {
                from { opacity: 0; transform: translateY(50px); }
                to { opacity: 1; transform: translateY(0); }
            }
        </style>
    """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.markdown("© 2025 HealthMonitor | All rights reserved.")