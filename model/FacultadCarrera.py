from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime
from sqlalchemy.sql.sqltypes import Integer, String
from datetime import datetime
from db.db import engine, meta_data


facultades_carreras = Table('facultades_carreras', meta_data,
    Column('facultades_id', ForeignKey('facultades.id')),
    Column('carreras_id', ForeignKey('carreras.id'))
)

meta_data.bind = engine
meta_data.create_all()  