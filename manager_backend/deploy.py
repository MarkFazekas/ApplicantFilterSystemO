"""Run commands with environment placeholders injected into Chalice config."""

import logging
import os
import re
import subprocess
import sys
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
ENV_FILE = ROOT / ".env"
CONFIG_FILE = ROOT / ".chalice" / "config.json"

MINIMUM_ARGUMENT_COUNT = 2
COMMAND_NOT_FOUND_EXIT_CODE = 127
INTERRUPTED_EXIT_CODE = 130

PLACEHOLDER_PATTERN = re.compile(
    r"\{\{ENV\\?:([A-Za-z0-9_\\]+)\}\}",
)

LOGGER = logging.getLogger(__name__)


class EnvironmentFileNotFoundError(RuntimeError):
    """Raised when the expected environment file does not exist."""


class MissingEnvironmentVariablesError(RuntimeError):
    """Raised when required environment variables are missing."""


class ConfigFileNotFoundError(RuntimeError):
    """Raised when the Chalice configuration file does not exist."""


def load_environment() -> None:
    """Load environment variables from the local environment file."""
    if not ENV_FILE.exists():
        raise EnvironmentFileNotFoundError(ENV_FILE)

    load_dotenv(ENV_FILE, override=False)


def get_placeholder_names(config_text: str) -> set[str]:
    """Return environment variable names referenced by placeholders."""
    placeholder_names = set()

    for match in PLACEHOLDER_PATTERN.finditer(config_text):
        placeholder_name = match.group(1).replace("\\", "")
        placeholder_names.add(placeholder_name)

    return placeholder_names


def validate_environment_variables(variable_names: set[str]) -> None:
    """Ensure that all required environment variables are defined."""
    missing_names = {variable_name for variable_name in variable_names if os.environ.get(variable_name) is None}

    if missing_names:
        raise MissingEnvironmentVariablesError(
            tuple(sorted(missing_names)),
        )


def render_config(config_text: str) -> str:
    """Replace environment placeholders with loaded environment values."""
    rendered_config = config_text

    for variable_name in get_placeholder_names(config_text):
        environment_value = os.environ[variable_name]

        plain_placeholder = f"{{{{ENV:{variable_name}}}}}"
        escaped_name = variable_name.replace("_", r"\_")
        escaped_placeholder = f"{{{{ENV\\:{escaped_name}}}}}"

        rendered_config = rendered_config.replace(
            plain_placeholder,
            environment_value,
        )
        rendered_config = rendered_config.replace(
            escaped_placeholder,
            environment_value,
        )

    return rendered_config


def atomic_write(file_path: Path, config_text: str) -> None:
    """Replace a file atomically with the supplied text."""
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=file_path.parent,
        delete=False,
    ) as temporary_file:
        temporary_file.write(config_text)
        temporary_path = Path(temporary_file.name)

    temporary_path.replace(file_path)


def read_config() -> str:
    """Read and return the Chalice configuration."""
    if not CONFIG_FILE.exists():
        raise ConfigFileNotFoundError(CONFIG_FILE)

    return CONFIG_FILE.read_text(encoding="utf-8")


def execute_command(command: list[str]) -> int:
    """Execute the requested command and return its exit code."""
    LOGGER.info("Running: %s", " ".join(command))

    completed_process = subprocess.run(  # noqa: S603
        command,
        env=os.environ.copy(),
        check=False,
    )

    return completed_process.returncode


@contextmanager
def temporary_config(rendered_config: str) -> Iterator[None]:
    """Temporarily install the rendered Chalice configuration."""
    original_config = read_config()
    atomic_write(CONFIG_FILE, rendered_config)

    try:
        yield
    finally:
        atomic_write(CONFIG_FILE, original_config)


def run_with_config(command: list[str], rendered_config: str) -> int:
    """Run a command while the rendered configuration is installed."""
    with temporary_config(rendered_config):
        return execute_command(command)


def prepare_config() -> str:
    """Load environment settings and render the Chalice configuration."""
    load_environment()

    original_config = read_config()
    variable_names = get_placeholder_names(original_config)

    validate_environment_variables(variable_names)

    return render_config(original_config)


def format_error(error: Exception) -> str:
    """Return a user-friendly error description."""
    if isinstance(error, EnvironmentFileNotFoundError):
        return f"Environment file not found: {error.args[0]}"

    if isinstance(error, ConfigFileNotFoundError):
        return f"Config file not found: {error.args[0]}"

    if isinstance(error, MissingEnvironmentVariablesError):
        missing_names = ", ".join(error.args[0])
        return f"Missing environment variables: {missing_names}"

    return str(error)


def run(command: list[str]) -> int:
    """Prepare configuration and execute the requested command."""
    try:
        rendered_config = prepare_config()
    except RuntimeError:
        LOGGER.exception("Failed to prepare configuration")
        return 1

    try:
        return run_with_config(command, rendered_config)
    except FileNotFoundError:
        LOGGER.exception("Command not found: %s", command[0])
        return COMMAND_NOT_FOUND_EXIT_CODE
    except KeyboardInterrupt:
        LOGGER.exception("Command interrupted")
        return INTERRUPTED_EXIT_CODE


def main() -> int:
    """Run the deployment command wrapper."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
    )

    if len(sys.argv) < MINIMUM_ARGUMENT_COUNT:
        LOGGER.error("Usage: python deploy.py <command> [args...]")
        return 1

    return run(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
