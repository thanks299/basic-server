import requests

def get_location(ip):
    response = requests.get(f"https://ipapi.co/{ip}/json/")
    data = response.json()
    city = data.get('city', 'Unknown')
    return city

def get_temperature(city):
    temp_key = "66e427f591ca401fbf1224257240407"
    response = requests.get(f'https://api.weatherapi.com/v1/current.json?key={temp_key}&q={city}')

    if response.status_code != 200:
        print(f"Error: Received response with status code {response.status_code}")
        return None
    
    data = response.json()
    if "current" not in data:
        print("Error: 'current' key not found in response data")
        return None
    
    temperature = data.get("current").get("temp_c")
    return temperature

