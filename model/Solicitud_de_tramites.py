from sqlalchemy import VARCHAR, ForeignKey, Table, Column, Integer, String, DateTime, Text
from sqlalchemy.sql.sqltypes import Integer, String
from datetime import datetime
from db.db import engine, meta_data


solicitudes_de_tramites = Table('solicitdes_de_tramites', meta_data,
    Column('id', Integer, primary_key=True),
    Column('id_secretarias', ForeignKey("secretarias.id")),
    Column('id_tramites', ForeignKey("tramites.id")),
    Column('id_carreras', ForeignKey("carreras.id")),
    Column('id_estudiantes', ForeignKey("estudiantes.id")),
    Column('datos_adjuntos_estudiante', Text),
    Column('datos_adjuntos_secretaria', Text),
    Column('mensaje_secretaria', Text),
    Column('fecha_de_solicitud',DateTime(), nullable=False),
    Column('estado', VARCHAR(120), nullable=False),
    Column('fecha_de_aprobacion',DateTime()),

    Column('fecha_de_creacion',DateTime(), default = datetime.now()),
    
    
    
)


meta_data.bind = engine
meta_data.create_all()  