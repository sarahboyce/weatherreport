from django.shortcuts import redirect
from django.utils.translation import get_language
from django.views import generic

from .forms import CitySearchForm
from .utils import search


class Index(generic.FormView):
    template_name = "index.html"
    form_class = CitySearchForm

    def form_valid(self, form, *args, **kwargs):
        city_name = form.cleaned_data.get("city_name")
        return redirect("api:searched_index", city_name=city_name)


class SearchedIndex(Index, generic.FormView):
    def get_context_data(self, **kwargs):
        lang = get_language()
        searched_data = search(city_name=self.kwargs["city_name"], lang=lang)
        context_data = super().get_context_data(**kwargs)
        return {**context_data, **searched_data}
