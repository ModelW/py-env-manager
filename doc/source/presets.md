# Presets

In the case of Django (or other) you might want to use the presets system. By
example, imagine that you're always using the same set of settings and only a
handful of values need to change from project to project. You can pack
everything into one preset and let it modify what you need.

## Preset interface

We'll be working on a simple preset that will help by enabling I18N and setting
the default language to the first language of the list.

We want to replace something like this:

```python
LANGUAGE_CODE = "en"

LANGUAGES = [
    ("en", "English"),
    ("fr", "French"),
]

USE_I18N = True
```

By something like that:

```python
from model_w.env_manager import EnvManager
from your_package.conf import I18nPreset

with EnvManager(I18nPreset()):
    LANGUAGES = [
        ("en", "English"),
        ("fr", "French"),
    ]
```

Here we suppose that `your_package` is some kind of internal package that you
share between your projects.

## Making the preset

Presets just need to implement the `Preset` interface. It simply has two hooks
(`pre` and `post`) that allow you to set configuration values from the preset.

```python
from model_w.env_manager import Preset
from typing import MutableMapping, Any

class I18nPreset(Preset):
    def pre(self, env: "EnvManager", context: MutableMapping[str, Any]):
        context['USE_I18N'] = True

    def post(self, env: "EnvManager", context: MutableMapping[str, Any]):
        context['LANGUAGE_CODE'] = context['LANGUAGES'][0][0]
```

Here in the `pre` hook we define static values while in the `post` hook we
look at what the developer put in `LANGUAGES` to define what is going to be the
default language (aka the first one of the list).

This way, you just need to set `LANGUAGES` and all I18N settings are set!

## Composing the preset

Maybe you want also to have a preset to set the time zone. Let's call it the
`TzPreset`.

```python
from model_w.env_manager import Preset
from typing import MutableMapping, Any

class TzPreset(Preset):
    def __init__(self, tz: str):
        self.tz = tz

    def post(self, env: "EnvManager", context: MutableMapping[str, Any]):
        context['USE_TZ'] = True
        context['TIME_ZONE'] = self.tz
```

Here we just set enable the time zone management and we make sure to set the
time zone to a value specified by the user.

Now how do you compose this with the other one?

```python
from model_w.env_manager import EnvManager, ComposePreset
from your_package.conf import I18nPreset, TzPreset

with EnvManager(ComposePreset(I18nPreset(), TzPreset('UTC'))):
    LANGUAGES = [
        ("en", "English"),
        ("fr", "French"),
    ]
```

## Auto Preset

Another way to split concerns is to use the `AutoPreset` helper, which will
automatically introspect your sub-class and call functions respecting a
given convention.

For example, this demo preset:

```python
from model_w.env_manager import AutoPreset

class FooFoo(AutoPreset):
    def pre_foo(self):
        yield 'FOO', 42

    def pre_bar(self):
        yield 'BAR', 24

    def post_foo_bar(self, context):
        yield 'FOO_BAR', context['FOO'] + context['BAR']
```

All you need to do is:

- Inherit from `AutoPreset`
- Put your code in methods named `pre_*` or `post_*` (based on when you want to
  execute your code)
- Yield all tuples of (key, value) that you want to define in the configuration

Optionally you can ask for `env` or `context` in your arguments and they will
be injected for you.
