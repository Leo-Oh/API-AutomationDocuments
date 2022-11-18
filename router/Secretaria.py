from distutils.log import error
from xmlrpc.client import SERVER_ERROR
from fastapi import APIRouter, Response, Header
from fastapi.responses import JSONResponse 
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from typing import List

from schema.Secretaria import Secretaria, SecretariaSettingsUpdate, SecretariaUpdate
from db.db import engine
from model.Secretaria import secretarias
import logging


secretarias_Router = APIRouter()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(message)s', filename = "log/registro.log", filemode = 'w',)

@secretarias_Router.get("/secretarias", response_model=List[Secretaria])
def get_secretarias():
    try:
        with engine.connect() as conn:
            result = conn.execute(secretarias.select()).fetchall()
        if(result):
            logging.info(f"Se obtuvo información de todas las secretarias")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    
    except Exception as exception_error:
        logging.error(f"Error al obtener información de las secretarias ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )
   
@secretarias_Router.get("/secretaria/{id_secretaria}", response_model=Secretaria)
def get_secretaria_by_id_secretaria(id_secretaria: int):
    try:
        with engine.connect() as conn:
            result = conn.execute(secretarias.select().where(secretarias.c.id == id_secretaria)).first()
        if(result):
            logging.info(f"Se obtuvo información de la secretaria con el ID: {id_secretaria}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información de la secretaria con el ID : {id_secretaria} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )

@secretarias_Router.get("/secretaria/{id_facultad}", response_model=List[Secretaria])
def get_secretarias_by_id_facultad(id_facultad: int):
    try:
        with engine.connect() as conn:
            result = conn.execute(secretarias.select().where(secretarias.c.id_facultades == id_facultad)).fetchall()
        if(result):
            logging.info(f"Se obtuvo información de las secretarias de la facultad con el ID: {id_facultad}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información de la secretarias  de la facultad con el ID: {id_facultad} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )

@secretarias_Router.get("/secretaria/{id_facultad}/{id_secretaria}", response_model=Secretaria)
def get_secretaria_by_id_facultad_and_by_id_secretaria(id_facultad: int, id_secretaria: int ):
    try:
        with engine.connect() as conn:
            result = conn.execute(secretarias.select().where(secretarias.c.id == id_secretaria and secretarias.c.id_facultades == id_facultad)).first()
        if(result):
            logging.info(f"Se obtuvo información de la secretaria con el ID: {id_secretaria} de la facultad con el ID: {id_facultad}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información de la secretaria con el ID : {id_secretaria} de la facultad con el ID: {id_facultad} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )


@secretarias_Router.post("/secretaria", status_code=HTTP_201_CREATED)
def create_secretaria(data_secretaria: Secretaria):
    try:
        with engine.connect() as conn:    
            new_secretaria = data_secretaria.dict()
            conn.execute(secretarias.insert().values(new_secretaria))
        logging.info(f"Secretaria {data_secretaria.nombre} creada correctamente")
        return Response(status_code=HTTP_201_CREATED)
    except Exception as exception_error:
        logging.error(f"Error al crear la facultad {data_secretaria.nombre} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )

  
@secretarias_Router.put("/secretaria/{id_facultad}/{id_secretaria}", response_model=Secretaria)
def update_secretaria(data_update: SecretariaUpdate, id_facultad:int, id_secretaria: int):
    try:
        with engine.connect() as conn:
            conn.execute(secretarias.update().values(
                id_facultades = data_update.nombre,    
                nombre = data_update.nombre,
                apellido_paterno = data_update.apellido_paterno,
                apellido_materno = data_update.apellido_materno,
                turno = data_update.turno,
                telefono = data_update.telefono,
                matricula = data_update.matricula,
                correo = data_update.correo,
                contrasena = data_update.contrasena,
                direccion = data_update.direccion,
                foto_perfil = data_update.foto_perfil,
            ).where(secretarias.c.id == id_secretaria and secretarias.c.id_facultades == id_facultad))

            result = conn.execute(secretarias.select().where(secretarias.c.id == id_secretaria and secretarias.c.id == id_facultad )).first()
        logging.warning(f"Secretaria {data_update.nombre} actualizada correctamente")
        return result
    except Exception as exception_error:
        logging.error(f"Error al actualizar la scretaria {data_update.nombre} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )



@secretarias_Router.put("/secretaria/perfil/{id_facultad}/{id_secretaria}", response_model=Secretaria)
def update_settings_secretaria(data_update: SecretariaSettingsUpdate, id_facultad: int, id_secretaria:int):
    try:
        with engine.connect() as conn:
            conn.execute(secretarias.update().values(
                telefono = data_update.telefono,
                contrasena = data_update.contrasena,
                direccion = data_update.direccion,
                foto_perfil = data_update.foto_perfil,
            ).where(secretarias.c.id == id_secretaria and secretarias.c.id_facultades == id_facultad ))

            result = conn.execute(secretarias.select().where(secretarias.c.id == id_secretaria and secretarias.c.id_facultades == id_facultad )).first()

        logging.warning(f"Secretaria con el ID: {id_secretaria} de la facultad con ID: {id_facultad} actualizada correctamente")
        return result
    except Exception as exception_error:
        logging.error(f"Error al actualizar la secretaria con el ID: {id_secretaria} de la facultad con ID: {id_facultad} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )


@secretarias_Router.delete("/secretaria/{id_facultad}/{id_secretaria}", status_code=HTTP_204_NO_CONTENT)
def delete_secretaria(id_facultad:int,id_secretaria:int):
    try:
        with engine.connect() as conn:
            conn.execute(secretarias.delete().where(secretarias.c.id == id_secretaria and secretarias.c.id_facultades == id_facultad ))
        logging.critical(f"Secretaria con el ID {id_secretaria} de la facultad {id_facultad} eliminada correctamente")
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al eliminar la secretaria con el ID {id_secretaria} de la facultad {id_facultad} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )