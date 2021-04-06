from django import forms
from django.utils.translation import ugettext_lazy as _


class CitySearchForm(forms.Form):
    city_name = forms.CharField(max_length=200, label=_("City Name"))

    def clean_city_name(self):
        """
        Remove trailing blank spaces and have consistent capitalization to be a consistent format as a cache key
        :return: cleaned version of city name
        """
        city_name = self.cleaned_data["city_name"]
        return city_name.strip().title()
