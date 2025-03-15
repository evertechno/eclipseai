import streamlit as st
import google.generativeai as genai
import datetime
import math

# Configure the API key securely from Streamlit's secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Function to calculate zodiac sign
def calculate_zodiac_sign(day, month):
    if (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "Pisces"
    elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius"

# Function to calculate planetary positions (simplified)
def calculate_planetary_positions(year, month, day, hour, minute):
    # Simplified calculations for demonstration
    # In a real app, use a proper astronomical library
    sun_position = (day + month * 30 + year * 365) % 360
    moon_position = (day * 12 + hour / 2 + minute / 120) % 360
    return {"Sun": sun_position, "Moon": moon_position}

# Function to generate horoscope using AI
def generate_horoscope_ai(zodiac_sign, planetary_positions):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Generate a horoscope for {zodiac_sign} with Sun at {planetary_positions['Sun']} and Moon at {planetary_positions['Moon']}. Focus on general life advice, career, and relationships."
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating horoscope: {e}"

# Streamlit App UI
st.title("Horoscope Analysis with AI")

# Date and time input
birth_date = st.date_input("Enter your birth date:", datetime.date(1990, 1, 1))
birth_time = st.time_input("Enter your birth time:", datetime.time(12, 0))

# Calculate zodiac sign and planetary positions
if st.button("Get Horoscope"):
    day = birth_date.day
    month = birth_date.month
    year = birth_date.year
    hour = birth_time.hour
    minute = birth_time.minute

    zodiac_sign = calculate_zodiac_sign(day, month)
    planetary_positions = calculate_planetary_positions(year, month, day, hour, minute)

    st.write(f"Your Zodiac Sign: {zodiac_sign}")
    st.write(f"Planetary Positions (Simplified): {planetary_positions}")

    # Generate and display horoscope using AI
    horoscope = generate_horoscope_ai(zodiac_sign, planetary_positions)
    st.write("Horoscope:")
    st.write(horoscope)

# Enhanced AI features (example: asking specific questions)
st.subheader("Ask AI a Question Related to Your Horoscope")
question = st.text_input("Enter your question:", "What are my career prospects based on my horoscope?")

if st.button("Ask AI"):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Based on the horoscope generated for {zodiac_sign}, with sun at {planetary_positions['Sun']} and moon at {planetary_positions['Moon']}, answer the following question: {question}"
    try:
        response = model.generate_content(prompt)
        st.write("AI Response:")
        st.write(response.text)
    except Exception as e:
        st.error(f"Error: {e}")
