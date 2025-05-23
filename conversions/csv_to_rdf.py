import rdflib
from rdflib import Namespace, URIRef, Literal
from rdflib.namespace import RDF, OWL, DC, DCTERMS, XSD, FOAF, SKOS, RDFS
import pandas as pd
import unicodedata
import re
from datetime import datetime

def normalize(text):
    if pd.isna(text):
        return None
    text = str(text).strip()
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text)
    return re.sub(r'\s+', '_', text)

def parse_date_flexible(date_string):
    if pd.isna(date_string) or not date_string.strip():
        return None
    date_string = str(date_string).strip()
    # Try parsing common date formats
    for fmt in ('%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y', '%Y/%m/%d', '%Y'):
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            pass
    return None # Return None if no format matches

def format_duration_for_xsd(duration_string):
    if pd.isna(duration_string) or not duration_string.strip():
        return None
    duration_string = str(duration_string).strip()

    # Attempt to handle common ISO 8601-like formats that might be slightly off
    # If it starts with 'pt' (case-insensitive), try to use it directly as XSD.duration
    if duration_string.lower().startswith("pt"):
        try:
            return Literal(duration_string, datatype=XSD.duration)
        except Exception:
            pass # Fallback to string if this specific format also fails

    # If it looks like a custom string (e.g., "2 pages", "1 tape", "Sound recordings")
    if "pages" in duration_string.lower() or \
       "tape" in duration_string.lower() or \
       "sound recordings" in duration_string.lower():
        return Literal(duration_string, datatype=XSD.string)
    
    # For any other string, try to parse it as an XSD duration.
    # If that fails, default to XSD.string to prevent errors.
    try:
        return Literal(duration_string, datatype=XSD.duration)
    except Exception:
        return Literal(duration_string, datatype=XSD.string)

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
physical_objects = URIRef(ggm + "physical_objects/") # Corrected typo here
group_of_people = URIRef(ggm + "group_of_people/")
company = URIRef(ggm + "company/")
occupation = URIRef(ggm + "occupation/")
genre_type = URIRef(ggm + "genre_type/")

#bind namespaces to graph
g.bind("schema", SCHEMA)
g.bind("crm", CRM)
g.bind("ggm", ggm) # Bind the base URI for easier debugging and visualization
g.bind("foaf", FOAF)
g.bind("dcterms", DCTERMS)
g.bind("xsd", XSD)
g.bind("skos", SKOS)
g.bind("owl", OWL)
g.bind("frbrer", FRBRER)
g.bind("rdfs", RDFS)

#list of csv files
files_csv = ["csv_files/Article.csv", "csv_files/Documentary.csv", "csv_files/Illustration.csv", "csv_files/Image.csv", "csv_files/Interview.csv", "csv_files/Letter.csv", "csv_files/Book.csv", "csv_files/Manuscript.csv", "csv_files/Nobel_Speech.csv", "csv_files/Series.csv"]

#for loop that iterates all the csv files and add data to the same graph
for file in files_csv:

    #create a pandas dataframe to read csv 
    df = pd.read_csv(file)   
    
    #dict to store uris
    uris_dict = dict()

    # It's better to get these from your actual data if possible, or define them clearly
    # For now, assuming these are types of items that should be URIs
    items_list = ["Article", "Documentary", "Illustration", "Letter", "Manuscript_General", "Manuscript_Hundred", "Nobel_Speech", "Series"]

    #iterate through the dataframe:
    for _, row in df.iterrows():
        
        #get row's subject, predicate and object
        subject = str(row["Subject"]).strip() if pd.notna(row["Subject"]) else None
        predicate = str(row["Predicate"]).strip() if pd.notna(row["Predicate"]) else None
        object = str(row["Object"]).strip() if pd.notna(row["Object"]) else None

        if not subject or not predicate or not object:
            continue # Skip rows with missing subject, predicate, or object

        # create subject uri
        normalized_subject = normalize(subject)
        if normalized_subject not in uris_dict:
            subject_uri = URIRef(item + normalized_subject)
            uris_dict[normalized_subject] = subject_uri   
        else:
            subject_uri = uris_dict[normalized_subject]

        predicate_uri = None # Initialize predicate_uri

        # specify predicates
        if predicate == "rdf:type":
            predicate_uri = RDF.type
        elif predicate in ["owl:SameAs", "owl:sameAs"]:
            predicate_uri = OWL.sameAs
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
        # Add any other predicates that might be missing or custom ones
        else:
            # If a predicate is not explicitly mapped, you might want to log it
            # or treat it as a custom property under your base URI, or simply skip
            # For now, let's assume it could be a property under your base URI
            predicate_uri = URIRef(ggm + normalize(predicate)) 
            # print(f"Warning: Unmapped predicate '{predicate}'. Treating as {predicate_uri}")


        # specify RDF types as objects
        obj = None # Initialize obj

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
            elif predicate == "crm:E57_consist_of":
                obj = CRM.E57_consist_of
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
            else:
                # If the object is an unmapped type, try to make it a generic concept or an item
                normalized_object = normalize(object)
                if normalized_object:
                    obj = URIRef(concept + normalized_object) # Default to concept URI
                else:
                    obj = Literal(object, datatype=XSD.string) # Fallback to string literal

        elif predicate_uri == OWL.sameAs:
            obj = URIRef(object)      

        # Mapping of people, persons and organizations
        elif predicate_uri in [DCTERMS.creator, SCHEMA.director, SCHEMA.recipient, SCHEMA.sender, CRM.P14_carried_out_by, SCHEMA.participant, DCTERMS.references, CRM.P138_represents]:
            normalized_object = normalize(object)
            if normalized_object not in uris_dict:
                # Check if it's an item, otherwise assume person for these predicates
                if object in items_list: # This check might need refinement based on your actual data
                    obj = URIRef(item + normalized_object)
                else:    
                    obj = URIRef(person + normalized_object)
                uris_dict[normalized_object] = obj
            else:
                obj = uris_dict[normalized_object]

        elif predicate_uri == CRM.P107_has_current_or_former_member:
            normalized_object = normalize(object)
            if normalized_object not in uris_dict:
                obj = URIRef(group_of_people + normalized_object)
                uris_dict[normalized_object] = obj
            else:
                obj = uris_dict[normalized_object]         

        elif predicate_uri == SCHEMA.productionCompany:
            normalized_object = normalize(object)
            if normalized_object not in uris_dict:
                obj = URIRef(company + normalized_object)
                uris_dict[normalized_object] = obj
            else:
                obj = uris_dict[normalized_object] 

        elif predicate_uri in [DCTERMS.publisher, CRM.P52_has_current_owner, DCTERMS.isPartOf]:
            normalized_object = normalize(object)
            if normalized_object not in uris_dict:
                obj = URIRef(institution + normalized_object)
                uris_dict[normalized_object] = obj
            else:
                obj = uris_dict[normalized_object]
        
        elif predicate_uri == SCHEMA.hasOccupation:
            normalized_object = normalize(object)
            if normalized_object not in uris_dict:
                obj = URIRef(occupation + normalized_object)
                uris_dict[normalized_object] = obj
            else:
                obj = uris_dict[normalized_object]
        
        # Mapping of places
        elif predicate_uri in [SCHEMA.birthPlace, CRM.P55_has_current_location, SCHEMA.locationCreated, SCHEMA.location, SCHEMA.countryOfOrigin]:
            normalized_object = normalize(object)
            if normalized_object not in uris_dict:
                obj = URIRef(place + normalized_object)
                uris_dict[normalized_object] = obj
            else:
                obj = uris_dict[normalized_object]
        
        # Mapping of events
        elif predicate_uri in [CRM.P67_refers_to, SCHEMA.recordedAt]:
            normalized_object = normalize(object)
            if normalized_object not in uris_dict:
                obj = URIRef(event + normalized_object)
                uris_dict[normalized_object] = obj
            else:
                obj = uris_dict[normalized_object]
        
        # Mapping of periods
        elif predicate_uri == CRM.P10_falls_within:
            normalized_object = normalize(object)
            if normalized_object not in uris_dict:
                obj = URIRef(period + normalized_object)
                uris_dict[normalized_object] = obj
            else:
                obj = uris_dict[normalized_object]
        
        # Mapping of genres
        elif predicate_uri == SCHEMA.genre:
            normalized_object = normalize(object)
            if normalized_object not in uris_dict:
                obj = URIRef(genre_type + normalized_object)
                uris_dict[normalized_object] = obj
            else:
                obj = uris_dict[normalized_object]

        # Mapping of concepts         
        elif predicate_uri == SCHEMA.about:
            normalized_object = normalize(object)
            if normalized_object not in uris_dict:  
                # Consider if 'about' always links to a concept or sometimes an item
                if object in items_list: # This check might need refinement
                    obj = URIRef(item + normalized_object)
                else:
                    obj = URIRef(concept + normalized_object)
                uris_dict[normalized_object] = obj
            else:    
                obj = uris_dict[normalized_object]
        
        elif predicate_uri == DCTERMS.subject:
            normalized_object = normalize(object)
            if normalized_object not in uris_dict:
                if object in items_list: # This check might need refinement
                    obj = URIRef(item + normalized_object)
                else:    
                    obj = URIRef(concept + normalized_object)
                uris_dict[normalized_object] = obj
            else:
                obj = uris_dict[normalized_object]

        # Mapping of books or physical objects
        elif predicate_uri in [CRM.E57_consist_of, CRM.P32_used_general_technique, SCHEMA.isBasedOn]: # DCTERMS.isPartOf already handled for institution
            normalized_object = normalize(object)
            if normalized_object not in uris_dict:
                obj = URIRef(physical_objects + normalized_object) # Corrected typo in variable name here
                uris_dict[normalized_object] = obj
            else:
                obj = uris_dict[normalized_object] 
        
        # Mapping of relations
        elif predicate_uri == DCTERMS.relation:
            normalized_object = normalize(object)
            if normalized_object not in uris_dict:
                if object in items_list:
                    obj = URIRef(item + normalized_object)
                elif object == "Aracataca":
                    obj = URIRef(place + normalized_object)
                elif object == "Gabriel Garcia Marquez":
                    obj = URIRef(person + normalized_object)
                else:
                    obj = URIRef(concept + normalized_object) # Default for other relations
                uris_dict[normalized_object] = obj
            else:
                obj = uris_dict[normalized_object]

        # mapping of dates and years  
        elif predicate_uri == DCTERMS.created:
            parsed_date = parse_date_flexible(object)
            if parsed_date:
                if parsed_date.month == 1 and parsed_date.day == 1: # If only year is present
                    obj = Literal(parsed_date.year, datatype=XSD.gYear)
                else:
                    obj = Literal(parsed_date.strftime('%Y-%m-%d'), datatype=XSD.date)
            else:
                obj = Literal(object, datatype=XSD.string) # Fallback if parsing fails
        
        elif predicate_uri == DCTERMS.issued:
            parsed_date = parse_date_flexible(object)
            if parsed_date:
                if parsed_date.month == 1 and parsed_date.day == 1:
                    obj = Literal(parsed_date.year, datatype=XSD.gYear)
                else:
                    obj = Literal(parsed_date.strftime('%Y-%m-%d'), datatype=XSD.date)
            else:
                obj = Literal(object, datatype=XSD.string) # Fallback if parsing fails
        
        # handle additional literal types
        elif predicate_uri == DCTERMS.language:
            obj = Literal(object, datatype=XSD.language)

        elif predicate_uri == DCTERMS.extent:
            obj = format_duration_for_xsd(object) 

        elif predicate_uri == SCHEMA.duration:
            obj = format_duration_for_xsd(object)

        elif predicate_uri == SCHEMA.numberOfEpisodes:
            try:
                obj = Literal(int(object), datatype=XSD.integer)
            except ValueError:
                obj = Literal(object, datatype=XSD.string) # Fallback if not an integer

        else:
            # Default for any other predicate if not explicitly handled and obj is still None
            if obj is None:
                obj = Literal(object, datatype=XSD.string)

        #add triple to graph if obj is not None
        if obj is not None and predicate_uri is not None:
            g.add((subject_uri, predicate_uri, obj))

#serialize the graph to Turtle format
# Ensure the base URI is properly handled in serialization, often it's done by binding
turtle_str = g.serialize(format="turtle", base=ggm, encoding="utf-8") # Removed base=ggm as it's bound

#write the Turtle string to a file
with open("output_rdf_serialization.ttl", "wb") as f:
    f.write(turtle_str)

print("RDF data generated and saved to output_rdf_visualization.ttl")