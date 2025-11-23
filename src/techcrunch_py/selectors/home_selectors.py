from pydantic import BaseModel

class HomePageSelectors(BaseModel):
    latest_article_link: str = "loop-card__title-link"
