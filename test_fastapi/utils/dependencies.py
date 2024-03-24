"""
FastApi dependencies are defined here.
"""
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from keycloak import KeycloakOpenID

from test_fastapi.logic.users.user_info import get_user_info
from test_fastapi.dto.users import User as UserDTO
from test_fastapi.config.app_settings_global import app_settings


keycloak_openid = KeycloakOpenID(
    server_url=app_settings.server_url,
    client_id=app_settings.client_id,
    realm_name=app_settings.realm,
    client_secret_key=app_settings.client_secret,
    verify=True,
)


async def get_idp_public_key():
    return (
        "-----BEGIN PUBLIC KEY-----\n"
        f"{keycloak_openid.public_key()}"
        "\n-----END PUBLIC KEY-----"
    )


async def access_token_dependency(token: OAuth2PasswordBearer(tokenUrl="/api/login") = Depends()) -> dict:
    try:
        return keycloak_openid.decode_token(
            token,
            key=await get_idp_public_key(),
            options={
                "verify_signature": True,
                "verify_aud": False,
                "exp": True
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),  # "Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def user_dependency(
    access_token: dict = Depends(access_token_dependency)
) -> UserDTO:
    """
    Return user fetched from the database by email from a validated access token.

    Ensures that User is approved to log in and valid.
    """
    print(type(access_token.get('sub')))
    print(type(access_token.get('created_at')))
    return await get_user_info(access_token.get('sub'), access_token.get('username'),
                               access_token.get('email'), access_token.get('created_at'))
