from datetime import datetime as dt, datetime
from enum import Enum
from typing import Optional

from fastapi import Query
from pydantic import (BaseModel, field_validator,
                      Field, model_validator)


class Visitor(BaseModel):
    """Site visitor model"""
    ip: str
    datetime: str = str(dt.utcnow())
    platform: str = "NULL"
    agent: str = "NULL"


class Mode(str, Enum):
    """Output mode"""
    raw = "raw"
    stat = "stat"


# noinspection PyNestedDecorators
class Filter(BaseModel):
    """Filter model for which database query will be built"""
    start: Optional[str] = Field(Query(None, description="Represents the start date & time"))
    end: Optional[str] = Field(Query(None, description="Represents the end date & time"))
    like: Optional[str] = Field(Query(None, description="Represents a keyword or pattern to filter results"
                                                        " based on a partial match. Example: \"apple\" to "
                                                        "filter results containing the word \"apple\""))
    limit: int = Field(Query(default=10, ge=1, le=100, description="Represents the maximum number of"
                                                                   " results to be returned"))
    skip: int = Field(Query(default=0, ge=0, description="Represents the number of results will be skipped"))
    utc: float = Field(Query(default=0, ge=-12, le=12, description="Represents the time zone offset in hours"))
    mode: Mode = Field(Query(default=Mode.raw, description="Represents mode of response"))

    @field_validator("start", "end")
    @classmethod
    def validate_str_datetime(cls, value):
        """Check date written by string in DD-MM-YYYY:hh:mm:ss format (exp: 16-05-2022:01:50:30)"""
        if value is None:
            return None
        try:
            return datetime.strptime(value, "%d-%m-%Y:%H:%M:%S")
        except (ValueError, TypeError):
            try:
                return datetime.strptime(value, "%d-%m-%Y")
            except (ValueError, TypeError):
                raise ValueError("Input should be DD-MM-YYYY:hh:mm:ss or DD-MM-YYYY")

    @field_validator("like")
    @classmethod
    def validate_isalnum(cls, value):
        """Validate that value contains only letters and digits"""
        if value is None:
            return value
        if value.isalnum():
            return value
        raise ValueError("Input should contain letters or numbers")

    @field_validator("utc")
    @classmethod
    def utc_validator(cls, utc):
        """Validate that UTC is correct"""
        if utc in map(lambda x: x / 10, range(-120, 121, 5)):
            return utc
        raise ValueError("Input should be an integer or half number")

    @model_validator(mode="after")
    def check_start_earlier_than_end(self) -> "Filter":
        """Validate that start earlier than end"""
        start, end = self.start, self.end
        if start is not None and end is not None:
            if start > end:
                raise ValueError("'start' datetime should be less or equal than 'end' datetime")
        if start is not None:
            self.start = str(start)
        else:
            self.start = None

        if end is not None:
            self.end = str(end)
        else:
            self.end = None

        return self
