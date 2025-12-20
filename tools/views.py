import base64
import io

import qrcode
from django.shortcuts import render
from PIL import Image


def home_view(request):
    return render(request, "tools/home.html")


def qr_view(request):
    qr_image = None
    url_value = ""
    error_message = None

    if request.method == "POST":
        url_value = request.POST.get("url", "").strip()
        if url_value:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=4,
            )
            qr.add_data(url_value)
            qr.make(fit=True)

            image = qr.make_image(fill_color="black", back_color="white")
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            qr_image = base64.b64encode(buffer.getvalue()).decode("ascii")
        else:
            error_message = "Please enter a URL before generating a QR code."

    context = {
        "qr_image": qr_image,
        "url_value": url_value,
        "error_message": error_message,
    }
    return render(request, "tools/qr.html", context)


def image_convert_view(request):
    allowed_formats = {"png", "jpeg", "webp"}
    converted_image = None
    target_format = "png"
    download_name = "converted.png"
    error_message = None

    if request.method == "POST":
        target_format = request.POST.get("target_format", "png").lower()
        image_file = request.FILES.get("image_file")

        if target_format not in allowed_formats:
            error_message = "Unsupported format requested."
        elif not image_file:
            error_message = "Please upload an image file."
        else:
            try:
                image = Image.open(image_file)
                if target_format == "jpeg" and image.mode in ("RGBA", "P"):
                    image = image.convert("RGB")

                buffer = io.BytesIO()
                image.save(buffer, format=target_format.upper())
                converted_image = base64.b64encode(buffer.getvalue()).decode("ascii")
                download_ext = "jpg" if target_format == "jpeg" else target_format
                download_name = f"converted.{download_ext}"
            except Exception:
                error_message = "Could not process the uploaded image. Please try another file."

    context = {
        "converted_image": converted_image,
        "target_format": target_format,
        "download_name": download_name,
        "error_message": error_message,
    }
    return render(request, "tools/image_convert.html", context)
