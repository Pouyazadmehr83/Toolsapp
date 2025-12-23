from django.urls import path
from .views import (
    home_view,
    image_compress_view,
    image_convert_view,
    image_filters_view,
    image_resize_view,
    image_watermark_view,
    qr_view,
    file_hash_view
)

app_name = "tools"


urlpatterns = [
    path("", home_view, name="home"),
    path("qr/", qr_view, name="qr"),
    path("image-converter/", image_convert_view, name="image_convert"),
    path("image-compressor/", image_compress_view, name="image_compress"),
    path("image-filters/", image_filters_view, name="image_filters"),
    path("image-resize/", image_resize_view, name="image_resize"),
    path("watermark/", image_watermark_view, name="image_watermark"),
    path("hash/",file_hash_view,name="hash")
]
