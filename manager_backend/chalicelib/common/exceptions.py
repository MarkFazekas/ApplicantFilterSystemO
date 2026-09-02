"""This file contains the common handled exceptions."""

from abc import ABC
from http import HTTPStatus

from chalicelib.common.classes import ApplicationErrorCodes, ExceptionTypes, FieldErrorDetails


class BaseAPIException(ABC, Exception):
    """This is the Base class of our exceptions."""

    default_error_type: ExceptionTypes = ExceptionTypes.APPLICATION_ERROR
    default_status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(
        self,
        detail: str,
        *,
        format_map: dict[str, str] | None = None,
        status_code: HTTPStatus | None = None,
        errors: FieldErrorDetails | None = None,
        create_log: bool = False,
    ) -> None:
        """The BaseAPIException init method, the descendant classes can call it directly.

        Args:
            detail: An error message description.
            format_map: If provided, we will format the error detail with this dictionary
            status_code: HTTP Status code of the raised error.
                If not present, we will use the default_status_code
            errors: Pydantic field level errors if it is field level.
            create_log: The exception handler will create a new ERROR level log from
                this Exception.

        Raises:
            AssertionError: If you misconfigured the parameters.
        """
        assert detail, f"{detail} must be filled."
        self.error_type = self.default_error_type
        self.status_code = status_code or self.default_status_code
        self.detail = detail
        if format_map:
            self.detail = self.detail.format_map(format_map)
        self.errors: FieldErrorDetails | None = errors or None
        self.create_log = create_log


class AFSApplicationException(BaseAPIException):
    """An error occurred at such an unplanned level that processing the request is no longer possible."""

    default_error_type = ExceptionTypes.APPLICATION_ERROR
    default_status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    default_detail = "An unexpected error occurred. Error code: {error_code}"

    def __init__(
        self,
        error_code: ApplicationErrorCodes,
    ) -> None:
        """The AFSApplicationException init method.

        Args:
            error_code: The error code of the raised error.
        """
        super().__init__(
            detail=self.default_detail,
            format_map={"error_code": error_code},
            status_code=self.default_status_code,
        )


class AFSErrorException(BaseAPIException):
    """Planned business logic-level errors."""

    default_error_type = ExceptionTypes.ERROR
    default_status_code = HTTPStatus.CONFLICT


class AFSWarningException(BaseAPIException):
    """Planned business logic-level warnings."""

    default_error_type = ExceptionTypes.WARNING
    default_status_code = HTTPStatus.CONFLICT


class AFSInformationException(BaseAPIException):
    """Planned business logic-level informational-exceptions."""

    default_error_type = ExceptionTypes.INFORMATION
    default_status_code = HTTPStatus.CONFLICT


class AFSFieldException(BaseAPIException):
    """Field level validation errors."""

    default_error_type = ExceptionTypes.VALIDATION_ERROR
    default_status_code = HTTPStatus.CONFLICT
