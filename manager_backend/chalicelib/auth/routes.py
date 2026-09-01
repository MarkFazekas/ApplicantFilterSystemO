"""Authentication routes providing registration and login endpoints."""

import datetime
from functools import partial
from http import HTTPStatus

from chalice.app import Blueprint, Response

from chalicelib.auth.classes import LoginAndRegistrationRequest, User, UserItem
from chalicelib.auth.constants import JWT_EXPIRATION_SECONDS
from chalicelib.auth.db import create_user, get_user_by_email
from chalicelib.auth.i18n import INVALID_CREDENTIALS
from chalicelib.auth.managers import EmailValidatorManager, JWTManager, PasswordManager
from chalicelib.common.exceptions import AFSErrorException
from chalicelib.common.functions import get_user_token, serialize_request

auth_routes = Blueprint(__name__)
serialize = partial(serialize_request, auth_routes)
get_token = partial(get_user_token, auth_routes)


@auth_routes.route("/register", methods=["POST"])
def register() -> Response:
    """Register a new user with email and password.

    Returns:
        A Response object indicating registration outcome.
    """
    request: LoginAndRegistrationRequest = serialize(LoginAndRegistrationRequest)
    EmailValidatorManager.validate_email(request.email)
    hashed_password = PasswordManager.hash_password(request.password)
    now = datetime.datetime.now(datetime.UTC)
    user = User(email=request.email, hashed_password=hashed_password, created_at=now, updated_at=now)

    user_info = create_user(user)

    return Response(
        body={"email": user_info.email},
        status_code=HTTPStatus.CREATED,
    )


@auth_routes.route("/login", methods=["POST"])
def login() -> Response:
    """Authenticate user with email and password, returning a JWT token.

    Returns:
        A Response object containing JWT token or error message.
    """
    request: LoginAndRegistrationRequest = serialize(LoginAndRegistrationRequest)
    user: UserItem | None = get_user_by_email(email=request.email)
    if not user:
        raise AFSErrorException(INVALID_CREDENTIALS)

    verified = PasswordManager.verify_password(request.password, user.hashed_password)
    if not verified:
        raise AFSErrorException(INVALID_CREDENTIALS)

    token = JWTManager.create_access_token(email=user.email)

    return Response(
        body={
            "access_token": token,
            "token_type": "Bearer",
            "expires_in": JWT_EXPIRATION_SECONDS,
        },
        status_code=HTTPStatus.OK,
    )


@auth_routes.route("/me")
def me() -> Response:
    """Check the current logged-in user."""
    token = get_token()
    return Response(body={"message": "protected", "user": token.email}, status_code=HTTPStatus.OK)
