from distutils.log import error
from xmlrpc.client import SERVER_ERROR
from fastapi import APIRouter, Response, Header
from fastapi.responses import JSONResponse 
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from typing import List

from schema.Carrera import Carrera, CarreraUpdate
from db.db import engine
from model.Carrera import carreras
import logging


carreras_Router = APIRouter()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(message)s', filename = "log/registro.log", filemode = 'w',)

@carreras_Router.get("/carreras", response_model=List[Carrera])
def get_carreras():
    try:
        with engine.connect() as conn:
            result = conn.execute(carreras.select()).fetchall()
    
        if(result):
            logging.info(f"Se obtuvo información de todas las carreas")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    
    except Exception as exception_error:
        logging.error(f"Error al obtener información de las carreras ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )
   

@carreras_Router.get("/carrera/{id_carrera}", response_model= Carrera)
def get_carrera_by_id(id_carrera: int):
    try:
        with engine.connect() as conn:
            result = conn.execute(carreras.select().where(carreras.c.id == id_carrera )).first()
        if(result):
            logging.info(f"Se obtuvo información de la carrera con el ID: {id_carrera}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información de la carrera con el ID: {id_carrera} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )


@carreras_Router.post("/carrera", status_code=HTTP_201_CREATED)
def create_carrera(data_carrera: Carrera):
    try:
        with engine.connect() as conn:    
            new_carrera = data_carrera.dict()
            conn.execute(carreras.insert().values(new_carrera))
        logging.info(f"Carrera {data_carrera.nombre} creada correctamente")
        return Response(status_code=HTTP_201_CREATED)
    except Exception as exception_error:
        logging.error(f"Error al crear la carrera {data_carrera.nombre} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )

  
@carreras_Router.put("/carrera/{id_carrera}", response_model=CarreraUpdate)
def update_carrera(data_update: CarreraUpdate , id_carrera: int):
    try:
        with engine.connect() as conn:
            conn.execute(carreras.update().values(
                nombre = data_update.nombre,
            ).where(carreras.c.id == id_carrera))

            result = conn.execute(carreras.select().where(carreras.c.id == id_carrera )).first()

        logging.warning(f"Carrera {data_update.nombre} actualizada correctamente")
        return result
    except Exception as exception_error:
        logging.error(f"Error al actualizar la carrera {data_update.nombre} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )
        

@carreras_Router.delete("/carrera/{id_carrera}", status_code=HTTP_204_NO_CONTENT)
def delete_carrera(id_carrera:int):
    try:
        with engine.connect() as conn:
            conn.execute(carreras.delete().where(carreras.c.id == id_carrera))
        
        logging.critical(f"Carrera con el ID {id_carrera} eliminada correctamente")
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al eliminar la carrera con el ID {id_carrera} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )