from xmlrpc.client import SERVER_ERROR
from fastapi import APIRouter, Response, Header
from fastapi.responses import JSONResponse 
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from typing import List
from sqlalchemy.sql import text

from db.db import engine

from schema.SecretariaCarrera import SecretariaCarrera
from model.SecretariaCarrera import secretarias_carreras
import logging
import os

secretariasCarreras_Router = APIRouter()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(message)s', filename = "log/registro.log", filemode = 'w',)

@secretariasCarreras_Router.get("/secretarias-carreras", response_model=List[SecretariaCarrera])
def get_secretarias_carreras():
    try:
        with engine.connect() as conn:
            result = conn.execute(secretarias_carreras.select()).fetchall()
            
        if(result):
            logging.info(f"Se obtuvo información de todas las secretarias y su relacion con las carreras ")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    
    except Exception as exception_error:
        logging.error(f"Error al obtener información de las secretarias y sus respectiva relacion con las carreras ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )


@secretariasCarreras_Router.get("/secretaria-carrera/secretaria/{id_secretaria}", response_model=List[SecretariaCarrera])
def get_carreras_by_id_secretaria(id_secretaria:int):
    try:
        with engine.connect() as conn:
            result = conn.execute(secretarias_carreras.select().where(secretarias_carreras.c.id_secretarias == id_secretaria)).fetchall()
        if(result):
            logging.info(f"Se obtuvo todos los ID's de todas las carreras de la secretaria con el ID: {id_secretaria}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener todos los ID's de las carreras de la secretaria con el ID: {id_secretaria} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )


@secretariasCarreras_Router.get("/secretaria-carrera/carrera/{id_carrera}", response_model=List[SecretariaCarrera])
def get_secretarias_by_id_carrera(id_carrera:int):
    try:
        with engine.connect() as conn:
            result = conn.execute(secretarias_carreras.select().where(secretarias_carreras.c.id_carreras == id_carrera)).fetchall()
        if(result):
            logging.info(f"Se obtuvo todos los ID's de todas las secretarias que tienen el ID de carrera: {id_carrera}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener los ID's de las secreatarias que tiene el ID de carrera: {id_carrera} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )


@secretariasCarreras_Router.get("/secretaria-carrera/{id_secretaria}/{id_carrera}", response_model=SecretariaCarrera )
def check_if_exists_relation_with_secretaria_and_carrera(id_secretaria:int, id_carrera:int):
    try:
        with engine.connect() as conn:
            #result = conn.execute(secretarias_carreras.select().where(secretarias_carreras.c.id_secretarias == id_secretaria and secretarias_carreras.c.id_carreras == id_carrera)).first()
            sql_query = text(f'SELECT * FROM secretarias_carreras WHERE id_secretarias = {id_secretaria} AND id_carreras = {id_carrera}')
            result = conn.execute(sql_query).first()
            
            if(result):
                logging.info(f"Se verifico la secretaria con el ID: {id_secretaria} y el carrera con el ID: {id_carrera}")
                return result
            else:
                return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al verificar la secretaria con el ID: {id_secretaria} y el carrera con el ID: {id_carrera} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )

    
@secretariasCarreras_Router.post("/secretaria-carrera", status_code=HTTP_201_CREATED)
def create_secretaria_carrera(data_secretaria_carrera: SecretariaCarrera):
    try:
        with engine.connect() as conn:    
            new_secretaria_carrera = data_secretaria_carrera.dict()
            conn.execute(secretarias_carreras.insert().values(new_secretaria_carrera))
        logging.info(f"secretaria con ID: {data_secretaria_carrera.id_secretarias} y carrera con el ID: {data_secretaria_carrera.id_carreras} creados correctamente")
        return Response(status_code=HTTP_201_CREATED)
    except Exception as exception_error:
        logging.error(f"Error al crear la secretaria con ID: {data_secretaria_carrera.id_secretarias} y carrera con ID: {data_secretaria_carrera.id_carreras} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )

  
@secretariasCarreras_Router.put("/secretaria-carrera/{id_secretaria}/{id_carrera}", response_model=SecretariaCarrera)
def update_secretaria_carrera(data_update: SecretariaCarrera, id_secretaria: int, id_carrera:int):
    try:
        with engine.connect() as conn:
            conn.execute(secretarias_carreras.update().values(
                id_secretarias = data_update.id_secretarias,
                id_carreras = data_update.id_carreras,
            ).where(secretarias_carreras.c.id_secretarias == id_secretaria and secretarias_carreras.c.id_carreras == id_carrera ))

            result = conn.execute(secretarias_carreras.select().where(secretarias_carreras.c.id_secretarias == id_secretaria and secretarias_carreras.c.id_carreras == id_carrera)).first()

        logging.warning(f"Secretaria con el ID: {data_update.id_secretaria} y el carrera con el ID: {data_update.id_carrera} actualizada correctamente")
        return result
    except Exception as exception_error:
        logging.error(f"Error al actualizar la secretaria con el ID: {data_update.id_secretaria} y el carrera con el ID: {data_update.id_carrera} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )
        

@secretariasCarreras_Router.delete("/facultad/secretaria-carrera/{id_carrera}/{id_secretaria}", status_code=HTTP_204_NO_CONTENT)
def delete_secretaria_carrera(id_carrera:int, id_secretaria: int):
    try:
        with engine.connect() as conn:
            conn.execute(secretarias_carreras.delete().where(secretarias_carreras.c.id_carreras == id_carrera and secretarias_carreras.c.id_secretarias == id_secretaria))
            
        logging.critical(f"la relacion de la secretaria con el ID: {id_secretaria} de la carreras con el ID: {id_carrera} eliminada correctamente")
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al eliminar la relacion de la secretaria con el ID: {id_secretaria} de la carreras con el ID: {id_carrera} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )