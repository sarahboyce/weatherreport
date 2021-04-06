from django.urls import path

from .views import Index, SearchedIndex

app_name = "api"
urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("<str:city_name>/", SearchedIndex.as_view(), name="searched_index"),
]
