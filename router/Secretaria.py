from os import getcwd, makedirs, path
from pathlib import Path
import pathlib
import uuid
from xmlrpc.client import SERVER_ERROR
from fastapi import APIRouter, File, Response, Header, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from functions_jwt import write_token 
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from typing import List

from schema.Secretaria import Secretaria, Secretaria_With_IdFacultad_IdCarrera_IdTramite, SecretariaAuth, SecretariaSettingsUpdate, SecretariaSettingsUpdatePassword, SecretariaSettingsUpdateUserPicture, SecretariaUpdate
from db.db import engine
from model.Secretaria import secretarias
import logging

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import text

secretarias_Router = APIRouter()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(message)s', filename = "log/registro.log", filemode = 'w',)


@secretarias_Router.get("/secretarias/informacion-completa")
def get_secretarias_full_info():
    try:
        with engine.connect() as conn:

            sql_query = text("""
                SELECT 
                    secretarias.id AS secretarias_id,
                    secretarias.id_facultades AS secretarias_id_facultades,
                    secretarias.nombre AS secretarias_nombre,
                    secretarias.apellido_paterno AS secretarias_apellido_paterno,
                    secretarias.apellido_materno AS secretarias_apellido_materno,
                    secretarias.turno AS secretarias_turno,
                    secretarias.telefono AS secretarias_telefono,
                    secretarias.matricula AS secretarias_matricula,
                    secretarias.direccion AS secretarias_direccion,
                    secretarias.correo AS secretarias_correo,
                    secretarias.foto_perfil AS secretarias_foto_perfil,
                    
                    facultades.id AS facultades_id,
                    facultades.nombre AS facultades_nombre,
                    facultades.direccion AS facultades_direccion,
                    facultades.telefono AS facultades_telefono,
                    facultades.id_regiones as facultades_id_regiones,
                    
                    regiones.nombre as regiones_nombre
                FROM 
                    secretarias
                INNER JOIN 
                    facultades ON secretarias.id_facultades = facultades.id
                INNER JOIN 
                    regiones ON facultades.id_regiones = regiones.id
            """)

            result = conn.execute(sql_query).fetchall()
        print([dict(row) for row in result])
        
        if(result):
            logging.info(f"Se obtuvo informacón completa de todas las secretarias")    
            return [dict(row) for row in result]
                
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    
    except Exception as exception_error:
        logging.error(f"Error al obtener informacion completa de las secretarias ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )


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



@secretarias_Router.get("/secretaria/facultad-carrera-tramite/{id_facultad}/{id_carrera}/{id_tramite}", response_model=List[Secretaria_With_IdFacultad_IdCarrera_IdTramite])
def get_secretaria_by_id_facultad_id_carrera_id_tramite(id_facultad: int, id_carrera: int, id_tramite: int ):
    try:
        with engine.connect() as conn:
    
            sql_query = text(f'select secretarias.id, secretarias.id_facultades, secretarias.nombre,secretarias.apellido_paterno, secretarias.apellido_materno, secretarias.turno,secretarias.correo, secretarias_tramites.id_tramites, secretarias_carreras.id_carreras from secretarias_tramites inner join secretarias_carreras on secretarias_carreras.id_secretarias = secretarias_tramites.id_secretarias inner join secretarias on secretarias.id = secretarias_tramites.id_secretarias where id_facultades = {id_facultad} and id_carreras = {id_carrera} and id_tramites = {id_tramite};')
            result = conn.execute(sql_query).fetchall()
            
        if(result):
            logging.info(f"Se obtuvo información de la secretaria con el ID de la facultad: {id_facultad} , ID carrera: {id_carrera} y ID del tramite que realiza: {id_tramite}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información de la secretaria con el ID de la facultad: {id_facultad} , ID carrera: {id_carrera} y ID del tramite que realiza: {id_tramite}||| {exception_error}") 
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




@secretarias_Router.post("/secretaria/perfil/picture")
async def secretary_profile_upload(file_document: UploadFile = File(...)):

    file_new_name = uuid.uuid4()
    archivo=["jpg","jpeg","png","pdf","doc"]
    
    makedirs('uploads', exist_ok=True)
    makedirs('uploads/secretary', exist_ok=True)
    
    file_name_document = pathlib.Path(file_document.filename)
    
    if file_name_document.suffix[1:] in archivo:
        with open(getcwd() + "/uploads/secretary/" + str(file_new_name) + file_name_document.suffix , "wb") as myfile_document:
            content = await file_document.read()
            myfile_document.write(content)
            myfile_document.close()
                    
        return JSONResponse(content={
                "message": "Files saved",
                "archivo": f"{str(file_new_name) + file_name_document.suffix}",
                }, status_code=200)

    else:
        return JSONResponse(content={
            "message": "File not saved",
            }, status_code=400)


@secretarias_Router.get("/secretaria/perfil/picture")
def get_file( nombre_archivo: str):
    return FileResponse(getcwd() + "/uploads/secretary/"+ nombre_archivo)




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