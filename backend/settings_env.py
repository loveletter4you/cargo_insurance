import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DB_HOST: str = os.environ.get("DB_HOST")
DB_ROOT: str = os.environ.get("DB_ROOT")
DB_PASSWORD: str = os.environ.get("DB_PASSWORD")
DB_NAME: str = os.environ.get("DB_NAME")


ADMIN_LOGIN: str = os.environ.get("ADMIN_LOGIN")
ADMIN_PASSWORD: str = os.environ.get("ADMIN_PASSWORD")