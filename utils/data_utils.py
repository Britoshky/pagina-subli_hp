import os
import json

def load_data(json_file):
    """
    Carga datos desde un archivo JSON.
    """
    if not os.path.exists(json_file):
        return []
    with open(json_file, 'r') as f:
        return json.load(f)

def save_data(json_file, data):
    """
    Guarda datos en un archivo JSON.
    """
    os.makedirs(os.path.dirname(json_file), exist_ok=True)
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)
