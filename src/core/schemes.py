from pydantic import BaseModel
from typing import Union


class CurrentUser(BaseModel):
    id: Union[int, None]
