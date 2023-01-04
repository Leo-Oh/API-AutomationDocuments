from distutils.log import error
from xmlrpc.client import SERVER_ERROR
from fastapi import APIRouter, Response, Header
from fastapi.responses import JSONResponse 
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT,HTTP_401_UNAUTHORIZED
from typing import List
import json
from schema.Estudiante import Estudiante, EstudianteAuth, EstudianteSettings, EstudianteUpdate
from db.db import engine
from model.Estudiante import estudiantes
import logging
from modules.login_uv import get_user_uv
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List
from functions_jwt import write_token, validate_token




estudiantes_Router = APIRouter()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(message)s', filename = "log/registro.log", filemode = 'w',)

@estudiantes_Router.get("/estudiantes", response_model=List[Estudiante])
def get_estudiantes():
    try:
        with engine.connect() as conn:
            result = conn.execute(estudiantes.select()).fetchall()
        if(result):
            logging.info(f"Se obtuvo información de todos los estudiantes")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    
    except Exception as exception_error:
        logging.error(f"Error al obtener información de los estudiantes ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )
   
@estudiantes_Router.get("/estudiante/estudiante/{id_estudiante}", response_model=Estudiante)
def get_estudiante_by_id_estudiante(id_estudiante: int):
    try:
        with engine.connect() as conn:
            result = conn.execute(estudiantes.select().where(estudiantes.c.id == id_estudiante)).first()
        if(result):
            logging.info(f"Se obtuvo información del estudiante con el ID: {id_estudiante}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información del estudiante con el ID : {id_estudiante} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )


@estudiantes_Router.get("/estudiante/carrera/{id_carrera}", response_model=List[Estudiante])
def get_estudiante_by_id_carrera(id_carrera: int ):
    try:
        with engine.connect() as conn:
            result = conn.execute(estudiantes.select().where(estudiantes.c.id_carreras == id_carrera)).fetchall()
        if(result):
            logging.info(f"Se obtuvo información de los esudiantes que pertencen a la carrera  con el ID: {id_carrera} ")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información de los estudiantes que pertenecen a la carrera con el ID : {id_carrera} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )

@estudiantes_Router.get("/estudiante/facultad/{id_facultad}", response_model=List[Estudiante])
def get_estudiante_by_id_facultad(id_facultad: int ):
    try:
        with engine.connect() as conn:
            result = conn.execute(estudiantes.select().where(estudiantes.c.id_facultades == id_facultad)).fetchall()
        if(result):
            logging.info(f"Se obtuvo información de los esudiantes que pertencen a la carrera  con el ID: {id_facultad} ")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información de los estudiantes que pertenecen a la carrera con el ID : {id_facultad} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )

@estudiantes_Router.get("/estudiante/carrera-estudiante/{id_facultad}/{id_carrera}/{id_estudiante}", response_model=Estudiante)
def get_estudiante_by_id_carrera_and_by_id_estudiante(id_facultad:int, id_carrera: int, id_estudiante: int ):
    try:
        with engine.connect() as conn:
            #result = conn.execute(estudiantes.select().where(estudiantes.c.id == id_estudiante and estudiantes.c.id_carreras == id_carrera)).first()
            sql_query = text(f'SELECT * FROM estudiantes WHERE id= {id_estudiante} AND id_facultades={id_facultad} AND id_carreras = {id_carrera}')
            result = conn.execute(sql_query).first()
        if(result):
            logging.info(f"Se obtuvo información del esudiante con el ID: {id_estudiante} de la carrera con el ID: {id_carrera}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información del estudiante con el ID : {id_estudiante} de la carrera con el ID: {id_carrera} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )


@estudiantes_Router.post("/estudiante", status_code=HTTP_201_CREATED)
def create_estudiante(data_estudiante: Estudiante):
    try:
        with engine.connect() as conn:
            result = conn.execute(estudiantes.select().where(estudiantes.c.correo == data_estudiante.correo or estudiantes.c.matricula == data_estudiante.matricula)).first()    
            
            if result != None:
                return Response(status_code=HTTP_401_UNAUTHORIZED)
   
            new_estudiante = data_estudiante.dict()
            new_estudiante["contrasena"] = generate_password_hash(data_estudiante.contrasena, "pbkdf2:sha256:30", 30)
            
            conn.execute(estudiantes.insert().values(new_estudiante))
        logging.info(f"Estudiante {data_estudiante.nombre_completo} creado correctamente")
        return Response(status_code=HTTP_201_CREATED)
    except Exception as exception_error:
        logging.error(f"Error al crear el estudiante {data_estudiante.nombre_completo} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )


@estudiantes_Router.post("/estudiante/ingresar")
def estudiantes_ingresar_al_sistema(estudiantes_auth : EstudianteAuth):
    with engine.connect() as conn:
        if(estudiantes_auth.correo != None):
            result = conn.execute(estudiantes.select().where(estudiantes.c.correo == estudiantes_auth.correo )).first()
        if(estudiantes_auth.matricula != None):
            result = conn.execute(estudiantes.select().where(estudiantes.c.matricula == estudiantes_auth.matricula )).first()

        if result != None:
            print(result)
            check_passw = check_password_hash(result[6], estudiantes_auth.contrasena)
            if check_passw:
                return {
                "status": 200,
                "message": "Access success",
                "token" : write_token(estudiantes_auth.dict()),
                "user" : result
                }
            else:
                return Response(status_code=HTTP_401_UNAUTHORIZED)
        
        
        if(result == None):
            if(estudiantes_auth.matricula != None):
                student_by_miuv = get_user_uv(user=estudiantes_auth.matricula,password=estudiantes_auth.contrasena)
                if(student_by_miuv["nombre"]):
                    with engine.connect() as conn:
                        sql_query_facultad = text(f'SELECT * FROM facultades WHERE nombre LIKE "{student_by_miuv["facultad"]}" ')
                        result_id_facultad = conn.execute(sql_query_facultad).first()
                        
                        sql_query_carrera = text(f'SELECT * FROM carreras WHERE nombre LIKE "{student_by_miuv["programa"]}" ')
                        result_id_carrera = conn.execute(sql_query_carrera).first()
                        
                        new_estudiante = Estudiante
                        new_estudiante.id_carreras = int(result_id_carrera[0])
                        new_estudiante.id_facultades = int(result_id_facultad[0])
                        new_estudiante.nombre_completo =  student_by_miuv["nombre"]
                        new_estudiante.telefono =  student_by_miuv["telefono"]
                        new_estudiante.foto_perfil =  student_by_miuv["foto_perfil"]
                        new_estudiante.correo =  student_by_miuv["correo"]
                        new_estudiante.semestre = int(student_by_miuv["periodo_actual"])
                        new_estudiante.matricula =  estudiantes_auth.matricula
                        new_estudiante.contrasena = generate_password_hash(estudiantes_auth.contrasena, "pbkdf2:sha256:30", 30)
                        
                     
                        #result_create = conn.execute(estudiantes.insert().values(new_estudiante))
                        
                        result_create = conn.execute(estudiantes.insert().values(                
                            id_carreras = int(result_id_carrera[0]),
                            id_facultades = int(result_id_facultad[0]),
                            nombre_completo = student_by_miuv["nombre"],
                            matricula = estudiantes_auth.matricula,
                            correo = student_by_miuv["correo"],
                            contrasena = generate_password_hash(estudiantes_auth.contrasena, "pbkdf2:sha256:30", 30),
                            semestre =  int(student_by_miuv["periodo_actual"]),
                            telefono = student_by_miuv["telefono"],
                            foto_perfil = student_by_miuv["foto_perfil"],
                        ))
                        
                        
                        logging.info(f"Estudiante {new_estudiante.nombre_completo} creado correctamente")
                        if result_create:
                            return {
                                "status": 200,
                                "message": "Access success",
                                "token" : write_token(estudiantes_auth.dict()),
                                "user" : result
                                }
                        else:
                            return {
                                "status": 404,
                                "message": "User not found",
                                }
                            
        else:
            return JSONResponse(content={"message": "User not found"}, status_code=404)

@estudiantes_Router.post("/estudiante/verify/token")
def estudiantes_verificar_token(token_estudiante:str=Header(default=None)):
  #token = user_token.split(' ')[1]
  token=token_estudiante.split(" ")[0]
  return validate_token(token_estudiante, output=True)


@estudiantes_Router.put("/estudiante/{id_estudiante}", response_model=Estudiante)
def update_estudiante(data_update: EstudianteUpdate,id_estudiante:int):
    try:
        with engine.connect() as conn:
            encryp_passw = generate_password_hash(data_update.contrasena, "pbkdf2:sha256:30", 30)

            conn.execute(estudiantes.update().values(                
                id_carreras = data_update.id_carreras,
                id_facultades = data_update.id_facultades,
                nombre_completo = data_update.nombre_completo,
                matricula = data_update.matricula,
                correo = data_update.correo,
                contrasena = encryp_passw,
                semestre = data_update.semestre,
                telefono = data_update.telefono,
                foto_perfil = data_update.foto_perfil,
            ).where(estudiantes.c.id == id_estudiante ))

            result = conn.execute(estudiantes.select().where(estudiantes.c.id == id_estudiante )).first()
        logging.warning(f"Estudiante con el ID: {id_estudiante} actualizado correctamente")
        return result
    except Exception as exception_error:
        logging.error(f"Error al actualizar el estudiante con el ID: {id_estudiante} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )


@estudiantes_Router.put("/estudiante/{id_facultad}/{id_carrera}/{id_estudiante}", response_model=Estudiante)
def update_estudiante(data_update: EstudianteUpdate,id_facultad: int, id_carrera: int, id_estudiante:int):
    try:
        with engine.connect() as conn:
            encryp_passw = generate_password_hash(data_update.contrasena, "pbkdf2:sha256:30", 30)

            conn.execute(estudiantes.update().values(                
                id_carreras = data_update.id_carreras,
                id_facultades = data_update.id_facultades,
                nombre_completo = data_update.nombre_completo,
                #nombre = data_update.nombre,
                #apellido_paterno = data_update.apellido_paterno,
                #apellido_materno = data_update.apellido_materno,
                matricula = data_update.matricula,
                correo = data_update.correo,
                contrasena = encryp_passw,
                semestre = data_update.semestre,
                telefono = data_update.telefono,
                foto_perfil = data_update.foto_perfil,
            ).where(estudiantes.c.id == id_estudiante and estudiantes.c.id_facultad == id_facultad and estudiantes.c.id_carreras == id_carrera ))

            result = conn.execute(estudiantes.select().where(estudiantes.c.id == id_estudiante  and estudiantes.c.id_facultad == id_facultad  and estudiantes.c.id_carreras == id_carrera )).first()
        logging.warning(f"Estudiante {data_update.nombre_completo} actualizada correctamente")
        return result
    except Exception as exception_error:
        logging.error(f"Error al actualizar el estudiante {data_update.nombre_completo} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )



@estudiantes_Router.put("/estudiante/perfil/{id_facultad}/{id_carrera}/{id_estudiante}", response_model=Estudiante)
def update_settings_estudiante(data_update: EstudianteSettings,id_facultad: int, id_carrera: int, id_estudiante:int):
    try:
        with engine.connect() as conn:
            encryp_passw = generate_password_hash(data_update.contrasena, "pbkdf2:sha256:30", 30)

            conn.execute(estudiantes.update().values(
                telefono = data_update.telefono,
                contrasena = encryp_passw,
                foto_perfil = data_update.foto_perfil,
            ).where(estudiantes.c.id == id_estudiante and estudiantes.c.id_facultades ==id_facultad and estudiantes.c.id_carreras ==id_carrera ))

            result = conn.execute(estudiantes.select().where(estudiantes.c.id == id_estudiante and estudiantes.c.id_facultades ==id_facultad and estudiantes.c.id_carreras == id_carrera )).first()

        logging.warning(f"Estudiante con el ID: {id_estudiante} de la  facultad {id_facultad} y la carrera con ID: {id_carrera} actualizada correctamente")
        return result
    except Exception as exception_error:
        logging.error(f"Error al actualizar el estudiante con el ID: {id_estudiante} de la  facultad {id_facultad} y la carrera con ID: {id_carrera} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )


@estudiantes_Router.delete("/estudiante/{id_facultad}/{id_carrera}/{id_estudiante}", status_code=HTTP_204_NO_CONTENT)
def delete_estudiante(id_facultad:int, id_carrera:int, id_estudiante:int, ):
    try:
        with engine.connect() as conn:
            conn.execute(estudiantes.delete().where(estudiantes.c.id == id_estudiante and estudiantes.c.id_facultades == id_facultad and estudiantes.c.id_carreras == id_carrera ))
        logging.critical(f"Estudiante con el ID {id_estudiante} de la  facultad {id_facultad} y la  carrera con el ID: {id_carrera} eliminada correctamente")
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al eliminar al estudiante con el ID {id_estudiante}  de la  facultad {id_facultad} y la carrera {id_carrera} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )


@estudiantes_Router.delete("/estudiante/{id_estudiante}", status_code=HTTP_204_NO_CONTENT)
def delete_estudiante_by_id(id_estudiante:int, ):
    try:
        with engine.connect() as conn:
            conn.execute(estudiantes.delete().where(estudiantes.c.id == id_estudiante ))
        logging.critical(f"Estudiante con el ID {id_estudiante} eliminado correctamente")
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        return Response(status_code= SERVER_ERROR )