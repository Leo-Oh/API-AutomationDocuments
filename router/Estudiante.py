from distutils.log import error
from xmlrpc.client import SERVER_ERROR
from fastapi import APIRouter, Response, Header
from fastapi.responses import JSONResponse 
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from typing import List

from schema.Estudiante import Estudiante, EstudianteSettings, EstudianteUpdate
from db.db import engine
from model.Estudiante import estudiantes
import logging


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
   
@estudiantes_Router.get("/estudiante/{id_estudiante}", response_model=Estudiante)
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


@estudiantes_Router.get("/estudiante/{id_carrera}", response_model=List[Estudiante])
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


@estudiantes_Router.get("/estudiante/{id_carrera}/{id_estudiante}", response_model=Estudiante)
def get_estudiante_by_id_carrera_and_by_id_estudiante(id_carrera: int, id_estudiante: int ):
    try:
        with engine.connect() as conn:
            result = conn.execute(estudiantes.select().where(estudiantes.c.id == id_estudiante and estudiantes.c.id_carreras == id_carrera)).first()
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
            new_estudiante = data_estudiante.dict()
            conn.execute(estudiantes.insert().values(new_estudiante))
        logging.info(f"Estudiante {data_estudiante.nombre} creado correctamente")
        return Response(status_code=HTTP_201_CREATED)
    except Exception as exception_error:
        logging.error(f"Error al crear el estudiante {data_estudiante.nombre} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )

  
@estudiantes_Router.put("/estudiante/{id_carrera}/{id_estudiante}", response_model=Estudiante)
def update_estudiante(data_update: EstudianteUpdate, id_carrera: int, id_estudiante:int):
    try:
        with engine.connect() as conn:
            conn.execute(estudiantes.update().values(                
                id_carreras = data_update.id_carreras,
                nombre = data_update.nombre,
                apellido_paterno = data_update.apellido_paterno,
                apellido_materno = data_update.apellido_materno,
                contrasena = data_update.contrasena,
                semestre = data_update.semestre,
                telefono = data_update.telefono,
                foto_perfil = data_update.foto_perfil,
            ).where(estudiantes.c.id == id_estudiante and estudiantes.c.id_carreras == id_carrera ))

            result = conn.execute(estudiantes.select().where(estudiantes.c.id == id_estudiante and estudiantes.c.id_carreras == id_carrera )).first()
        logging.warning(f"Estudiante {data_update.nombre} actualizada correctamente")
        return result
    except Exception as exception_error:
        logging.error(f"Error al actualizar el estudiante {data_update.nombre} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )



@estudiantes_Router.put("/estudiante/perfil/{id_carrera}/{id_estudiante}", response_model=Estudiante)
def update_settings_estudiante(data_update: EstudianteSettings, id_carrera: int, id_estudiante:int):
    try:
        with engine.connect() as conn:
            conn.execute(estudiantes.update().values(
                telefono = data_update.telefono,
                contrasena = data_update.contrasena,
                foto_perfil = data_update.foto_perfil,
            ).where(estudiantes.c.id == id_estudiante and estudiantes.c.id_carreras ==id_carrera ))

            result = conn.execute(estudiantes.select().where(estudiantes.c.id == id_estudiante and estudiantes.c.id_carreras == id_carrera )).first()

        logging.warning(f"Estudiante con el ID: {id_estudiante} de la carrera con ID: {id_carrera} actualizada correctamente")
        return result
    except Exception as exception_error:
        logging.error(f"Error al actualizar el estudiante con el ID: {id_estudiante} de la carrera con ID: {id_carrera} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )


@estudiantes_Router.delete("/estudiante/{id_carrera}/{id_estudiante}", status_code=HTTP_204_NO_CONTENT)
def delete_estudiante(id_carrera:int, id_estudiante:int, ):
    try:
        with engine.connect() as conn:
            conn.execute(estudiantes.delete().where(estudiantes.c.id == id_estudiante and estudiantes.c.id_carreras == id_carrera ))
        logging.critical(f"Estudiante con el ID {id_estudiante} de la carrera con el ID: {id_carrera} eliminada correctamente")
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al eliminar al estudiante con el ID {id_estudiante} de la carrera {id_carrera} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )