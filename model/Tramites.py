from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime, Text
from sqlalchemy.sql.sqltypes import Integer, String
from datetime import datetime
from db.db import engine, meta_data


tramites = Table('tramites', meta_data,
    Column('id', Integer, primary_key=True),  
    Column('nombre', String(150), nullable=False),
    Column('descripcion', Text, nullable=False),

    Column('fecha_de_creacion',DateTime(), default = datetime.now()),
)


meta_data.bind = engine
meta_data.create_all()  