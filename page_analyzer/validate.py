from urllib.parse import urlparse


def validate(url):
    errors = {}
    if len(url['url']) > 255:
        errors['name'] = 'Url length must be less than 256 characters'
    parsed = urlparse(url['url'])
    if not parsed.scheme or not parsed.netloc:
        errors['name'] = 'Incorrect URL'
    return errors
