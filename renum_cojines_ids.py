# Script para renumerar todos los ids de los cojines desde 1 en adelante
import json

with open('data/cojines.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

for idx, item in enumerate(items, start=1):
    item['id'] = idx

with open('data/cojines_ids_ordenados.json', 'w', encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print('Archivo guardado como cojines_ids_ordenados.json con ids consecutivos desde 1.')
