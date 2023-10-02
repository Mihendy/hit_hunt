from datetime import datetime

from psycopg2.extensions import connection

from source.functions import get_statistic_by


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


def raw_visitors_selection(conn: connection, filters):
    utc = f"'{str(filters.utc).replace('.5', ':30').replace('.0', ':00')}'"
    limit, skip = filters.limit, filters.skip
    start, end, like = filters.start, filters.end, filters.like

    query = f"SELECT ip, datetime AT TIME ZONE {utc}, platform, agent FROM visits WHERE TRUE"
    if start is not None:
        query += f" AND datetime >= '{filters.start}'"
    if end is not None:
        query += f" AND datetime <= '{filters.end}'"
    if like is not None:
        query += f" AND platform ILIKE '%{filters.like}%'"
    query += f" OFFSET {skip}"
    query += f" LIMIT {limit};"

    with conn.cursor() as cursor:

        cursor.execute(query)
        result = cursor.fetchall()
        datetime.now()
        data = list(map(lambda x: dict([('ip', x[0]), ('session_time', x[1].strftime("%d-%m-%Y %H:%M:%S")),
                                        ('platform', x[2]), ('agent', x[3])]), result))
        return data


def get_visitors_statistic(conn: connection, filters):
    utc = f"'{str(filters.utc).replace('.5', ':30').replace('.0', ':00')}'"
    start, end, like = filters.start, filters.end, filters.like
    query = f"SELECT ip, datetime AT TIME ZONE {utc}, platform, agent FROM visits WHERE TRUE"
    if start is not None:
        query += f" AND datetime >= '{filters.start}'"
    if end is not None:
        query += f" AND datetime <= '{filters.end}'"
    if like is not None:
        query += f" AND platform ILIKE '%{filters.like}%'"

    with conn.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        raw_data = list(map(lambda x: dict([("ip", x[0]), ("session_time", x[1]),
                                            ("platform", x[2]), ("agent", x[3])]), result))

        data = {"ips": get_statistic_by("ip", raw_data),
                "platforms": get_statistic_by("platform", raw_data),
                "agents": get_statistic_by("agent", raw_data)}

        return data
