from pydantic import BaseModel, validator


class Order(BaseModel):
    id: int
    pet_id: int
    quantity: int
    status: str
    complete: bool

    @validator("status")
    def validate_status(cls, status):
        if status != "complete" and status != "approved" and status != "delivered":
            raise ValueError(
                "Status does not correct, available status: complete,approved,delivered. "
            )
        return status


class OrderUpdate(BaseModel):
    pet_id: int
    quantity: int
    status: str
    complete: bool

    @validator("status")
    def validate_status(cls, status):
        if status != "complete" and status != "approved" and status != "delivered":
            raise ValueError(
                "Status does not correct, available status: complete,approved,delivered. "
            )
        return status
