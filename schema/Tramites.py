
from pydantic import BaseModel, EmailStr, Datetime
from typing import Optional
from datetime import datetime

class Tramite(BaseModel):
    id: Optional[int]
    nombre: str
    descripcion: str


class TramiteUpdate(BaseModel):
    nombre: str
    descripcion: str