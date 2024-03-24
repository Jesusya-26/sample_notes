"""
Api routers are defined here.

It is needed to import files which use these routers to initialize endpoints.
"""
from fastapi import APIRouter
from .users import user_data_router

notes_router = APIRouter(tags=["notes"], prefix="/notes")

system_router = APIRouter(tags=["system"])

routers_list = [
    notes_router,
    system_router,
    user_data_router
]

__all__ = [
    "routers_list",
]
