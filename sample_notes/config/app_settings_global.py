"""
Application settings singleton is defined here.
"""
from sample_notes.config import AppSettings


app_settings = AppSettings.try_from_env()
