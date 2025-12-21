import base64
import io

import qrcode
from django.shortcuts import render
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


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


def image_compress_view(request):
    allowed_formats = {"jpeg", "webp", "png"}
    compressed_image = None
    target_format = "jpeg"
    quality = 80
    download_name = "compressed.jpg"
    error_message = None

    if request.method == "POST":
        target_format = request.POST.get("target_format", "jpeg").lower()
        image_file = request.FILES.get("image_file")
        try:
            quality = int(request.POST.get("quality", 80))
        except (TypeError, ValueError):
            quality = 80

        quality = max(10, min(95, quality))

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
                save_kwargs = {"format": target_format.upper()}

                if target_format in {"jpeg", "webp"}:
                    save_kwargs.update({"quality": quality, "optimize": True})
                    if target_format == "webp":
                        save_kwargs["method"] = 6
                else:
                    save_kwargs.update(
                        {
                            "optimize": True,
                            "compress_level": max(0, min(9, int((100 - quality) / 10))),
                        }
                    )

                image.save(buffer, **save_kwargs)
                compressed_image = base64.b64encode(buffer.getvalue()).decode("ascii")
                download_ext = "jpg" if target_format == "jpeg" else target_format
                download_name = f"compressed.{download_ext}"
            except Exception:
                error_message = "Could not process the uploaded image. Please try another file."

    context = {
        "compressed_image": compressed_image,
        "target_format": target_format,
        "quality": quality,
        "download_name": download_name,
        "error_message": error_message,
    }
    return render(request, "tools/image_compress.html", context)


def image_watermark_view(request):
    allowed_formats = {"png", "jpeg", "webp"}
    watermarked_image = None
    target_format = "png"
    position = "bottom_right"
    watermark_text = "© ToolsApp"
    download_name = "watermarked.png"
    error_message = None

    if request.method == "POST":
        image_file = request.FILES.get("image_file")
        watermark_text = request.POST.get("watermark_text", "").strip()
        position = request.POST.get("position", "bottom_right")
        target_format = request.POST.get("target_format", "png").lower()

        if target_format not in allowed_formats:
            error_message = "Unsupported format requested."
        elif not image_file:
            error_message = "Please upload an image file."
        elif not watermark_text:
            error_message = "Please enter watermark text."
        else:
            try:
                base_image = Image.open(image_file).convert("RGBA")
                text_layer = Image.new("RGBA", base_image.size, (255, 255, 255, 0))
                draw = ImageDraw.Draw(text_layer)
                font = ImageFont.load_default()

                text_width, text_height = draw.textsize(watermark_text, font=font)
                padding = 12

                if position == "top_left":
                    coords = (padding, padding)
                elif position == "top_right":
                    coords = (base_image.width - text_width - padding, padding)
                elif position == "bottom_left":
                    coords = (padding, base_image.height - text_height - padding)
                elif position == "center":
                    coords = ((base_image.width - text_width) / 2, (base_image.height - text_height) / 2)
                else:
                    coords = (base_image.width - text_width - padding, base_image.height - text_height - padding)

                shadow_offset = (1, 1)
                shadow_color = (0, 0, 0, 120)
                text_color = (255, 255, 255, 200)

                draw.text((coords[0] + shadow_offset[0], coords[1] + shadow_offset[1]), watermark_text, font=font, fill=shadow_color)
                draw.text(coords, watermark_text, font=font, fill=text_color)

                combined = Image.alpha_composite(base_image, text_layer)

                if target_format == "jpeg" and combined.mode in ("RGBA", "P"):
                    combined = combined.convert("RGB")

                buffer = io.BytesIO()
                save_kwargs = {"format": target_format.upper()}
                if target_format in {"jpeg", "webp"}:
                    save_kwargs.update({"quality": 90, "optimize": True})
                    if target_format == "webp":
                        save_kwargs["method"] = 6
                combined.save(buffer, **save_kwargs)

                watermarked_image = base64.b64encode(buffer.getvalue()).decode("ascii")
                download_ext = "jpg" if target_format == "jpeg" else target_format
                download_name = f"watermarked.{download_ext}"
            except Exception:
                error_message = "Could not process the uploaded image. Please try another file."

    context = {
        "watermarked_image": watermarked_image,
        "target_format": target_format,
        "position": position,
        "watermark_text": watermark_text,
        "download_name": download_name,
        "error_message": error_message,
    }
    return render(request, "tools/image_watermark.html", context)


def image_resize_view(request):
    allowed_formats = {"png", "jpeg", "webp"}
    processed_image = None
    target_format = "png"
    mode = "resize"
    width = None
    height = None
    download_name = "resized.png"
    error_message = None

    if request.method == "POST":
        target_format = request.POST.get("target_format", "png").lower()
        mode = request.POST.get("mode", "resize")
        image_file = request.FILES.get("image_file")

        try:
            width = int(request.POST.get("width", "0"))
            height = int(request.POST.get("height", "0"))
        except (TypeError, ValueError):
            width = height = 0

        if target_format not in allowed_formats:
            error_message = "Unsupported format requested."
        elif not image_file:
            error_message = "Please upload an image file."
        elif width <= 0 or height <= 0:
            error_message = "Width and height must be positive numbers."
        else:
            try:
                image = Image.open(image_file)
                if mode == "crop":
                    image = ImageOps.fit(
                        image,
                        (width, height),
                        method=Image.Resampling.LANCZOS,
                        centering=(0.5, 0.5),
                    )
                else:
                    image = image.resize((width, height), Image.Resampling.LANCZOS)

                if target_format == "jpeg" and image.mode in ("RGBA", "P"):
                    image = image.convert("RGB")

                buffer = io.BytesIO()
                save_kwargs = {"format": target_format.upper()}
                if target_format in {"jpeg", "webp"}:
                    save_kwargs.update({"quality": 90, "optimize": True})
                    if target_format == "webp":
                        save_kwargs["method"] = 6
                image.save(buffer, **save_kwargs)

                processed_image = base64.b64encode(buffer.getvalue()).decode("ascii")
                download_ext = "jpg" if target_format == "jpeg" else target_format
                download_name = f"processed.{download_ext}"
            except Exception:
                error_message = "Could not process the uploaded image. Please try another file."

    context = {
        "processed_image": processed_image,
        "target_format": target_format,
        "mode": mode,
        "width": width,
        "height": height,
        "download_name": download_name,
        "error_message": error_message,
    }
    return render(request, "tools/image_resize.html", context)


def image_filters_view(request):
    allowed_formats = {"png", "jpeg", "webp"}
    filter_map = {
        "original": lambda img: img,
        "blur": lambda img: img.filter(ImageFilter.BLUR),
        "contour": lambda img: img.filter(ImageFilter.CONTOUR),
        "detail": lambda img: img.filter(ImageFilter.DETAIL),
        "edge_enhance": lambda img: img.filter(ImageFilter.EDGE_ENHANCE_MORE),
        "emboss": lambda img: img.filter(ImageFilter.EMBOSS),
        "find_edges": lambda img: img.filter(ImageFilter.FIND_EDGES),
        "sharpen": lambda img: img.filter(ImageFilter.SHARPEN),
        "smooth": lambda img: img.filter(ImageFilter.SMOOTH_MORE),
        "grayscale": lambda img: ImageOps.grayscale(img),
        "invert": lambda img: ImageOps.invert(img.convert("RGB")),
        "solarize": lambda img: ImageOps.solarize(img.convert("RGB"), threshold=128),
        "posterize": lambda img: ImageOps.posterize(img.convert("RGB"), bits=4),
    }
    filter_labels = [
        ("original", "Original"),
        ("blur", "Blur"),
        ("contour", "Contour"),
        ("detail", "Detail"),
        ("edge_enhance", "Edge Enhance"),
        ("emboss", "Emboss"),
        ("find_edges", "Find Edges"),
        ("sharpen", "Sharpen"),
        ("smooth", "Smooth"),
        ("grayscale", "Grayscale"),
        ("invert", "Invert"),
        ("solarize", "Solarize"),
        ("posterize", "Posterize"),
    ]

    filtered_image = None
    filter_name = "original"
    target_format = "png"
    download_name = "filtered.png"
    error_message = None

    if request.method == "POST":
        target_format = request.POST.get("target_format", "png").lower()
        filter_name = request.POST.get("filter_name", "original")
        image_file = request.FILES.get("image_file")

        if target_format not in allowed_formats:
            error_message = "Unsupported format requested."
        elif not image_file:
            error_message = "Please upload an image file."
        elif filter_name not in filter_map:
            error_message = "Unknown filter selected."
        else:
            try:
                image = Image.open(image_file)
                processed = filter_map[filter_name](image)
                if target_format == "jpeg" and processed.mode in ("RGBA", "P"):
                    processed = processed.convert("RGB")

                buffer = io.BytesIO()
                save_kwargs = {"format": target_format.upper()}
                if target_format in {"jpeg", "webp"}:
                    save_kwargs.update({"quality": 90, "optimize": True})
                    if target_format == "webp":
                        save_kwargs["method"] = 6
                processed.save(buffer, **save_kwargs)

                filtered_image = base64.b64encode(buffer.getvalue()).decode("ascii")
                download_ext = "jpg" if target_format == "jpeg" else target_format
                download_name = f"filtered_{filter_name}.{download_ext}"
            except Exception:
                error_message = "Could not process the uploaded image. Please try another file."

    context = {
        "filtered_image": filtered_image,
        "filter_name": filter_name,
        "filter_options": filter_labels,
        "target_format": target_format,
        "download_name": download_name,
        "error_message": error_message,
    }
    return render(request, "tools/image_filters.html", context)
