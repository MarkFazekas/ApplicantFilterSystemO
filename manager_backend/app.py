import uuid
from typing import TYPE_CHECKING, cast

from chalice import Chalice  # type: ignore[attr-defined]

from chalicelib.infrastructure import db

if TYPE_CHECKING:
    from chalice.app import Request
    from types_boto3_dynamodb.type_defs import ScanOutputTableTypeDef

app = Chalice(app_name="manager_backend")
app.debug = True


@app.route("/")
def index() -> dict[str, ScanOutputTableTypeDef]:
    """Asd."""
    return {"table": db.get_table().scan()}


@app.route("/hello/{name}")
def hello_name(name: str) -> dict[str, str]:
    """Asd."""
    return {"hello": name}


@app.route("/users", methods=["POST"])
def create_user() -> dict[str, str]:
    """Asd."""
    user_as_json = cast("Request", app.current_request).json_body
    db.get_table().put_item(Item={"pk": f"uuid#{uuid.uuid4()}", "sk": f"uuid#{uuid.uuid4()}", **user_as_json})
    return {"user": user_as_json}
