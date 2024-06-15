from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from os import getcwd, remove, makedirs
from shutil import rmtree
import pathlib
import uuid

from modules.detection import compare_images
from modules.verify_uv_credential import is_uv_credential

arhivosTramites_Router = APIRouter()


@arhivosTramites_Router.post("/subir")
async def upload_file(file_document: UploadFile = File(...)):
    file_new_name = uuid.uuid4()
    
    archivo=["jpg","jpeg","png","pdf","doc"]
    
    makedirs('uploads', exist_ok=True)
    makedirs('uploads/solicitudes', exist_ok=True)
    
    file_name_document = pathlib.Path(file_document.filename)
    
    if file_name_document.suffix[1:] in archivo:
        with open(getcwd() + "/uploads/solicitudes/" + str(file_new_name) + file_name_document.suffix , "wb") as myfile_document:
            content = await file_document.read()
            myfile_document.write(content)
            myfile_document.close()
                    
        return JSONResponse(content={
                "message": "Files saved",
                "archivo": myfile_document.name,
                }, status_code=200)

    else:
        return JSONResponse(content={
            "message": "File not saved",
            }, status_code=400)



@arhivosTramites_Router.get("/archivo/{nombre_archivo}")
def get_file( nombre_archivo: str):
    return FileResponse(getcwd() + "/uploads/solicitudes/"+ nombre_archivo)



@arhivosTramites_Router.get("/descargar/{nombre_archivo}")
def download_file( nombre_archivo: str):
    return FileResponse(getcwd() + "/uploads/solicitudes/" + nombre_archivo, media_type="application/octet-stream", filename=nombre_archivo)


@arhivosTramites_Router.delete("/borrar/{nombre_archivo}")
def delete_file(nombre_archivo: str):
    try:
        remove(getcwd() + "/uploads/solicitudes/" + nombre_archivo)
        return JSONResponse(content={
            "removed": True
        }, status_code=200)
    except FileNotFoundError:
        return JSONResponse(content={
            "removed": False,
            "message": "File not found"
        }, status_code=404)