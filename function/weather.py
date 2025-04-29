import requests

class WeatherForecast:
    """
    A class to retrieve weather forecasts using Open Meteo APIs.

    Methods:
        get_position(city): Retrieves the latitude and longitude of a given city.
        get_weather(city='milan'): Retrieves the weather forecast for a given city.

    Example:
        weather_forecast = WeatherForecast()
        weather_data = weather_forecast.get_weather('New York')
        print(weather_data)
    """

    def get_position(self, city):
        """
        Retrieves the latitude and longitude of a given city.

        Args:
            city (str): The name of the city.

        Returns:
            tuple: A tuple containing latitude and longitude.
        """
        self.url = "https://geocoding-api.open-meteo.com/v1/search"
        self.params = {
            'name': city,
            'format': 'json',
            'count': '1',
            'language': 'en'
        }
        resp = requests.get(url=self.url, params=self.params)
        data = resp.json()
        return data['results'][0]['latitude'], data['results'][0]['longitude']

    def get_weather(self, city='milan'):
        """
        Retrieves the weather forecast for a given city.

        Args:
            city (str, optional): The name of the city. Defaults to 'milan'.

        Returns:
            tuple: A tuple containing high temperature, low temperature, average precipitation probability,
                   and average wind speed.
        """
        try:
            latitude, longitude = self.get_position(city)

            self.url = "https://api.open-meteo.com/v1/forecast?"
            self.params = {
                'latitude': latitude,
                'longitude': longitude,
                'hourly': 'temperature_2m,precipitation_probability,wind_speed_10m',
                'forecast_days': '1'
            }
            resp = requests.get(url=self.url, params=self.params)
            data = resp.json()
            high_temp = max(data['hourly']['temperature_2m'])
            low_temp = min(data['hourly']['temperature_2m'])
            ave_pre = sum(data['hourly']['precipitation_probability']) / len(data['hourly']['precipitation_probability'])
            ave_wind = sum(data['hourly']['wind_speed_10m']) / len(data['hourly']['wind_speed_10m'])
            return (high_temp, low_temp, ave_pre, ave_wind)
        except:
            return (None, None, None, None)
