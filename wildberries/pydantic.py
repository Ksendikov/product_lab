from pydantic import BaseModel, Field


class CardPydantic(BaseModel):
    article: int = Field(alias='id')
    brand: str
    title: str = Field(alias='name')
