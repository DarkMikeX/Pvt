import importlib
import logging
import os
import sys

logger = logging.getLogger(__name__)

class PluginLoader:
    def __init__(self, plugin_dir):
        """
        Initialize the plugin loader with the directory containing plugins.

        Args:
            plugin_dir (str): Path to the plugin directory.
        """
        self.plugin_dir = plugin_dir
        self.plugins = {}

        # Add plugin_dir to sys.path to allow imports
        if self.plugin_dir not in sys.path:
            sys.path.insert(0, self.plugin_dir)

    def load_plugins(self):
        """
        Discover and import all plugins (.py files) in the plugin directory.
        Plugins must be Python files that do not start with an underscore (_).
        """
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and not filename.startswith("_"):
                mod_name = filename[:-3]
                try:
                    module = importlib.import_module(mod_name)
                    self.plugins[mod_name] = module
                    logger.info(f"Loaded plugin: {mod_name}")
                except Exception as e:
                    logger.error(f"Failed to load plugin '{mod_name}': {e}")

    def reload_plugin(self, mod_name):
        """
        Reload a specific plugin by module name.

        Args:
            mod_name (str): Plugin module name to reload.
        """
        if mod_name not in self.plugins:
            logger.warning(f"Plugin '{mod_name}' not loaded; cannot reload.")
            return
        try:
            importlib.reload(self.plugins[mod_name])
            logger.info(f"Reloaded plugin: {mod_name}")
        except Exception as e:
            logger.error(f"Failed to reload plugin '{mod_name}': {e}")

    def get_plugin(self, mod_name):
        """
        Retrieve a loaded plugin module by name.

        Args:
            mod_name (str): Plugin module name to retrieve.

        Returns:
            module or None: The imported module or None if not loaded.
        """
        return self.plugins.get(mod_name)


# Example Usage:
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)
#     loader = PluginLoader("bot/library/plugin")
#     loader.load_plugins()
#     plugin = loader.get_plugin("example_plugin")
#     loader.reload_plugin("example_plugin")
