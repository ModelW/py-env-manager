from os import environ
from pathlib import Path
from tempfile import NamedTemporaryFile

from model_w.env_manager import EnvManager
from model_w.env_manager._dotenv import find_dotenv  # noqa


def test_load():
    with NamedTemporaryFile("w") as f:
        f.write("set -a\nFOO_BAR_BAZ=42\n")
        f.flush()

        with EnvManager(dotenv_path=f.name) as env:
            fbb = env.get("FOO_BAR_BAZ")
            assert fbb == "42"

            fbb = env.get("FOO_BAR_BAZ", is_yaml=True)
            assert fbb == 42

            assert environ["FOO_BAR_BAZ"] == "42"


def test_find_dotenv():
    assert find_dotenv("dotenv.txt") == Path(__file__).parent / "dotenv.txt"
