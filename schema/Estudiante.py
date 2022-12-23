from pydantic import BaseModel, EmailStr
from typing import Optional


class Estudiante(BaseModel):
    id: Optional[int]
    id_carreras: int
    id_facultades: int
    nombre_completo: str
    #nombre: str
    #apellido_paterno: str
    #apellido_materno: str
    matricula: str
    correo: EmailStr
    contrasena: str
    semestre: int
    telefono: Optional[str]
    foto_perfil: Optional[str]

class EstudianteUpdate(BaseModel):
    id_carreras: int
    id_facultades: int
    nombre_completo: str
    #apellido_paterno: str
    #apellido_materno: str
    matricula: str
    correo: EmailStr
    contrasena: str
    semestre: int
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
