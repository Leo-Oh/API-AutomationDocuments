from distutils.log import error
from xmlrpc.client import SERVER_ERROR
from fastapi import APIRouter, Response, Header
from fastapi.responses import JSONResponse 
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from typing import List

from db.db import engine

from schema.FacultadCarrera import FacultadCarrera
from model.FacultadCarrera import facultades_carreras
import logging


facultadesCarreras_Router = APIRouter()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(message)s', filename = "log/registro.log", filemode = 'w',)

@facultadesCarreras_Router.get("/facultades-carreras", response_model=List[FacultadCarrera])
def get_facultades_carreras():
    try:
        with engine.connect() as conn:
            result = conn.execute(facultades_carreras.select()).fetchall()
            
        if(result):
            logging.info(f"Se obtuvo información de todas las dacultades Y carreras")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    
    except Exception as exception_error:
        logging.error(f"Error al obtener información de las facultades y carreras ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )


@facultadesCarreras_Router.get("/facultades-carreras/{id_facultad}", response_model=List[FacultadCarrera])
def get_carreras_by_id_facultad(id_facultad:int):
    try:
        with engine.connect() as conn:
            result = conn.execute(facultades_carreras.select().where(facultades_carreras.c.id_facultades == id_facultad)).fetchall()
        if(result):
            logging.info(f"Se obtuvo todos los ID's de todas las carreras de la facultad con el ID: {id_facultad}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener todos los ID's de las carreras de la facultad con el ID: {id_facultad} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )


@facultadesCarreras_Router.get("/facultades-carreras/{id_carrera}", response_model=List[FacultadCarrera])
def get_facultades_by_id_carrera(id_carrera:int):
    try:
        with engine.connect() as conn:
            result = conn.execute(facultades_carreras.select().where(facultades_carreras.c.id_carreras == id_carrera)).fetchall()
        if(result):
            logging.info(f"Se obtuvo todos los ID's de todas las facultades que tienen la carrera con el ID: {id_carrera}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener los ID's de las facultades que tienen la carrera con el ID: {id_carrera} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )


@facultadesCarreras_Router.get("/facultades-carreras/{id_facultad}/{id_carrera}", response_model=FacultadCarrera )
def check_if_exists_relation_with_facultad_carrera(id_facultad:int, id_carrera:int):
    try:
        with engine.connect() as conn:
            result = conn.execute(facultades_carreras.select().where(facultades_carreras.c.id_facultades == id_facultad and facultades_carreras.c.id_carreras == id_carrera)).fetchall()
        if(result):
            logging.info(f"Se verifico la facultad con el ID: {id_facultad} y la carrera con el ID: {id_carrera}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al verificar la facultad con el ID: {id_facultad} y la carrera con el ID: {id_carrera} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )

    
@facultadesCarreras_Router.post("/facultades-carreras", status_code=HTTP_201_CREATED)
def create_facultad_carrera(data_facultadCarrera: FacultadCarrera):
    try:
        with engine.connect() as conn:    
            new_facultad = data_facultadCarrera.dict()
            conn.execute(facultades_carreras.insert().values(new_facultad))
        logging.info(f"Facultad con ID: {data_facultadCarrera.id_facultades} y carrera con ID: {data_facultadCarrera.id_carreras} creados correctamente")
        return Response(status_code=HTTP_201_CREATED)
    except Exception as exception_error:
        logging.error(f"Error al crear la facultad con ID: {data_facultadCarrera.facultad_id} y carrera con ID: {data_facultadCarrera.carrera_id} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )

  
@facultadesCarreras_Router.put("/facultades-carreras/{facultad_id}/{carrera_id}", response_model=FacultadCarrera)
def update_facultad_carrera(data_update: FacultadCarrera, facultad_id: int, carrera_id:int):
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
        logging.error(f"Error al actualizar la facultad con el ID: {data_update.facultad_id} y la carrera con el ID: {data_update.carrera_id} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )
        

@facultadesCarreras_Router.delete("/facultad/{id_facultad}/{id_carrera}", status_code=HTTP_204_NO_CONTENT)
def delete_facultad_carrera(id_facultad:int, id_carrera: str):
    try:
        with engine.connect() as conn:
            conn.execute(facultades_carreras.delete().where(facultades_carreras.c.id_facultades == id_facultad and facultades_carreras.c.id_carreras == id_carrera ))
        
        logging.critical(f"Facultad con el ID: {id_facultad} de con el ID de la carrera: {id_carrera} eliminada correctamente")
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al eliminar la facultad  con el ID: {id_facultad} con la carrera con el ID: {id_carrera} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )