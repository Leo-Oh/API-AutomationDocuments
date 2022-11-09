
from pydantic import BaseModel, EmailStr, Datetime
from typing import Optional
from datetime import datetime

class Tramites(BaseModel):
    id: Optional[int]
    nombre: str
    aprobado: Optional[bool] = False
    fecha_de_solicitud: Optional[Datetime]= datetime.datetime.now()
    estudiantes_id: int

class TramitesUpdate(BaseModel):
    nombre: str
    aprobado: Optional[bool] = False
    fecha_de_aprobacion: Optional[Datetime] = None