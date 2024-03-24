"""
Authorization logic is defined here.
"""

from test_fastapi.dto.users import TokensTuple
from test_fastapi.utils.dependencies import keycloak_openid


async def authorize(username: str, password: str) -> TokensTuple:
    """
    Returns an access and refresh tokens for a user if user with given login (email or name)"
        exists and password hash matched
    """

    token = keycloak_openid.token(username, password)

    return TokensTuple(token['access_token'], token['refresh_token'])


async def refresh_tokens(refresh_token: str) -> TokensTuple:
    """
    Returns an access and refresh tokens for a given refresh token if it is valid and user is active
    """

    token = keycloak_openid.refresh_token(refresh_token)

    return TokensTuple(token['access_token'], token['refresh_token'])
