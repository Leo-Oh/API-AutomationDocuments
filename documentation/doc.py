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
        "name": "Facultades-Carreras",
        "description": "Se hace la relacion de las carreras con las que cuenta la facultad y la carrera en que facultades se encuentra"
    },
    {
        "name": "Secretarias",
        "description": "Para que se registre una secretaria es necesaria es necesario que pertenzca a una facultad en especifico"
    },
    {
        "name": "Tramites",
        "description": "Se crean los tramites posibles que se podrán realizar y una breve descipción"
    },
     {
        "name": "Secretarias-Tramites",
        "description": "Se hace la relación de los tramites que puede realizar una secretaria y el tramite que hacen muchas secretarias"
    },
      {
        "name": "Secretarias-Carreras",
        "description": "Se hace la relacion de las carreras que supervisa una secretaria y las secretarias que supervisan varias carreras"
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
       

       
    
]