from functools import cache

import boto3
from types_boto3_dynamodb.service_resource import DynamoDBServiceResource, Table

from chalicelib import settings

dynamodb: DynamoDBServiceResource = boto3.resource("dynamodb")


@cache
def get_table() -> Table:
    """Return with an AWS DynamoDB Table Resource."""
    return dynamodb.Table(settings.TABLE_NAME)
