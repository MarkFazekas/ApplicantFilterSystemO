from typing import TYPE_CHECKING, cast

from chalice import Chalice  # type: ignore[attr-defined]

if TYPE_CHECKING:
    from chalice.app import Request

app = Chalice(app_name="manager_backend")
app.debug = True

@app.route("/")
def index() -> dict[str, str]:
    """Asd."""
    return {"hello": "world"}


@app.route("/hello/{name}")
def hello_name(name: str) -> dict[str, str]:
    """Asd."""
    return {"hello": name}


@app.route("/users", methods=["POST"], content_types=["text/plain"])
def create_user() -> dict[str, str]:
    """Asd."""
    user_as_json = cast("Request", app.current_request).raw_body
    return {"user": user_as_json}


@app.route("/cities/{city}")
def state_of_city(city: str) -> dict[str, str]:
    """Asd."""
    cities_to_state = {
        "seattle": "WA",
        "portland": "OR",
    }

    return {"state": cities_to_state[city]}
