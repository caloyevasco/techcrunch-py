from .client import create_client, home
from .schemas.latest_article_schema import LatestArticleSchema
from bs4 import BeautifulSoup

from techcrunch_py.selectors.home_selectors import HomePageSelectors
from techcrunch_py.selectors.article_selectors import ArticleCardSelectors

def get_latest(limit=10):
    client = create_client()
    home_content = client.get(home)
    home_content.raise_for_status()
    soup = BeautifulSoup(home_content.text, 'html.parser')
    links = [LatestArticleSchema(
        element_class=element.get('class')[0],
        href=element.get('href'),
        text=element.get_text()
    ) for element in soup.find_all('a', class_='wp-block-post-template is-layout-flow wp-block-post-template-is-layout-flow')]
    links = links[:limit]
    return links


def get_latest_headlines(limit=10):
    
    client = create_client()
    home_content = client.get(home)
    home_content.raise_for_status()

    homepage = BeautifulSoup(home_content.text, 'html.parser')

    headlines_ul = homepage.find(
        HomePageSelectors.LIST_HEADLINES.tag,
        class_=HomePageSelectors.LIST_HEADLINES.class_name
    )

    articles = headlines_ul.find_all(
        HomePageSelectors.ARTICLE_LIST.tag,
        class_=HomePageSelectors.ARTICLE_LIST.class_name
    )[:limit]

    for article in articles:
        title = BeautifulSoup(str(article), 'html.parser').find(
            ArticleCardSelectors.TITLE.tag,
            class_=ArticleCardSelectors.TITLE.class_name
        )

        category = BeautifulSoup(str(article), 'html.parser').find(
            ArticleCardSelectors.CATEGORY.tag,
            class_=ArticleCardSelectors.CATEGORY.class_name
        )

        article_publish_time = BeautifulSoup(str(article), 'html.parser').find(
            ArticleCardSelectors.ARTICLE_PUBLISH_TIME.tag,
            class_=ArticleCardSelectors.ARTICLE_PUBLISH_TIME.class_name
        )

        article_author = BeautifulSoup(str(article), 'html.parser').find(
            ArticleCardSelectors.ARTICLE_AUTHOR.tag,
            class_=ArticleCardSelectors.ARTICLE_AUTHOR.class_name
        )

        article_image = BeautifulSoup(str(article), 'html.parser').find(
            ArticleCardSelectors.ARTICLE_IMAGE.tag,
            class_=ArticleCardSelectors.ARTICLE_IMAGE.class_name
        )

        full_article_link = BeautifulSoup(str(article), 'html.parser').find(
            ArticleCardSelectors.FULL_ARTICLE_LINK.tag,
            class_=ArticleCardSelectors.FULL_ARTICLE_LINK.class_name
        )

        

