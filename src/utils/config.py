import os

from dotenv import load_dotenv

load_dotenv()


DEBUG = bool(os.getenv("DEBUG"))
PORT = int(os.getenv("PORT"))
HOST_APP = os.getenv("HOST_APP")
HOST_DB = os.getenv("MYSQLHOST")
DB_PORT = os.getenv("MYSQLPORT")
USERNAME = os.getenv("MYSQLUSER")
PASSWORD = os.getenv("MYSQLPASSWORD")
DATABASE = os.getenv("MYSQL_DATABASE")

# DEBUG = bool(os.getenv("DEBUG", "True"))
# PORT = int(os.getenv("PORT", "5003"))
# HOST_APP = os.getenv("HOST_APP", "127.0.0.1")
# HOST_DB = "db4free.net"
# DB_PORT = 3306
# USERNAME = "issaprojects"
# PASSWORD = "test123456"
# DATABASE = "testmyprojectsdb"
