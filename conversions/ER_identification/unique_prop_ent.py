import csv

def get_unique_values_from_csv(file_path, column_name):
    values_set = set()

    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            value = row.get(column_name)
            if value:
                values_set.add(value.strip())

    return sorted(values_set)

def save_combined_to_csv(entities, properties, output_file):
    max_len = max(len(entities), len(properties))
    # Rellenar con cadenas vacías para que tengan la misma longitud
    entities += [""] * (max_len - len(entities))
    properties += [""] * (max_len - len(properties))

    with open(output_file, mode='w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Entity', 'Property'])  # Cabeceras
        for entity, prop in zip(entities, properties):
            writer.writerow([entity, prop])

# Rutas de los archivos de entrada
entities_file = 'conversions/ER_identification/Entities.csv'
properties_file = 'conversions/ER_identification/Properties.csv'
output_file = 'conversions/ER_identification/tot_entities_properties.csv'

# Obtener valores únicos
unique_entities = get_unique_values_from_csv(entities_file, 'Entities')
unique_properties = get_unique_values_from_csv(properties_file, 'Properties')

# Guardar en un único archivo CSV combinado
save_combined_to_csv(unique_entities, unique_properties, output_file)

print(f"Archivo combinado guardado con {len(unique_entities)} entidades y {len(unique_properties)} propiedades en '{output_file}'")
