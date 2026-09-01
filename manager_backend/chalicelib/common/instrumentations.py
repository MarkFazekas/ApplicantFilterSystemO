"""This file contains the application wide instrumentations."""

from chalice.app import RestAPIEventHandler

from chalicelib.common.exception_handler import custom_unhandled_exception_to_response


def instrument_api_event_exception_handler() -> None:
    """Instrument the chalice exception handler."""
    RestAPIEventHandler._unhandled_exception_to_response = custom_unhandled_exception_to_response  # type: ignore[method-assign]  # noqa: SLF001
