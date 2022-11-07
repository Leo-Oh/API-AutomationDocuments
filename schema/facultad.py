from pydantic import BaseModel, EmailStr
from typing import Optional


class Facultad(BaseModel):
    id: Optional[int]
    nombre: str
    regiones_id: int

class FacultadUpdate(BaseModel):
    nombre: str
    regiones_id: int
