# TRAMITES branch

Versión de python donde se desarrolló 

Python 3.8.10

Systema Operativo Windows 11

Configuración:

1. Crear archivo de configuración llamado ".env" con las siguientes credenciales:

    SECRET_KEY = ""

    LOCAL_DB_USER = ""
    LOCAL_DB_PASSWORD = ""
    LOCAL_DB_HOST = ""
    LOCAL_DB_PORT = ""
    LOCAL_DB_NAME = ""

2. Crear un entorno virtual para la instalación de las librerias

    python3 -m venv venv

    -- o --

    python -m venv venv

3. Ingresar al enntorno virtual:

    Linux:

    source venv/bin/activate

    Windows:

    .\venv\Scripts\activate.bat

    -- o --

    .\venv\Scripts\activate  

4. Instalar las librerias necesarias que se encuentran en el archivo "requirements.txt"

    pip install -r requirements.txt

    -- o -- 

    pip install -r requirements.txt

5. Ejecutar la API

    uvicorn main:app --reload 
 

Crear Docker con MySQL

Creamos un volumen

    sudo docker volume create mysql-db

Verificamos que se haya creado el volumen

    sudo docker volume ls

Correr imagen de mysql asignando la contraseña

    sudo docker run -d -p 3306:3306 --name mysql-db-container  -e MYSQL_ROOT_PASSWORD=password --mount src=mysql-db,dst=/var/lib/mysql mysql

    sudo docker exec -it mysql-db  mysql -p

