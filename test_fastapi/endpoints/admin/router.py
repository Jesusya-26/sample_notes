"""
Update router is defined here.
"""
from fastapi import APIRouter


admin_data_router = APIRouter(tags=["admin"], prefix="/users/{user_id}")
