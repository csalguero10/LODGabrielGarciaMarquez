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

# === Metadata General ===
desc_title = root.find(".//tei:titleStmt/tei:title[@type='desc']", NS).text
sub_title = root.find(".//tei:titleStmt/tei:title[@type='sub']", NS).text
resp = root.find(".//tei:titleStmt/tei:respStmt/tei:resp", NS).text
resp_name = root.find(".//tei:titleStmt/tei:respStmt/tei:persName", NS).text
resp_id = root.find(".//tei:titleStmt/tei:respStmt/tei:persName", NS).get("{http://www.w3.org/XML/1998/namespace}id")

project_uri = URIRef(BASE + normalize(desc_title))

# === Edition Info ===
edition = root.find(".//tei:editionStmt/tei:edition", NS).text.strip()
edition_date = root.find(".//tei:editionStmt/tei:edition/tei:date", NS).text.strip()

# === Publication Info ===
publisher = root.find(".//tei:publicationStmt/tei:publisher", NS).text
address_lines = root.findall(".//tei:publicationStmt/tei:address/tei:addrLine", NS)
address = ", ".join(line.text for line in address_lines)
pub_date = root.find(".//tei:publicationStmt/tei:date", NS)
copyright_text = root.find(".//tei:publicationStmt/tei:availability/tei:p", NS).text.strip()

# === Source Description ===
main_title = root.find(".//tei:sourceDesc//tei:title[@type='main']", NS).text
alt_title = root.find(".//tei:sourceDesc//tei:title[@type='alt']", NS).text
author = root.find(".//tei:sourceDesc//tei:author", NS).text
author_id = root.find(".//tei:sourceDesc//tei:author", NS).get("{http://www.w3.org/XML/1998/namespace}id")
source_date = root.find(".//tei:sourceDesc//tei:date", NS).get("when")
pub_place = root.find(".//tei:sourceDesc//tei:pubPlace", NS).text
extent = root.find(".//tei:sourceDesc//tei:extent", NS).text

# === Identificadores físicos ===
callno = root.find(".//tei:idno[@type='callno']", NS).text
box = root.find(".//tei:idno[@type='box']", NS).text
folder = root.find(".//tei:idno[@type='folder']", NS).text
institution = root.find(".//tei:msIdentifier/tei:institution", NS).text
collection = root.find(".//tei:msIdentifier/tei:collection", NS).text

# === Idioma ===
lang = root.find(".//tei:language", NS).text
lang_code = root.find(".//tei:langUsage", NS).get("{http://www.w3.org/XML/1998/namespace}lang")

# === Proyecto ===
project_desc = root.find(".//tei:projectDesc/tei:p", NS).text.strip()

# === Revisión ===
revision = root.find(".//tei:revisionDesc/tei:change", NS).text.strip()
revision_date = root.find(".//tei:revisionDesc/tei:change", NS).get("when")
revision_resp = root.find(".//tei:revisionDesc/tei:change", NS).get("who").strip("#")

# === Crear URIs ===
author_uri = URIRef(BASE + "person/" + normalize(author))
resp_uri = URIRef(BASE + "person/" + normalize(resp_name))
pub_uri = URIRef(BASE + "organization/" + normalize(publisher))
place_uri = URIRef(BASE + "place/" + normalize(pub_place))
institution_uri = URIRef(BASE + "organization/" + normalize(institution))

# === Triples ===
g.add((project_uri, RDF.type, DCTERMS.BibliographicResource))
g.add((project_uri, RDFS.label, Literal(desc_title)))
g.add((project_uri, DCTERMS.title, Literal(desc_title)))
g.add((project_uri, DCTERMS.alternative, Literal(sub_title)))
g.add((project_uri, DCTERMS.creator, resp_uri))
g.add((resp_uri, RDF.type, FOAF.Person))
g.add((resp_uri, FOAF.name, Literal(resp_name)))
g.add((project_uri, DCTERMS.publisher, pub_uri))
g.add((pub_uri, RDFS.label, Literal(publisher)))
g.add((pub_uri, RDFS.comment, Literal(address)))
g.add((project_uri, DCTERMS.issued, Literal(pub_date.get("when"), datatype=XSD.date)))
g.add((project_uri, DCTERMS.rights, Literal(copyright_text)))
g.add((project_uri, DCTERMS.hasPart, Literal(main_title)))
g.add((project_uri, DC.language, Literal(lang_code)))
g.add((project_uri, DCTERMS.description, Literal(project_desc)))
g.add((project_uri, DCTERMS.modified, Literal(revision_date, datatype=XSD.date)))

g.add((author_uri, RDF.type, FOAF.Person))
g.add((author_uri, FOAF.name, Literal(author)))
g.add((project_uri, DC.creator, author_uri))

g.add((project_uri, DCTERMS.spatial, place_uri))
g.add((place_uri, RDFS.label, Literal(pub_place)))

g.add((project_uri, DCTERMS.extent, Literal(extent)))
g.add((project_uri, DCTERMS.identifier, Literal(f"Call No: {callno}, Box: {box}, Folder: {folder}")))
g.add((project_uri, DCTERMS.source, Literal(collection)))
g.add((project_uri, DCTERMS.contributor, institution_uri))
g.add((institution_uri, RDFS.label, Literal(institution)))

# Bibliographic Info
bibl = root.find(".//tei:sourceDesc/tei:bibl", NS)
if bibl is not None:
    title = bibl.find("tei:title[@type='main']", NS)
    alt_title = bibl.find("tei:title[@type='alt']", NS)
    author = bibl.find("tei:author", NS)
    date = bibl.find("tei:date", NS)
    extent = bibl.find("tei:extent", NS)
    pub_place = bibl.find("tei:pubPlace", NS)

    doc_uri = URIRef(BASE + (title.text.replace(" ", "_") if title is not None else "document"))

    g.add((doc_uri, RDF.type, DCTERMS.BibliographicResource))

    if title is not None:
        g.add((doc_uri, RDFS.label, Literal(title.text)))
    if alt_title is not None:
        g.add((doc_uri, DCTERMS.alternative, Literal(alt_title.text)))
    if date is not None:
        g.add((doc_uri, DCTERMS.issued, Literal(date.get("when"))))
    if extent is not None:
        g.add((doc_uri, DCTERMS.extent, Literal(extent.text)))
    if pub_place is not None:
        g.add((doc_uri, DCTERMS.spatial, Literal(pub_place.text)))
    if author is not None:
        author_uri = URIRef(BASE + author.text.replace(" ", "_"))
        g.add((author_uri, RDF.type, FOAF.Person))
        g.add((author_uri, FOAF.name, Literal(author.text)))
        g.add((doc_uri, DC.creator, author_uri))

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
for person in root.xpath(".//tei:name[@type='person']", namespaces=NS):
    pname = person.text
    if pname:
        norm_name = normalize(pname)
        person_uri = URIRef(BASE + "person/" + norm_name)
        character_dict[norm_name] = person_uri
        g.add((person_uri, RDF.type, FOAF.Person))
        g.add((person_uri, FOAF.name, Literal(pname)))

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
        speaker_uri = character_dict.get(speaker_norm, URIRef(BASE + "person/" + speaker_norm))

        g.add((quote_uri, RDF.type, SCHEMA.Quotation))
        g.add((quote_uri, RDFS.label, Literal(quote_content)))
        g.add((quote_uri, SCHEMA.spokenByPerson, speaker_uri))
        g.add((speaker_uri, RDF.type, FOAF.Person))
        g.add((speaker_uri, FOAF.name, Literal(speaker_name)))

# === EXTRAER FIGURAS ===
for fig in root.xpath(".//tei:figure", namespaces=NS):
    desc = fig.find(".//tei:figDesc", namespaces=NS)
    if desc is not None:
        fig_uri = URIRef(BASE + "figure/" + str(hash(desc.text)))
        g.add((fig_uri, RDF.type, GGM.Figure))
        g.add((fig_uri, RDFS.comment, Literal(desc.text)))

# === EXTRAER FIGURAS (dibujos) ===
for fig in root.xpath(".//tei:figure", namespaces=NS):
    desc = fig.find(".//tei:figDesc", namespaces=NS)
    if desc is not None:
        fig_uri = URIRef(BASE + "figure/" + str(hash(desc.text)))
        g.add((fig_uri, RDF.type, GGM.Figure))
        g.add((fig_uri, RDFS.comment, Literal(desc.text)))

# === Exportar RDF ===
g.serialize("tei_metadata_serialization.ttl", format="turtle", base=BASE)
print("✔ RDF metadata serializada en tei_metadata_serialization.ttl")
