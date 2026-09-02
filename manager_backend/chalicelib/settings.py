"""Settings variables used by the application."""

import os

TABLE_NAME: str = os.environ["TABLE_NAME"]
CHECK_EMAIL_DELIVERABILITY: bool = os.environ["CHECK_EMAIL_DELIVERABILITY"].lower() == "true"
JWT_SECRET: str = os.environ["JWT_SECRET"]
