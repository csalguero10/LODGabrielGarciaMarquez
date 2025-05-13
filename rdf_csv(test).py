import pandas as pd
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, FOAF, DCTERMS
import unicodedata
import re

# --- Función para normalizar nombres en URIs ---
def normalize(text):
    text = text.lower()
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r"[^\w\s-]", '', text)
    text = re.sub(r"\s+", '-', text.strip())
    return text

# --- Configuraciones base ---
BASE = "https://w3id.org/GGM/"
GGM = Namespace(BASE)
SCHEMA = Namespace("https://schema.org/")

# --- Cargar el CSV ---
df = pd.read_csv("Play.csv")

# --- Crear el grafo RDF ---
g = Graph()
g.bind("ggm", GGM)
g.bind("foaf", FOAF)
g.bind("schema", SCHEMA)
g.bind("rdfs", RDFS)
g.bind("dcterms", DCTERMS)

# --- Recorrer cada fila y generar triples ---
for i, row in df.iterrows():
    character_name = row['character']
    place_name = row['place']
    quote_text = row['quote']

    # URIs
    char_uri = URIRef(BASE + "person/" + normalize(character_name))
    place_uri = URIRef(BASE + "place/" + normalize(place_name))
    quote_uri = URIRef(BASE + f"quote/{i+1}")

    # Person
    g.add((char_uri, RDF.type, FOAF.Person))
    g.add((char_uri, FOAF.name, Literal(character_name)))

    # Place
    g.add((place_uri, RDF.type, GGM.Place))
    g.add((place_uri, RDFS.label, Literal(place_name)))

    # Quote
    g.add((quote_uri, RDF.type, SCHEMA.Quotation))
    g.add((quote_uri, RDFS.label, Literal(quote_text)))
    g.add((quote_uri, SCHEMA.spokenByCharacter, char_uri))
    g.add((quote_uri, DCTERMS.spatial, place_uri))

# --- Exportar ---
g.serialize("play_rdf_output.ttl", format="turtle", base=BASE)
print("✔ RDF exportado a play_rdf_output.ttl")
