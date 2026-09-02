"""This file contains the common classes."""

from enum import StrEnum
from typing import TypedDict

from pydantic_core import ErrorDetails


class ExceptionTypes(StrEnum):
    """The available Exception Types."""

    # Unexpected but caught errors.
    APPLICATION_ERROR = "APPLICATION_ERROR"

    # Planned business logic-level errors.
    ERROR = "ERROR"

    # Planned business logic-level warnings.
    WARNING = "WARNING"

    # Planned business logic-level information.
    INFORMATION = "INFORMATION"

    # Planned serializer-level errors.
    VALIDATION_ERROR = "VALIDATION_ERROR"


class ApplicationErrorCodes(StrEnum):
    """Unique error codes for the AFSApplicationException class."""

    # Used for unexpected and otherwise unhandled errors.
    UNHANDLED_ERROR = "UHER"

    # Used if there is a KeyError
    KEY_ERROR = "KER"

    # Used if there is a ValueError
    VALUE_ERROR = "VER"

    # Used when we do not expect the occurrence of a particular condition combination,
    #   and we are unable to assign a translated error message to it.
    UNKNOWN_OUTPUT = "UNOT"


class FieldErrorDetails(TypedDict):
    """The field error details."""

    errors: list[ErrorDetails]
    error_count: int
