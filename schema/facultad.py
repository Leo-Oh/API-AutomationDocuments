from pydantic import BaseModel, EmailStr
from typing import Optional


class Facultad(BaseModel):
    id: Optional[int]
    id_regiones: int
    nombre: str
    direccion: str
    telefono: Optional[str]

class FacultadUpdate(BaseModel):
    nombre: str
    direccion: str
    telefono: Optional[str]
