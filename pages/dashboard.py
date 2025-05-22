import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import json
from streamlit_option_menu import option_menu
import plotly.express as px
import time
import joblib

# Set page config as the first Streamlit command
st.set_page_config(page_title="Wearable Health Monitoring", layout="wide")

# Constants
SCOPES = [
    'https://www.googleapis.com/auth/fitness.activity.read',
    'https://www.googleapis.com/auth/fitness.heart_rate.read',
    'https://www.googleapis.com/auth/fitness.oxygen_saturation.read'
]
TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "credentials.json"
CSV_FILE = "health.csv"
DEBUG_LOG_FILE = "debug_log.txt"
MODEL_FILE = "random_forest_model.pkl"

# --- CSS Styling ---
st.markdown("""
    <style>
    /* Full page layout */
    .stApp {
        background: linear-gradient(135deg, #0d1321, #1b263b);
        color: #e0e0e0;
        font-family: 'Orbitron', sans-serif;
        min-height: 100vh;
        overflow: auto;
        position: relative;
    }

    /* Particle background effect */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgogIDxkZWZzPgogICAgPGZpbHRlciBpZD0iZ2xvd0ZpbHRlciI+CiAgICAgIDxmZUdhdXNzaWFuQmx1ciBpbj0iU291cmNlR3JhcGhpYyIgc3RkRGV2aWF0aW9uPSIyIiAvPgogICAgPC9maWx0ZXIAogIDwvZGVmcz4KICA8ZyBmaWx0ZXI9InVybCgjZ2xvd0ZpbHRlcikiPgogICAgPHBhdGggZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMDBmN2ZmIiBzdHJva2Utd2lkdGg9IjEiIGQ9Ik0wLDBoMjAwMHYxMjAwSDB6IiAvPgogICAgPGNpcmNsZSBjeD0iMTAwIiBjeT0iMTAwIiByPSIzIiBmaWxsPSIjMDBmN2ZmIiBvcGFjaXR5PSIwLjciIGFuaW1hdGVNb3Rpb24gZHVyPSIzMHMiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBiZWdpbj0iMHMiIHBhdGhUPSJNMTAwLDEwMCBDMzAwLDMwMCw1MDAsMTAwLDcwMCwzMDBDMTAwMCwxMDAsMTIwMCwzMDAsMTUwMCwxMDBDMTgwMCwzMDAsMjAwMCwxMDAsMjAwMCwxMjAwQzE1MDAsOTAwLDEyMDAsMTIwMCwxMDAwLDkwMEM3MDAsMTIwMCw1MDAsOTAwLDMwMCwxMjAwQzEwMCw5MDAsMCwxMjAwLDAsMTAwWiIgLz4KICAgIDxjaXJjbGUgY3g9IjUwMCIgY3k9IjUwMCIgcj0iMiIgZmlsbD0iI2ZmMDBlNiIgb3BhY2l0eT0iMC41IiBhbmltYXRlTW90aW9uIGR1cj0iMjBzIiByZXBlYXRDb3VudD0iaW5kZWZpbml0ZSIgYmVnaW49IjVzIiBwYXRoPSJNNTAwLDUwMCBDNzAwLDMwMCw5MDAsNTAwLDExMDAsMzAwQzEzMDAsNTAwLDE1MDAsMzAwLDE3MDAsNTAwQzE5MDAsNzAwLDE3MDAsOTAwLDE1MDAsMTEwMEMxMzAwLDkwMCwxMTAwLDExMDAsOTAwLDkwMEM3MDAsMTEwMCw1MDAsOTAwLDMwMCwxMTAwQzEwMCw5MDAsMzAwLDcxMCw1MD0sNTAwWiIgLz4KICA8L2c+Cjwvc3ZnPg==');
        pointer-events: none;
        z-index: 0;
    }

    /* Hide Streamlit banner and sidebar */
    .css-1aumxhk, [data-testid="stSidebar"] {
        display: none !important;
    }

    /* Navigation bar styling */
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
    }

    .dashboard-header {
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

    @keyframes pulse {
        from { transform: scale(1); }
        to { transform: scale(1.05); }
    }

    @keyframes glow {
        from { text-shadow: 0 0 10px #00f7ff, 0 0 20px #ff00e6, 0 0 30px #39ff14; }
        to { text-shadow: 0 0 20px #ff00e6, 0 0 30px #39ff14, 0 0 40px #00f7ff; }
    }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(145deg, #1b263b, #2a3b5b);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.4s ease;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.5);
        border: 2px solid transparent;
        position: relative;
        overflow: hidden;
        animation: neonGlow 2s infinite alternate;
    }

    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, transparent, rgba(0, 247, 255, 0.2), transparent);
        transition: all 0.4s ease;
        z-index: 0;
    }

    .metric-card:hover {
        transform: translateY(-8px) scale(1.05) rotate(2deg);
        box-shadow: 0 12px 25px rgba(0, 247, 255, 0.7), 0 0 40px rgba(255, 0, 230, 0.5);
        border-color: #ff00e6;
    }

    .metric-card:hover::before {
        background: linear-gradient(45deg, transparent, rgba(255, 0, 230, 0.3), transparent);
    }

    .metric-label {
        font-size: 16px;
        color: #a5d8ff;
        margin-bottom: 0.4rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        z-index: 1;
        position: relative;
    }

    .metric-value {
        font-size: 32px;
        font-weight: bold;
        color: #ffffff;
        background: linear-gradient(90deg, #00f7ff, #ff00e6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        z-index: 1;
        position: relative;
    }

    @keyframes neonGlow {
        from { border-color: #00f7ff; box-shadow: 0 0 8px #00f7ff; }
        to { border-color: #ff00e6; box-shadow: 0 0 16px #ff00e6; }
    }

    /* Charts */
    .plotly-chart {
        background: #1b263b;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
        border: 1px solid #00f7ff;
        transition: all 0.3s ease;
    }

    .plotly-chart:hover {
        box-shadow: 0 10px 30px rgba(0, 247, 255, 0.7);
        border-color: #ff00e6;
    }

    hr {
        border: 1px solid #00f7ff;
        margin: 2rem 0;
        box-shadow: 0 0 10px #00f7ff;
    }

    /* Subheader styling */
    h2 {
        color: #ffffff;
        background: linear-gradient(90deg, #39ff14, #ff00e6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 28px;
        margin-top: 2rem;
        text-shadow: 0 0 10px rgba(57, 255, 20, 0.7);
    }

    /* Data table styling */
    .stDataFrame {
        background: #1b263b;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        border: 1px solid #00f7ff;
    }
    </style>
""", unsafe_allow_html=True)

# --- Hide Sidebar ---
hide_sidebar = """
    <style>
        [data-testid="stToolbar"] {right: 2rem;}
        .css-18ni7ap {padding-top: 3rem;}
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
                       menu_icon="cast", default_index=1, orientation="horizontal",
                       styles={
                           "container": {"padding": "0", "background-color": "transparent"},
                           "nav-link": {"font-size": "18px", "text-align": "center", "margin": "0 10px", "color": "#e0e0e0"},
                           "nav-link-selected": {"background": "linear-gradient(45deg, #00f7ff, #ff00e6)", "color": "#ffffff"},
                       })
st.markdown("</div></div>", unsafe_allow_html=True)

# --- Navigation Logic ---
if selected == "Home":
    try:
        st.switch_page("pages/home.py")
    except Exception as e:
        st.write("Home page not found. Please ensure 'pages/home.py' exists.")
elif selected == "Dashboard":
    pass
elif selected == "Alert":
    try:
        st.switch_page("pages/alert.py")
    except Exception as e:
        st.write("Alert page not found. Please ensure 'pages/alert.py' exists.")
elif selected == "About Us":
    try:
        st.switch_page("pages/about.py")
    except Exception as e:
        st.write("About Us page not found. Please ensure 'pages/about.py' exists.")
elif selected == "Feedback":
    try:
        st.switch_page("pages/feedback.py")
    except Exception as e:
        st.write("Feedback page not found. Please ensure 'pages/feedback.py' exists.")
# --- Google Fit Data Functions ---
def authenticate_google():
    creds = None
    if not os.path.exists(CREDENTIALS_FILE):
        st.error(f"Credentials file '{CREDENTIALS_FILE}' not found. Please ensure it exists in the project directory.")
        return None
    
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, 'r') as token:
                creds = Credentials.from_authorized_user_info(json.load(token), SCOPES)
        except Exception as e:
            st.error(f"Error loading token file: {e}")
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                with open(TOKEN_FILE, 'w') as token:
                    token.write(creds.to_json())
            except Exception as e:
                st.error(f"Token refresh failed: {e}")
                creds = None
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
                with open(TOKEN_FILE, 'w') as token:
                    token.write(creds.to_json())
            except Exception as e:
                st.error(f"Authentication failed: {e}")
                return None
    return creds

def get_data_sources(creds):
    headers = {'Authorization': f'Bearer {creds.token}'}
    url = 'https://www.googleapis.com/fitness/v1/users/me/dataSources'
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code != 200:
            st.error(f"Error fetching data sources: {response.status_code} - {response.text}")
            return []
        data = response.json()
        if 'dataSource' not in data:
            st.warning("No data sources found in Google Fit. Ensure your wearable device is synced.")
            return []
        return data.get('dataSource', [])
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch data sources: {e}")
        return []
def round_to_nearest_5min(dt):
    minutes = (dt.minute // 5) * 5
    return dt.replace(minute=minutes, second=0, microsecond=0)

def log_debug(message):
    with open(DEBUG_LOG_FILE, 'a') as f:
        f.write(f"{datetime.now()}: {message}\n")
def round_to_nearest_lower_5min(dt: datetime) -> datetime:
    return dt - timedelta(minutes=dt.minute % 5, seconds=dt.second, microseconds=dt.microsecond)
# check the def fetch_google_fit_data delay in the fetching the data.
def fetch_google_fit_data(creds):
    headers = {'Authorization': f'Bearer {creds.token}'}
    now = datetime.now()

    start_time = int((now - timedelta(hours=2)).timestamp() * 1000)
    end_time = int(now.timestamp() * 1000)

    sources = get_data_sources(creds)
    aggregate_by = [{"dataTypeName": "com.google.step_count.delta"}]

    if any("heart_rate" in ds.get("dataType", {}).get("name", "").lower() for ds in sources):
        aggregate_by.append({"dataTypeName": "com.google.heart_rate.bpm"})
    else:
        st.warning("Heart rate data source not available in Google Fit.")

    spo2_source = next((ds.get("dataType", {}).get("name") for ds in sources if "oxygen_saturation" in ds.get("dataType", {}).get("name", "").lower()), None)
    if spo2_source:
        aggregate_by.append({"dataTypeName": spo2_source})
    else:
        st.warning("SpO2 data source not available in Google Fit.")

    body = {
        "aggregateBy": aggregate_by,
        "bucketByTime": {"durationMillis": 300000},
        "startTimeMillis": start_time,
        "endTimeMillis": end_time
    }

    url = 'https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate'
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=body, timeout=30)
            if response.status_code == 200:
                break
            elif response.status_code == 429:
                st.error("Rate limit exceeded. Retrying after delay...")
                time.sleep(10 * (attempt + 1))
            else:
                st.error(f"Attempt {attempt + 1} failed with status {response.status_code}: {response.text}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                else:
                    return []
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
            else:
                return []

    data = response.json() if response.status_code == 200 else {}
    log_debug(f"API Response: {json.dumps(data, indent=2)}")

    rows = []

    for bucket in data.get("bucket", []):
        start_time_millis = int(bucket.get('startTimeMillis', 0))
        dt_raw = datetime.fromtimestamp(start_time_millis / 1000)
        dt_rounded = round_to_nearest_lower_5min(dt_raw)
        timestamp = dt_rounded.strftime('%Y-%m-%d %H:%M:%S')

        steps = 0
        heart_rate = None
        spo2 = None

        for dataset in bucket.get("dataset", []):
            ds_id = dataset.get("dataSourceId", "").lower()
            for point in dataset.get("point", []):
                value = point.get('value', [{}])[0]
                if "step_count" in ds_id:
                    steps += value.get('intVal', 0)
                elif "heart_rate" in ds_id:
                    heart_rate = value.get('fpVal')
                elif "oxygen_saturation" in ds_id:
                    spo2 = value.get('fpVal')

        row = {
            "Timestamp": timestamp,
            "Steps": steps if steps is not None else 0,
            "Heart Rate (BPM)": round(heart_rate) if heart_rate is not None else None,
            "SpO2 (%)": round(spo2) if spo2 is not None else None
        }
        rows.append(row)

    # Add current 5-min block if missing
    current_5min = round_to_nearest_lower_5min(now)
    if not rows or datetime.strptime(rows[-1]["Timestamp"], '%Y-%m-%d %H:%M:%S') < current_5min:
        rows.append({
            "Timestamp": current_5min.strftime('%Y-%m-%d %H:%M:%S'),
            "Steps": None,
            "Heart Rate (BPM)": None,
            "SpO2 (%)": None
        })

    if any(row["Steps"] or row["Heart Rate (BPM)"] or row["SpO2 (%)"] for row in rows):
        st.info(f"Fetched {len(rows)} data points. Latest timestamp: {rows[-1]['Timestamp']}")
    else:
        st.warning("❗ No valid data received from Google Fit.\n\nPlease ensure:\n- Your wearable is synced with Google Fit.\n- The Google Fit app displays your heart rate, steps, and SpO2.\n- You clicked 'Refresh Now'.")


    # Save to CSV
    if rows:
        new_df = pd.DataFrame(rows)
        if os.path.exists(CSV_FILE):
            old_df = pd.read_csv(CSV_FILE)
            for col in ["Sleep Hours", "Activity"]:
                if col in old_df.columns:
                    old_df = old_df.drop(columns=[col])
            old_df['Timestamp'] = pd.to_datetime(old_df['Timestamp']).apply(round_to_nearest_lower_5min).dt.strftime('%Y-%m-%d %H:%M:%S')
            combined = pd.concat([old_df, new_df], ignore_index=True)
            combined = combined.sort_values(by="Timestamp").drop_duplicates(subset=["Timestamp"], keep="last")
            combined.to_csv(CSV_FILE, index=False)
        else:
            new_df.to_csv(CSV_FILE, index=False)

    return rows

# --- Dashboard Content ---
st.markdown("<div class='content'>", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='dashboard-header'>🩺 Health Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Fetch and Display Data
creds = authenticate_google()
if creds:
    # Fetch data only once per page load
    if st.button("🔄 Refresh Now"):
        st.session_state.data_fetched = fetch_google_fit_data(creds)
    elif "data_fetched" not in st.session_state:
        st.session_state.data_fetched = fetch_google_fit_data(creds)


    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(
                CSV_FILE,
                usecols=['Timestamp', 'Steps', 'Heart Rate (BPM)', 'SpO2 (%)'],
                engine='python',
                on_bad_lines='warn',
                sep=',',
                parse_dates=['Timestamp'],
                skipinitialspace=True
            )
            for col in ["Sleep Hours"]:
                if col in df.columns:
                    df = df.drop(columns=[col])

            if not df.empty:
                df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S')
                df = df.sort_values(by="Timestamp")

                # Get the latest non-null values
                latest_hr_row = df[df["Heart Rate (BPM)"].notna()].tail(1)
                latest_spo2_row = df[df["SpO2 (%)"].notna()].tail(1)

                latest_hr = latest_hr_row["Heart Rate (BPM)"].iloc[0] if not latest_hr_row.empty else None
                # 🔐 Save the latest heart rate in session_state
                if latest_hr is not None:
                     st.session_state.latest_heart_rate = latest_hr
                latest_spo2 = latest_spo2_row["SpO2 (%)"].iloc[0] if not latest_spo2_row.empty else None

                latest = {
                    "Steps": df["Steps"].iloc[-1] if pd.notna(df["Steps"].iloc[-1]) else 0,
                    "Heart Rate (BPM)": latest_hr,
                    "SpO2 (%)": latest_spo2
                }

                # Load the RandomForest model
                try:
                    model = joblib.load(MODEL_FILE)
                    # Prepare input for prediction
                    input_data = [[
                        latest["Steps"],
                        latest["Heart Rate (BPM)"],
                        latest["SpO2 (%)"]
                    ]]
                    # Check if all inputs are valid
                    if all(v is not None for v in input_data[0]):
                        prediction = model.predict(input_data)[0]
                        health_status = "Normal" if prediction == 0 else "Abnormal"
                    else:
                        health_status = "Insufficient Data"
                except FileNotFoundError:
                    st.error(f"Model file '{MODEL_FILE}' not found. Please ensure it exists in the project directory.")
                    health_status = "Model Not Loaded"
                except Exception as e:
                    st.error(f"Error loading model or making prediction: {e}")
                    health_status = "Prediction Error"

                # Latest Metrics
                st.subheader("📊 Latest Health Metrics", anchor=None)
                metric_keys = [key for key in latest.keys() if pd.notna(latest[key])] + ["Health Status"]
                num_metrics = len(metric_keys)
                if num_metrics > 0:
                    metric_cols = st.columns(num_metrics)
                    index = 0
                    for key in metric_keys:
                        with metric_cols[index]:
                            if key == "Health Status":
                                value = health_status
                                icon = "🚨" if health_status == "Abnormal" else "✅"
                            else:
                                value = latest[key]
                                if isinstance(value, float) and value.is_integer():
                                    value = int(value)
                                icon = "👟" if key == "Steps" else "❤" if key == "Heart Rate (BPM)" else "🩺"
                            st.markdown(f"""
                                <div class='metric-card'>
                                    <div class='metric-label'>{icon} {key}</div>
                                    <div class='metric-value'>{value}</div>
                                </div>
                            """, unsafe_allow_html=True)
                        index += 1
                else:
                    st.warning("No health metrics available to display for the latest timestamp.")

                # Data Table with 20 entries
                st.subheader("📋 Latest Health Data", anchor=None)
                display_df = df.tail(20).copy()
                display_df['Timestamp'] = display_df['Timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
                st.dataframe(display_df, use_container_width=True)

                # Trends with 20 entries
                st.subheader("📈 Trends", anchor=None)
                num_entries = len(df)
                if num_entries < 2:
                    st.warning("Not enough data points to plot trends (minimum 2 required).")
                else:
                    entries_to_plot = min(num_entries, 20)

                    if "Steps" in df.columns:
                        fig_steps = px.line(df.tail(entries_to_plot), x="Timestamp", y="Steps", title="Steps Over Time",
                                          line_shape="spline", color_discrete_sequence=["#00f7ff"])
                        fig_steps.update_traces(line=dict(width=4), fill='tozeroy', fillcolor='rgba(0, 247, 255, 0.2)')
                        fig_steps.update_layout(
                            xaxis_title="Time", yaxis_title="Steps", template="plotly_dark",
                            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                            title_font=dict(size=24, color="#39ff14"),
                            xaxis=dict(tickcolor="#00f7ff", gridcolor="rgba(255,255,255,0.1)"),
                            yaxis=dict(tickcolor="#00f7ff", gridcolor="rgba(255,255,255,0.1)")
                        )
                        st.plotly_chart(fig_steps, use_container_width=True)

                    if "Heart Rate (BPM)" in df.columns and df["Heart Rate (BPM)"].notna().any():
                        fig_hr = px.area(df.tail(entries_to_plot), x="Timestamp", y="Heart Rate (BPM)", title="Heart Rate Over Time",
                                        line_shape="spline", color_discrete_sequence=["#ff00e6"])
                        fig_hr.update_traces(line=dict(width=4), fill='tozeroy', fillcolor='rgba(255, 0, 230, 0.2)')
                        fig_hr.update_layout(
                            xaxis_title="Time", yaxis_title="Heart Rate (BPM)", template="plotly_dark",
                            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                            title_font=dict(size=24, color="#39ff14"),
                            xaxis=dict(tickcolor="#ff00e6", gridcolor="rgba(255,255,255,0.1)"),
                            yaxis=dict(tickcolor="#ff00e6", gridcolor="rgba(255,255,255,0.1)")
                        )
                        st.plotly_chart(fig_hr, use_container_width=True)
                    else:
                        st.warning("No valid heart rate data available to plot.")

                    if "SpO2 (%)" in df.columns and df["SpO2 (%)"].notna().any():
                        fig_spo2 = px.line(df.tail(entries_to_plot), x="Timestamp", y="SpO2 (%)", title="SpO2 Over Time",
                                         line_shape="spline", color_discrete_sequence=["#a5d8ff"])
                        fig_spo2.update_traces(line=dict(width=4), fill='tozeroy', fillcolor='rgba(165, 216, 255, 0.2)')
                        fig_spo2.update_layout(
                            xaxis_title="Time", yaxis_title="SpO2 (%)", template="plotly_dark",
                            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                            title_font=dict(size=24, color="#39ff14"),
                            xaxis=dict(tickcolor="#a5d8ff", gridcolor="rgba(255,255,255,0.1)"),
                            yaxis=dict(tickcolor="#a5d8ff", gridcolor="rgba(255,255,255,0.1)")
                        )
                        st.plotly_chart(fig_spo2, use_container_width=True)
                    else:
                        st.warning("No valid SpO2 data available to plot.")
            else:
                st.warning("⚠ No data found in CSV file.")
        except pd.errors.ParserError as e:
            st.error(f"Error parsing CSV file: {e}. Please check the file format.")
        except Exception as e:
            st.error(f"Error reading CSV file: {e}")
    else:
        st.warning("⚠ No data file found. Ensure data is being fetched and saved correctly.")
else:
    st.warning("⚠ Authentication failed. Unable to fetch data.")

st.markdown("</div>", unsafe_allow_html=True)