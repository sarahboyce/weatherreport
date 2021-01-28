import requests_mock
from django.core.cache import cache
from django.test import TestCase

from api.forms import CitySearchForm


class CitySearchFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.search_url = "https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}&units=metric&lang={lang}"
        cls.OPEN_WEATHER_API_KEY = "foo"

    def test_clean_city_name(self):
        """
        Test the City Search Form cleans city names to be consistent
        Important for cache key
        """
        similar_city_names = ["New York", "NEW YORK", "new york", "NeW York "]

        for city_name in similar_city_names:
            form = CitySearchForm(data={"city_name": city_name})
            self.assertTrue(form.is_valid())
            self.assertEqual(
                form.cleaned_data["city_name"],
                "New York",
                msg="after clean method, each return the same string - 'New York'",
            )

    def test_search_successful(self):
        """
        Test a valid City Search Form calls the open weather api
        and returns a dictionary for rendering in the template and this is saved to cache
        """
        city_name = "New York"
        lang = "en"
        with requests_mock.Mocker() as m, self.settings(
            OPEN_WEATHER_API_KEY=self.OPEN_WEATHER_API_KEY
        ):
            test_url = self.search_url.format(
                city_name=city_name, API_key=self.OPEN_WEATHER_API_KEY, lang=lang
            )
            m.get(
                test_url,
                json={
                    "coord": {"lon": -74.006, "lat": 40.7143},
                    "weather": [
                        {
                            "id": 800,
                            "main": "Clear",
                            "description": "clear sky",
                            "icon": "01d",
                        }
                    ],
                    "base": "stations",
                    "main": {
                        "temp": -0.19,
                        "feels_like": -3,
                        "temp_min": -1.11,
                        "temp_max": 1,
                        "pressure": 1020,
                        "humidity": 34,
                    },
                    "visibility": 10000,
                    "wind": {"speed": 3.09, "deg": 308},
                    "clouds": {"all": 1},
                    "dt": 1611511880,
                    "sys": {
                        "type": 1,
                        "id": 5141,
                        "country": "US",
                        "sunrise": 1611490354,
                        "sunset": 1611525811,
                    },
                    "timezone": -18000,
                    "id": 5128581,
                    "name": city_name,
                },
                status_code=200,
            )
            form = CitySearchForm(data={"city_name": city_name})
            self.assertTrue(
                form.is_valid(), msg="Confirm valid form as needed before can search"
            )
            expected_result = {
                "city_name": city_name,
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
            self.assertEqual(
                form.search("en"), expected_result,
            )
            self.assertEqual(
                cache.get(f"{city_name}_{lang}"),
                expected_result,
                msg="result now saved into cache",
            )

    def test_search_already_cached(self):
        """
        Test a valid City Search Form checks the cache and if already in cache returns this result
        """
        example_cached_value = "TEST"
        city_name = "Cologne"
        lang = "de"
        cache.set(f"{city_name}_{lang}", example_cached_value)
        form = CitySearchForm(data={"city_name": city_name})
        self.assertTrue(
            form.is_valid(), msg="Confirm valid form as needed before can search"
        )
        self.assertEqual(
            form.search(lang),
            example_cached_value,
            msg="confirm returns value from cache",
        )

    def test_search_unsuccessful_city_not_found(self):
        """
        Test a valid City Search Form calls the open weather api and if the city not found,
        returns an error message to render in the template
        """
        city_name = "Fake City"
        lang = "fr"
        with requests_mock.Mocker() as m, self.settings(
            OPEN_WEATHER_API_KEY=self.OPEN_WEATHER_API_KEY
        ):
            test_url = self.search_url.format(
                city_name=city_name, API_key=self.OPEN_WEATHER_API_KEY, lang=lang
            )
            m.get(test_url, status_code=404)
            form = CitySearchForm(data={"city_name": city_name})
            self.assertTrue(
                form.is_valid(), msg="Confirm valid form as needed before can search"
            )
            self.assertEqual(
                form.search(lang),
                {
                    "city_name": city_name,
                    "success": False,
                    "error_message": f"No entry found for {city_name}",
                },
            )

    def test_search_unsuccessful_other_error(self):
        """
        Test a valid City Search Form calls the open weather api
        and if the code is not 200 (successful) or 404 (not found) an error message is returned
        """
        city_name = "Super Failing City"
        lang = "en"
        with requests_mock.Mocker() as m, self.settings(
            OPEN_WEATHER_API_KEY=self.OPEN_WEATHER_API_KEY
        ):
            test_url = self.search_url.format(
                city_name=city_name, API_key=self.OPEN_WEATHER_API_KEY, lang=lang
            )
            m.get(test_url, status_code=502)
            form = CitySearchForm(data={"city_name": city_name})
            self.assertTrue(
                form.is_valid(), msg="Confirm valid form as needed before can search"
            )
            self.assertEqual(
                form.search(lang),
                {
                    "city_name": city_name,
                    "success": False,
                    "error_message": "The Open Weather API is not available right now - please try again later",
                },
            )
