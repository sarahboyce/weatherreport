from django.urls import path, re_path

from api import views

app_name = "api"
urlpatterns = [
    path("", views.index, name="index"),
]
