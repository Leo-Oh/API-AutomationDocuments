import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from router.Region import regiones_Router
from router.Facultad import facultades_Router
from router.Carrera import carreras_Router
from router.FacultadCarrera import facultadesCarreras_Router
from router.Secretaria import secretarias_Router
from router.Tramite import tramites_Router
from router.SecretariaTramite import secretariasTramites_Router
from router.SecretariaCarrera import secretariasCarreras_Router
from router.Estudiante import estudiantes_Router
from router.SolicitudTramite import solicitud_de_tramites_Router

from router.ArchivoVerificacionTramite import arhivosVerificacionTramites_Router
from router.ArchivoTramite import arhivosTramites_Router

from router.Administrador import administradores_Router

from documentation.doc import tags_metadatas

from os import makedirs

from pathlib import Path

app = FastAPI(
    title="REST API to Automation Documents by UV",
    description="By ISW UV",
    version="0.1",
    openapi_tags=tags_metadatas
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(regiones_Router,prefix='/api',tags=["Regiones"])
app.include_router(facultades_Router,prefix='/api',tags=["Facultades"])
app.include_router(carreras_Router,prefix='/api',tags=["Carreras"])
app.include_router(facultadesCarreras_Router,prefix='/api',tags=["Facultades-Carreras"])
app.include_router(secretarias_Router,prefix='/api',tags=["Secretarias"])
app.include_router(tramites_Router,prefix='/api',tags=["Tramites"])
app.include_router(secretariasTramites_Router,prefix='/api',tags=["Secretarias-Tramites"])
app.include_router(secretariasCarreras_Router,prefix='/api',tags=["Secretarias-Carreras"])

app.include_router(estudiantes_Router,prefix='/api',tags=["Estudiantes"])
app.include_router(administradores_Router,prefix='/api',tags=["Administrador"])
app.include_router(solicitud_de_tramites_Router,prefix='/api',tags=["Solicitud de tramites"])

app.include_router(arhivosVerificacionTramites_Router,prefix='/api/files/verificacion-tramites',tags=["Archvivos para la verificación de tramites"])
app.include_router(arhivosTramites_Router,prefix='/api/files/tramites',tags=["Archvivos que mandan las secretarias a los estudiantes"])

load_dotenv()
if __name__ == "__main__":

    Path("log").mkdir(parents=True, exist_ok=True)
    uvicorn.run(app, port=1001, host="0.0.0.0", debug=True)