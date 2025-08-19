# Este script detecta ids duplicados en cojines.json y sugiere ids únicos
import json
from collections import Counter

with open('data/cojines.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

ids = [item['id'] for item in items]
id_counts = Counter(ids)
duplicados = [id for id, count in id_counts.items() if count > 1]

print('IDs duplicados:')
for id in duplicados:
    print(f'ID {id} aparece {id_counts[id]} veces')
    for item in items:
        if item['id'] == id:
            print(f"  - {item['name']}")

# Sugerir ids únicos para los duplicados
disponibles = set(range(1, max(ids)+len(duplicados)+10)) - set(ids)

nuevo_id = iter(disponibles)
for id in duplicados:
    first = True
    for item in items:
        if item['id'] == id:
            if first:
                first = False
                continue  # El primero se queda con el id
            item['id'] = next(nuevo_id)

with open('data/cojines_sin_duplicados.json', 'w', encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print('Archivo corregido guardado como cojines_sin_duplicados.json')
