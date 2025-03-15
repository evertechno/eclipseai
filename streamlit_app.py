import streamlit as st
import google.generativeai as genai
import datetime
import math
import requests

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

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

def calculate_planetary_positions(year, month, day, hour, minute):
    sun_position = (day + month * 30 + year * 365) % 360
    moon_position = (day * 12 + hour / 2 + minute / 120) % 360
    return {"Sun": sun_position, "Moon": moon_position}

def generate_horoscope_ai(zodiac_sign, planetary_positions):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Generate a horoscope for {zodiac_sign} with Sun at {planetary_positions['Sun']} and Moon at {planetary_positions['Moon']}. Focus on general life advice, career, and relationships."
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating horoscope: {e}"

st.title("Horoscope Analysis with AI")

birth_date = st.date_input("Enter your birth date:", datetime.date(1990, 1, 1))
birth_time = st.time_input("Enter your birth time:", datetime.time(12, 0))

day = birth_date.day
month = birth_date.month
year = birth_date.year
hour = birth_time.hour
minute = birth_time.minute

zodiac_sign = calculate_zodiac_sign(day, month)
planetary_positions = calculate_planetary_positions(year, month, day, hour, minute)

if st.button("Get Horoscope"):
    st.write(f"Your Zodiac Sign: {zodiac_sign}")
    st.write(f"Planetary Positions (Simplified): {planetary_positions}")

    horoscope = generate_horoscope_ai(zodiac_sign, planetary_positions)
    st.write("Horoscope:")
    st.write(horoscope)

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

st.subheader("Calculate Your Age")
if st.button("Calculate Age"):
    today = datetime.date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    st.write(f"Your Age: {age} years")

zodiac_traits = {
    "Aries": "Courageous, determined, confident",
    "Taurus": "Reliable, patient, practical",
    "Gemini": "Gentle, affectionate, curious",
    "Cancer": "Tenacious, highly imaginative, loyal",
    "Leo": "Creative, passionate, generous",
    "Virgo": "Loyal, analytical, kind",
    "Libra": "Cooperative, diplomatic, gracious",
    "Scorpio": "Resourceful, brave, passionate",
    "Sagittarius": "Generous, idealistic, great sense of humor",
    "Capricorn": "Responsible, disciplined, self-control",
    "Aquarius": "Progressive, original, independent",
    "Pisces": "Compassionate, artistic, intuitive"
}
if zodiac_sign in zodiac_traits:
    st.write(f"Personality Traits for {zodiac_sign}: {zodiac_traits[zodiac_sign]}")

st.subheader("Compatibility Check")
partner_zodiac_sign = st.selectbox("Select your partner's zodiac sign:", list(zodiac_traits.keys()))
if st.button("Check Compatibility"):
    compatibility = f"{zodiac_sign} and {partner_zodiac_sign} compatibility is high!" 
    st.write(compatibility)

lucky_numbers = {
    "Aries": [1, 8, 17],
    "Taurus": [2, 6, 9],
    "Gemini": [3, 7, 12],
    "Cancer": [2, 7, 11],
    "Leo": [1, 4, 9],
    "Virgo": [5, 14, 23],
    "Libra": [6, 15, 24],
    "Scorpio": [8, 11, 18],
    "Sagittarius": [3, 12, 21],
    "Capricorn": [4, 8, 13],
    "Aquarius": [4, 7, 11],
    "Pisces": [3, 9, 12]
}
if zodiac_sign in lucky_numbers:
    st.write(f"Lucky Numbers for {zodiac_sign}: {lucky_numbers[zodiac_sign]}")

st.subheader("Daily Horoscope")
if st.button("Get Daily Horoscope"):
    try:
        response = requests.post(f"https://aztro.sameerkumar.website/?sign={zodiac_sign.lower()}&day=today")
        if response.status_code == 200:
            daily_horoscope = response.json()
            st.write(f"Today's Horoscope for {zodiac_sign}: {daily_horoscope['description']}")
        else:
            st.error(f"Error fetching daily horoscope: {response.status_code}")
    except Exception as e:
        st.error(f"Error fetching daily horoscope: {e}")

st.subheader("Chinese Zodiac Sign")
chinese_zodiac = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"]
chinese_zodiac_sign = chinese_zodiac[(year - 4) % 12]
st.write(f"Your Chinese Zodiac Sign: {chinese_zodiac_sign}")

zodiac_elements = {
    "Aries": "Fire",
    "Taurus": "Earth",
    "Gemini": "Air",
    "Cancer": "Water",
    "Leo": "Fire",
    "Virgo": "Earth",
    "Libra": "Air",
    "Scorpio": "Water",
    "Sagittarius": "Fire",
    "Capricorn": "Earth",
    "Aquarius": "Air",
    "Pisces": "Water"
}
if zodiac_sign in zodiac_elements:
    st.write(f"Element for {zodiac_sign}: {zodiac_elements[zodiac_sign]}")

affirmations = {
    "Aries": "I am confident and fearless.",
    "Taurus": "I am grounded and patient.",
    "Gemini": "I am curious and adaptable.",
    "Cancer": "I am nurturing and compassionate.",
    "Leo": "I am creative and passionate.",
    "Virgo": "I am analytical and kind.",
    "Libra": "I am diplomatic and fair-minded.",
    "Scorpio": "I am passionate and resourceful.",
    "Sagittarius": "I am adventurous and optimistic.",
    "Capricorn": "I am disciplined and responsible.",
    "Aquarius": "I am innovative and independent.",
    "Pisces": "I am intuitive and compassionate."
}
if zodiac_sign in affirmations:
    st.write(f"Daily Affirmation for {zodiac_sign}: {affirmations[zodiac_sign]}")

st.subheader("Historical Events on Your Birthday")
if st.button("Get Historical Events"):
    try:
        response = requests.get(f"https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/all/{month}/{day}")
        events = response.json()['events']
        st.write(f"Historical Events on {month}/{day}:")
        for event in events[:5]:
            st.write(f"{event['year']}: {event['text']}")
    except Exception as e:
        st.error(f"Error fetching historical events: {e}")

st.subheader("Moon Phase on Your Birthday")
if st.button("Get Moon Phase"):
    try:
        response = requests.get(f"https://api.farmsense.net/v1/moonphases/?d={year}-{month}-{day}")
        moon_phase = response.json()[0]['Phase']
        st.write(f"Moon Phase on {birth_date}: {moon_phase}")
    except Exception as e:
        st.error(f"Error fetching moon phase: {e}")

st.subheader("Planetary Influences")
if st.button("Get Planetary Influences"):
    st.write(f"Planetary Influences on {zodiac_sign}:")
    st.write(f"Sun at {planetary_positions['Sun']} degrees")
    st.write(f"Moon at {planetary_positions['Moon']} degrees")

st.subheader("Personalized Health Tips")
health_tips = {
    "Aries": "Stay active and eat a balanced diet.",
    "Taurus": "Take time to relax and avoid stress.",
    "Gemini": "Engage in mental exercises and social activities.",
    "Cancer": "Maintain emotional balance and a healthy diet.",
    "Leo": "Keep up with physical exercise and creative outlets.",
    "Virgo": "Focus on digestive health and mental clarity.",
    "Libra": "Balance your diet and stay hydrated.",
    "Scorpio": "Practice stress management and stay physically active.",
    "Sagittarius": "Maintain an active lifestyle and positive mindset.",
    "Capricorn": "Focus on bone health and regular check-ups.",
    "Aquarius": "Engage in physical activities and mental relaxation.",
    "Pisces": "Take care of your feet and practice mindfulness."
}
if zodiac_sign in health_tips:
    st.write(f"Health Tips for {zodiac_sign}: {health_tips[zodiac_sign]}")

st.subheader("Financial Advice")
financial_advice = {
    "Aries": "Invest in your passions and be bold.",
    "Taurus": "Save consistently and avoid impulsive spending.",
    "Gemini": "Diversify your investments and stay informed.",
    "Cancer": "Plan for the future and secure your home.",
    "Leo": "Invest in creative ventures and save for luxury.",
    "Virgo": "Stick to a budget and invest in practical assets.",
    "Libra": "Balance your spending and saving habits.",
    "Scorpio": "Take calculated risks and invest in security.",
    "Sagittarius": "Seek financial freedom and invest wisely.",
    "Capricorn": "Focus on long-term investments and savings.",
    "Aquarius": "Invest in innovative ideas and technology.",
    "Pisces": "Plan for the future and avoid financial escapism."
}
if zodiac_sign in financial_advice:
    st.write(f"Financial Advice for {zodiac_sign}: {financial_advice[zodiac_sign]}")

st.subheader("Recommended Travel Destinations")
travel_destinations = {
    "Aries": ["New Zealand", "Japan", "Iceland"],
    "Taurus": ["Italy", "Greece", "Provence"],
    "Gemini": ["USA", "Germany", "Australia"],
    "Cancer": ["Bali", "Scotland", "Portugal"],
    "Leo": ["France", "Spain", "Brazil"],
    "Virgo": ["Switzerland", "Canada", "Norway"],
    "Libra": ["France", "Argentina", "South Africa"],
    "Scorpio": ["Egypt", "Morocco", "Peru"],
    "Sagittarius": ["Thailand", "Mexico", "Australia"],
    "Capricorn": ["UK", "China", "Russia"],
    "Aquarius": ["Sweden", "South Korea", "Finland"],
    "Pisces": ["India", "Indonesia", "New Zealand"]
}
if zodiac_sign in travel_destinations:
    st.write(f"Recommended Travel Destinations for {zodiac_sign}: {travel_destinations[zodiac_sign]}")

st.subheader("Relationship Advice")
relationship_advice = {
    "Aries": "Be direct and honest in your communication.",
    "Taurus": "Show appreciation and affection regularly.",
    "Gemini": "Keep things exciting and be adaptable.",
    "Cancer": "Nurture your relationships and be supportive.",
    "Leo": "Be generous and express your love openly.",
    "Virgo": "Pay attention to details and be considerate.",
    "Libra": "Maintain balance and harmony in your relationships.",
    "Scorpio": "Build trust and be passionate.",
    "Sagittarius": "Keep an open mind and be adventurous.",
    "Capricorn": "Be reliable and show your commitment.",
    "Aquarius": "Give space and value freedom.",
    "Pisces": "Be empathetic and understanding."
}
if zodiac_sign in relationship_advice:
    st.write(f"Relationship Advice for {zodiac_sign}: {relationship_advice[zodiac_sign]}")

st.subheader("Career Advice")
career_advice = {
    "Aries": "Take the lead and pursue new challenges.",
    "Taurus": "Focus on stability and long-term goals.",
    "Gemini": "Embrace change and continuous learning.",
    "Cancer": "Use your intuition and nurture your career.",
    "Leo": "Showcase your talents and be confident.",
    "Virgo": "Be detail-oriented and strive for perfection.",
    "Libra": "Work on collaboration and diplomacy.",
    "Scorpio": "Be passionate and strategic.",
    "Sagittarius": "Seek adventure and growth opportunities.",
    "Capricorn": "Be disciplined and aim for the top.",
    "Aquarius": "Innovate and think outside the box.",
    "Pisces": "Use your creativity and empathy."
}
if zodiac_sign in career_advice:
    st.write(f"Career Advice for {zodiac_sign}: {career_advice[zodiac_sign]}")

st.subheader("Inspirational Quotes")
quotes = {
    "Aries": "The only way to do great work is to love what you do. - Steve Jobs",
    "Taurus": "The best preparation for tomorrow is doing your best today. - H. Jackson Brown Jr.",
    "Gemini": "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
    "Cancer": "The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt",
    "Leo": "Believe you can and you're halfway there. - Theodore Roosevelt",
    "Virgo": "Success is not the key to happiness. Happiness is the key to success. - Albert Schweitzer",
    "Libra": "Happiness is not something ready-made. It comes from your own actions. - Dalai Lama",
    "Scorpio": "The best way to predict the future is to create it. - Abraham Lincoln",
    "Sagittarius": "You miss 100% of the shots you don't take. - Wayne Gretzky",
    "Capricorn": "Hard work beats talent when talent doesn't work hard. - Tim Notke",
    "Aquarius": "The only way to achieve the impossible is to believe it is possible. - Charles Kingsleigh",
    "Pisces": "The best and most beautiful things in the world cannot be seen or even touched - they must be felt with the heart. - Helen Keller"
}
if zodiac_sign in quotes:
    st.write(f"Inspirational Quote for {zodiac_sign}: {quotes[zodiac_sign]}")

st.subheader("Birthstone Information")
birthstones = {
    "January": "Garnet",
    "February": "Amethyst",
    "March": "Aquamarine",
    "April": "Diamond",
    "May": "Emerald",
    "June": "Pearl",
    "July": "Ruby",
    "August": "Peridot",
    "September": "Sapphire",
    "October": "Opal",
    "November": "Topaz",
    "December": "Turquoise"
}
birth_month = birth_date.strftime("%B")
if birth_month in birthstones:
    st.write(f"Your Birthstone: {birthstones[birth_month]}")

st.subheader("Famous Birthdays on Your Date")
if st.button("Get Famous Birthdays"):
    try:
        response = requests.get(f"https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/births/{month}/{day}")
        birthdays = response.json()['births']
        st.write(f"Famous Birthdays on {month}/{day}:")
        for birthday in birthdays[:5]:
            st.write(f"{birthday['year']}: {birthday['text']}")
    except Exception as e:
        st.error(f"Error fetching famous birthdays: {e}")
