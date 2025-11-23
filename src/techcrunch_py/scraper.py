from .client import create_client, home
from bs4 import BeautifulSoup

from techcrunch_py.selectors.home_selectors import HomePageSelectors
from techcrunch_py.selectors.article_selectors import ArticleCardSelectors
from techcrunch_py.selectors.article_selectors import ArticleContentSelectors
from .schemas.latest_article_schema import ArticleSchema

def get_latest_headlines(limit=10):
    
    client = create_client()
    home_content = client.get(home)

    home_content.raise_for_status()

    homepage = BeautifulSoup(home_content.text, 'html.parser')

    headlines_ul = homepage.find(
        HomePageSelectors.LIST_HEADLINES.tag,
        class_=HomePageSelectors.LIST_HEADLINES.class_name
    )

    if headlines_ul is None:
        return []


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

        article_content = client.get(full_article_link.get('href'))
        article_content.raise_for_status()
        article_soup = BeautifulSoup(article_content.text, 'html.parser')
        content_paragraphs = article_soup.find_all(
            ArticleContentSelectors.CONTENT_PARAGRAPH.tag,
            class_=ArticleContentSelectors.CONTENT_PARAGRAPH.class_name
        )
        content = "\n".join(
            [para.get_text() for para in content_paragraphs]
        )

        article_data = ArticleSchema(
            title=title.get_text() if title else '',
            category=category.get_text() if category else '',
            publish_time=article_publish_time.get_text() if article_publish_time else '',
            author=article_author.get_text() if article_author else '',
            image_url=article_image.get('src') if article_image else '',
            full_article_link=full_article_link.get('href') if full_article_link else '',
            content=content
        )

        yield article_data