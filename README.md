# 🌦️ Dynamic Weather Dashboard using Python, Pandas & OpenWeather API

## 📄 Description

A data-driven dashboard that allows users to search for any city and retrieve current weather conditions along with a 5-day forecast. Built with **Python**, **Pandas**, and **Streamlit**, the app fetches real-time data from the **OpenWeatherMap API** and visualizes it using **Plotly**. It provides dynamic, interactive time-series plots for temperature and humidity, with clean UI and error handling for invalid inputs.

---

## 🧰 Tech Stack

- Python 3.7+
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Requests](https://docs.python-requests.org/)
- [Plotly](https://plotly.com/python/)
- [OpenWeatherMap API](https://openweathermap.org/api)

---

## 🚀 Features

- 🌍 Search weather by city name
- 📅 View 5-day forecast (3-hour intervals)
- 📈 Interactive time-series plots for temperature and humidity
- 🧹 Clean and user-friendly interface
- ⚠️ Error handling for invalid city names or API limits
- 🌐 Add location-based auto-detection
- 📊 Add more weather metrics (wind speed, pressure, etc.)

---

## 🔑 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/weather-dashboard.git
cd weather-dashboard

✅ If you’re working in a virtual environment (recommended):
Activate your virtual environment
For example:
# Windows
.\venv\Scripts\activate

### Install packages as needed
pip install streamlit pandas requests plotly

### Generate the requirements.txt file
pip freeze > requirements.txt

### Get Your OpenWeatherMap API Key

Sign up at OpenWeatherMap
Go to your dashboard and copy your API key

### Run the App

streamlit run weather_dashboard.py

## CODE:

'''
This code creates a web app that:
Shows the current weather and a 5-day forecast (like temperature, humidity, etc.) for any city you type in.
Automatically fills in your city using your IP address.
Plots nice interactive graphs using Plotly.
'''

#  PART 1: Importing Tools((called libraries))
'''
streamlit: Makes the web app.
requests: Talks to the weather API (to get weather data).
pandas: Organizes data into tables.
plotly.express: Creates beautiful graphs.
datetime: Handles date and time info.
'''

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# PART 2: Set the API and URL
'''
Where to get the weather data from (OpenWeather API).
Our access key (API key) that allows us to fetch the data.
'''

BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"
API_KEY = 'YOUR API KEY'

# PART 3: Get City from Your IP
'''
This function tries to guess your city using your internet location (IP address). 
If it can’t, it uses “New York” as a backup.
'''
def get_city_from_ip():
    try:
        ip_info = requests.get("https://ipinfo.io").json()
        return ip_info.get("city", "New York")
    except:
        return "New York"  # fallback default

# PART 4: Get Weather Data for a City (Gets weather data from the internet)
'''
This function:
Sends a request to the weather website (API) with your city and key.
If it works, it returns the weather data.
If not, it shows an error message.
'''
def get_weather_data(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("City not found or API limit reached.")
        return None

# PART 5: Organize the Weather Data (Organizes it in a table)
'''
This turns the raw weather data into a clean table with:
Date & time
Temperature
Humidity
Pressure
Wind speed
'''
def parse_forecast(json_data):
    forecast_list = json_data['list']
    df = pd.DataFrame([{
        'datetime': datetime.fromtimestamp(item['dt']),
        'temperature': item['main']['temp'],
        'humidity': item['main']['humidity'],
        'pressure': item['main']['pressure'],
        'wind_speed': item['wind']['speed']
    } for item in forecast_list])
    return df

# PART 6: Create the Web App Interface (Builds the app layout)
# This sets up the title and basic layout of the app.

st.set_page_config(page_title="🌦️ Dynamic Weather Dashboard", layout="centered")
st.title("🌦️ Dynamic Weather Dashboard")

# PART 7: Choose the City ( Lets you enter/select a city)
'''
This shows a text box where you can type your city. 
It auto-fills with your city name (if detected from IP).
'''
default_city = get_city_from_ip()
city = st.text_input("Enter city name:", default_city)

# PART 8: Show Weather Info (Shows current weather)
'''
If there’s a city name:
It gets the weather for that city.
Shows a summary of current weather (like a weather app).
'''

if city:
    data = get_weather_data(city)
    if data:
        st.subheader(f"Current Weather in {city}")
        current = data['list'][0]

        # Display key metrics
        st.metric("Temperature (°C)", f"{current['main']['temp']}°C")
        st.metric("Humidity (%)", f"{current['main']['humidity']}%")
        st.metric("Pressure (hPa)", f"{current['main']['pressure']} hPa")
        st.metric("Wind Speed (m/s)", f"{current['wind']['speed']} m/s")

        # PART 9: Show Forecast Graphs (Displays nice graphs)
        '''
        This:
        Converts the forecast into a table.
        Shows tabs with interactive line graphs of:
            🌡️ Temperature
            💧 Humidity
            🔽 Pressure
            🍃 Wind Speed

        '''
        df = parse_forecast(data)

        st.subheader("📈 5-Day Forecast Trends")

        # Tabs for different weather trends
        tabs = st.tabs(["🌡️ Temperature", "💧 Humidity", "🔽 Pressure", "🍃 Wind Speed"])

        with tabs[0]:
            fig1 = px.line(df, x='datetime', y='temperature', title='Temperature Over Time')
            st.plotly_chart(fig1, use_container_width=True)

        with tabs[1]:
            fig2 = px.line(df, x='datetime', y='humidity', title='Humidity Over Time')
            st.plotly_chart(fig2, use_container_width=True)

        with tabs[2]:
            fig3 = px.line(df, x='datetime', y='pressure', title='Pressure Over Time')
            st.plotly_chart(fig3, use_container_width=True)

        with tabs[3]:
            fig4 = px.line(df, x='datetime', y='wind_speed', title='Wind Speed Over Time')
            st.plotly_chart(fig4, use_container_width=True)



