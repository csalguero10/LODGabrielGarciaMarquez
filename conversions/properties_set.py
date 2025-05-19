import pandas as pd

# Leer el archivo CSV
df = pd.read_csv("conversions/Properties.csv")  # Reemplaza con el nombre de tu archivo

# Crear un set vacío
unique_properties = set()

# Iterar la columna "properties" y agregar al set
for prop in df["Properties"]:
    unique_properties.add(prop.strip())  # Elimina espacios extra si los hay

# Mostrar el contenido del set
print("Propiedades únicas encontradas:")
for p in sorted(unique_properties):
    print(p)
