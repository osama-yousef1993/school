import os

from dotenv import load_dotenv

load_dotenv()


DEBUG = bool(os.getenv("DEBUG"))
PORT = int(os.getenv("PORT"))
HOST_DB = os.getenv("HOST_DB")
DB_PORT = int(os.getenv("DB_PORT"))
HOST_APP = os.getenv("HOST_APP")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")
