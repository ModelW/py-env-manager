"""Tests for `.env` file discovery and loading."""

from os import environ
from pathlib import Path
from tempfile import NamedTemporaryFile

from model_w.env_manager import EnvManager
from model_w.env_manager._dotenv import find_dotenv


def test_load():
    """A `set -a` line is ignored and the values are parsed and exported."""

    with NamedTemporaryFile("w") as f:
        f.write("set -a\nFOO_BAR_BAZ=42\n")
        f.flush()

        with EnvManager(dotenv_path=f.name) as env:
            fbb = env.get("FOO_BAR_BAZ", is_yaml=True)
            assert fbb == 42

            assert environ["FOO_BAR_BAZ"] == "42"


def test_find_dotenv():
    """`find_dotenv` locates a sibling dotenv file by walking the stack."""

    assert find_dotenv("dotenv.txt") == Path(__file__).parent / "dotenv.txt"
