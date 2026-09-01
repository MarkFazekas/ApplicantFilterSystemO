"""User management and authentication service for DynamoDB single-table design."""

from typing import Any

from botocore.exceptions import ClientError

from chalicelib.auth.classes import User, UserItem
from chalicelib.auth.constants import CONDITIONAL_CHECK_FAILED, PK_PREFIX, SK_METADATA
from chalicelib.auth.i18n import USER_WITH_EMAIL_EXISTS
from chalicelib.common.exceptions import AFSErrorException
from chalicelib.infrastructure.classes import Key
from chalicelib.infrastructure.db import get_table


def build_user_pk(email: str) -> str:
    """Build the DynamoDB partition key for a user.

    Args:
        email: The normalized user email.

    Returns:
        The partition key string.
    """
    return f"{PK_PREFIX}{email}"


def create_user(user: User) -> UserItem:
    """Register a new user in DynamoDB.

    Args:
        user: The user object.

    Returns:
        A dictionary containing user details.

    Raises:
        ValueError: If email or password is invalid.
        UserAlreadyExistsError: If a user with the given email already exists.
    """
    target_table = get_table()

    user_item = UserItem(
        pk=build_user_pk(user.email),
        sk=SK_METADATA,
        **user.model_dump(),
    )

    try:
        target_table.put_item(
            Item=user_item.model_dump(mode="json"),
            ConditionExpression="attribute_not_exists(pk)",
        )
    except ClientError as exc:
        error_code = exc.response.get("Error", {}).get("Code")
        if error_code == CONDITIONAL_CHECK_FAILED:
            raise AFSErrorException(detail=USER_WITH_EMAIL_EXISTS, format_map={"email": user.email}) from exc
        raise

    return user_item


def get_user_by_email(
    email: str,
) -> UserItem | None:
    """Retrieve a user item from DynamoDB by email.

    Args:
        email: The user email address.

    Returns:
        The user item dictionary if found, or None.
    """
    target_table = get_table()
    key = Key(pk=build_user_pk(email), sk=SK_METADATA)
    response = target_table.get_item(Key=key.model_dump(mode="json"))
    user_data: dict[str, Any] | None = response.get("Item")
    if user_data is None:
        return None
    return UserItem.model_validate(user_data)
