from django.shortcuts import render
from api.forms import CitySearchForm
from django.utils.translation import get_language


def index(request):
    lang = get_language()
    city_search_form = CitySearchForm(request.POST or None)
    searched_data = {}
    if city_search_form.is_valid():
        searched_data = city_search_form.search(lang=lang)

    return render(request, "index.html", {'form': city_search_form, **searched_data})
