from xmlrpc.client import SERVER_ERROR
from fastapi import APIRouter, Response, Header
from fastapi.responses import JSONResponse 
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from typing import List

from db.db import engine

from schema.SecretariaTramite import SecretariaTramite
from model.SecretariaTramite import secretarias_tramites
import logging
import os

secretariasTramites_Router = APIRouter()
os.makedirs('log/secretarias-tramites', exist_ok=True)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(message)s', filename = "log/secretarias-tramites/registro.log", filemode = 'w',)

@secretariasTramites_Router.get("/secretarias-tramites", response_model=List[SecretariaTramite])
def get_secretarias_tramites():
    try:
        with engine.connect() as conn:
            result = conn.execute(secretarias_tramites.select()).fetchall()
            
        if(result):
            logging.info(f"Se obtuvo información de todas las secretarias y sus respectivos tramites")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    
    except Exception as exception_error:
        logging.error(f"Error al obtener información de las secretarias y sus respectivos tramites ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )


@secretariasTramites_Router.get("/secretaria-tramite/{id_secretaria}", response_model=List[SecretariaTramite])
def get_tramites_by_id_secretaria(id_secretaria:int):
    try:
        with engine.connect() as conn:
            result = conn.execute(secretarias_tramites.select().where(secretarias_tramites.c.id_secretarias == id_secretaria)).fetchall()
        if(result):
            logging.info(f"Se obtuvo todos los ID's de todos los tramites de la secretaria con el ID: {id_secretaria}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener todos los ID's de los tramites de la secretaria con el ID: {id_secretaria} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )


@secretariasTramites_Router.get("/secretaria-tramite/{id_tramites}", response_model=List[SecretariaTramite])
def get_secretarias_by_id_tramite(id_tramites:int):
    try:
        with engine.connect() as conn:
            result = conn.execute(secretarias_tramites.select().where(secretarias_tramites.c.id_tramites == id_tramites)).fetchall()
        if(result):
            logging.info(f"Se obtuvo todos los ID's de todas las secretarias que tienen el ID de tramite: {id_tramites}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener los ID's de las secreatarias que tiene el ID de tramite: {id_tramites} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )


@secretariasTramites_Router.get("/secretaria-tramite/{id_secretaria}/{id_tramite}", response_model=SecretariaTramite )
def check_if_exists_relation_with_secretaria_and_tramite(id_secretaria:int, id_tramite:int):
    try:
        with engine.connect() as conn:
            result = conn.execute(secretarias_tramites.select().where(secretarias_tramites.c.id_secretarias == id_secretaria and secretarias_tramites.c.id_tramites == id_tramite)).first()
        if(result):
            logging.info(f"Se verifico la secretaria con el ID: {id_secretaria} y el tramite con el ID: {id_tramite}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al verificar la secretaria con el ID: {id_secretaria} y el tramite con el ID: {id_tramite} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )

    
@secretariasTramites_Router.post("/secretaria-tramite", status_code=HTTP_201_CREATED)
def create_secretaria_tramite(data_secretaria_tramite: SecretariaTramite):
    try:
        with engine.connect() as conn:    
            new_secretaria_tramite = data_secretaria_tramite.dict()
            conn.execute(secretarias_tramites.insert().values(new_secretaria_tramite))
        logging.info(f"secretaria con ID: {data_secretaria_tramite.id_secretarias} y tramite con el ID: {data_secretaria_tramite.id_tramites} creados correctamente")
        return Response(status_code=HTTP_201_CREATED)
    except Exception as exception_error:
        logging.error(f"Error al crear la secretaria con ID: {data_secretaria_tramite.id_secretarias} y tramite con ID: {data_secretaria_tramite.id_tramites} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )

  
@secretariasTramites_Router.put("/secretaria-tramite/{id_secretaria}/{id_tramite}", response_model=SecretariaTramite)
def update_secretaria_tramite(data_update: SecretariaTramite, id_secretaria: int, id_tramite:int):
    try:
        with engine.connect() as conn:
            conn.execute(secretarias_tramites.update().values(
                id_secretarias = data_update.id_secretarias,
                id_tramites = data_update.id_tramites,
            ).where(secretarias_tramites.c.id_secretarias == id_secretaria and secretarias_tramites.c.id_tramites == id_tramite ))

            result = conn.execute(secretarias_tramites.select().where(secretarias_tramites.c.id_secretarias == id_secretaria and secretarias_tramites.c.id_tramites == id_tramite)).first()

        logging.warning(f"Secretaria con el ID: {data_update.id_secretaria} y el tramite con el ID: {data_update.id_tramite} actualizada correctamente")
        return result
    except Exception as exception_error:
        logging.error(f"Error al actualizar la secretaria con el ID: {data_update.id_secretaria} y el tramite con el ID: {data_update.id_tramite} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )
        

@secretariasTramites_Router.delete("/facultad/{id_secretaria}/{id_tramites}", status_code=HTTP_204_NO_CONTENT)
def delete_secretaria_tramite(id_secretaria:int, id_tramite: int):
    try:
        with engine.connect() as conn:
            conn.execute(secretarias_tramites.delete().where(secretarias_tramites.c.id_secretarias == id_secretaria and secretarias_tramites.c.id_tramites == id_tramite ))
        
        logging.critical(f"la relacion de la secretaria con el ID: {id_secretaria} de que realiza tramites con el ID: {id_tramite} eliminada correctamente")
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al eliminar la relacion de la secretaria con el ID: {id_secretaria} que realiza los tramites con el ID: {id_tramite} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )