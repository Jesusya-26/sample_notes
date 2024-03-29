"""
Authorization logic is defined here.
"""
from test_fastapi.dto.users import TokensTuple
from test_fastapi.utils.dependencies import keycloak_openid


async def get_token(username: str, password: str) -> TokensTuple:
    """
    Returns an access and refresh tokens for a user if user with given login (email or name)"
        exists and password hash matched
    """

    token = keycloak_openid.token(username, password)

    return TokensTuple(token['access_token'], token['refresh_token'])
