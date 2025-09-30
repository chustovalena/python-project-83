

def test_get_main(client):
    response = client.get('/')

    assert response.status_code == 200
    assert b"SEO" in response.data


def test_get_urls(client):
    response = client.get('/urls')

    assert response.status_code == 200
    assert b'http://' not in response.data


def test_post_urls(client):
    response = client.post('/urls', data={"url": "http://example.com"})
    resp = client.get('/urls')

    assert response.status_code == 302
    assert b"http://example.com" in resp.data


def test_get_url(client):
    client.post('/urls', data={"url": "http://example.com"})
    response = client.get('/urls/1')

    assert b"http://example.com" in response.data
    assert response.status_code == 200


def test_no_duple(client):
    client.post('/urls', data={"url": "http://example.com"})
    client.post('/urls', data={"url": "http://example.com"})

    response = client.get('/urls')
    assert response.data.count(b'http://example.com') == 1


def test_check(client):
    client.post('/urls', data={"url": "https://web.mit.edu"})
    response = client.post('/urls/1/checks')
    assert response.status_code == 302
    response = client.get('/urls/1')
    assert b'https://web.mit.edu' in response.data


