import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define API configurations
# 🔒 Security Best Practice: Never hardcode secrets. Use environment variables.
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather_data(city):
    """
    Fetches raw weather data from OpenWeatherMap API.
    Returns a dictionary with weather details or None if an error occurs.
    """
    if not API_KEY:
        print("❌ Error: API Key is missing. Please check your .env file.")
        return None

    try:
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric' 
        }
        # Added timeout to prevent hanging on slow connections
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()  

        return response.json()

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            print("❌ Authentication Error: Invalid API Key.")
        elif response.status_code == 404:
            print(f"❌ City '{city}' not found. Please check the spelling.")
        else:
            print(f"⚠️ HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError:
        print("❌ Network Error: Please check your internet connection.")
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: The server took too long to respond.")
    except requests.exceptions.RequestException as req_err:
        print(f"⚠️ Request error occurred: {req_err}")
    
    return None

def display_weather(data, city):
    """
    Formats and prints the weather data to the console.
    """
    if not data:
        return

    try:
        weather_desc = data['weather'][0]['description'].capitalize()
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']

        print("\n" + "="*30)
        print(f"🌤️  Weather in {city.title()}")
        print("="*30)
        print(f"  Description : {weather_desc}")
        print(f"  Temperature : {temp}°C")
        print(f"  Feels Like  : {feels_like}°C")
        print(f"  Humidity    : {humidity}%")
        print("="*30 + "\n")
        
    except KeyError:
        print("❌ Error: Could not parse weather data. The API response format may have changed.")

def main():
    """
    Main application loop with input validation.
    """
    print("🌙 Welcome to Moon Weather App!")
    print("Type 'exit' to quit.\n")
    
    while True:
        city = input("Enter the city name: ").strip()
        
        if not city:
            print("⚠️ Input cannot be empty. Please try again.\n")
            continue
            
        if city.lower() == 'exit':
            print("👋 Goodbye! Stay safe and sustainable.")
            break
            
        data = get_weather_data(city)
        if data:
            display_weather(data, city)

if __name__ == "__main__":
    main()
