from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from os import getcwd, remove, makedirs
from shutil import rmtree
import pathlib
import uuid

from modules.detection import compare_images
from modules.verify_uv_credential import is_uv_credential

arhivosVerificacionTramites_Router = APIRouter()


@arhivosVerificacionTramites_Router.post("/subir/verificar-credencial-uv")
async def upload_file(file_credential: UploadFile = File(...)):
    makedirs('uploads/credential', exist_ok=True)

    file_new_name = uuid.uuid4()
    
    imagen=["jpg","jpeg","png","gif"]
    makedirs('uploads', exist_ok=True)
    makedirs('uploads/credential', exist_ok=True)
    file_name_credential = pathlib.Path(file_credential.filename)

    if file_name_credential.suffix[1:] in imagen:
        with open(getcwd() + "/uploads/credential/" + str(file_new_name) + file_name_credential.suffix , "wb") as myfile_credential:
            content = await file_credential.read()
            myfile_credential.write(content)
            myfile_credential.close()
            #is_uv_credential(myfile_credential.name)
        
        return JSONResponse(content={
                "message": is_uv_credential(myfile_credential.name),
                "uv_credential": True,
                }, status_code=200)
    else:
        return JSONResponse(content={
            "message": "File not valid, please verify it",
            "uv_credential": False,
            }, status_code=400)

@arhivosVerificacionTramites_Router.post("/subir")
async def upload_file(file_photo: UploadFile = File(...), file_credential: UploadFile = File(...),file_video: UploadFile = File(...)):
    file_new_name = uuid.uuid4()
    
    imagen=["jpg","jpeg","png","gif"]
    video=["avi","mp4","mkv"]
    
    makedirs('uploads', exist_ok=True)
    makedirs('uploads/credential', exist_ok=True)
    makedirs('uploads/photo', exist_ok=True)
    makedirs('uploads/video', exist_ok=True)
    
    file_name_photo = pathlib.Path(file_photo.filename)
    file_name_credential = pathlib.Path(file_credential.filename)
    file_name_video = pathlib.Path(file_video.filename)
    
    if file_name_photo.suffix[1:] in imagen and file_name_credential.suffix[1:] in imagen and file_name_video.suffix[1:] in video :
        with open(getcwd() + "/uploads/photo/" + str(file_new_name) + file_name_photo.suffix , "wb") as myfile_photo:
            content = await file_photo.read()
            myfile_photo.write(content)
            myfile_photo.close()
            
    
        with open(getcwd() + "/uploads/credential/" + str(file_new_name) + file_name_credential.suffix , "wb") as myfile_credential:
            content = await file_credential.read()
            myfile_credential.write(content)
            myfile_credential.close()
            #is_uv_credential(myfile_credential.name)

        with open(getcwd() + "/uploads/video/" + str(file_new_name) + file_name_video.suffix , "wb") as myfile_video:
            content = await file_video.read()
            myfile_video.write(content)
            myfile_video.close()
        
        return JSONResponse(content={
                "message": "Files saved",
                "photo": myfile_photo.name,
                "credential": myfile_credential.name,
                "video": myfile_video.name,
                "detection": compare_images(Know= myfile_photo.name, Unknown= myfile_credential.name, Video=myfile_video.name)
                }, status_code=200)

    else:
        return JSONResponse(content={
            "message": "File not saved, verify send photo, credential and video",
            }, status_code=400)



@arhivosVerificacionTramites_Router.get("/archivo/{type_file}/{name_file}")
def get_file(type_file: str, name_file: str):
    return FileResponse(getcwd() + "/uploads/"+type_file +"/"+ name_file)


    """
    download file:
    
    °type_file = this is a folder as photo/credential/video
    °name_file = this is a name assigned by uuid
    Returns:
        FileResponse: download a file 
    """

@arhivosVerificacionTramites_Router.get("/descargar/{type_file}/{name_file}")
def download_file(type_file:str, name_file: str):
    return FileResponse(getcwd() + "/uploads/"+type_file+"/" + name_file, media_type="application/octet-stream", filename=name_file)



    """
    delete_file
    °type_file = this is a folder as photo/credential/video
    °name_file = this is a name assigned by uuid
    Returns:
        JSONResponse: return true is the file was deleted or false if it was not deleted
    """
@arhivosVerificacionTramites_Router.delete("/borrar/{type_file}/{name_file}")
def delete_file(type_file:str, name_file: str):
    try:
        remove(getcwd() + "/uploads/"+ type_file + "/" + name_file)
        return JSONResponse(content={
            "removed": True
        }, status_code=200)
    except FileNotFoundError:
        return JSONResponse(content={
            "removed": False,
            "message": "File not found"
        }, status_code=404)