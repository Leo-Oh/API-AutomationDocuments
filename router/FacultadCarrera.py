from distutils.log import error
from xmlrpc.client import SERVER_ERROR
from fastapi import APIRouter, Response, Header
from fastapi.responses import JSONResponse 
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from typing import List

from db.db import engine
from schema.Carrera import Carrera
from schema.Facultad import Facultad
from schema.FacultadCarrera import FacultadCarrera
from model.FacultadCarrera import facultades_carreras
import logging


facultad_carreraRouter = APIRouter()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(message)s', filename = "log/registro.log", filemode = 'w',)

@facultad_carreraRouter.get("/facultades-carreras", response_model=List[FacultadCarrera])
def get_facultades():
    try:
        with engine.connect() as conn:
            result = conn.execute(facultades_carreras.select()).fetchall()
            
        if(result):
            logging.info(f"Se obtuvo información de todas las dacultades Y carreras")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    
    except Exception as exception_error:
        logging.error(f"Error al obtener información de las facultades y carreras: {exception_error}") 
        return Response(status_code= SERVER_ERROR )


@facultad_carreraRouter.get("/facultades-carreras/{facultades_id}", response_model=List[FacultadCarrera])
def get_carreras_from_facultad(facultades_id:int):
    try:
        with engine.connect() as conn:
            result = conn.execute(facultades_carreras.select().where(facultades_carreras.c.facultades_id == facultades_id)).fetchall()
        if(result):
            logging.info(f"Se obtuvo información de todas las carreras de la facultad con el ID: {facultades_id}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información de las carreras de la facultad con el ID= {facultades_id}: {exception_error}") 
        return Response(status_code= SERVER_ERROR )


@facultad_carreraRouter.get("/facultades-carreras/{carreras_id}", response_model=List[FacultadCarrera])
def get_carreras_from_facultad(carreras_id:int):
    try:
        with engine.connect() as conn:
            result = conn.execute(facultades_carreras.select().where(facultades_carreras.c.carreras_id == carreras_id)).fetchall()
        if(result):
            logging.info(f"Se obtuvo información de todas las facultad que tienen la carrera con el ID: {carreras_id}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información de las facultades que tienen la carrera con el ID= {carreras_id}: {exception_error}") 
        return Response(status_code= SERVER_ERROR )


    
@facultad_carreraRouter.post("/facultades-carreras", status_code=HTTP_201_CREATED)
def create_facultad(data_facultadCarrera: FacultadCarrera):
    try:
        with engine.connect() as conn:    
            new_facultad = data_facultadCarrera.dict()
            conn.execute(facultades_carreras.insert().values(new_facultad))
        logging.info(f"Facultad con ID: {data_facultadCarrera.facultad_id} y carrera con ID: {data_facultadCarrera.carrera_id} creados correctamente")
        return Response(status_code=HTTP_201_CREATED)
    except Exception as exception_error:
        logging.error(f"Error al crear la facultad con ID: {data_facultadCarrera.facultad_id} y carrera con ID: {data_facultadCarrera.carrera_id}: {exception_error}")
        return Response(status_code= SERVER_ERROR )

  
@facultad_carreraRouter.put("/facultades-carreras/{facultad_id}/{carrera_id}", response_model=FacultadCarrera)
def update_facultad(data_update: FacultadCarrera, facultad_id: int, carrera_id:int):
    try:
        with engine.connect() as conn:
            conn.execute(facultades_carreras.update().values(
                facultad_id = data_update.facultad_id,
                carrera_id = data_update.carrera_id,
            ).where(facultades_carreras.c.facultades_id == facultad_id and facultades_carreras.c.carreras_id == carrera_id ))

            result = conn.execute(facultades_carreras.select().where(facultades_carreras.c.facultades_id == facultad_id and facultades_carreras.c.carreras_id == carrera_id)).first()

        logging.warning(f"Facultad con el ID: {data_update.facultad_id} y la carrera con el ID: {data_update.carrera_id} actualizada correctamente")
        return result
    except Exception as exception_error:
        logging.error(f"Error al actualizar la facultad con el ID: {data_update.facultad_id} y la carrera con el ID: {data_update.carrera_id}: {exception_error}")
        return Response(status_code= SERVER_ERROR )
        

@facultad_carreraRouter.delete("/facultad/{facultad_id}/{carrera__id}", status_code=HTTP_204_NO_CONTENT)
def delete_facultad(facultad_id:int, carrera_id: str):
    try:
        with engine.connect() as conn:
            conn.execute(facultades_carreras.delete().where(facultades_carreras.c.facultad_id == facultad_id and facultades_carreras.c.carreras_id == carrera_id ))
        
        logging.critical(f"Facultad con el ID= {facultad_id} de con la carrera ID= {carrera_id} eliminada correctamente")
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al eliminar la facultad  con el ID= {facultad_id} con la carrera ID= {carrera_id} : {exception_error}")
        return Response(status_code= SERVER_ERROR )