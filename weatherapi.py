import requests


def weather_data(city):
    api_key = '9314352a486f4453fd7bdb57844cda91'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed = data['wind']['speed']
        wind_direction = data['wind']['deg']

        # print(data)
        print(f'Weather in {city}:')
        print("-" * 20)
        print(f'Description: {weather_description}')
        print(f'Temperature: {temperature}°C')
        print(f'Feels Like: {feels_like}°C')
        print(f'Wind Speed: {wind_speed} m/s')
        print(f'Wind Direction: {wind_direction}°')
        print(f'Humidity: {humidity}%')
        print(f'Pressure: {pressure} hPa')
        return f'Pressure: {pressure} hPa'
    else:
        print('Error:', response.status_code)


if __name__ == "__main__":
    weather_data()