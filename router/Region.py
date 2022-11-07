from distutils.log import error
from xmlrpc.client import SERVER_ERROR
from fastapi import APIRouter, Response, Header
from fastapi.responses import JSONResponse 
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED

from typing import List

from schema.Region import Region, RegionUpdate
from db.db import engine
from model.Region import regiones
import logging


regionRouter = APIRouter()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(message)s', filename = "log/Registro.log", filemode = 'w',)

@regionRouter.get("/regiones", response_model=List[Region])
def get_regiones():
    try:
        with engine.connect() as conn:
            result = conn.execute(regiones.select()).fetchall()
    
        if(result):
            logging.info(f"Se obtuvo información de todas las dacultades")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    
    except Exception as exception_error:
        logging.error(f"Error al obtener información de las facultades: {exception_error}") 
        return Response(status_code= SERVER_ERROR )
   


@regionRouter.get("/region/{region_id}", response_model=Region)
def get_region(region_id: int):
    try:
        with engine.connect() as conn:
            result = conn.execute(regiones.select().where(regiones.c.id == region_id)).first()
        
        if(result):
            logging.info(f"Se obtuvo información de la region con el ID: {region_id}")
            return result
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información de la region con ID = {region_id}: {exception_error}") 
        return Response(status_code= SERVER_ERROR )



@regionRouter.post("/region", status_code=HTTP_201_CREATED)
def create_region(data_region: Region):
    try:
        with engine.connect() as conn:    
            new_region = data_region.dict()
            conn.execute(regiones.insert().values(new_region))
        
        logging.info(f"Region {new_region.nombre} creada correctamente")
        return Response(status_code=HTTP_201_CREATED)
    except Exception as exception_error:
        logging.error(f"Error al crear la region {data_region.nombre}: {exception_error}")
        return Response(status_code= SERVER_ERROR )

  
@regionRouter.put("/region/{region_id}", response_model=RegionUpdate)
def update_facultad(data_update: RegionUpdate, region_id: int):
    try:
        with engine.connect() as conn:
            conn.execute(regiones.update().values(
                nombre = data_update.nombre,
            ).where(regiones.c.id == region_id))

            result = conn.execute(regiones.select().where(regiones.c.id == region_id)).first()

        logging.warning(f"Region {data_update.nombre} actualizada correctamente")
        return result
    except Exception as exception_error:
        logging.error(f"Error al actualizar la region {data_update.nombre}: {exception_error}")
        return Response(status_code= SERVER_ERROR )
        

@regionRouter.delete("/region/{region_id}", status_code=HTTP_204_NO_CONTENT)
def delete_facultad(region_id: int):
    try:
        with engine.connect() as conn:
            conn.execute(regiones.delete().where(regiones.c.id == region_id))
        logging.critical(f"Region eliminada correctamente {region_id}: {exception_error}")
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al eliminar la facultad {region_id}: {exception_error}")
        return Response(status_code= SERVER_ERROR )