"""
Application settings singleton is defined here.
"""
from test_fastapi.config import AppSettings


app_settings = AppSettings.try_from_env()
