"""
Login (authorization) response is defined here.

Login request is not needed due to use of OAuth2PasswordRequestForm from fastapi.security.
"""
from pydantic import BaseModel


class LoginResponse(BaseModel):
    """
    Response body class for login endpoint - contains access and refresh tokens.
    """

    access_token: str
    refresh_token: str
