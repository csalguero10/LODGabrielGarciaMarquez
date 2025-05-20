import csv

def get_unique_entities_from_csv(file_path):
    entities_set = set()

    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            entity = row.get('Entities')
            if entity:
                entities_set.add(entity.strip())

    return tuple(entities_set)

# Ejemplo de uso
file_path = 'conversions/Entities.csv'  # Reemplaza con la ruta a tu archivo
unique_entities = get_unique_entities_from_csv(file_path)

# Mostrar el contenido del set
print("Entities únicas encontradas:")
for p in sorted(unique_entities):
    print(p)
