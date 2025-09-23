import requests
from bs4 import BeautifulSoup


def perform_check(url: str):
    response = requests.get(url, timeout=5)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')

    h1 = soup.find('h1')
    title = soup.find('title')
    meta = soup.find('meta', {'name': 'description'})

    return {
        'status_code': response.status_code,
        'h1': h1.text.strip() if h1 else None,
        'title': title.text.strip() if title else None,
        'description': meta.get('content').strip() if meta else None
    }

