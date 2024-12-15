import os

from dotenv import load_dotenv

load_dotenv()


DEBUG = bool(os.getenv("DEBUG"))
PORT = int(os.getenv("PORT"))
HOST_APP = os.getenv("HOST_APP")
HOST_DB = os.getenv("MYSQLHOST", "mysql.railway.internal")
DB_PORT = os.getenv("MYSQLPORT", 3306)
USERNAME = os.getenv("MYSQLUSER", "root")
PASSWORD = os.getenv("MYSQLPASSWORD", "mSnuQOuRkKoqlONttfrxArCHBRmWFKmF")
DATABASE = os.getenv("MYSQL_DATABASE", "railway")
