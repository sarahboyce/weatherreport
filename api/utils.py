from dataclasses import dataclass

import requests
from django.conf import settings
from django.core.cache import cache
from django.utils.functional import cached_property
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from . import config


@dataclass
class CitySearch:
    city_name: str
    lang: str

    @cached_property
    def cache_key(self):
        return slugify(f"{self.city_name}_{self.lang}")


def _get_data_open_weather_api(response):
    """
    Given the open weather api data, return a dictionary of only the required data
    Format the wind direction into N/E/S/W
    Format the description to be title case for nice rendering in template
    """

    wind_deg = response["wind"]["deg"]
    if 45 < wind_deg <= 135:
        wind_direction = config.EAST
    elif 135 < wind_deg <= 225:
        wind_direction = config.SOUTH
    elif 225 < wind_deg <= 315:
        wind_direction = config.WEST
    else:
        wind_direction = config.NORTH

    return {
        "description": response["weather"][0]["description"].title(),
        "icon": response["weather"][0]["icon"],
        "temp": response["main"]["temp"],
        "temp_min": response["main"]["temp_min"],
        "temp_max": response["main"]["temp_max"],
        "pressure": response["main"]["pressure"],
        "humidity": response["main"]["humidity"],
        "wind_speed": response["wind"]["speed"],
        "wind_direction": wind_direction,
    }


def _get_city_name_data_from_open_weather_api(city_search):
    """
    Using the open weather api, search for the city name's weather data
    Add a success indicator and error message if appropriate

    :return:
        {
            "success": bool,
            "city_name": str,  # cleaned version of searched city name
            "error_message": str,  # available when success is False

        }
    """

    response = requests.get(
        config.OPEN_WEATHER_API_URL,
        params={
            "q": city_search.city_name,
            "lang": city_search.lang,
            "appid": settings.OPEN_WEATHER_API_KEY,
            "units": "metric",
        },
    )

    response_message = config.OPEN_WEATHER_RESPONSES.get(
        response.status_code,
        {
            "success": False,
            "error_message": _(
                "Unhandled error code, please raise an issue in the GitHub repo"
            ),
        },
    )
    response_message["city_name"] = city_search.city_name

    if response_message["success"]:
        response_message.update(_get_data_open_weather_api(response.json()))

    return response_message


def search(city_search):
    """
    If the city_name is not available in the cache,
    search for the city_name using `_get_city_name_data_from_open_weather_api`
    and then save to cache, otherwise return cached result

    :return:
        {
            "success": bool,
            "result": dict,  # Note: available when success is True, this is the API response
            "error_message": str,  # Note: available when success is False
        }
    """
    result = cache.get(city_search.cache_key)
    if not result:
        result = _get_city_name_data_from_open_weather_api(city_search)
        cache.set(city_search.cache_key, result, settings.CACHE_TIMEOUT)
    return result
