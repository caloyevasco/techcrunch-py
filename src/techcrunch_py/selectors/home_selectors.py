from techcrunch_py.selectors.primitives import Selector

class HomePageSelectors:
    LIST_HEADLINES = Selector('ul', 'wp-block-post-template')
    ARTICLE_LIST = Selector('li', 'wp-block-post')
