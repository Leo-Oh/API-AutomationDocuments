from sqlalchemy import VARCHAR, ForeignKey, Table, Column, Integer, DateTime, Text
from datetime import datetime
from db.db import engine, meta_data


facultades = Table('facultades', meta_data,
    Column('id', Integer,nullable=False,  primary_key=True),
    Column('id_regiones', ForeignKey("regiones.id")),
    Column('nombre', VARCHAR(150), nullable=False),
    Column('direccion', Text, nullable=False),
    Column('telefono', VARCHAR(20)),
    
    Column('fecha_de_creacion',DateTime(), default = datetime.now()),
    
)


meta_data.bind = engine
meta_data.create_all()  
