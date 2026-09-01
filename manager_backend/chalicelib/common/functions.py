"""This file contains the serializer related functions."""

from chalice.app import Blueprint
from pydantic import BaseModel

from chalicelib.auth.classes import JWTObject
from chalicelib.auth.i18n import INVALID_OR_EXPIRED_TOKEN
from chalicelib.common.exceptions import AFSErrorException


def serialize_request[ModelType: BaseModel](blueprint: Blueprint, model: type[ModelType]) -> ModelType:
    """Serialize a request model to JSON.

    Args:
        blueprint: The used Blueprint.
        model: The model being serialized.

    Returns:
        The serialized request.
    """
    return model.model_validate_json(blueprint.current_request.raw_body)


def get_user_token(blueprint: Blueprint) -> JWTObject:
    """Returns the validated JWT token for an authenticated user.

    Args:
        blueprint: The used Blueprint.

    Returns:
        The validated JWT token.
    """
    token: JWTObject | None = blueprint.current_request.context.get("token")
    if not token:
        raise AFSErrorException(INVALID_OR_EXPIRED_TOKEN)
    return token
