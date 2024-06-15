from distutils.log import error
from xmlrpc.client import SERVER_ERROR
from fastapi import APIRouter, Response, Header
from fastapi.responses import JSONResponse 
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from typing import List

from schema.SolicitudTramite import SolicitudTramite,SolicitudTramite_update_by_secretaria, SolicitudTramiteAllField
from db.db import engine
from model.SolicitudTramite import solicitudes_de_tramites
import logging
import os
from sqlalchemy.sql import text

solicitud_de_tramites_Router = APIRouter()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(message)s', filename = "log/registro.log", filemode = 'w',)


@solicitud_de_tramites_Router.get("/solicitud-de-tramite/informacion-completa")
def get_solicitud_de_tramite_all_data():
    try:
        with engine.connect() as conn:
            sql_query = text("""
                SELECT 
                        solicitdes_de_tramites.id AS id,
                        solicitdes_de_tramites.id_tramites AS tramites_id,
                        solicitdes_de_tramites.id_secretarias AS secretarias_id,
                        solicitdes_de_tramites.id_estudiantes AS estudiantes_id,
                        solicitdes_de_tramites.datos_adjuntos_estudiante AS solicitdes_de_tramites_datos_adjuntos_estudiante, 
                        solicitdes_de_tramites.fecha_de_solicitud AS solicitdes_de_tramites_fecha_de_solicitud,
                        solicitdes_de_tramites.estado solicitdes_de_tramites_estado,
                        
                        estudiantes.id AS estudiantes_id,
                        estudiantes.nombre_completo AS estudiantes_nombre_completo,
                        estudiantes.matricula AS estudiantes_matricula,
                        estudiantes.correo AS estudiantes_correo,
                        estudiantes.semestre AS estudiantes_semestre,
                        estudiantes.telefono AS estudiantes_telefono,
                        estudiantes.foto_perfil AS estudiantes_foto_perfil,
                        
                        tramites.id AS tramites_id,
                        tramites.nombre AS tramites_nombre,
                        tramites.descripcion AS tramites_descripcion,
                        
                        secretarias.id AS secretarias_id,
                        secretarias.nombre AS secretarias_nombre,
                        secretarias.apellido_paterno AS secretarias_apellido_paterno,
                        secretarias.apellido_materno AS secretarias_apellido_materno,
                        secretarias.turno AS secretarias_turno,
                        secretarias.correo AS secretarias_correo,
                        
                        carreras.id AS carreras_id,
                        carreras.nombre AS carreras_nombre,
                    
                        facultades.id AS facultades_id,
                        facultades.id_regiones AS facultades_id_regiones,
                        facultades.nombre AS facultades_nombre,
                        facultades.direccion AS facultades_direccion,
                        facultades.telefono AS facultades_telefono,
                        
                        
                        regiones.id AS regiones_id,
                        regiones.nombre AS regiones_nombre
                        
                    FROM solicitdes_de_tramites 
                    INNER JOIN estudiantes ON solicitdes_de_tramites.id_estudiantes = estudiantes.id
                    INNER JOIN tramites ON solicitdes_de_tramites.id_tramites = tramites.id
                    INNER JOIN secretarias ON solicitdes_de_tramites.id_secretarias = secretarias.id
                    INNER JOIN carreras ON estudiantes.id_carreras = carreras.id
                    INNER JOIN facultades ON estudiantes.id_facultades = facultades.id
                    INNER JOIN regiones ON facultades.id_regiones = regiones.id;
                """)
            

            
            result = conn.execute(sql_query).fetchall()
            
            if result:
                logging.info("Se obtuvo información completa de todas las solicitudes de tramites y su información completa")
                return [dict(row) for row in result]

                
            else:
                logging.warning("No se encontró información")
                return Response(status_code=HTTP_204_NO_CONTENT)
    
    except Exception as exception_error:
        logging.error(f"Error al obtener informacion completa de todas las solicitudes de tramites: {exception_error}", exc_info=True)
        return Response(status_code= SERVER_ERROR )





@solicitud_de_tramites_Router.get("/solicitud-de-tramite-secretarias")
def get_solicitud_de_tramite_secretarias():
    try:
        with engine.connect() as conn:
            
            
            sql_query = text(f"""
    SELECT 
        solicitdes_de_tramites.id AS id,
        solicitdes_de_tramites.id_tramites AS tramites_id,
        solicitdes_de_tramites.id_secretarias AS secretarias_id,
        solicitdes_de_tramites.id_estudiantes AS estudiantes_id,
        solicitdes_de_tramites.datos_adjuntos_estudiante, 
        solicitdes_de_tramites.fecha_de_solicitud,
        solicitdes_de_tramites.estado,
        estudiantes.id AS estudiantes_id,
        estudiantes.nombre_completo AS estudiantes_nombre_completo,
        estudiantes.matricula AS estudiantes_matricula,
        estudiantes.correo AS estudiantes_correo,
        estudiantes.semestre AS estudiantes_semestre,
        estudiantes.telefono AS estudiantes_telefono,
        estudiantes.foto_perfil AS estudiantes_foto_perfil,
        tramites.id AS tramites_id,
        tramites.nombre AS tramites_nombre,
        tramites.descripcion AS tramites_descripcion,
        secretarias.id AS secretarias_id,
        secretarias.nombre AS secretarias_nombre,
        secretarias.apellido_paterno AS secretarias_apellido_paterno,
        secretarias.apellido_materno AS secretarias_apellido_materno,
        secretarias.turno AS secretarias_turno,
        secretarias.correo AS secretarias_correo
    FROM solicitdes_de_tramites
    INNER JOIN estudiantes ON solicitdes_de_tramites.id_estudiantes = estudiantes.id
    INNER JOIN tramites ON solicitdes_de_tramites.id_tramites = tramites.id
    INNER JOIN secretarias ON solicitdes_de_tramites.id_secretarias = secretarias.id
""")

            result = conn.execute(sql_query).fetchall()
        
            
    
        if(result):
            logging.info(f"Se obtuvo información de todos los tramites")
            
            formatted_results = []
            for row in result:
                formatted_row = {
                    "solicitud_de_tramites": {
                        "id": row["id"],
                        "id_tramites": row["tramites_id"],
                        "id_secretarias": row["secretarias_id"],
                        "id_estudiantes": row["estudiantes_id"],
                        "datos_adjuntos_estudiante": row["datos_adjuntos_estudiante"],
                        "fecha_de_solicitud": row["fecha_de_solicitud"],
                        "estado": row["estado"]
                    },
                    "estudiantes": {
                        "id": row["estudiantes_id"],
                        "nombre_completo": row["estudiantes_nombre_completo"],
                        "matricula": row["estudiantes_matricula"],
                        "correo": row["estudiantes_correo"],
                        "semestre": row["estudiantes_semestre"],
                        "telefono": row["estudiantes_telefono"],
                        "foto_perfil": row["estudiantes_foto_perfil"]
                    },
                    "tramites": {
                        "id": row["tramites_id"],
                        "nombre": row["tramites_nombre"],
                        "descripcion": row["tramites_descripcion"]
                    },
                    "secretarias": {
                        "id": row["secretarias_id"],
                        "nombre": row["secretarias_nombre"],
                        "apellido_paterno": row["secretarias_apellido_paterno"],
                        "apellido_materno": row["secretarias_apellido_materno"],
                        "turno": row["secretarias_turno"],
                        "correo": row["secretarias_correo"]
                    }
                }
                formatted_results.append(formatted_row)
        
            return formatted_results
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    
    except Exception as exception_error:
        logging.error(f"Error al obtener información de las solicitudes de tramites ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )


@solicitud_de_tramites_Router.get("/solicitud-de-tramite-secretarias/{id_secretaria}")
def get_solicitud_de_tramite_secretarias_id(id_secretaria:int):
    try:
        with engine.connect() as conn:
    
            sql_query = text(f"""
    SELECT 
        solicitdes_de_tramites.id AS id,
        solicitdes_de_tramites.id_tramites AS tramites_id,
        solicitdes_de_tramites.id_secretarias AS secretarias_id,
        solicitdes_de_tramites.id_estudiantes AS estudiantes_id,
        solicitdes_de_tramites.datos_adjuntos_estudiante, 
        solicitdes_de_tramites.fecha_de_solicitud,
        solicitdes_de_tramites.estado,
        estudiantes.id AS estudiantes_id,
        estudiantes.nombre_completo AS estudiantes_nombre_completo,
        estudiantes.matricula AS estudiantes_matricula,
        estudiantes.correo AS estudiantes_correo,
        estudiantes.semestre AS estudiantes_semestre,
        estudiantes.telefono AS estudiantes_telefono,
        estudiantes.foto_perfil AS estudiantes_foto_perfil,
        tramites.id AS tramites_id,
        tramites.nombre AS tramites_nombre,
        tramites.descripcion AS tramites_descripcion,
        secretarias.id AS secretarias_id,
        secretarias.nombre AS secretarias_nombre,
        secretarias.apellido_paterno AS secretarias_apellido_paterno,
        secretarias.apellido_materno AS secretarias_apellido_materno,
        secretarias.turno AS secretarias_turno,
        secretarias.correo AS secretarias_correo
    FROM solicitdes_de_tramites 
    INNER JOIN estudiantes ON solicitdes_de_tramites.id_estudiantes = estudiantes.id
    INNER JOIN tramites ON solicitdes_de_tramites.id_tramites = tramites.id
    INNER JOIN secretarias ON solicitdes_de_tramites.id_secretarias = secretarias.id
    
    WHERE solicitdes_de_tramites.id_secretarias = {id_secretaria}
    
""")

            result = conn.execute(sql_query).fetchall()
        
    
        if(result):
            logging.info(f"Se obtuvo información de todos los tramites")
            
            formatted_results = []
            for row in result:
                formatted_row = {
                    "solicitud_de_tramites": {
                        "id": row["id"],
                        "id_tramites": row["tramites_id"],
                        "id_secretarias": row["secretarias_id"],
                        "id_estudiantes": row["estudiantes_id"],
                        "datos_adjuntos_estudiante": row["datos_adjuntos_estudiante"],
                        "fecha_de_solicitud": row["fecha_de_solicitud"],
                        "estado": row["estado"]
                    },
                    "estudiantes": {
                        "id": row["estudiantes_id"],
                        "nombre_completo": row["estudiantes_nombre_completo"],
                        "matricula": row["estudiantes_matricula"],
                        "correo": row["estudiantes_correo"],
                        "semestre": row["estudiantes_semestre"],
                        "telefono": row["estudiantes_telefono"],
                        "foto_perfil": row["estudiantes_foto_perfil"]
                    },
                    "tramites": {
                        "id": row["tramites_id"],
                        "nombre": row["tramites_nombre"],
                        "descripcion": row["tramites_descripcion"]
                    },
                    "secretarias": {
                        "id": row["secretarias_id"],
                        "nombre": row["secretarias_nombre"],
                        "apellido_paterno": row["secretarias_apellido_paterno"],
                        "apellido_materno": row["secretarias_apellido_materno"],
                        "turno": row["secretarias_turno"],
                        "correo": row["secretarias_correo"]
                    }
                }
                formatted_results.append(formatted_row)
        

            return formatted_results
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    
    except Exception as exception_error:
        logging.error(f"Error al obtener información de las solicitudes de tramites ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )

@solicitud_de_tramites_Router.get("/solicitud-de-tramite", response_model=List[SolicitudTramiteAllField])
def get_solicitud_de_tramite():
    try:
        with engine.connect() as conn:
            result = conn.execute(solicitudes_de_tramites.select()).fetchall()
            
         
        if(result):
            logging.info(f"Se obtuvo información de todos los tramites")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    
    except Exception as exception_error:
        logging.error(f"Error al obtener información de las solicitudes de tramites ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )
   

@solicitud_de_tramites_Router.get("/solicitud-de-tramite/id/{id_solicitud_de_tramite}", response_model=List[SolicitudTramiteAllField])
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


@solicitud_de_tramites_Router.get("/solicitud-de-tramite/secretaria/{id_secretaria}", response_model=List[SolicitudTramiteAllField])
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

@solicitud_de_tramites_Router.get("/solicitud-de-tramite/tramite/{id_tramite}", response_model=List[SolicitudTramiteAllField])
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


@solicitud_de_tramites_Router.get("/solicitud-de-tramite/carrera/{id_carrera}", response_model=List[SolicitudTramiteAllField])
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

@solicitud_de_tramites_Router.get("/solicitud-de-tramite/estudiante/{id_estudiante}", response_model=List[SolicitudTramiteAllField])
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

@solicitud_de_tramites_Router.get("/solicitud-de-tramite/secretaria/{id_secretaria}/tramite/{id_tramite}/carrera/{id_carrera}/estudiante/{id_estudiante}", response_model=SolicitudTramite)
def get_solicitudes_de_tramites_all_ids( id_secretaria:int,id_tramite:int, id_carrera:int, id_estudiante: int):
    try:
        with engine.connect() as conn:
            #result = conn.execute(solicitudes_de_tramites.select().where(solicitudes_de_tramites.c.id == id_solicitud_de_tramite and solicitudes_de_tramites.c.id_secretariais == id_secretaria and solicitudes_de_tramites.c.id_tramites == id_tramite and solicitudes_de_tramites.c.id_carreras == id_carrera and solicitudes_de_tramites.c.id_estudiantes == id_estudiante)).fetchall()
            sql_query = text(f'SELECT * FROM solicitdes_de_tramites WHERE id_secretarias = {id_secretaria} AND id_tramites = {id_tramite} AND id_carreras = {id_carrera} AND id_estudiantes = {id_estudiante}')
            result = conn.execute(sql_query).first()
        if(result):
            logging.info(f"Se obtuvo información de las solicitudes de tramites con el ID de la secretaria: {id_secretaria}, tipo de tramite: {id_tramite}, carrera: {id_carrera}, estudiante: {id_estudiante} ")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener nformación de las solicitudes de tramites con el ID de la secretaria: {id_secretaria}, tipo de tramite: {id_tramite}, carrera: {id_carrera}, estudiante: {id_estudiante} ||| {exception_error}") 
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

  
@solicitud_de_tramites_Router.put("/solicitud-de-tramite/{id_solicitud_de_tramite}", response_model=SolicitudTramite_update_by_secretaria)
def update_soliitud_de_tramite(data_update: SolicitudTramite_update_by_secretaria , id_solicitud_de_tramite: int):
    try:
        with engine.connect() as conn:
            conn.execute(solicitudes_de_tramites.update().values(
                datos_adjuntos_secretaria = data_update.datos_adjuntos_secretaria,
                mensaje_secretaria = data_update.mensaje_secretaria,
                estado = data_update.estado,
                fecha_de_aprobacion = data_update.fecha_de_aprobacion,
                url_file = data_update.url_file,
            ).where(solicitudes_de_tramites.c.id == id_solicitud_de_tramite))

            
            result = conn.execute(solicitudes_de_tramites.select().where(solicitudes_de_tramites.c.id == id_solicitud_de_tramite )).first()

        logging.warning(f"Solicitud de tamite con el ID: {id_solicitud_de_tramite} actualizada correctamente")
        return result
    except Exception as exception_error:
        logging.error(f"Error al actualizar la solicitud de tramite con el ID: {id_solicitud_de_tramite} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )
        

@solicitud_de_tramites_Router.delete("/solicitud-de-tramite/{id_solicitud_de_tramite}", status_code=HTTP_204_NO_CONTENT)
def delete_solicitud_de_tramite(id_solicitud_de_tramite:int):
    try:
        with engine.connect() as conn:
            conn.execute(solicitudes_de_tramites.delete().where(solicitudes_de_tramites.c.id == id_solicitud_de_tramite))
        
        logging.critical(f"SolicitudTramite con el ID: {id_solicitud_de_tramite} eliminada correctamente")
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al eliminar la solicitud de tramite con el ID {id_solicitud_de_tramite} ||| {exception_error}")
        return Response(status_code= SERVER_ERROR )