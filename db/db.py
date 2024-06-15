from sqlalchemy import create_engine, MetaData
import os
from dotenv import load_dotenv

load_dotenv()

# Se lee el archivo de configuración 
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')


engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

conn = engine.connect()
meta_data = MetaData()
