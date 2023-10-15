mapquest_key = "key"
weather_key = "key"
import requests
city = input("Enter your city: ")
country = input("Enter the country: ")

loc = city+","+country

url = f"https://www.mapquestapi.com/geocoding/v1/address?key={mapquest_key}&location={loc}"

r = requests.get(url)
data = r.json()['results'][0]['locations'][0]['displayLatLng']
lat = data['lat']
lng = data['lng']

print(f"The coords of {loc} are latitude: {lat} and longitude: {lng}")

weather_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={weather_key}&units=metric'

r2 = requests.get(weather_url)
w_data = r2.json()
print(w_data)

data_weather = w_data['weather'][0]
data_temp = w_data['main']

for e, val in data_temp.items():
    print(e+":",val)
