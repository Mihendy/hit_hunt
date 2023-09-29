from datetime import datetime as dt
from pydantic import BaseModel


class Visitor(BaseModel):
    ip: str
    datetime: str = str(dt.utcnow())
    platform: str = "NULL"  # optional
    agent: str = "NULL"  # optional
