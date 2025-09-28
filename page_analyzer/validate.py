from urllib.parse import urlparse


from urllib.parse import urlparse


def validate(url):
    errors = []
    url_value = url.get("url", "").strip()

    if len(url_value) > 255:
        errors.append("Url length must be less than 256 characters")

    parsed = urlparse(url_value)

    if parsed.scheme not in ("http", "https"):
        errors.append("URL must start with http:// or https://")

    hostname = parsed.hostname
    if not hostname or "." not in hostname:
        errors.append("Incorrect URL")

    return errors
