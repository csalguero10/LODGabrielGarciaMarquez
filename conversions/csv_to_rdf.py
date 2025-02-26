
import rdflib
from rdflib import Namespace, URIRef, Literal
from rdflib.namespace import RDF, OWL, DC, DCTERMS, XSD, FOAF, SKOS, RDFS
import pandas as pd

#Namespaces
SCHEMA = Namespace("https://schema.org/")
CRM = Namespace("https://www.cidoc-crm.org/")
FRBRER = Namespace("http://iflastandards.info/ns/fr/frbr/frbrer/")

#creating a rdf graph
g = rdflib.Graph()

#base_uri
ggm = URIRef("https://w3id.org/PoorThings.org/") 

#creating uris
item = URIRef(ggm + "item/")
person = URIRef(ggm + "person/")
organization = URIRef(ggm + "organization/")
place = URIRef(ggm + "place/")
concept = URIRef(ggm + "concept/")
periodical = URIRef(ggm + "periodical/")
event = URIRef(ggm + "event/")
#bind namespaces to graph
g.bind("schema", SCHEMA)
g.bind("crm", CRM)

#list of csv files
files_csv = ["csv files/poor_things_movie.csv", "csv files/activity.csv", "csv files/article.csv", "csv files/bio_ent_char.csv", "csv files/bio_ent_person.csv", "csv files/movie.csv", "csv files/monument.csv", "csv files/book.csv", "csv files/painting.csv", "csv files/portrait.csv", "csv files/soundtrack.csv"]

#for loop that iterates all the csv files and add data to the same graph
for file in files_csv:

    #create a pandas dataframe to read csv 
    df = pd.read_csv(file)   
    
    #dict to store uris
    uris_dict = dict()

    items_list = ["Image", "Interview", "Letter", "Illustration", "Manuscript Cien Anos", "Documentary", "Nobel Speech", "Play", "Article", "Manuscript General", "Gabriel Garcia Marquez"]
 
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
                                                                   
        #specify predicates

        """elif predicate == "dcterms:isReferencedBy":
                predicate_uri = DCTERMS.isReferencedBy"""

        if predicate == "rdf:type":
            predicate_uri = RDF.type

        elif predicate== "owl:sameAs":
            predicate_uri = OWL.sameAs 
        
        elif predicate == "dcterms:publisher": #ok
            predicate_uri = DCTERMS.publisher
        
        elif predicate == "dcterms:contributor":  #ok
            predicate_uri = DCTERMS.contributor

        elif predicate == "dcterms:creator":  #ok
            predicate_uri = DCTERMS.creator   

        elif predicate == "dcterms:title": #ok
            predicate_uri = DCTERMS.title
            
        elif predicate == "dcterms:subject": #ok
            predicate_uri = DCTERMS.subject     
        
        elif predicate == "dcterms:medium": #ok
            predicate_uri = DCTERMS.medium     

        elif predicate == "dcterms:language": #ok
            predicate_uri = DCTERMS.language  

        elif predicate == "dcterms:description": #ok
            predicate_uri = DCTERMS.description     

        elif predicate == "dcterms:extent": #ok
            predicate_uri = DCTERMS.extent

        elif predicate == "dcterms:format": #ok
            predicate_uri = DCTERMS.format

        elif predicate == "dcterms:isPartOf": #ok
            predicate_uri = DCTERMS.isPartOf

        elif predicate == "dcterms:references": #ok
            predicate_uri = DCTERMS.references     
     
        elif predicate == "dcterms:created": #ok
            predicate_uri = DCTERMS.created  

        elif predicate == "dcterms:issued": #ok
            predicate_uri = DCTERMS.issued  

        elif predicate == "dcterms:date": # ok
            predicate_uri = DCTERMS.date  
        
        elif predicate == "dcterms:relation": # ok
            predicate_uri = DCTERMS.relation  
        
        elif predicate == "foaf:Person":  #ok
            predicate_uri = FOAF.Person

        elif predicate == "schema:director":  #ok
            predicate_uri = SCHEMA.director
        
        elif predicate == "schema:sender":  #ok
            predicate_uri = SCHEMA.sender

        elif predicate == "schema:recipient":  #ok
            predicate_uri = SCHEMA.recipient

        elif predicate == "schema:alternateName": #ok
            predicate_uri = SCHEMA.alternateName    

        elif predicate == "schema:material": #ok
            predicate_uri = SCHEMA.material  

        elif predicate == "schema:genre": #ok
            predicate_uri = SCHEMA.genre  

        elif predicate == "schema:Duration": #ok
            predicate_uri = SCHEMA.Duration
        
        elif predicate == "schema:recordedAt": #ok
            predicate_uri = SCHEMA.recordedAt        

        elif predicate == "schema:bookEdition": #ok
            predicate_uri = SCHEMA.bookEdition

        elif predicate == "schema:hasOccupation": #ok
            predicate_uri = SCHEMA.hasOccupation

        elif predicate == "schema:birthDate": #ok
            predicate_uri = SCHEMA.birthDate    

        elif predicate == "schema:countryOfOrigin": #ok
            predicate_uri = SCHEMA.countryOfOrigin   

        elif predicate == "schema:locationCreated": #ok
            predicate_uri = SCHEMA.locationCreated         

        elif predicate == "crm:P94_has_created": #ok
            predicate_uri = CRM.P94_has_created

        elif predicate == "crm:P2_has_type": #ok
            predicate_uri = CRM.P2_has_type   

        elif predicate == "crm:P102_has_title": #ok
            predicate_uri = CRM.P102_has_title    

        elif predicate == "crm:P138_represents": #ok
            predicate_uri = CRM.represents    

        elif predicate == "crm:P129_is_about":  #ok
            predicate_uri = CRM.P129_is_about       

        elif predicate == "crm:P52_has_current_current": #ok
            predicate_uri = CRM.P52_has_current_current

        elif predicate == "crm:P55_has_current_location": #ok
            predicate_uri = CRM.P55_has_current_location 

        elif predicate == "crm:P7_took_place_at": #ok
            predicate_uri = CRM.P7_took_place_at


        #specify if objects are uris or literals
        if predicate_uri == RDF.type:
            if object == "schema:image":
                obj = SCHEMA.image
            elif object == "schema:Place":
                obj = SCHEMA.Place  
            elif object == "schema:Article":
                obj = SCHEMA.Article
            elif object == "schema:Periodical":
                obj = SCHEMA.Periodical  
            elif object == "schema:VisualArtwork":
                obj = SCHEMA.VisualArtwork   
            elif object == "schema:Manuscript":
                obj = SCHEMA.Manuscript
            elif object == "schema:Book":
                obj = SCHEMA.Book
            elif object == "crm:E73_Information_Object":
                obj = CRM.E73_Information_Object
            elif object == "crm:E78_Curated_Holding":
                obj = CRM.E78_Curated_Holding 
            elif object == "crm:E22_Human_Made_Object":
                obj = CRM.E22_Human_Made_Object
            elif object == "crm:E29_Design_Or_Procedure":
                obj = CRM.E29_Design_Or_Procedure
            elif object == "crm:E74_Group":
                obj = CRM.E74_Group
            elif object == "crm:E5_Event":
                obj = CRM.E5_Event
            elif object == "crm:E4_Period":
                obj = CRM.E4_Period
            elif object == "dcterms:Text":
                obj = DCTERMS.Text
            elif object == "skos:Concept":
                obj = SKOS.Concept
            elif object == "foaf:Person":
                obj = FOAF.Person
            elif object == "frbrer:Character":
                obj = FRBRER.Character
            
        elif predicate_uri == OWL.sameAs:
            obj = URIRef(object)


            #DA QUI --> modificano i collegamenti diretti tra gli item e quelli tra item e item centrale

            #property dirette a GGM: DCTERMS.relation DCTERMS.subject SCHEMA.sender DCTERMS.creator DCTERMS.references    

        elif predicate_uri == DCTERMS.relation:
            if object not in uris_dict:
                if object in items_list:
                    obj = URIRef(item + object.replace(" ", "_"))
                    uris_dict[object] = obj
                elif object == "Colombian Armed Conflict":
                    obj = URIRef(concept + object.replace(" ", "_"))
                    uris_dict[object] = obj
            else:
                obj = uris_dict[object]

        elif predicate_uri == DCTERMS.sender:
            if object not in uris_dict:
                object = uris_dict[object]           
        
        elif predicate_uri == DCTERMS.references:
            if object not in uris_dict:
                group_of_concepts = ["Magic Realism", "Social Criticism", "Politics"]
                #hanno property references: "Aracataca", "Bananas Massacre", 
                if object in items_list:
                    obj = URIRef(item + object.replace(" ", "_"))
                    uris_dict[object] = obj
                elif object in group_of_concepts:
                    obj = URIRef(concept + object.replace(" ", "_"))
                    uris_dict[object] = obj
                elif object == "Aracataca":
                    obj = URIRef(place + object.replace(" ", "_"))
                    uris_dict[object] = obj
                elif object == "Bananas Massacre":
                    obj = URIRef(event + object.replace(" ", "_"))
                    uris_dict[object] = obj
            else:
                obj = uris_dict[object]
        
        elif predicate_uri == DCTERMS.subject:
            if object not in uris_dict:
                if object in items_list:
                    obj = URIRef(item + object.replace(" ", "_"))
                    uris_dict[object] = obj
                elif object == "Colombian Armed Conflict":
                    obj = URIRef(concept + object.replace(" ", "_"))
                    uris_dict[object] = obj
            else:
                obj = uris_dict[object]
        
        
        
        
        
        elif predicate_uri == CDWA.Commissioner or predicate_uri == CRM.P14_carried_out_by:
            if object not in uris_dict:
                obj = URIRef(person + object.replace(" ", "_"))
                uris_dict[object] = obj
            else:
                obj = uris_dict[object]    

        elif predicate_uri == FOAF.member:
            if object not in uris_dict:
                groups_list = ["Greek Weird Wave", "Ptolemaic dinasty", "Young upper-class men"]
                if object in groups_list:
                    obj = URIRef(group_of_people + object.replace(" ", "_"))
                    uris_dict[object] = obj
                else:
                    obj = URIRef(person + object.replace(" ", "_"))
                    uris_dict[object] = obj    
            else:
                obj = uris_dict[object] 
         
        elif predicate_uri == SCHEMA.agent:
            if object not in uris_dict:
                if object in items_list:
                    obj = URIRef(item + object.replace(" ", "_"))
                    uris_dict[object] = obj
                else:
                    obj = URIRef(group_of_people + object.replace(" ", "_"))
                    uris_dict[object] = obj
            else:
                obj = uris_dict[object]                    

        elif predicate_uri == DC.publisher or predicate_uri == SCHEMA.copyrightHolder:
            if object not in uris_dict:
                obj = URIRef(organization + object.replace(" ", "_"))
                uris_dict[object] = obj
            else:
                obj = uris_dict[object]      

        elif predicate_uri == DCTERMS.spatial or predicate_uri == CRM.P55_has_current_location or predicate_uri == SCHEMA.containedInPlace or predicate_uri == SCHEMA.containsPlace or predicate_uri == SCHEMA.birthPlace:    
            if object not in uris_dict:
                obj = URIRef(place + object.replace(" ", "_"))
                uris_dict[object] = obj
            else:
                obj = uris_dict[object]    

        elif predicate_uri == DCTERMS.isPartOf:
            if object not in uris_dict:
                obj = URIRef(group_of_objects + object.replace(" ", "_"))
                uris_dict[object] = obj
            else:
                obj = uris_dict[object]          

        elif predicate_uri == CRM.P21_had_general_purpose:
            if object not in uris_dict:
                obj = URIRef(concept + object.replace(" ", "_"))
                uris_dict[object] = obj
            else:
                obj = uris_dict[object]    

        elif predicate_uri == MO.published_as:
            if object not in uris_dict:
                obj = URIRef(song + object.replace(" ", "_"))
                uris_dict[object] = obj   
            else:
                obj = uris_dict[object]

        elif predicate_uri == SCHEMA.parent:
            if object not in uris_dict:
                obj = URIRef(conceptual_object + object.replace(" ", "_"))
                uris_dict[object] = obj  
            else:
                obj = uris_dict[object]        
# our literals 
        elif predicate_uri == DCTERMS.created:
                obj = Literal(object, datatype=XSD.gYear)
                
        
        elif predicate_uri == DCTERMS.issued:
            if object not in uris_dict:
                if "-" in object:
                    obj = Literal(object, datatype=XSD.date) 
                else:
                    obj = Literal(object, datatype=XSD.gYear)     
            else:
                obj = uris_dict[object]    

        elif predicate_uri == SCHEMA.duration:
             obj = Literal(object, datatype=XSD.duration)     

        elif predicate_uri == DCTERMS.extent:
             obj = Literal(object, datatype=XSD.string) 

        elif predicate_uri == SCHEMA.genre:
             obj = Literal(object, datatype=XSD.string)   

        elif predicate_uri == DCTERMS.language:
            obj = Literal(object, datatype=XSD.language) 

        elif predicate_uri == SCHEMA.edition:
            obj = Literal(object, datatype=XSD.string)

# end of our literals

        elif predicate_uri == SCHEMA.startDate or predicate_uri == SCHEMA.endDate or predicate_uri == CRM.P82a_begin_of_the_begin or predicate_uri == CRM.P82b_end_of_the_end or predicate_uri == SCHEMA.birthDate or predicate_uri == DBP.yeardeactivated:
            obj = Literal(object, datatype=XSD.gYear)

        elif predicate_uri == DCTERMS.extent:
             obj = Literal(object, datatype=XSD.dayTimeDuration)    

        elif predicate_uri == SCHEMA.inLanguage:
            obj = Literal(object, datatype=XSD.language)    

        else:
            obj = Literal(object, datatype=XSD.string)      

        #add triple to graph
        g.add((subject_uri, predicate_uri, obj))

#serialize the graph to Turtle format
turtle_str = g.serialize(format="turtle", base=pt, encoding="utf-8")

#write the Turtle string to a file
with open("output_rdf_visualization.ttl", "wb") as f:
    f.write(turtle_str)
  