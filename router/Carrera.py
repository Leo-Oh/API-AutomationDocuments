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


carreraRouter = APIRouter()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(message)s', filename = "log/registro.log", filemode = 'w',)

@carreraRouter.get("/carreras", response_model=List[Carrera])
def get_facultad():
    try:
        with engine.connect() as conn:
            result = conn.execute(carreras.select()).fetchall()
    
        if(result):
            logging.info(f"Se obtuvo información de todas las carreas")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    
    except Exception as exception_error:
        logging.error(f"Error al obtener información de las carreras: {exception_error}") 
        return Response(status_code= SERVER_ERROR )
   

@carreraRouter.get("/carrera/{carrera_id}", response_model= Carrera)
def get_facultad(carrera_id: int):
    try:
        with engine.connect() as conn:
            result = conn.execute(carreras.select().where(carreras.c.id == carrera_id )).first()
        if(result):
            logging.info(f"Se obtuvo información de la carrera con el ID = {carrera_id} .")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información de la carrera con el ID = {carrera_id}. ") 
        return Response(status_code= SERVER_ERROR )


@carreraRouter.post("/carrera", status_code=HTTP_201_CREATED)
def create_facultad(data_carrera: Carrera):
    try:
        with engine.connect() as conn:    
            new_carrea = data_carrera.dict()
            conn.execute(carreras.insert().values(new_carrea))
        logging.info(f"Carrera {data_carrera.nombre} creada correctamente")
        return Response(status_code=HTTP_201_CREATED)
    except Exception as exception_error:
        logging.error(f"Error al crear la carrera {data_carrera.nombre}: {exception_error}")
        return Response(status_code= SERVER_ERROR )

  
@carreraRouter.put("/carrera/{carrera_id}", response_model=CarreraUpdate)
def update_facultad(data_update: CarreraUpdate , carrera_id: int):
    try:
        with engine.connect() as conn:
            conn.execute(carreras.update().values(
                nombre = data_update.nombre,
            ).where(carreras.c.id == carrera_id))

            result = conn.execute(carreras.select().where(carreras.c.id == carrera_id )).first()

        logging.warning(f"Carrera {data_update.nombre} actualizada correctamente")
        return result
    except Exception as exception_error:
        logging.error(f"Error al actualizar la carrera {data_update.nombre}: {exception_error}")
        return Response(status_code= SERVER_ERROR )
        

@carreraRouter.delete("/carrera/{carrera_id}", status_code=HTTP_204_NO_CONTENT)
def delete_facultad(carrera_id:int):
    try:
        with engine.connect() as conn:
            conn.execute(carreras.delete().where(carreras.c.id == carrera_id))
        
        logging.critical(f"Carrera con el ID {carrera_id} eliminada correctamente")
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al eliminar la carrera con el ID {carrera_id}: {exception_error}")
        return Response(status_code= SERVER_ERROR )