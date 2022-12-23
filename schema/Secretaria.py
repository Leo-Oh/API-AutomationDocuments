from pydantic import BaseModel, EmailStr
from typing import Optional


class Secretaria(BaseModel):
    id: Optional[int]
    id_facultades: int
    nombre: str
    apellido_paterno: str
    apellido_materno: str
    turno: str
    telefono: Optional[str]
    matricula: str
    correo: EmailStr
    contrasena: str
    direccion: Optional[str]
    foto_perfil: Optional[str]

class SecretariaUpdate(BaseModel):
    id_facultades: int
    nombre: str
    apellido_paterno: str
    apellido_materno: str
    turno: str
    telefono: Optional[str]
    matricula: str
    correo: EmailStr
    contrasena: str
    direccion: Optional[str]
    foto_perfil: Optional[str]
    

class SecretariaSettingsUpdate(BaseModel):
    telefono: Optional[str]
    contrasena: str
    direccion: Optional[str]
    foto_perfil: Optional[str]
    

class SecretariaAuth(BaseModel):
    matricula: Optional[str]
    correo : Optional[EmailStr]
    contrasena: str