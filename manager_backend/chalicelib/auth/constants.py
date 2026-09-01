"""Constants used by the Auth package."""

from typing import Final

# managers.py
# - PasswordManager
SALT_BYTE_COUNT: Final[int] = 16
PBKDF2_ITERATION_COUNT: Final[int] = 100_000
MIN_PASSWORD_LENGTH: Final[int] = 8
HASH_NAME: Final[str] = "sha256"
PASSWORD_PART_DELIMITER: Final[str] = "$"  # noqa: S105
HASH_PARTS_COUNT: Final[int] = 2

# - JWTManager
BEARER_PREFIX: Final[str] = "Bearer "
JWT_ALGORITHM: Final[str] = "HS256"
JWT_EXPIRATION_SECONDS: Final[int] = 3600

# db.py
PK_PREFIX: str = "USER#"
SK_METADATA: str = "METADATA"
CONDITIONAL_CHECK_FAILED: str = "ConditionalCheckFailedException"

# middleware.py
UN_AUTH_PATHS: Final[frozenset[str]] = frozenset(
    (
        "/auth/login",
        "/auth/register",
    )
)
