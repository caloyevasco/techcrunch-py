from pydantic import BaseModel


class LatestArticleSchema(BaseModel):
    element_class: str
    href: str
    text: str