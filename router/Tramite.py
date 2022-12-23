from distutils.log import error
from xmlrpc.client import SERVER_ERROR
from fastapi import APIRouter, Response, Header
from fastapi.responses import JSONResponse 
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from typing import List

from schema.Tramites import Tramite, TramiteUpdate
from db.db import engine
from model.Tramites import tramites
import logging
import os

tramites_Router = APIRouter()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(message)s', filename = "log/registro.log", filemode = 'w',)

@tramites_Router.get("/tramites", response_model=List[Tramite])
def get_tramites():
    try:
        with engine.connect() as conn:
            result = conn.execute(tramites.select()).fetchall()
    
        if(result):
            logging.info(f"Se obtuvo información de todos los tramites posibles")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    
    except Exception as exception_error:
        logging.error(f"Error al obtener información de todos los tramites posibles ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )
   

@tramites_Router.get("/tramite/{id_tramite}", response_model= Tramite)
def get_tramite(id_tramite: int):
    try:
        with engine.connect() as conn:
            result = conn.execute(tramites.select().where(tramites.c.id == id_tramite )).first()
        if(result):
            logging.info(f"Se obtuvo información del tramite con el ID: {id_tramite}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información del tramite con el ID: {id_tramite} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )


@tramites_Router.post("/tramite", status_code=HTTP_201_CREATED)
def create_tramite(data_tramite: Tramite):
    try:
        with engine.connect() as conn:    
            new_tramite = data_tramite.dict()
            conn.execute(tramites.insert().values(new_tramite))
        logging.info(f"Tramites {data_tramite.nombre} creado correctamente")
        return Response(status_code=HTTP_201_CREATED)
    except Exception as exception_error:
        logging.error(f"Error al crea el tramite {data_tramite.nombre} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )

  
@tramites_Router.put("/tramite/{id_tramite}", response_model=TramiteUpdate)
def update_tramite(data_update: TramiteUpdate , id_tramite: int):
    try:
        with engine.connect() as conn:
            conn.execute(tramites.update().values(
                nombre = data_update.nombre,
                descripcion = data_update.descripcion,
            ).where(tramites.c.id == id_tramite))

            result = conn.execute(tramites.select().where(tramites.c.id == id_tramite )).first()

        logging.warning(f"Tramites {data_update.nombre} actualizado correctamente")
        return result
    except Exception as exception_error:
        logging.error(f"Error al actualizar el tramite {data_update.nombre} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )
        

@tramites_Router.delete("/tramite/{id_tramite}", status_code=HTTP_204_NO_CONTENT)
def delete_tramite(id_tramite:int):
    try:
        with engine.connect() as conn:
            conn.execute(tramites.delete().where(tramites.c.id == id_tramite))
        
        logging.critical(f"Tramites con el ID {id_tramite} eliminada correctamente")
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al eliminar la carrera con el ID: {id_tramite} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )