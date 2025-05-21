import rdflib
from rdflib import Namespace, URIRef, Literal
from rdflib.namespace import RDF, OWL, DC, DCTERMS, XSD, FOAF, SKOS, RDFS
import pandas as pd
import unicodedata
import re
from datetime import datetime

# Normalize function for URI safety
def normalize(text):
    if pd.isna(text):
        return None
    text = str(text).strip()
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text)
    return re.sub(r'\s+', '_', text)

# Validate ISO date format
def try_parse_date(value):
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None

# Validate if string is a year
def is_year(val):
    return val.isdigit() and len(val) == 4

# Namespaces
SCHEMA = Namespace("https://schema.org/")
CRM = Namespace("https://www.cidoc-crm.org/")
FRBRER = Namespace("http://iflastandards.info/ns/fr/frbr/frbrer/")

# RDF graph
g = rdflib.Graph()

# Base URI
ggm = URIRef("https://w3id.org/GGM/") 

# Entity URIs
namespaces = {
    'item': URIRef(ggm + "item/"),
    'person': URIRef(ggm + "person/"),
    'institution': URIRef(ggm + "institution/"),
    'organization': URIRef(ggm + "organization/"),
    'place': URIRef(ggm + "place/"),
    'concept': URIRef(ggm + "concept/"),
    'event': URIRef(ggm + "event/"),
    'period': URIRef(ggm + "period/"),
    'date': URIRef(ggm + "date/"),
    'phisical_objects': URIRef(ggm + "phisical_objects/"),
    'group_of_people': URIRef(ggm + "group_of_people/"),
    'company': URIRef(ggm + "company/"),
    'occupation': URIRef(ggm + "occupation/"),
    'genre_type': URIRef(ggm + "genre_type/")
}

# Bind namespaces
for prefix, ns in [("schema", SCHEMA), ("crm", CRM), ("frbrer", FRBRER)]:
    g.bind(prefix, ns)

# List of input CSVs
files_csv = [
    "csv_files/Article.csv", "csv_files/Documentary.csv", "csv_files/Illustration.csv",
    "csv_files/Image.csv", "csv_files/Interview.csv", "csv_files/Letter.csv",
    "csv_files/Manuscript_General.csv", "csv_files/Manuscript_Hundred.csv",
    "csv_files/Nobel_Speech.csv", "csv_files/Series.csv"
]

# Items list to distinguish known objects
items_list = [
    "Article", "Documentary", "Illustration", "Letter", "Manuscript_General",
    "Manuscript_Hundred", "Nobel_Speech", "Series"
]

# RDF types
rdf_types = {
    "schema:Article": SCHEMA.Article,
    "schema:Book": SCHEMA.Book,
    "schema:ImageObject": SCHEMA.ImageObject,
    "schema:Manuscript": SCHEMA.Manuscript,
    "schema:Movie": SCHEMA.Movie,
    "schema:Periodical": SCHEMA.Periodical,
    "schema:Place": SCHEMA.Place,
    "schema:TVSeries": SCHEMA.TVSeries,
    "schema:VisualArtwork": SCHEMA.VisualArtwork,
    "crm:E29_Design_or_Procedure": CRM.E29_Design_or_Procedure,
    "crm:E4_Period": CRM.E4_Period,
    "crm:E5_Event": CRM.E5_Event,
    "crm:E73_Information_Object": CRM.E73_Information_Object,
    "crm:E74_Group": CRM.E74_Group,
    "crm:E78_Curated_Holding": CRM.E78_Curated_Holding,
    "foaf:Person": FOAF.Person,
    "frbrer:Character": FRBRER.Character,
    "skos:Concept": SKOS.Concept
}

# Main RDF population
for file in files_csv:
    df = pd.read_csv(file)
    uris_dict = {}

    for _, row in df.iterrows():
        subject = normalize(row["Subject"])
        predicate = row["Predicate"].strip()
        object = row["Object"].strip()

        subject_uri = uris_dict.get(subject) or URIRef(namespaces['item'] + subject)
        uris_dict[subject] = subject_uri

        predicate_uri = RDF.type if predicate == "rdf:type" else \
                        OWL.sameAs if predicate in ["owl:sameAs", "owl:SameAs"] else \
                        getattr(DCTERMS, predicate.split(":")[-1], None) or \
                        getattr(SCHEMA, predicate.split(":")[-1], None) or \
                        getattr(CRM, predicate.split(":")[-1], None)

        if predicate_uri == RDF.type and object in rdf_types:
            obj = rdf_types[object]

        elif predicate_uri == OWL.sameAs:
            obj = URIRef(object)

        elif predicate_uri in [DCTERMS.created, DCTERMS.issued]:
            iso = try_parse_date(object)
            if iso:
                obj = Literal(iso, datatype=XSD.date)
            elif is_year(object):
                obj = Literal(object, datatype=XSD.gYear)
            else:
                obj = Literal(object, datatype=XSD.string)

        elif predicate_uri == DCTERMS.language:
            obj = Literal(object, datatype=XSD.language)

        elif predicate_uri in [DCTERMS.extent, SCHEMA.duration]:
            if re.match(r'^P(\d+Y)?(\d+M)?(\d+D)?(T(\d+H)?(\d+M)?(\d+S)?)?$', object):
                obj = Literal(object, datatype=XSD.duration)
            else:
                obj = Literal(object, datatype=XSD.string)

        elif predicate_uri == SCHEMA.numberOfEpisodes:
            try:
                obj = Literal(int(re.search(r'\d+', object).group()), datatype=XSD.integer)
            except:
                obj = Literal(object, datatype=XSD.string)

        else:
            obj = Literal(object, datatype=XSD.string)

        g.add((subject_uri, predicate_uri, obj))

# Serialize graph
with open("output_rdf_visualization.ttl", "wb") as f:
    f.write(g.serialize(format="turtle", base=ggm, encoding="utf-8"))
