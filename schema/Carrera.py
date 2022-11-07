from pydantic import BaseModel, EmailStr
from typing import Optional


class Carrera(BaseModel):
    id: Optional[int]
    nombre: str

class CarreraUpdate(BaseModel):
    nombre: str

