from http import HTTPStatus

import requests_mock
from django.test import TestCase
from django.urls import reverse

from api.forms import OPEN_WEATHER_API_URL
from api.tests.helpers import NEW_YORK_RESPONSE


class IndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.OPEN_WEATHER_API_KEY = "foo"
        cls.index_url = reverse("api:index")

    def test_get_index(self):
        """
        Test the index page loads with the form rendered
        """
        response = self.client.get(self.index_url)
        self.assertEqual(
            response.status_code, HTTPStatus.OK, msg="index page loads successfully"
        )
        self.assertContains(
            response,
            '<button type="submit" class="btn btn-primary"><i class="fas fa-search"></i></button>',
        )

    def test_post_invalid_form(self):
        """
        Test that when the form is sent without the city_name
        page is loaded with error message
        """
        response = self.client.post(self.index_url, {"city_name": ""})
        self.assertEqual(
            response.status_code, HTTPStatus.OK, msg="index page loads successfully"
        )
        # has-error is the bootstrap class for forms with errors
        self.assertContains(response, "has-error")
        self.assertContains(
            response, '<div class="help-block">This field is required.</div>'
        )

    def test_post_valid_form(self):
        """
        Test when post a valid City Search Form calls the open weather api
        and the data returned is rendered in the view
        """
        city_name = "New York"
        with requests_mock.Mocker() as m, self.settings(
            OPEN_WEATHER_API_KEY=self.OPEN_WEATHER_API_KEY
        ):
            m.get(
                OPEN_WEATHER_API_URL, json=NEW_YORK_RESPONSE, status_code=HTTPStatus.OK,
            )
            response = self.client.post(self.index_url, {"city_name": city_name})
            self.assertEqual(
                response.status_code, HTTPStatus.OK, msg="index page loads successfully"
            )
            expected_result_render_page = {
                "city_name": city_name,
                "description": "Clear Sky",
                "temp": -0.19,
                "temp_min": -1.11,
                "temp_max": 1,
                "pressure": 1020,
                "humidity": 34,
                "wind_speed": 3.09,
                "wind_direction": "W",
            }
            # test that each of the results are contained on the page
            for _, value in expected_result_render_page.items():
                self.assertContains(response, value)
