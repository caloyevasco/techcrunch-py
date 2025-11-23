from .client import create_client, home
from bs4 import BeautifulSoup

from techcrunch_py.selectors.home_selectors import HomePageSelectors
from techcrunch_py.selectors.article_selectors import ArticleCardSelectors
from techcrunch_py.selectors.article_selectors import ArticleContentSelectors
from .schemas.latest_article_schema import ArticleSchema

def get_latest_headlines(limit=10):
    
    client = create_client()
    home_content = client.get(home)

    from .client import create_client, home
    from bs4 import BeautifulSoup

    from techcrunch_py.selectors.home_selectors import HomePageSelectors
    from techcrunch_py.selectors.article_selectors import ArticleCardSelectors
    from techcrunch_py.selectors.article_selectors import ArticleContentSelectors
    from .schemas.latest_article_schema import ArticleSchema


    def get_latest_headlines(limit=10):
        """Yield latest articles (up to `limit`) from the TechCrunch homepage.

        This function is defensive: it skips articles missing a link and
        avoids re-parsing the article node repeatedly.
        """
        client = create_client()
        home_content = client.get(home)
        home_content.raise_for_status()

        homepage = BeautifulSoup(home_content.text, 'html.parser')

        headlines_ul = homepage.find(
            HomePageSelectors.LIST_HEADLINES.tag,
            class_=HomePageSelectors.LIST_HEADLINES.class_name,
        )

        if headlines_ul is None:
            return []

        articles = headlines_ul.find_all(
            HomePageSelectors.ARTICLE_LIST.tag,
            class_=HomePageSelectors.ARTICLE_LIST.class_name,
        )[:limit]

        for article in articles:
            # `article` is already a BeautifulSoup Tag; query it directly.
            title_tag = article.find(
                ArticleCardSelectors.TITLE.tag,
                class_=ArticleCardSelectors.TITLE.class_name,
            )

            category_tag = article.find(
                ArticleCardSelectors.CATEGORY.tag,
                class_=ArticleCardSelectors.CATEGORY.class_name,
            )

            publish_time_tag = article.find(
                ArticleCardSelectors.ARTICLE_PUBLISH_TIME.tag,
                class_=ArticleCardSelectors.ARTICLE_PUBLISH_TIME.class_name,
            )

            author_tag = article.find(
                ArticleCardSelectors.ARTICLE_AUTHOR.tag,
                class_=ArticleCardSelectors.ARTICLE_AUTHOR.class_name,
            )

            image_tag = article.find(
                ArticleCardSelectors.ARTICLE_IMAGE.tag,
                class_=ArticleCardSelectors.ARTICLE_IMAGE.class_name,
            )

            full_article_link_tag = article.find(
                ArticleCardSelectors.FULL_ARTICLE_LINK.tag,
                class_=ArticleCardSelectors.FULL_ARTICLE_LINK.class_name,
            )

            href = None
            if full_article_link_tag:
                href = full_article_link_tag.get('href')

            # If we don't have a link, skip this entry.
            if not href:
                continue

            article_content = client.get(href)
            article_content.raise_for_status()
            article_soup = BeautifulSoup(article_content.text, 'html.parser')
            content_paragraphs = article_soup.find_all(
                ArticleContentSelectors.CONTENT_PARAGRAPH.tag,
                class_=ArticleContentSelectors.CONTENT_PARAGRAPH.class_name,
            )
            content = "\n".join([para.get_text() for para in content_paragraphs]) if content_paragraphs else ''

            article_data = ArticleSchema(
                title=title_tag.get_text(strip=True) if title_tag else '',
                category=category_tag.get_text(strip=True) if category_tag else '',
                publish_time=publish_time_tag.get_text(strip=True) if publish_time_tag else '',
                author=author_tag.get_text(strip=True) if author_tag else '',
                image_url=image_tag.get('src') if image_tag else '',
                full_article_link=href,
                content=content,
            )

            yield article_data