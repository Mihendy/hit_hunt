from psycopg2.extensions import connection

from data_base.queries import visits_table_create, are_tables_exist


def initialize(conn: connection) -> None:
    tables = {
        'visits': visits_table_create
    }

    existing_tables = are_tables_exist(conn, *tables.keys())

    for table_name, table_create_func in tables.items():
        if not existing_tables[table_name]:
            table_create_func(conn)
