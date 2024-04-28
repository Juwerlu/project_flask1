from flask import current_app
import requests


def get_weather_by_city(city):
    url = 'http://api.worldweatheronline.com/premium/v1/weather.ashx'
    params = {
        'key': current_app.config['WEATHER_API_KEY'],
        'q': city,
        'format': 'json',
        'num_of_days': 1,
        'lang': 'ru',
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        response = response.json()
    except (requests.RequestException, ValueError):
        return False
    if 'data' in response:
        if 'current_condition' in response['data']:
            try:
                weather = response['data']['current_condition'][0]
                return weather
            except (TypeError, IndexError):
                return False
    return False


if __name__ == '__main__':
    get_weather_by_city('russia,moscow')
