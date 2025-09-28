from urllib.parse import urlparse


def validate(form):
    errors = []
    url = form.get('url', '').strip()

    if not url:
        errors.append('URL is required')

    elif len(url) > 255:
        errors.append('URL length must be less than 256 characters')

    else:
        parsed = urlparse(url)
        if parsed.scheme not in ('http', 'https') or not parsed.netloc:
            errors.append('Incorrect URL')

    return errors
