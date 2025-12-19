import base64
import io

import qrcode
from django.shortcuts import render


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
