
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
    datos_adjuntos_estudiante:  Optional[str]
    datos_adjuntos_secretaria:  Optional[str]
    mensaje_secretaria:  Optional[str]
    fecha_de_solicitud: Optional[datetime]
    esta: str
    fecha_de_aprobacion: Optional[datetime]
   


class SolicitudTramite(BaseModel):
    id: Optional[int]
    id_secretarias: int
    id_tramites: int
    id_carreras: int
    id_estudiantes: int
    datos_adjuntos_estudiante:  Optional[str]
    estado: str
    fecha_de_solicitud: Optional[datetime]

class SolicitudTramite_update_by_secretaria(BaseModel):
    datos_adjuntos_secretaria:  Optional[str]
    mensaje_secretaria:  Optional[str]
    estado: str
    fecha_de_aprobacion: Optional[datetime]