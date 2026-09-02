"""This file contains the application wide exception handler."""

import logging
import sys

from chalice.app import Response, RestAPIEventHandler
from pydantic import ValidationError

from chalicelib.common.classes import ApplicationErrorCodes, FieldErrorDetails
from chalicelib.common.exceptions import AFSApplicationException, AFSFieldException, BaseAPIException


def normalize_exception(exc: BaseException | None) -> BaseAPIException:
    """Normalize the exception to our internal Specified Exception."""
    if isinstance(exc, BaseAPIException):
        normalized_exception = exc
    elif isinstance(exc, ValidationError):
        pydantic_errors = exc.errors()
        pydantic_error_count = exc.error_count()
        normalized_exception = AFSFieldException(
            detail=str(exc), errors=FieldErrorDetails(errors=pydantic_errors, error_count=pydantic_error_count)
        )
    elif isinstance(exc, KeyError):
        normalized_exception = AFSApplicationException(error_code=ApplicationErrorCodes.KEY_ERROR)
    elif isinstance(exc, ValueError):
        normalized_exception = AFSApplicationException(error_code=ApplicationErrorCodes.VALUE_ERROR)
    else:
        normalized_exception = AFSApplicationException(error_code=ApplicationErrorCodes.UNHANDLED_ERROR)

    return normalized_exception


def custom_unhandled_exception_to_response(self: RestAPIEventHandler) -> Response:
    """Custom unhandled exception handler."""
    _exc_type, exc, _traceback = sys.exc_info()

    normalized_exception = normalize_exception(exc)

    error_response_body: dict[str, str | FieldErrorDetails | None] = {
        "detail": normalized_exception.detail,
        "error_type": normalized_exception.error_type,
    }
    # If field level errors exists.
    if normalized_exception.errors:
        error_response_body["errors"] = normalized_exception.errors

    log_event = "Handled Exception Happened"
    log_level = logging.WARNING

    # If we want to explicitly create a log for this exception, we do it at ERROR level.
    if normalized_exception.create_log:
        log_event = "Logged Exception happened"
        log_level = logging.ERROR

    # Every exception that is unexpected and unplanned has to be escalated.
    if isinstance(normalized_exception, AFSApplicationException):
        log_event = "Uncaught Exception happened"
        log_level = logging.CRITICAL

    # Should be migrated to structlog and use this: getattr(self.current_request, "path", "unknown")
    self.log.log(log_level, log_event, exc_info=exc)

    return Response(body=error_response_body, status_code=normalized_exception.status_code)
