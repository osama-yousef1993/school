import os

from dotenv import load_dotenv

load_dotenv()


DEBUG = bool(os.getenv("DEBUG"))
PORT = int(os.getenv("PORT"))
HOST_APP = os.getenv("HOST_APP")
HOST_DB = os.getenv("MYSQLHOST")
DB_PORT = int(os.getenv("MYSQLPORT"))
USERNAME = os.getenv("MYSQLUSER")
PASSWORD = os.getenv("MYSQLPASSWORD")
DATABASE = os.getenv("MYSQL_DATABASE")
