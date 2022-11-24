from pydantic import BaseModel, EmailStr
from typing import Optional


class Region(BaseModel):
    id: Optional[int]
    nombre: str

class RegionUpdate(BaseModel):
    nombre: str
    
