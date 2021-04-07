from http import HTTPStatus

import requests_mock
from django.core.cache import cache
from django.test import TestCase

from ..config import OPEN_WEATHER_API_URL, OPEN_WEATHER_RESPONSES
from ..utils import CitySearch, search
from .helpers import NEW_YORK_RESPONSE


class SearchTest(TestCase):
    OPEN_WEATHER_API_KEY = "foo"
    CITY_NAME = "New York"
    LANG = "en"
    EXPECTED_NEW_YORK_DATA = {
        "city_name": "New York",
        "success": True,
        "description": "Clear Sky",
        "icon": "01d",
        "temp": -0.19,
        "temp_min": -1.11,
        "temp_max": 1,
        "pressure": 1020,
        "humidity": 34,
        "wind_speed": 3.09,
        "wind_direction": "W",
    }

    def test_search_successful(self):
        """
        Test search function calls the open weather api
        and returns a dictionary for rendering in the template and this is saved to cache
        """
        city_search = CitySearch(city_name=self.CITY_NAME, lang=self.LANG)
        with requests_mock.Mocker() as m, self.settings(
            OPEN_WEATHER_API_KEY=self.OPEN_WEATHER_API_KEY
        ):
            m.get(
                OPEN_WEATHER_API_URL, json=NEW_YORK_RESPONSE, status_code=HTTPStatus.OK,
            )
            self.assertEqual(
                search(city_search), self.EXPECTED_NEW_YORK_DATA,
            )
            self.assertEqual(
                cache.get(city_search.cache_key),
                self.EXPECTED_NEW_YORK_DATA,
                msg="result now saved into cache",
            )

    def test_search_already_cached(self):
        """
        Test search function checks the cache and if already in cache returns this result
        """
        example_cached_value = "TEST"
        city_search = CitySearch(city_name="Cologne", lang="de")
        cache.set(city_search.cache_key, example_cached_value)
        self.assertEqual(
            search(city_search),
            example_cached_value,
            msg="confirm returns value from cache",
        )

    def test_search_unsuccessful_handled_error(self):
        """
        Test a valid City Search Form calls the open weather api and if the city not found,
        returns an error message to render in the template
        """
        city_name = "Fake City"
        city_search = CitySearch(city_name=city_name, lang="fr")
        expected_result = {
            "city_name": city_name,
            **OPEN_WEATHER_RESPONSES[HTTPStatus.NOT_FOUND],
        }
        with requests_mock.Mocker() as m, self.settings(
            OPEN_WEATHER_API_KEY=self.OPEN_WEATHER_API_KEY
        ):
            m.get(OPEN_WEATHER_API_URL, status_code=HTTPStatus.NOT_FOUND)
            self.assertEqual(
                search(city_search), expected_result,
            )

    def test_search_unsuccessful_unhandled(self):
        """
        Test that when an unhandled status code is returned from the API the generic message is returned
        """
        city_search = CitySearch(city_name=self.CITY_NAME, lang=self.LANG)
        with requests_mock.Mocker() as m, self.settings(
            OPEN_WEATHER_API_KEY=self.OPEN_WEATHER_API_KEY
        ):
            m.get(OPEN_WEATHER_API_URL, status_code=HTTPStatus.LOCKED)
            self.assertEqual(
                search(city_search),
                {
                    "city_name": self.CITY_NAME,
                    "success": False,
                    "error_message": "Unhandled error code, please raise an issue in the GitHub repo",
                },
            )
