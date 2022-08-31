from os import environ
from typing import Any, MutableMapping

from model_w.env_manager import AutoPreset, ComposePreset, EnvManager, Preset


class FooPreset(Preset):
    def pre(self, env: EnvManager, context: MutableMapping[str, Any]):
        context["FOO"] = env.get("FOO")

    def post(self, env: EnvManager, context: MutableMapping[str, Any]):
        context["BAR"] = context["FOO"]
        context["BONJOUR"] = context["HELLO"]


class ContextPreset(Preset):
    def pre(self, env: "EnvManager", context: MutableMapping[str, Any]):
        assert context["foo"] == "yolo"

    def post(self, env: "EnvManager", context: MutableMapping[str, Any]):
        assert context["foo"] == "rofl"


class TzPreset(Preset):
    def __init__(self, tz: str):
        self.tz = tz

    def post(self, env: "EnvManager", context: MutableMapping[str, Any]):
        context["USE_TZ"] = True
        context["TIME_ZONE"] = self.tz


class I18nPreset(Preset):
    def pre(self, env: "EnvManager", context: MutableMapping[str, Any]):
        context["USE_I18N"] = True

    def post(self, env: "EnvManager", context: MutableMapping[str, Any]):
        context["LANGUAGE_CODE"] = context["LANGUAGES"][0][0]


class FooFoo(AutoPreset):
    def pre_foo(self):
        yield "FOO", 42

    def pre_bar(self):
        yield "BAR", 24

    def post_foo_bar(self, context: MutableMapping[str, Any]):
        yield "FOO_BAR", context["FOO"] + context["BAR"]


def test_get_context():
    foo = "yolo"  # noqa

    with EnvManager(ContextPreset()):
        foo = "rofl"  # noqa


# noinspection PyUnusedLocal,PyPep8Naming
def test_preset():
    FOO = None
    BAR = None
    BONJOUR = None

    environ["FOO"] = "yolo"

    with EnvManager(FooPreset()) as env:
        HELLO = "hello"

    assert FOO == "yolo"
    assert BAR == "yolo"
    assert BONJOUR == "hello"
    assert HELLO == "hello"


def test_doc():
    """
    That's roughly the example from the doc
    """

    USE_I18N = None
    LANGUAGE_CODE = None
    USE_TZ = None
    TIME_ZONE = None

    with EnvManager(ComposePreset(I18nPreset(), TzPreset("UTC"))):
        LANGUAGES = [
            ("en", "English"),
            ("fr", "French"),
        ]

    assert USE_TZ == True
    assert LANGUAGE_CODE == "en"
    assert USE_I18N == True
    assert TIME_ZONE == "UTC"


def test_auto_preset():
    FOO = None
    BAR = None
    FOO_BAR = None

    with EnvManager(FooFoo()):
        pass

    assert FOO == 42
    assert BAR == 24
    assert FOO_BAR == 66
