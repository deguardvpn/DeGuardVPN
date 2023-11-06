from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
API_KEYS = os.environ.get("BEARER_TOKEN")
SWAGGER_LOGIN = os.environ.get("SWAGGER_LOGIN")
SWAGGER_PASSWORD = os.environ.get("SWAGGER_PASSWORD")
WG_PORT = os.environ.get("WG_PORT")
