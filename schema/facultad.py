from pydantic import BaseModel, EmailStr
from typing import Optional


class Facultad(BaseModel):
    id: Optional[int]
    name: str
    region: str

