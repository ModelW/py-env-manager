"""Tests for `EnvManager` default handling and error reporting."""

from os import environ

import pytest

from model_w.env_manager import EnvManager
from model_w.env_manager._exceptions import ImproperlyConfigured
from model_w.env_manager._manager import no_default


def _missing_build_default() -> None:
    with EnvManager() as env:
        assert "A_B_C_D_E_F_G_H" not in environ
        assert "BUILD_MODE" not in environ
        assert not env.get("A_B_C_D_E_F_G_H", build_default="foo")


def test_default():
    """A missing variable that only has a build default raises at exit."""

    with pytest.raises(ImproperlyConfigured):
        _missing_build_default()


def test_no_default():
    """The `no_default` singleton is falsy and renders as `no_default`."""

    assert no_default.__repr__() == "no_default"
    assert repr(no_default) == "no_default"

    assert no_default.__bool__() is False
    assert not no_default

    assert no_default == no_default


def _mismatching_signatures() -> None:
    with EnvManager() as env:
        env.get("FOO", default="foo")
        env.get("FOO", default="foo", is_yaml=True)


def test_signature_mismatch():
    """Calling `get()` twice with different signatures raises at exit."""

    with pytest.raises(ImproperlyConfigured):
        _mismatching_signatures()
