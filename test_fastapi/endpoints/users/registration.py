"""
Registration endpoint is defined here.
"""
from starlette import status

from test_fastapi.logic.users import register
from test_fastapi.schemas.basic_responses import OkResponse
from test_fastapi.schemas.users import RegistrationRequest

from .router import user_data_router


@user_data_router.post("/register", status_code=status.HTTP_200_OK)
async def register_user(
    registration_request: RegistrationRequest
) -> OkResponse:
    """
    Registers user by given email, name and password if they are all valid and no user with such email or name exist.
    """
    await register(registration_request.username, registration_request.email, registration_request.password)
    return OkResponse()
