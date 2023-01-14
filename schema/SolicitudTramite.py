
from datetime import datetime
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr

class SolicitudTramiteAllField(BaseModel):
    id: Optional[int]
    id_secretarias: int
    id_tramites: int
    id_carreras: int
    id_estudiantes: int
    datos_adjuntos_estudiante: str
    datos_adjuntos_secretaria: str
    mensaje_secretaria: str
    fecha_de_solicitud: Optional[datetime]
    estado: Optional[str]
    fecha_de_aprobacion: Optional[datetime]
   


class SolicitudTramite(BaseModel):
    id: Optional[int]
    id_secretarias: int
    id_tramites: int
    id_carreras: int
    id_estudiantes: int
    datos_adjuntos_estudiante: str
    estado: Optional[str]
    fecha_de_solicitud: Optional[datetime]

class SolicitudTramite_update_by_secretaria(BaseModel):
    datos_adjuntos_secretaria: str
    mensaje_secretaria: str
    estado: str
    fecha_de_aprobacion: Optional[datetime]