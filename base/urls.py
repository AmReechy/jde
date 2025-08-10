
from django.urls import path
from . import views

app_name = "base"

urlpatterns = [
        #path("old", views.home, name="home"),
        #path("new", views.new_home, name="new-home"),
        path("jde-consulte", views.homepage, name="homepage"),
        ]
