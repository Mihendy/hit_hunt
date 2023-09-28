from psycopg2.extensions import connection


def are_tables_exist(conn: connection, *tables):
    """Функция получает на вход соединение с БД PostgreSQL
    и список названий таблиц и возвращает словарь с названиями
    таблиц и ответом, где True - существует, а False - нет.
    Пример:
    In: (connection, 'ips', 'logs')
    Out: {'ips': True, 'logs': False}"""
    with conn.cursor() as cursor:
        query = (f"SELECT table_name FROM information_schema.tables "
                 f"WHERE table_schema='public' AND table_type='BASE TABLE';")
        cursor.execute(query)
        result = tuple(map(lambda x: x[0], cursor.fetchall()))
        out = dict([(table, table in result) for table in tables])
        return out


def visits_table_create(conn: connection):
    with conn.cursor() as cursor:
        table_create_query = ("CREATE TABLE visits "
                              "(id SERIAL PRIMARY KEY, ip VARCHAR(128) NOT NULL, "
                              "datetime TIMESTAMP, platform VARCHAR(256) NULL,"
                              "agent VARCHAR(512) NULL);")
        cursor.execute(table_create_query)
        conn.commit()
        print("Таблица создана")


def save_new_visitors(conn: connection, visitors):
    with conn.cursor() as cursor:
        query = ("INSERT INTO visits "
                 "(ip, datetime, platform, agent) values "
                 + ", ".join(f"('{visitor.ip}', "
                             f"'{visitor.datetime}', "
                             f"{visitor.platform}, "
                             f"{visitor.agent})" for visitor in visitors) + ";")
        cursor.execute(query)
        conn.commit()
        print("Выгружено")
