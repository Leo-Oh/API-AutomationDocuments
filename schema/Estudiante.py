from pydantic import BaseModel, EmailStr
from typing import Optional


class Estudiante(BaseModel):
    id: Optional[int]
    id_carreras: int
    nombre: str
    apellido_paterno: str
    apellido_materno: str
    matricula: str
    correo: EmailStr
    contrasena: str
    semestre: str
    telefono: Optional[str]
    foto_perfil: Optional[str]

class EstudianteUpdate(BaseModel):
    id_carreras: int
    nombre: str
    apellido_paterno: str
    apellido_materno: str
    contrasena: str
    semestre: str
    telefono: Optional[str]
    foto_perfil: Optional[str]
    
    
class EstudianteSettings(BaseModel):
    contrasena: str
    telefono: str
    foto_perfil: Optional[str]
    
class EstudianteAuth(BaseModel):
    matricula: Optional[str]
    correo : Optional[EmailStr]
    contrasena: str
