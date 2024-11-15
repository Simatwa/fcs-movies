"""Version 1 of the API
Unlike the version 2 which sources data from sqlite3 db (not yet implemented),
this one sources data direct from host in real time.
"""

from fastapi import APIRouter
from backend.v1.main import router as main_router

v1_router = APIRouter()

v1_router.include_router(main_router)
