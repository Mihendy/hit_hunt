from fastapi import FastAPI, Request, status, Depends
from fastapi.responses import JSONResponse

from datetime import datetime as dt
from datetime import timedelta
from contextlib import asynccontextmanager

from pydantic import ValidationError

from data_base.sql_init import initialize
from data_base.connection import DB_CONNECTION
from data_base.queries import save_new_visitors

from source.classes import Visitor, Filter

banned_ips = dict()
strange_ips = dict()
new_visitors = list()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # do something before the application starts taking requests
    initialize(DB_CONNECTION)

    yield

    if new_visitors:
        save_new_visitors(DB_CONNECTION, new_visitors)
        new_visitors.clear()
    # do something after the application finishes handling request


app = FastAPI(lifespan=lifespan)


@app.exception_handler(ValidationError)
async def value_error_exception_handler(request: Request, exc: ValidationError):
    """Обработчик ошибок возникших в процессе валидации"""
    error = [{"type": err["type"], "loc": err["loc"][0],
              "msg": err["msg"].replace("Value error, ", ""),
              "input": err["input"]} for err in exc.errors()]
    print(error)

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": error}
    )


@app.middleware("http")
async def validate_ip(request: Request, call_next):
    ip = str(request.client.host)
    now = dt.utcnow()

    if ip in strange_ips:

        visits = strange_ips[ip]["visits"]

        if visits == 15:
            banned_ips[ip] = now
            strange_ips.pop(ip, None)

        elif now - strange_ips[ip]["first_request_dt"] < timedelta(seconds=15):
            visits += 1
            strange_ips[ip]["visits"] = visits

    elif ip not in banned_ips:
        strange_ips[ip] = {"visits": 1, "first_request_dt": now}

    if ip in banned_ips:

        if now - banned_ips[ip] > timedelta(seconds=15):
            banned_ips.pop(ip, None)
            return await call_next(request)

        data = {"message": f"IP {ip} was temporarily banned."}

        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=data)

    return await call_next(request)


@app.get("/")
async def root(request: Request):
    headers = request.headers
    platform = "".join(s for s in str(headers.get("sec-ch-ua-platform")) if s.isalpha() or s.isspace())
    agent = str(headers.get("user-agent"))
    ip = request.client.host
    data = {"message": "Your visit has been recorded."}

    visitor = Visitor(ip=ip)
    if platform != str(None):
        visitor.platform = f"'{platform}'"
    if agent != str(None):
        visitor.agent = f"'{agent}'"

    new_visitors.append(visitor)

    return JSONResponse(status_code=status.HTTP_200_OK, content=data)


@app.get("/api/v1/get/")
async def v1_get_visitors(filters: Filter = Depends()):
    if new_visitors:
        save_new_visitors(DB_CONNECTION, new_visitors)
        new_visitors.clear()
    data = {"message": None}
    return JSONResponse(status_code=status.HTTP_200_OK, content=data)
