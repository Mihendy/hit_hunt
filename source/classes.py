from datetime import datetime as dt, datetime
from typing import Any, Optional

from fastapi import Query
from pydantic import (BaseModel, Field, conint,
                      field_validator, model_validator)


class Visitor(BaseModel):
    ip: str
    datetime: str = str(dt.utcnow())  # optional
    platform: str = "NULL"  # optional
    agent: str = "NULL"  # optional


class Filter(BaseModel):
    start: Optional[str] = Field(Query(None, description="Represents the start date & time"))
    end: Optional[str] = Field(Query(None, description="Represents the end date & time"))
    like: Optional[str] = Field(Query(None, description="Represents a keyword or pattern to filter results"
                                                        " based on a partial match. Example: \"apple\" to "
                                                        "filter results containing the word \"apple\"."))
    limit: conint(ge=0, le=100) = 10
    utc: float = Field(default=0, ge=-12, le=12)
    unique: bool = False

    @classmethod
    @field_validator("start", "end")
    def validate_str_datetime(cls, value):
        """Проверка даты, написанной строкой слитно в
            формате ДД-ММ-ГГГГ:чч:мм:cc (exp: 16-05-2022:01:50:30)"""
        if value is None:
            return value
        try:
            datetime.strptime(value, "%d-%m-%Y:%H:%M:%S")
        except (ValueError, TypeError):
            try:
                datetime.strptime(value, "%d-%m-%Y")
            except (ValueError, TypeError):
                raise ValueError("Input should be DD-MM-YYYY:hh:mm:ss or DD-MM-YYYY")
        return value

    @classmethod
    @field_validator("like")
    def validate_isalnum(cls, value):
        if value is None:
            return value
        if value.isalnum():
            return value
        raise ValueError("Input should contain letters or numbers")

    @classmethod
    @field_validator("utc")
    def utc_validator(cls, utc):
        """Проверка валидности UTC"""
        if utc in map(lambda x: x / 10, range(-120, 121, 5)):
            return utc
        raise ValueError("Input should be an integer or half number")
