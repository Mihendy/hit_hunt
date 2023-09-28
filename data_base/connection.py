import data_base.constants as const
import psycopg2

DB_CONNECTION = psycopg2.connect(host=const.PSQL_HOST,
                                 user=const.PSQL_USER,
                                 dbname=const.PSQL_DB_NAME,
                                 password=const.PSQL_PASSWORD)
