import pytest
import requests
from page_analyzer.services.checks import perform_check


class FakeResponse:
    def __init__(self, text, status_code=200):
        self.text = text
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(f'{self.status_code} Error')


def test_perform_check_parss_fields(monkeypatch):
    html = """
    <html>
      <head>
        <title>My Title</title>
        <meta name='description' content='Description text'>
      </head>
      <body>
        <h1>Page Heading</h1>
      </body>
    </html>
    """
    fake_resp = FakeResponse(html, status_code=200)

    monkeypatch.setattr(
        'page_analyzer.services.checks.requests.get',
        lambda *args, **kwargs: fake_resp
    )

    result = perform_check('http://example.com')

    assert result['status_code'] == 200
    assert result['title'] == 'My Title'
    assert result['h1'] == 'Page Heading'
    assert result['description'] == 'Description text'


def test_perform_check_no_data(monkeypatch):
    fake_resp = FakeResponse('', status_code=200)

    monkeypatch.setattr(
        'page_analyzer.services.checks.requests.get',
        lambda *args, **kwargs: fake_resp
    )

    result = perform_check('http://example.com')
    assert result['status_code'] == 200
    assert result['title'] is None
    assert result['h1'] is None
    assert result['description'] is None


def test_perform_check_raise_for_bad_status(monkeypatch):
    fake_resp = FakeResponse('<html></html>', status_code=500)
    monkeypatch.setattr(
        'page_analyzer.services.checks.requests.get',
        lambda *args, **kwargs: fake_resp
    )

    with pytest.raises(requests.exceptions.HTTPError):
        perform_check('http://example.com')
