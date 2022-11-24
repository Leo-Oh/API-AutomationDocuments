
from pydantic import BaseModel
from typing import Optional

class Tramite(BaseModel):
    id: Optional[int]
    nombre: str
    descripcion: str


class TramiteUpdate(BaseModel):
    nombre: str
    descripcion: str