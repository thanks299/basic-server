from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Function to get the location from the IP address
def get_location(ip):
    response = requests.get(f"https://ipapi.co/{ip}/json/")
    data = response.json()
    city = data.get('city', 'Unknown')
    return city

# Function to get the temperature for a given city
def get_temperature(city):
    # Get the weather API key from environment variables
    temp_key = os.getenv('WEATHER_API_KEY')

    # Example API call to get current weather
    response = requests.get(f'https://api.weatherapi.com/v1/current.json?key={temp_key}&q={city}')

    # Check if the response is successful
    if response.status_code != 200:
        print(f"Error: Received response with status code {response.status_code}")
        return None

    data = response.json()
    if "current" not in data:
        print("Error: 'current' key not found in response data")
        return None

    temperature = data.get("current").get("temp_c")
    return temperature

# API endpoint to greet the visitor and provide weather information
@app.route('/api/hello', methods=['GET'])
def hello():
    if "X-Forwarded-For" in request.headers:
        client_ip = request.headers.getlist('X-Forwarded-For')[0]
    else:
        client_ip = request.remote_addr

    visitor_name = request.args.get('visitor_name', 'Guest')
    location = get_location(client_ip)
    temperature = get_temperature(location)

    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {location}"
    response = {
        "client_ip": client_ip,
        "location": location,
        "greeting": greeting
    }

    return jsonify(response)

# Adapt the Flask app to Vercel's serverless environment
def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    app.run(debug=True)

