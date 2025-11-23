from techcrunch_py.selectors.primitives import Selector

class ArticleCardSelectors:
    TITLE = Selector('a', 'loop-card__title-link')
    CATEGORY = Selector('a', 'loop-card__cat')
    ARTICLE_PUBLISH_TIME = Selector('time', 'loop-card__meta-item')
    ARTICLE_AUTHOR = Selector('a', 'loop-card__author')
    ARTICLE_IMAGE = Selector('img', 'attachment-card-block-16x9')
    FULL_ARTICLE_LINK = Selector('a', 'loop-card__title-link')
