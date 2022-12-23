from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime, Text
from sqlalchemy.sql.sqltypes import Integer, String
from datetime import datetime
from db.db import engine, meta_data


estudiantes = Table('estudiantes', meta_data,
    Column('id', Integer, primary_key=True),
    Column('id_carreras', Integer, ForeignKey("facultades_carreras.id_carreras")),
    Column('id_facultades',Integer, ForeignKey("facultades_carreras.id_facultades")),
    Column('nombre_completo', String(200), nullable=False),
    #Column('nombre', String(150), nullable=False),
    #Column('apellido_paterno', String(40), nullable=False),
    #Column('apellido_materno', String(40), nullable=False),
    Column('matricula', String(150), nullable=False),
    Column('correo', String(150), nullable=False),
    Column('contrasena', Text, nullable=False),
    Column('semestre', Integer, nullable=False),
    Column('telefono', String(20)),
    Column('foto_perfil', Text),
    
    Column('fecha_de_creacion',DateTime(), default = datetime.now()),
)

meta_data.bind = engine
meta_data.create_all()  