from distutils.log import error
from xmlrpc.client import SERVER_ERROR
from fastapi import APIRouter, Response, Header
from fastapi.responses import JSONResponse 
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from typing import List

from schema.SolicitudTramite import SolicitudTramite, SolicitudTramite_secretaria
from db.db import engine
from model.SolicitudTramite import solicitudes_de_tramites
import logging


solicitud_de_tramites_Router = APIRouter()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(message)s', filename = "log/registro.log", filemode = 'w',)

@solicitud_de_tramites_Router.get("/solicitud-de-tramite", response_model=List[SolicitudTramite])
def get_solicitud_de_tramite():
    try:
        with engine.connect() as conn:
            result = conn.execute(solicitudes_de_tramites.select()).fetchall()
    
        if(result):
            logging.info(f"Se obtuvo información de todas las carreas")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    
    except Exception as exception_error:
        logging.error(f"Error al obtener información de las solicitudes de tramites ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )
   

@solicitud_de_tramites_Router.get("/solicitud-de-tramite/{id_solicitud_de_tramite}", response_model=List[SolicitudTramite])
def get_solicitud_de_tramites_by_id(id_solicitud_de_tramite: int):
    try:
        with engine.connect() as conn:
            result = conn.execute(solicitudes_de_tramites.select().where(solicitudes_de_tramites.c.id == id_solicitud_de_tramite )).fetchall()
        if(result):
            logging.info(f"Se obtuvo información de la solicitud del tramite con el ID: {id_solicitud_de_tramite}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información de la solicitud de tramite con el ID: {id_solicitud_de_tramite} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )


@solicitud_de_tramites_Router.get("/solicitud-de-tramite/{id_secretaria}", response_model=List[SolicitudTramite])
def get_solicitudes_de_tramites_by_id_secretarias(id_secretaria: int):
    try:
        with engine.connect() as conn:
            result = conn.execute(solicitudes_de_tramites.select().where(solicitudes_de_tramites.c.id_secretarias == id_secretaria )).fetchall()
        if(result):
            logging.info(f"Se obtuvo información de las solicitudes del tramite con el ID de la secretaria: {id_secretaria}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información de las solicitudes de tramite con el ID de la secretaria: {id_secretaria} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )

@solicitud_de_tramites_Router.get("/solicitud-de-tramite/{id_tramite}", response_model=List[SolicitudTramite])
def get_solicitudes_de_tramites_by_id_tramite(id_tramite: int):
    try:
        with engine.connect() as conn:
            result = conn.execute(solicitudes_de_tramites.select().where(solicitudes_de_tramites.c.id_tramites == id_tramite )).fetchall()
        if(result):
            logging.info(f"Se obtuvo información de las solicitudes del tramites con el ID del tipo de tramite: {id_tramite}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información de las solicitudes de tramite con el ID del tramite: {id_tramite} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )


@solicitud_de_tramites_Router.get("/solicitud-de-tramite/{id_carrera}", response_model=List[SolicitudTramite])
def get_solicitudes_de_tramites_by_id_carrera(id_carrera: int):
    try:
        with engine.connect() as conn:
            result = conn.execute(solicitudes_de_tramites.select().where(solicitudes_de_tramites.c.id_carreras == id_carrera )).fetchall()
        if(result):
            logging.info(f"Se obtuvo información de las solicitudes de tramites con el ID de la carrera: {id_carrera}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información de las solicitudes de tramites con el ID de la carrera: {id_carrera} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )

@solicitud_de_tramites_Router.get("/solicitud-de-tramite/{id_estudiante}", response_model=List[SolicitudTramite])
def get_solicitudes_de_tramites_by_id_estudiante(id_estudiante: int):
    try:
        with engine.connect() as conn:
            result = conn.execute(solicitudes_de_tramites.select().where(solicitudes_de_tramites.c.id_estudiantes == id_estudiante )).fetchall()
        if(result):
            logging.info(f"Se obtuvo información de las solicitudes de tramites con el ID de la carrera: {id_estudiante}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información de las solicitudes de tramites con el ID de la carrera: {id_estudiante} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )

@solicitud_de_tramites_Router.get("/solicitud-de-tramite/{id_solicitud_de_tramite}/{id_secretaria}/{id_tramite}/{id_carrera}/{id_estudiante}", response_model=List[SolicitudTramite])
def get_solicitudes_de_tramites_all_ids(id_solicitud_de_tramite:int, id_secretaria:int,id_tramite:int, id_carrera:int, id_estudiante: int):
    try:
        with engine.connect() as conn:
            result = conn.execute(solicitudes_de_tramites.select().where(solicitudes_de_tramites.c.id == id_solicitud_de_tramite and solicitudes_de_tramites.c.id_secretariais == id_secretaria and solicitudes_de_tramites.c.id_tramites == id_tramite and solicitudes_de_tramites.c.id_carreras == id_carrera and solicitudes_de_tramites.c.id_estudiantes == id_estudiante)).fetchall()
        if(result):
            logging.info(f"Se obtuvo información de las solicitudes de tramites con el ID's de; solicitud de tramite: {id_solicitud_de_tramite}, secretaria: {id_secretaria}, tipo de tramite: {id_tramite}, carrera: {id_carrera}, estudiante: {id_estudiante} ")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener nformación de las solicitudes de tramites con el ID's de; solicitud de tramite: {id_solicitud_de_tramite}, secretaria: {id_secretaria}, tipo de tramite: {id_tramite}, carrera: {id_carrera}, estudiante: {id_estudiante} ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )

@solicitud_de_tramites_Router.post("/solicitud-de-tramite", status_code=HTTP_201_CREATED)
def create_solicitud_de_tramite(data_solicitud_de_tramite: SolicitudTramite):
    try:
        with engine.connect() as conn:    
            new_solicitud = data_solicitud_de_tramite.dict()
            conn.execute(solicitudes_de_tramites.insert().values(new_solicitud))
        logging.info(f"SolicitudTramite  con el ID: {data_solicitud_de_tramite.id} creada correctamente")
        return Response(status_code=HTTP_201_CREATED)
    except Exception as exception_error:
        logging.error(f"Error al crear la solicitud con el ID: {data_solicitud_de_tramite.id} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )

  
@solicitud_de_tramites_Router.put("/solicitud-de-tramite/{id_solicitud_de_tamite}", response_model=SolicitudTramite_secretaria)
def update_soliitud_de_tramite(data_update: SolicitudTramite_secretaria , id_solicitud_de_tramite: int):
    try:
        with engine.connect() as conn:
            conn.execute(solicitudes_de_tramites.update().values(
                datos_adjuntos_secretaria = data_update.datos_adjuntos_secretaria,
                mensaje_secretaria = data_update.mensaje_secretaria,
                estado = data_update.estado,
                fecha_de_aprobacion = data_update.fecha_de_aprobacion,
            ).where(solicitudes_de_tramites.c.id == id_solicitud_de_tramite))

            result = conn.execute(solicitudes_de_tramites.select().where(solicitudes_de_tramites.c.id == id_solicitud_de_tramite )).first()

        logging.warning(f"Solicitud de tamite con el ID: {data_update.id} actualizada correctamente")
        return result
    except Exception as exception_error:
        logging.error(f"Error al actualizar la solicitud de tramite con el ID: {data_update.id} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )
        

@solicitud_de_tramites_Router.delete("/carrera/{id_solicitud_de_tramite}", status_code=HTTP_204_NO_CONTENT)
def delete_carrera(id_solicitud_de_tramite:int):
    try:
        with engine.connect() as conn:
            conn.execute(solicitudes_de_tramites.delete().where(solicitudes_de_tramites.c.id == id_solicitud_de_tramite))
        
        logging.critical(f"SolicitudTramite con el ID: {id_solicitud_de_tramite} eliminada correctamente")
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al eliminar la solicitud de tramite con el ID {id_solicitud_de_tramite} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )