"""
Version 2 of the API.
Unlike the v1 which searches movies from host
in real-time, this searches movies from
sqlite3 db
"""

from fastapi import APIRouter
from backend.v2.routes import router

v2_router = APIRouter()

v2_router.include_router(router)
