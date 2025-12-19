from django.urls import path
from .views import home_view, qr_view

app_name = "tools"


urlpatterns = [
    path("", home_view, name="home"),
    path("qr/", qr_view, name="qr"),
]
