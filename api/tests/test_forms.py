from django.test import TestCase

from ..forms import CitySearchForm


class CitySearchFormTest(TestCase):
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
