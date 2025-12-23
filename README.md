# ToolsApp

ToolsApp is a Django-based collection of small, focused utilities for working with URLs and images. It is designed to be easy to extend and straightforward for new contributors to pick up.

## Current tools
- URL → QR: generate QR codes from any URL.
- Image Converter: upload and convert between PNG, JPEG, and WEBP.
- Image Compressor: upload, choose output format/quality, and download a smaller file.
- Resize / Crop: set exact width/height, choose resize or center-crop, and export in your chosen format.
- Watermark: add text watermarks at common positions with a subtle shadow.
- Filters: apply common Pillow filters (blur, contour, detail, edge enhance, emboss, find edges, sharpen, smooth, grayscale, invert, solarize, posterize, original).
- File Hash: upload a file and calculate its hash (SHA-256, SHA-1) with a size limit and instant result display.

### File Hash tool
Upload any file and calculate its cryptographic hash using common algorithms such as **SHA-256** and **SHA-1**.  
This tool is useful for verifying file integrity and learning how hashing works in practice.  
A maximum file size limit is enforced to keep the tool safe and fast.


## Tech stack
- Python 3.13+
- Django 6
- Pillow for all image processing
- qrcode for QR generation
- Bootstrap (via CDN) for UI
- hashlib for show file hash

## Getting started (development)
1) Install dependencies (Poetry):
```
poetry install
```
2) Apply migrations (uses SQLite by default):
```
poetry run python manage.py migrate
```
3) Run the dev server:
```
poetry run python manage.py runserver
```
Then open http://127.0.0.1:8000/ in your browser.

## Project status
Active development. New tools and improvements are welcome; existing features are stable for development use but not production-hardened yet.

## Contributing
- Fork/branch from `main`.
- Keep UI additions aligned with the existing Bootstrap layout in `tools/templates/tools/base.html`.
- Add new tools as separate views with clear routing under `tools/urls.py` and templates under `tools/templates/tools/`.
- Open a PR describing the feature, implementation details, and any manual testing you performed.

## Roadmap ideas
- Add drag-and-drop uploads.
- Add history/download logs for generated assets.
- Expand filters with adjustable parameters (e.g., blur radius, brightness/contrast).
- Bundle Bootstrap assets locally for offline use.
- Support additional hash algorithms (MD5, SHA-512).
- Compare hashes of two files.


## Notes
- Static assets are pulled from CDNs; run in an environment with internet access or serve them locally if needed.
- Default SQLite database is included for quick start; swap in your preferred database by updating `core/settings.py`.
