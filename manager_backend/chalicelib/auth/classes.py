"""Classes used by the Auth package."""

import datetime

from pydantic import BaseModel, EmailStr, Field

from chalicelib.auth.constants import MIN_PASSWORD_LENGTH
from chalicelib.infrastructure.classes import Key


class LoginAndRegistrationRequest(BaseModel):
    """Login and registration request."""

    email: EmailStr
    password: str = Field(min_length=MIN_PASSWORD_LENGTH)


class User(BaseModel):
    """User model."""

    email: EmailStr
    hashed_password: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserItem(User, Key):
    """DynamoDB representation of a User."""


class JWTObject(BaseModel):
    """Created and validated JWT object."""

    email: EmailStr
    iat: int
    exp: int
