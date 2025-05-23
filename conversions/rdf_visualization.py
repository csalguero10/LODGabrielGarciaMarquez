# Cargar RDF y construir grafo interactivo con Pyvis
from importlib.metadata import files
import rdflib
from pyvis.network import Network

ttl_file = "conversions/output_rdf_serialization.ttl"

g = rdflib.Graph()
g.parse(ttl_file, format="turtle")

# Crear grafo interactivo
net = Network(height="800px", width="100%", directed=True)
net.barnes_hut(gravity=-30000, central_gravity=0.5, spring_length=350, spring_strength=0.05, damping=0.8)

# Añadir nodos y aristas con flechas más visibles
for subj, pred, obj in g:
    subj_str = str(subj)
    obj_str = str(obj)
    pred_str = str(pred)
    net.add_node(subj_str, label=subj_str)
    net.add_node(obj_str, label=obj_str)
    net.add_edge(subj_str, obj_str, title=pred_str, label=pred_str, arrows="to", width=1.5)

# Paso 4: Guardar como HTML (funciona mejor en Colab)
output_file = "conversions/rdf_graph.html"
net.write_html(output_file)

# El archivo HTML ha sido creado en el directorio actual.
print(f"Archivo HTML creado: {output_file}")
# ...existing code...