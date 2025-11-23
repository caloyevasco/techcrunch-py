from .client import create_client, home
from .schemas.latest_article_schema import LatestArticleSchema
from bs4 import BeautifulSoup

def get_latest(limit=10):
    client = create_client()
    home_content = client.get(home)
    home_content.raise_for_status()
    soup = BeautifulSoup(home_content.text, 'html.parser')
    links = [LatestArticleSchema(
        element_class=element.get('class')[0],
        href=element.get('href'),
        text=element.get_text()
    ) for element in soup.find_all('a', class_='loop-card__title-link')]
    links = links[:limit]
    return links