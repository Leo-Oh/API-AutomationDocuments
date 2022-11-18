from pydantic import BaseModel, EmailStr
from typing import Optional


class Administrador(BaseModel):
    id: Optional[int]
    id_facultades: int
    usuario: str
    correo: EmailStr
    contrasena: str
    nombre: str
    apellido_paterno: str
    apellido_materno: str
    foto_perfil: Optional[str]
    
class AdministradorUpdate(BaseModel):
    id_facultades: int
    usuario: str
    correo: EmailStr
    contrasena: str
    nombre: str
    apellido_paterno: str
    apellido_materno: str
    foto_perfil: Optional[str]
    
    
class AdministradorSettings(BaseModel):
    usuario: str
    correo: EmailStr
    contrasena: str
    foto_perfil: Optional[str]