#  PART 1: Importing Tools((called libraries))

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
from dotenv import load_dotenv
import os

# PART 2: Set the API and URL
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

# Set your API key here
load_dotenv()  # Load variables from .env file
API_KEY = os.getenv("OPENWEATHER_API_KEY")


# PART 3: Get City from Your IP
def get_city_from_ip():
    try:
        ip_info = requests.get("https://ipinfo.io").json()
        return ip_info.get("city", "New York")
    except:
        return "New York"  # fallback default
    

# PART 4: Get Weather Data for a City (Gets weather data from the internet)
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

# # PART 5: Organize the Weather Data (Organizes it in a table)
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
st.set_page_config(page_title="Dynamic Weather Dashboard", layout="centered")
st.title("Dynamic Weather Dashboard")

# PART 7:Get default city from IP location ( Choose the City ( Lets you enter/select a city))
default_city = get_city_from_ip()
city = st.text_input("Enter city name:", default_city)


# PART 8: Show Weather Info (Shows current weather)
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
        df = parse_forecast(data)

        st.subheader("5-Day Forecast Trends")

        # Tabs for different weather trends
        tabs = st.tabs(["Temperature", "Humidity", "Pressure", "Wind Speed"])

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