from pydantic import BaseModel, EmailStr
from typing import Optional


class FacultadCarrera(BaseModel):
    facultad_id: int
    regiones_id: int
