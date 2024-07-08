#!/usr/bin/python3

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Function to get the location from the IP address
def get_location(ip):
    response = requests.get(f"https://ipapi.co/54.152.54.130/json/")
    data = response.json()
    city = data.get('city', 'Unknown')
    return city

# Function to get the temperature for a given city
def get_temperature(city):
    # Replace with your weather API key
    temp_key = "66e427f591ca401fbf1224257240407"

    # Example API call to get current weather
    response = requests.get(f'https://api.weatherapi.com/v1/current.json?key={temp_key}&q={city}')

    # Check if the response is successful
    if response.status_code != 200:
        # Log the error or handle it accordingly
        print(f"Error: Received response with status code {response.status_code}")
        return None
    
    data = response.json()
    # Check if the 'current' key exists in the data
    if "current" not in data:
        # Log the error or handle it accordingly
        print("Error: 'current' key not found in response data")
        return None
    
    temperature = data.get("current").get("temp_c")
    return temperature

# API endpoint to greet the visitor and provide weather information
B@app.route('/api/hello', methods=['GET'])
def hello():
    # Determine the client's IP address
    if "X-Forwarded-For" in request.headers:
        client_ip = request.headers.getlist('X-Forwarded-For')[0]
    else:
        client_ip = request.remote_addr

    # Get visitor's name from query parameters
    visitor_name = request.args.get('visitor_name', 'Guest')
    
    # Get the location based on the IP address
    location = get_location(client_ip)    
    # Get the temperature for the location
    temperature = get_temperature(location)
    
    # Create the greeting message
    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {location}"
    # Create the response object
    response = {
        "client_ip": client_ip,
        "location": location,
        "greeting": greeting
    }
    
    # Return the response as JSON
    return jsonify(response)
