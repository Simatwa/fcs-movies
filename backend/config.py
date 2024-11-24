"""Contains configuration"""

from pydantic import BaseModel, field_validator, PositiveInt
from dotenv import dotenv_values
from pathlib import Path
import typing as t
import re
import logging

logger = logging.getLogger("fcs_movies")


class Config(BaseModel):
    """Configurations set"""

    database_engine: t.Optional[str] = "sqlite:///assets/db.sqlite3"
    search_limit_per_query: t.Optional[PositiveInt] = 100
    search_stream_limit_per_query: t.Optional[PositiveInt] = 500
    download_link_cache_duration_in_hours: t.Optional[PositiveInt] = 24

    @field_validator("database_engine")
    def validate_database_engine(value):
        """Checks if the database exists incase it's an sqlite3 engine"""
        pattern = re.compile(r"sqlite:///(.+)")
        if pattern.match(value):
            db_path = Path(pattern.findall(value)[0])
            if not db_path.exists():
                raise ValueError(f"Database engine does not exists - {value}")

        return value


config = Config(**dotenv_values())
"""Configurations loaded from .env file"""
