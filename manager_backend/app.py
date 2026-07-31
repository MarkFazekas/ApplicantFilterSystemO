import uuid
from typing import TYPE_CHECKING, cast

import boto3
from chalice import Chalice  # type: ignore[attr-defined]

if TYPE_CHECKING:
    from chalice.app import Request
    from types_boto3_dynamodb.type_defs import ScanOutputTableTypeDef

app = Chalice(app_name="manager_backend")
app.debug = True

table = boto3.resource("dynamodb").Table("ApplicantFilterSystemDev")


@app.route("/")
def index() -> dict[str, ScanOutputTableTypeDef]:
    """Asd."""
    return {"table": table.scan()}


@app.route("/hello/{name}")
def hello_name(name: str) -> dict[str, str]:
    """Asd."""
    return {"hello": name}


@app.route("/users", methods=["POST"])
def create_user() -> dict[str, str]:
    """Asd."""
    user_as_json = cast("Request", app.current_request).json_body
    table.put_item(Item={"pk": f"uuid#{uuid.uuid4()}", "sk": f"uuid#{uuid.uuid4()}", **user_as_json})
    return {"user": user_as_json}
