from http import HTTPStatus

import requests
from django import forms
from django.conf import settings
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _

from api.utils import get_data_open_weather_api

OPEN_WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

OPEN_WEATHER_RESPONSES = {
    HTTPStatus.OK: {"success": True},
    HTTPStatus.NOT_FOUND: {
        "success": False,
        "error_message": _("No entry found for this city"),
    },
    HTTPStatus.BAD_REQUEST: {
        "success": False,
        "error_message": _(
            "Bad request syntax or unsupported method - please raise an issue in the GitHub repo"
        ),
    },
    HTTPStatus.UNAUTHORIZED: {
        "success": False,
        "error_message": _(
            "Request unauthorised - please check you have set up your Open Weather API key correctly"
        ),
    },
    HTTPStatus.REQUEST_TIMEOUT: {
        "success": False,
        "error_message": _(
            "The Open Weather API is not available right now - please try again later"
        ),
    },
    HTTPStatus.INTERNAL_SERVER_ERROR: {
        "success": False,
        "error_message": _(
            "Internal Server Error - please raise an issue in the GitHub repo"
        ),
    },
    HTTPStatus.BAD_GATEWAY: {
        "success": False,
        "error_message": _(
            "Invalid response from another server/proxy - please raise an issue in the GitHub repo"
        ),
    },
}


class CitySearchForm(forms.Form):
    city_name = forms.CharField(max_length=200, label=_("City Name"))

    def clean_city_name(self):
        """
        Remove trailing blank spaces and have consistent capitalization to be a consistent format as a cache key
        :return: cleaned version of city name
        """
        city_name = self.cleaned_data["city_name"]
        return city_name.strip().title()

    @staticmethod
    def get_city_name_data_from_open_weather_api(city_name, lang):
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
            OPEN_WEATHER_API_URL,
            params={
                "q": city_name,
                "appid": settings.OPEN_WEATHER_API_KEY,
                "lang": lang,
                "units": "metric",
            },
        )

        response_message = OPEN_WEATHER_RESPONSES.get(
            response.status_code,
            {
                "success": False,
                "error_message": _(
                    "Unhandled error code, please raise an issue in the GitHub repo"
                ),
            },
        )
        response_message["city_name"] = city_name

        if response_message["success"]:
            response_message.update(get_data_open_weather_api(response.json()))

        return response_message

    def search(self, lang):
        """
        If the city_name is not available in the cache,
        search for the city_name using `get_city_name_data_from_open_weather_api`
        and then save to cache, otherwise return cached result

        :return:
            {
                "success": bool,
                "result": dict,  # Note: available when success is True, this is the API response
                "error_message": str,  # Note: available when success is False
            }
        """
        city_name = self.cleaned_data["city_name"]

        cache_key = f"{city_name}_{lang}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        else:
            result = self.get_city_name_data_from_open_weather_api(city_name, lang=lang)
            cache.set(cache_key, result, settings.CACHE_TIMEOUT)
            return result
