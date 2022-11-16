from distutils.log import error
from xmlrpc.client import SERVER_ERROR
from fastapi import APIRouter, Response, Header
from fastapi.responses import JSONResponse 
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from typing import List

from schema.Facultad import Facultad, FacultadUpdate
from db.db import engine
from model.Facultad import facultades
import logging


facultadRouter = APIRouter()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(message)s', filename = "log/registro.log", filemode = 'w',)

@facultadRouter.get("/facultades", response_model=List[Facultad])
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
   

@facultadRouter.get("/facultad/{region_id}/{facultad_id}", response_model=Facultad)
def get_facultad(region_id: int, facultad_id: int):
    try:
        with engine.connect() as conn:
            result = conn.execute(facultades.select().where(facultades.c.id == facultad_id and region_id == region_id)).first()
        if(result):
            logging.info(f"Se obtuvo información de la facultad con el ID = {region_id} y la region con el ID= {facultad_id}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información de la facultad con el ID = {region_id} y la region con el ID= {facultad_id}: {exception_error}") 
        return Response(status_code= SERVER_ERROR )


@facultadRouter.post("/facultad", status_code=HTTP_201_CREATED)
def create_facultad(data_facultad: Facultad):
    try:
        with engine.connect() as conn:    
            new_facultad = data_facultad.dict()
            conn.execute(facultades.insert().values(new_facultad))
        logging.info(f"Facultad {data_facultad.nombre} creada correctamente")
        return Response(status_code=HTTP_201_CREATED)
    except Exception as exception_error:
        logging.error(f"Error al crear la facultad {data_facultad.nombre}: {exception_error}")
        return Response(status_code= SERVER_ERROR )

  
@facultadRouter.put("/facultad/{region_id}/{facultad_id}", response_model=Facultad)
def update_facultad(data_update: FacultadUpdate, region_id: int, facultad_id: int):
    try:
        with engine.connect() as conn:
            conn.execute(facultades.update().values(
                nombre = data_update.nombre,
                region_id = data_update.regiones_id
            ).where(facultades.c.id == facultad_id and facultades.c.regiones_id == region_id))

            result = conn.execute(facultades.select().where(facultades.c.id == facultad_id and region_id == region_id)).first()

        logging.warning(f"Facultad {data_update.nombre} actualizada correctamente")
        return result
    except Exception as exception_error:
        logging.error(f"Error al actualizar la facultad {data_update.nombre}: {exception_error}")
        return Response(status_code= SERVER_ERROR )
        

@facultadRouter.delete("/facultad/{region_id}/{facultad_id}", status_code=HTTP_204_NO_CONTENT)
def delete_facultad(region_id:int, facultad_id: str):
    try:
        with engine.connect() as conn:
            conn.execute(facultades.delete().where(facultades.c.id == facultad_id and facultades.c.regiones_id == region_id))
        
        logging.critical(f"Facultad con el ID {facultad_id} de la region {region_id} eliminada correctamente")
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al eliminar la facultad  con el ID {facultad_id} de la region {region_id} : {exception_error}")
        return Response(status_code= SERVER_ERROR )