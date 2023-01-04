from distutils.log import error
from xmlrpc.client import SERVER_ERROR
from fastapi import APIRouter, Response, Header
from fastapi.responses import JSONResponse
from functions_jwt import write_token 
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from typing import List

from schema.Secretaria import Secretaria, SecretariaAuth, SecretariaSettingsUpdate, SecretariaSettingsUpdatePassword, SecretariaSettingsUpdateUserPicture, SecretariaUpdate
from db.db import engine
from model.Secretaria import secretarias
import logging

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import text

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
   
@secretarias_Router.get("/secretaria/secretaria/{id_secretaria}", response_model=Secretaria)
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

@secretarias_Router.get("/secretaria/facultad/{id_facultad}", response_model=List[Secretaria])
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

@secretarias_Router.get("/secretaria/facultad-secretaria/{id_facultad}/{id_secretaria}", response_model=Secretaria)
def get_secretaria_by_id_facultad_and_by_id_secretaria(id_facultad: int, id_secretaria: int ):
    try:
        with engine.connect() as conn:
            #result = conn.execute(secretarias.select().where(secretarias.c.id == id_secretaria and secretarias.c.id_facultades == id_facultad)).first()
            sql_query = text(f'SELECT * FROM secretarias WHERE id = {id_secretaria} AND id_facultades = {id_facultad}')
            result = conn.execute(sql_query).first()
            
            
        if(result):
            logging.info(f"Se obtuvo información de la secretaria con el ID: {id_secretaria} de la facultad con el ID: {id_facultad}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información de la secretaria con el ID : {id_secretaria} de la facultad con el ID: {id_facultad} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )

@secretarias_Router.post("/secretaria/ingresar")
def secretarias_ingresar_al_sistema(secretaria : SecretariaAuth):
  with engine.connect() as conn:
    if(secretaria.correo != None):
        result = conn.execute(secretarias.select().where(secretarias.c.correo == secretaria.correo )).first()
    if(secretaria.matricula != None):
        result = conn.execute(secretarias.select().where(secretarias.c.matricula == secretaria.matricula )).first()

    print(result[9])

    if result != None:
        check_passw = check_password_hash(result[9], secretaria.contrasena)
        if check_passw:
            return {
            "status": 200,
            "message": "Access success",
            "token" : write_token(secretaria.dict()),
            "user" : result
            }
        else:
            return Response(status_code=HTTP_401_UNAUTHORIZED)
    else:
        return JSONResponse(content={"message": "Usuario no encontrado"}, status_code=404)


@secretarias_Router.post("/secretaria", status_code=HTTP_201_CREATED)
def create_secretaria(data_secretaria: Secretaria):
    try:
        with engine.connect() as conn:
            result = conn.execute(secretarias.select().where(secretarias.c.correo == data_secretaria.correo or secretarias.c.matricula == data_secretaria.matricula)).first()
            
            if result != None:
                return Response(status_code=HTTP_401_UNAUTHORIZED)
            
            new_secretaria = data_secretaria.dict()
            new_secretaria["contrasena"] = generate_password_hash(data_secretaria.contrasena, "pbkdf2:sha256:30", 30)
            
            conn.execute(secretarias.insert().values(new_secretaria))
        logging.info(f"Secretaria {data_secretaria.nombre} creada correctamente")
        return Response(status_code=HTTP_201_CREATED)
    except Exception as exception_error:
        logging.error(f"Error al crear la secretaria {data_secretaria.nombre} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )



@secretarias_Router.put("/secretaria/{id_facultad}/{id_secretaria}", response_model=Secretaria)
def update_secretaria(data_update: SecretariaUpdate, id_facultad:int, id_secretaria: int):
    try:
        with engine.connect() as conn:
            encryp_passw = generate_password_hash(data_update.contrasena, "pbkdf2:sha256:30", 30)

            conn.execute(secretarias.update().values(
                id_facultades = data_update.id_facultades,    
                nombre = data_update.nombre,
                apellido_paterno = data_update.apellido_paterno,
                apellido_materno = data_update.apellido_materno,
                turno = data_update.turno,
                telefono = data_update.telefono,
                matricula = data_update.matricula,
                correo = data_update.correo,
                contrasena = encryp_passw,
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
            encryp_passw = generate_password_hash(data_update.contrasena, "pbkdf2:sha256:30", 30)
            
            conn.execute(secretarias.update().values(
                telefono = data_update.telefono,
                contrasena = encryp_passw,
                direccion = data_update.direccion,
                foto_perfil = data_update.foto_perfil,
            ).where(secretarias.c.id == id_secretaria and secretarias.c.id_facultades == id_facultad ))

            result = conn.execute(secretarias.select().where(secretarias.c.id == id_secretaria and secretarias.c.id_facultades == id_facultad )).first()

        logging.warning(f"Secretaria con el ID: {id_secretaria} de la facultad con ID: {id_facultad} actualizada correctamente")
        return result
    except Exception as exception_error:
        logging.error(f"Error al actualizar la secretaria con el ID: {id_secretaria} de la facultad con ID: {id_facultad} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )


@secretarias_Router.put("/secretaria/perfil/password/{id_facultad}/{id_secretaria}", response_model=Secretaria)
def update_settings_secretaria_password(data_update: SecretariaSettingsUpdatePassword, id_facultad: int, id_secretaria:int):
    try:
        with engine.connect() as conn:
            encryp_passw = generate_password_hash(data_update.contrasena, "pbkdf2:sha256:30", 30)
            
            conn.execute(secretarias.update().values(
                contrasena = encryp_passw,
            ).where(secretarias.c.id == id_secretaria and secretarias.c.id_facultades == id_facultad ))

            result = conn.execute(secretarias.select().where(secretarias.c.id == id_secretaria and secretarias.c.id_facultades == id_facultad )).first()

        logging.warning(f"Secretaria con el ID: {id_secretaria} de la facultad con ID: {id_facultad} actualizada correctamente")
        return result
    except Exception as exception_error:
        logging.error(f"Error al actualizar la secretaria con el ID: {id_secretaria} de la facultad con ID: {id_facultad} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )

@secretarias_Router.put("/secretaria/perfil/picture/{id_facultad}/{id_secretaria}", response_model=Secretaria)
def update_settings_secretaria_user_picture(data_update: SecretariaSettingsUpdateUserPicture, id_facultad: int, id_secretaria:int):
    try:
        with engine.connect() as conn:
    
            conn.execute(secretarias.update().values(
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