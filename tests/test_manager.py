from os import environ

from pytest import raises

from model_w.env_manager import EnvManager
from model_w.env_manager._exceptions import ImproperlyConfigured  # noqa
from model_w.env_manager._manager import no_default  # noqa


def test_default():
    with raises(ImproperlyConfigured):
        with EnvManager() as env:
            assert "A_B_C_D_E_F_G_H" not in environ
            assert "BUILD_MODE" not in environ
            assert not env.get("A_B_C_D_E_F_G_H", build_default="foo")


def test_no_default():
    assert no_default.__repr__() == "no_default"
    assert repr(no_default) == "no_default"

    assert no_default.__bool__() is False
    assert not no_default
