from os import environ, path

from dotenv import load_dotenv

if path.exists('.env'):
    load_dotenv('.env')
else:
    raise ImportError("Can't import environment variables")

PSQL_HOST = environ.get("PSQL_HOST")
PSQL_PORT = environ.get("PSQL_PORT", "5432")
PSQL_DB_NAME = environ.get("PSQL_DB_NAME")
PSQL_USER = environ.get("PSQL_USER")
PSQL_PASSWORD = environ.get("PSQL_PASSWORD")
