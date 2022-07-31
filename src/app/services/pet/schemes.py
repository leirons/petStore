from pydantic import BaseModel


class Category(BaseModel):
    id: int
    name: str = " Dogs"


class PetBase(BaseModel):
    id: int
    user_id: int
    name: str = "doggie"
    category: Category
    status: str = "available"
