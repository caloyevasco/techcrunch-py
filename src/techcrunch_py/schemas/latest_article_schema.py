from pydantic import BaseModel


class LatestArticleSchema(BaseModel):
    element_class: str
    href: str
    text: str
    category: str
    

class ArticleSchema(BaseModel):

    title: str = ''
    category: str = ''
    publish_time: str = ''
    author: str = ''
    image_url: str = ''
    full_article_link: str = ''
    content: str = ''