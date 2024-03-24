"""
Registration logic is defined here.
"""
from loguru import logger
from keycloak import KeycloakAdmin

from test_fastapi.config.app_settings_global import app_settings


async def register(username: str, email: str, password: str) -> None:
    """
    Register a user if the given email, login and password if email and login are both available.
    """

    admin = KeycloakAdmin(
            server_url=app_settings.server_url,
            username=app_settings.keycloak_admin,
            password=app_settings.keycloak_admin_sercet,
            realm_name=app_settings.realm,
            user_realm_name=app_settings.realm)

    admin.create_user({"email": email,
                       "username": username,
                       "enabled": True,
                       "credentials": [{"value": password, "type": "password", }]},
                      exist_ok=False)

    logger.info("Registered user {}", username)

