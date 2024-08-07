# Счётчик посещений сайта на FastAPI

Пример реализации API для получения данных о посещении сайта.

## [Виртуальные переменные](example.env)

| Название переменной               | Значение                                                |   Пример    | 
|:----------------------------------|:--------------------------------------------------------|:-----------:|
| [`PSQL_HOST`](example.env#L1)     | Хост, на котором развернут сервер баз данных PostgreSQL | `127.0.0.1` |
| [`PSQL_PORT` ](example.env#L2)    | Порт сервера баз данных PostgreSQL                      |   `5432`    |
| [`PSQL_USER` ](example.env#L3)    | Имя пользователя, имеющего доступ к БД                  | `username`  |
| [`PSQL_PASSWORD`](example.env#L4) | Пароль пользователя                                     | `password`  |
| [`PSQL_DB_NAME`](example.env#L5)  | Имя БД, к которой нужно подключиться                    |  `dbname`   |

## API счётчика

**Посещение засчитывается на главной станице:**

Запрос:

```shell
curl 127.0.0.1:8000
```

Ответ:

```shell
StatusCode        : 200
StatusDescription : OK
Content           : {"message":"Your visit has been recorded."}
```

**API V1**

API имеет 2 вида работы (`raw` и `stat`): `raw` - `default`, реализует посещение главной страницы в сыром виде, но с
большим
количеством фильтров. А `stat` - получение статистики посещений по **дням** / **месяцам** / **годам**.

`raw` запрос:

```shell
curl 127.0.0.1:8000/api/v1/get?limit=1&skip=5&like=windows
```

Ответ заголовка `Content` в формате `JSON`:

```json
[
  {
    "ip": "127.0.0.1",
    "session_time": "01-10-2023 12:00:50",
    "platform": "Windows",
    "agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
  }
]
```

`stat` запрос:

```shell
curl 127.0.0.1:8000/api/v1/get?limit=1&skip=5&like=windows&mode=stat
```

Ответ заголовка `Content` в формате `JSON` по ключу `ips`:

```json
{
  "all": {
    "2023": {
      "total": 1,
      "by_month": {
        "9": {
          "total": 1,
          "by_day": {
            "29": {"total": 1, "127.0.0.1": 1}
          },
          "127.0.0.1": 1
        }
      },
      "127.0.0.1": 1
    }
  },
  "unique": {
    "2023": {
      "unique": ["127.0.0.1"],
      "length": 1,
      "by_month": {
        "9": {"unique": ["127.0.0.1"],
          "length": 1,
          "by_day": {
            "29": {
              "unique": ["127.0.0.1"],
              "length": 1
            }
          }
        }
      }
    }
  }
}
```

## P.S.

Больше информации по запросам и ответам в документации по адресу /docs.
