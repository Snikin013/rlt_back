from typing import Optional
from pydantic import BaseModel



class UserDataUpdateForm(BaseModel):
    napr: str


class check_inn(BaseModel):
    innform: str


