import os

from dotenv import load_dotenv

load_dotenv()


DEBUG = True
PORT = 5000
HOST_DB = os.getenv("HOST_DB", "autorack.proxy.rlwy.net")
DB_PORT = os.getenv("DB_PORT", "52650")
HOST_APP = os.getenv("HOST_APP")
USERNAME = os.getenv("USERNAME", "root")
PASSWORD = os.getenv("PASSWORD", "LqEfixuPehYcVjFAILrIUylPMyAWZGUm")
DATABASE = os.getenv("DATABASE", "railway")
