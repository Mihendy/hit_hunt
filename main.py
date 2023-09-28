from fastapi import FastAPI, Request
# from datetime import datetime as dt
from data_base.sql_init import initialize
from data_base.connection import DB_CONNECTION

app = FastAPI()
initialize(DB_CONNECTION)


@app.get("/")
async def root(request: Request):
    headers = request.headers
    platform = "".join(s for s in str(headers.get("sec-ch-ua-platform")) if s.isalpha() or s.isspace())
    agent = str(headers.get("user-agent"))
    ip = request.client.host
    # current_time = dt.utcnow()
    response = {"message": {"platform": platform, "agent": agent, "host": ip}}
    print(response)
    return response
