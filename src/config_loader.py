import yaml
import os

yaml_config=os.path.abspath(os.path.join(os.path.dirname(__file__), '../config/settings.yaml'))

def chunking_config():
    with open(yaml_config,'r') as file:
        config= yaml.safe_load(file)
        chunk_config = config['chunking']
        return {'chunk_size':chunk_config["chunk_size"],'chunk_overlap': chunk_config["chunk_overlap"]}

def embedding_config():
    with open(yaml_config,'r') as file:
        config= yaml.safe_load(file)
        embedding_config = config['embedding']
        return {'embedding_model':embedding_config["embedding_model"]}