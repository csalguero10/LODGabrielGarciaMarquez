from lxml import etree
import os

# Define the absolute paths for the XML and XSLT files
base_path = os.path.dirname(os.path.abspath(__file__))
xml_path = os.path.join(base_path, "tei.xml")
xslt_path = os.path.join(base_path, "html.xslt")

# Load XML input and XSLT stylesheet
xml_doc = etree.parse(xml_path)
xslt_doc = etree.parse(xslt_path)

# Create an XSLT transformer
transform = etree.XSLT(xslt_doc)

# Apply the transformation
result_tree = transform(xml_doc)

# Add language attribute to the <html> tag in the result
html_element = result_tree.getroot()
html_element.attrib['lang'] = 'es'

# Add the viewport meta tag
head_element = result_tree.find(".//head")
if head_element is not None:
    meta_viewport = etree.Element("meta", name="viewport", content="width=device-width, initial-scale=1.0")
    head_element.insert(0, meta_viewport)  # Insert it as the first child of <head>

# Output the transformed HTML to a new file
with open(os.path.join(base_path, "index.html"), "wb") as f:
    f.write(etree.tostring(result_tree, pretty_print=True))
