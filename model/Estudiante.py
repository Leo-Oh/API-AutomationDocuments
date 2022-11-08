from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime
from sqlalchemy.sql.sqltypes import Integer, String
from datetime import datetime
from db.db import engine, meta_data


estudiantes = Table('estudiantes', meta_data,
    Column('id', Integer, primary_key=True),
    Column('nombre', String(150), nullable=False),
    Column('apellido_paterno', String(150), nullable=False),
    Column('apellido_materno', String(150), nullable=False),
    Column('matricula', String(150), nullable=False),
    Column('correo', String(150), nullable=False),
    Column('contrasena', String(250), nullable=False),
    Column('semestre', Integer, nullable=False),
    
    Column('carreras_id', ForeignKey("carreras.id")),
    Column('fecha_de_creacion',DateTime(), default = datetime.now()),
)


meta_data.bind = engine
meta_data.create_all()  