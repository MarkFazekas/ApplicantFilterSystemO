from functools import cache
from typing import TYPE_CHECKING

import boto3

from chalicelib import settings

if TYPE_CHECKING:
    from types_boto3_dynamodb.service_resource import DynamoDBServiceResource, Table

dynamodb: DynamoDBServiceResource = boto3.resource("dynamodb")


@cache
def get_table() -> Table:
    """Return with an AWS DynamoDB Table Resource."""
    return dynamodb.Table(settings.TABLE_NAME)
