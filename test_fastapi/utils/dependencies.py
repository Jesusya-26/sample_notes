"""
FastApi dependencies are defined here.
"""
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi import Security, HTTPException, status, Depends
from keycloak import KeycloakOpenID

from test_fastapi.dto.users import User as UserDTO
from test_fastapi.config.app_settings_global import app_settings


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=app_settings.authorization_url,
    tokenUrl=app_settings.token_url,
)

# This actually does the auth checks
# client_secret_key is not mandatory if the client is public on keycloak
keycloak_openid = KeycloakOpenID(
    server_url=app_settings.server_url,  # https://sso.example.com/auth/
    client_id=app_settings.client_id,  # backend-client-id
    realm_name=app_settings.realm,  # example-realm
    client_secret_key=app_settings.client_secret,  # your backend client secret
    verify=True,
)


async def get_idp_public_key():
    return (
        "-----BEGIN PUBLIC KEY-----\n"
        f"{keycloak_openid.public_key()}"
        "\n-----END PUBLIC KEY-----"
    )


async def get_payload(token: str = Security(oauth2_scheme)) -> dict:
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


async def get_user_info(payload: dict = Depends(get_payload)) -> UserDTO:
    try:
        return UserDTO(
            id=payload.get("sub"),
            username=payload.get("user"),
            email=payload.get("email"),
            registered_at=payload.get("created_at")
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),  # "Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
