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


facultades_Router = APIRouter()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(message)s', filename = "log/registro.log", filemode = 'w',)

@facultades_Router.get("/facultades", response_model=List[Facultad])
def get_facultades():
    try:
        with engine.connect() as conn:
            result = conn.execute(facultades.select()).fetchall()
        if(result):
            logging.info(f"Se obtuvo información de todas las facultades")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    
    except Exception as exception_error:
        logging.error(f"Error al obtener información de las facultades ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )
   
@facultades_Router.get("/facultad/{id_facultad}", response_model=Facultad)
def get_facultad_by_id_facultad(id_facultad: int):
    try:
        with engine.connect() as conn:
            result = conn.execute(facultades.select().where(facultades.c.id == id_facultad)).first()
        if(result):
            logging.info(f"Se obtuvo información de la facultad con el ID: {id_facultad}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información de la facultad con el ID : {id_facultad} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )

@facultades_Router.get("/facultad/{id_region}", response_model=List[Facultad])
def get_facultad_by_id_region_and_by_id_facultad(id_region: int):
    try:
        with engine.connect() as conn:
            result = conn.execute(facultades.select().where(facultades.c.id_regiones == id_region)).fetchall()
        if(result):
            logging.info(f"Se obtuvo información de las facultades de la region con el ID: {id_region}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información de las facultades de la region con el ID: {id_region} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )


@facultades_Router.get("/facultad/{id_region}/{id_facultad}", response_model=Facultad)
def get_facultad_by_id_region_and_by_id_facultad(id_region: int, id_facultad: int):
    try:
        with engine.connect() as conn:
            result = conn.execute(facultades.select().where(facultades.c.id == id_facultad and facultades.c.id_regiones == id_region)).first()
        if(result):
            logging.info(f"Se obtuvo información de la facultad con el ID: {id_facultad} de la region con el ID: {id_region}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información de la facultad con el ID : {id_facultad} y la region con el ID: {id_region} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )


@facultades_Router.post("/facultad", status_code=HTTP_201_CREATED)
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

  
@facultades_Router.put("/facultad/{id_region}/{id_facultad}", response_model=Facultad)
def update_facultad(data_update: FacultadUpdate, id_region: int, id_facultad: int):
    try:
        with engine.connect() as conn:
            conn.execute(facultades.update().values(
                nombre = data_update.nombre,
                direccion = data_update.direccion,
                telefono = data_update.telefono,
            ).where(facultades.c.id == id_facultad and facultades.c.id_regiones == id_region))

            result = conn.execute(facultades.select().where(facultades.c.id == id_facultad and id_region == id_region)).first()

        logging.warning(f"Facultad {data_update.nombre} actualizada correctamente")
        return result
    except Exception as exception_error:
        logging.error(f"Error al actualizar la facultad {data_update.nombre} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )
        

@facultades_Router.delete("/facultad/{id_region}/{id_facultad}", status_code=HTTP_204_NO_CONTENT)
def delete_facultad(id_region:int, id_facultad: str):
    try:
        with engine.connect() as conn:
            conn.execute(facultades.delete().where(facultades.c.id == id_facultad and facultades.c.id_regiones == id_region))
        
        logging.critical(f"Facultad con el ID {id_facultad} de la region {id_region} eliminada correctamente")
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al eliminar la facultad  con el ID {id_facultad} de la region {id_region} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )
