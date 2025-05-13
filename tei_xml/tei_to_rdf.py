from lxml import etree
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, FOAF, DC, DCTERMS

# Load XML
tree = etree.parse("tei_xml/tei.xml")
root = tree.getroot()

# Namespaces
NS = {"tei": "http://www.tei-c.org/ns/1.0"}
BASE = "https://w3id.org/PoorThings.org/"
EX = Namespace(BASE)
SCHEMA = Namespace("https://schema.org/")

# Graph init
g = Graph()
g.bind("ex", EX)
g.bind("foaf", FOAF)
g.bind("dc", DC)
g.bind("dcterms", DCTERMS)
g.bind("schema", SCHEMA)

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

# People mentioned (from <name type="person"> and <persName>)
for person in root.xpath("//tei:name[@type='person']", namespaces=NS):
    pname = person.text
    if pname:
        person_uri = URIRef(BASE + "person/" + pname.replace(" ", "_"))
        g.add((person_uri, RDF.type, FOAF.Person))
        g.add((person_uri, FOAF.name, Literal(pname)))

# Places mentioned
for place in root.xpath("//tei:name[@type='place']", namespaces=NS):
    pname = place.text
    if pname:
        place_uri = URIRef(BASE + "place/" + pname.replace(" ", "_"))
        g.add((place_uri, RDF.type, SCHEMA.Place))
        g.add((place_uri, RDFS.label, Literal(pname)))

# Speech quotes: <said>
quote_id = 1
for quote in root.xpath("//tei:said", namespaces=NS):
    text = ''.join(quote.itertext()).strip()
    speaker = quote.get("who")
    quote_uri = URIRef(BASE + f"quote/{quote_id}")
    quote_id += 1

    g.add((quote_uri, RDF.type, SCHEMA.Quotation))
    g.add((quote_uri, RDFS.label, Literal(text)))

    if speaker:
        speaker = speaker.strip("#")
        speaker_uri = URIRef(BASE + "person/" + speaker)
        g.add((quote_uri, SCHEMA.spokenByCharacter, speaker_uri))

# Output to Turtle
g.serialize("tei_xml/tei_rdf_output.ttl", format="turtle", base=BASE)
