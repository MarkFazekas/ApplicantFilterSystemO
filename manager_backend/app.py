"""Entry point for the backend app."""

from chalice.app import Chalice

from chalicelib.auth.middleware import auth_middleware
from chalicelib.auth.routes import auth_routes
from chalicelib.common.instrumentations import instrument_api_event_exception_handler

instrument_api_event_exception_handler()
app = Chalice(app_name="manager_backend")
app.register_blueprint(auth_routes, name_prefix="auth", url_prefix="/auth")
app.register_blueprint(auth_middleware, name_prefix="auth")
