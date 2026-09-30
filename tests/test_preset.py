"""Tests for the preset system."""

from collections.abc import MutableMapping
from os import environ
from typing import Any

from model_w.env_manager import AutoPreset, ComposePreset, EnvManager, Preset


class FooPreset(Preset):
    """A preset that copies a couple of values into the context."""

    def pre(self, env: EnvManager, context: MutableMapping[str, Any]):
        """Read `FOO` from the environment."""
        context["FOO"] = env.get("FOO")

    def post(self, env: EnvManager, context: MutableMapping[str, Any]):
        """Derive `BAR` and `BONJOUR` from the context."""
        context["BAR"] = context["FOO"]
        context["BONJOUR"] = context["HELLO"]


class ContextPreset(Preset):
    """A preset that asserts on the caller's locals."""

    def pre(self, env: "EnvManager", context: MutableMapping[str, Any]):
        """The caller's locals are visible before the block runs."""
        assert context["foo"] == "yolo"

    def post(self, env: "EnvManager", context: MutableMapping[str, Any]):
        """Changes made inside the block are visible afterwards."""
        assert context["foo"] == "rofl"


class TzPreset(Preset):
    """A preset that enables timezone support."""

    def __init__(self, tz: str):
        self.tz = tz

    def post(self, env: "EnvManager", context: MutableMapping[str, Any]):
        """Set `USE_TZ` and `TIME_ZONE` in the context."""
        context["USE_TZ"] = True
        context["TIME_ZONE"] = self.tz


class I18nPreset(Preset):
    """A preset that enables i18n based on `LANGUAGES`."""

    def pre(self, env: "EnvManager", context: MutableMapping[str, Any]):
        """Enable i18n."""
        context["USE_I18N"] = True

    def post(self, env: "EnvManager", context: MutableMapping[str, Any]):
        """Default the language code to the first configured language."""
        context["LANGUAGE_CODE"] = context["LANGUAGES"][0][0]


class FooFoo(AutoPreset):
    """An auto-preset yielding values from all its `pre_*` / `post_*` methods."""

    def pre_foo(self):
        """Yield `FOO`."""
        yield "FOO", 42

    def pre_bar(self):
        """Yield `BAR`."""
        yield "BAR", 24

    def post_foo_bar(self, context: MutableMapping[str, Any]):
        """Yield `FOO_BAR` as the sum of the two previous values."""
        yield "FOO_BAR", context["FOO"] + context["BAR"]


def test_get_context():
    """The caller's locals are the context the presets operate on."""

    foo = "yolo"

    with EnvManager(ContextPreset()):
        foo = "rofl"

    assert foo == "rofl"


# noinspection PyUnusedLocal,PyPep8Naming
def test_preset():
    """A preset can read and write the caller's locals."""

    FOO = None
    BAR = None
    BONJOUR = None

    environ["FOO"] = "yolo"

    with EnvManager(FooPreset()):
        HELLO = "hello"

    assert FOO == "yolo"
    assert BAR == "yolo"
    assert BONJOUR == "hello"
    assert HELLO == "hello"


def test_doc():
    """That's roughly the example from the doc."""

    USE_I18N = None
    LANGUAGE_CODE = None
    USE_TZ = None
    TIME_ZONE = None

    with EnvManager(ComposePreset(I18nPreset(), TzPreset("UTC"))):
        LANGUAGES = [
            ("en", "English"),
            ("fr", "French"),
        ]

    assert USE_TZ is True
    assert LANGUAGE_CODE == "en"
    assert USE_I18N is True
    assert TIME_ZONE == "UTC"
    assert LANGUAGES == [("en", "English"), ("fr", "French")]


def test_auto_preset():
    """An `AutoPreset` calls all its `pre_*` and `post_*` methods."""

    FOO = None
    BAR = None
    FOO_BAR = None

    with EnvManager(FooFoo()):
        pass

    assert FOO == 42
    assert BAR == 24
    assert FOO_BAR == 66
