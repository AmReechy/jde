
from django.urls import path
from . import views

app_name = "base"

urlpatterns = [
        path("old", views.home, name="home"),
        path("new", views.new_home, name="new-home"),
        path("", views.homepage, name="homepage"),
        ]
