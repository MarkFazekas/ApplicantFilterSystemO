"""Internalization values used by the Auth package."""

from typing import Final

NON_DELIVERABLE_EMAIL: Final[str] = "This is email ({email}) is not email receiver address: {reason}"
USER_WITH_EMAIL_EXISTS: Final[str] = "User with email '{email}' already exists."
INVALID_CREDENTIALS: Final[str] = "Invalid email or password."
INVALID_OR_EXPIRED_TOKEN: Final[str] = "Invalid or expired token."  # noqa: S105
