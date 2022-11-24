from pydantic import BaseModel, EmailStr
from typing import Optional


class FacultadCarrera(BaseModel):
    id_facultades: int
    id_carreras: int
