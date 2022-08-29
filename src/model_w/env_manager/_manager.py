from io import StringIO
from os import environ
from pathlib import Path
from typing import Any, Optional, Union

from yaml import YAMLError, safe_load

from ._dotenv import load_dotenv
from ._exceptions import ImproperlyConfigured

no_default = object()


class EnvManager:
    """
    Allows to manage the loading of environment variables from the settings:

    - Auto-parse of YAML values for non-string config
    - Reporting missing/incorrect values

    Use it like this from settings.py

    >>> with EnvManager() as env:
    >>>     FOO_BAR = env.get('FOO_BAR', is_yaml=True)

    During Docker (or other) builds, some Django commands need to be run,
    however at that time environment variables are inaccessible. In order to
    be still able to run some commands, knowing than anything else than
    collectstatic won't be called, there is a build mode which enables to
    have different default values for variables. All you need to do to enable
    the build mode is set BUILD_MODE=yes (or the configured variable name, cf
    the constructor parameters).
    """

    def __init__(
        self,
        dotenv_path: Union[str, Path, None, bool] = None,
        assume_yaml: bool = False,
        build_mode_var: str = "BUILD_MODE",
    ) -> None:
        """
        Constructs the object

        Parameters
        ----------
        dotenv_path
            Optional path to the .env to load before going further.
                - If set to a path, this path will be loaded
                - If set to None, the path will be auto-detected
                - If set to False, no .env loading will be intended
        assume_yaml
            If set to True, all variables will be implicitly considered to be
            YAML, unless stated otherwise during get() calls
        build_mode_var
            When in build mode, variable values fall back to the build
            defaults, which are not the regular defaults. This gives the name
            if the (YAML-parsed) environment variable which indicates that we
            are in build mode.
        """

        self.dotenv_path = dotenv_path
        self.assume_yaml = assume_yaml
        self.build_mode_var = build_mode_var
        self.missing = set()
        self.syntax_error = set()
        self.read = {}

    def __enter__(self):
        """
        When entering the context, the .env file is automatically loaded
        """

        self.load_dotenv()
        return self

    def __exit__(self, *_):
        """
        Upon exit, if any value failed to be configured then raise an error
        listing all that is wrong.
        """

        self.raise_parse_fail()

    @property
    def in_build_mode(self):
        try:
            return bool(safe_load(StringIO(environ[self.build_mode_var])))
        except (YAMLError, KeyError):
            return None

    def load_dotenv(self) -> None:
        """
        If a dotenv path was specified then attempt to load it.
        """

        if self.dotenv_path is not False:
            load_dotenv(self.dotenv_path)

    def get(
        self,
        name: str,
        default: Any = no_default,
        build_default: Any = no_default,
        is_yaml: Optional[bool] = None,
    ) -> Any:
        """
        Gets a configured value

        Parameters
        ----------
        name
            Name of the variable you want to get
        default
            Default value to be returned. The special "no_default" value
            indicates that there is no default, thus making this variable
            mandatory
        build_default
            Default value when in build mode
        is_yaml
            Enables YAML parsing of the value
        """

        if is_yaml is None:
            is_yaml = self.assume_yaml

        current_default = (
            build_default
            if self.in_build_mode and build_default is not no_default
            else default
        )

        self.read[name] = dict(
            is_yaml=is_yaml,
            is_required=current_default is no_default,
        )

        if name not in environ:
            if current_default is no_default:
                self.missing.add(name)

            return current_default

        if is_yaml:
            try:
                value = safe_load(StringIO(environ[name]))
            except YAMLError:
                self.syntax_error.add(name)
                return None
        else:
            value = environ[name]

        return value

    def raise_parse_fail(self):
        """
        If during the lifetime of this object some values were missing or had
        incorrect syntax then this will raise an exception to signify so.
        """

        if self.get("NO_ENV_CHECK", is_yaml=True, default=False):
            return

        if not self.missing and not self.syntax_error:
            return

        parts = ["Incorrect environment variables."]

        if self.missing:
            parts.append(f' Missing: {", ".join(self.missing)}.')

        if self.syntax_error:
            parts.append(f' Syntax error: {", ".join(self.missing)}.')

        raise ImproperlyConfigured("".join(parts))
