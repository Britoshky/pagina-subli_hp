import json
from flask import current_app as app

def load_data():
    try:
        with open('data/avisos.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    with open('data/avisos.json', 'w') as file:
        json.dump(data, file, indent=4)
