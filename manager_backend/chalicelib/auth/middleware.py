"""Auth package middlewares."""

from collections.abc import Callable
from typing import TYPE_CHECKING

from chalice.app import Blueprint, Request, Response

from chalicelib.auth.constants import UN_AUTH_PATHS
from chalicelib.auth.i18n import INVALID_OR_EXPIRED_TOKEN
from chalicelib.auth.managers import JWTManager
from chalicelib.common.exceptions import AFSErrorException

if TYPE_CHECKING:
    from chalicelib.auth.classes import JWTObject

auth_middleware = Blueprint(__name__)


@auth_middleware.middleware("http")
def check_auth_token(event: Request, get_response: Callable[[Request], Response]) -> Response:
    """This middleware is responsible for checking authorization token for the auth endpoints."""
    path = event.path
    if path not in UN_AUTH_PATHS:
        token = event.headers.get("Authorization", "")
        validated: JWTObject | None = JWTManager.decode_access_token(token=token)
        if not validated:
            raise AFSErrorException(INVALID_OR_EXPIRED_TOKEN)

        event.context["token"] = validated

    return get_response(event)
