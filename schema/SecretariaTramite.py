from pydantic import BaseModel, EmailStr
from typing import Optional


class SecretariaTramite(BaseModel):
    id_secretarias: int
    id_tramites: int
