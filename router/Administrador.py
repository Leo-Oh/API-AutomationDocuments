import logging
import os

from xmlrpc.client import SERVER_ERROR
from fastapi import APIRouter, Response, Header
from fastapi.responses import JSONResponse 
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from typing import List
from werkzeug.security import generate_password_hash, check_password_hash

from schema.Administrador import Administrador, AdministradorAuth, AdministradorSettings, AdministradorUpdate
from db.db import engine
from model.Administrador import administradores

from functions_jwt import write_token, validate_token


administradores_Router = APIRouter()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(message)s', filename = "log/registro.log", filemode = 'w',)

@administradores_Router.get("/administradores", response_model=List[Administrador])
def get_administradores():
    try:
        with engine.connect() as conn:
            result = conn.execute(administradores.select()).fetchall()
        if(result):
            logging.info(f"Se obtuvo información de todos los administradores")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    
    except Exception as exception_error:
        logging.error(f"Error al obtener información de los administradores ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )
   
@administradores_Router.get("/administrador/administrador/{id_administrador}", response_model=Administrador)
def get_administrador_by_id_administrador(id_administrador: int):
    try:
        with engine.connect() as conn:
            result = conn.execute(administradores.select().where(administradores.c.id == id_administrador)).first()
        if(result):
            logging.info(f"Se obtuvo información del administrador con el ID: {id_administrador}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información del administrador con el ID : {id_administrador} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )


@administradores_Router.get("/administrador/facultad/{id_facultad}", response_model=List[Administrador])
def get_administrador_by_id_facultad(id_facultad: int ):
    try:
        with engine.connect() as conn:
            result = conn.execute(administradores.select().where(administradores.c.id_facultades == id_facultad)).fetchall()
        if(result):
            logging.info(f"Se obtuvo información de los administradores que pertencen a la facultad con el ID: {id_facultad} ")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información de los administradores que pertenecen a la facultad con el ID : {id_facultad} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )


@administradores_Router.get("/administrador/facultad/administrador/{id_facultad}/{id_administrador}", response_model=Administrador)
def get_administrador_by_id_facultad_and_by_id_administrador(id_facultad: int, id_administrador: int ):
    try:
        with engine.connect() as conn:
            result = conn.execute(administradores.select().where(administradores.c.id == id_administrador and administradores.c.id_facultades == id_facultad)).first()
        if(result):
            logging.info(f"Se obtuvo información del administador con el ID: {id_administrador} de la facultad con el ID: {id_facultad}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información del administrador con el ID : {id_administrador} de la facultad con el ID: {id_facultad} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )


@administradores_Router.post("/administrador", status_code=HTTP_201_CREATED)
def create_administrador(data_administrador: Administrador):
    try:
        with engine.connect() as conn:    
            result = conn.execute(administradores.select().where(administradores.c.correo == data_administrador.correo or administradores.c.usuario == data_administrador.usuario)).first()
            if result != None:
                return Response(status_code=HTTP_401_UNAUTHORIZED)
            
            new_administrador = data_administrador.dict()
            new_administrador["contrasena"] = generate_password_hash(data_administrador.contrasena, "pbkdf2:sha256:30", 30)

            conn.execute(administradores.insert().values(new_administrador))
            logging.info(f"Administrador {data_administrador.nombre} creado correctamente")
        return Response(status_code=HTTP_201_CREATED)
    except Exception as exception_error:
        logging.error(f"Error al crear el administrador {data_administrador.nombre} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )
    

@administradores_Router.post("/administrador/ingresar")
def administradores_ingresar_al_sistema(administrador : AdministradorAuth):
  with engine.connect() as conn:
    if(administrador.correo != None):
        result = conn.execute(administradores.select().where(administradores.c.correo == administrador.correo )).first()
    if(administrador.usuario != None):
        result = conn.execute(administradores.select().where(administradores.c.usuario == administrador.usuario )).first()

    print(result[4])

    if result != None:
        check_passw = check_password_hash(result[4], administrador.contrasena)
        if check_passw:
            return {
            "status": 200,
            "message": "Access success",
            "token" : write_token(administrador.dict()),
            "user" : result
            }
        else:
            return Response(status_code=HTTP_401_UNAUTHORIZED)
    else:
        return JSONResponse(content={"message": "Usuario no encontrado"}, status_code=404)

@administradores_Router.post("/administrador/verify/token")
def verify_token(token_administrador:str=Header(default=None)):
  token = token_administrador.split(" ")[0]
  return validate_token(token, output=True)

  
@administradores_Router.put("/administrador/{id_facultad}/{id_administrador}", response_model=AdministradorUpdate)
def update_administrador(data_update: AdministradorUpdate, id_facultad: int, id_administrador:int):
    try:
        with engine.connect() as conn:
            encryp_passw = generate_password_hash(data_update.contrasena, "pbkdf2:sha256:30", 30)
            
            conn.execute(administradores.update().values(                                
                id_facultades =  data_update.id_facultades,
                usuario =  data_update.usuario,
                correo =  data_update.correo,
                contrasena =  encryp_passw,
                nombre =  data_update.nombre,
                apellido_paterno =  data_update.apellido_paterno,
                apellido_materno =  data_update.apellido_materno,
                foto_perfil =  data_update.foto_perfil,
            ).where(administradores.c.id == id_administrador and administradores.c.id_facultades == id_facultad ))

            result = conn.execute(administradores.select().where(administradores.c.id == id_administrador and administradores.c.id_facultades == id_facultad )).first()
        logging.warning(f"Administrador {data_update.nombre} actualizada correctamente")
        return result
    except Exception as exception_error:
        logging.error(f"Error al actualizar el administrador {data_update.nombre} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )



@administradores_Router.put("/administrador/perfil/{id_facultad}/{id_administrador}", response_model=AdministradorSettings)
def update_settings_administrador(data_update: AdministradorSettings, id_facultad: int, id_administrador:int):
    try:
        with engine.connect() as conn:
            encryp_passw = generate_password_hash(data_update.contrasena, "pbkdf2:sha256:30", 30)
            conn.execute(administradores.update().values(
                usuario = data_update.usuario,
                correo = data_update.correo,
                contrasena = encryp_passw,
                foto_perfil = data_update.foto_perfil,
            ).where(administradores.c.id == id_administrador and administradores.c.id_facultades ==id_facultad ))

            result = conn.execute(administradores.select().where(administradores.c.id == id_administrador and administradores.c.id_facultades == id_facultad )).first()

        logging.warning(f"Administrador con el ID: {id_administrador} de la facultad con ID: {id_facultad} actualizada correctamente")
        return result
    except Exception as exception_error:
        logging.error(f"Error al actualizar el administrador con el ID: {id_administrador} de la facultad con ID: {id_facultad} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )


@administradores_Router.delete("/administrador/{id_facultad}/{id_administrador}", status_code=HTTP_204_NO_CONTENT)
def delete_administrador(id_facultad:int, id_administrador:int, ):
    try:
        with engine.connect() as conn:
            conn.execute(administradores.delete().where(administradores.c.id == id_administrador and administradores.c.id_facultades == id_facultad ))
        logging.critical(f"Administrador con el ID {id_administrador} de la facultad con el ID: {id_facultad} eliminada correctamente")
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al eliminar al administrador con el ID {id_administrador} de la facultad {id_facultad} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )