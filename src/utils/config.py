import os

from dotenv import load_dotenv

load_dotenv()


DEBUG = True
PORT = 5000
HOST_DB = os.getenv("HOST_DB")
HOST_APP = os.getenv("HOST_APP")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")
