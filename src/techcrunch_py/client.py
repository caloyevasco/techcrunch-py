import requests
from bs4 import BeautifulSoup

home = 'https://techcrunch.com/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'en-US,en;q=0.9',
}

def create_client():
    session = requests.get(home)
    session.headers.update(headers)
    return requests