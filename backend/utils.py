"""Contains frequently required functions and variables
"""

from functools import wraps
from fastapi import status
from fastapi.exceptions import HTTPException
from fzmovies_api.errors import SessionExpired
import typing as t
from datetime import datetime, UTC
from backend.config import logger


def router_exception_handler(func: t.Callable):
    """Decorator for handling api routes exceptions accordingly

    Args:
        func (t.Callable): FastAPI router.
    """

    @wraps(func)
    async def decorator(*args, **kwargs):
        try:
            resp = await func(*args, **kwargs)
            return resp
        except AssertionError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except SessionExpired as e:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail=(
                    "Looks like previous requests was never made recently "
                    "or from this server.!"
                ),
            )
        except Exception as e:
            logger.exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=(
                    "There was an issue with the server while "
                    "while trying to handle that request!",
                ),
            )

    return decorator


def utcnow() -> datetime:
    """UTC time now"""
    return datetime.now(UTC)
