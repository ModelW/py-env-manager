from typing import TYPE_CHECKING, Any, MutableMapping

if TYPE_CHECKING:
    from model_w.env_manager import EnvManager


class Preset:
    """
    Implement this class to have a configuration preset
    """

    def pre(self, env: "EnvManager", context: MutableMapping[str, Any]):
        """Will be run at the beginning of the context"""

    def post(self, env: "EnvManager", context: MutableMapping[str, Any]):
        """
        Will be run at the end of the context. You can use this to check what
        settings the user has set and to modify them if needed.
        """


class ComposePreset(Preset):
    """
    This helps composing different presets into one preset. Just provide them
    as arguments.
    """

    def __init__(self, *presets: Preset):
        self.presets = presets

    def pre(self, env: "EnvManager", context: MutableMapping[str, Any]):
        """
        Run all presets in order
        """

        for preset in self.presets:
            preset.pre(env, context)

    def post(self, env: "EnvManager", context: MutableMapping[str, Any]):
        """
        Run all presets in order
        """

        for preset in self.presets:
            preset.post(env, context)
