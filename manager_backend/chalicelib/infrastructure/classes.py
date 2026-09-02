"""This file contains the infrastructure classes."""

from pydantic import BaseModel


class Key(BaseModel):
    """Model used to represent a DynamoDB Key Resource."""

    pk: str
    sk: str
