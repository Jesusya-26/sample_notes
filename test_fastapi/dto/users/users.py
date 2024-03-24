"""
User DTO is defined here.
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class User:
    """
    Full User data transfer object, but without password_hash.
    """

    id: str
    username: str
    email: str
    registered_at: datetime

    def __str__(self) -> str:
        return f"(id={self.id}, username: {self.username}"
