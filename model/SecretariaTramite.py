from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime
from sqlalchemy.sql.sqltypes import Integer, String
from datetime import datetime
from db.db import engine, meta_data


secretarias_tramites = Table('secretarias_tramites', meta_data,
    Column('id_secretarias', ForeignKey('secretarias.id')),
    Column('id_tramites', ForeignKey('tramites.id')),
)

meta_data.bind = engine
meta_data.create_all()  