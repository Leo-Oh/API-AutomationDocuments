from pydantic import BaseModel, EmailStr
from typing import Optional


class SecretariaCarrera(BaseModel):
    id_secretarias: int
    id_carreras: int
