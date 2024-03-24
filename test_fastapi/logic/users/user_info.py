from fastapi import HTTPException, status
from datetime import datetime

from test_fastapi.dto.users import User as UserDTO


async def get_user_info(user_id: str, username: str, email: str, created_at: datetime) -> UserDTO:
    try:
        return UserDTO(
            id=user_id,
            username=username,
            email=email,
            registered_at=created_at
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),  # "Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )