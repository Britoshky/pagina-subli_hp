import os
import json

ADS_FILE = "data/avisos.json"  # Define la ruta constante para el archivo JSON

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

def load_ads():
    try:
        if not os.path.exists(ADS_FILE):
            return []
        with open(ADS_FILE, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error cargando el archivo JSON: {e}")
        return []

def save_ads(data):
    try:
        os.makedirs(os.path.dirname(ADS_FILE), exist_ok=True)
        with open(ADS_FILE, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error guardando el archivo JSON: {e}")
