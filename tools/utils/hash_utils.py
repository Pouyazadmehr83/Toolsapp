import hashlib


SUPPORTED_ALLGORITHMS = {
    "sha256": hashlib.sha256,
    "sha1":hashlib.sha1,
    "md5": hashlib.md5,
}

def calculate_file_hash(uploaded_file, algorithm="sha256"):
    if algorithm not in SUPPORTED_ALLGORITHMS:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    hasher = SUPPORTED_ALLGORITHMS[algorithm]()

    for chunk in uploaded_file.chunks():
        hasher.update(chunk)

    return hasher.hexdigest()   