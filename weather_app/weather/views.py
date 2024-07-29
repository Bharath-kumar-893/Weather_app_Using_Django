from django.shortcuts import render
import json
import urllib.request
import os

def index(request):
    data = {}
    if request.method == 'POST':
        city = request.POST.get('city', '')
        api_key = os.getenv('OPENWEATHERMAP_API_KEY', 'ca6978305a800a1ce4247dcf24867970')  # Ensure API key is correct
        api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

        print(f"API URL: {api_url}")  # Debugging line to verify URL

        try:
            with urllib.request.urlopen(api_url) as response:
                source = response.read()
                list_of_data = json.loads(source)

                print(f"API Response: {list_of_data}")  # Debugging line to see the API response

                # Convert temperature from Kelvin to Celsius
                temp_kelvin = list_of_data['main']['temp']
                temp_celsius = temp_kelvin - 273.15

                # Data for template
                data = {
                    "country_code": list_of_data['sys']['country'],
                    "coordinate": f"{list_of_data['coord']['lon']} {list_of_data['coord']['lat']}",
                    "temp": f"{temp_celsius:.2f}°C",
                    "pressure": str(list_of_data['main']['pressure']),
                    "humidity": str(list_of_data['main']['humidity']),
                }
        except urllib.error.HTTPError as e:
            print(f"HTTPError: {e}")  # Debugging line for HTTPError
            if e.code == 401:
                data = {"error": "Unauthorized: Invalid API key."}
            else:
                data = {"error": str(e)}
        except Exception as e:
            print(f"Exception: {e}")  # Debugging line for general exceptions
            data = {"error": str(e)}

    print(f"Data to be rendered: {data}")  # Debugging line to see the data being passed to the template

    return render(request, "index.html", data)
