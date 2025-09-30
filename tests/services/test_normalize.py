from page_analyzer.services.normalize import normalize_url


def test_normalize_url():
    raw_url1 = 'http://rgreggr.com/users/1'
    raw_url2 = 'https://google.com/7/books/3'
    assert normalize_url(raw_url1) == 'http://rgreggr.com'
    assert normalize_url(raw_url2) == 'https://google.com'
