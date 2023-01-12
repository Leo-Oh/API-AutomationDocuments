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
    
class SecretariaSettingsUpdatePassword(BaseModel):
    contrasena: str

class SecretariaSettingsUpdateUserPicture(BaseModel):
    foto_perfil: Optional[str]

class SecretariaAuth(BaseModel):
    matricula: Optional[str]
    correo : Optional[EmailStr]
    contrasena: str
    
class Secretaria_With_IdFacultad_IdCarrera_IdTramite(BaseModel):
    id: Optional[str]
    id_facultades: Optional[str]
    id_tramites: Optional[str]
    id_carreras: Optional[str]
    nombre: Optional[str]
    apellido_paterno: Optional[str]
    apellido_materno: Optional[str]
    turno: Optional[str]
    correo: Optional[str]
