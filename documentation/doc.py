"""
    ==================================
    This is a documentation from API
    here are the title about each 
    action.
    ==================================
"""
tags_metadatas = [
    {
        "name": "Regiones",
        "description": "Es la entidad más alta de la cual parte el sistema"
    },
    {
        "name": "Facultades",
        "description": "Para que exista una facultad es necesario tenr una region"
    },
    {
        "name": "Carreras",
        "description": "A qui solo es necesario tener registradas las carreras con las que cuenta la facultad"
    },
    {
        "name": "Secretarias",
        "description": "Para que se registre una secretaria es necesaria es necesario que pertenezca a una facultad en especifico"
    },
    {
        "name": "Tramites",
        "description": "Se crean los tramites posibles que se podrán realizar y una breve descipción"
    },
       {
        "name": "Estudiantes",
        "description": "Se registran a los estudiantes perteneientes a cada carrera"
    },
       {
        "name": "Solicitud de tramites",
        "description": "Para realizar una solicitud de tramite es necesario tener a los involucrados en dicha petición (estudiante,secretaria,carrera y el tipo de tramite a realizar)"
    },
       {
        "name": "Archvivos para la verificación de tramites",
        "description": "Antes de realiar una petición de un tramite es necesario que el estudiante suba sus datos para la autenticidad"
    },
    {
        "name": "Archvivos que mandan las secretarias a los estudiantes",
        "description": "Se crea un registro los archiivos proporcionados por las secretarias"
    },
    {
        "name": "Facultades-Carreras",
        "description": ""
    },
    {
        "name": "Secretarias-Tramites",
        "description": ""
    },
    {
        "name": "Secretarias-Carreras",
        "description": ""
    }       
    
]