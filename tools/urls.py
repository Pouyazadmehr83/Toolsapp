from django.urls import path
from .views import home_view, image_convert_view, qr_view

app_name = "tools"


urlpatterns = [
    path("", home_view, name="home"),
    path("qr/", qr_view, name="qr"),
    path("image-converter/", image_convert_view, name="image_convert"),
]
