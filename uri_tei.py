from lxml import etree as ET
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, FOAF, DCTERMS, DC, XSD
import unicodedata
import re

# --- Configuración base ---
ns = {"tei": "http://www.tei-c.org/ns/1.0"}
base = "https://w3id.org/GGM/"
GGM = Namespace(base)
DBO = Namespace("https://dbpedia.org/ontology/")
SCHEMA = Namespace("https://schema.org/")

# --- Función para normalizar nombres (URIs amigables) ---
def normalize(name):
    name = name.lower()
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('utf-8')  # quita tildes
    name = re.sub(r"[^\w\s-]", '', name)  # elimina puntuación
    name = re.sub(r"\s+", '-', name.strip())  # reemplaza espacios por guiones
    return name

# --- Parseo del TEI ---
tree = ET.parse("tei_xml/tei.xml")
root = tree.getroot()

# --- Inicializar grafo RDF ---
g = Graph()
g.bind("ggm", GGM)
g.bind("foaf", FOAF)
g.bind("dcterms", DCTERMS)
g.bind("dc", DC)
g.bind("rdfs", RDFS)
g.bind("dbo", DBO)
g.bind("schema", SCHEMA)

# --- EXTRAER TÍTULO DE OBRA ---
title_el = root.find(".//tei:sourceDesc/tei:bibl/tei:title[@type='main']", ns)
if title_el is not None:
    title = title_el.text
    title_uri = URIRef(base + "book/" + normalize(title))
    g.add((title_uri, RDF.type, DCTERMS.BibliographicResource))
    g.add((title_uri, RDFS.label, Literal(title, lang="es")))

# --- EXTRAER AUTOR ---
author_el = root.find(".//tei:sourceDesc/tei:bibl/tei:author", ns)
if author_el is not None:
    author = author_el.text
    author_uri = URIRef(base + "person/" + normalize(author))
    g.add((author_uri, RDF.type, FOAF.Person))
    g.add((author_uri, FOAF.name, Literal(author)))
    g.add((title_uri, DC.creator, author_uri))

# --- EXTRAER PERSONAS MENCIONADAS ---
for pers in root.xpath("//tei:name[@type='person']", namespaces=ns):
    name = pers.text
    if name:
        person_uri = URIRef(base + "person/" + normalize(name))
        g.add((person_uri, RDF.type, FOAF.Person))
        g.add((person_uri, FOAF.name, Literal(name)))

# --- EXTRAER LUGARES MENCIONADOS ---
for place in root.xpath("//tei:name[@type='place']", namespaces=ns):
    name = place.text
    if name:
        place_uri = URIRef(base + "place/" + normalize(name))
        g.add((place_uri, RDF.type, GGM.Place))
        g.add((place_uri, RDFS.label, Literal(name)))

# --- EXPORTAR ---
output_path = "ggm_entities.ttl"
g.serialize(destination=output_path, format="turtle", base=base)
print(f"RDF generado en {output_path}")
