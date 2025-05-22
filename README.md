# wearable_health_monitoring_ai
Wearable Health Monitoring [Intern: Swati Londhe, Mentor: Bhagyesh]

# Overview
The **Wearable Health Monitoring System** is an AI/ML-based real-time health monitoring solution that collects data from smartwatches (via Google Fit API), analyzes it using machine learning models, and provides insights and emergency alerts to users and their family members. The project is designed to help users track vital signs and detect health anomalies proactively.

## 💡 Key Features
- 🔄 Real-time data fetching from Google Fit API
- 📊 Streamlit dashboard with:
  - Heart Rate Monitoring
  - SpO2 Levels
  - Step Count Tracking
- 🧠 ML-based Health Analysis:
  - **Random Forest** for Health Status
- 💬 Emergency notifications via WhatsApp, Email, and SMS
- 🗃 Stores health data in **CSV** and **SQLite database**

## 🔧 Technologies Used
- **Frontend**: Streamlit
- **Backend**: Python, SQLite
- **APIs**: Google Fit API (OAuth2.0 authentication)
- **ML Models**:  Random Forest


## 📂 Project Structure
wearable_health_monitoring_ai/
├── main.py # Main Streamlit app
├── pages/ # Streamlit multi-page components
├── models/ # Trained ML models
├── health.csv # Realtime data log
├── health_data.db # SQLite database for health data
├── credentials.json # Google OAuth2 credentials
├── token.json # Access token for Google Fit
├── users.db # User login/auth data
├── README.md # Project README file
└── requirements.txt # Python dependencies


## 🚀 Getting Started

 1. Clone the repository
```bash
git clone https://github.com/your-username/wearable_health_monitoring_ai.git
cd wearable_health_monitoring_ai
2. Install dependencies
   pip install -r requirements.txt

3. Set up Google Fit API
  1. Create a Google Cloud Project
    Go to Google Cloud Console.
    Click on "New Project".
    Enter a Project Name (e.g., HealthMonitorApp) and click "Create".

📦 2. Enable Google Fit API
    With your project selected, go to:
    Google Fit API Library
    Click “Enable”.

🔐 3. Set Up OAuth 2.0 Credentials
    1.Navigate to APIs & Services → Credentials.
    2.Click “Create Credentials” → “OAuth 2.0 Client ID”.
    3. Configure consent screen if prompted:
        User Type: External
        Fill in basic info (App name, Support email, etc.)
        Scopes: Add the required Google Fit scopes (listed below)
        Test Users: Add your Gmail account
    4.Go back to Create OAuth Client ID:
        Application type: Desktop app (or Web App for deployed apps)
        Name: FitAPIClient
        Click Create
   5. Click Download JSON — this is your credentials.json

🔑 4. Required OAuth Scopes for Google Fit
      Here are commonly used scopes:
      https://www.googleapis.com/auth/fitness.activity.read
      https://www.googleapis.com/auth/fitness.heart_rate.read
      https://www.googleapis.com/auth/fitness.sleep.read
      https://www.googleapis.com/auth/fitness.body.read
      Add these during the OAuth consent screen setup

4. Run the Streamlit App
 streamlit run main.py

5. Use Cases
 Continuous remote patient monitoring
 Elderly care and fall detection
 Personal health and fitness tracking

6. Future Enhancements
 Integration with Apple HealthKit and Samsung Health
 Role-based dashboards for patients and doctors
 Historical analytics and cloud dashboard
 Mobile app support


