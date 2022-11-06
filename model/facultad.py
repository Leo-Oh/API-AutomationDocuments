from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from db.db import engine, meta_data


facultades = Table('facultad', meta_data,
    Column('id', Integer, primary_key=True),
    Column('nombre', String(150), nullable=False),
    Column('region', String(60), nullable=False),
)


meta_data.bind = engine
meta_data.create_all()  