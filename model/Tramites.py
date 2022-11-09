from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime
from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from datetime import datetime
from db.db import engine, meta_data

tramites = Table('tramites', meta_data,
    Column('id', Integer, primary_key=True),
    Column('nombre', String(150), nullable=False),
    Column('aprobado',Boolean , nullable=False),
    Column('fecha_de_solicitud',DateTime(), nullable=False ),
    Column('fecha_de_aprobacion',DateTime(),nullable=True ),
    Column('fecha_de_creacion',DateTime(), default = datetime.now()),
    Column('estudiantes_id', ForeignKey("estudiantes.id")),
)



meta_data.bind = engine
meta_data.create_all()  