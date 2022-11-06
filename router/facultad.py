from distutils.log import error
from xmlrpc.client import SERVER_ERROR
from fastapi import APIRouter, Response, Header
from fastapi.responses import JSONResponse 
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List

from schema.facultad import Facultad
from db.db import engine
from model.facultad import facultades
import logging


facultad = APIRouter()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(message)s', filename = "log/registro.log", filemode = 'w',)

@facultad.get("/facultades", response_model=List[Facultad])
def get_facultad():
    try:
        with engine.connect() as conn:
            result = conn.execute(facultades.select()).fetchall()
    
        if(result):
            logging.info(f"Se obtuvo información de todas las dacultades")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    
    except Exception as exception_error:
        logging.error(f"Error al obtener información de las facultades: {exception_error}") 
        return Response(status_code= SERVER_ERROR )
   


@facultad.get("/facultad/{facultad_id}", response_model=Facultad)
def get_facultad(facultad_id: int):
    try:
        with engine.connect() as conn:
            result = conn.execute(facultades.select().where(facultades.c.id == facultad_id)).first()
        
        if(result):
            logging.info(f"Se obtuvo información de la facultad: {facultad_id}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información de la facultad con id= {facultad_id}: {exception_error}") 
        return Response(status_code= SERVER_ERROR )



@facultad.post("/facultad", status_code=HTTP_201_CREATED)
def create_facultad(data_facultad: Facultad):
    try:
        with engine.connect() as conn:    
            new_facultad = data_facultad.dict()
            conn.execute(facultades.insert().values(new_facultad))
        
        logging.info(f"Facultad {new_facultad.name} creada correctamente")
        return Response(status_code=HTTP_201_CREATED)
    except Exception as exception_error:
        logging.error(f"Error al crear la facultad {facultad.name}: {exception_error}")
        return Response(status_code= SERVER_ERROR )
        
    

  
@facultad.put("/facultad/{facultad_id}", response_model=Facultad)
def update_facultad(data_update: Facultad, facultad_id: str):
    try:
        with engine.connect() as conn:
            conn.execute(facultades.update().values(
                id = data_update.id,
                nombre = data_update.nombre,
                region = data_update.region,
            ).where(facultades.c.id == facultad_id))

            result = conn.execute(facultades.select().where(facultades.c.id == facultad_id)).first()

        logging.warning(f"Facultad {data_update.nombre} actualizada correctamente")
        return result
    except Exception as exception_error:
        logging.error(f"Error al actualizar la facultad {data_update.nombre}: {exception_error}")
        return Response(status_code= SERVER_ERROR )
        

@facultad.delete("/facultad/{facultad_id}", status_code=HTTP_204_NO_CONTENT)
def delete_facultad(facultad_id: str):
    try:
        with engine.connect() as conn:
            conn.execute(facultades.delete().where(facultades.c.id == facultad_id))
        
        logging.critical(f"Error al eliminar la facultad {facultad_id}: {exception_error}")
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al eliminar la facultad {facultad_id}: {exception_error}")
        return Response(status_code= SERVER_ERROR )