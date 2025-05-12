import xml.etree.ElementTree as ET
import rdflib
from rdflib import Namespace, URIRef, Literal
from rdflib.namespace import RDF, FOAF, RDFS, DC, DCTERMS

#namespaces definition
TEI = Namespace("http://www.tei-c.org/ns/1.0")
DBO = Namespace("https://dbpedia.org/ontology/")
SCHEMA = Namespace("https://schema.org/")

#parsing the xml document
tree = ET.parse('tei.xml')

#creating a graph
g = rdflib.Graph()

#define namespace for tei
ns = {"tei": TEI}

#base_uri
pt = URIRef("https://w3id.org/PoorThings.org/")

#bind namespaces to graph
g.bind("dbo", DBO)
g.bind("schema", SCHEMA)

#extraction of metadata
title = tree.find(".//tei:titleStmt/tei:title", ns).text
author = tree.find(".//tei:titleStmt/tei:author", ns).text
format = tree.find(".//tei:editionStmt/tei:edition", ns).text
extent = tree.find(".//tei:extent", ns).text
publisher = tree.find(".//tei:publicationStmt/tei:publisher/tei:orgName", ns).text
address = tree.find(".//tei:publicationStmt/tei:address/tei:addrLine", ns).text
id = tree.find(".//tei:publicationStmt/tei:idno", ns).text
copyright = tree.find(".//tei:publicationStmt/tei:availability/tei:p", ns).text
date = tree.find(".//tei:publicationStmt/tei:date", ns)
when = date.get("when")

#metadata uris
title_uri = URIRef(pt + title.replace(" ", "_"))
author_uri = URIRef(pt + author.replace(",", "").replace(" (1934-2019)", "").replace(" ", "_"))
publisher_uri = URIRef(pt + publisher.replace(" ", "_"))

#adding metadata triples to the graph
g.add((title_uri, RDF.type, DCTERMS.BibliographicResource))
g.add((title_uri, DC.creator, author_uri))
g.add((title_uri, DCTERMS.issued, Literal(when)))
g.add((title_uri, DC.format, Literal(format)))
g.add((title_uri, DCTERMS.extent, Literal(extent)))
g.add((title_uri, DCTERMS.publisher, publisher_uri))
g.add((title_uri, DC.identifier, Literal(id)))
g.add((title_uri, DC.rights, Literal(copyright)))
g.add((author_uri, RDF.type, FOAF.Person))
g.add((title_uri, RDFS.label, Literal(title)))
g.add((publisher_uri, RDF.type, DBO.publisher))
g.add((publisher_uri, SCHEMA.address, Literal(address)))

#character dictionary
character_dict = dict()

#characters extraction
for character in tree.findall(".//tei:profileDesc/tei:particDesc/tei:listPerson/tei:person", ns):

    #create charecter uri and add them to graph
    name = character.find("tei:persName", ns).text.rstrip()
    id = character.get("{http://www.w3.org/XML/1998/namespace}id")
    character_uri = URIRef(pt + "character/" + name.replace(" ", "_"))
    character_dict[id] = character_uri
    g.add((character_uri, RDF.type, FOAF.Person))
    g.add((character_uri, RDFS.label, Literal(name)))
    
    #find if character has occupation and add it to graph
    if character.find("tei:occupation", ns) is not None:
        occupation = character.find("tei:occupation", ns).text
        g.add((character_uri, SCHEMA.hasOccupation, Literal(occupation)))        

#lines dictionary
lines_dict = dict()

#counter
counter_l = 1

#find lines
for line in tree.findall(".//tei:text/tei:body/tei:div/tei:div/tei:l", ns):

    #create id and uri for every line
    line_id = counter_l
    line_uri = URIRef(pt + "line/" + str(line_id))
    #add id and uri to dict
    lines_dict[line_id] = line_uri 
    counter_l += 1

    #find text of line
    text = ''.join(line.itertext()) 

    #find if characters are mentioned
    mention = line.find("tei:name[@type='person']", ns)
    if mention is not None:
        ref = mention.get("ref")
        if ref is not None:
            ref = ref.strip('#')
            if ref in character_dict:
                character_uri = character_dict[ref]
                g.add((line_uri, RDF.type, SCHEMA.Text))
                g.add((line_uri, RDFS.label, Literal(text))) 
                g.add((line_uri, DCTERMS.references, character_uri))
                g.add((character_uri, DCTERMS.isReferencedBy, line_uri))

    #find if places are mentioned
    place = line.find("tei:name[@type='place']", ns)
    if place is not None:
        place_uri = URIRef(pt + "place/" + place.text.replace(" ", "_"))
        g.add((place_uri, RDF.type, SCHEMA.place))
        g.add((place_uri, RDFS.label, Literal(place.text)))
        g.add((place_uri, DCTERMS.isReferencedBy, line_uri))
        g.add((line_uri, RDF.type, SCHEMA.Text))
        g.add((line_uri, RDFS.label, Literal(text)))
        g.add((line_uri, DCTERMS.references, place_uri))        

#function to unite text of quotes that are in separate lines
def unite_quotes_text(link, root):
    targets = link.get("target").split()
    quotes = []
    for qs in targets:
        qs = qs.strip('#')
        xml_ns = "{http://www.w3.org/XML/1998/namespace}"
        s = root.find(f".//tei:s[@{xml_ns}id='{qs}']", ns)
        if s is not None:
            quotes.append(''.join(s.itertext()))
    return ' '.join(quotes)

#dictionary for links
link_dict = dict()

#find text of quotes that must be linked to each other
for link in tree.findall(".//tei:text/tei:body/tei:div/tei:div/tei:link", ns):
    complte_quote_text = unite_quotes_text(link, tree.getroot())
    target = link.get("target").split()
    complete_quote_id = target[0].strip('#')
    link_dict[complete_quote_id] = complte_quote_text

#dictionary for quotes and their text
quote_text_dict = dict()

#find all the quotes
for quote in tree.findall(".//tei:text/tei:body/tei:div/tei:div/tei:l/tei:q", ns):

    #find quote text
    s = quote.find("tei:s", ns)
    if s is not None:
        id = s.get("{http://www.w3.org/XML/1998/namespace}id")
        if id in link_dict:
            quote_text = link_dict[id] 
            quote_text_dict[quote] = quote_text 
    else:        
        quote_text = ''.join(quote.itertext())
        quote_text_dict[quote] = quote_text 

    #counter
    counter_q = 1   
    
    for q, text in quote_text_dict.items():

        #create id and uri for every quote
        quote_id = counter_q
        counter_q += 1
        quote_uri = URIRef(pt + "quote/" + str(quote_id))
    
        #find speaker
        speaker = q.get("who").strip('#')
        speaker_uri = character_dict[speaker]
        g.add((quote_uri, RDF.type, SCHEMA.Quotation))
        g.add((quote_uri, RDFS.label, Literal(text))) 
        g.add((quote_uri, SCHEMA.spokenByCharacter, speaker_uri))

#serialize the graph to Turtle format
turtle_str = g.serialize(format="turtle", base=pt, encoding="utf-8")

#write the Turtle string to a file
with open("output_tei_rdf.ttl", "wb") as f:
    f.write(turtle_str)