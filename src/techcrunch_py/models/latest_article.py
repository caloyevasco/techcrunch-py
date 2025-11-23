
from pydantic import BaseModel

class HomePageLatestArticleModel(BaseModel):
    title: str = ''
    href: str = ''
