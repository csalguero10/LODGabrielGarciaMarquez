from lxml import etree as ET
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, FOAF, DCTERMS, DC, XSD
import unicodedata
import re

# Normalizador para URIs
def normalize(text):
    if not text:
        return ""
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = text.strip().replace(" ", "_")
    return re.sub(r"[^\w\-_.]", "", text)

# Namespaces
BASE = "https://w3id.org/GGM/"
GGM = Namespace(BASE)
SCHEMA = Namespace("https://schema.org/")

# Cargar archivo TEI
tree = ET.parse("tei_xml/tei.xml")
root = tree.getroot()
NS = {"tei": "http://www.tei-c.org/ns/1.0"}

# Crear grafo
g = Graph()
g.bind("ggm", GGM)
g.bind("dcterms", DCTERMS)
g.bind("foaf", FOAF)
g.bind("dc", DC)
g.bind("rdfs", RDFS)
g.bind("schema", SCHEMA)

# === Documento base: El general en su laberinto ===
bibl = root.find(".//tei:sourceDesc/tei:bibl", NS)
if bibl is not None:
    title_el = bibl.find("tei:title[@type='main']", NS)
    alt_title_el = bibl.find("tei:title[@type='alt']", NS)
    author_el = bibl.find("tei:author", NS)
    date_el = bibl.find("tei:date", NS)
    extent_el = bibl.find("tei:extent", NS)
    place_el = bibl.find("tei:pubPlace", NS)

    title_text = title_el.text.strip()
    doc_uri = URIRef(BASE + normalize(title_text))

    g.add((doc_uri, RDF.type, DCTERMS.BibliographicResource))
    g.add((doc_uri, RDFS.label, Literal(title_text)))

    if author_el is not None:
        author_text = author_el.text.strip()
        author_uri = URIRef(BASE + normalize(author_text))
        g.add((author_uri, RDF.type, FOAF.Person))
        g.add((author_uri, FOAF.name, Literal(author_text)))
        g.add((doc_uri, DC.creator, author_uri))

    if alt_title_el is not None:
        g.add((doc_uri, DCTERMS.alternative, Literal(alt_title_el.text.strip())))
    if extent_el is not None:
        g.add((doc_uri, DCTERMS.extent, Literal(extent_el.text.strip())))
    if date_el is not None:
        g.add((doc_uri, DCTERMS.issued, Literal(date_el.get("when"))))
    if place_el is not None:
        g.add((doc_uri, DCTERMS.spatial, Literal(place_el.text.strip())))

    # Identificadores físicos
    callno = root.find(".//tei:idno[@type='callno']", NS)
    box = root.find(".//tei:idno[@type='box']", NS)
    folder = root.find(".//tei:idno[@type='folder']", NS)
    if callno is not None and box is not None and folder is not None:
        identifier = f"Call No: {callno.text}, Box: {box.text}, Folder: {folder.text}"
        g.add((doc_uri, DCTERMS.identifier, Literal(identifier)))

    g.add((doc_uri, DC.language, Literal("es")))

# === Proyecto LOD Gabriel García Márquez ===
title_desc_el = root.find(".//tei:titleStmt/tei:title[@type='desc']", NS)
project_uri = URIRef(BASE + normalize(title_desc_el.text))
g.add((project_uri, RDF.type, DCTERMS.BibliographicResource))
g.add((project_uri, RDFS.label, Literal(title_desc_el.text)))
g.add((project_uri, DCTERMS.title, Literal(title_desc_el.text)))

# Subtítulo / Título alternativo
title_alt_el = root.find(".//tei:titleStmt/tei:title[@type='sub']", NS)
if title_alt_el is not None:
    g.add((project_uri, DCTERMS.alternative, Literal(title_alt_el.text.strip())))

# Responsabilidad
pers_name = root.find(".//tei:titleStmt/tei:respStmt/tei:persName", NS)
if pers_name is not None:
    person_uri = URIRef(BASE + "person/" + normalize(pers_name.text))
    g.add((person_uri, RDF.type, FOAF.Person))
    g.add((person_uri, FOAF.name, Literal(pers_name.text)))
    g.add((project_uri, DCTERMS.creator, person_uri))

# Edición
edition = root.find(".//tei:editionStmt/tei:edition", NS)
if edition is not None:
    g.add((project_uri, DC.format, Literal(edition.text.strip())))

# Fecha de edición
edition_date = root.find(".//tei:publicationStmt/tei:date", NS)
if edition_date is not None:
    g.add((project_uri, DCTERMS.issued, Literal(edition_date.get("when"), datatype=XSD.date)))

# Editorial
publisher = root.find(".//tei:publicationStmt/tei:publisher", NS)
if publisher is not None:
    pub_uri = URIRef(BASE + "organization/" + normalize(publisher.text))
    g.add((project_uri, DCTERMS.publisher, pub_uri))

# Derechos
rights = root.find(".//tei:publicationStmt/tei:availability/tei:p", NS)
if rights is not None:
    g.add((project_uri, DC.rights, Literal(rights.text.strip())))

# Fuente (colección)
collection = root.find(".//tei:msIdentifier/tei:collection", NS)
if collection is not None:
    g.add((project_uri, DCTERMS.source, Literal(collection.text.strip())))

# Relación con el documento
if title_text:
    g.add((project_uri, DCTERMS.hasPart, Literal(title_text)))

# Descripción del proyecto
desc = root.find(".//tei:projectDesc/tei:p", NS)
if desc is not None:
    g.add((project_uri, DCTERMS.description, Literal(desc.text.strip())))

# Fecha de revisión
revision = root.find(".//tei:revisionDesc/tei:change", NS)
if revision is not None:
    rev_date = revision.get("when")
    g.add((project_uri, DCTERMS.modified, Literal(rev_date, datatype=XSD.date)))

# === EXTRAER PÁGINAS ===
for pb in root.xpath(".//tei:pb", namespaces=NS):
    pb_id = pb.get("{http://www.w3.org/XML/1998/namespace}id")
    facs = pb.get("facs")
    page_uri = URIRef(BASE + "page/" + normalize(pb_id))
    g.add((page_uri, RDF.type, GGM.Page))
    if facs:
        g.add((page_uri, GGM.facs, Literal(facs)))

# === EXTRAER PERSONAS ===
character_dict = {}
unique_persons = set()
for person in root.xpath(".//tei:name[@type='person']", namespaces=NS):
    pname = person.text
    if pname:
        norm_name = normalize(pname)
        if norm_name not in unique_persons and pname != "SIMÓN BOLIVAR":
            person_uri = URIRef(BASE + "person/" + norm_name)
            character_dict[norm_name] = person_uri
            g.add((person_uri, RDF.type, FOAF.Person))
            g.add((person_uri, FOAF.name, Literal(pname)))
            unique_persons.add(norm_name)

# === EXTRAER LUGARES ===
for place in root.xpath(".//tei:name[@type='place']", namespaces=NS):
    pname = place.text
    if pname:
        place_uri = URIRef(BASE + "place/" + normalize(pname))
        g.add((place_uri, RDF.type, GGM.Place))
        g.add((place_uri, RDFS.label, Literal(pname)))

# === EXTRAER EPÍGRAFE (Simón Bolívar) ===
epigraph_div = root.find(".//tei:div[@type='epigraph']", namespaces=NS)
if epigraph_div is not None:
    quote_text = epigraph_div.find(".//tei:quote", namespaces=NS)
    quote_content = ''.join(quote_text.itertext()).strip() if quote_text is not None else None

    speaker_el = epigraph_div.find(".//tei:said/tei:name[@type='person']", namespaces=NS)
    speaker_name = speaker_el.text if speaker_el is not None else None

    if quote_content and speaker_name:
        quote_uri = URIRef(BASE + "quote/epigraph")
        speaker_norm = normalize(speaker_name)
        speaker_uri = URIRef(BASE + "person/" + speaker_norm)

        # Formatear nombre capitalizado (Solo primera letra en mayúsculas por palabra)
        formatted_name = ' '.join([w.capitalize() for w in speaker_name.lower().split()])

        g.add((quote_uri, RDF.type, SCHEMA.Quotation))
        g.add((quote_uri, RDFS.label, Literal(quote_content)))
        g.add((quote_uri, SCHEMA.spokenByPerson, speaker_uri))
        g.add((speaker_uri, RDF.type, FOAF.Person))
        g.add((speaker_uri, FOAF.name, Literal(formatted_name)))

# === EXTRAER FIGURAS ===
for fig in root.xpath(".//tei:figure", namespaces=NS):
    desc = fig.find(".//tei:figDesc", namespaces=NS)
    if desc is not None:
        fig_uri = URIRef(BASE + "figure/" + str(hash(desc.text)))
        g.add((fig_uri, RDF.type, GGM.Figure))
        g.add((fig_uri, RDFS.comment, Literal(desc.text)))


# === Exportar RDF ===
g.serialize("tei_xml/tei_rdf_serialization.ttl", format="turtle", base=BASE)
print("✔ RDF metadata serializada en tei_rdf_serialization.ttl")
