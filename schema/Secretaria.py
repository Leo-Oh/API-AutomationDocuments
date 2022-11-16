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
    correo: str
    contrasena: str
    direccion: Optional[str]

class SecretariaUpdate(BaseModel):
    id_facultades: int
    nombre: str
    apellido_paterno: str
    apellido_materno: str
    turno: str
    telefono: Optional[str]
    contrasena: str
    direccion: Optional[str]