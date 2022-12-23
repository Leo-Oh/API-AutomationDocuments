from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime, Text
from sqlalchemy.sql.sqltypes import Integer, String
from datetime import datetime
from db.db import engine, meta_data


administradores = Table('administradores', meta_data,
    Column('id', Integer, primary_key=True),
    Column('id_facultades', ForeignKey("facultades.id")),
    Column('usuario', String(25), nullable=False),
    Column('correo', String(60), nullable=False), 
    Column('contrasena',String(300), nullable=False),
    Column('nombre', String(60), nullable=False),
    Column('apellido_paterno', String(40), nullable=False),
    Column('apellido_materno', String(40), nullable=False),
    Column('foto_perfil', Text),
     
    Column('fecha_de_creacion',DateTime(), default = datetime.now()),
)


meta_data.bind = engine
meta_data.create_all()  