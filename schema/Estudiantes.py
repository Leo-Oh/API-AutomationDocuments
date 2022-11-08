from pydantic import BaseModel, EmailStr
from typing import Optional


class Estudiante(BaseModel):
    id: Optional[int]
    nombre: str
    apellido_paterno: str
    apellido_materno: str
    matricula: str
    correo: EmailStr
    contrasena: str
    semestre: str
    carreras_id: int
    

class EstudianteUpdate(BaseModel):
    nombre: str
    apellido_paterno: str
    apellido_materno: str
    contrasena: str
    semestre: str
    carreras_id: int
