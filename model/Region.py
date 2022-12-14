from sqlalchemy import VARCHAR, Table, Column, Integer, String, DateTime
from sqlalchemy.sql.sqltypes import Integer, String
from datetime import datetime
from db.db import engine, meta_data

regiones = Table('regiones', meta_data,
    Column('id', Integer, primary_key=True),
    Column('nombre', VARCHAR(150), nullable=False),
    
    Column('fecha_de_creacion',DateTime(), default = datetime.now())
)



meta_data.bind = engine
meta_data.create_all()  