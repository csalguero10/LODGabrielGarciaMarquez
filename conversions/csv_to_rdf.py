
import rdflib
from rdflib import Namespace, URIRef, Literal
from rdflib.namespace import RDF, OWL, DC, DCTERMS, XSD, FOAF, SKOS, RDFS
import pandas as pd
import unicodedata
import re

def normalize(text):
    if pd.isna(text):
        return None
    text = str(text).strip()
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text)
    return re.sub(r'\s+', '_', text)

#Namespaces
SCHEMA = Namespace("https://schema.org/")
CRM = Namespace("https://www.cidoc-crm.org/")
FRBRER = Namespace("http://iflastandards.info/ns/fr/frbr/frbrer/")

#creating a rdf graph
g = rdflib.Graph()

#base_uri
ggm = URIRef("https://w3id.org/GGM/") 

#creating uris
item = URIRef(ggm + "item/")
person = URIRef(ggm + "person/")
institution = URIRef(ggm + "institution/")
organization = URIRef(ggm + "organization/")
place = URIRef(ggm + "place/")
concept = URIRef(ggm + "concept/")
event = URIRef(ggm + "event/")
period = URIRef(ggm + "period/")
date = URIRef(ggm + "date/")
phisical_objects = URIRef(ggm + "phisical_objects/")
group_of_people = URIRef(ggm + "group_of_people/")
company = URIRef(ggm + "company/")
occupation = URIRef(ggm + "occupation/")
genre_type = URIRef(ggm + "genre_type/")

#bind namespaces to graph
g.bind("schema", SCHEMA)
g.bind("crm", CRM)

#list of csv files
files_csv = ["csv_files/Article.csv", "csv_files/Documentary.csv", "csv_files/Illustration.csv", "csv_files/Image.csv", "csv_files/Interview.csv", "csv_files/Letter.csv", "csv_files/Manuscript_General.csv", "csv_files/Manuscript_Hundred.csv", "csv_files/Nobel_Speech.csv", "csv_files/Series.csv"]

#for loop that iterates all the csv files and add data to the same graph
for file in files_csv:

    #create a pandas dataframe to read csv 
    df = pd.read_csv(file)   
    
    #dict to store uris
    uris_dict = dict()

    items_list = ["Article", "Documentary", "Illustration", "Letter", "Manuscript_General", "Manuscript_Hundred", "Nobel_Speech", "Series"]

    #iterate through the dataframe:
    for _, row in df.iterrows():
        
        #get row's subject, predicate and object
        subject = row["Subject"]
        predicate = row["Predicate"]
        object = row["Object"]
        
        #create subject uri
        if subject not in uris_dict:
            subject_uri = URIRef(item + subject.replace(" ", "_"))
            uris_dict[subject] = subject_uri   
        else:
            subject_uri = uris_dict[subject]

        # specify predicates
        if predicate == "rdf:type":
            predicate_uri = RDF.type

        elif predicate in ["owl:SameAs", "owl:sameAs"]:
            predicate_uri = OWL.sameAs

        # DCTERMS
        elif predicate == "dcterms:created":
            predicate_uri = DCTERMS.created

        elif predicate == "dcterms:creator":
            predicate_uri = DCTERMS.creator

        elif predicate == "dcterms:extent":
            predicate_uri = DCTERMS.extent

        elif predicate == "dcterms:format":
            predicate_uri = DCTERMS.format

        elif predicate == "dcterms:isPartOf":
            predicate_uri = DCTERMS.isPartOf

        elif predicate == "dcterms:issued":
            predicate_uri = DCTERMS.issued

        elif predicate == "dcterms:language":
            predicate_uri = DCTERMS.language

        elif predicate == "dcterms:publisher":
            predicate_uri = DCTERMS.publisher

        elif predicate == "dcterms:relation":
            predicate_uri = DCTERMS.relation

        elif predicate == "dcterms:subject":
            predicate_uri = DCTERMS.subject

        elif predicate == "dcterms:references":
            predicate_uri = DCTERMS.references

        # SCHEMA
        elif predicate == "schema:about":
            predicate_uri = SCHEMA.about

        elif predicate == "schema:birthPlace":
            predicate_uri = SCHEMA.birthPlace

        elif predicate == "schema:countryOfOrigin":
            predicate_uri = SCHEMA.countryOfOrigin

        elif predicate == "schema:director":
            predicate_uri = SCHEMA.director

        elif predicate == "schema:duration":
            predicate_uri = SCHEMA.duration

        elif predicate == "schema:genre":
            predicate_uri = SCHEMA.genre

        elif predicate == "schema:hasOccupation":
            predicate_uri = SCHEMA.hasOccupation

        elif predicate == "schema:isBasedOn":
            predicate_uri = SCHEMA.isBasedOn

        elif predicate == "schema:location":
            predicate_uri = SCHEMA.location

        elif predicate == "schema:locationCreated":
            predicate_uri = SCHEMA.locationCreated

        elif predicate == "schema:numberOfEpisodes":
            predicate_uri = SCHEMA.numberOfEpisodes

        elif predicate == "schema:productionCompany":
            predicate_uri = SCHEMA.productionCompany

        elif predicate == "schema:recipient":
            predicate_uri = SCHEMA.recipient

        elif predicate == "schema:recordedAt":
            predicate_uri = SCHEMA.recordedAt

        elif predicate == "schema:sender":
            predicate_uri = SCHEMA.sender
        
        elif predicate == "schema:participant":
            predicate_uri = SCHEMA.participant

        # CIDOC CRM
        elif predicate == "crm:P107_has_current_or_former_member":
            predicate_uri = CRM.P107_has_current_or_former_member

        elif predicate == "crm:P10_falls_within":
            predicate_uri = CRM.P10_falls_within

        elif predicate == "crm:P138_represents":
            predicate_uri = CRM.P138_represents

        elif predicate == "crm:P14_carried_out_by":
            predicate_uri = CRM.P14_carried_out_by

        elif predicate == "crm:P67_refers_to":
            predicate_uri = CRM.P67_refers_to

        elif predicate == "crm:E57_consist_of":
            predicate_uri = CRM.E57_consist_of

        elif predicate == "crm:E74_Group":
            predicate_uri = CRM.E74_Group

        elif predicate == "crm:P102_has_title":
            predicate_uri = CRM.P102_has_title

        elif predicate == "crm:P32_used_general_technique":
            predicate_uri = CRM.P32_used_general_technique

        elif predicate == "crm:P43_has_dimension":
            predicate_uri = CRM.P43_has_dimension

        elif predicate == "crm:P52_has_current_owner":
            predicate_uri = CRM.P52_has_current_owner

        elif predicate == "crm:P55_has_current_location":
            predicate_uri = CRM.P55_has_current_location

        # specify RDF types as objects
        if predicate_uri == RDF.type:
            if object == "schema:Article":
                obj = SCHEMA.Article
            elif object == "schema:Book":
                obj = SCHEMA.Book
            elif object == "schema:ImageObject":
                obj = SCHEMA.ImageObject
            elif object == "schema:Manuscript":
                obj = SCHEMA.Manuscript
            elif object == "schema:Movie":
                obj = SCHEMA.Movie
            elif object == "schema:Periodical":
                obj = SCHEMA.Periodical
            elif object == "schema:Place":
                obj = SCHEMA.Place
            elif object == "schema:TVSeries":
                obj = SCHEMA.TVSeries
            elif object == "schema:VisualArtwork":
                obj = SCHEMA.VisualArtwork
            elif object == "crm:E29_Design_or_Procedure":
                obj = CRM.E29_Design_or_Procedure
            elif object == "crm:E4_Period":
                obj = CRM.E4_Period
            elif object == "crm:E5_Event":
                obj = CRM.E5_Event
            elif object == "crm:E73_Information_Object":
                obj = CRM.E73_Information_Object
            elif object == "crm:E74_Group":
                obj = CRM.E74_Group
            elif object == "crm:E78_Curated_Holding":
                obj = CRM.E78_Curated_Holding
            elif object == "schema:Message":
                obj = SCHEMA.Message
            elif object == "foaf:Person":
                obj = FOAF.Person
            elif object == "frbrer:Character":
                obj = FRBRER.Character
            elif object == "skos:Concept":
                obj = SKOS.Concept

        elif predicate_uri == OWL.sameAs:
            obj = URIRef(object)      

        #Mapping of people, persons and organizations
        elif predicate_uri == DCTERMS.creator or predicate_uri == SCHEMA.director or predicate_uri == SCHEMA.recipient or predicate_uri == SCHEMA.sender or predicate_uri == CRM.P14_carried_out_by or predicate_uri == SCHEMA.participant or predicate_uri == DCTERMS.references or predicate_uri == CRM.P138_represents:
            if object not in uris_dict:
                if object in items_list:
                    obj = URIRef(item + object.replace(" ", "_"))
                    uris_dict[object] = obj
                else:    
                    obj = URIRef(person + object.replace(" ", "_"))
                    uris_dict[object] = obj

        elif predicate_uri == CRM.P107_has_current_or_former_member:
            if object not in uris_dict:
                obj = URIRef(group_of_people + object.replace(" ", "_"))
                uris_dict[object] = obj
            else:
                obj = uris_dict[object]         

        elif predicate_uri == SCHEMA.productionCompany:
            if object not in uris_dict:
                obj = URIRef(company + object.replace(" ", "_"))
                uris_dict[object] = obj
            else:
                obj = uris_dict[object] 

        elif predicate_uri == DCTERMS.publisher or predicate_uri == CRM.P52_has_current_owner or predicate_uri == DCTERMS.isPartOf:
            if object not in uris_dict:
                obj = URIRef(institution + object.replace(" ", "_"))
                uris_dict[object] = obj
            else:
                obj = uris_dict[object]
        
        elif predicate_uri == SCHEMA.hasOccupation:
            if object not in uris_dict:
                obj = URIRef(occupation + object.replace(" ", "_"))
                uris_dict[object] = obj
            else:
                obj = uris_dict[object]
        
        # Mapping of places
        elif predicate_uri == SCHEMA.birthPlace or predicate_uri == CRM.P55_has_current_location or predicate_uri == SCHEMA.locationCreated or predicate_uri == SCHEMA.location or predicate_uri == SCHEMA.countryOfOrigin:
            if object not in uris_dict:
                obj = URIRef(place + object.replace(" ", "_"))
                uris_dict[object] = obj
            else:
                obj = uris_dict[object]
        
        # Mapping of events
        elif predicate_uri == CRM.P67_refers_to or predicate_uri == SCHEMA.recordedAt:
            if object not in uris_dict:
                obj = URIRef(event + object.replace(" ", "_"))
                uris_dict[object] = obj
            else:
                obj = uris_dict[object]
        
        # Mapping of periods
        elif predicate_uri == CRM.P10_falls_within:
            if object not in uris_dict:
                obj = URIRef(period + object.replace(" ", "_"))
                uris_dict[object] = obj
            else:
                obj = uris_dict[object]
        
        # Mapping of genres
        elif predicate_uri == SCHEMA.genre:
            if object not in uris_dict:
                obj = URIRef(genre_type + object.replace(" ", "_"))
                uris_dict[object] = obj
            else:
                obj = uris_dict[object]

        # Mapping of concepts         
        elif predicate_uri == SCHEMA.about:
            if object not in uris_dict:  
                obj = URIRef(item + object.replace(" ", "_"))
                uris_dict[object] = obj
            else:    
                    obj = URIRef(concept + object.replace(" ", "_"))
                    uris_dict[object] = obj
        
        elif predicate_uri == DCTERMS.subject:
            if object not in uris_dict:
                if object in items_list:
                    obj = URIRef(item + object.replace(" ", "_"))
                    uris_dict[object] = obj
                else:    
                    obj = URIRef(concept + object.replace(" ", "_"))
                    uris_dict[object] = obj
            else:
                obj = uris_dict[object]

        # Mapping of books or phisical objects
        elif predicate_uri == DCTERMS.isPartOf or predicate_uri == CRM.E57_consist_of or predicate_uri == CRM.P32_used_general_technique or predicate_uri == CRM.P2_has_type or predicate_uri == SCHEMA.isBasedOn:
            if object not in uris_dict:
                obj = URIRef(phisical_objects + object.replace(" ", "_"))
                uris_dict[object] = obj
            else:
                obj = uris_dict[object] 
        
        # Mapping of relations
        elif predicate_uri == DCTERMS.relation:
            if object not in uris_dict:
                if object in items_list:
                    obj = URIRef(item + object.replace(" ", "_"))
                    uris_dict[object] = obj
                elif object == "Aracataca":
                    obj = URIRef(place + object.replace(" ", "_"))
                    uris_dict[object] = obj
                elif object == "Gabriel Garcia Marquez":
                    obj = URIRef(person + object.replace(" ", "_"))
                    uris_dict[object] = obj
                else:
                    obj = URIRef(concept + object.replace(" ", "_"))
                    uris_dict[object] = obj
            else:
                obj = uris_dict[object]

        # mapping of dates and years  
        elif predicate_uri == DCTERMS.created:
            if object not in uris_dict:
                if "-" in object:    
                    obj = URIRef(date + object.replace(" ", "_"))
                    uris_dict[object] = obj  
                else:
                    obj = Literal(object, datatype=XSD.gYear)
            else:
                obj = uris_dict[object]    
        
        elif predicate_uri == DCTERMS.issued:
            if object not in uris_dict:
                if "-" in object:
                    obj = Literal(object, datatype=XSD.date)   
                else:
                    obj = Literal(object, datatype=XSD.gYear)   
            else:
                obj = uris_dict[object]         
        
        # handle additional literal types
        elif predicate_uri == DCTERMS.language:
            obj = Literal(object, datatype=XSD.language)

        elif predicate_uri == DCTERMS.extent:
            obj = Literal(object, datatype=XSD.duration)

        elif predicate_uri == SCHEMA.duration:
            obj = Literal(object, datatype=XSD.duration)

        elif predicate_uri == SCHEMA.numberOfEpisodes:
            obj = Literal(object, datatype=XSD.integer)

        else:
            obj = Literal(object, datatype=XSD.string)

        #add triple to graph
        g.add((subject_uri, predicate_uri, obj))

#serialize the graph to Turtle format
turtle_str = g.serialize(format="turtle", base=ggm, encoding="utf-8")

#write the Turtle string to a file
with open("output_rdf_visualization.ttl", "wb") as f:
    f.write(turtle_str)
