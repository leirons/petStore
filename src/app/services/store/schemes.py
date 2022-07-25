from pydantic import BaseModel


class Order(BaseModel):
    id: int
    pet_id: int
    quantity: int
    status: str
    complete: bool
