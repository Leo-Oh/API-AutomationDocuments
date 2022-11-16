
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Datetime, EmailStr


class SolicitudTramite_estudiante(BaseModel):
    id: Optional[int]
    id_secretarias: int
    id_tramite: int
    id_carrera: int
    id_estudiante: int
    datos_adjuntos_secretaria: str
    estado: Optional[str:"pendiente"]

class SolicitudTramite_secretaria(BaseModel):
    datos_adjuntos_secretaria: str
    mensaje_secretaria: str
    estado: str
    fecha_de_aprobacion: Optional[datetime.datetime]