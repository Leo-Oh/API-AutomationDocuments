from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime, Text
from sqlalchemy.sql.sqltypes import Integer, String
from datetime import datetime
from db.db import engine, meta_data


secretarias = Table('secretarias', meta_data,
    Column('id', Integer, primary_key=True),
    Column('id_facultades', ForeignKey("facultades.id")),
    
    Column('nombre', String(150), nullable=False),
    Column('apellido_paterno', String(40), nullable=False),
    Column('apelldo_materno', String(40), nullable=False),
    Column('turno', String(40), nullable=False),
    Column('telefono', String(20)),
    Column('matricula', String(30), nullable=False),
    Column('correo', String(60), nullable=False),
    Column('contrasena', Text, nullable=False),
    Column('direccion', Text),
    Column('foto_perfil', Text),
    
    Column('fecha_de_creacion',DateTime(), default = datetime.now()),
        
)


meta_data.bind = engine
meta_data.create_all()  