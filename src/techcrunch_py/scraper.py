from .client import create_client, home
from bs4 import BeautifulSoup

def get_latest(limit=10):
    client = create_client()
    home_content = client.get(home)
    soup = BeautifulSoup(home_content.text, 'html.parser')
    links = soup.find_all('a', class_='loop-card__title-link')
    return links