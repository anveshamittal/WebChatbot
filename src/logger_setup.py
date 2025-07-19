import yaml
import logging.config
from pathlib import Path

def setup_logging():
    """
    Loads the logging configuration from the YAML file.
    This should be called only once when the application starts.
    """
    config_file = Path(__file__).parent.parent / "config" / "logging_config.yaml"
    
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    
    logger = logging.getLogger(__name__)
    logger.info("Logging has been configured.")