import unicodedata
import re

# Función para normalizar los nombres y hacerlos URI-friendly
def normalize(text):
    text = text.strip().replace(" ", "_")
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w_]', '', text)  # elimina caracteres no alfanuméricos salvo _
    return text

# Base del proyecto
base_uri = "https://w3id.org/GGM"

# Diccionario con categorías y elementos
data = {
    "person": ["Gabriel Garcia Marquez", "Louis Jaquez Mandre Daguerre", "Melecio Galvan", "Justin Webster", "Salman Rushdie", "Simon Bolivar", "Ernesto Gonzalez Bermejo", "Hugo Antonio Toro Restrepo", "Leo Matiz"],
    "conceptual_object": ["Dr Godwin Baxter"],
    "physical_thing": ["Costumes in Poor Things"],
    "place": ["Athens", "Colombia", "Cienaga de Magdalena", "Zona Bananera", "Macondo", "Aracataca", "Stockholm", "New York", "Austin", "Texas"], 
    "group_of_people": ["The Greek Wired Wave", "Young upper-class men"],
    "organization": ["Harcourt Brace Jovanovich"],
    "concept": ["Magic Realism", "Colombian Armed Conflict", "Bananeras Massacre"],
    "time": ["284-246 BC", "1490-1500"],
    "timespan": ["20th Century"],
    "group_of_object": ["Seven Wonders of the Ancient World"],
    "article": ["Melena Ryzik"],
    "item": [
        "Article", "Manuscript", "Image", "Interview", "Letter", "Series", "Nobel_Speech", "Documentary", "Illustration", "Manuscript_General"]
}

# Lista para guardar URIs
uris = []

# Generar URIs
for category, items in data.items():
    for item in items:
        uri = f"{base_uri}/{category}/{normalize(item)}"
        uris.append(uri)

# Guardar en archivo o mostrar
with open("uris_ggmLOD.txt", "w", encoding="utf-8") as f:
    for uri in sorted(uris):
        f.write(uri + "\n")

print("✔ URIs generadas y guardadas en uris_ggmLOD.txt")
