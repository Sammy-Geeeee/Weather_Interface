# This will be all the behind the scenes functions needed to run this program


import requests
import json


def currentWeatherData(location, key):
    # This function will take the location name and the api key, and return all the weather data for this location
    url = f'https://api.weatherbit.io/v2.0/current?&key={key}&city={location}'
    api_response = requests.get(url)
    data = api_response.text
    parsed_json = json.loads(data)

    data_dict = {
        'city_name': parsed_json['data'][0]['city_name'],               # City name "Perth"
        'country_code': parsed_json['data'][0]['country_code'],         # Country code "AU"
        'time_ob': parsed_json['data'][0]['ts'],                        # Time of data retrieval in utc, as a unix timestamp
        'time_local': parsed_json['data'][0]['datetime'],               # Local date and time of the requested location
        'weather': parsed_json['data'][0]['weather']['description'],    # Description of the weather
        'cloud_cover': parsed_json['data'][0]['clouds'],                # Cloud cover %
        'temp': parsed_json['data'][0]['temp'],                         # Actual temp C
        'feels_like': parsed_json['data'][0]['app_temp'],               # Feels like temp C
        'humidity': parsed_json['data'][0]['rh'],                       # Relative humidity %
        'wind_spd': parsed_json['data'][0]['wind_spd'],                 # Wind speed, m\s
        'wind_dir': parsed_json['data'][0]['wind_cdir'],                # Wind direction
        'precip': parsed_json['data'][0]['precip'],                     # Precipitation mm/hr
        'snow': parsed_json['data'][0]['snow'],                         # Snowfall mm/hr
        'uv_index': parsed_json['data'][0]['uv'],                       # UV index, 0-11+
    }

    return data_dict



def dailyWeatherData(location, key):
    # This function will take the location name and the api key, and return all the daily weather data for this location
    url = f' https://api.weatherbit.io/v2.0/forecast/daily?&days=7&key={key}&city={location}'  # Set to 7 days ahead
    api_response = requests.get(url)
    data = api_response.text
    parsed_json = json.loads(data)

    days = []  # Blank list to load all the daily data into

    for day in range(7):  # To iterate through the 7 days of the forecast
        data_dict = {
            'city_name': parsed_json['city_name'],                          # City name "Perth"
            'country_code': parsed_json['country_code'],                    # Country code "AU"     
            'time': parsed_json['data'][day]['ts'],                         # Time of data retrieval in utc as a unix timestamp          
            'sunrise': parsed_json['data'][day]['sunrise_ts'],              # Sunrise time as unix timestamp
            'sunset': parsed_json['data'][day]['sunset_ts'],                # Sunset time as unix timestamp
            'weather': parsed_json['data'][day]['weather']['description'],  # Description of the weather
            'cloud_cover': parsed_json['data'][day]['clouds'],              # Cloud cover %
            'avg_temp': parsed_json['data'][day]['temp'],                   # Average temp C
            'max_temp': parsed_json['data'][day]['max_temp'],               # Max temp C
            'min_temp': parsed_json['data'][day]['min_temp'],               # Min temp C
            'humidity': parsed_json['data'][day]['rh'],                     # Relative humidity %
            'wind_spd': parsed_json['data'][day]['wind_spd'],               # Wind speed, m\s
            'wind_dir': parsed_json['data'][day]['wind_cdir'],              # Wind direction "NW"
            'precip': parsed_json['data'][day]['pop'],                      # Precipitation probability %
            'snow': parsed_json['data'][day]['snow'],                       # accumulated snowfall mm
            'uv_index': parsed_json['data'][day]['uv'],                     # UV index, 0-11+
        }
        days.append(data_dict)

    return days
