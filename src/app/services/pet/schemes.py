from typing import List

from pydantic import BaseModel, create_model, validator


class Category(BaseModel):
    id: int
    name: str = "Dogs"


class Tag(BaseModel):
    name: str = "Tag"


def exclude_id(baseclass, to_exclude: list):
    fields = baseclass.__fields__
    validators = {'__validators__': baseclass.__validators__}
    new_fields = {key: (item.type_, ... if item.required else None)
                  for key, item in fields.items() if key not in to_exclude}
    return create_model(f'{baseclass.__name__}Excluded', **new_fields, __validators__=validators)


class PetBase(BaseModel):
    id: int
    user_id: int
    name: str = "doggie"
    category: Category
    status: str = "available"
    tag: List[Tag]

    @validator("status")
    def validate_status(cls, status):
        if status != "available" and status != "pending" and status != "sold":
            raise ValueError(
                "Status does not correct, available status: available,sold,pending"
            )
        return status


class PetPut(BaseModel):
    user_id: int
    name: str = "doggie"
    category: Category
    status: str = "available"
    tag: List[Tag]

    @validator("status")
    def validate_status(cls, status):
        if status != "available" and status != "pending" and status != "sold":
            raise ValueError(
                "Status does not correct, available status: available,sold,pending"
            )
        return status
