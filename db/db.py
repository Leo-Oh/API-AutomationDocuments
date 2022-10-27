from sqlalchemy import create_engine, MetaData
import os
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv('LOCAL_DB_USER')
db_password = os.getenv('LOCAL_DB   _PASSWORD')
db_host = os.getenv('LOCAL_DB_HOST')
db_port = os.getenv('LOCAL_DB_PORT')
db_name = os.getenv('LOCAL_DB_NAME')

engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

conn = engine.connect()
meta_data = MetaData()
