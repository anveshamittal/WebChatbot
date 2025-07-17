import yaml
from pathlib import Path

class AppConfig:
    """
    A singleton class to load and provide access to the application configuration.
    It reads the settings.yaml file only once.
    """
    _instance = None
    _config_data = {}

    def __new__(cls):
        # This makes sure we only ever create one instance of this class (singleton pattern)
        if cls._instance is None:
            cls._instance = super(AppConfig, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """Finds and loads the settings.yaml file into memory."""
        try:
            # Get the path to settings.yaml relative to this file
            config_path = Path(__file__).parent.parent / "config" / "settings.yaml"
            with open(config_path, "r") as f:
                self._config_data = yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found at: {config_path}")
        except yaml.YAMLError as e:
            raise IOError(f"Error parsing YAML file: {e}")

    def _get_section(self, section_name: str):
        """A helper to safely get a top-level section from the config."""
        if not self._config_data:
            self._load_config()
        
        section = self._config_data.get(section_name)
        if section is None:
            raise KeyError(f"'{section_name}' section not found in settings.yaml")
        return section

    @property
    def chunking(self) -> dict:
        return self._get_section('chunking')

    @property
    def embedding(self) -> dict:
        return self._get_section('embedding')

    @property
    def azure(self) -> dict:
        return self._get_section('azure')

    @property
    def files(self) -> dict:
        return self._get_section('files')