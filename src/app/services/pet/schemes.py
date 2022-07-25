from pydantic import (
    BaseModel
)


class Category(BaseModel):
    id: int
    name: str = " Dogs"


class Tags(BaseModel):
    id: int
    name: str


class PetBase(BaseModel):
    id:int
    name: str = "doggie"
    tags: Tags
    category: Category
    status: str = "available"
