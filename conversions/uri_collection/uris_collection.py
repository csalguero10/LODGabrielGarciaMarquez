import rdflib

# Load the graph
g = rdflib.Graph()
g.parse("conversions/output_rdf_serialization.ttl", format="turtle")

# Define your base namespace
base_ns = "https://w3id.org/GGM/"

# Collect unique entity URIs from the subject positions that start with base namespace
entity_uris = sorted({str(s) for s in g.subjects() if str(s).startswith(base_ns)})

# Write to file
with open("conversions/ggm_entity_uris.txt", "w") as f:
    for uri in entity_uris:
        f.write(uri + "\n")
