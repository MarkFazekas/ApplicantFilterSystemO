"""Manager classes used by the Auth package."""

import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta

import jwt
from email_validator import EmailNotValidError, validate_email
from pydantic import ValidationError

from chalicelib import settings
from chalicelib.auth.classes import JWTObject
from chalicelib.auth.constants import (
    BEARER_PREFIX,
    HASH_NAME,
    HASH_PARTS_COUNT,
    JWT_ALGORITHM,
    JWT_EXPIRATION_SECONDS,
    PASSWORD_PART_DELIMITER,
    PBKDF2_ITERATION_COUNT,
    SALT_BYTE_COUNT,
)
from chalicelib.auth.i18n import NON_DELIVERABLE_EMAIL
from chalicelib.common.exceptions import AFSErrorException
from chalicelib.constants import ENCODING


class EmailValidatorManager:
    """Email validation manager using email-validator."""

    @classmethod
    def validate_email(
        cls,
        email: str,
    ) -> None:
        """Validate email address deliverability if needed.

        Args:
            email: The email address string to validate.

        Raises:
            ValueError: If the email address is empty, not a string, or invalid.
        """
        try:
            validate_email(
                email,
                check_deliverability=settings.CHECK_EMAIL_DELIVERABILITY,
            )
        except EmailNotValidError as exc:
            raise AFSErrorException(
                NON_DELIVERABLE_EMAIL,
                format_map={
                    "email": email,
                    "reason": str(exc),
                },
            ) from exc


class PasswordManager:
    """Password hashing, verification manager."""

    @classmethod
    def hash_password(cls, password: str) -> str:
        """Hash a plaintext password using PBKDF2-HMAC-SHA256 with a salt.

        Args:
            password: The plaintext password to hash.

        Returns:
            A string formatted as salt$hash.
        """
        salt = secrets.token_hex(SALT_BYTE_COUNT)
        derived = hashlib.pbkdf2_hmac(
            HASH_NAME,
            password.encode(ENCODING),
            salt.encode(ENCODING),
            PBKDF2_ITERATION_COUNT,
        )
        return f"{salt}{PASSWORD_PART_DELIMITER}{derived.hex()}"

    @classmethod
    def verify_password(cls, password: str, hashed_password: str) -> bool:
        """Verify a plaintext password against a stored hashed password.

        Args:
            password: The plaintext password to verify.
            hashed_password: The stored hashed password in salt$hash format.

        Returns:
            True if the password matches the hash, False otherwise.
        """
        if not password or not hashed_password:
            return False

        parts = hashed_password.split(PASSWORD_PART_DELIMITER, 1)
        if len(parts) != HASH_PARTS_COUNT:
            return False

        salt, expected_hex = parts
        derived = hashlib.pbkdf2_hmac(
            HASH_NAME,
            password.encode(ENCODING),
            salt.encode(ENCODING),
            PBKDF2_ITERATION_COUNT,
        )
        return hmac.compare_digest(derived.hex(), expected_hex)


class JWTManager:
    """JSON Web Token manager for token creation and verification."""

    @classmethod
    def create_access_token(
        cls,
        email: str,
        *,
        duration: int = JWT_EXPIRATION_SECONDS,
    ) -> str:
        """Create a signed JSON Web Token (JWT).

        Args:
            email: The user's email.
            duration: Lifetime of the token in seconds. Defaults to 3600 (1 hour).

        Returns:
            A signed JWT token string.
        """
        issued_at = datetime.now(UTC)
        issued_at_timestamp = int(issued_at.timestamp())
        expires_at = issued_at + timedelta(seconds=duration)
        expires_at_timestamp = int(expires_at.timestamp())

        jwt_value = JWTObject(email=email, iat=issued_at_timestamp, exp=expires_at_timestamp)

        encoded_token: str = jwt.encode(
            jwt_value.model_dump(),
            settings.JWT_SECRET,
            algorithm=JWT_ALGORITHM,
        )
        return encoded_token

    @classmethod
    def decode_access_token(cls, token: str) -> JWTObject | None:
        """Decode and validate a JWT access token.

        Args:
            token: The JWT string to decode, optionally prefixed with 'Bearer '.

        Returns:
            The decoded payload dictionary if valid, or None if the token is invalid or expired.
        """
        clean_token = token.strip()
        prefix_length = len(BEARER_PREFIX)
        if clean_token.startswith(BEARER_PREFIX):
            clean_token = clean_token[prefix_length:].strip()

        if not clean_token:
            return None

        try:
            payload = jwt.decode(
                clean_token,
                settings.JWT_SECRET,
                algorithms=[JWT_ALGORITHM],
            )
            return JWTObject.model_validate(payload)
        except (jwt.PyJWTError, ValidationError):
            return None
