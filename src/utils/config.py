import os

from dotenv import load_dotenv

load_dotenv()


DEBUG = bool(os.getenv("DEBUG"))
PORT = int(os.getenv("PORT"))
HOST_DB = os.getenv("MYSQLHOST")
DB_PORT = int(os.getenv("MYSQLPORT"))
HOST_APP = os.getenv("HOST_APP")
USERNAME = os.getenv("MYSQLUSER")
PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD")
DATABASE = os.getenv("MYSQL_DATABASE")
